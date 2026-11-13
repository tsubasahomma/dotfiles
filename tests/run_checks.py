#!/usr/bin/env python3
"""Run source checks with existing binaries, a clean environment and no skips.

Targets are suites or test modules (test_git_fetch, test_git_fetch.Class.test).
Each module runs in its own isolated child with a temporary HOME, in parallel.
The fast layer is every test that does not apply; there chezmoi refuses apply.
No installs here: each binary comes from NAME_BIN, then PATH, then the mise
install of the version this repository declares. CI's tool setup supplies the
same prerequisites.
"""

# Keep this file parseable by older Python 3 so it can re-launch itself on 3.11+.
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

TESTS = Path(__file__).resolve().parent
REPO = TESTS.parent
# Every module of the fast and slow layers. test_lint has its own suite and
# test_vale_lint needs prepared plugin checkouts, so both stay outside.
MODULES = [
    'test_render_syntax',
    'test_repo_rules',
    'test_ci_changes',
    'test_mise_read_boundary',
    'test_identity_boundary',
    'test_identity_transaction',
    'test_identity_convergence',
    'test_ownership_boundary',
    'test_completion_transaction',
    'test_completion_convergence',
    'test_git_fetch',
    'test_diagnostic_boundary',
    'test_generated_convergence',
    'test_windows_packages',
    'test_windows_config_sync',
    'test_homebrew_packages',
    'test_first_install_order',
    'test_lazy_lock_update',
    'test_lazy_restore',
    'test_ci_verify',
    'test_shell_startup',
    'test_mason_log',
]
# The slow layer: tests that run chezmoi apply (also --dry-run or init --apply) on a
# reduced source. None means the whole module. Every other test is fast, and the
# fast layer runs with a chezmoi that refuses those commands, so a test that
# starts to apply fails there until it is listed here.
SLOW = {
    'test_ci_verify': None,
    'test_completion_convergence': None,
    'test_first_install_order': None,
    'test_generated_convergence': None,
    'test_identity_convergence': None,
    'test_identity_transaction': [
        'Transaction.test_r05_before_failure_prevents_target_change_and_retry'
    ],
    'test_ownership_boundary': [
        'OwnershipBoundary.test_owned_source_modes_still_apply',
        'OwnershipBoundary.test_retired_files_and_manual_docker_install',
        'OwnershipBoundary.test_retired_names_replaced_by_nested_directories',
        'OwnershipBoundary.test_retired_names_replaced_by_symlinks',
    ],
    'test_windows_config_sync': None,
}
SUITES = {
    'fast': [(module, 'fast') for module in MODULES],
    'slow': [(module, 'slow') for module in MODULES if module in SLOW],
    'lint': [('test_lint', 'all')],
    'full': [('test_lint', 'all')]
    + [(module, layer) for module in MODULES for layer in ('fast', 'slow')],
}
# Pins used when PATH has no real binary or only a mise shim:
# name -> (manifest, mise tool key, executable).
MANIFEST_TOOLS = {
    'chezmoi': ('.mise.toml', 'aqua:twpayne/chezmoi', 'chezmoi'),
    'nvim': ('dot_config/mise/conf.d/10-tools.toml', 'aqua:neovim/neovim', 'nvim'),
    'python3': ('dot_config/mise/conf.d/10-tools.toml', 'python', 'python3'),
    'vale': ('dot_config/mise/conf.d/10-tools.toml', 'aqua:errata-ai/vale', 'vale'),
    'stylua': ('dot_config/mise/conf.d/10-tools.toml', 'aqua:JohnnyMorganz/StyLua', 'stylua'),
    'shellcheck': (
        'dot_config/mise/conf.d/10-tools.toml',
        'aqua:koalaman/shellcheck',
        'shellcheck',
    ),
    'shfmt': ('dot_config/mise/conf.d/10-tools.toml', 'aqua:mvdan/sh', 'shfmt'),
    'ruff': ('tests/lint-tools.toml', 'aqua:astral-sh/ruff', 'ruff'),
    'zizmor': ('tests/lint-tools.toml', 'aqua:zizmorcore/zizmor', 'zizmor'),
    'actionlint': ('tests/lint-tools.toml', 'aqua:rhysd/actionlint', 'actionlint'),
}
BASE_TOOLS = ['chezmoi', 'nvim', 'zsh', 'git', 'ssh', 'ssh-keygen']
# Modules that run without mise; every other module gets the pinned mise.
WITHOUT_MISE = {'test_render_syntax', 'test_lint', 'test_repo_rules', 'test_ci_changes'}
# Modules that need more tools, and variables they may read.
# Modules that need only these tools instead of BASE_TOOLS (no Neovim or Zsh).
OWN_TOOLS = {
    'test_repo_rules': ['git'],
    'test_ci_changes': ['git'],
    'test_lint': [
        'chezmoi',
        'git',
        'ruff',
        'stylua',
        'shfmt',
        'shellcheck',
        'actionlint',
        'zizmor',
    ],
}
EXTRA_TOOLS = {
    'test_vale_lint': ['vale'],
}
PASSTHROUGH = {'test_vale_lint': ['NVIM_LINT_DIR', 'LAZYVIM_DIR']}


def env_name(name):
    return name.upper().replace('-', '_') + '_BIN'


def is_shim(path):
    return 'shims' in Path(path).absolute().parts


def mise_data_dir():
    value = os.environ.get('MISE_DATA_DIR')
    return Path(value) if value else Path.home() / '.local/share/mise'


def declared_version(manifest, key):
    text = (REPO / manifest).read_text()
    quoted = '"' + key + '"' if ':' in key else key
    matches = re.findall(r'^' + re.escape(quoted) + r' = "v?([0-9][0-9.]*)"$', text, re.M)
    if len(matches) != 1:
        raise LookupError(f'{manifest} must declare exactly one {key} version')
    return matches[0]


def install_dir_names(key):
    # mise stores "aqua:JohnnyMorganz/StyLua" as "aqua-johnny-morganz-sty-lua".
    kebab = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '-', key)
    return sorted({re.sub(r'[:/]', '-', value).lower() for value in (key, kebab)})


def find_installed(name):
    """Return the mise-installed binary of the declared version, or None."""
    if name == 'mise':
        candidate = Path.home() / '.local/bin/mise'
        return candidate if candidate.is_file() and os.access(candidate, os.X_OK) else None
    if name not in MANIFEST_TOOLS:
        return None
    manifest, key, executable = MANIFEST_TOOLS[name]
    version = declared_version(manifest, key)
    for directory in install_dir_names(key):
        root = mise_data_dir() / 'installs' / directory / version
        if not root.is_dir():
            continue
        matches = sorted(
            (p for p in root.rglob(executable) if p.is_file() and os.access(p, os.X_OK)),
            key=lambda p: (p.parent.name != 'bin', len(p.parts)),
        )
        if matches:
            return matches[0]
    return None


def mise_version(path):
    """Read a mise binary's version without user config, tasks or update checks."""
    with tempfile.TemporaryDirectory(prefix='run-checks-mise-') as home:
        result = subprocess.run(
            [str(path), '--version'],
            capture_output=True,
            text=True,
            timeout=30,
            env={
                'HOME': home,
                'PATH': '/usr/bin:/bin',
                'MISE_NO_CONFIG': '1',
                'MISE_LOG_LEVEL': 'error',
            },
        )
    words = result.stdout.split()
    return words[0] if result.returncode == 0 and words else None


def resolve(name):
    """Resolve an existing executable without installing anything."""
    variable = env_name(name)
    if os.environ.get(variable):
        path = Path(os.environ[variable]).absolute()
        if is_shim(path) or not path.is_file() or not os.access(path, os.X_OK):
            raise LookupError(f'{variable} must name an executable binary, not a shim: {path}')
        path, origin = path.resolve(), variable
    else:
        found = shutil.which(name)
        installed = None if found and not is_shim(found) else find_installed(name)
        if found and not is_shim(found):
            path, origin = Path(found).absolute().resolve(), 'PATH'
        elif installed:
            path, origin = installed.resolve(), 'mise install'
        else:
            hint = f'set {variable}'
            if name in MANIFEST_TOOLS:
                manifest, key, _ = MANIFEST_TOOLS[name]
                hint += (
                    f' or install {key} {declared_version(manifest, key)} declared in {manifest}'
                )
            state = 'only a shim on PATH' if found else 'not found'
            raise LookupError(f'{name} is required ({state}); {hint}')
    if name == 'mise':
        # The diagnostics compare the hermetic mise with this pin.
        expected = (REPO / '.mise-version').read_text().strip()
        actual = mise_version(path)
        if actual != expected:
            raise LookupError(
                f'mise {expected} from .mise-version is required, but {path} reports '
                f'{actual or "no version"}; set MISE_BIN to a {expected} binary'
            )
    return path, origin


def ensure_python():
    """Re-launch on the declared Python when started by an older interpreter."""
    if sys.version_info >= (3, 11):
        return
    installed = None if os.environ.get('RUN_CHECKS_REEXEC') else find_installed('python3')
    if not installed:
        sys.exit(
            'Python 3.11+ is required (tomllib); run with python3.11+ or install the '
            'python version declared in dot_config/mise/conf.d/10-tools.toml'
        )
    os.environ['RUN_CHECKS_REEXEC'] = '1'
    os.execv(str(installed), [str(installed), str(Path(__file__).resolve())] + sys.argv[1:])


def known_modules():
    return sorted(p.stem for p in TESTS.glob('test_*.py'))


def unit_for(module, layer):
    """Return (label, names, excluded test ids, guard) for one child, or None if empty."""
    slow = SLOW.get(module, ())
    if layer == 'fast':
        if slow is None:
            return None
        return (
            f'{module} (fast)' if module in SLOW else module,
            [module],
            [f'{module}.{name}' for name in slow],
            True,
        )
    if layer == 'slow':
        names = [module] if slow is None else [f'{module}.{name}' for name in slow]
        return (f'{module} (slow)' if slow else module, names, [], False) if names else None
    return module, [module], [], False


def expand(targets, parser):
    """Turn suite and module targets into a de-duplicated list of child units."""
    units, modules = [], set(known_modules())
    explicit = {}
    for target in targets:
        if target.endswith('.py'):
            target = Path(target).stem
        if target in SUITES:
            selected = [unit_for(module, layer) for module, layer in SUITES[target]]
        elif target.split('.')[0] in modules:
            explicit.setdefault(target.split('.')[0], []).append(target)
            continue
        else:
            parser.error(
                f'unknown target {target!r}; use a suite ({", ".join(SUITES)}) '
                f'or a module: {", ".join(sorted(modules))}'
            )
        units += [unit for unit in selected if unit and unit not in units]
    for module, names in explicit.items():
        # A whole module wins over single tests of the same module.
        unit = (module, [module] if module in names else names, [], False)
        if unit not in units:
            units.append(unit)
    return units


class TimedResult(unittest.TextTestResult):
    seconds = {}

    def startTest(self, test):
        self._started = time.monotonic()
        super().startTest(test)

    def stopTest(self, test):
        TimedResult.seconds[test.id()] = time.monotonic() - self._started
        super().stopTest(test)


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run_child(names, excluded, report):
    """Inside the isolated child: run the names and write a JSON report."""
    loaded = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(names)))
    missing = [name for name in excluded if name not in {test.id() for test in loaded}]
    tests = unittest.TestSuite(test for test in loaded if test.id() not in excluded)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2, resultclass=TimedResult).run(
        tests
    )
    if missing:
        print('Listed in SLOW but not found: ' + ', '.join(missing))
    Path(report).write_text(
        json.dumps(
            {
                'run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(result.skipped),
                'expected_failures': len(result.expectedFailures),
                'unexpected_successes': len(result.unexpectedSuccesses),
                'seconds': TimedResult.seconds,
            }
        )
    )
    return 0 if result.wasSuccessful() and not missing else 1


GUARD = """#!/bin/sh
# Fast layer: apply belongs to the slow layer in tests/run_checks.py (SLOW).
for argument in "$@"; do
  case "$argument" in
    apply | --apply | update)
      echo "run_checks fast layer: chezmoi $argument is refused; list this test in SLOW" >&2
      exit 97 ;;
  esac
done
exec {chezmoi} "$@"
"""


def isolated_env(root, binaries, module, guard):
    home = root / 'home'
    home.mkdir()
    bin_dir = root / 'bin'
    bin_dir.mkdir()
    binaries = dict(binaries)
    if guard:
        wrapper = root / 'guard' / 'chezmoi'
        wrapper.parent.mkdir()
        wrapper.write_text(GUARD.replace('{chezmoi}', shlex.quote(binaries['chezmoi'])))
        wrapper.chmod(0o755)
        binaries['chezmoi'] = str(wrapper)
    for name, path in dict(binaries, python3=sys.executable).items():
        (bin_dir / name).symlink_to(path)
    env = {
        'HOME': str(home),
        'PATH': f'{bin_dir}:/usr/bin:/bin:/usr/sbin:/sbin',
        'TMPDIR': str(root),
        'LC_ALL': 'C',
        'PYTHONDONTWRITEBYTECODE': '1',
        'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_GLOBAL': str(home / '.gitconfig'),
        'GIT_TERMINAL_PROMPT': '0',
    }
    for key, part in [
        ('CONFIG', '.config'),
        ('DATA', '.local/share'),
        ('CACHE', '.cache'),
        ('STATE', '.local/state'),
    ]:
        env[f'XDG_{key}_HOME'] = str(home / part)
    for name, path in binaries.items():
        env[env_name(name)] = path
    for variable in PASSTHROUGH.get(module, []):
        if os.environ.get(variable):
            env[variable] = os.environ[variable]
    # No OP_*, SSH agent, Git overrides, mise settings, tokens or user PATH.
    return env


def run_unit(unit, binaries):
    """Run one unit in a fresh temporary root; return (label, code, output, report, secs)."""
    label, names, excluded, guard = unit
    module = names[0].split('.')[0]
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f'dotfiles-checks-{module}-') as temporary:
        root = Path(temporary).resolve()
        report = root / 'report.json'
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            '--isolated-child',
            '--report',
            str(report),
        ]
        for name in excluded:
            command += ['--exclude', name]
        result = subprocess.run(
            command + names,
            cwd=root,
            env=isolated_env(root, binaries, module, guard),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        data = json.loads(report.read_text()) if report.is_file() else None
    return label, result.returncode, result.stdout, data, time.monotonic() - started


def main():
    ensure_python()
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'targets', nargs='+', metavar='target', help=f'suite ({", ".join(SUITES)}) or test module'
    )
    parser.add_argument(
        '-j',
        '--jobs',
        type=int,
        default=max(2, os.cpu_count() or 2),
        help='modules to run at once (default: CPU count)',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='print the output of passing modules too'
    )
    parser.add_argument('--isolated-child', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--report', help=argparse.SUPPRESS)
    parser.add_argument('--exclude', action='append', default=[], help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.isolated_child:
        return run_child(args.targets, args.exclude, args.report)
    started = time.monotonic()
    units = expand(args.targets, parser)
    modules = {unit[1][0].split('.')[0] for unit in units}
    names = [] if modules <= set(OWN_TOOLS) else list(BASE_TOOLS)
    if modules - WITHOUT_MISE:
        names.append('mise')
    for module in sorted(modules):
        names += [
            tool for tool in OWN_TOOLS.get(module, EXTRA_TOOLS.get(module, [])) if tool not in names
        ]
    binaries = {}
    for name in names:
        try:
            path, origin = resolve(name)
        except LookupError as error:
            parser.error(str(error))
        binaries[name] = str(path)
        print(f'{name}: {path} ({origin})', flush=True)
    print(
        f'Running {len(units)} unit(s) from {len(modules)} module(s), {args.jobs} at a time',
        flush=True,
    )
    failed, counts, slowest = [], {'run': 0, 'skipped': 0}, []
    # Longest modules first keeps the wall time near the slowest single module.
    order = sorted(
        units,
        key=lambda unit: (
            SLOW_FIRST.index(unit[1][0].split('.')[0])
            if unit[1][0].split('.')[0] in SLOW_FIRST
            else len(SLOW_FIRST)
        ),
    )
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(run_unit, unit, binaries) for unit in order]
        for future in as_completed(futures):
            module, code, output, data, seconds = future.result()
            ok = (
                code == 0
                and data
                and data['run']
                and not (
                    data['skipped'] or data['expected_failures'] or data['unexpected_successes']
                )
            )
            if data:
                counts['run'] += data['run']
                counts['skipped'] += data['skipped'] + data['expected_failures']
                slowest += list(data['seconds'].items())
            tests = data['run'] if data else '?'
            print(
                f'{"ok  " if ok else "FAIL"} {module}: {tests} tests in {seconds:.1f}s', flush=True
            )
            if not ok:
                failed.append(module)
            if args.verbose or not ok:
                print(output, flush=True)
    print('\nSlowest tests (seconds):')
    for name, seconds in sorted(slowest, key=lambda item: -item[1])[:10]:
        print(f'  {seconds:6.1f}  {name}')
    elapsed = time.monotonic() - started
    if counts['skipped']:
        print('NOT PASSED: skipped or expected-failure tests are not evidence.')
    status = 'passed' if not failed and not counts['skipped'] else 'FAILED'
    print(
        f'{" ".join(args.targets)}: {status}, {counts["run"]} tests, {len(units)} units, '
        f'{elapsed:.1f}s wall' + (f'; failed: {", ".join(failed)}' if failed else '')
    )
    return 0 if status == 'passed' else 1


# Started first so they do not extend the wall time at the end of the queue.
SLOW_FIRST = [
    'test_completion_convergence',
    'test_generated_convergence',
    'test_windows_config_sync',
    'test_identity_convergence',
    'test_identity_transaction',
    'test_completion_transaction',
    'test_diagnostic_boundary',
    'test_identity_boundary',
    'test_lazy_lock_update',
]

if __name__ == '__main__':
    sys.exit(main())

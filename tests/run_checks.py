#!/usr/bin/env python3
"""Run source checks with existing binaries, a clean environment and no skips.

Targets are suites or test modules (test_git_fetch, test_git_fetch.Class.test).
Each module runs in its own isolated child with a temporary HOME, in parallel.
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
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

TESTS = Path(__file__).resolve().parent
REPO = TESTS.parent
REGRESSION = [
    'test_mise_read_boundary', 'test_identity_boundary', 'test_identity_transaction',
    'test_identity_convergence', 'test_ownership_boundary', 'test_completion_transaction', 'test_completion_convergence', 'test_git_fetch',
    'test_diagnostic_boundary', 'test_generated_convergence', 'test_windows_packages', 'test_windows_config_sync', 'test_homebrew_packages',
    'test_first_install_order', 'test_lazy_lock_update', 'test_lazy_restore', 'test_ci_verify',
    'test_shell_startup', 'test_mason_log',
]
# Modules with no chezmoi apply, not even --dry-run, on any fixture.
FAST = [
    'test_render_syntax', 'test_mise_read_boundary', 'test_identity_boundary',
    'test_completion_transaction', 'test_git_fetch', 'test_diagnostic_boundary',
    'test_windows_packages', 'test_homebrew_packages', 'test_lazy_lock_update',
    'test_lazy_restore', 'test_shell_startup', 'test_mason_log',
]
SUITES = {
    'fast': FAST,
    'full': ['test_render_syntax'] + REGRESSION,
    # Kept until CI and the documents move to the suites above.
    'render': ['test_render_syntax'],
    'regression': REGRESSION,
}
# Pins used when PATH has no real binary or only a mise shim:
# name -> (manifest, mise tool key, executable).
MANIFEST_TOOLS = {
    'chezmoi': ('.mise.toml', 'aqua:twpayne/chezmoi', 'chezmoi'),
    'nvim': ('dot_config/mise/conf.d/10-tools.toml', 'aqua:neovim/neovim', 'nvim'),
    'python3': ('dot_config/mise/conf.d/10-tools.toml', 'python', 'python3'),
    'vale': ('dot_config/mise/conf.d/10-tools.toml', 'aqua:errata-ai/vale', 'vale'),
}
BASE_TOOLS = ['chezmoi', 'nvim', 'zsh', 'git', 'ssh', 'ssh-keygen']
# Modules that run without mise; every other module gets the pinned mise.
WITHOUT_MISE = {'test_render_syntax'}
# Modules that need more tools, and variables they may read.
EXTRA_TOOLS = {'test_vale_lint': ['vale']}
PASSTHROUGH = {'test_vale_lint': ['NVIM_LINT_DIR', 'LAZYVIM_DIR']}
# Modules outside the suites: they need prepared plugin checkouts.
STANDALONE = ['test_vale_lint']


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
        matches = sorted((p for p in root.rglob(executable) if p.is_file() and os.access(p, os.X_OK)),
                         key=lambda p: (p.parent.name != 'bin', len(p.parts)))
        if matches:
            return matches[0]
    return None


def mise_version(path):
    """Read a mise binary's version without user config, tasks or update checks."""
    with tempfile.TemporaryDirectory(prefix='run-checks-mise-') as home:
        result = subprocess.run([str(path), '--version'], capture_output=True, text=True, timeout=30,
                                env={'HOME': home, 'PATH': '/usr/bin:/bin', 'MISE_NO_CONFIG': '1',
                                     'MISE_LOG_LEVEL': 'error'})
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
                hint += f' or install {key} {declared_version(manifest, key)} declared in {manifest}'
            state = 'only a shim on PATH' if found else 'not found'
            raise LookupError(f'{name} is required ({state}); {hint}')
    if name == 'mise':
        # The diagnostics compare the hermetic mise with this pin.
        expected = (REPO / '.mise-version').read_text().strip()
        actual = mise_version(path)
        if actual != expected:
            raise LookupError(f'mise {expected} from .mise-version is required, but {path} reports '
                              f'{actual or "no version"}; set MISE_BIN to a {expected} binary')
    return path, origin


def ensure_python():
    """Re-launch on the declared Python when started by an older interpreter."""
    if sys.version_info >= (3, 11):
        return
    installed = None if os.environ.get('RUN_CHECKS_REEXEC') else find_installed('python3')
    if not installed:
        sys.exit('Python 3.11+ is required (tomllib); run with python3.11+ or install the '
                 'python version declared in dot_config/mise/conf.d/10-tools.toml')
    os.environ['RUN_CHECKS_REEXEC'] = '1'
    os.execv(str(installed), [str(installed), str(Path(__file__).resolve())] + sys.argv[1:])


def known_modules():
    return sorted(p.stem for p in TESTS.glob('test_*.py'))


def expand(targets, parser):
    """Turn suite and module names into {module: [unittest names]} in a stable order."""
    groups, modules = {}, set(known_modules())
    for target in targets:
        if target.endswith('.py'):
            target = Path(target).stem
        if target in SUITES:
            selected = SUITES[target]
        elif target.split('.')[0] in modules:
            selected = [target]
        else:
            parser.error(f'unknown target {target!r}; use a suite ({", ".join(SUITES)}) '
                         f'or a module: {", ".join(sorted(modules))}')
        for name in selected:
            names = groups.setdefault(name.split('.')[0], [])
            if name not in names:
                names.append(name)
    # A whole module wins over single tests of the same module.
    return {module: [module] if module in names else names for module, names in groups.items()}


class TimedResult(unittest.TextTestResult):
    seconds = {}

    def startTest(self, test):
        self._started = time.monotonic()
        super().startTest(test)

    def stopTest(self, test):
        TimedResult.seconds[test.id()] = time.monotonic() - self._started
        super().stopTest(test)


def run_child(names, report):
    """Inside the isolated child: run the names and write a JSON report."""
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2, resultclass=TimedResult).run(tests)
    Path(report).write_text(json.dumps({
        'run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
        'skipped': len(result.skipped), 'expected_failures': len(result.expectedFailures),
        'unexpected_successes': len(result.unexpectedSuccesses), 'seconds': TimedResult.seconds}))
    return 0 if result.wasSuccessful() else 1


def isolated_env(root, binaries, module):
    home = root / 'home'; home.mkdir()
    bin_dir = root / 'bin'; bin_dir.mkdir()
    for name, path in dict(binaries, python3=sys.executable).items():
        (bin_dir / name).symlink_to(path)
    env = {'HOME': str(home), 'PATH': f'{bin_dir}:/usr/bin:/bin:/usr/sbin:/sbin',
           'TMPDIR': str(root), 'LC_ALL': 'C', 'PYTHONDONTWRITEBYTECODE': '1',
           'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': str(home / '.gitconfig'),
           'GIT_TERMINAL_PROMPT': '0'}
    for key, part in [('CONFIG', '.config'), ('DATA', '.local/share'),
                      ('CACHE', '.cache'), ('STATE', '.local/state')]:
        env[f'XDG_{key}_HOME'] = str(home / part)
    for name, path in binaries.items():
        env[env_name(name)] = path
    for variable in PASSTHROUGH.get(module, []):
        if os.environ.get(variable):
            env[variable] = os.environ[variable]
    # No OP_*, SSH agent, Git overrides, mise settings, tokens or user PATH.
    return env


def run_module(module, names, binaries):
    """Run one module in a fresh temporary root; return (module, code, output, report, secs)."""
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f'dotfiles-checks-{module}-') as temporary:
        root = Path(temporary).resolve()
        report = root / 'report.json'
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--isolated-child',
                                 '--report', str(report), *names],
                                cwd=root, env=isolated_env(root, binaries, module),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        data = json.loads(report.read_text()) if report.is_file() else None
    return module, result.returncode, result.stdout, data, time.monotonic() - started


def main():
    ensure_python()
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('targets', nargs='+', metavar='target',
                        help=f'suite ({", ".join(SUITES)}) or test module')
    parser.add_argument('-j', '--jobs', type=int, default=max(2, os.cpu_count() or 2),
                        help='modules to run at once (default: CPU count)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print the output of passing modules too')
    parser.add_argument('--isolated-child', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--report', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.isolated_child:
        return run_child(args.targets, args.report)
    started = time.monotonic()
    groups = expand(args.targets, parser)
    names = list(BASE_TOOLS)
    if set(groups) - WITHOUT_MISE:
        names.append('mise')
    for module in groups:
        names += [tool for tool in EXTRA_TOOLS.get(module, []) if tool not in names]
    binaries = {}
    for name in names:
        try:
            path, origin = resolve(name)
        except LookupError as error:
            parser.error(str(error))
        binaries[name] = str(path)
        print(f'{name}: {path} ({origin})', flush=True)
    print(f'Running {len(groups)} module(s), {args.jobs} at a time', flush=True)
    failed, counts, slowest = [], {'run': 0, 'skipped': 0}, []
    # Longest modules first keeps the wall time near the slowest single module.
    order = sorted(groups, key=lambda m: SLOW_FIRST.index(m) if m in SLOW_FIRST else len(SLOW_FIRST))
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(run_module, module, groups[module], binaries) for module in order]
        for future in as_completed(futures):
            module, code, output, data, seconds = future.result()
            ok = code == 0 and data and data['run'] and not (
                data['skipped'] or data['expected_failures'] or data['unexpected_successes'])
            if data:
                counts['run'] += data['run']
                counts['skipped'] += data['skipped'] + data['expected_failures']
                slowest += list(data['seconds'].items())
            tests = data['run'] if data else '?'
            print(f'{"ok  " if ok else "FAIL"} {module}: {tests} tests in {seconds:.1f}s', flush=True)
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
    print(f'{" ".join(args.targets)}: {status}, {counts["run"]} tests, {len(groups)} modules, '
          f'{elapsed:.1f}s wall' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 0 if status == 'passed' else 1


# Started first so they do not extend the wall time at the end of the queue.
SLOW_FIRST = ['test_completion_convergence', 'test_generated_convergence', 'test_windows_config_sync',
              'test_identity_convergence', 'test_identity_transaction', 'test_completion_transaction',
              'test_diagnostic_boundary', 'test_identity_boundary', 'test_lazy_lock_update']

if __name__ == '__main__':
    sys.exit(main())

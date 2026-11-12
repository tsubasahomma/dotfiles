#!/usr/bin/env python3
"""Run source checks with existing binaries, a clean environment and no skips.

No installs here. CI's separate tool-setup step supplies the same prerequisites.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TESTS = Path(__file__).resolve().parent
REGRESSION = [
    'test_mise_read_boundary', 'test_identity_boundary', 'test_identity_transaction',
    'test_identity_convergence', 'test_ownership_boundary', 'test_completion_transaction', 'test_completion_convergence', 'test_git_fetch',
    'test_diagnostic_boundary', 'test_generated_convergence', 'test_windows_packages', 'test_windows_config_sync', 'test_homebrew_packages',
    'test_first_install_order', 'test_lazy_lock_update', 'test_lazy_restore', 'test_ci_verify',
    'test_shell_startup',
]


def run_suite(suite):
    modules = REGRESSION if suite == 'regression' else ['test_render_syntax']
    tests = unittest.defaultTestLoader.loadTestsFromNames(modules)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.skipped or result.expectedFailures or not result.testsRun:
        print('NOT PASSED: skipped, expected-failure or empty suites are not evidence.', file=sys.stderr)
        return 1
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('suite', choices=['regression', 'render'])
    parser.add_argument('--isolated-child', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error('Python 3.11+ is required (tomllib); install it separately')
    if args.isolated_child:
        return run_suite(args.suite)
    names = ['chezmoi', 'nvim', 'zsh', 'git', 'ssh', 'ssh-keygen']
    if args.suite == 'regression':
        names.append('mise')
    binaries = {}
    for name in names:
        value = os.environ.get(name.upper().replace('-', '_') + '_BIN') or shutil.which(name)
        if not value:
            parser.error(f'{name} is required; supply an existing binary (no automatic install)')
        path = Path(value).absolute()
        if 'shims' in path.parts or not path.is_file() or not os.access(path, os.X_OK):
            parser.error(f'{name} must be an executable binary, not a shim: {path}')
        binaries[name] = str(path.resolve())
    with tempfile.TemporaryDirectory(prefix='dotfiles-checks-') as temporary:
        root = Path(temporary).resolve()
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
            env[name.upper().replace('-', '_') + '_BIN'] = path
        # No OP_*, SSH agent, Git overrides, mise settings, tokens or user PATH.
        return subprocess.call([sys.executable, str(Path(__file__).resolve()), args.suite,
                                '--isolated-child'], cwd=root, env=env)


if __name__ == '__main__':
    sys.exit(main())

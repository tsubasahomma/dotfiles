#!/usr/bin/env python3
"""Exercise Vale integration with existing pinned plugins and installed binaries.

Standalone: NVIM_LINT_DIR and LAZYVIM_DIR must point to clean adopted checkouts.
NVIM_BIN and VALE_BIN optionally select existing binaries; no installs or startup.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


def binary(name):
    value = os.environ.get(name.upper() + '_BIN') or shutil.which(name)
    if not value:
        raise RuntimeError(f'{name} is required; provide an installed binary')
    path = Path(value).absolute()
    if 'shims' in path.parts or not path.is_file() or not os.access(path, os.X_OK):
        raise RuntimeError(f'{name} must be an executable binary, not a shim: {path}')
    return path.resolve()


class ValeLintTest(unittest.TestCase):
    def test_adopted_integration(self):
        nvim, vale, git = binary('nvim'), binary('vale'), binary('git')
        lock = json.loads((SOURCE / 'dot_config/nvim/lazy-lock.json').read_text())
        with tempfile.TemporaryDirectory(prefix='vale-lint-') as temp:
            root = Path(temp)
            home = root / 'home'
            home.mkdir()
            bins = root / 'bin'
            bins.mkdir()
            (bins / 'vale').symlink_to(vale)
            env = {
                'HOME': str(home),
                'PATH': f'{bins}:/usr/bin:/bin',
                'LC_ALL': 'C',
                'GIT_CONFIG_NOSYSTEM': '1',
                'GIT_CONFIG_GLOBAL': str(home / '.gitconfig'),
                'GIT_TERMINAL_PROMPT': '0',
            }
            for key, part in [
                ('CONFIG', 'config'),
                ('DATA', 'data'),
                ('CACHE', 'cache'),
                ('STATE', 'state'),
            ]:
                env[f'XDG_{key}_HOME'] = str(home / part)
            for name, variable, paths in [
                ('nvim-lint', 'NVIM_LINT_DIR', ['lua']),
                ('LazyVim', 'LAZYVIM_DIR', ['lua/lazyvim/plugins/linting.lua']),
            ]:
                checkout = Path(os.environ[variable]).resolve()
                head = subprocess.check_output(
                    [str(git), '-C', str(checkout), 'rev-parse', 'HEAD'], env=env, text=True
                ).strip()
                self.assertEqual(head, lock[name]['commit'], f'{name} must match source lock')
                subprocess.run(
                    [str(git), '-C', str(checkout), 'diff', '--exit-code', 'HEAD', '--', *paths],
                    env=env,
                    check=True,
                    capture_output=True,
                )
                for relative in paths:
                    dest = root / name / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if (checkout / relative).is_dir():
                        shutil.copytree(checkout / relative, dest)
                    else:
                        shutil.copyfile(checkout / relative, dest)
            styles = root / 'styles/Local'
            styles.mkdir(parents=True)
            for name, severity, token in [
                ('Error', 'error', 'test'),
                ('Warning', 'warning', '日'),
                ('Suggestion', 'suggestion', '😀'),
            ]:
                (styles / f'{name}.yml').write_text(
                    f"extends: existence\nmessage: '{name}: %s'\nlevel: {severity}\nnonword: true\ntokens:\n  - '{token}'\n"
                )
            config = f'StylesPath = {root}/styles\nMinAlertLevel = suggestion\n[*.md]\nBasedOnStyles = Local\n'
            (root / 'config 日本 space.ini').write_text(config)
            (root / '.vale.ini').write_text(config.replace('suggestion', 'error'))
            result = subprocess.run(
                [
                    str(nvim),
                    '--headless',
                    '-u',
                    'NONE',
                    '--noplugin',
                    '-i',
                    'NONE',
                    '-n',
                    '-l',
                    str(SOURCE / 'tests/fixtures/vale_lint.lua'),
                    str(root),
                    str(SOURCE),
                ],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            print(result.stdout + result.stderr, end='')
            print(
                subprocess.check_output([str(nvim), '--version'], env=env, text=True).splitlines()[
                    0
                ]
            )
            print(subprocess.check_output([str(vale), '--version'], env=env, text=True).strip())


if __name__ == '__main__':
    unittest.main()

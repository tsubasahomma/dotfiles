#!/usr/bin/env python3
"""R13: real chezmoi stage boundaries in empty homes and minimal sources.

No host config, auth, installer, package manager or external asset is used.
Windows and sudo are stubs; successful identity preparation uses real Python/Git.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
PREPARE = '.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl'
LINUX = '.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl'
LINK = 'dot_local/bin/symlink_wezterm.tmpl'
WEZTERM = 'dot_config/wezterm/wezterm.lua.tmpl'
SHELL = 'dot_config/mise/repo-tasks/provision/executable_linux-shell.tmpl'


class FirstInstallOrder(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, 'Supply an existing CHEZMOI_BIN; no automatic install')
        self.tmp = tempfile.TemporaryDirectory(prefix='r13-order-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.home = self.root / 'empty home'
        self.home.mkdir()
        self.assertEqual(list(self.home.iterdir()), [])
        self.source = self.root / 'minimal source'
        self.source.mkdir()
        # init must not clone or initialize a real Git repository.
        (self.source / '.git').mkdir()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.config = self.root / 'config.json'
        self.target = self.home / '.stage-target'
        self.trace = self.root / 'trace'
        self.env = {
            'HOME': str(self.home),
            'PATH': str(self.bin),
            'LC_ALL': 'C',
            'TMPDIR': str(self.root),
            'TRACE': str(self.trace),
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': str(self.root / 'no-global-git-config'),
        }
        for key, part in [
            ('CONFIG', '.config'),
            ('DATA', '.local/share'),
            ('CACHE', '.cache'),
            ('STATE', '.local/state'),
        ]:
            self.env[f'XDG_{key}_HOME'] = str(self.home / part)
        for name in ['sh', 'dirname', 'true']:
            binary = shutil.which(name)
            self.assertTrue(binary, name)
            (self.bin / name).symlink_to(binary)
        self.data = {
            'osid': 'linux',
            'is_wsl': False,
            'identities': [],
            'paths': {'home': str(self.home), 'xdg_config': str(self.home / '.config')},
        }

    def copy(self, name):
        target = self.source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / name, target)
        return target

    def executable(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(0o700)

    def markers(self):
        (self.source / 'dot_stage-target').write_text('placed\n')
        self.executable(
            self.source / '.chezmoiscripts/run_before_00-marker.sh',
            '#!/bin/sh\nset -eu\n[ ! -e "$HOME/.stage-target" ]\nprintf "before\\n" >> "$TRACE"\n',
        )
        self.executable(
            self.source / '.chezmoiscripts/run_after_99-marker.sh',
            '#!/bin/sh\nset -eu\n[ -f "$HOME/.stage-target" ]\nprintf "after\\n" >> "$TRACE"\n',
        )

    def write_config(self):
        self.config.write_text(json.dumps({'data': self.data}))

    def chezmoi(self, *args):
        return subprocess.run(
            [
                str(CHEZMOI),
                '--config',
                str(self.config),
                '--source',
                str(self.source),
                '--destination',
                str(self.home),
                '--cache',
                str(self.root / 'cache'),
                '--color=false',
                '--no-tty',
                *args,
            ],
            env=self.env,
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def assert_stopped(self, result, message, trace=''):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)
        self.assertFalse(self.target.exists())
        self.assertEqual(self.trace.read_text() if self.trace.exists() else '', trace)

    def test_init_stops_on_missing_cli_and_failed_account_then_only_writes_config(self):
        self.config = self.root / 'config.toml'
        self.copy('.chezmoi.toml.tmpl')
        self.copy('.chezmoitemplates/validated_identities.tmpl')
        self.copy('.bootstrap-mise.sh')
        self.markers()
        # Keep the actual generated read hook; its required executable is a stub.
        self.executable(self.home / '.local/bin/mise', '#!/bin/sh\nexit 95\n')
        result = self.chezmoi('init')
        self.assert_stopped(result, "1Password CLI ('op') not found")
        self.assertIn('retrying chezmoi init', result.stderr)
        self.assertFalse(self.config.exists())
        self.executable(self.bin / 'op', '#!/bin/sh\nexit 1\n')
        result = self.chezmoi('init')
        self.assert_stopped(result, 'account check failed')
        self.assertIn('app integration and authentication', result.stderr)
        self.assertFalse(self.config.exists())
        self.executable(
            self.bin / 'op',
            '''#!/bin/sh
case "$*" in
  'account get') exit 0 ;;
  'account list --format json') printf '[]\n' ;;
  *) exit 96 ;;
esac
''',
        )
        result = self.chezmoi('init')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.config.is_file())
        self.assertFalse(self.target.exists())
        self.assertFalse(self.trace.exists())
        result = self.chezmoi('apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.trace.read_text(), 'before\nafter\n')
        self.assertEqual(self.target.read_text(), 'placed\n')

    def test_wsl_missing_wezterm_stops_after_before_then_prepared_path_applies(self):
        self.copy(LINK)
        self.markers()
        self.data['is_wsl'] = True
        self.write_config()
        windows = self.root / 'Windows Program Files/WezTerm/wezterm.exe'
        self.env['WEZTERM_FIXTURE'] = str(windows)
        self.executable(self.bin / 'wslpath', '#!/bin/sh\nprintf "%s\\n" "$WEZTERM_FIXTURE"\n')
        result = self.chezmoi('apply')
        self.assert_stopped(result, 'Prepare WezTerm on Windows', 'before\n')
        self.assertFalse((self.home / '.local/bin/wezterm').is_symlink())
        self.trace.unlink()
        self.executable(windows, '#!/bin/sh\nexit 97\n')
        result = self.chezmoi('apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.trace.read_text(), 'before\nafter\n')
        self.assertEqual(os.readlink(self.home / '.local/bin/wezterm'), str(windows))

    def test_macos_wezterm_render_uses_fixed_path_without_existence_check(self):
        self.copy(LINK)
        self.data['osid'] = 'darwin'
        self.write_config()
        result = self.chezmoi('execute-template', (REPO / LINK).read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '/Applications/WezTerm.app/Contents/MacOS/wezterm')

    def test_before_can_supply_external_wezterm_for_lazy_target_render(self):
        self.copy(LINK)
        self.markers()
        self.data['is_wsl'] = True
        self.write_config()
        # Outside destination: a before script must not mutate chezmoi's source
        # or destination state. This models the separate Windows application.
        windows = self.root / 'Windows Program Files/WezTerm/wezterm.exe'
        windows.parent.mkdir(parents=True)
        self.env['WEZTERM_FIXTURE'] = str(windows)
        self.executable(self.bin / 'wslpath', '#!/bin/sh\nprintf "%s\\n" "$WEZTERM_FIXTURE"\n')
        before = self.source / '.chezmoiscripts/run_before_00-marker.sh'
        before.write_text(before.read_text() + 'printf "fixture\\n" > "$WEZTERM_FIXTURE"\n')
        self.assertFalse(windows.exists())
        result = self.chezmoi('apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(windows.is_file())
        self.assertEqual(os.readlink(self.home / '.local/bin/wezterm'), str(windows))
        self.assertEqual(self.trace.read_text(), 'before\nafter\n')

    def test_wsl_missing_distro_stops_target_after_before(self):
        self.copy(WEZTERM)
        self.markers()
        self.data['is_wsl'] = True
        self.write_config()
        result = self.chezmoi('apply')
        self.assert_stopped(result, 'Run apply from the intended WSL distribution', 'before\n')
        self.trace.unlink()
        self.env['WSL_DISTRO_NAME'] = 'Fixture-Distro'
        result = self.chezmoi('apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('WSL:Fixture-Distro', (self.home / '.config/wezterm/wezterm.lua').read_text())
        self.assertEqual(self.trace.read_text(), 'before\nafter\n')

    def test_identity_missing_python_or_git_stops_before_writes_but_keeps_prior_stage(self):
        self.copy(PREPARE)
        for name in [
            'identity_payload.tmpl',
            'validated_identities.tmpl',
            'posix_shell_quote.tmpl',
            'identity_transaction.py',
        ]:
            self.copy('.chezmoitemplates/' + name)
        self.markers()
        self.write_config()
        result = self.chezmoi('apply')
        self.assert_stopped(result, 'Prepare it outside the post-apply mise install', 'before\n')
        self.assertFalse((self.home / '.config/git').exists())
        self.trace.unlink()
        (self.bin / 'python3').symlink_to(sys.executable)
        result = self.chezmoi('apply')
        self.assert_stopped(result, 'Git must be on PATH before apply', 'before\n')
        self.assertFalse((self.home / '.config/git').exists())
        self.trace.unlink()
        git = shutil.which('git')
        self.assertTrue(git)
        (self.bin / 'git').symlink_to(git)
        result = self.chezmoi('apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / '.config/git/identity.inc').is_file())
        self.assertEqual(self.trace.read_text(), 'before\nafter\n')

    def test_linux_sudo_refusal_stops_packages_targets_and_after(self):
        self.copy(LINUX)
        self.copy('.chezmoitemplates/linux-packages.list.tmpl')
        self.markers()
        # The actual Linux 00-provision sorts after 00-marker, before 05-identity.
        self.data['packages'] = {'headless': {'common': [], 'linux': {}}}
        self.write_config()
        self.executable(
            self.bin / 'sudo', '#!/bin/sh\nprintf "sudo %s\\n" "$*" >> "$TRACE"\nexit 1\n'
        )
        for name in ['apt-get', 'dnf', 'pacman']:
            self.executable(
                self.bin / name, '#!/bin/sh\nprintf "unexpected-package\\n" >> "$TRACE"\nexit 98\n'
            )
        result = self.chezmoi('apply')
        self.assert_stopped(result, 'Confirm sudo availability', 'before\nsudo -n true\n')
        self.assertIn('apt-get/dnf/pacman permissions', result.stderr)
        self.assertNotIn('NOPASSWD', result.stderr)
        # The later Linux shell task must give bounded guidance too.
        rendered = self.chezmoi('execute-template', (REPO / SHELL).read_text())
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        result = subprocess.run(
            ['/bin/bash'],
            input=rendered.stdout,
            env=self.env,
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('/etc/shells registration and chsh', result.stderr)
        self.assertNotIn('passwordless', result.stderr)
        self.assertEqual(self.trace.read_text(), 'before\nsudo -n true\nsudo -n true\n')


if __name__ == '__main__':
    unittest.main()

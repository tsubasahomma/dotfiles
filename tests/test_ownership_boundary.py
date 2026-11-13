#!/usr/bin/env python3
"""R06: isolated permission and retired-path preservation checks.

Uses installed chezmoi with a minimal hookless source/config, temporary HOME/XDG,
and dummy file contents. Never runs the host's apply, repair, doctor or mise.
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
REPAIR = 'dot_config/mise/repo-tasks/repair/executable_security.tmpl'
# Historical names are fixtures, not an ownership list or deletion manifest.
RETIRED = '''
.config/vale/.vale.ini
.cache/zsh/completions/_hyperfine
.config/nvim/lua/plugins/fzf.lua
.config/git/config_personal
.local/share/mise/installs/docker-cli
.local/share/mise/shims/docker
.config/mise/tasks/converge/bat
.config/mise/tasks/converge/completions
.config/mise/tasks/converge/identity
.config/mise/tasks/converge/pbfile
.config/mise/tasks/doctor/_default
.config/mise/tasks/doctor/completion
.config/mise/tasks/doctor/hubspot
.config/mise/tasks/doctor/identity
.config/mise/tasks/doctor/npm-backend
.config/mise/tasks/doctor/nvim
.config/mise/tasks/doctor/security
.config/mise/tasks/doctor/toolchain
.config/mise/tasks/doctor/vale
.config/mise/tasks/integrate/nvim
.config/mise/tasks/setup/_default
.config/mise/tasks/setup/bat
.config/mise/tasks/setup/pnpm
.config/mise/tasks/setup/security
.config/mise/tasks/setup/vale
.config/mise/tasks/sync/vale
.config/mise/tasks/sync/wezterm
.config/mise/tasks/update/lazy-lock
.config/mise/repo-tasks/converge/bat
.config/mise/repo-tasks/converge/completions
.config/mise/repo-tasks/converge/identity
.config/mise/repo-tasks/converge/pbfile
.config/mise/repo-tasks/doctor/completion
.config/mise/repo-tasks/doctor/hubspot
.config/mise/repo-tasks/doctor/identity
.config/mise/repo-tasks/doctor/npm-backend
.config/mise/repo-tasks/doctor/nvim
.config/mise/repo-tasks/doctor/security
.config/mise/repo-tasks/doctor/toolchain
.config/mise/repo-tasks/doctor/vale
.config/mise/repo-tasks/integrate/nvim
.config/mise/repo-tasks/setup/_default
.config/mise/repo-tasks/setup/bat
.config/mise/repo-tasks/setup/pnpm
.config/mise/repo-tasks/setup/security
.config/mise/repo-tasks/setup/vale
.config/systemd/user/1password-bridge.service
.config/systemd/user/default.target.wants/1password-bridge.service
.config/mise/repo-tasks/service/1password-bridge
'''.split()


def snapshot(root):
    """Capture exact names, type, modes, bytes and links without following links."""
    result = {}

    def visit(path):
        mode = path.lstat().st_mode
        key = str(path.relative_to(root))
        if stat.S_ISLNK(mode):
            data = ('link', os.readlink(path))
        elif stat.S_ISDIR(mode):
            data = ('directory',)
            for child in sorted(path.iterdir()):
                visit(child)
        else:
            data = ('file', hashlib.sha256(path.read_bytes()).hexdigest())
        result[key] = (stat.S_IMODE(mode), *data)

    visit(root)
    return result


class OwnershipBoundary(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, 'An installed chezmoi is required')
        self.tmp = tempfile.TemporaryDirectory(prefix='r06-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.home = self.root / "home ' $(touch NOT_EXECUTED) `touch NOT_EXECUTED_BT`"
        self.home.mkdir()
        self.source = self.root / 'source'
        self.source.mkdir()
        # Only these inputs are allowed into the removal fixture: no hooks,
        # scripts, externals, host config or full repo apply.
        shutil.copyfile(REPO / '.chezmoiremove.tmpl', self.source / '.chezmoiremove.tmpl')
        shutil.copytree(REPO / '.chezmoitemplates', self.source / '.chezmoitemplates')
        self.config = self.root / 'config.json'
        self.env = {
            'HOME': str(self.home),
            'PATH': '/usr/bin:/bin',
            'LC_ALL': 'C',
            'TMPDIR': str(self.root),
            'XDG_CONFIG_HOME': str(self.root / 'config'),
            'XDG_CACHE_HOME': str(self.root / 'cache'),
            'XDG_STATE_HOME': str(self.root / 'state'),
            'XDG_DATA_HOME': str(self.root / 'data'),
        }
        self.write_config(False)

    def write_config(self, wsl):
        self.config.write_text(
            json.dumps({'data': {'is_wsl': wsl, 'paths': {'home': str(self.home)}}})
        )

    def run_ok(self, args, **kwargs):
        p = subprocess.run(
            [str(x) for x in args],
            env=self.env,
            cwd=self.root,
            text=True,
            capture_output=True,
            **kwargs,
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def chezmoi(self, *args, **kwargs):
        return self.run_ok(
            [
                CHEZMOI,
                '--config',
                self.config,
                '--source',
                self.source,
                '--destination',
                self.home,
                '--cache',
                self.root / 'cache',
                '--no-tty',
                '--color=false',
                *args,
            ],
            **kwargs,
        )

    def file(self, path, mode=0o640):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('unmanaged fixture only: ' + path.name + '\n')
        path.chmod(mode)

    def test_repair_preserves_keys_nested_files_and_links(self):
        ssh = self.home / '.ssh'
        for name, mode in [
            ('id_ed25519', 0o640),
            ('id_rsa', 0o400),
            ('id_unrelated', 0o644),
            ('id_ed25519.pub', 0o604),
            ('nested/id_private', 0o660),
            ('nested/deeper/id_other', 0o444),
            ('known_hosts', 0o600),
        ]:
            self.file(ssh / name, mode)
        outside = self.home / 'outside'
        self.file(outside / 'id_external', 0o640)
        (ssh / 'id_link').symlink_to(outside / 'id_external')
        (ssh / 'id_broken').symlink_to(outside / 'absent')
        (ssh / 'nested/link').symlink_to(outside, target_is_directory=True)
        before = snapshot(self.home)
        for wsl in (False, True):
            self.write_config(wsl)
            rendered = self.chezmoi('execute-template', input=(REPO / REPAIR).read_text())
            self.run_ok(['/bin/bash', '-n'], input=rendered)
            message = self.run_ok(['/bin/bash'], input=rendered)
            self.assertEqual(snapshot(self.home), before)
            self.assertIn('No permission changes', message)

    def check_retired(self, kind):
        outside = self.home / 'user-managed'
        self.file(outside / 'payload', 0o604)
        for name in RETIRED:
            p = self.home / name
            p.parent.mkdir(parents=True, exist_ok=True)
            if kind == 'files':
                if name.endswith('/installs/docker-cli'):
                    self.file(p / 'manual-version/bin/docker', 0o751)
                    self.file(p / 'nested/id_unrelated', 0o640)
                    (p / 'nested/linked').symlink_to(outside / 'payload')
                else:
                    self.file(p, 0o751 if name.endswith('/shims/docker') else 0o640)
            elif kind == 'directories':
                self.file(p / 'nested/id_unrelated', 0o604)
                p.chmod(0o750)
                (p / 'nested/link').symlink_to(outside, target_is_directory=True)
            else:
                p.symlink_to(outside / 'payload')
        before = snapshot(self.home)
        for wsl in (False, True):
            self.write_config(wsl)
            # Real chezmoi target calculation plus application in the fixture.
            self.assertEqual(self.chezmoi('diff'), '')
            self.chezmoi('apply', '--dry-run')
            self.assertEqual(snapshot(self.home), before)
            self.chezmoi('apply', '--force')
            self.assertEqual(snapshot(self.home), before)
        # Positive control proves the real remove evaluator saw these fixtures.
        (self.source / '.chezmoiremove.tmpl').write_text('.local/share/mise/shims/docker\n')
        self.assertIn('docker', self.chezmoi('diff'))
        self.assertEqual(snapshot(self.home), before)

    def test_retired_files_and_manual_docker_install(self):
        self.check_retired('files')

    def test_retired_names_replaced_by_nested_directories(self):
        self.check_retired('directories')

    def test_retired_names_replaced_by_symlinks(self):
        self.check_retired('links')

    def test_owned_source_modes_still_apply(self):
        owned = self.source / 'private_dot_owned'
        owned.mkdir()
        (owned / 'private_marker').write_text('owned fixture\n')
        self.chezmoi('apply', '--force')
        target = self.home / '.owned'
        self.assertEqual(target.stat().st_mode & 0o777, 0o700)
        self.assertEqual((target / 'marker').stat().st_mode & 0o777, 0o600)
        self.assertEqual((target / 'marker').read_text(), 'owned fixture\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)

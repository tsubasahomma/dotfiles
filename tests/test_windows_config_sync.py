#!/usr/bin/env python3
"""R14/R10 Windows: real reduced apply and file policy, Windows boundary stubs."""

import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
WRAPPER = '.chezmoiscripts/run_after_50-wsl-sync-services.sh.tmpl'
SOURCES = {'wezterm': 'wezterm/wezterm.lua', '1password-agent': '1Password/ssh/agent.toml'}
WINDOWS_STUB = r'''#!PYTHON
import base64,json,os,pathlib,sys
args=sys.argv[1:]
if pathlib.Path(sys.argv[0]).name=='powershell.exe':
    assert args[:4]==['-NoLogo','-NoProfile','-NonInteractive','-EncodedCommand'] and len(args)==5
    script=base64.b64decode(args[4]).decode('utf-16le')
    assert 'ReparsePoint' in script and 'Get-Item -LiteralPath' in script
    assert 'catch [System.Management.Automation.ItemNotFoundException]' in script
    assert '[Environment]::GetEnvironmentVariable' in script and "'Process'" in script
    variable='LOCALAPPDATA' if "'LOCALAPPDATA'" in script else 'USERPROFILE'
    assert ('1Password\\config\\ssh\\agent.toml' if variable=='LOCALAPPDATA' else '.wezterm.lua') in script
    failure=os.environ.get('PROBE_FAIL')
    if failure in ('failure','reparse'): sys.exit(41)
    if failure=='json': print('not-json');sys.exit()
    if failure=='stderr': print('query warning',file=sys.stderr)
    root=os.environ.get('WIN_'+variable, 'D:\\Redirected Local 日本語' if variable=='LOCALAPPDATA' else 'C:\\Profile')
    if failure=='empty': root=''
    print(base64.b64encode(json.dumps({'root':root}).encode()).decode())
else:
    assert args[0]=='-u' and len(args)==2
    if os.environ.get('CONVERT_FAIL'): sys.exit(42)
    print(os.environ['FIXTURE_LOCAL'] if args[1].startswith('D:') else os.environ['FIXTURE_PROFILE'])
'''


def executable(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
    path.chmod(0o700)


def install_windows_stubs(bin_dir, env, profile, local):
    env.update(FIXTURE_PROFILE=str(profile), FIXTURE_LOCAL=str(local))
    for name in ['powershell.exe', 'wslpath']:
        executable(bin_dir / name, WINDOWS_STUB.replace('PYTHON', sys.executable))
    (bin_dir / 'python3').symlink_to(sys.executable)


def engine():
    spec = importlib.util.spec_from_file_location(
        'windows_config_sync', REPO / '.chezmoitemplates/windows_config_sync.py'
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WindowsSync(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, 'existing chezmoi required')
        temp = tempfile.TemporaryDirectory(prefix='r14-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.home = self.root / "home ' $(literal) `literal` 日本語"
        self.home.mkdir()
        self.source = self.root / 'source'
        self.source.mkdir()
        shutil.copytree(REPO / '.chezmoitemplates', self.source / '.chezmoitemplates')
        shutil.copytree(REPO / '.chezmoidata', self.source / '.chezmoidata')
        files = [
            WRAPPER,
            '.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl',
            'dot_config/wezterm/wezterm.lua.tmpl',
            'dot_config/1Password/ssh/private_agent.toml.tmpl',
            'dot_config/mise/config.toml.tmpl',
            'dot_config/mise/conf.d/10-tools.toml',
        ]
        files += [
            str(p.relative_to(REPO))
            for p in (REPO / 'dot_config/mise/repo-tasks').rglob('*')
            if p.is_file()
        ]
        for name in files:
            p = self.source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / name, p)
        (self.source / '.chezmoiexternal.toml.tmpl').write_text('')
        ignores = ['.config/mise/config.toml', '.config/mise/conf.d']
        for p in (self.source / 'dot_config/mise/repo-tasks').rglob('*'):
            if p.is_file():
                name = (
                    str(p.relative_to(self.source / 'dot_config/mise/repo-tasks'))
                    .replace('executable_', '')
                    .removesuffix('.tmpl')
                )
                if name not in ['sync/' + kind for kind in SOURCES]:
                    ignores.append('.config/mise/repo-tasks/' + name)
        (self.source / '.chezmoiignore').write_text('\n'.join(ignores) + '\n')
        (self.source / '.chezmoiscripts/run_before_01-fixture.sh').write_text(
            '#!/bin/sh\nprintf "before\\n" >> "$HOME/calls"\n'
        )
        self.bin = self.home / '.local/bin'
        self.bin.mkdir(parents=True)
        self.profile = self.root / 'Windows profile'
        self.profile.mkdir()
        self.local = self.root / "redirected ' 日本語 local"
        self.local.mkdir()
        self.env = {
            'HOME': str(self.home),
            'PATH': f'{self.bin}:/usr/bin:/bin',
            'TMPDIR': str(self.root),
            'LC_ALL': 'C',
            'PYTHONDONTWRITEBYTECODE': '1',
            'WSL_DISTRO_NAME': 'FixtureDistro',
        }
        install_windows_stubs(self.bin, self.env, self.profile, self.local)
        executable(
            self.bin / 'mise',
            '''#!/bin/sh
[ -f "$HOME/.config/wezterm/wezterm.lua" ] || exit 83
[ -f "$HOME/.config/1Password/ssh/agent.toml" ] || exit 84
printf '%s\n' "$*" >> "$HOME/calls"
''',
        )
        paths = {'home': str(self.home), 'mise': str(self.bin / 'mise'), 'op': ''}
        for name, part in [
            ('config', '.config'),
            ('data', '.local/share'),
            ('state', '.local/state'),
            ('cache', '.cache'),
        ]:
            paths['xdg_' + name] = str(self.home / part)
            self.env['XDG_' + name.upper() + '_HOME'] = str(self.home / part)
        self.config = self.root / 'config.json'
        self.data = {'data': {'paths': paths, 'osid': 'linux', 'is_wsl': True, 'identities': []}}
        self.config.write_text(json.dumps(self.data))
        self.targets = {
            'wezterm': self.profile / '.wezterm.lua',
            '1password-agent': self.local / '1Password/config/ssh/agent.toml',
        }
        self.helper = engine()

    def apply(self, success=True):
        result = subprocess.run(
            [
                CHEZMOI,
                '--config',
                str(self.config),
                '--source',
                str(self.source),
                '--destination',
                str(self.home),
                '--no-tty',
                'apply',
                '--force',
            ],
            env=self.env,
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def task(self, kind='wezterm', success=True):
        result = subprocess.run(
            ['/bin/bash', str(self.home / '.config/mise/repo-tasks/sync' / kind)],
            env=self.env,
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def receipt(self, kind='wezterm'):
        p = self.targets[kind]
        return p.with_name(p.name + '.dotfiles-sync.json')

    def snapshot(self):
        paths = list(self.targets.values()) + [self.receipt(k) for k in SOURCES]
        return {
            str(p): (p.read_bytes(), p.stat().st_mtime_ns, p.stat().st_ino, p.stat().st_mode)
            for p in paths
            if p.exists()
        }

    def direct(self, kind='wezterm'):
        with mock.patch.dict(os.environ, self.env, clear=True):
            self.helper.sync(kind, self.home / '.config' / SOURCES[kind])

    def change(self):
        p = self.home / '.config/wezterm/wezterm.lua'
        p.write_bytes(p.read_bytes() + b'\n-- changed\n')

    def test_apply_order_noop_and_each_missing_target(self):
        self.apply()
        calls = (self.home / 'calls').read_text()
        self.assertEqual(calls.splitlines(), ['before', 'install', 'run lifecycle:post-apply'])
        before = self.snapshot()
        self.apply()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual((self.home / 'calls').read_text(), calls + 'before\n')
        for kind, target in self.targets.items():
            with self.subTest(kind=kind):
                target.unlink()
                self.apply()
                after = self.snapshot()
                self.assertEqual(after[str(target)][0], before[str(target)][0])
                self.assertEqual(
                    {k: v for k, v in before.items() if k != str(target)},
                    {k: v for k, v in after.items() if k != str(target)},
                )
                before = after
        self.assertFalse((self.profile / 'AppData').exists())

    def test_render_dependencies_same_apply(self):
        self.apply()
        before = self.snapshot()
        self.env['WSL_DISTRO_NAME'] = 'DifferentDistro'
        self.apply()
        self.assertIn(b'WSL:DifferentDistro', self.targets['wezterm'].read_bytes())
        self.assertEqual(
            self.snapshot()[str(self.targets['1password-agent'])],
            before[str(self.targets['1password-agent'])],
        )
        shared = self.source / '.chezmoitemplates/validated_identities.tmpl'
        # Change shared input output, using an explicitly dummy item without auth.
        shared.write_text(
            '{{ list (dict "item_id" "fixture-item" "account_id" "fixture-account") | toJson }}'
        )
        self.apply()
        self.assertIn(b'fixture-item', self.targets['1password-agent'].read_bytes())
        before = self.snapshot()
        manifest = self.source / 'dot_config/mise/conf.d/10-tools.toml'
        manifest.write_text(manifest.read_text() + '\n# changed mise requirement\n')
        self.apply()
        self.assertEqual(before, self.snapshot())
        self.assertEqual((self.home / 'calls').read_text().count('install'), 2)

    def test_mise_pin_binary_and_adapter_only_changes_do_not_rewrite(self):
        pin = self.source / '.mise-version'
        pin.write_bytes((REPO / '.mise-version').read_bytes())
        self.apply()
        before = self.snapshot()
        calls = (self.home / 'calls').read_text()
        changes = [
            (pin, 'fixture-next-version\n'),
            (
                self.bin / 'mise',
                (self.bin / 'mise').read_text() + '\n# fixture binary version change\n',
            ),
            (
                self.source / '.chezmoitemplates/windows_config_sync.py',
                (self.source / '.chezmoitemplates/windows_config_sync.py').read_text()
                + '\n# helper-only change\n',
            ),
            (
                self.source / 'dot_config/mise/repo-tasks/sync/executable_wezterm.tmpl',
                (
                    self.source / 'dot_config/mise/repo-tasks/sync/executable_wezterm.tmpl'
                ).read_text()
                + '\n# adapter-only change\n',
            ),
        ]
        for index, (path, content) in enumerate(changes, 1):
            with self.subTest(path=path.name):
                path.write_text(content)
                self.apply()
                self.assertEqual(before, self.snapshot())
                self.assertEqual((self.home / 'calls').read_text(), calls + 'before\n' * index)

    def test_initial_equal_adopts_without_replacing_and_conflict_preserved(self):
        self.env['CI'] = 'true'
        self.apply()
        del self.env['CI']
        target = self.targets['wezterm']
        source = self.home / '.config/wezterm/wezterm.lua'
        target.write_bytes(source.read_bytes())
        before = target.stat()
        self.task()
        self.assertEqual(target.stat().st_ino, before.st_ino)
        self.assertEqual(target.stat().st_mtime_ns, before.st_mtime_ns)
        self.receipt().unlink()
        target.write_bytes(b'custom')
        self.task(success=False)
        self.assertEqual(target.read_bytes(), b'custom')
        self.assertFalse(self.receipt().exists())

    def test_manual_edit_receipt_loss_and_invalid_receipt(self):
        self.apply()
        target = self.targets['wezterm']
        expected = target.read_bytes()
        self.receipt().unlink()
        self.task()
        self.assertEqual(target.read_bytes(), expected)
        target.write_bytes(b'manual')
        self.change()
        source = self.home / '.config/wezterm/wezterm.lua'
        source.write_bytes(b'manual')
        self.task(success=False)
        self.assertEqual(target.read_bytes(), b'manual')
        self.receipt().unlink()
        target.write_bytes(b'different')
        self.task(success=False)
        target.write_bytes(expected)
        for value in [b'bad', b'{}', b'{"version":true}', b'[]']:
            with self.subTest(value=value):
                self.receipt().write_bytes(value)
                self.task(success=False)
                self.assertEqual(target.read_bytes(), expected)
                self.assertEqual(self.receipt().read_bytes(), value)

    def test_shared_distro_receipt_and_lock(self):
        self.apply()
        self.change()
        # Different Linux source/home, identical Windows mapping and receipt.
        other = self.root / 'other-distro'
        other.mkdir()
        src = other / 'wezterm.lua'
        src.write_bytes(b'other distro')
        with mock.patch.dict(os.environ, self.env, clear=True):
            self.helper.sync('wezterm', src)
        self.assertEqual(self.targets['wezterm'].read_bytes(), b'other distro')
        lock = self.targets['wezterm'].with_name('.wezterm.lua.dotfiles-sync.lock')
        lock.mkdir()
        before = self.snapshot()
        self.task(success=False)
        self.assertEqual(before, self.snapshot())
        self.assertTrue(lock.exists())
        lock.rmdir()
        self.task()
        self.assertIn(b'changed', self.targets['wezterm'].read_bytes())

    def test_source_missing_and_bridge_failures_keep_old(self):
        self.apply()
        before = self.snapshot()
        src = self.home / '.config/wezterm/wezterm.lua'
        data = src.read_bytes()
        src.unlink()
        self.task(success=False)
        self.assertEqual(before, self.snapshot())
        src.write_bytes(data)
        for value in ['failure', 'json', 'stderr', 'empty', 'reparse']:
            with self.subTest(value=value):
                self.env['PROBE_FAIL'] = value
                self.task(success=False)
                self.assertEqual(before, self.snapshot())
        del self.env['PROBE_FAIL']
        self.env['CONVERT_FAIL'] = '1'
        self.task(success=False)
        del self.env['CONVERT_FAIL']
        for value in ['relative', '\\\\server\\share', 'C:\\bad..\\x', 'C:\\a:stream']:
            self.env['WIN_USERPROFILE'] = value
            self.task(success=False)
        del self.env['WIN_USERPROFILE']
        self.assertEqual(before, self.snapshot())

    def test_symlinks_nonregular_hardlinks_and_unknown_neighbors(self):
        self.apply()
        target = self.targets['wezterm']
        old = target.read_bytes()
        unknown = self.profile / 'unknown'
        unknown.write_bytes(b'preserve')
        for path in [target, self.receipt(), self.home / '.config/wezterm/wezterm.lua']:
            with self.subTest(path=path.name):
                saved = path.read_bytes()
                path.unlink()
                path.symlink_to(unknown)
                self.task(success=False)
                self.assertEqual(unknown.read_bytes(), b'preserve')
                path.unlink()
                path.write_bytes(saved)
        target.unlink()
        target.mkdir()
        self.task(success=False)
        target.rmdir()
        target.write_bytes(old)
        alias = self.profile / 'alias'
        os.link(target, alias)
        self.task(success=False)
        alias.unlink()
        parent = self.local / '1Password/config'
        backup = self.local / 'config-backup'
        parent.rename(backup)
        parent.symlink_to(backup)
        self.task('1password-agent', success=False)
        parent.unlink()
        backup.rename(parent)
        self.assertEqual(unknown.read_bytes(), b'preserve')

    def test_copy_replace_receipt_and_rollback_failures(self):
        self.apply()
        self.change()
        before = self.snapshot()
        original = self.helper.os.replace
        for fail_at in [1, 2]:
            calls = []

            def replacement(a, b):
                calls.append((a, b))
                if len(calls) == fail_at:
                    raise OSError('injected copy/publish failure')
                return original(a, b)

            with (
                self.subTest(fail_at=fail_at),
                mock.patch.object(self.helper.os, 'replace', side_effect=replacement),
            ):
                with self.assertRaises((RuntimeError, OSError)):
                    self.direct()
            self.assertEqual(
                self.targets['wezterm'].read_bytes(), before[str(self.targets['wezterm'])][0]
            )
            self.assertEqual(self.receipt().read_bytes(), before[str(self.receipt())][0])
        with mock.patch.object(self.helper.os, 'fsync', side_effect=OSError('copy write failure')):
            with self.assertRaises(OSError):
                self.direct()
        self.assertEqual(
            self.targets['wezterm'].read_bytes(), before[str(self.targets['wezterm'])][0]
        )
        calls = []

        def rollback_fail(a, b):
            calls.append((a, b))
            if len(calls) > 1:
                raise OSError('receipt and rollback unavailable')
            return original(a, b)

        with mock.patch.object(self.helper.os, 'replace', side_effect=rollback_fail):
            with self.assertRaisesRegex(RuntimeError, 'rollback failed'):
                self.direct()
        backups = list(self.profile.glob('.*.stage-*'))
        self.assertTrue(backups)
        self.assertTrue(
            any(p.read_bytes() == before[str(self.targets['wezterm'])][0] for p in backups)
        )
        self.task(success=False)  # mismatched receipt is not auto-adopted

    def test_concurrent_edit_before_publish_kept(self):
        self.apply()
        self.change()
        original = self.helper.staged
        count = []

        def edit_after_stage(*args):
            p = original(*args)
            count.append(p)
            if len(count) == 3:
                self.targets['wezterm'].write_bytes(b'concurrent edit')
            return p

        with mock.patch.object(self.helper, 'staged', side_effect=edit_after_stage):
            with self.assertRaisesRegex(RuntimeError, 'Concurrent change'):
                self.direct()
        self.assertEqual(self.targets['wezterm'].read_bytes(), b'concurrent edit')

    def test_receipt_destination_root_relocation_and_old_path_preservation(self):
        self.apply()
        old = self.snapshot()
        obj = json.loads(self.receipt().read_bytes())
        obj['destination'] = 'c:\\elsewhere'
        self.receipt().write_text(json.dumps(obj))
        self.task(success=False)
        self.receipt().write_bytes(old[str(self.receipt())][0])
        old = self.snapshot()
        other = self.root / 'new-local'
        other.mkdir()
        self.env['FIXTURE_LOCAL'] = str(other)
        self.env['WIN_LOCALAPPDATA'] = 'D:\\NewLocal'
        self.task('1password-agent')
        self.assertTrue((other / '1Password/config/ssh/agent.toml').is_file())
        self.assertEqual(self.snapshot(), old)
        old_wrong = self.profile / 'AppData/Local/1Password/config/ssh/agent.toml'
        old_wrong.parent.mkdir(parents=True)
        old_wrong.write_bytes(b'legacy unowned')
        self.task('1password-agent')
        self.assertEqual(old_wrong.read_bytes(), b'legacy unowned')

    def test_late_read_failure_and_external_edit_do_not_discard_backup(self):
        self.apply()
        self.change()
        old = self.targets['wezterm'].read_bytes()
        original = self.helper.os.replace
        published = []

        def publish_then_edit(a, b):
            original(a, b)
            if Path(b) == self.targets['wezterm']:
                published.append(True)
                Path(b).write_bytes(b'external after publish')

        with mock.patch.object(self.helper.os, 'replace', side_effect=publish_then_edit):
            with self.assertRaisesRegex(RuntimeError, 'rollback failed'):
                self.direct()
        self.assertEqual(self.targets['wezterm'].read_bytes(), b'external after publish')
        self.assertTrue(any(p.read_bytes() == old for p in self.profile.glob('.*.stage-*')))

    def test_killed_writer_leaves_conflict_and_recovery_evidence(self):
        self.apply()
        self.change()
        before = self.snapshot()
        script = self.root / 'kill-writer.py'
        script.write_text("""import importlib.util, os, signal, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('sync',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
replace=m.os.replace
def killed(a,b):
    replace(a,b)
    if str(b)==sys.argv[3]:os.kill(os.getpid(),signal.SIGKILL)
m.os.replace=killed
m.sync('wezterm',Path(sys.argv[2]))
""")
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                str(REPO / '.chezmoitemplates/windows_config_sync.py'),
                str(self.home / '.config/wezterm/wezterm.lua'),
                str(self.targets['wezterm']),
            ],
            env=self.env,
        )
        self.assertLess(result.returncode, 0)
        self.assertEqual(self.receipt().read_bytes(), before[str(self.receipt())][0])
        self.assertNotEqual(
            self.targets['wezterm'].read_bytes(), before[str(self.targets['wezterm'])][0]
        )
        self.assertTrue(list(self.profile.glob('.*.stage-*')))
        lock = self.profile / '.wezterm.lua.dotfiles-sync.lock'
        self.assertTrue(lock.is_dir())
        self.task(success=False)
        lock.rmdir()  # Explicit isolated-fixture recovery; production never steals locks.
        self.task(success=False)  # Receipt mismatch still rejects adoption.

    def test_wrapper_failure_is_nonzero_and_prior_setting_may_be_published(self):
        self.env['CI'] = 'true'
        self.apply()
        del self.env['CI']
        self.targets['wezterm'].write_bytes(b'unowned conflict')
        result = self.apply(success=False)
        self.assertTrue(self.targets['1password-agent'].is_file())
        self.assertEqual(self.targets['wezterm'].read_bytes(), b'unowned conflict')
        self.assertNotIn('Windows wezterm setting file', result.stdout)

    def test_nonwsl_and_ci_are_inapplicable(self):
        self.env['CI'] = 'true'
        self.env['PROBE_FAIL'] = 'failure'
        self.apply()
        self.assertFalse(any(p.exists() for p in self.targets.values()))
        del self.env['CI']
        self.data['data']['is_wsl'] = False
        self.config.write_text(json.dumps(self.data))
        self.apply()
        for kind in SOURCES:
            self.task(kind)
        self.assertFalse(any(p.exists() for p in self.targets.values()))


if __name__ == '__main__':
    unittest.main(verbosity=2)

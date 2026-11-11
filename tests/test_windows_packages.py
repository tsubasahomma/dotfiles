#!/usr/bin/env python3
"""Real chezmoi render + shell/Python policy, with a PowerShell transport stub.

This does NOT execute PowerShell/.NET, WinGet or WSL. The stub decodes the exact
EncodedCommand and checks its intended Windows arguments, then returns fixture
Int32 HRESULT/output. Native argv marshalling must still be checked on Windows.
"""
import base64
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
SCRIPT = '.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl'
GUI = 'AgileBits.1Password'
CLI = GUI + '.CLI'
NIGHTLY = 'wez.wezterm.nightly'
MISSING = 0x8A150014
COMMON = ['--source', 'winget', '--exact', '--accept-source-agreements',
          '--disable-interactivity', '--authentication-mode', 'silent']
STUB = r'''
import base64, json, os, re, sys
from pathlib import Path
assert sys.argv[1:5] == ['-NoLogo', '-NoProfile', '-NonInteractive', '-EncodedCommand'], sys.argv
assert len(sys.argv) == 6
script = base64.b64decode(sys.argv[5], validate=True).decode('utf-16le')
Path(os.environ['BRIDGE_CAPTURE']).write_text(script)
match = re.search(r"^    \$info.Arguments = '([A-Za-z0-9._ -]+)'$", script, re.M)
assert match, script
args = match[1].split(' ')
log = Path(os.environ['CALL_LOG'])
with log.open('a') as stream:
    stream.write(json.dumps(args) + '\n')
plan = json.loads(Path(os.environ['PLAN']).read_text())
index = len(log.read_text().splitlines()) - 1
assert index < len(plan), ('unexpected call', args)
step = plan[index]
assert args == step['args'], (args, step['args'])
if 'bridge_stderr' in step:
    print(step['bridge_stderr'], file=sys.stderr)
if 'raw' in step:
    print(step['raw'])
else:
    print(json.dumps(step['reply']))
sys.exit(step.get('bridge_exit', 0))
'''


def call(command, app_id, code=0, output=None, error='', **extra):
    args = [command, '--id', app_id, *COMMON]
    if command == 'install':
        args += ['--silent', '--accept-package-agreements', '--no-upgrade']
    if output is None:
        output = f'Found Application [{app_id}] Version 1.0\nSuccessfully installed\n' if command == 'install' and code == 0 else ''
    signed = code if code < 2**31 else code - 2**32
    return dict(args=args, reply=dict(exitCode=signed, stdout=output, stderr=error), **extra)


def present(app_id):
    return call('list', app_id, output=f'名前 ID バージョン\n--------------------------------------------\nApplication {app_id} 1.0\n')


def absent(app_id):
    return call('list', app_id, MISSING, '入力条件に一致するインストール済みパッケージが見つかりませんでした。\r\n')


class WindowsPackages(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, 'existing chezmoi required')
        self.temporary = tempfile.TemporaryDirectory(prefix='windows-packages-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / 'home'; self.home.mkdir()
        self.source = self.root / 'source'; self.source.mkdir()
        for path in (SCRIPT, '.chezmoitemplates/windows_packages.py'):
            target = self.source / path; target.parent.mkdir(exist_ok=True)
            shutil.copyfile(REPO / path, target)
        (self.source / '.chezmoidata').mkdir()
        self.bin = self.root / 'bin'; self.bin.mkdir()
        (self.bin / 'python3').symlink_to(sys.executable)
        stub = self.bin / 'powershell.exe'
        stub.write_text(f'#!{sys.executable}\n' + STUB); stub.chmod(0o700)
        self.env = {'HOME': str(self.home), 'PATH': f'{self.bin}:/usr/bin:/bin',
                    'TMPDIR': str(self.root), 'LC_ALL': 'C',
                    'PLAN': str(self.root / 'plan.json'), 'CALL_LOG': str(self.root / 'calls.jsonl'),
                    'BRIDGE_CAPTURE': str(self.root / 'bridge.ps1'),
                    'PYTHONDONTWRITEBYTECODE': '1'}
        for key, part in [('CONFIG', '.config'), ('DATA', '.local/share'),
                          ('CACHE', '.cache'), ('STATE', '.local/state')]:
            self.env[f'XDG_{key}_HOME'] = str(self.home / part)

    def render(self, headless=(), gui=(GUI, CLI), wsl=True, ci=False):
        config = self.root / 'config.json'
        config.write_text(json.dumps({'data': {'is_wsl': wsl}}))
        (self.source / '.chezmoidata/packages.yaml').write_text(json.dumps({
            'packages': {'headless': {'windows': list(headless)}, 'gui': {'windows': list(gui)}}}))
        if ci:
            self.env['CI'] = 'true'
        else:
            self.env.pop('CI', None)
        result = subprocess.run([CHEZMOI, '--config', str(config), '--source', str(self.source),
                                 '--destination', str(self.home), '--cache', str(self.home / '.cache/chezmoi'),
                                 '--no-tty', 'execute-template'], input=(self.source / SCRIPT).read_text(),
                                capture_output=True, text=True, env=self.env, cwd=self.root, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.rendered = self.root / 'rendered.sh'; self.rendered.write_text(result.stdout)
        syntax = subprocess.run(['/bin/sh', '-n', str(self.rendered)], capture_output=True, text=True)
        self.assertEqual(syntax.returncode, 0, syntax.stderr)
        return result.stdout

    def run_plan(self, plan, success=True):
        Path(self.env['PLAN']).write_text(json.dumps(plan))
        Path(self.env['CALL_LOG']).unlink(missing_ok=True)
        result = subprocess.run(['/bin/sh', str(self.rendered)], capture_output=True, text=True,
                                env=self.env, cwd=self.root, timeout=30)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        log = Path(self.env['CALL_LOG'])
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        self.assertEqual(calls, [step['args'] for step in plan], result.stdout + result.stderr)
        if not success:
            self.assertNotIn('provisioning complete.', result.stdout)
        return result

    def test_cli_alone_does_not_satisfy_gui(self):
        self.render()
        self.run_plan([absent(GUI), call('install', GUI), present(CLI)])

    def test_exact_installed_never_reinstalled(self):
        self.render()
        self.run_plan([present(GUI), present(CLI)])

    def test_normal_absence_localization_and_nightly_hash(self):
        self.render(gui=(NIGHTLY,))
        for message in ['No installed package found matching input criteria.', '未導入です。', 'Aucun paquet installé.']:
            with self.subTest(message=message):
                self.run_plan([call('list', NIGHTLY, MISSING, message), call('install', NIGHTLY)])

    def test_query_failures_and_low_byte_collisions(self):
        self.render(gui=(GUI,))
        for code in [0x8A150016, 0x8A15000F, 0x8A150012, 0x8A150015, 0x8A150045,
                     0x8A150074, 0x8A150075, 0x8A150076, 0x80070005, 0x80070114, 20, 0x80070000, 0x8A150002]:
            with self.subTest(code=hex(code)):
                result = self.run_plan([call('list', GUI, code, 'No installed package found matching input criteria.')], False)
                self.assertIn(f'0x{code:08X}', result.stderr)

    def test_warning_bearing_no_match_is_not_absence(self):
        self.render(gui=(GUI,))
        for warning in ['Failed when searching source: winget', 'ソース検索に失敗しました', 'Source update failed']:
            with self.subTest(warning=warning):
                self.run_plan([call('list', GUI, MISSING, warning + '\nNo installed package found.')], False)
        self.run_plan([call('list', GUI, MISSING, '', '')], False)
        self.run_plan([call('list', GUI, MISSING, 'No installed package found.', 'source error')], False)

    def test_success_status_with_warning_or_multiple_rows_is_not_success(self):
        self.render(gui=(GUI,))
        normal = present(GUI)['reply']['stdout']
        for output in ['warning\n' + normal, normal + f'Other {GUI} 2.0\n', '',
                       normal.replace(GUI, CLI), normal.replace(GUI, 'AgileBits.1Pass…')]:
            with self.subTest(output=output):
                self.run_plan([call('list', GUI, output=output)], False)
        self.run_plan([call('list', GUI, output=normal, error='warning')], False)

    def test_display_formatting_does_not_hide_warnings(self):
        self.render(gui=(GUI,))
        normal = present(GUI)['reply']['stdout']
        self.run_plan([call('list', GUI, output='\r   -\r   \\ \r\x1b[?25l' + normal + '\x1b[?25h')])
        self.run_plan([call('list', GUI, MISSING, '\x1b[33m警告\x1b[0m\r\n未導入です。')], False)

    def test_hash_and_install_failures_stop_later_packages(self):
        self.render(gui=(NIGHTLY, GUI))
        for code in [0x8A150011, 0x8A150016, 0x8A150008, 0x80070005, 0x80070000, MISSING]:
            with self.subTest(code=hex(code)):
                result = self.run_plan([absent(NIGHTLY), call('install', NIGHTLY, code)], False)
                self.assertIn(f'0x{code:08X}', result.stderr)

    def test_install_source_warning_with_zero_exit_is_failure(self):
        self.render(gui=(GUI, CLI))
        normal = call('install', GUI)['reply']['stdout']
        for warning in ['Failed in attempting to update the source: winget',
                        'ソースの更新に失敗しました: winget', 'Source requires authentication']:
            with self.subTest(warning=warning):
                self.run_plan([absent(GUI), call('install', GUI, output=warning + '\n' + normal)], False)
        for output, error in [('', ''), (normal, 'source error'), (normal.replace(GUI, CLI), '')]:
            with self.subTest(output=output, error=error):
                self.run_plan([absent(GUI), call('install', GUI, output=output, error=error)], False)

    def test_install_identity_is_locale_independent(self):
        self.render(gui=(GUI,))
        for output in [f'見つかりました Application [{GUI}] バージョン 1.0\nインストール完了\n',
                       f'\r -\r\x1b[?25lFound Application [{GUI}] Version 1.0\nSuccessfully installed\x1b[?25h\n']:
            with self.subTest(output=output):
                self.run_plan([absent(GUI), call('install', GUI, output=output)])

    def test_bridge_failures_are_not_package_absence(self):
        self.render(gui=(GUI,))
        for overrides in [dict(bridge_exit=20), dict(bridge_exit=1, bridge_stderr='missing winget'),
                          dict(raw=''), dict(raw='{}'), dict(raw='not json'),
                          dict(raw=json.dumps({'exitCode': 0x8A150014, 'stdout': 'absent', 'stderr': ''})),
                          dict(raw=json.dumps({'exitCode': True, 'stdout': 'absent', 'stderr': ''})),
                          dict(raw=json.dumps({'exitCode': -1978335212, 'stdout': [], 'stderr': ''})),
                          dict(bridge_stderr='PowerShell failure')]:
            with self.subTest(overrides=overrides):
                self.run_plan([call('list', GUI, MISSING, 'absent', **overrides)], False)

    def test_missing_powershell_fails_without_install(self):
        self.render(gui=(GUI,))
        (self.bin / 'powershell.exe').unlink()
        self.run_plan([], False)

    def test_ids_rejected_before_any_windows_call(self):
        for bad in ['', '-bad', 'ID name', "ID'quote", 'ID$(touch injected)', 'ID`x`', 'ID\nnext', '非ASCII', None]:
            with self.subTest(bad=bad):
                self.render(gui=(GUI, bad))
                self.run_plan([], False)
                self.assertFalse((self.root / 'injected').exists())

    def test_non_wsl_and_ci_preserve_scope(self):
        for ci in (False, True):
            self.assertFalse(self.render(wsl=False, ci=ci).strip())
            self.run_plan([])
        self.render(headless=('DenoLand.Deno',), ci=True)
        self.run_plan([present('DenoLand.Deno')])
        self.render(headless=('DenoLand.Deno',), ci=False)
        self.run_plan([present('DenoLand.Deno'), present(GUI), present(CLI)])

    def test_actual_declaration_and_bridge_contract(self):
        # Use the real package YAML in addition to focused fixture IDs.
        self.render()
        shutil.copyfile(REPO / '.chezmoidata/packages.yaml', self.source / '.chezmoidata/packages.yaml')
        result = subprocess.run([CHEZMOI, '--config', str(self.root / 'config.json'), '--source', str(self.source),
                                 '--destination', str(self.home), '--no-tty', 'execute-template'],
                                input=(self.source / SCRIPT).read_text(), env=self.env, cwd=self.root,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.rendered.write_text(result.stdout)
        import re
        payloads = re.findall(r"base64.b64decode\('([^']+)'\)", result.stdout)
        ids = sum((json.loads(base64.b64decode(p)) for p in payloads), [])
        self.assertIn(GUI, ids); self.assertIn(CLI, ids); self.assertIn(NIGHTLY, ids)
        self.run_plan([present(app_id) for app_id in ids])
        bridge = Path(self.env['BRIDGE_CAPTURE']).read_text()
        for fragment in ['$info.UseShellExecute = $false', '$info.RedirectStandardInput = $true',
                         '$process.StandardInput.Close()', '$process.StandardOutput.ReadToEndAsync()',
                         '$process.StandardError.ReadToEndAsync()', '$process.WaitForExit()',
                         'exitCode = $process.ExitCode', 'ConvertTo-Json -Compress', 'exit 1']:
            self.assertIn(fragment, bridge)
        self.assertNotIn('ignore-security-hash', result.stdout)
        self.assertNotIn('source update', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)

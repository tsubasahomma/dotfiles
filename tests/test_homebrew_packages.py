#!/usr/bin/env python3
"""Real chezmoi render + Zsh execution with a stateful brew boundary stub.

No Homebrew command or installer is run. The stub models top-level package
selection only; Homebrew dependency/link/post-install behavior is not simulated.
"""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
ZSH = os.environ.get('ZSH_BIN') or shutil.which('zsh')
SCRIPT = '.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl'
BREWFILE = 'dot_config/homebrew/Brewfile.tmpl'
FLAGS = [
    'HOMEBREW_NO_AUTO_UPDATE',
    'HOMEBREW_NO_INSTALL_CLEANUP',
    'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK',
]
UNSET = [
    'HOMEBREW_FORCE_API_AUTO_UPDATE',
    'HOMEBREW_BUNDLE_INSTALL_CLEANUP',
    'HOMEBREW_BUNDLE_FORCE_INSTALL_CLEANUP',
    'HOMEBREW_BUNDLE_BREW_SKIP',
    'HOMEBREW_BUNDLE_CASK_SKIP',
]
STUB = r'''
import json, os, re, sys
from pathlib import Path
args = sys.argv[1:]
with Path(os.environ['CALL_LOG']).open('a') as log:
    log.write(json.dumps(args) + '\n')
assert args[:3] == ['bundle', 'install', '--no-upgrade'], args
assert len(args) == 4 and args[3].startswith('--file='), args
for key in json.loads(os.environ['REQUIRED_FLAGS']):
    assert os.environ.get(key) == '1', (key, os.environ.get(key))
for key in json.loads(os.environ['REQUIRED_UNSET']):
    assert key not in os.environ, key
brewfile = Path(args[3].split('=', 1)[1])
Path(os.environ['CAPTURE']).write_text(brewfile.read_text())
entries = re.findall(r'^(brew|cask) "([^"]+)"$', brewfile.read_text(), re.M)
state_file = Path(os.environ['STATE'])
state = json.loads(state_file.read_text())
for kind, name in entries:
    key = kind + ':' + name
    if key in state:
        continue
    if name == os.environ.get('FAIL_PACKAGE'):
        sys.exit(23)
    state[key] = 'new-fixture-version'
    state_file.write_text(json.dumps(state))
sys.exit(0)
'''


class HomebrewPackages(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI and ZSH, 'existing chezmoi and Zsh required')
        temporary = tempfile.TemporaryDirectory(prefix='homebrew-packages-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.home = self.root / 'home'
        self.home.mkdir()
        self.source = self.root / 'source'
        self.source.mkdir()
        for rel in (SCRIPT, BREWFILE, '.chezmoidata/packages.yaml'):
            target = self.source / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / rel, target)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        stub = self.bin / 'brew'
        stub.write_text(f'#!{sys.executable}\n' + STUB)
        stub.chmod(0o700)
        # If an installer returns to this path, stop without network or host writes.
        for name in ['curl', 'bash']:
            guard = self.bin / name
            guard.write_text('#!/bin/sh\necho forbidden-installer >&2\nexit 91\n')
            guard.chmod(0o700)
        self.env = {
            'HOME': str(self.home),
            'PATH': f'{self.bin}:/usr/bin:/bin',
            'TMPDIR': str(self.root),
            'LC_ALL': 'C',
            'CALL_LOG': str(self.root / 'calls.jsonl'),
            'STATE': str(self.root / 'state.json'),
            'CAPTURE': str(self.root / 'Brewfile'),
            'REQUIRED_FLAGS': json.dumps(FLAGS),
            'REQUIRED_UNSET': json.dumps(UNSET),
        }
        for key, part in [
            ('CONFIG', '.config'),
            ('DATA', '.local/share'),
            ('CACHE', '.cache'),
            ('STATE', '.local/state'),
        ]:
            self.env[f'XDG_{key}_HOME'] = str(self.home / part)
        for key in FLAGS:
            self.env[key] = ''  # The script must override inherited values.
        for key in UNSET:
            self.env[key] = '1'
        self.env['HOMEBREW_BUNDLE_BREW_SKIP'] = 'jq eza'
        self.env['HOMEBREW_BUNDLE_CASK_SKIP'] = 'slack'
        self.config = self.root / 'config.json'
        self.rendered = self.root / 'rendered.zsh'

    def template(self, content):
        result = subprocess.run(
            [
                CHEZMOI,
                '--config',
                str(self.config),
                '--source',
                str(self.source),
                '--destination',
                str(self.home),
                '--cache',
                str(self.home / '.cache/chezmoi'),
                '--no-tty',
                'execute-template',
            ],
            input=content,
            env=self.env,
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def render(self, ci=False, osid='darwin'):
        self.config.write_text(json.dumps({'data': {'osid': osid}}))
        if ci:
            self.env['CI'] = 'true'
        else:
            self.env.pop('CI', None)
        script = self.template((self.source / SCRIPT).read_text())
        self.rendered.write_text(script)
        self.brewfile = self.template((self.source / BREWFILE).read_text())
        self.entries = dict(
            (kind + ':' + name, 'old-fixture-version')
            for kind, name in re.findall(r'^(brew|cask) "([^"]+)"$', self.brewfile, re.M)
        )
        return script

    def execute(self, state, code=0):
        Path(self.env['STATE']).write_text(json.dumps(state))
        result = subprocess.run(
            [ZSH, '-f', str(self.rendered)],
            env=self.env,
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        log = Path(self.env['CALL_LOG'])
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        if calls:
            self.assertEqual(len(calls), 1)
            self.assertEqual(Path(self.env['CAPTURE']).read_text(), self.brewfile + '\n')
            self.assertFalse(
                Path(calls[0][-1].split('=', 1)[1]).exists(), 'temporary Brewfile leaked'
            )
        if code:
            self.assertNotIn('provisioning complete.', result.stdout)
        return result, json.loads(Path(self.env['STATE']).read_text()), calls

    def test_installed_old_versions_and_undeclared_packages_are_preserved(self):
        self.render()
        state = dict(self.entries, **{'brew:personal': 'manual', 'brew:deno': 'manual'})
        result, after, calls = self.execute(state)
        self.assertEqual(after, state)
        self.assertEqual(len(calls), 1)
        self.assertIn('provisioning complete.', result.stdout)

    def test_missing_formula_and_cask_added_with_existing_versions_preserved(self):
        self.render()
        state = dict(self.entries)
        for key in ['brew:eza', 'cask:slack']:
            del state[key]
        _, after, _ = self.execute(state)
        self.assertEqual(
            after,
            dict(state, **{'brew:eza': 'new-fixture-version', 'cask:slack': 'new-fixture-version'}),
        )

    def test_install_failure_propagates_and_cleans_temporary_file(self):
        self.render()
        state = dict(self.entries)
        del state['brew:eza']
        self.env['FAIL_PACKAGE'] = 'eza'
        _, after, _ = self.execute(state, 23)
        self.assertEqual(after, state)

    def test_missing_brew_fails_without_installer_or_prefix_fallback(self):
        self.render()
        (self.bin / 'brew').unlink()
        result, _, calls = self.execute({}, 1)
        self.assertEqual(calls, [])
        self.assertIn('Homebrew is required in PATH', result.stderr)
        self.assertNotIn('forbidden-installer', result.stderr)

    def test_ci_has_headless_only_and_other_os_is_empty(self):
        self.render(ci=True)
        self.assertFalse(any(key.startswith('cask:') for key in self.entries))
        self.assertNotIn('brew:ffmpeg', self.entries)
        self.assertNotIn('brew:azure-cli', self.entries)
        _, after, _ = self.execute({})
        self.assertEqual(set(after), set(self.entries))
        Path(self.env['CALL_LOG']).unlink()
        self.assertFalse(self.render(osid='linux').strip())
        _, after, calls = self.execute({})
        self.assertEqual(after, {})
        self.assertEqual(calls, [])

    def test_real_declarations_remove_only_selected_mac_duplicates(self):
        self.render()
        packages = json.loads(self.template('{{ .packages | toJson }}'))
        self.assertEqual(
            packages['headless']['darwin']['brews'], ['openssl@3', 'colima', 'eza', 'xh']
        )
        self.assertEqual(packages['headless']['darwin']['casks'], [])
        self.assertEqual(packages['headless']['common'], ['ca-certificates', 'git', 'zsh', 'jq'])
        self.assertEqual(
            packages['headless']['windows'],
            [
                'Atuinsh.Atuin',
                'DuckDB.cli',
                'DenoLand.Deno',
                'eza-community.eza',
                'ducaale.xh',
                'Amazon.AWSCLI',
            ],
        )
        for name in ['just', 'atuin', 'duckdb', 'deno', 'awscli']:
            self.assertNotIn('brew:' + name, self.entries)
        self.assertIn('brew:ffmpeg', self.entries)
        self.assertIn('cask:slack', self.entries)

    def test_embedded_brewfile_tracks_declaration_changes_for_onchange(self):
        before = self.render()
        path = self.source / '.chezmoidata/packages.yaml'
        path.write_text(
            path.read_text().replace(
                '        - colima', '        - fixture-added\n        - colima'
            )
        )
        after = self.render()
        self.assertNotEqual(before, after)
        self.assertIn('brew "fixture-added"', after)


if __name__ == '__main__':
    unittest.main(verbosity=2)

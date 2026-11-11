#!/usr/bin/env python3
"""R10b: real reduced before/target/after applies, stub tool preparation only."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

from test_completion_transaction import CompletionTransaction, REPO, CHEZMOI, ZSH

AFTER = '.chezmoiscripts/run_after_30-completions.sh.tmpl'
WRAPPER = '.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl'
GEN = 'dot_config/mise/repo-tasks/generate/executable_completions.tmpl'


class Convergence(CompletionTransaction):
    def setUp(self):
        super().setUp()
        self.source = self.root / 'source'
        self.config = self.root / 'config.json'
        data = json.loads(self.config.read_text())
        paths = data['data']['paths']
        paths.update({f'xdg_{k.lower()}': self.env[f'XDG_{k}_HOME']
                      for k in ('CONFIG', 'DATA', 'STATE')})
        paths['op'] = ''
        data['data'].update(osid='darwin', is_wsl=False)
        self.config.write_text(json.dumps(data))
        references = [AFTER, WRAPPER, GEN, '.chezmoiexternal.toml.tmpl',
                      'dot_config/mise/config.toml.tmpl', 'dot_config/mise/conf.d/10-tools.toml',
                      'dot_config/vale/vale.ini.tmpl', 'dot_local/share/pbcopy/pbfile.swift']
        references += [str(p.relative_to(REPO)) for p in (REPO / 'dot_config/mise/repo-tasks').rglob('*') if p.is_file()]
        for name in references:
            p = self.source / name; p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / name, p)
        (self.source / '.chezmoiexternal.toml.tmpl').write_text('# Fixture: no external downloads.\n')
        # Ignore real external destinations and all unrelated task targets.
        ignores = ['.config/bat', '.config/zsh', '.config/vale', '.local',
                   '.config/mise/config.toml', '.config/mise/conf.d']
        ignores += ['.config/mise/repo-tasks/' + str(p.relative_to(self.source / 'dot_config/mise/repo-tasks')).replace('executable_', '').removesuffix('.tmpl')
                    for p in (self.source / 'dot_config/mise/repo-tasks').rglob('*')
                    if p.is_file() and str(p.relative_to(self.source)) != GEN]
        (self.source / '.chezmoiignore').write_text('\n'.join(ignores) + '\n')
        (self.source / '.chezmoiscripts/run_before_01-fixture.sh').write_text(
            '#!/bin/sh\nprintf "before\\n" >> "$HOME/order"\n')
        self.calls = self.home / 'calls'
        self.calls.touch()
        self.env['CALLS'] = str(self.calls)
        original = self.stub.read_text()
        self.stub.write_text(original.replace('if [ "$1" = which ]; then', '''printf '%s\\n' "$*" >> "$CALLS"
if [ "$1" = install ]; then
  [ -f "$HOME/.config/mise/repo-tasks/generate/completions" ] || exit 81
  printf 'target then install\\n' >> "$HOME/order"
  touch "$HOME/prepared"
  exit
fi
if [ "$1" = run ]; then printf 'graph\\n' >> "$HOME/order"; exit; fi
[ -f "$HOME/prepared" ] || exit 82
if [ "$1" = which ]; then
  if [ "$4" = gh ] && [ -n "${SELECT_GH:-}" ]; then printf '%s\\n' "$SELECT_GH"; exit; fi'''))
        self.task = self.home / '.config/mise/repo-tasks/generate/completions'

    def apply(self, success=True):
        p = subprocess.run([CHEZMOI, '--config', str(self.config), '--source', str(self.source),
                            '--destination', str(self.home), '--no-tty', 'apply', '--force'],
                           env=self.env, cwd=self.root, text=True, capture_output=True)
        if success:
            self.assertEqual(p.returncode, 0, p.stderr)
        else:
            self.assertNotEqual(p.returncode, 0)
        return p

    def snapshot(self):
        return {str(p.relative_to(self.cache)): (p.read_bytes(), p.stat().st_mode & 0o777,
                                               p.stat().st_mtime_ns, p.stat().st_ino)
                for p in self.cache.rglob('*') if p.is_file()}

    def generated_calls(self):
        return [l for l in self.calls.read_text().splitlines()
                if l.startswith(('exec ', 'completion ')) and 'command -v usage' not in l]

    def assert_no_graph(self, since):
        self.assertFalse(any(l.startswith(('install', 'run '))
                             for l in self.calls.read_text().splitlines()[since:]))

    def test_r10b_apply_twice_and_every_required_missing_output(self):
        self.apply()
        self.assertEqual((self.home / 'order').read_text().splitlines(), ['before', 'target then install', 'graph'])
        snap = self.snapshot(); calls = self.generated_calls()
        since = len(self.calls.read_text().splitlines())
        self.apply()
        self.assertEqual(self.snapshot(), snap)
        self.assertEqual(self.generated_calls(), calls)
        self.assertEqual((self.home / 'order').read_text().splitlines()[-1], 'before')
        outputs = [p for p in (*self.comp.iterdir(), *self.init.iterdir()) if not p.name.startswith('.')]
        self.assertEqual(len(outputs), 21)
        for p in outputs:
            with self.subTest(missing=p.name):
                previous = self.snapshot(); relative = str(p.relative_to(self.cache))
                p.unlink(); self.apply()
                current = self.snapshot()
                self.assertEqual(current[relative][:2], previous[relative][:2])
                receipt = str((p.parent / ('.' + p.name + '.generation.json')).relative_to(self.cache))
                self.assertEqual({k:v for k,v in previous.items() if k not in (relative, receipt)},
                                 {k:v for k,v in current.items() if k not in (relative, receipt)})
        self.assert_no_graph(since)
        # R08 checks remain read-only; normal apply now restores its inventory.
        p = subprocess.run([CHEZMOI, '--config', str(self.config), '--source', str(self.source),
                            '--destination', str(self.home), 'execute-template'],
                           input=(REPO / 'dot_config/mise/repo-tasks/check/executable_completion.tmpl').read_text(),
                           env=self.env, cwd=self.root, text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        before = self.snapshot()
        check = subprocess.run(['/bin/bash'], input=p.stdout, env=self.env, cwd=self.root, text=True, capture_output=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_r10b_actual_dependencies_and_render_changes(self):
        self.apply()
        since = len(self.calls.read_text().splitlines())
        for path in (self.bin / 'gh', self.bin / 'node', self.bin / 'usage', self.sdk / 'completion.zsh.inc',
                     self.package / 'vendor', self.stub):
            with self.subTest(dependency=path.name):
                before = self.snapshot(); calls = len(self.generated_calls())
                path.write_text(path.read_text() + '\n# dependency changed\n')
                self.apply()
                self.assertNotEqual(self.snapshot(), before)
                if path.name == 'gh':
                    self.assertEqual(len(self.generated_calls()) - calls, 1)
                if path.name == 'completion.zsh.inc':
                    self.assertEqual(len(self.generated_calls()), calls)
                if path.name != 'completion.zsh.inc':
                    self.assertGreater(len(self.generated_calls()), calls)
                unchanged = self.snapshot(); calls = self.generated_calls()
                self.apply()
                self.assertEqual(self.snapshot(), unchanged)
                self.assertEqual(self.generated_calls(), calls)
        # Same launcher, different selected execution path must also invalidate.
        alternate = self.bin / 'gh-new'; shutil.copy2(self.bin / 'gh', alternate)
        self.env['SELECT_GH'] = str(alternate)
        calls = len(self.generated_calls())
        self.apply()
        self.assertEqual(len(self.generated_calls()) - calls, 1)
        self.assertIn(str(alternate), self.generated_calls()[-1])
        self.assert_no_graph(since)
        calls = len(self.generated_calls())
        self.env['NO_USAGE'] = '1'
        self.apply()
        self.assertEqual(len(self.generated_calls()) - calls, 1)
        calls = len(self.generated_calls())
        self.apply()
        self.assertEqual(len(self.generated_calls()), calls)
        self.env.pop('NO_USAGE')
        self.apply()
        self.assertEqual(len(self.generated_calls()) - calls, 1)
        for path in (self.source / '.chezmoidata/completions.yaml',
                     self.source / '.chezmoitemplates/completion_state.py'):
            before = self.snapshot(); calls = len(self.generated_calls())
            if path.suffix == '.yaml':
                path.write_text(path.read_text().replace('aqua:cli/cli', 'aqua:fixture/gh'))
            else:
                path.write_text(path.read_text() + '\n# Changed shared fingerprint template.\n')
            self.apply()
            self.assertNotEqual(self.snapshot(), before)
            self.assertGreater(len(self.generated_calls()), calls)
        self.assert_no_graph(since)

    def test_r10b_failure_receipts_and_unmanaged_state(self):
        self.apply()
        unknown = self.comp / '_unmanaged'; unknown.write_text('keep\n')
        target = self.comp / '_gh'
        old = self.old(target)
        self.env.update(FAIL='gh', MODE='invalid')
        self.apply(success=False); self.assert_old(target, old)
        self.assertEqual(unknown.read_text(), 'keep\n')
        self.env.pop('FAIL'); self.env.pop('MODE')
        self.apply()
        receipt = self.comp / '._gh.generation.json'
        receipt.unlink(); receipt.symlink_to(unknown)
        self.apply(success=False)
        self.assertEqual(unknown.read_text(), 'keep\n')
        receipt.unlink(); receipt.write_text('unmanaged\n')
        self.apply(success=False)
        self.assertEqual(receipt.read_text(), 'unmanaged\n')


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(Convergence(name) for name in Convergence.__dict__ if name.startswith('test_r10b_'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

"""Static CI verification must ignore runnable scripts, not file drift."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class VerifyBoundary(unittest.TestCase):
    def test_runnable_script_and_static_drift_are_distinct(self):
        chezmoi = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
        self.assertTrue(chezmoi, 'existing chezmoi required')
        with tempfile.TemporaryDirectory(prefix='verify-boundary-') as temporary:
            root = Path(temporary).resolve()
            home, source = root / 'home', root / 'source'
            home.mkdir(); source.mkdir()
            config = root / 'config.toml'; config.write_text('')
            (source / 'dot_fixture').write_text('expected\n')
            scripts = source / '.chezmoiscripts'; scripts.mkdir()
            (scripts / 'run_after_fixture.sh').write_text('#!/bin/sh\nprintf run >> "$HOME/calls"\n')
            env = {'HOME': str(home), 'PATH': '/usr/bin:/bin', 'TMPDIR': str(root)}
            command = [chezmoi, '--config', str(config), '--source', str(source),
                       '--destination', str(home), '--no-tty']

            def run(*args):
                return subprocess.run([*command, *args], env=env, cwd=root,
                                      capture_output=True, text=True, timeout=30)

            applied = run('apply')
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertEqual((home / 'calls').read_text(), 'run')
            self.assertEqual(run('verify').returncode, 1)
            checked = run('verify', '--exclude=scripts')
            self.assertEqual(checked.returncode, 0, checked.stderr)
            (home / '.fixture').write_text('manual drift\n')
            self.assertEqual(run('verify', '--exclude=scripts').returncode, 1)
            self.assertEqual((home / 'calls').read_text(), 'run')

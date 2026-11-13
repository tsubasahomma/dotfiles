#!/usr/bin/env python3
"""The CI change classifier: only documents skip the build jobs."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import ci_changes

SCRIPT = Path(__file__).resolve().parent / 'ci_changes.py'


class Classifier(unittest.TestCase):
    def test_documents_only(self):
        self.assertTrue(ci_changes.docs_only(['docs/validation.md', 'AGENTS.md', 'README.md']))
        self.assertTrue(ci_changes.docs_only(['docs/platforms/wsl.md', 'LICENSE']))

    def test_anything_else_runs_everything(self):
        for paths in (
            [],
            ['docs/validation.md', 'tests/run_checks.py'],
            ['dot_config/nvim/README.md'],
            ['docs/image.png'],
            ['NOTES.md'],
            ['.github/workflows/compliance.yml'],
        ):
            with self.subTest(paths=paths):
                self.assertFalse(ci_changes.docs_only(paths))

    def test_git_range_and_events(self):
        git = os.environ.get('GIT_BIN') or 'git'
        with tempfile.TemporaryDirectory(prefix='ci-changes-') as temporary:
            root = Path(temporary)

            def run(*args):
                return subprocess.run(
                    [git, *args], cwd=root, capture_output=True, text=True, check=True
                ).stdout.strip()

            run('init', '-q', '-b', 'main')
            run('config', 'user.name', 'Fixture')
            run('config', 'user.email', 'fixture@example.test')
            run('config', 'commit.gpgsign', 'false')
            (root / 'docs').mkdir()
            (root / 'docs/a.md').write_text('a\n')
            run('add', '.')
            run('commit', '-q', '-m', 'base')
            base = run('rev-parse', 'HEAD')
            (root / 'docs/a.md').write_text('b\n')
            run('commit', '-q', '-am', 'doc')
            doc = run('rev-parse', 'HEAD')
            (root / 'tool.sh').write_text('true\n')
            run('add', '.')
            run('commit', '-q', '-m', 'code')
            code = run('rev-parse', 'HEAD')
            env = dict(os.environ, PATH=str(Path(git).parent) + os.pathsep + os.environ['PATH'])
            for event, start, head, expected in [
                ('pull_request', base, doc, 'true'),
                ('pull_request', base, code, 'false'),
                ('push', '0' * 40, doc, 'false'),
                ('schedule', base, doc, 'false'),
                ('workflow_dispatch', base, doc, 'false'),
            ]:
                with self.subTest(event=event, head=head):
                    output = root / 'output'
                    output.write_text('')
                    subprocess.run(
                        [sys.executable, SCRIPT, '--event', event, '--base', start, '--head', head],
                        cwd=root,
                        env=dict(env, GITHUB_OUTPUT=str(output)),
                        capture_output=True,
                        check=True,
                    )
                    self.assertEqual(output.read_text(), f'docs_only={expected}\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)

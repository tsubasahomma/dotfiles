#!/usr/bin/env python3
"""R03: render the global config and fetch only from disposable local remotes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
GIT = shutil.which('git')


class GitFetch(unittest.TestCase):
    def test_normal_fetch_preserves_tags_and_prunes_branches(self):
        self.assertTrue(CHEZMOI and GIT, 'installed chezmoi and Git required')
        with tempfile.TemporaryDirectory(prefix='r03-fetch-') as tmp:
            root = Path(tmp).resolve()
            home = root / 'home'
            home.mkdir()
            source = root / 'source'
            source.mkdir()
            shutil.copytree(REPO / '.chezmoitemplates', source / '.chezmoitemplates')
            config = root / 'chezmoi.json'
            config.write_text(json.dumps({'data': {'identities': [], 'paths': {
                'home': str(home), 'xdg_config': str(home / '.config'),
                'op_sign': '/unused/sign-helper'}}}))
            global_config = home / '.gitconfig'
            env = {'HOME': str(home), 'PATH': '/usr/bin:/bin', 'LC_ALL': 'C',
                   'XDG_CONFIG_HOME': str(home / '.config'),
                   'XDG_CACHE_HOME': str(home / '.cache'),
                   'XDG_DATA_HOME': str(home / '.local/share'),
                   'XDG_STATE_HOME': str(home / '.local/state'),
                   'TMPDIR': str(root),
                   'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': str(global_config),
                   'GIT_TERMINAL_PROMPT': '0', 'GIT_ALLOW_PROTOCOL': 'file'}

            def run(args, *, input=None, expected=0):
                result = subprocess.run([str(x) for x in args], cwd=root, env=env,
                                        input=input, text=True, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                return result.stdout.strip()

            rendered = run([CHEZMOI, '--config', config, '--source', source,
                            '--destination', home, '--cache', home / '.cache/chezmoi',
                            '--no-tty', 'execute-template'],
                           input=(REPO / 'dot_config/git/config.tmpl').read_text())
            global_config.write_text(rendered + '\n')

            def git(repo, *args, **kwargs):
                location = ['--git-dir', repo] if repo.suffix == '.git' else ['-C', repo]
                return run([GIT, *location, *args], **kwargs)

            origin, other, client = (root / x for x in ('origin.git', 'other.git', 'client'))
            for remote in (origin, other):
                run([GIT, 'init', '--bare', '-q', remote])
                # Plumbing creates fixture objects without signing, hooks or a push.
                tree = git(remote, 'mktree', input='')
                oid = git(remote, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test',
                          'commit-tree', tree, input=remote.name + '\n')
                git(remote, 'update-ref', 'refs/heads/main', oid)
                git(remote, 'update-ref', 'refs/tags/' + remote.stem + '-tag', oid)
            initial = git(origin, 'rev-parse', 'refs/heads/main')
            git(origin, 'update-ref', 'refs/heads/obsolete', initial)
            run([GIT, 'init', '-q', client])
            for name, remote in (('origin', origin), ('other', other)):
                git(client, 'remote', 'add', name, remote)
                git(client, 'fetch', name)
            git(client, 'update-ref', 'refs/tags/local-only', initial)
            retained = {tag: git(client, 'rev-parse', 'refs/tags/' + tag)
                        for tag in ('origin-tag', 'other-tag', 'local-only')}
            self.assertEqual(git(client, 'rev-parse', 'refs/remotes/origin/obsolete'), initial)
            git(origin, 'update-ref', '-d', 'refs/heads/obsolete')
            updated = git(origin, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test',
                          'commit-tree', tree, '-p', initial, input='update\n')
            git(origin, 'update-ref', 'refs/heads/main', updated)
            git(origin, 'update-ref', 'refs/tags/new-tag', updated)
            git(client, 'fetch', 'origin')
            for tag, oid in retained.items():
                self.assertEqual(git(client, 'rev-parse', 'refs/tags/' + tag), oid)
            self.assertEqual(git(client, 'rev-parse', 'refs/remotes/origin/main'), updated)
            self.assertEqual(git(client, 'rev-parse', 'refs/tags/new-tag'), updated)
            git(client, 'show-ref', '--verify', '--quiet', 'refs/remotes/origin/obsolete', expected=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)

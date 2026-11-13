#!/usr/bin/env python3
"""R05: real Git consumers, isolated HOME, migration and interrupted publication.

No real apply/auth/install. One reduced chezmoi apply contains only the Git
consumer, identity before script and identity generator (no hooks/externals).
"""

import copy
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import unittest

import test_identity_boundary as boundary

PREPARE = '.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl'


class Transaction(boundary.IdentityBoundary):
    def script(self, template, *args):
        rendered = self.render(template)
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        return self.command([boundary.ZSH, '-s', '--', *args], input=rendered.stdout)

    def prepare(self):
        result = self.script(PREPARE)
        self.assertEqual(result.returncode, 0, result.stderr)

    def put_consumer(self):
        result = self.render(boundary.GIT)
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.home / '.config/git/config').write_text(result.stdout)

    def adopt(self):
        self.prepare()
        self.put_consumer()
        result = self.script(boundary.GEN)
        self.assertEqual(result.returncode, 0, result.stderr)
        for identity in self.ids:
            self.run_ok(['git', 'init', '-q', self.repo(identity)])

    def repo(self, identity):
        return Path(identity['dirs'].replace('~/', str(self.home) + '/', 1)) / 'project'

    def entry(self):
        return self.home / '.config/git/identity.inc'

    def selected_snapshot(self):
        generation = self.generation()
        return (
            self.entry().read_bytes(),
            {p.name: (p.read_bytes(), p.stat().st_mode & 0o777) for p in generation.iterdir()},
        )

    def assert_adopted(self, ids):
        for identity in ids:
            repo = self.repo(identity)
            self.assertEqual(self.git_value(repo, 'user.name'), identity['name'])
            self.assertEqual(self.git_value(repo, 'user.email'), identity['email'])
            self.assertEqual(
                self.git_value(repo, 'user.signingkey'), 'key::' + identity['public_key']
            )
            command = self.git_value(repo, 'core.sshcommand')
            keypath = Path(shlex.split(command)[2])
            self.assertEqual(keypath.read_text(), identity['public_key'] + '\n')
            signers = Path(self.git_value(repo, 'gpg.ssh.allowedsignersfile'))
            self.assertEqual(
                self.run_ok(
                    ['ssh-keygen', '-Y', 'match-principals', '-I', identity['email'], '-f', signers]
                ).strip(),
                identity['email'],
            )

    def change_inputs(self):
        self.ids = [self.identity('next' + str(i), '~/new' + str(i)) for i in range(2)]
        self.write_data()

    def failing_git(self, behavior='exit'):
        real = self.run_ok(['/usr/bin/which', 'git']).strip()
        self.env['REAL_GIT'] = real
        self.env['FAIL_BEHAVIOR'] = behavior
        self.env['FAIL_COUNT'] = str(self.root / 'fail-count')
        boundary.executable(
            self.bin / 'git',
            '''#!/usr/bin/python3
import os,signal,sys
from pathlib import Path
if 'core.sshCommand' in sys.argv:
    p=Path(os.environ['FAIL_COUNT']); n=int(p.read_text())+1 if p.exists() else 1; p.write_text(str(n))
    if n == 2:
        if os.environ['FAIL_BEHAVIOR'] != 'exit':
            os.kill(os.getppid(), getattr(signal, os.environ['FAIL_BEHAVIOR']))
        sys.exit(73)
os.execv(os.environ['REAL_GIT'], [os.environ['REAL_GIT'], *sys.argv[1:]])
''',
        )

    def unfail(self):
        (self.bin / 'git').unlink()
        (self.root / 'fail-count').unlink()

    def legacy(self):
        # Healthy pre-R05 placement, including a sibling unknown file.
        parent = self.home / '.config/git'
        signers = parent / 'allowed_signers'
        signers.write_text(
            ''.join(i['email'] + ' namespaces="git" ' + i['public_key'] + '\n' for i in self.ids)
        )
        config = parent / 'config'
        config.write_text('[user]\n useConfigOnly = true\n')
        self.run_ok(['git', 'config', '-f', config, 'gpg.ssh.allowedSignersFile', signers])
        for i in self.ids:
            fragment = parent / 'identities' / ('config_' + i['key_hash'] + '_' + i['item_id'])
            pubkey = self.home / '.ssh' / ('id_legacy_' + i['item_id'] + '.pub')
            pubkey.write_text(i['public_key'] + '\n')
            fragment.write_text('')
            for field in ('name', 'email'):
                self.run_ok(['git', 'config', '-f', fragment, 'user.' + field, i[field]])
            self.run_ok(
                ['git', 'config', '-f', fragment, 'user.signingkey', 'key::' + i['public_key']]
            )
            self.run_ok(
                [
                    'git',
                    'config',
                    '-f',
                    fragment,
                    'core.sshCommand',
                    'ssh -i '
                    + shlex.quote(str(pubkey))
                    + ' -o IdentitiesOnly=yes -o ControlPath=none',
                ]
            )
            route = i['dirs'].replace('~/', str(self.home) + '/', 1)
            self.run_ok(
                [
                    'git',
                    'config',
                    '-f',
                    config,
                    'includeIf.gitdir/i:' + route + '/**.path',
                    fragment,
                ]
            )
            self.run_ok(['git', 'init', '-q', self.repo(i)])
        self.assert_adopted(self.ids)

    def test_r05_second_output_failure_and_retry_keep_real_routing(self):
        self.adopt()
        old_ids = copy.deepcopy(self.ids)
        before = self.selected_snapshot()
        self.change_inputs()
        self.prepare()
        self.put_consumer()  # Actual target-before-generator ordering.
        self.failing_git()
        result = self.script(boundary.GEN)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.selected_snapshot(), before)
        self.assert_adopted(old_ids)
        self.unfail()
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        for identity in self.ids:
            self.run_ok(['git', 'init', '-q', self.repo(identity)])
        self.assert_adopted(self.ids)
        for identity in old_ids:
            self.assertIsNone(self.git_value(self.repo(identity), 'user.name'))

    def test_r05_signals_before_switch_and_kill_lock_preserve_old(self):
        self.adopt()
        old_ids = copy.deepcopy(self.ids)
        before = self.selected_snapshot()
        self.change_inputs()
        for sig in ('SIGTERM', 'SIGINT', 'SIGKILL'):
            with self.subTest(signal=sig):
                self.failing_git(sig)
                result = self.script(boundary.GEN)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.selected_snapshot(), before)
                self.assert_adopted(old_ids)
                self.unfail()
                lock = self.entry().parent / '.identity-writer-lock'
                if sig == 'SIGKILL':
                    self.assertTrue(lock.exists())
                    self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
                    lock.rmdir()  # Fixture-only simulation of explicit inspected recovery.
                else:
                    self.assertFalse(lock.exists())
        self.assertEqual(self.script(boundary.GEN).returncode, 0)

    def test_r05_conversion_failure_missing_and_empty_input_preserve_old(self):
        self.adopt()
        before = self.selected_snapshot()
        self.write_data(wsl=True)
        boundary.executable(self.bin / 'wslpath', '#!/bin/sh\nexit 71\n')
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(self.selected_snapshot(), before)
        for ids in ([], None, {}):
            self.write_data(ids=ids) if ids is not None else self.write_data()
            if ids is None:
                data = json.loads(self.config.read_text())
                del data['data']['identities']
                self.config.write_text(json.dumps(data))
            result = self.render(boundary.GEN)
            if result.returncode == 0:
                result = self.command([boundary.ZSH], input=result.stdout)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(self.selected_snapshot(), before)
        self.write_data(ids=[])
        self.env['CI'] = 'true'
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(self.selected_snapshot(), before)
        del self.env['CI']
        self.assert_adopted(self.ids)
        self.assertEqual(self.script(boundary.GEN, '--clear').returncode, 0)
        self.assertEqual((self.generation() / 'allowed_signers').read_bytes(), b'')
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        for identity in self.ids:
            self.assertIsNone(self.git_value(self.repo(identity), 'user.email'))
        self.write_data()
        self.assertNotEqual(self.script(boundary.GEN, '--clear').returncode, 0)

    def test_r05_old_reader_references_survive_switch(self):
        self.adopt()
        repo = self.repo(self.ids[0])
        command = self.git_value(repo, 'core.sshcommand')
        signers = Path(self.git_value(repo, 'gpg.ssh.allowedsignersfile'))
        pubkey = Path(shlex.split(command)[2])
        old = {p: p.read_bytes() for p in (signers, pubkey)}
        self.change_inputs()
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        for path, content in old.items():
            self.assertEqual(path.read_bytes(), content)
        self.assertNotEqual(pubkey.parent, self.generation())

    def test_r05_legacy_migration_failure_reentry_and_unknown_files(self):
        self.legacy()
        old_ids = copy.deepcopy(self.ids)
        parent = self.entry().parent
        protected = [
            *list((parent / 'identities').iterdir()),
            *list((self.home / '.ssh').iterdir()),
            parent / 'allowed_signers',
        ]
        before = {p: (p.read_bytes(), p.stat().st_mode) for p in protected}
        self.change_inputs()
        self.prepare()
        entry = self.entry().read_bytes()
        self.prepare()  # Interrupted after preparation but before target is safe.
        self.assertEqual(self.entry().read_bytes(), entry)
        self.put_consumer()
        self.failing_git()
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assert_adopted(old_ids)
        self.unfail()
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual({p: (p.read_bytes(), p.stat().st_mode) for p in protected}, before)

    def test_r05_unknown_entry_symlink_and_modified_generation_refused(self):
        parent = self.entry().parent
        self.entry().write_text('unknown entry\n')
        for template in (PREPARE, boundary.GEN):
            self.assertNotEqual(self.script(template).returncode, 0)
            self.assertEqual(self.entry().read_text(), 'unknown entry\n')
        self.entry().unlink()
        foreign = self.root / 'foreign'
        foreign.write_text('foreign\n')
        self.entry().symlink_to(foreign)
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(foreign.read_text(), 'foreign\n')
        self.entry().unlink()
        unknown_dir = parent / '.identity-generation-unknown'
        unknown_dir.mkdir()
        (unknown_dir / 'precious').write_text('keep\n')
        self.adopt()
        self.assertEqual((unknown_dir / 'precious').read_text(), 'keep\n')
        key = self.keypath(self.ids[0])
        key.write_text('manually edited\n')
        before = self.entry().read_bytes()
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(key.read_text(), 'manually edited\n')
        self.assertEqual(self.entry().read_bytes(), before)

    def test_r05_before_failure_prevents_target_change_and_retry(self):
        self.legacy()
        original = (self.home / '.config/git/config').read_bytes()
        # Reduced source: only real before, Git target and real generator after.
        reduced = self.root / 'reduced'
        reduced.mkdir()
        shutil.copytree(self.source / '.chezmoitemplates', reduced / '.chezmoitemplates')
        (reduced / '.chezmoiscripts').mkdir()
        shutil.copy2(self.source / PREPARE, reduced / PREPARE)
        (reduced / 'dot_config/git').mkdir(parents=True)
        shutil.copy2(self.source / boundary.GIT, reduced / boundary.GIT)
        shutil.copy2(
            self.source / boundary.GEN, reduced / '.chezmoiscripts/run_after_identity.sh.tmpl'
        )
        self.source = reduced
        old_ids = copy.deepcopy(self.ids)
        self.change_inputs()
        self.entry().write_text('unknown\n')
        failed = self.chezmoi('apply', '--force')
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual((self.home / '.config/git/config').read_bytes(), original)
        self.assert_adopted(old_ids)
        self.entry().unlink()
        self.failing_git()
        failed = self.chezmoi('apply', '--force')
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('identity.inc', (self.home / '.config/git/config').read_text())
        self.assert_adopted(old_ids)
        self.unfail()
        succeeded = self.chezmoi('apply', '--force')
        self.assertEqual(succeeded.returncode, 0, succeeded.stderr)
        for i in self.ids:
            self.run_ok(['git', 'init', '-q', self.repo(i)])
        self.assert_adopted(self.ids)

    def test_r05_legacy_modified_after_preparation_is_not_silently_replaced(self):
        self.legacy()
        self.prepare()
        before = self.entry().read_bytes()
        config = self.home / '.config/git/config'
        self.run_ok(
            ['git', 'config', '-f', config, 'includeIf.gitdir/i:/new-manual/**.path', str(self.old)]
        )
        changed = config.read_bytes()
        result = self.script(PREPARE)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_bytes(), changed)
        self.assertEqual(self.entry().read_bytes(), before)

    def test_r05_direct_generator_refuses_unmigrated_or_missing_consumer(self):
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assertFalse(self.entry().exists())
        self.legacy()
        before = (self.home / '.config/git/config').read_bytes()
        self.prepare()
        entry = self.entry().read_bytes()
        self.change_inputs()
        result = self.script(boundary.GEN)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not migrated', result.stderr)
        self.assertEqual((self.home / '.config/git/config').read_bytes(), before)
        self.assertEqual(self.entry().read_bytes(), entry)

    def test_r05_interrupted_before_staging_and_retry(self):
        self.legacy()
        original = (self.home / '.config/git/config').read_bytes()
        real = self.run_ok(['/usr/bin/which', 'git']).strip()
        self.env['REAL_GIT'] = real
        boundary.executable(
            self.bin / 'git',
            '''#!/usr/bin/python3
import os,signal,sys
if '--list' in sys.argv and any(arg.endswith('/dispatch') for arg in sys.argv):
    os.kill(os.getppid(), signal.SIGTERM)
    sys.exit(73)
os.execv(os.environ['REAL_GIT'], [os.environ['REAL_GIT'], *sys.argv[1:]])
''',
        )
        self.assertNotEqual(self.script(PREPARE).returncode, 0)
        self.assertFalse(self.entry().exists())
        self.assertEqual((self.home / '.config/git/config').read_bytes(), original)
        self.assert_adopted(self.ids)
        (self.bin / 'git').unlink()
        self.prepare()
        self.put_consumer()
        self.assert_adopted(self.ids)

    def test_r05_missing_python_stops_before_any_migration_write(self):
        rendered = self.render(PREPARE)
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        self.legacy()
        original = (self.home / '.config/git/config').read_bytes()
        old_path = self.env['PATH']
        self.env['PATH'] = str(self.bin)
        result = self.command(['/bin/sh'], input=rendered.stdout)
        self.env['PATH'] = old_path
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Python 3.9+', result.stderr)
        self.assertFalse(self.entry().exists())
        self.assertEqual((self.home / '.config/git/config').read_bytes(), original)
        self.assert_adopted(self.ids)

    def test_r05_fresh_ci_empty_has_no_stub_and_non_ci_fails(self):
        self.write_data(ids=[])
        self.prepare()
        self.put_consumer()
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.env['CI'] = 'true'
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        self.assertNotIn('FALLBACK', (self.generation() / 'dispatch').read_text())
        self.assertEqual(list(self.generation().glob('id_*')), [])
        self.assertFalse((self.home / '.config/git/allowed_signers').exists())


def load_tests(loader, tests, pattern):
    # Reuse the fixture helpers, not the inherited R02/R04 test cases.
    return unittest.TestSuite(
        Transaction(name) for name in Transaction.__dict__ if name.startswith('test_r05_')
    )


if __name__ == '__main__':
    unittest.main(verbosity=2)

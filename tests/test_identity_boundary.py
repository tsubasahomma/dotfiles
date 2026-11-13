#!/usr/bin/env python3
"""R02: isolated producer, template, generator and real Git consumer checks.

Requires installed chezmoi, zsh, Git and ssh-keygen. No real op/auth/apply.
"""

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import socket
import subprocess
import tempfile
import threading
import tomllib
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
ZSH = shutil.which('zsh')
REPAIR = 'dot_config/mise/repo-tasks/repair/executable_security.tmpl'
WRAPPER = '.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl'
WSL_CHECK = 'dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl'
GEN = 'dot_config/mise/repo-tasks/generate/executable_identity.tmpl'
GIT = 'dot_config/git/config.tmpl'
CHECK = 'dot_config/mise/repo-tasks/check/executable_identity.tmpl'
AGENT = 'dot_config/1Password/ssh/private_agent.toml.tmpl'


def executable(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(0o700)


class IdentityBoundary(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI and ZSH)
        self.tmp = tempfile.TemporaryDirectory(prefix='r02-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        # Shell metacharacters, apostrophe and spaces in real output paths.
        self.home = self.root / "home ' \"quoted\" $(touch HOME_PWN) `touch HOME_BT`"
        self.home.mkdir()
        self.source = self.root / 'source'
        shutil.copytree(REPO, self.source, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        (self.source / '.chezmoiexternal.toml.tmpl').write_text('')
        producer = self.source / '.chezmoi.toml.tmpl'
        text = producer.read_text()
        hook = '\n[hooks.read-source-state.pre]'
        self.assertEqual(text.count(hook), 1)
        producer.write_text(text.split(hook)[0] + '\n')
        self.bin = self.root / "bin ' quote"
        self.bin.mkdir()
        self.config = self.root / 'config.json'
        self.env = {
            'HOME': str(self.home),
            'PATH': f'{self.bin}:/usr/bin:/bin',
            'XDG_CONFIG_HOME': str(self.home / '.config'),
            'XDG_CACHE_HOME': str(self.home / '.cache'),
            'XDG_DATA_HOME': str(self.home / '.local/share'),
            'XDG_STATE_HOME': str(self.home / '.local/state'),
            'TMPDIR': str(self.root),
            'LC_ALL': 'C',
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': str(self.home / '.config/git/config'),
            'FIXTURE': str(self.root / 'items.json'),
            'ARGV_LOG': str(self.root / 'argv.json'),
        }
        self.run_ok(
            [
                'ssh-keygen',
                '-q',
                '-t',
                'ed25519',
                '-N',
                '',
                '-C',
                'fixture',
                '-f',
                str(self.root / 'key'),
            ]
        )
        self.key = (self.root / 'key.pub').read_text().strip().rsplit(' ', 1)[0]
        self.ids = [
            self.identity('alpha', "~/work ' $(touch ROUTE_PWN) `touch ROUTE_BT`"),
            self.identity('beta', '~/other'),
        ]
        self.paths = {
            'home': str(self.home),
            'xdg_config': str(self.home / '.config'),
            'op': str(self.bin / 'op'),
            'op_sign': '/fixture/sign-helper',
            'mise': str(self.home / '.local/bin/mise'),
            'xdg_data': str(self.home / '.local/share'),
            'xdg_state': str(self.home / '.local/state'),
            'xdg_cache': str(self.home / '.cache'),
        }
        (self.home / '.ssh').mkdir()
        (self.home / '.config/git/identities').mkdir(parents=True)
        self.old = self.home / '.config/git/identities/old'
        self.old.write_text('old usable config\n')
        self.write_data()

    def identity(self, label, dirs):
        key = (
            self.key
            + ' '
            + label
            + ' $(touch KEY_PWN) `touch KEY_BT` "quote" \\backslash #semi; EOF'
        )
        return {
            'item_id': label,
            'account_id': 'fixture-account',
            'key_type': 'ed25519',
            'key_hash': hashlib.sha256(key.encode()).hexdigest()[:8],
            'public_key': key,
            'name': label + ' 日本語 " \' $(touch NAME_PWN) `touch NAME_BT` # ; \\  ',
            'email': label + "+tag'$`@example.test",
            'dirs': dirs,
        }

    def command(self, args, **kwargs):
        return subprocess.run(
            [str(x) for x in args],
            env=self.env,
            cwd=self.root,
            text=True,
            capture_output=True,
            **kwargs,
        )

    def run_ok(self, args, **kwargs):
        result = self.command(args, **kwargs)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def write_data(self, ids=None, wsl=False):
        self.config.write_text(
            json.dumps(
                {
                    'data': {
                        'identities': self.ids if ids is None else ids,
                        'paths': self.paths,
                        'is_wsl': wsl,
                        'ssh_auth_sock': r'\\.\pipe\openssh-ssh-agent' if wsl else '',
                    }
                }
            )
        )

    def chezmoi(self, *args, **kwargs):
        return self.command(
            [
                CHEZMOI,
                '--config',
                self.config,
                '--source',
                self.source,
                '--destination',
                self.home,
                '--cache',
                self.home / '.cache/chezmoi',
                '--no-tty',
                '--color=false',
                *args,
            ],
            **kwargs,
        )

    def render(self, path):
        return self.chezmoi('execute-template', input=(self.source / path).read_text())

    def generate(self, wsl=False):
        self.write_data(wsl=wsl)
        result = self.render(GEN)
        self.assertEqual(result.returncode, 0, result.stderr)
        script = self.root / 'identity.zsh'
        script.write_text(result.stdout)
        self.run_ok([ZSH, '-n', script])
        repair = self.render(REPAIR)
        self.assertEqual(repair.returncode, 0, repair.stderr)
        private_fixture = self.home / '.ssh/id_fixture_private'
        private_fixture.write_text('fixture only')
        private_fixture.chmod(0o640)
        self.run_ok(['/bin/bash'], input=repair.stdout)
        self.assertEqual(private_fixture.stat().st_mode & 0o777, 0o640)
        self.assertEqual(private_fixture.read_text(), 'fixture only')
        private_fixture.unlink()
        self.prepare_consumer()
        self.run_ok([ZSH, script])

    def prepare_consumer(self):
        result = self.render('.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.run_ok(['/bin/sh'], input=result.stdout)
        result = self.render(GIT)
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.home / '.config/git/config').write_text(result.stdout)

    def generation(self):
        entry = self.home / '.config/git/identity.inc'
        return Path(self.run_ok(['git', 'config', '-f', entry, 'include.path']).strip()).parent

    def keypath(self, identity):
        return (
            self.generation()
            / f"id_{identity['key_type']}_{identity['email']}_{identity['key_hash']}.pub"
        )

    def git_value(self, repo, key):
        result = self.command(['git', '-C', repo, 'config', '--get', key])
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.stdout.removesuffix('\n') if result.returncode == 0 else None

    def test_literal_values_routing_and_ssh_argv(self):
        self.generate()
        executable(
            self.bin / 'ssh',
            '#!/usr/bin/python3\nimport json,os,sys\nopen(os.environ["ARGV_LOG"],"w").write(json.dumps(sys.argv[1:]))\n',
        )
        expected_files = set()
        for identity in self.ids:
            route = identity['dirs'].replace('~/', str(self.home) + '/', 1)
            repo = Path(route) / 'project'
            self.run_ok(['git', 'init', '-q', repo])
            for field in ('name', 'email'):
                self.assertEqual(self.git_value(repo, 'user.' + field), identity[field])
            self.assertEqual(
                self.git_value(repo, 'user.signingkey'), 'key::' + identity['public_key']
            )
            command = self.git_value(repo, 'core.sshcommand')
            self.run_ok(['/bin/sh', '-c', command])
            keypath = self.keypath(identity)
            expected_files.add(keypath.name)
            self.assertEqual(
                json.loads((self.root / 'argv.json').read_text()),
                ['-i', str(keypath), '-o', 'IdentitiesOnly=yes', '-o', 'ControlPath=none'],
            )
            self.command(['git', '-C', repo, 'ls-remote', 'ssh://fixture.invalid/repo'])
            git_argv = json.loads((self.root / 'argv.json').read_text())
            self.assertEqual(git_argv[git_argv.index('-i') + 1], str(keypath))
            self.assertIn('IdentitiesOnly=yes', git_argv)
            self.assertEqual(keypath.read_text(), identity['public_key'] + '\n')
            self.assertEqual(keypath.stat().st_mode & 0o777, 0o600)
            signers = self.generation() / 'allowed_signers'
            self.assertIn(
                identity['email'] + ' namespaces="git" ' + identity['public_key'],
                signers.read_text(),
            )
            self.assertEqual(signers.stat().st_mode & 0o777, 0o644)
            self.assertEqual(
                self.run_ok(
                    ['ssh-keygen', '-Y', 'match-principals', '-I', identity['email'], '-f', signers]
                ).strip(),
                identity['email'],
            )
        self.assertEqual({p.name for p in self.generation().glob('id_*.pub')}, expected_files)
        for location in ('outside', 'other-sibling', 'work-sibling'):
            repo = self.home / location
            self.run_ok(['git', 'init', '-q', repo])
            for key in ('user.name', 'user.email', 'user.signingkey', 'core.sshcommand'):
                self.assertIsNone(self.git_value(repo, key))
            self.command(['git', '-C', repo, 'ls-remote', 'ssh://fixture.invalid/repo'])
            self.assertNotIn('-i', json.loads((self.root / 'argv.json').read_text()))
        executable(self.bin / 'op', '#!/bin/sh\nexit 0\n')
        executable(self.bin / 'ssh-add', '#!/bin/sh\nexit 1\n')
        self.env['CI'] = 'true'
        check = self.render(CHECK)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.run_ok(['/bin/bash', '-n'], input=check.stdout)
        self.run_ok(['/bin/bash'], input=check.stdout)
        wsl_check = self.render(WSL_CHECK)
        self.assertEqual(wsl_check.returncode, 0, wsl_check.stderr)
        self.run_ok(['/bin/bash'], input=wsl_check.stdout)
        agent = self.render(AGENT)
        self.assertEqual(agent.returncode, 0, agent.stderr)
        self.assertEqual(len(tomllib.loads(agent.stdout)['ssh-keys']), len(self.ids))
        # Use exact marker paths; directory names deliberately contain their text.
        for name in (
            'HOME_PWN',
            'HOME_BT',
            'KEY_PWN',
            'KEY_BT',
            'NAME_PWN',
            'NAME_BT',
            'ROUTE_PWN',
            'ROUTE_BT',
        ):
            self.assertFalse((self.root / name).exists())

    def test_absolute_routes_trim_and_trailing_slash(self):
        route = self.root / 'absolute "quoted" 日本語 path'
        other = self.root / 'second route'
        self.ids = [self.identity('alpha', f'  {route}/ , {other}  ')]
        self.generate()
        for location, expected in (
            (route, True),
            (route / 'nested', True),
            (other, True),
            (Path(str(route) + '-sibling'), False),
        ):
            self.run_ok(['git', 'init', '-q', location])
            self.assertEqual(
                self.git_value(location, 'user.email'), self.ids[0]['email'] if expected else None
            )

    def test_invalid_set_rejected_by_every_consumer_before_outputs(self):
        changes = [
            ('dirs', value)
            for value in (
                '~/work,',
                '~/work,,~/other',
                ' ',
                ',~/work',
                'relative',
                '/',
                '/**',
                '~/work/*',
                '~/work/?',
                '~/work/[a]',
                '~/work/../other',
                '~/work//nested',
                '~/work//',
                '~/work/./child',
                '~/work/\\escape',
                '~/work,~/work/',
                '~/work,~/WORK/child',
                '~/work/child,~/work',
            )
        ]
        changes += [
            ('name', '\nEOF\ntouch BAD\n'),
            ('name', '  '),
            ('name', 'tab\tname'),
            ('name', 'nul\x00name'),
            ('email', '../../escape@example.test'),
            ('email', '*@example.test'),
            ('email', 'a?@example.test'),
            ('email', 'a,b@example.test'),
            ('email', 'a b@example.test'),
            ('email', 'a%h@example.test'),
            ('email', 'a${HOME}@example.test'),
            ('email', 'a|b@example.test'),
            ('email', '!a@example.test'),
            ('key_type', '../../escape'),
            ('key_hash', '../escape'),
            ('public_key', 'ssh-ed25519 AAAA broken'),
            ('public_key', self.key + '\nEOF\ntouch BAD\n'),
            ('dirs', '~/work\n[include]'),
        ]
        before = self.old.read_bytes()
        for field, value in changes:
            with self.subTest(field=field, value=value):
                ids = copy.deepcopy(self.ids)
                ids[-1][field] = value
                if field == 'public_key':
                    ids[-1]['key_hash'] = hashlib.sha256(value.encode()).hexdigest()[:8]
                self.write_data(ids)
                for consumer in (GEN, GIT, CHECK, AGENT):
                    result = self.render(consumer)
                    self.assertNotEqual(result.returncode, 0, consumer)
                    self.assertRegex(result.stderr, r'identity [0-9]+:')
                self.assertEqual(self.old.read_bytes(), before)
                self.assertEqual(list((self.home / '.ssh').iterdir()), [])
        for invalid in ({}, None, 'invalid', False):
            self.write_data()
            data = json.loads(self.config.read_text())
            data['data']['identities'] = invalid
            self.config.write_text(json.dumps(data))
            for consumer in (GEN, GIT, CHECK, AGENT):
                self.assertNotEqual(self.render(consumer).returncode, 0)
        for ids in (
            [self.ids[0], self.ids[0]],
            [self.ids[0], dict(self.ids[1], dirs=self.ids[0]['dirs'] + '/nested')],
        ):
            self.write_data(ids)
            self.assertNotEqual(self.render(GEN).returncode, 0)

    def test_wsl_command_preserves_converted_path(self):
        winpath = "C:\\Users\\O'Brien $(touch WIN_PWN) `touch WIN_BT`\\.ssh"
        self.env['WINDOWS_KEY_PATH'] = winpath
        executable(
            self.bin / 'wslpath',
            '#!/bin/sh\n[ -d "$2" ] || exit 71\nprintf "%s\\n" "$WINDOWS_KEY_PATH"\n',
        )
        executable(
            self.bin / 'ssh.exe',
            '#!/usr/bin/python3\nimport json,os,sys\nopen(os.environ["ARGV_LOG"],"w").write(json.dumps(sys.argv[1:]))\n',
        )
        self.generate(wsl=True)
        # R08: inspect the full generated WSL binding without auth/path-conversion probes.
        check = self.render(CHECK)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.run_ok(['/bin/bash'], input=check.stdout)
        cfg = next(self.generation().glob('config_*'))
        command = self.run_ok(['git', 'config', '-f', cfg, 'core.sshCommand']).strip()
        self.run_ok(['/bin/sh', '-c', command])
        identity = next(i for i in self.ids if cfg.name == f"config_{i['email']}_{i['key_hash']}")
        filename = f"id_{identity['key_type']}_{identity['email']}_{identity['key_hash']}.pub"
        self.assertEqual(
            json.loads((self.root / 'argv.json').read_text()),
            [
                '-i',
                winpath + '\\' + filename,
                '-o',
                'IdentitiesOnly=yes',
                '-o',
                'ControlPath=none',
                '-o',
                r'IdentityAgent="\\\\.\\pipe\\openssh-ssh-agent"',
            ],
        )
        self.assertFalse((self.root / 'WIN_PWN').exists())
        self.assertFalse((self.root / 'WIN_BT').exists())
        # POSIX parser evidence only: Windows runtime/interop remains untested.
        output = self.run_ok(
            ['/usr/bin/ssh', '-G', '-F', '/dev/null', *shlex.split(command)[1:], 'fixture.invalid']
        )
        self.assertIn('identityagent ' + r'\\.\pipe\openssh-ssh-agent' + '\n', output)
        self.assertNotIn('controlpath ', output)
        for order in (self.ids, list(reversed(self.ids))):
            for identity in order:
                repo = Path(identity['dirs'].replace('~/', str(self.home) + '/', 1)) / 'project'
                self.run_ok(['git', 'init', '-q', repo])
                self.command(['git', '-C', repo, 'ls-remote', 'git@fixture.invalid:repo'])
                argv = json.loads((self.root / 'argv.json').read_text())
                self.assertEqual(
                    argv[argv.index('-i') + 1],
                    winpath
                    + '\\'
                    + f"id_{identity['key_type']}_{identity['email']}_{identity['key_hash']}.pub",
                )
                self.assertIn('ControlPath=none', argv)
                self.assertIn(r'IdentityAgent="\\\\.\\pipe\\openssh-ssh-agent"', argv)
        # Execute only the generated shape checks, without their auth/network probes.
        for template, var, options in (
            (CHECK, 'CORE_SSH_COMMAND', 'SSH_IDENTITY_OPTIONS'),
            (WSL_CHECK, 'core_ssh_command', 'ssh_identity_options'),
        ):
            rendered = self.render(template)
            self.assertEqual(rendered.returncode, 0, rendered.stderr)
            self.run_ok(['/bin/bash', '-n'], input=rendered.stdout)
            assignment = next(
                line.strip().removeprefix('local ')
                for line in rendered.stdout.splitlines()
                if line.strip().removeprefix('local ').startswith(options + '=')
            )
            block = re.search(r'case "\$' + var + r'" in.*?esac', rendered.stdout, re.S).group()
            for value, valid in (
                (command, True),
                (command.replace('ControlPath=none', 'ControlPath=/wrong'), False),
            ):
                script = (
                    'log_ok() { :; }; log_guide() { :; }; log_err() { exit 41; }; record_error() { exit 41; };\n'
                    + var
                    + '='
                    + shlex.quote(value)
                    + '\n'
                    + assignment
                    + '\n'
                    + block
                )
                result = self.command(['/bin/bash'], input=script)
                self.assertEqual(result.returncode, 0 if valid else 41, result.stderr)

    def test_openssh_loads_literal_public_key_without_network(self):
        self.generate()
        identity = self.ids[0]
        cfg = self.generation() / f"config_{identity['email']}_{identity['key_hash']}"
        command = self.run_ok(['git', 'config', '-f', cfg, 'core.sshCommand']).strip()
        # ProxyCommand false prevents network; no agent or known_hosts use.
        args = shlex.split(command)
        args[0] = '/usr/bin/ssh'
        result = self.command(
            args
            + [
                '-vvv',
                '-F',
                '/dev/null',
                '-o',
                'IdentityAgent=none',
                '-o',
                'UserKnownHostsFile=none',
                '-o',
                'GlobalKnownHostsFile=none',
                '-o',
                'ProxyCommand=/bin/false',
                'localhost',
            ]
        )
        self.assertNotEqual(result.returncode, 0)  # Deliberately no server.
        keypath = self.keypath(identity)
        self.assertIn(f'identity file {keypath} type ', result.stderr)
        self.assertNotIn(f'identity file {keypath} type -1', result.stderr)
        self.assertNotIn('unknown key %', result.stderr)

    def test_unsupported_ssh_path_expansion_rejected_before_writes(self):
        for home in (str(self.home) + '%h', str(self.home) + '${HOME}'):
            with self.subTest(home=home):
                self.paths['home'] = home
                self.write_data()
                self.assertNotEqual(self.render(GEN).returncode, 0)
                self.assertTrue(self.old.exists())
        self.paths['home'] = str(self.home)
        self.write_data(wsl=True)
        self.prepare_consumer()
        for converted in (
            'C:\\Users\\key%h.pub',
            'C:\\Users\\key${HOME}.pub',
            'C:\\Users\\bad\nkey.pub',
            '',
        ):
            with self.subTest(converted=converted):
                self.env['WINDOWS_KEY_PATH'] = converted
                executable(
                    self.bin / 'wslpath',
                    '#!/bin/sh\n[ -d "$2" ] || exit 71\nprintf "%s\\n" "$WINDOWS_KEY_PATH"\n',
                )
                result = self.render(GEN)
                self.assertEqual(result.returncode, 0, result.stderr)
                result = self.command([ZSH], input=result.stdout)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('unsupported converted OpenSSH path', result.stderr)
                self.assertEqual(self.old.read_text(), 'old usable config\n')
                self.assertEqual(list((self.home / '.ssh').iterdir()), [])

    def test_post_apply_caller_with_stub_mise_and_identity_entry(self):
        for name, template in [('repair', REPAIR), ('generate', GEN)]:
            rendered = self.render(template)
            self.assertEqual(rendered.returncode, 0, rendered.stderr)
            (self.root / name).write_text(rendered.stdout)
        self.env['FIXTURE_ROOT'] = str(self.root)
        self.env['ZSH_BIN'] = str(ZSH)
        executable(
            Path(self.paths['mise']),
            '''#!/usr/bin/python3
import json, os, subprocess, sys
root = os.environ['FIXTURE_ROOT']
with open(root + '/mise-calls', 'a') as log:
    log.write(json.dumps(sys.argv[1:]) + '\\n')
assert os.environ['XDG_CONFIG_HOME'] == os.environ['HOME'] + '/.config'
if sys.argv[1:] == ['install']: pass
elif sys.argv[1:] == ['run', 'lifecycle:post-apply']:
    subprocess.run(['/bin/bash', root + '/repair'], check=True)
else: sys.exit(77)
''',
        )
        self.prepare_consumer()
        identity = self.render('.chezmoiscripts/run_after_10-identity.sh.tmpl')
        self.assertEqual(identity.returncode, 0, identity.stderr)
        self.run_ok(['/bin/sh'], input=identity.stdout)
        selected = self.generation()
        wrapper = self.render(WRAPPER)
        self.assertEqual(wrapper.returncode, 0, wrapper.stderr)
        self.run_ok(['/bin/bash'], input=wrapper.stdout)
        self.assertEqual(
            (self.root / 'mise-calls').read_text().splitlines(),
            ['["install"]', '["run", "lifecycle:post-apply"]'],
        )
        self.assertTrue(self.old.exists())
        self.assertEqual(self.generation(), selected)
        self.assertNotIn(
            'generate:identity',
            (
                self.source / 'dot_config/mise/repo-tasks/lifecycle/executable_post-apply.tmpl'
            ).read_text(),
        )
        self.assertEqual(len(list(self.generation().glob('id_*.pub'))), len(self.ids))
        self.assertFalse((self.root / 'HOME_PWN').exists())
        self.assertFalse((self.root / 'HOME_BT').exists())

    def test_shared_ssh_paths_parse_and_wsl_agent_delivery(self):
        included = self.home / '.config/ssh/conf.d/github'
        included.parent.mkdir(parents=True)
        included.write_text(self.render('dot_config/ssh/conf.d/github.tmpl').stdout)
        rendered = self.render('dot_config/ssh/config.tmpl')
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        ssh_config = self.root / 'ssh_config'
        ssh_config.write_text(rendered.stdout)
        output = self.run_ok(['/usr/bin/ssh', '-G', '-F', ssh_config, 'github.com'])
        self.assertIn('user git\n', output)
        self.assertIn('controlpath ' + self.paths['xdg_state'] + '/ssh/sockets/', output)
        self.assertIn('userknownhostsfile ' + self.paths['xdg_state'] + '/ssh/known_hosts', output)
        self.write_data(wsl=True)
        rendered = self.render(AGENT)
        agent = self.home / '.config/1Password/ssh/agent.toml'
        agent.parent.mkdir(parents=True)
        agent.write_text(rendered.stdout)
        from test_windows_config_sync import install_windows_stubs

        winhome = self.root / "Windows ' home"
        winhome.mkdir()
        local = self.root / "Redirected ' Local"
        local.mkdir()
        install_windows_stubs(self.bin, self.env, winhome, local)
        sync = self.render('dot_config/mise/repo-tasks/sync/executable_1password-agent.tmpl')
        self.assertEqual(sync.returncode, 0, sync.stderr)
        self.run_ok(['/bin/bash'], input=sync.stdout)
        destination = local / '1Password/config/ssh/agent.toml'
        self.assertEqual(destination.read_bytes(), agent.read_bytes())
        self.assertFalse((winhome / 'AppData').exists())
        self.assertFalse((self.root / 'HOME_PWN').exists())
        self.assertFalse((self.root / 'HOME_BT').exists())

    def test_producer_validates_tagged_items_and_preserves_old_config(self):
        executable(
            self.bin / 'op',
            '''#!/usr/bin/python3
import json, os, sys
args = sys.argv[1:]
if args == ['account', 'get']: pass
elif args[:2] == ['account', 'list']: print(os.environ.get('ACCOUNT_LIST', '[{"account_uuid":"fixture-account"}]'))
elif args[:2] == ['item', 'list']: print(os.environ.get('ITEM_LIST', '[{"id":"fixture-item"}]'))
elif args[:2] == ['item', 'get']: print(open(os.environ['FIXTURE']).read())
else: sys.exit(70)
''',
        )
        executable(self.home / '.local/bin/mise', '#!/bin/sh\nexit 0\n')
        item = self.ids[0]

        def write_item(item):
            fields = [
                {
                    'label': 'dotfiles_git_' + name,
                    'value': item[name],
                    'section': {'label': 'dotfiles'},
                }
                for name in ('name', 'email', 'dirs')
            ]
            fields += [
                {'label': 'public key', 'value': item['public_key']},
                {'label': 'key type', 'value': 'Ed25519'},
            ]
            (self.root / 'items.json').write_text(json.dumps({'fields': fields}))

        write_item(item)
        self.config = self.root / 'producer.toml'
        result = self.chezmoi('init')
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = tomllib.loads(self.config.read_text())
        self.assertNotIn('hooks', parsed)
        self.assertEqual(parsed['data']['identities'][0]['public_key'], item['public_key'])
        self.assertEqual(parsed['data']['identities'][0]['name'], item['name'])
        before = self.config.read_bytes()
        for key in ('ACCOUNT_LIST', 'ITEM_LIST'):
            if key == 'ACCOUNT_LIST':
                self.env['ITEM_LIST'] = '[]'  # Invalid account must not become a valid empty set.
            field = 'account_uuid' if key == 'ACCOUNT_LIST' else 'id'
            invalid_lists = ['null', '{}', '', '[null]', 'false', '"bad"']
            invalid_lists += [
                json.dumps([{field: value}]) for value in ('', '   ', '\n', None, 123)
            ]
            for value in invalid_lists:
                with self.subTest(key=key, value=value):
                    self.env[key] = value
                    result = self.chezmoi('init')
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.config.read_bytes(), before)
            del self.env[key]
            if key == 'ACCOUNT_LIST':
                del self.env['ITEM_LIST']
        for field, value in [
            ('dirs', '~/work,'),
            ('name', ''),
            ('email', '../../bad@example.test'),
            ('public_key', self.key + '\nEOF'),
        ]:
            with self.subTest(field=field):
                write_item(dict(item, **{field: value}))
                result = self.chezmoi('init')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.config.read_bytes(), before)

    def test_r04_agent_contract_without_environment(self):
        data = json.loads(self.config.read_text())
        agent = str(self.home / 'agent "quote" \\ literal.sock')
        data['data']['ssh_auth_sock'] = agent
        # A stale nested key must not win over the producer's root key.
        data['data']['paths']['ssh_auth_sock'] = '/wrong/nested.sock'
        self.config.write_text(json.dumps(data))
        rendered = self.render('dot_config/ssh/config.tmpl')
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        config = self.root / 'ssh_config'
        config.write_text(rendered.stdout)
        for env_sock in (None, '/wrong/environment.sock'):
            if env_sock is None:
                self.env.pop('SSH_AUTH_SOCK', None)
            else:
                self.env['SSH_AUTH_SOCK'] = env_sock
            output = self.run_ok(['/usr/bin/ssh', '-G', '-F', config, 'fixture.invalid'])
            self.assertIn('identityagent ' + agent + '\n', output)
        for invalid in (
            'relative.sock',
            r'\\.\pipe\openssh-ssh-agent',
            '/tmp/%h',
            '/tmp/${HOME}',
            '/tmp/bad\npath',
        ):
            data['data']['ssh_auth_sock'] = invalid
            self.config.write_text(json.dumps(data))
            self.assertNotEqual(self.render('dot_config/ssh/config.tmpl').returncode, 0)
        data['data']['is_wsl'] = True
        data['data']['ssh_auth_sock'] = r'\\.\pipe\openssh-ssh-agent'
        self.config.write_text(json.dumps(data))
        config.write_text(self.render('dot_config/ssh/config.tmpl').stdout)
        output = self.run_ok(['/usr/bin/ssh', '-G', '-F', config, 'fixture.invalid'])
        self.assertIn('identityagent none\n', output)

    def test_r04_real_openssh_does_not_contact_shared_master(self):
        # Different key material, not just different comments or filenames.
        self.run_ok(
            [
                'ssh-keygen',
                '-q',
                '-t',
                'ed25519',
                '-N',
                '',
                '-C',
                'fixture-b',
                '-f',
                self.root / 'key-b',
            ]
        )
        self.key = (self.root / 'key-b.pub').read_text().strip().rsplit(' ', 1)[0]
        self.ids[1] = self.identity('beta', '~/other')
        self.generate()
        # A short isolated socket avoids AF_UNIX sun_path limits on macOS.
        with tempfile.TemporaryDirectory(prefix='r04-mux-', dir='/tmp') as sockdir:
            sockpath = str(Path(sockdir) / 'master')
            config = self.root / 'ssh_config'
            config.write_text(
                'Host *\n ControlMaster auto\n ControlPath ' + sockpath + '\n'
                ' IdentityAgent none\n UserKnownHostsFile none\n GlobalKnownHostsFile none\n'
                ' ProxyCommand /bin/false\n BatchMode yes\n'
            )
            self.env['SSH_FIXTURE_CONFIG'] = str(config)
            # Git invokes this wrapper with its real argv, then runs real OpenSSH.
            executable(
                self.bin / 'ssh',
                '''#!/usr/bin/python3
import json, os, sys
open(os.environ['ARGV_LOG'], 'w').write(json.dumps(sys.argv[1:]))
os.execv('/usr/bin/ssh', ['/usr/bin/ssh', '-vvv', '-F', os.environ['SSH_FIXTURE_CONFIG']] + sys.argv[1:])
''',
            )
            repos = []
            for identity in self.ids:
                repo = Path(identity['dirs'].replace('~/', str(self.home) + '/', 1)) / 'project'
                self.run_ok(['git', 'init', '-q', repo])
                repos.append(repo)
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
                listener.bind(sockpath)
                listener.listen(8)
                listener.settimeout(0.1)
                observed = []
                stop = threading.Event()

                def accept_mux():
                    while not stop.is_set():
                        try:
                            conn, _ = listener.accept()
                        except TimeoutError:
                            continue
                        with conn:
                            conn.settimeout(2)
                            observed.append(conn.recv(1024))

                worker = threading.Thread(target=accept_mux)
                worker.start()
                try:
                    # Positive controls prove the socket can detect the regression.
                    # ControlMaster=no alone still tries an existing master.
                    for extra in ('', ' -o ControlMaster=no'):
                        command = (
                            self.git_value(repos[0], 'core.sshcommand').replace(
                                ' -o ControlPath=none', ''
                            )
                            + extra
                        )
                        result = self.command(
                            [
                                'git',
                                '-C',
                                repos[0],
                                '-c',
                                'core.sshCommand=' + command,
                                'ls-remote',
                                'git@fixture.invalid:repo',
                            ],
                            timeout=10,
                        )
                        self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(len(observed), 2)
                    self.assertTrue(
                        all(
                            packet[:12] == b'\x00\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x04'
                            for packet in observed
                        )
                    )
                    for order in ((0, 1), (1, 0)):
                        for index in order:
                            result = self.command(
                                [
                                    'git',
                                    '-C',
                                    repos[index],
                                    'ls-remote',
                                    'git@fixture.invalid:repo',
                                ],
                                timeout=10,
                            )
                            self.assertNotEqual(result.returncode, 0)  # No SSH server by design.
                            argv = json.loads((self.root / 'argv.json').read_text())
                            identity = self.ids[index]
                            keypath = self.keypath(identity)
                            self.assertEqual(argv[argv.index('-i') + 1], str(keypath))
                            self.assertIn('ControlPath=none', argv)
                            self.assertIn(f'identity file {keypath} type ', result.stderr)
                            self.assertNotIn(f'identity file {keypath} type -1', result.stderr)
                            self.assertNotIn('mux_client_hello_exchange', result.stderr)
                            self.assertEqual(len(observed), 2)
                finally:
                    stop.set()
                    worker.join(timeout=3)
                    self.assertFalse(worker.is_alive())


if __name__ == '__main__':
    unittest.main(verbosity=2)

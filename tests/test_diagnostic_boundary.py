#!/usr/bin/env python3
"""R08: hookless rendering and local probes in an isolated HOME/XDG.

No real authentication, network probe, package installation or workstation apply.
"""

import hashlib
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
MISE = os.environ.get('MISE_BIN') or shutil.which('mise')
NVIM = os.environ.get('NVIM_BIN') or shutil.which('nvim')


def executable(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    path.chmod(0o755)


def tree(path):
    result = {}
    for p in path.rglob('*'):
        mode = p.lstat().st_mode
        payload = (
            os.readlink(p)
            if p.is_symlink()
            else hashlib.sha256(p.read_bytes()).hexdigest()
            if p.is_file()
            else None
        )
        result[str(p.relative_to(path))] = (mode, payload)
    return result


class DiagnosticBoundary(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, 'installed chezmoi required')
        self.tmp = tempfile.TemporaryDirectory(prefix='r08-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.home = self.root / "home ' $(touch PWN) `literal`"
        self.home.mkdir()
        self.source = self.root / 'source'
        self.source.mkdir()
        shutil.copytree(REPO / '.chezmoitemplates', self.source / '.chezmoitemplates')
        self.config = self.root / 'config.json'
        self.paths = {
            'home': str(self.home),
            'mise': str(self.home / '.local/bin/mise'),
            'op': str(self.home / '.local/bin/op'),
        }
        for key, part in [
            ('config', '.config'),
            ('cache', '.cache'),
            ('data', '.local/share'),
            ('state', '.local/state'),
        ]:
            self.paths['xdg_' + key] = str(self.home / part)
        self.env = {
            'HOME': str(self.home),
            'PATH': f'{self.home}/.local/bin:/usr/bin:/bin',
            'LC_ALL': 'C',
            'TMPDIR': str(self.root),
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': str(self.home / '.gitconfig'),
            'CALLS': str(self.root / 'calls'),
            'MARKER': str(self.root / 'marker'),
        }
        for key in ['config', 'cache', 'data', 'state']:
            self.env[f'XDG_{key.upper()}_HOME'] = self.paths['xdg_' + key]
        self.data = {
            'paths': self.paths,
            'identities': [],
            'is_wsl': False,
            'ssh_auth_sock': '',
            'osid': 'darwin',
        }
        self.tasks = self.home / '.config/mise/repo-tasks'
        for category in ['check', 'probe', 'doctor']:
            for p in (REPO / 'dot_config/mise/repo-tasks' / category).glob('*.tmpl'):
                self.render(
                    p,
                    self.tasks
                    / category
                    / p.name.removeprefix('executable_').removesuffix('.tmpl'),
                )
        self.entry = self.home / '.local/bin/dotfiles-diagnose'
        self.render(REPO / 'dot_local/bin/executable_dotfiles-diagnose.tmpl', self.entry)
        for name in [
            'nvim',
            'vale',
            'hs',
            'node',
            'npm',
            'op',
            'ssh-add',
            'ssh.exe',
            'powershell.exe',
            'chezmoi',
            'neovim-node-host',
        ]:
            executable(
                self.home / '.local/bin' / name,
                '#!/bin/sh\nprintf "%s\\n" "$0 $*" >> "$CALLS"\nexit 91\n',
            )
        executable(
            Path(self.paths['mise']),
            '''#!/bin/sh
[ "$*" = --version ] || { echo "$*" >> "$CALLS"; exit 92; }
[ "$MISE_AUTO_INSTALL:$MISE_TASK_RUN_AUTO_INSTALL:$MISE_NOT_FOUND_AUTO_INSTALL" = false:false:false ] || exit 93
printf '2026.6.11 fixture\n'
''',
        )
        (self.source / '.mise-version').write_text('2026.6.11\n')
        self.fixture_file(self.source / 'dot_config/nvim/lazy-lock.json', '{"fixture":{}}\n')
        self.fixture_file(self.home / '.config/nvim/lazy-lock.json', '{"fixture":{}}\n')
        self.fixture_file(
            self.home / '.config/mise/config.toml', '[settings]\nnot_found_auto_install = true\n'
        )
        self.fixture_file(self.home / '.config/vale/vale.ini', 'StylesPath = styles\n')
        (self.home / '.local/share/vale/styles/Google').mkdir(parents=True)
        for part in ['.ssh', '.local/state/ssh']:
            (self.home / part).mkdir(parents=True, exist_ok=True)
            (self.home / part).chmod(0o700)
        for name in 'mise gh rg fd uv starship yq doggo kubectl helm k9s lazygit pnpm codex scc delta chezmoi gcloud'.split():
            self.fixture_file(self.home / '.cache/zsh/completions' / ('_' + name), '# fixture\n')
        for name in ['zoxide.zsh', 'starship.zsh', 'gcloud.zsh.inc']:
            self.fixture_file(self.home / '.cache/zsh/init' / name, '# fixture\n')

    def fixture_file(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def run_cmd(self, args, **kwargs):
        return subprocess.run(
            [str(a) for a in args],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=40,
            **kwargs,
        )

    def render(self, source, target, shell=True):
        self.config.write_text(json.dumps({'data': self.data}))
        p = self.run_cmd(
            [
                CHEZMOI,
                '--config',
                self.config,
                '--source',
                self.source,
                '--destination',
                self.home,
                '--no-tty',
                'execute-template',
            ],
            input=source.read_text(),
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        executable(target, p.stdout)
        if shell:
            syntax = self.run_cmd(['/bin/bash', '-n', target])
            self.assertEqual(syntax.returncode, 0, syntax.stderr)
        else:
            target.chmod(0o644)
        return target

    def diagnose(self, *args):
        return self.run_cmd(['/bin/bash', self.entry, *args])

    def test_default_does_not_execute_apps_or_mutate_files(self):
        before = tree(self.home)
        for ci in ['false', 'true']:
            self.env['CI'] = ci
            result = self.diagnose()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Optional HubSpot', result.stdout)
            self.assertIn('warnings and untested', result.stdout)
            self.assertNotIn('Zero Drift', result.stdout)
        self.assertEqual(tree(self.home), before)
        self.assertFalse((self.root / 'calls').exists())

    def test_required_missing_and_drift_fail_in_ci_and_workstation(self):
        for ci in ['false', 'true']:
            self.env['CI'] = ci
            for part in [
                '.config/nvim/lazy-lock.json',
                '.config/mise/config.toml',
                '.cache/zsh/completions/_pnpm',
                '.cache/zsh/init/gcloud.zsh.inc',
                '.local/bin/nvim',
                '.local/bin/hs',
            ]:
                with self.subTest(ci=ci, missing=part):
                    path = self.home / part
                    saved = path.read_bytes(), path.stat().st_mode & 0o777
                    path.unlink()
                    self.assertNotEqual(self.diagnose().returncode, 0)
                    path.write_bytes(saved[0])
                    path.chmod(saved[1])
            lock = self.home / '.config/nvim/lazy-lock.json'
            lock.write_text('{"drift":{}}\n')
            self.assertNotEqual(self.diagnose().returncode, 0)
            lock.write_text('{"fixture":{}}\n')
        self.assertFalse((self.root / 'calls').exists())

    def test_missing_security_directory_fails(self):
        (self.home / '.ssh').rmdir()
        self.assertNotEqual(self.diagnose('check:security').returncode, 0)

    def test_failed_mise_version_command_and_empty_config_fail(self):
        executable(Path(self.paths['mise']), "#!/bin/sh\nprintf '2026.6.11 fixture\\n'\nexit 17\n")
        result = self.diagnose('check:toolchain')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('version command failed', result.stdout)
        executable(Path(self.paths['mise']), "#!/bin/sh\nprintf '2026.6.11 fixture\\n'\n")
        (self.home / '.config/mise/config.toml').write_text('')
        self.assertNotEqual(self.diagnose('check:toolchain').returncode, 0)

    def test_shim_is_not_a_required_executable(self):
        (self.home / '.local/bin/nvim').unlink()
        shim = self.home / '.local/share/mise/shims/nvim'
        executable(shim, '#!/bin/sh\ntouch "$MARKER"\n')
        self.env['PATH'] = f'{shim.parent}:' + self.env['PATH']
        result = self.diagnose('check:nvim')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'marker').exists())

    def test_platform_na_and_explicit_wsl_gate(self):
        result = self.diagnose('check:wsl-openssh')
        self.assertEqual(result.returncode, 0)
        self.assertIn('[N/A]', result.stdout)
        self.data.update(is_wsl=True, ssh_auth_sock=r'\\.\pipe\openssh-ssh-agent')
        self.render(
            REPO / 'dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl',
            self.tasks / 'check/wsl-openssh',
        )
        result = self.diagnose('check:wsl-openssh')
        self.assertEqual(result.returncode, 2)
        self.assertIn('[NOT RUN]', result.stdout)
        self.assertFalse((self.root / 'calls').exists())

    def test_completion_probe_never_executes_emitted_code(self):
        executable(
            self.home / '.local/bin/hs',
            '''#!/bin/sh
case "$1" in --help) exit 0;; completion) printf 'touch "$MARKER"\n';; *) exit 1;; esac
''',
        )
        result = self.diagnose('--probe', 'completion')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / 'marker').exists())
        executable(
            self.home / '.local/bin/hs',
            "#!/bin/sh\n[ \"$1\" = --help ] && exit 0\nprintf 'if then )\\n'\n",
        )
        self.assertNotEqual(self.diagnose('--probe', 'completion').returncode, 0)

    def test_real_nvim_probe_never_loads_normal_initialization(self):
        self.assertTrue(NVIM, 'installed nvim required; set NVIM_BIN to a real binary')
        p = self.home / '.local/bin/nvim'
        p.unlink()
        p.symlink_to(NVIM)
        executable(self.home / '.local/bin/neovim-node-host', '#!/bin/sh\nexit 0\n')
        self.fixture_file(
            self.home / '.config/nvim/init.lua',
            'vim.fn.writefile({"bootstrapped"}, vim.env.MARKER)\n',
        )
        # Python discovery may fail on this deliberately incomplete PATH; that is a failure, not a skip.
        result = self.diagnose('--probe', 'nvim')
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertIn('Python provider', result.stdout)
        self.assertFalse((self.root / 'marker').exists())
        self.assertFalse((self.home / '.local/share/nvim/lazy').exists())

    def test_required_identity_files_fail_without_auth_even_in_ci(self):
        key = self.root / 'identity-key'
        self.assertEqual(
            self.run_cmd(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-f', key]).returncode, 0
        )
        public = Path(str(key) + '.pub').read_text().strip()
        identity = {
            'item_id': 'fixture',
            'account_id': 'fixture',
            'key_type': 'ed25519',
            'key_hash': hashlib.sha256(public.encode()).hexdigest()[:8],
            'public_key': public,
            'name': 'Fixture',
            'email': 'fixture@example.test',
            'dirs': '~/work',
        }
        self.data['identities'] = [identity]
        self.render(
            REPO / 'dot_config/mise/repo-tasks/check/executable_identity.tmpl',
            self.tasks / 'check/identity',
        )
        self.env['CI'] = 'true'
        self.assertNotEqual(self.diagnose('check:identity').returncode, 0)
        self.paths['op_sign'] = '/fixture/sign-helper'
        # Produce a complete generation through the actual R05 scripts and Git consumer.
        before = self.render(
            REPO / '.chezmoiscripts/run_before_05-identity-dispatch.sh.tmpl', self.root / 'before'
        )
        result = self.run_cmd(['/bin/sh', before])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.render(
            REPO / 'dot_config/git/config.tmpl', self.home / '.config/git/config', shell=False
        )
        generator = self.render(
            REPO / 'dot_config/mise/repo-tasks/generate/executable_identity.tmpl',
            self.root / 'generate',
        )
        result = self.run_cmd([shutil.which('zsh'), '-f', generator])
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = self.home / '.config/git/identity.inc'
        dispatch = Path(
            self.run_cmd(['git', 'config', '--file', entry, 'include.path']).stdout.strip()
        )
        generation = dispatch.parent
        signers = generation / 'allowed_signers'
        fragment = generation / ('config_' + identity['email'] + '_' + identity['key_hash'])
        pubkey = generation / (
            'id_ed25519_' + identity['email'] + '_' + identity['key_hash'] + '.pub'
        )
        for ci in ['false', 'true']:
            self.env['CI'] = ci
            result = self.diagnose('check:identity')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for path in [
                signers,
                fragment,
                dispatch,
                pubkey,
                generation / 'manifest.json',
                generation / 'entry',
            ]:
                content = path.read_bytes()
                mode = path.stat().st_mode & 0o777
                path.unlink()
                before = tree(self.home)
                self.assertNotEqual(self.diagnose('check:identity').returncode, 0)
                self.assertEqual(tree(self.home), before)
                path.write_bytes(content)
                path.chmod(mode)
            mutations = [
                (pubkey, None, 'wrong key\n'),
                (fragment, 'user.signingkey', 'key::wrong'),
                (fragment, 'core.sshCommand', 'ssh -i /wrong'),
                (dispatch, 'includeIf.gitdir/i:' + str(self.home / 'work') + '/**.path', '/wrong'),
                (signers, None, 'wrong signer\n'),
                (dispatch, 'includeIf.gitdir/i:/unexpected/**.path', str(fragment)),
                (dispatch, 'core.sshCommand', 'ssh -i /wrong'),
                (fragment, 'include.path', '/unexpected'),
                (fragment, 'gpg.ssh.allowedSignersFile', '/unexpected'),
                (fragment, 'gpg.format', 'openpgp'),
                (entry, 'user.email', 'override@example.test'),
                (entry, 'gpg.ssh.allowedSignersFile', '/unexpected'),
                (entry, 'includeIf.gitdir/i:/unexpected/**.path', str(fragment)),
                (self.home / '.config/git/config', 'include.path', '/wrong'),
            ]
            for path, field, value in mutations:
                content = path.read_bytes()
                if field:
                    self.run_cmd(['git', 'config', '--file', path, field, value])
                else:
                    path.write_text(value)
                before = tree(self.home)
                self.assertNotEqual(self.diagnose('check:identity').returncode, 0)
                self.assertEqual(tree(self.home), before)
                path.write_bytes(content)
        self.assertFalse((self.root / 'calls').exists())

    def test_explicit_auth_probe_failure_is_not_bypassed_in_ci(self):
        self.env['CI'] = 'true'
        result = self.diagnose('--probe', 'identity')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('account probe failed', result.stdout)
        self.assertIn('SSH agent unavailable', result.stdout)

    def test_git_signature_requires_the_trusted_key(self):
        for key in ['a', 'b']:
            p = self.run_cmd(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-f', self.root / key])
            self.assertEqual(p.returncode, 0, p.stderr)
        generation = self.home / '.config/git/generation'
        generation.mkdir(parents=True)
        allowed = generation / 'allowed_signers'
        identity = generation / 'config_fixture'
        for field, value in [
            ('user.name', 'Fixture'),
            ('user.email', 'fixture@example.test'),
            ('user.signingkey', str(self.root / 'a')),
        ]:
            self.assertEqual(
                self.run_cmd(['git', 'config', '--file', identity, field, value]).returncode, 0
            )
        entry = self.home / '.config/git/identity.inc'
        dispatch = generation / 'dispatch'
        self.run_cmd(['git', 'config', '--file', entry, 'include.path', str(dispatch)])
        self.run_cmd(
            ['git', 'config', '--file', dispatch, 'gpg.ssh.allowedSignersFile', str(allowed)]
        )
        self.run_cmd(['git', 'config', '--global', 'gpg.ssh.program', shutil.which('ssh-keygen')])
        self.data.update(is_wsl=True, ssh_auth_sock=r'\\.\pipe\openssh-ssh-agent')
        full = self.render(
            REPO / 'dot_config/mise/repo-tasks/check/executable_wsl-openssh.tmpl', self.root / 'wsl'
        )
        # Run the actual signing function, excluding OS/network/auth functions.
        text = full.read_text().split('echo "--- WSL Windows OpenSSH / 1Password preflight ---"')[0]
        signing = self.root / 'signing'
        executable(signing, text + '\ncheck_git_signing\nexit "$HAS_ERROR"\n')
        for key, expected in [('b', 1), ('a', 0)]:
            allowed.write_text('fixture@example.test ' + (self.root / (key + '.pub')).read_text())
            result = self.run_cmd(['/bin/bash', signing, '--probe'])
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            self.assertIn('git commit -S succeeded', result.stdout)
        self.assertFalse((self.root / 'calls').exists())

    def seed_caller_mise_state(self):
        # All pointers are fixtures; never use caller/host mise configuration.
        state = self.root / 'caller-mise-state'
        alias = self.root / 'temporary-alias'
        alias.symlink_to(self.root, target_is_directory=True)
        self.env['TMPDIR'] = str(alias)
        for key, part in [
            ('CONFIG', 'config'),
            ('DATA', 'data'),
            ('CACHE', 'cache'),
            ('STATE', 'state'),
            ('SYSTEM_CONFIG', 'system'),
            ('SYSTEM_DATA', 'system-data'),
            ('PLUGINS', 'plugins'),
            ('INSTALLS', 'installs'),
            ('DOWNLOADS', 'downloads'),
            ('SHIMS', 'shims'),
        ]:
            path = state / part
            path.mkdir(parents=True, exist_ok=True)
            self.env[f'MISE_{key}_DIR'] = str(path)
        for part in [
            'cache/aged-fixture',
            'cache/latest-version',
            'cache/trusted-configs/fixture',
            'data/tracked_config_files/fixture',
            'plugins/node/.git/config',
            'installs/node/latest/bin/node',
            'system-data/installs/node/latest/fixture',
            'system-data/installs/node/24.0.0/bin/node',
        ]:
            path = state / part
            self.fixture_file(path, 'fixture only: github.com/mise-plugins/rtx-nodejs\n')
            os.utime(path, (946684800, 946684800))
        self.fixture_file(state / 'config/config.toml', '[settings]\ncache_prune_age = "1s"\n')
        self.fixture_file(state / 'config/miserc.toml', 'invalid [ fixture\n')
        self.fixture_file(self.root / '.miserc.toml', 'invalid [ fixture\n')
        self.env.update(
            CI='false',
            MISE_CACHE_PRUNE_AGE='1s',
            MISE_OFFLINE='true',
            MISE_GLOBAL_CONFIG_FILE=str(state / 'config/config.toml'),
            MISE_SHARED_INSTALL_DIRS=str(state / 'shared-installs'),
            MISE_LOG_FILE=str(state / 'unexpected-log'),
            MISE_GITHUB_CREDENTIAL_COMMAND='must-not-be-called',
            DOTFILES_SENTINEL='must-not-be-inherited',
        )
        return state

    def test_version_query_contains_forced_startup_mutations_and_cleans_up(self):
        state = self.seed_caller_mise_state()
        record = self.root / 'version-record.json'
        # Force the destructive branches on EVERY run, even when pruning is disabled.
        # This pessimistic stub tests directory isolation independently of randomness.
        program = (
            f'#!{sys.executable} -B\n'
            + r'''
import json, os, shutil
from pathlib import Path
home = Path(os.environ['HOME'])
cache = Path(os.environ.get('MISE_CACHE_DIR', home / '.cache/mise'))
data = Path(os.environ.get('MISE_DATA_DIR', home / '.local/share/mise'))
state = Path(os.environ.get('MISE_STATE_DIR', home / '.local/state/mise'))
plugins = Path(os.environ.get('MISE_PLUGINS_DIR', data / 'plugins'))
cache.mkdir(parents=True, exist_ok=True)
(cache / 'aged-fixture').unlink(missing_ok=True)
(cache / '.auto_prune').mkdir(exist_ok=True)
(cache / 'latest-version').write_text('forced startup cache write\n')
state.mkdir(parents=True, exist_ok=True)
if (cache / 'trusted-configs').exists():
    shutil.move(str(cache / 'trusted-configs'), str(state / 'trusted-configs'))
shutil.rmtree(plugins / 'node', ignore_errors=True)
(data / 'migrations').mkdir(parents=True, exist_ok=True)
(data / 'migrations/fixture').write_text('forced migration\n')
'''
            + f'''
# Model mise's hardcoded system-data fallback with a fixture-only path.
# A missing child override must fail deterministically without touching /usr/local.
system_data = Path(os.environ.get('MISE_SYSTEM_DATA_DIR', {str(state / 'system-data')!r}))
shutil.rmtree(system_data / 'installs/node/latest', ignore_errors=True)
system_data.mkdir(parents=True, exist_ok=True)
(system_data / 'forced-migration').write_text('forced system migration\\n')
Path({str(record)!r}).write_text(json.dumps(dict(os.environ, recorded_cwd=os.getcwd())))
'''
        )
        before = tree(self.home), tree(state)
        for output, status in [
            ('2026.6.11 fixture', 0),
            ('2026.6.11 fixture', 17),
            ('0.0.0 fixture', 0),
        ]:
            executable(
                Path(self.paths['mise']),
                program + f'print({output!r})\nraise SystemExit({status})\n',
            )
            # Only the executable fixture has intentionally changed since before.
            before = tree(self.home), tree(state)
            result = self.diagnose('check:toolchain')
            self.assertEqual(
                result.returncode,
                0 if status == 0 and output.startswith('2026.') else 1,
                result.stdout + result.stderr,
            )
            seen = json.loads(record.read_text())
            self.assertNotEqual(seen['HOME'], str(self.home))
            self.assertEqual(seen['HOME'], seen['recorded_cwd'])
            for key in [
                'MISE_CONFIG_DIR',
                'MISE_DATA_DIR',
                'MISE_CACHE_DIR',
                'MISE_STATE_DIR',
                'MISE_SYSTEM_CONFIG_DIR',
                'MISE_SYSTEM_DATA_DIR',
                'XDG_CONFIG_HOME',
                'XDG_DATA_HOME',
                'XDG_CACHE_HOME',
                'XDG_STATE_HOME',
                'TMPDIR',
            ]:
                self.assertTrue(Path(seen[key]).is_relative_to(Path(seen['HOME'])))
            for key, value in [
                ('CI', 'true'),
                ('MISE_CACHE_PRUNE_AGE', '0s'),
                ('MISE_OFFLINE', 'true'),
                ('MISE_NO_CONFIG', 'true'),
                ('MISE_NO_ENV', 'true'),
                ('MISE_NO_HOOKS', 'true'),
            ]:
                self.assertEqual(seen[key], value)
            for key in [
                'DOTFILES_SENTINEL',
                'MISE_LOG_FILE',
                'MISE_GITHUB_CREDENTIAL_COMMAND',
                'MISE_GLOBAL_CONFIG_FILE',
                'MISE_PLUGINS_DIR',
                'MISE_INSTALLS_DIR',
                'MISE_SHARED_INSTALL_DIRS',
            ]:
                self.assertNotIn(key, seen)
            self.assertEqual((tree(self.home), tree(state)), before)
            self.assertFalse(
                Path(seen['HOME']).exists(),
                'temporary version state must be removed on success/failure',
            )
            self.assertEqual(list(self.root.glob('dotfiles-mise-version.*')), [])
        # Positive control: the same forced startup stub without isolation really
        # deletes the aged fixture/plugin and moves trust state. No native tools.
        self.run_cmd([self.paths['mise'], '--version'])
        self.assertFalse((state / 'cache/aged-fixture').exists())
        self.assertFalse((state / 'plugins/node').exists())
        self.assertFalse((state / 'system-data/installs/node/latest').exists())
        self.assertTrue((state / 'state/trusted-configs/fixture').exists())
        self.assertNotEqual(tree(state), before[1])

    def test_native_version_query_preserves_cold_aged_state_without_warmup(self):
        self.assertTrue(MISE, 'installed adopted mise required')
        binary = Path(self.paths['mise'])
        binary.unlink()
        binary.symlink_to(MISE)
        self.seed_caller_mise_state()
        (self.source / '.mise-version').write_bytes((REPO / '.mise-version').read_bytes())
        before = tree(self.root)
        for ci in ['false', 'true']:
            self.env['CI'] = ci
            result = self.diagnose('check:toolchain')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('matches the declared version', result.stdout)
            self.assertEqual(tree(self.root), before)
        # No retries to hit a random branch: forced-mutation coverage is above;
        # the 0s early return before prune/marker creation is established upstream.

    def test_actual_mise_missing_tools_direct_entry_cannot_install(self):
        self.assertTrue(MISE, 'installed mise required; set MISE_BIN to a real binary')
        mise = Path(self.paths['mise'])
        mise.unlink()
        mise.symlink_to(MISE)
        # A configured missing tool, with a local asdf fixture that fails before doing any install.
        data = self.home / '.local/share/mise'
        plugin = data / 'plugins/asdf-r08-fixture/bin'
        executable(plugin / 'list-all', '#!/bin/sh\necho 1.0.0\n')
        executable(plugin / 'download', '#!/bin/sh\ntouch "$MARKER"\nexit 97\n')
        executable(plugin / 'install', '#!/bin/sh\ntouch "$MARKER"\nexit 97\n')
        self.env.update(
            MISE_DATA_DIR=str(data),
            MISE_CONFIG_DIR=self.paths['xdg_config'] + '/mise',
            MISE_CACHE_DIR=self.paths['xdg_cache'] + '/mise',
            MISE_STATE_DIR=self.paths['xdg_state'] + '/mise',
            MISE_OFFLINE='true',
            MISE_YES='true',
            MISE_TRUSTED_CONFIG_PATHS=str(self.root),
            MISE_GLOBAL_CONFIG_FILE=str(self.home / '.config/mise/config.toml'),
        )
        cfg = self.home / '.config/mise/config.toml'
        cfg.write_text('''[settings]
not_found_auto_install = true
[tools]
"asdf:r08-fixture" = "1.0.0"
[tasks.late-guard]
run = 'export MISE_AUTO_INSTALL=false; touch "$LATE_BODY"'
''')
        self.env['LATE_BODY'] = str(self.root / 'late-body')
        # No native warmup: compare from before the first real version query.
        (self.source / '.mise-version').write_bytes((REPO / '.mise-version').read_bytes())
        before = tree(self.home)
        result = self.diagnose()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.home), before)
        self.assertFalse((self.root / 'marker').exists())
        # Positive control: the legacy invocation enters the local backend before task-body export.
        result = self.run_cmd([MISE, 'run', 'late-guard'])
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / 'marker').exists(), result.stdout + result.stderr)
        self.assertFalse((self.root / 'late-body').exists())


if __name__ == '__main__':
    unittest.main()

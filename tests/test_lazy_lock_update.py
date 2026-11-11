"""Real Git revision/retention fixtures and native Lua driver failure gates.

CLI downloads/editor outputs are stubs; upstream native network evidence is
recorded separately. Tests never use normal Neovim config or plugin directories.
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
HELPER = REPO / '.chezmoitemplates/lazy_lock_update.py'
DRIVER = REPO / '.chezmoitemplates/lazy_lock_update.lua'
ENGINE = '85c7ff3711b730b4030d03144f6db6375044ae82'
GIT = shutil.which('git')
NVIM = os.environ.get('NVIM_BIN') or shutil.which('nvim')


class LockCandidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='lazy-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.env = {'HOME': str(self.root / 'home'), 'PATH': '/usr/bin:/bin', 'TMPDIR': str(self.root),
                    'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
                    'PYTHONDONTWRITEBYTECODE': '1'}
        self.repo = self.root / 'source'; self.repo.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.config = self.repo / 'dot_config/nvim'; self.config.mkdir(parents=True)
        (self.config / 'lua/config').mkdir(parents=True)
        (self.config / 'lua/config/options.lua.tmpl').write_text('selected options A')
        (self.config / 'init.lua.tmpl').write_text('A')
        self.lock = {'lazy.nvim': {'branch': 'main', 'commit': ENGINE},
                     'LazyVim': {'branch': 'main', 'commit': '0' * 40}}
        (self.config / 'lazy-lock.json').write_text(json.dumps(self.lock))
        self.commit(); self.a = self.git('rev-parse', 'HEAD').strip()
        (self.config / 'init.lua.tmpl').write_text('B')
        (self.config / 'lua/config/options.lua.tmpl').write_text('selected options B')
        self.commit(); self.b = self.git('rev-parse', 'HEAD').strip()
        self.git_bin = self.root / 'git-stub'
        self.git_bin.write_text('#!' + sys.executable + '\n' + f'''
import sys,subprocess
from pathlib import Path
a=sys.argv[1:]
if a[0]=='clone':
 Path(a[-1]).mkdir(parents=True);sys.exit(0)
if a[0]=='-C' and 'checkout' in a: sys.exit(0)
sys.exit(subprocess.call([{GIT!r}]+a))
''')
        self.git_bin.chmod(0o700)
        self.nvim = self.root / 'nvim-stub'
        self.nvim.write_text('#!' + sys.executable + '\n' + r'''
import sys,os,json
from pathlib import Path
if '--version' in sys.argv: print('NVIM v0.12.3');sys.exit(0)
c=Path(os.environ['XDG_CONFIG_HOME'])/'nvim'
mode=(c/'init.lua').read_text()
if mode=='fail': sys.exit(1)
if mode=='missing-report': sys.exit(0)
p=c/'lazy-lock.json';lock=json.loads(p.read_text())
if os.environ['DOTFILES_LAZY_PHASE']!='verify':
 lock['LazyVim']['commit']=('1' if mode=='A' else '2')*40
 if mode=='bad-lock': lock['LazyVim']['commit']='bad'
 p.write_text(json.dumps(lock)+'\n')
Path(os.environ['DOTFILES_LAZY_REPORT']).write_text(json.dumps({'phase':os.environ['DOTFILES_LAZY_PHASE'],'active':lock}))
''')
        self.nvim.chmod(0o700)

    def git(self, *args):
        return subprocess.check_output([GIT, '-C', str(self.repo), *args], env=self.env,
                                       stderr=subprocess.PIPE, text=True)

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'fixture')

    def run_update(self, *args):
        result = subprocess.run([sys.executable, str(HELPER), str(self.repo), '--git', str(self.git_bin),
                                 '--nvim', str(self.nvim), *args], env=self.env, cwd=self.root,
                                capture_output=True, text=True, timeout=20)
        path = Path(result.stdout.splitlines()[0].removeprefix('Retained artifact: '))
        self.assertTrue(path.is_dir(), result.stderr)
        return result, path

    def test_revision_selection_preserves_index_dirty_untracked_and_config(self):
        (self.config / 'lazy-lock.json').write_text('user staged lock'); self.git('add', '.')
        (self.config / 'init.lua.tmpl').write_text('uncommitted')
        (self.repo / 'untracked').write_text('keep')
        sentinel = self.root / 'home/.config/nvim/init.lua'; sentinel.parent.mkdir(parents=True)
        sentinel.write_text('normal config C')
        before = {str(p): p.read_bytes() for p in self.repo.rglob('*') if p.is_file()}
        for revision, expected in [(self.a, '1'), ('HEAD', '2')]:
            res, out = self.run_update('--revision', revision)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertEqual(json.loads((out / 'candidate.json').read_text())['LazyVim']['commit'], expected * 40)
            self.assertIn('options ' + ('A' if expected == '1' else 'B'), (out / 'config/nvim/lua/config/options.lua').read_text())
            self.assertEqual(json.loads((out / 'before.json').read_text()), self.lock)
            self.assertIn('a/dot_config/nvim/lazy-lock.json', (out / 'lazy-lock.patch').read_text())
            self.assertEqual(json.loads((out / 'manifest.json').read_text())['engine_retained'], ENGINE)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.repo.rglob('*') if p.is_file()})
        self.assertEqual(sentinel.read_text(), 'normal config C')

    def test_failures_keep_artifact_without_success_candidate(self):
        for mode in ('fail', 'missing-report', 'bad-lock'):
            with self.subTest(mode=mode):
                (self.config / 'init.lua.tmpl').write_text(mode); self.commit()
                res, out = self.run_update()
                self.assertNotEqual(res.returncode, 0)
                self.assertEqual(json.loads((out / 'status.json').read_text())['status'], 'failed')
                self.assertTrue((out / 'before.json').exists())
                self.assertFalse((out / 'candidate.json').exists())

    def test_unsupported_sources_and_input_lock_fail_before_download(self):
        cases = [('lua/config/extra.lua.tmpl', '{{ .secret }}'),
                 ('.lazy.lua', 'return {}'), ('symlink_extra.lua', '/outside'),
                 ('lazy-lock.json', '{}')]
        cases += [(prefix + '_extra.lua', 'return {}') for prefix in
                  ('dot', 'create', 'readonly', 'empty', 'remove', 'literal', 'modify', 'run', 'external')]
        cases.append(('lua/dot_nested/spec.lua', 'return {}'))
        for path, value in cases:
            with self.subTest(path=path):
                self.git('reset', '--hard', self.b)
                p = self.config / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(value); self.commit()
                res, out = self.run_update()
                self.assertNotEqual(res.returncode, 0)
                self.assertFalse((out / 'data/nvim/lazy').exists())

    def test_patch_applies_to_literal_lock_and_all_line_endings(self):
        for suffix, ending in [('', ''), ('.tmpl', '\n'), ('', '\r\n')]:
            with self.subTest(suffix=suffix, ending=repr(ending)):
                self.git('reset', '--hard', self.b)
                lock_path = self.config / ('lazy-lock.json' + suffix)
                if suffix:
                    (self.config / 'lazy-lock.json').unlink()
                lock_path.write_bytes((json.dumps(self.lock, indent=2).replace('\n', ending or '\n') + ending).encode())
                self.commit()
                res, out = self.run_update()
                self.assertEqual(res.returncode, 0, res.stderr)
                adoption = Path(tempfile.mkdtemp(prefix='adopt-', dir=self.root))
                subprocess.run([GIT, 'clone', '-q', '--no-hardlinks', str(self.repo), str(adoption)],
                               env=self.env, check=True)
                for command in (['--check'], []):
                    subprocess.run([GIT, '-C', str(adoption), 'apply', *command, str(out / 'lazy-lock.patch')],
                                   env=self.env, check=True, capture_output=True)
                self.assertEqual((adoption / 'dot_config/nvim' / lock_path.name).read_bytes(),
                                 (out / 'candidate.json').read_bytes())

    def test_invalid_revision_does_not_mutate_source(self):
        before = (self.repo / '.git/index').read_bytes()
        res, out = self.run_update('--revision=--not-a-revision')
        self.assertNotEqual(res.returncode, 0)
        self.assertEqual(before, (self.repo / '.git/index').read_bytes())
        self.assertEqual(json.loads((out / 'status.json').read_text())['status'], 'failed')


class NativeDriver(unittest.TestCase):
    def test_native_driver_success_and_error_gates(self):
        self.assertTrue(NVIM, 'existing Neovim required')
        with tempfile.TemporaryDirectory(prefix='lazy-driver-') as tmp:
            root = Path(tmp).resolve()
            for case in ('success', 'silent-process', 'task-error', 'spec-error', 'verify-success', 'target-error', 'origin-error'):
                with self.subTest(case=case):
                    r = root / case; (r / 'config/nvim').mkdir(parents=True)
                    lock = {'lazy.nvim': {'branch': 'main', 'commit': ENGINE},
                            'probe': {'branch': 'main', 'commit': 'a' * 40}}
                    (r / 'config/nvim/lazy-lock.json').write_text(json.dumps(lock))
                    (r / 'config/nvim/init.lua').write_text('require("lazy").setup({spec={},rocks={enabled=false}})')
                    env = {'HOME': str(r), 'PATH': '/usr/bin:/bin', 'CASE': case,
                           'DOTFILES_LAZY_PHASE': 'update', 'DOTFILES_LAZY_REPORT': str(r / 'report.json'),
                           'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null'}
                    for k in ('CONFIG', 'DATA', 'STATE', 'CACHE', 'RUNTIME'):
                        env['XDG_' + k + ('_DIR' if k == 'RUNTIME' else '_HOME')] = str(r / k.lower())
                    if case in ('verify-success', 'target-error', 'origin-error'):
                        env['DOTFILES_LAZY_PHASE'] = 'verify'
                        probe = r / 'data/nvim/lazy/probe'; probe.mkdir(parents=True)
                        subprocess.run([GIT, 'init', '-q', str(probe)], check=True, env=env)
                        (probe / 'data').write_text('fixture')
                        subprocess.run([GIT, '-C', str(probe), 'add', '.'], check=True, env=env)
                        subprocess.run([GIT, '-C', str(probe), '-c', 'user.name=Fixture',
                                        '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false',
                                        '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'fixture'], check=True, env=env)
                        env['PROBE_COMMIT'] = subprocess.check_output([GIT, '-C', str(probe), 'rev-parse', 'HEAD'], env=env, text=True).strip()
                        lock['probe']['commit'] = env['PROBE_COMMIT']
                        (r / 'config/nvim/lazy-lock.json').write_text(json.dumps(lock))
                    # Module doubles expose the observed upstream boundaries; the production driver runs unchanged.
                    prelude = r'''
local C={plugins={},spec={modules={},disabled={},ignore_installed={}}}
C.spec.report=function() return vim.env.CASE=='spec-error' and 1 or 0 end
C.options={lockfile=vim.fn.stdpath('config')..'/lazy-lock.json'}
for _,n in ipairs({'lazy.nvim','probe'}) do C.plugins[n]={name=n,dir=vim.fn.stdpath('data')..'/lazy/'..n,url='fixture',_={installed=true}} end
C.plugins['lazy.nvim'].pin=true
local task={spawn=function() return vim.env.CASE~='silent-process' end}
local manager={setup=function() end,install=function() end,update=function()
 local p=C.plugins.probe
 local t={error=function() p.failed=true end}
 task.spawn(t,'git',{})
 if vim.env.CASE=='task-error' then p.failed=true end
end}
package.preload.lazy=function() return manager end
package.preload['lazy.core.loader']=function() return {startup=function() error('must not start') end} end
package.preload['lazy.core.config']=function() return C end
package.preload['lazy.core.plugin']=function() return {has_errors=function(p) return p.failed end} end
package.preload['lazy.manage.task.plugin']=function() return {build={run=function() error('must not build') end}} end
package.preload['lazy.manage.task']=function() return task end
package.preload['lazy.manage.git']=function() return {info=function(dir) return {commit=dir:match('lazy.nvim$') and 'ENGINE' or (vim.env.PROBE_COMMIT or string.rep('a',40))} end,
 get_origin=function() return vim.env.CASE=='origin-error' and 'wrong' or 'fixture' end,
 get_target=function() return {branch='main',commit=vim.env.CASE=='target-error' and string.rep('b',40) or vim.env.PROBE_COMMIT} end} end
'''.replace('ENGINE', ENGINE)
                    script = r / 'run.lua'; script.write_text(prelude + DRIVER.read_text())
                    result = subprocess.run([NVIM, '--headless', '-u', 'NONE', '-i', 'NONE', '-n', '-l', str(script)],
                                            cwd=r, env=env, capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode == 0, case in ('success', 'verify-success'), result.stderr)
                    self.assertEqual((r / 'report.json').exists(), case in ('success', 'verify-success'))


if __name__ == '__main__':
    unittest.main()

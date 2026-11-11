#!/usr/bin/env python3
"""Hookless rendering, stub CLIs and installed chezmoi completion in isolated HOME."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
ZSH = shutil.which('zsh')
TEMPLATE = REPO / 'dot_config/mise/repo-tasks/generate/executable_completions.tmpl'


class CompletionTransaction(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI and ZSH, 'installed chezmoi and zsh required')
        self.tmp = tempfile.TemporaryDirectory(prefix='r07-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.home = self.root / "home ' $() `literal`"
        self.home.mkdir()
        self.bin = self.home / '.local/bin'
        self.bin.mkdir(parents=True)
        self.cache = self.home / '.cache'
        self.comp = self.cache / 'zsh/completions'
        self.init = self.cache / 'zsh/init'
        self.comp.mkdir(parents=True)
        self.init.mkdir()
        self.sdk = self.root / 'sdk with spaces'
        self.sdk.mkdir()
        self.package = self.root / 'package'
        self.package.mkdir()
        (self.package / 'vendor').write_text('fixture package implementation')
        (self.sdk / 'completion.zsh.inc').write_text('_python_argcomplete() { print -r -- gcloud-new; }\n')
        # No ambient optional CLI can be discovered, even if /usr/bin has WezTerm.
        utilities = self.root / 'utilities'
        utilities.mkdir()
        for name in ('mkdir', 'mktemp', 'mv', 'rm', 'rmdir', 'chmod', 'cat', 'tr', 'touch', 'sleep', 'python3', 'bash'):
            (utilities / name).symlink_to(shutil.which(name))
        self.env = {'HOME': str(self.home), 'PATH': str(utilities), 'LC_ALL': 'C',
                    'TMPDIR': str(self.root), 'XDG_CACHE_HOME': str(self.cache),
                    'XDG_CONFIG_HOME': str(self.home / '.config'),
                    'XDG_DATA_HOME': str(self.home / '.local/share'),
                    'XDG_STATE_HOME': str(self.home / '.local/state'),
                    'SDK': str(self.sdk), 'PACKAGE_ROOT': str(self.package), 'READY': str(self.root / 'ready')}
        self.stub = self.bin / 'mise'
        self.stub.write_text('''#!/bin/sh
if [ "$1" = exec ] && [ "$3" = -- ]; then
  [ "${NO_USAGE:-}" = 1 ] || printf '%s\\n' "$HOME/.local/bin/usage"
  exit 0
fi
if [ "$1" = which ]; then
  printf '%s\\n' "$HOME/.local/bin/${4}"
  exit
fi
if [ "$1" = where ]; then
  [ "${FAIL:-}" != where ] || exit 42
  if [ "$2" = gcloud ]; then printf '%s\\n' "$SDK"; else printf '%s\\n' "$PACKAGE_ROOT"; fi
  exit
fi
if [ "$1" = exec ]; then shift 4; fi
if [ "$1" = /bin/sh ]; then shift 5; fi
name=${1##*/}
name=${1##*/}
case "$name" in completion) name=mise;; esac
case " $* " in *" init "*) name=$name-init;; esac
if [ "$name" = "${FAIL:-}" ]; then
  case "$MODE" in
    fail) printf '# partial\\n'; exit 42;;
    invalid) printf 'if then )\\n'; exit 0;;
    empty) exit 0;;
    wait) printf '# partial\\n'; touch "$READY"; while [ ! -f "$READY.release" ]; do sleep .02; done; exit 42;;
  esac
fi
printf '#compdef %s\\nprint -r -- %s-new\\n' "$name" "$name"
''')
        self.stub.chmod(0o755)
        for name in ('gh', 'rg', 'fd', 'uv', 'starship', 'yq', 'doggo', 'kubectl',
                     'helm', 'k9s', 'lazygit', 'pnpm', 'codex', 'scc', 'delta', 'zoxide', 'node', 'usage'):
            (self.bin / name).write_text('#!/bin/sh\n# fixture dependency\n')
            (self.bin / name).chmod(0o755)
        source = self.root / 'source'
        source.mkdir()
        shutil.copytree(REPO / '.chezmoitemplates', source / '.chezmoitemplates')
        shutil.copytree(REPO / '.chezmoidata', source / '.chezmoidata')
        config = self.root / 'config.json'
        config.write_text(json.dumps({'data': {'paths': {'home': str(self.home),
                              'mise': str(self.stub), 'xdg_cache': str(self.cache)}}}))
        result = subprocess.run([CHEZMOI, '--config', str(config), '--source', str(source),
                                 '--destination', str(self.home), '--no-tty', 'execute-template'],
                                input=TEMPLATE.read_text(), env=self.env, cwd=self.root,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.script = self.root / 'generate.zsh'
        self.script.write_text(result.stdout)
        self.run_zsh(['-n', str(self.script)])

    def run_zsh(self, args):
        p = subprocess.run([ZSH, '-f', *args], env=self.env, cwd=self.root,
                           text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def run_generator(self, fail='', mode='fail'):
        return subprocess.run([ZSH, '-f', str(self.script)], cwd=self.root,
                              env={**self.env, 'FAIL': fail, 'MODE': mode},
                              text=True, capture_output=True)

    def old(self, path, content='print -r -- old-good\n'):
        path.write_text(content)
        path.chmod(0o640)
        self.run_zsh(['-c', 'zcompile -U "$1"', 'zsh', str(path)])
        # Force the old compiled copy to outrank a same-second new source.
        os.utime(str(path) + '.zwc', (2000000000, 2000000000))
        return path.read_bytes(), Path(str(path) + '.zwc').read_bytes()

    def assert_old(self, path, before):
        self.assertEqual(path.read_bytes(), before[0])
        self.assertEqual(path.stat().st_mode & 0o777, 0o640)
        self.assertEqual(Path(str(path) + '.zwc').read_bytes(), before[1])

    def test_success_loadability_and_bounded_cache_changes(self):
        old = self.comp / '_gh'
        self.old(old)
        self.old(self.init / 'zoxide.zsh')
        unknown = [self.comp / '_unmanaged.zwc', self.init / 'unmanaged.zwc',
                   self.cache / 'zsh/zcompdump.other', self.home / '.zcompdump']
        for p in unknown:
            p.write_text('keep')
        dump = self.cache / 'zsh/zcompdump'
        self.old(dump)
        (self.init / 'gcloud.zsh.inc').symlink_to(self.sdk / 'completion.zsh.inc')
        p = self.run_generator()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('wezterm not found', p.stderr)
        self.assertFalse(Path(str(old) + '.zwc').exists())
        self.assertFalse(dump.exists())
        self.assertFalse(Path(str(dump) + '.zwc').exists())
        for path in unknown:
            self.assertEqual(path.read_text(), 'keep')
        self.assertFalse((self.init / 'gcloud.zsh.inc').is_symlink())
        self.assertEqual(self.run_zsh(['-c', 'source "$1"', 'zsh', str(self.init / 'zoxide.zsh')]), 'zoxide-init-new\n')
        self.assertEqual(self.run_zsh(['-c', 'fpath=("$1" $fpath); autoload -Uz _gh _gcloud; _gh; _gcloud', 'zsh', str(self.comp)]), 'gh-new\ngcloud-new\n')
        # Parse every generated function via the real consumer without executing CLIs.
        self.run_zsh(['-c', 'fpath=("$1" $fpath); for f in "$1"/_*; do autoload -Uz "${f:t}"; autoload +X "${f:t}" || exit; done', 'zsh', str(self.comp)])
        self.assertFalse(list(self.cache.rglob('.completion-stage.*')))

    def test_required_generator_failures_preserve_source_and_compiled(self):
        for name, path in [('mise', self.comp / '_mise'), ('gh', self.comp / '_gh'),
                           ('pnpm', self.comp / '_pnpm'), ('delta', self.comp / '_delta'),
                           ('zoxide-init', self.init / 'zoxide.zsh'),
                           ('starship-init', self.init / 'starship.zsh')]:
            for mode in ('fail', 'empty', 'invalid'):
                with self.subTest(name=name, mode=mode):
                    before = self.old(path)
                    p = self.run_generator(name, mode)
                    self.assertNotEqual(p.returncode, 0)
                    self.assertIn('Required Zsh asset failed', p.stderr)
                    self.assert_old(path, before)

    def test_optional_failure_is_visible_and_preserves_old(self):
        wezterm = self.bin / 'wezterm'
        wezterm.write_text('#!/bin/sh\nprintf "if then )\\n"\nexit 0\n')
        wezterm.chmod(0o755)
        before = self.old(self.comp / '_wezterm')
        p = self.run_generator()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('Optional completion unavailable', p.stderr)
        self.assert_old(self.comp / '_wezterm', before)
        wezterm.write_text('#!/bin/sh\nprintf "# partial\\n"\nexit 42\n')
        p = self.run_generator()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('Optional completion unavailable', p.stderr)
        self.assert_old(self.comp / '_wezterm', before)

    def test_gcloud_missing_and_invalid_preserve_link_and_wrapper(self):
        include = self.init / 'gcloud.zsh.inc'
        legacy = self.root / 'legacy.inc'
        legacy.write_text('# good old SDK\n')
        include.symlink_to(legacy)
        before = self.old(self.comp / '_gcloud')
        for content in (None, 'if then )\n', ''):
            sdk_include = self.sdk / 'completion.zsh.inc'
            if content is None:
                sdk_include.unlink()
            else:
                sdk_include.write_text(content)
            p = self.run_generator()
            self.assertNotEqual(p.returncode, 0)
            self.assertEqual(include.readlink(), legacy)
            self.assert_old(self.comp / '_gcloud', before)

    def test_interruption_during_generation_preserves_old(self):
        path = self.comp / '_mise'
        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGKILL):
            with self.subTest(signal=sig):
                before = self.old(path)
                ready = Path(self.env['READY'])
                ready.unlink(missing_ok=True)
                Path(str(ready) + ".release").unlink(missing_ok=True)
                p = subprocess.Popen([ZSH, '-f', str(self.script)], cwd=self.root,
                                     env={**self.env, 'FAIL': 'mise', 'MODE': 'wait'},
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     start_new_session=True)
                try:
                    deadline = time.monotonic() + 5
                    while not ready.exists() and time.monotonic() < deadline:
                        time.sleep(.02)
                    self.assertTrue(ready.exists())
                    os.killpg(p.pid, sig)
                    Path(str(ready) + ".release").touch()
                    p.communicate(timeout=5)
                    self.assertNotEqual(p.returncode, 0)
                    self.assert_old(path, before)
                    retry = self.run_generator('mise', 'fail')
                    self.assertNotEqual(retry.returncode, 0)
                    self.assertIn('Required Zsh asset failed', retry.stderr)
                finally:
                    if p.poll() is None:
                        os.killpg(p.pid, signal.SIGKILL)
                        p.communicate()

    def test_single_pid_termination_cannot_leave_a_publisher(self):
        self.single_pid_cancellation(signal.SIGTERM)

    def test_single_pid_kill_cannot_leave_a_publisher(self):
        self.single_pid_cancellation(signal.SIGKILL)

    def single_pid_cancellation(self, sig):
        # A supervisor may signal only the task PID, not its entire process group.
        # Let its generator finish successfully afterwards; it must never publish.
        release = self.root / 'release'
        self.env['RELEASE'] = str(release)
        original_stub = self.stub.read_text()
        self.stub.write_text('''#!/bin/sh
printf '#compdef mise\\n'
touch "$READY"
while [ ! -f "$RELEASE" ]; do sleep .02; done
printf 'print -r -- completed-after-termination\\n'
''')
        path = self.comp / '_mise'
        before = self.old(path)
        p = subprocess.Popen([ZSH, '-f', str(self.script)], cwd=self.root,
                             env=self.env, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
        try:
            deadline = time.monotonic() + 5
            while not Path(self.env['READY']).exists() and time.monotonic() < deadline:
                time.sleep(.02)
            self.assertTrue(Path(self.env['READY']).exists())
            other_writer = self.run_generator()
            self.assertNotEqual(other_writer.returncode, 0)
            self.assertIn('Completion generator locked', other_writer.stderr)
            self.assert_old(path, before)
            p.send_signal(sig)
            time.sleep(.1)
            release.touch()
            p.communicate(timeout=5)
            self.assertNotEqual(p.returncode, 0)
            self.assert_old(path, before)
            self.stub.write_text(original_stub)
            retry = self.run_generator('mise', 'fail')
            self.assertIn('Required Zsh asset failed', retry.stderr)
        finally:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.communicate()

    def test_rename_failure_and_interrupt_at_commit(self):
        # Instrument only the rendered fixture; production renames execute inside
        # the task process, so a killed parent cannot leave an orphan mv publisher.
        self.assertNotIn('command mv', self.script.read_text())
        injected = '''function test_move {
  local candidate="$1"
  [[ "$1" != -f ]] || candidate="$3"
  if [[ "$candidate" == */.completion-stage.*/_mise ]]; then
    case "$MOVE_MODE" in
      fail) return 42 ;;
      before) kill -TERM $$; return 42 ;;
      after) builtin zf_mv "$@" || return; kill -TERM $$; return 0 ;;
    esac
  fi
  builtin zf_mv "$@"
}
'''
        self.script.write_text(injected + self.script.read_text().replace('builtin zf_mv', 'test_move'))
        path = self.comp / '_mise'
        for mode in ('fail', 'before', 'after'):
            with self.subTest(mode=mode):
                before = self.old(path, '#compdef old-mise-alias\nprint -r -- old-good\n')
                dump = self.cache / 'zsh/zcompdump'
                self.run_zsh(['-c', 'fpath=("$1" $fpath); autoload -Uz compinit; compinit -d "$2"; zcompile "$2"',
                              'zsh', str(self.comp), str(dump)])
                dump_before = dump.read_bytes(), Path(str(dump) + '.zwc').read_bytes()
                self.env['MOVE_MODE'] = mode
                p = self.run_generator()
                self.assertNotEqual(p.returncode, 0)
                if mode == 'after':
                    self.assertIn('mise-new', path.read_text())
                    self.assertFalse(Path(str(path) + '.zwc').exists())
                    self.assertFalse(dump.exists())
                    self.assertFalse(Path(str(dump) + '.zwc').exists())
                    # Exercise the exact .zshrc dispatch-cache decision after interruption.
                    consumer = (REPO / 'dot_config/zsh/dot_zshrc.tmpl').read_text()
                    consumer = consumer[consumer.index('  local zcompdump='):consumer.index('  bashcompinit')]
                    result = self.run_zsh(['-c', 'fpath=("$1" $fpath); autoload -Uz compinit; '
                                           'ZSH_COMPDUMP_DIR="$2"; ' + consumer +
                                           '; print -r -- "${_comps[mise]-missing}" "${_comps[old-mise-alias]-missing}"',
                                           'zsh', str(self.comp), str(self.cache / 'zsh')])
                    self.assertEqual(result, '_mise missing\n')
                else:
                    self.assertEqual((dump.read_bytes(), Path(str(dump) + '.zwc').read_bytes()), dump_before)
                    self.assert_old(path, before)
                self.assertFalse(list(self.cache.rglob('.completion-stage.*')))

    def test_fixed_subdirectory_symlinks_are_refused(self):
        for directory in (self.comp, self.init, self.cache / 'zsh'):
            with self.subTest(directory=directory.name):
                outside = self.root / ('outside-' + directory.name)
                shutil.move(directory, outside)
                directory.symlink_to(outside, target_is_directory=True)
                marker = outside / '_mise'
                marker.write_text('keep outside')
                compiled = outside / '_mise.zwc'
                compiled.write_text('keep outside cache')
                p = self.run_generator()
                self.assertNotEqual(p.returncode, 0)
                self.assertIn('Refusing redirected asset directory', p.stderr)
                self.assertEqual(marker.read_text(), 'keep outside')
                self.assertEqual(compiled.read_text(), 'keep outside cache')
                directory.unlink()
                shutil.move(outside, directory)

    def test_lock_symlink_and_directory_are_refused(self):
        lock = self.cache / 'zsh/.completion-generation.lock'
        outside = self.root / 'unmanaged-lock'
        outside.write_text('keep')
        before = self.old(self.comp / '_mise')
        lock.symlink_to(outside)
        p = self.run_generator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Refusing non-regular completion lock', p.stderr)
        self.assertEqual(outside.read_text(), 'keep')
        self.assert_old(self.comp / '_mise', before)
        lock.unlink()
        lock.mkdir()
        p = self.run_generator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Refusing non-regular completion lock', p.stderr)
        self.assertTrue(lock.is_dir())
        self.assert_old(self.comp / '_mise', before)

    def test_unowned_directory_digest_is_retained_and_reported(self):
        digest = Path(str(self.comp) + '.zwc')
        digest.write_text('unmanaged digest')
        before = self.old(self.comp / '_mise')
        p = self.run_generator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('compiled directory shadows', p.stderr)
        self.assertEqual(digest.read_text(), 'unmanaged digest')
        self.assert_old(self.comp / '_mise', before)

    def test_output_symlink_is_not_followed(self):
        outside = self.root / 'outside'
        outside.write_text('keep\n')
        (self.comp / '_mise').symlink_to(outside)
        p = self.run_generator()
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(outside.read_text(), 'keep\n')
        self.assertTrue((self.comp / '_mise').is_symlink())


if __name__ == '__main__':
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""R10c: real reduced apply ordering, native generator stubs, isolated HOME."""
import json
import importlib.util
from unittest import mock
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
TASKS = {'bat': 'cache/bat', 'vale': 'sync/vale', 'pbfile': 'build/pbfile'}
STUB = r'''#!PYTHON
import hashlib, json, os, pathlib, re, sys
P=pathlib.Path
name=P(sys.argv[0]).name
args=sys.argv[1:]
home=P(os.environ['HOME'])
def log(value):
    with (home/'calls').open('a') as f: f.write(value+'\n')
if name=='mise':
    if args[0]=='install':
        assert (home/'.config/mise/repo-tasks/cache/bat').is_file()
        log('target then install'); (home/'prepared').touch()
    elif args[0]=='run': log('graph')
    elif args[0]=='which':
        assert (home/'prepared').exists()
        print(home/'.local/bin'/args[-1])
    else: sys.exit(81)
    sys.exit()
if name=='xcrun':
    if '--find' in args: print(home/'.local/bin/swiftc')
    elif '--show-sdk-path' in args: print(home/'sdk')
    else: print('fixture-sdk-1')
    sys.exit()
if '--version' in args: print(name+' 1.0.0'); sys.exit()
if name=='bat':
    if args[0]=='cache':
        log('generate bat')
        out=P(args[args.index('--target')+1]); src=P(args[args.index('--source')+1])
        content=b''.join(p.read_bytes() for p in sorted(src.rglob('*')) if p.is_file())
        (out/'syntaxes.bin').write_bytes(b'syntax'+content)
        if os.environ.get('FAIL')=='bat': sys.exit(42)
        (out/'themes.bin').write_bytes(b'theme'+content)
        (out/'metadata.yaml').write_text('bat_version: 1.0.0\n')
        if os.environ.get('BUILD_WARNING'): print('Failed to load one or more themes')
    else:
        if os.environ.get('INVALID')=='bat': print('bad cache',file=sys.stderr)
        print('Catppuccin Mocha Swift')
elif name=='vale':
    cfg=P(next(a.split('=',1)[1] for a in args if a.startswith('--config='))).read_text()
    out=P(re.search(r'^StylesPath\s*=\s*(.*)$',cfg,re.M)[1])
    if 'sync' in args:
        log('generate vale'); (out/'Google').mkdir()
        package=re.search(r'^Packages\s*=\s*(.*)$',cfg,re.M)[1]
        content=b'extends: existence\n'
        if P(package).is_dir(): content+=(P(package)/'input').read_bytes()
        (out/'Google/Acronyms.yml').write_bytes(content)
        if os.environ.get('FAIL')=='vale': sys.exit(42)
        (out/'Google/AMPM.yml').write_bytes(content)
        (out/'Google/Headings.yml').write_bytes(content)
        (out/'Google/vocab.txt').write_text('')
        (out/'Google/meta.json').write_text('{}')
    elif os.environ.get('INVALID')=='vale': sys.exit(42)
elif name=='swiftc':
    log('generate pbfile')
    out=P(args[args.index('-o')+1]); src=P(args[args.index('-o')-1])
    out.write_text('#!/bin/sh\n# '+hashlib.sha256(src.read_bytes()).hexdigest()+'\nexit 0\n')
    if os.environ.get('FAIL')=='pbfile': sys.exit(42)
    if os.environ.get('INVALID')=='pbfile': out.write_text('#!/bin/sh\nexit 42\n')
    out.chmod(0o755)
'''


class GeneratedConvergence(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, 'existing chezmoi required')
        temporary = tempfile.TemporaryDirectory(prefix='r10c-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.home = self.root / "home ' $() `literal`"; self.home.mkdir()
        self.source = self.root / 'source'; self.source.mkdir()
        shutil.copytree(REPO / '.chezmoitemplates', self.source / '.chezmoitemplates')
        shutil.copytree(REPO / '.chezmoidata', self.source / '.chezmoidata')
        files = ['.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl',
                 '.chezmoiscripts/run_after_40-bat-cache.sh.tmpl',
                 '.chezmoiscripts/run_after_41-vale-styles.sh.tmpl',
                 '.chezmoiscripts/run_after_42-pbfile.sh.tmpl',
                 'dot_config/mise/config.toml.tmpl', 'dot_config/mise/conf.d/10-tools.toml',
                 'dot_config/vale/vale.ini.tmpl', 'dot_local/share/pbcopy/pbfile.swift']
        files += [str(p.relative_to(REPO)) for p in (REPO / 'dot_config/mise/repo-tasks').rglob('*') if p.is_file()]
        for name in files:
            target = self.source / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / name, target)
        (self.source / '.chezmoiexternal.toml.tmpl').write_text('# no external downloads\n')
        ignores = ['.config/mise/config.toml', '.config/mise/conf.d']
        for p in (self.source / 'dot_config/mise/repo-tasks').rglob('*'):
            if p.is_file():
                target = str(p.relative_to(self.source / 'dot_config/mise/repo-tasks')).replace('executable_', '').removesuffix('.tmpl')
                if target not in TASKS.values(): ignores.append('.config/mise/repo-tasks/' + target)
        (self.source / '.chezmoiignore').write_text('\n'.join(ignores) + '\n')
        (self.source / '.chezmoiscripts/run_before_01-fixture.sh').write_text('#!/bin/sh\nprintf "before\\n" >> "$HOME/calls"\n')
        self.bin = self.home / '.local/bin'; self.bin.mkdir(parents=True)
        for name in ['mise', 'bat', 'vale', 'swiftc', 'xcrun']:
            p = self.bin / name; p.write_text(STUB.replace('PYTHON', sys.executable)); p.chmod(0o755)
        utilities = self.root / 'utilities'; utilities.mkdir()
        (utilities / 'python3').symlink_to(sys.executable)
        self.env = {'HOME': str(self.home), 'PATH': f'{self.bin}:{utilities}:/usr/bin:/bin',
                    'TMPDIR': str(self.root), 'LC_ALL': 'C', 'PYTHONDONTWRITEBYTECODE': '1'}
        paths = {'home': str(self.home), 'mise': str(self.bin / 'mise'), 'op': ''}
        for name, part in [('config', '.config'), ('data', '.local/share'), ('state', '.local/state'), ('cache', '.cache')]:
            paths['xdg_' + name] = str(self.home / part)
            self.env['XDG_' + name.upper() + '_HOME'] = str(self.home / part)
        self.config = self.root / 'config.json'
        self.config.write_text(json.dumps({'data': {'paths': paths, 'osid': 'darwin', 'is_wsl': False}}))
        self.theme = self.source / 'dot_config/bat/themes/Catppuccin Mocha.tmTheme'
        self.theme.parent.mkdir(parents=True); self.theme.write_text('fixture theme\n')
        (self.home / 'sdk').mkdir(); (self.home / 'sdk/SDKSettings.json').write_text('{}')
        self.outputs = {'bat': self.home / '.cache/bat', 'vale': self.home / '.local/share/vale/styles', 'pbfile': self.bin}
        self.names = {'bat': ['syntaxes.bin', 'themes.bin', 'metadata.yaml'],
                      'vale': ['Google/Acronyms.yml', 'Google/AMPM.yml', 'Google/Headings.yml', 'Google/vocab.txt', 'Google/meta.json'], 'pbfile': ['pbfile']}

    def apply(self, success=True):
        result = subprocess.run([CHEZMOI, '--config', str(self.config), '--source', str(self.source),
                                 '--destination', str(self.home), '--no-tty', 'apply', '--force'],
                                env=self.env, cwd=self.root, text=True, capture_output=True)
        if success: self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else: self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def calls(self):
        return (self.home / 'calls').read_text().splitlines()

    def snapshot(self, name):
        paths = [self.outputs[name] / p for p in self.names[name]]
        paths += [self.home / '.local/state/dotfiles-generators' / (name + '.json')]
        return {str(p): (p.read_bytes(), p.stat().st_mode & 0o777, p.stat().st_mtime_ns, p.stat().st_ino)
                for p in paths if p.exists()}

    def task(self, name, success):
        result = subprocess.run(['/bin/bash', str(self.home / '.config/mise/repo-tasks' / TASKS[name])],
                                env=self.env, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_apply_order_noop_and_each_missing_file(self):
        self.apply()
        self.assertEqual(self.calls(), ['before', 'target then install', 'graph', 'generate bat', 'generate vale', 'generate pbfile'])
        snapshots = {n: self.snapshot(n) for n in TASKS}
        calls = self.calls()
        self.apply()
        self.assertEqual(self.calls(), calls + ['before'])
        for name in TASKS: self.assertEqual(self.snapshot(name), snapshots[name])
        for name in TASKS:
            for file in self.names[name]:
                with self.subTest(name=name, missing=file):
                    before = self.snapshot(name)
                    target = self.outputs[name] / file; target.unlink()
                    calls = self.calls(); self.apply()
                    self.assertEqual(self.calls(), calls + ['before', 'generate ' + name])
                    after = self.snapshot(name)
                    self.assertEqual(after[str(target)][:2], before[str(target)][:2])
                    self.assertEqual({k:v for k,v in after.items() if k != str(target)},
                                     {k:v for k,v in before.items() if k != str(target)})

    def test_dependencies_same_apply_and_no_tool_preparation(self):
        self.apply()
        dependencies = [('bat', self.theme), ('bat', self.bin / 'bat'),
                        ('vale', self.source / 'dot_config/vale/vale.ini.tmpl'),
                        ('pbfile', self.source / 'dot_local/share/pbcopy/pbfile.swift'),
                        ('pbfile', self.bin / 'swiftc'), ('pbfile', self.home / 'sdk/SDKSettings.json')]
        for name, path in dependencies:
            with self.subTest(dependency=path.name):
                path.write_text(path.read_text() + '\n# fixture dependency\n')
                before = self.calls(); self.apply()
                self.assertEqual(self.calls(), before + ['before', 'generate ' + name])
                if path == self.theme:
                    self.assertIn(b'fixture dependency', (self.outputs['bat'] / 'themes.bin').read_bytes())
                before = self.calls(); self.apply(); self.assertEqual(self.calls(), before + ['before'])
        package = self.root / 'Google'; package.mkdir(); (package / 'input').write_text('v1')
        config = self.source / 'dot_config/vale/vale.ini.tmpl'
        config.write_text(config.read_text().replace('Packages = Google', 'Packages = ' + str(package)))
        before = self.calls(); self.apply(); self.assertEqual(self.calls(), before + ['before', 'generate vale'])
        (package / 'input').write_text('v2')
        before = self.calls(); self.apply(); self.assertEqual(self.calls(), before + ['before', 'generate vale'])

    def test_generation_and_validation_failure_preserve_all_old_outputs(self):
        self.apply()
        for name in TASKS:
            for failure in ['FAIL', 'INVALID']:
                with self.subTest(name=name, failure=failure):
                    # Change only the installed task's input fingerprint.
                    task = self.home / '.config/mise/repo-tasks' / TASKS[name]
                    task.write_text(task.read_text() + '\n# new implementation\n')
                    before = self.snapshot(name)
                    self.env[failure] = name
                    self.task(name, False)
                    self.assertEqual(self.snapshot(name), before)
                    self.env.pop(failure)
                    self.task(name, True)

    def test_apply_generation_failure_keeps_previous_state(self):
        self.apply()
        for name in TASKS:
            task = Path(TASKS[name])
            source = self.source / 'dot_config/mise/repo-tasks' / task.parent / ('executable_' + task.name + '.tmpl')
            source.write_text(source.read_text() + '\n# changed implementation\n')
            before = {n: self.snapshot(n) for n in TASKS}
            self.env['FAIL'] = name
            self.apply(False)
            for n in TASKS: self.assertEqual(self.snapshot(n), before[n])
            self.env.pop('FAIL'); self.apply()

    def test_unknown_files_conflicts_and_manual_tools_preserved(self):
        self.apply()
        protected = [self.outputs['bat'] / 'unknown.bin', self.outputs['vale'] / 'Google/Custom.yml',
                     self.outputs['vale'] / 'Private/Rule.yml', self.bin / 'manual-tool',
                     self.home / '.config/bat/syntaxes/Custom.sublime-syntax']
        for p in protected: p.parent.mkdir(parents=True, exist_ok=True); p.write_text('keep\n')
        self.apply()
        for p in protected: self.assertEqual(p.read_text(), 'keep\n')
        for name in TASKS:
            target = self.outputs[name] / self.names[name][0]
            original = target.read_bytes(); target.write_text('user edit\n')
            before = self.snapshot(name); self.task(name, False)
            self.assertEqual(self.snapshot(name), before)
            target.write_bytes(original)
        for name in TASKS:
            receipt = self.home / '.local/state/dotfiles-generators' / (name + '.json')
            original = receipt.read_bytes(); receipt.unlink()
            before = self.snapshot(name); self.task(name, False)
            self.assertEqual(self.snapshot(name), before)
            receipt.write_bytes(original)
        for p in protected: self.assertEqual(p.read_text(), 'keep\n')

    def test_missing_required_inputs_and_other_os(self):
        self.apply()
        for name, path in [('bat', self.home / '.config/bat/themes/Catppuccin Mocha.tmTheme'),
                           ('vale', self.home / '.config/vale/vale.ini'),
                           ('pbfile', self.home / '.local/share/pbcopy/pbfile.swift')]:
            original = path.read_bytes(); path.unlink(); before = self.snapshot(name)
            self.task(name, False); self.assertEqual(self.snapshot(name), before); path.write_bytes(original)
        data = json.loads(self.config.read_text()); data['data']['osid'] = 'linux'
        self.config.write_text(json.dumps(data))
        before = self.snapshot('pbfile'); self.apply()
        self.assertEqual(self.snapshot('pbfile'), before)
        self.task('pbfile', True)

    def test_bat_success_with_builtin_fallback_is_failure(self):
        self.apply()
        self.theme.write_text('broken theme')
        before = self.snapshot('bat'); self.env['BUILD_WARNING'] = '1'
        self.apply(False)
        self.assertEqual(self.snapshot('bat'), before)

    def test_vale_ini_spelling_cannot_redirect_staging(self):
        self.apply()
        config = self.home / '.config/vale/vale.ini'
        config.write_text(config.read_text().replace('StylesPath =', 'stylespath:'))
        before = self.snapshot('vale')
        self.env['FAIL'] = 'vale'
        self.task('vale', False)
        self.assertEqual(self.snapshot('vale'), before)
        self.env.pop('FAIL'); self.task('vale', True)

    def test_receipt_and_directory_redirection_refused(self):
        self.apply()
        for name in TASKS:
            receipt = self.home / '.local/state/dotfiles-generators' / (name + '.json')
            original = receipt.read_bytes(); receipt.write_text('{}')
            before = self.snapshot(name); self.task(name, False); self.assertEqual(self.snapshot(name), before)
            receipt.unlink(); other = self.root / (name + '-foreign'); other.write_text('keep')
            receipt.symlink_to(other); self.task(name, False); self.assertEqual(other.read_text(), 'keep')
            receipt.unlink(); receipt.write_bytes(original)
        google = self.outputs['vale'] / 'Google'; moved = self.root / 'moved'; google.rename(moved)
        google.symlink_to(moved, target_is_directory=True)
        before = {p.name:p.read_bytes() for p in moved.iterdir()}
        self.task('vale', False)
        self.assertEqual({p.name:p.read_bytes() for p in moved.iterdir()}, before)


class PublicationBoundary(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='r10c-publish-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.stage = self.root / 'stage'; self.stage.mkdir()
        self.receipt = self.root / 'receipt.json'
        spec = importlib.util.spec_from_file_location('generated_files', REPO / '.chezmoitemplates/generated_files.py')
        self.io = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.io)
        for name in ('a', 'b'):
            (self.root / name).write_text('old ' + name); (self.root / name).chmod(0o644)
            (self.stage / name).write_text('new ' + name); (self.stage / name).chmod(0o644)
        self.previous = {'owner': 'fixture-v1', 'input': 'old',
                         'files': {n:self.io.record(self.root / n) for n in ('a', 'b')}}
        self.receipt.write_text(json.dumps(self.previous))

    def test_publication_io_error_rolls_back_and_retry_succeeds(self):
        replace = self.io.os.replace
        def fail_once(src, dst):
            if Path(src) == self.stage / 'b': raise OSError('injected publish failure')
            return replace(src, dst)
        with mock.patch.object(self.io.os, 'replace', side_effect=fail_once):
            with self.assertRaises(OSError):
                self.io.publish(self.root, self.stage, ['a','b'], self.receipt, 'fixture', 'new', self.previous)
        self.assertEqual(json.loads(self.receipt.read_text()), self.previous)
        for n in ('a','b'): self.assertEqual(self.io.record(self.root/n), self.previous['files'][n])
        (self.stage/'a').write_text('new a'); (self.stage/'a').chmod(0o644)
        self.io.publish(self.root, self.stage, ['a','b'], self.receipt, 'fixture', 'new', self.previous)
        self.assertEqual((self.root/'a').read_text(), 'new a')
        self.assertFalse(list(self.root.glob('.publish-*')))

    def test_failed_rollback_retains_named_backup_for_explicit_recovery(self):
        replace = self.io.os.replace
        def fail(src, dst):
            if Path(src) == self.stage / 'b' or 'old' in Path(src).parts:
                raise OSError('injected rollback failure')
            return replace(src, dst)
        with mock.patch.object(self.io.os, 'replace', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'backup at'):
                self.io.publish(self.root, self.stage, ['a','b'], self.receipt, 'fixture', 'new', self.previous)
        backups = list(self.root.glob('.publish-*')); self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0]/'old/a').read_text(), 'old a')
        with self.assertRaisesRegex(RuntimeError, 'reconcile'):
            self.io.current(self.root, self.previous, 'new')
        self.assertEqual(json.loads(self.receipt.read_text()), self.previous)

    def test_unreadable_receipt_during_recovery_keeps_backup(self):
        replace = self.io.os.replace
        read_bytes = Path.read_bytes
        failed = False
        def fail_publish(src, dst):
            nonlocal failed
            if Path(src) == self.stage / 'b':
                failed = True
                raise OSError('injected publish failure')
            return replace(src, dst)
        def fail_observation(path):
            if path == self.receipt and failed:
                raise OSError('injected receipt read failure')
            return read_bytes(path)
        with mock.patch.object(self.io.os, 'replace', side_effect=fail_publish), \
                mock.patch.object(Path, 'read_bytes', fail_observation):
            with self.assertRaisesRegex(RuntimeError, 'Cannot determine receipt commit'):
                self.io.publish(self.root, self.stage, ['a','b'], self.receipt, 'fixture', 'new', self.previous)
        backups = list(self.root.glob('.publish-*')); self.assertEqual(len(backups), 1)
        for name in ('a','b'):
            self.assertEqual((backups[0]/'old'/name).read_text(), 'old ' + name)
        self.assertEqual(json.loads((backups[0]/'receipt.previous.json').read_text()), self.previous)
        self.assertEqual((self.root/'a').read_text(), 'new a')
        self.assertEqual(json.loads(self.receipt.read_text()), self.previous)
        with self.assertRaisesRegex(RuntimeError, 'reconcile'):
            self.io.current(self.root, self.previous, 'new')

    def test_sigint_after_receipt_commit_keeps_new_consistent_state(self):
        replace = self.io.os.replace
        def interrupt_after_commit(src, dst):
            replace(src, dst)
            if Path(dst) == self.receipt:
                raise KeyboardInterrupt('injected SIGINT after receipt rename')
        with mock.patch.object(self.io.os, 'replace', side_effect=interrupt_after_commit):
            with self.assertRaises(KeyboardInterrupt):
                self.io.publish(self.root, self.stage, ['a','b'], self.receipt, 'fixture', 'new', self.previous)
        committed = json.loads(self.receipt.read_text())
        self.assertEqual(committed['input'], 'new')
        self.assertTrue(self.io.current(self.root, committed, 'new'))
        for n in ('a','b'): self.assertEqual((self.root/n).read_text(), 'new ' + n)
        self.assertFalse(list(self.root.glob('.publish-*')))

    def test_process_death_mid_publish_is_detected_on_retry(self):
        script = self.root / 'interrupt.py'
        script.write_text((REPO / '.chezmoitemplates/generated_files.py').read_text() +             "\nroot=Path(sys.argv[1]); stage=root/'stage'; receipt=root/'receipt.json'\n"
            "previous=json.loads(receipt.read_text()); replace=os.replace\n"
            "def interrupt(src,dst):\n"
            "    replace(src,dst)\n"
            "    if Path(dst)==root/'a': os.kill(os.getpid(), signal.SIGKILL)\n"
            "os.replace=interrupt\n"
            "publish(root,stage,['a','b'],receipt,'fixture','new',previous)\n")
        script.write_text('import sys, signal\n' + script.read_text())
        result = subprocess.run([sys.executable, str(script), str(self.root)], capture_output=True)
        self.assertLess(result.returncode, 0)
        self.assertEqual((self.root/'a').read_text(), 'new a')
        self.assertEqual((self.root/'b').read_text(), 'old b')
        self.assertEqual(json.loads(self.receipt.read_text()), self.previous)
        with self.assertRaisesRegex(RuntimeError, 'reconcile'):
            self.io.current(self.root, self.previous, 'new')
        backups=list(self.root.glob('.publish-*')); self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0]/'old/a').read_text(), 'old a')


if __name__ == '__main__':
    unittest.main(verbosity=2)

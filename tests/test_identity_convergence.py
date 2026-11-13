#!/usr/bin/env python3
"""R10a: isolated real apply; owned missing files, no-op, dependencies, refusal.

The reduced source applies real before/after/Git templates and the real onchange
wrapper against a mise stub. No hooks, external assets, package or auth commands.
"""

import copy
import json
from pathlib import Path
import shutil
import unittest

import test_identity_boundary as boundary
from test_identity_transaction import Transaction, PREPARE

AFTER = '.chezmoiscripts/run_after_10-identity.sh.tmpl'


class Convergence(Transaction):
    def reduced(self):
        original = self.source
        reduced = self.root / 'reduced'
        reduced.mkdir()
        shutil.copytree(original / '.chezmoitemplates', reduced / '.chezmoitemplates')
        # All include dependencies of the real wrapper; only Git config is a target.
        references = [
            PREPARE,
            AFTER,
            boundary.WRAPPER,
            boundary.GIT,
            'dot_config/mise/config.toml.tmpl',
            'dot_config/mise/conf.d/10-tools.toml',
            '.chezmoiexternal.toml.tmpl',
            '.chezmoidata/completions.yaml',
            'dot_config/vale/vale.ini.tmpl',
            'dot_local/share/pbcopy/pbfile.swift',
        ]
        references += [
            str(p.relative_to(original))
            for p in (original / 'dot_config/mise/repo-tasks').rglob('*')
            if p.is_file()
        ]
        for name in references:
            target = reduced / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original / name, target)
        (reduced / '.chezmoiignore').write_text('.config/mise\n.config/vale\n.local\n')
        # Full wrapper calls install/run only when its actual rendered content changes.
        boundary.executable(
            Path(self.paths['mise']), '#!/bin/sh\nprintf "%s\\n" "$*" >> "$HOME/mise-calls"\n'
        )
        self.source = reduced
        data = json.loads(self.config.read_text())
        data['data']['osid'] = 'darwin'
        self.config.write_text(json.dumps(data))
        return original

    def apply_ok(self):
        result = self.chezmoi('apply', '--force')
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def snapshot_tree(self, parent):
        return {
            str(p.relative_to(parent)): (
                p.read_bytes(),
                p.stat().st_mode & 0o777,
                p.stat().st_mtime_ns,
                p.stat().st_ino,
            )
            for p in parent.rglob('*')
            if p.is_file() and not p.is_symlink()
        }

    def test_r10a_apply_twice_and_each_missing_output(self):
        self.reduced()
        self.apply_ok()
        generation = self.generation()
        snapshot = self.snapshot_tree(generation)
        entry = self.snapshot_tree(self.entry().parent)['identity.inc']
        calls = (self.home / 'mise-calls').read_bytes()
        names = set(p.name for p in self.entry().parent.glob('.identity-generation-*'))
        self.apply_ok()
        self.assertEqual(self.snapshot_tree(generation), snapshot)
        self.assertEqual(self.snapshot_tree(self.entry().parent)['identity.inc'], entry)
        self.assertEqual(
            set(p.name for p in self.entry().parent.glob('.identity-generation-*')), names
        )
        for name in snapshot:
            if name == 'manifest.json':
                continue  # Ownership-anchor loss has a distinct refusal test.
            with self.subTest(missing=name):
                (generation / name).unlink()
                self.apply_ok()
                self.assertEqual(self.generation(), generation)
                restored = self.snapshot_tree(generation)
                self.assertEqual(restored[name][:2], snapshot[name][:2])
                self.assertEqual(
                    {k: v for k, v in restored.items() if k != name},
                    {k: v for k, v in snapshot.items() if k != name},
                )
                snapshot = restored
                self.assertEqual((self.home / 'mise-calls').read_bytes(), calls)
                rendered = self.render(boundary.CHECK)
                self.assertEqual(rendered.returncode, 0, rendered.stderr)
                check = self.command(['/bin/bash'], input=rendered.stdout)
                self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
        for identity in self.ids:
            self.run_ok(['git', 'init', '-q', self.repo(identity)])
        self.assert_adopted(self.ids)

    def test_r10a_shared_template_and_engine_change_in_same_apply(self):
        self.reduced()
        self.apply_ok()
        old_generation = self.generation()
        old = self.snapshot_tree(old_generation)
        calls = (self.home / 'mise-calls').read_bytes()
        template = self.source / '.chezmoitemplates/git_identity_config.tmpl'
        template.write_text(
            template.read_text().replace(
                '# Auto-generated identity config.', '# Changed shared template.'
            )
        )
        self.apply_ok()
        self.assertNotEqual(self.generation(), old_generation)
        self.assertTrue(
            all(
                '# Changed shared template.' in p.read_text()
                for p in self.generation().glob('config_*')
            )
        )
        self.assertEqual(self.snapshot_tree(old_generation), old)
        self.assertEqual((self.home / 'mise-calls').read_bytes(), calls)
        engine = self.source / '.chezmoitemplates/identity_transaction.py'
        generation = self.generation()
        engine.write_text(engine.read_text() + '\n# Fixture engine dependency change.\n')
        self.apply_ok()
        self.assertNotEqual(self.generation(), generation)
        self.assertEqual((self.home / 'mise-calls').read_bytes(), calls)

    def test_r10a_missing_plus_conflict_never_partially_restores(self):
        self.reduced()
        self.apply_ok()
        generation = self.generation()
        missing = next(generation.glob('id_*.pub'))
        missing.unlink()
        fragment = next(generation.glob('config_*'))
        original = fragment.read_bytes()
        foreign = self.root / 'foreign'
        foreign.write_text('manual\n')
        for conflict in ('edit', 'symlink', 'unknown', 'mode'):
            with self.subTest(conflict=conflict):
                if conflict == 'edit':
                    fragment.write_text('manual\n')
                elif conflict == 'symlink':
                    fragment.unlink()
                    fragment.symlink_to(foreign)
                elif conflict == 'unknown':
                    (generation / 'unknown').write_text('precious\n')
                else:
                    fragment.chmod(0o644)
                before = self.entry().read_bytes()
                result = self.chezmoi('apply', '--force')
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(missing.exists())
                self.assertEqual(self.entry().read_bytes(), before)
                self.assertEqual(foreign.read_text(), 'manual\n')
                if fragment.is_symlink():
                    fragment.unlink()
                fragment.write_bytes(original)
                fragment.chmod(0o600)
                if (generation / 'unknown').exists():
                    self.assertEqual((generation / 'unknown').read_text(), 'precious\n')
                    (generation / 'unknown').unlink()
        self.apply_ok()

    def test_r10a_old_missing_file_restored_before_new_input_failure(self):
        self.reduced()
        self.apply_ok()
        generation = self.generation()
        snapshot = self.selected_snapshot()
        old_ids = copy.deepcopy(self.ids)
        for identity in old_ids:
            self.run_ok(['git', 'init', '-q', self.repo(identity)])
        missing = next(generation.glob('id_*.pub'))
        missing.unlink()
        self.change_inputs()
        data = json.loads(self.config.read_text())
        data['data']['osid'] = 'darwin'
        self.config.write_text(json.dumps(data))
        self.failing_git()
        result = self.chezmoi('apply', '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.selected_snapshot(), snapshot)
        self.assert_adopted(old_ids)
        self.unfail()
        self.apply_ok()
        self.assertEqual(
            {p.name: (p.read_bytes(), p.stat().st_mode & 0o777) for p in generation.iterdir()},
            snapshot[1],
        )
        for identity in self.ids:
            self.run_ok(['git', 'init', '-q', self.repo(identity)])
        self.assert_adopted(self.ids)

    def test_r10a_missing_anchors_refuse_without_guessing(self):
        self.reduced()
        self.apply_ok()
        generation = self.generation()
        for path in (self.entry(), generation / 'manifest.json'):
            with self.subTest(anchor=path.name):
                content = path.read_bytes()
                mode = path.stat().st_mode & 0o777
                path.unlink()
                before = self.snapshot_tree(self.entry().parent)
                result = self.chezmoi('apply', '--force')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.snapshot_tree(self.entry().parent), before)
                self.assertFalse(path.exists())
                path.write_bytes(content)
                path.chmod(mode)  # Explicit fixture recovery.

    def test_r10a_r05_manifest_upgrade_and_exact_missing_recovery(self):
        self.adopt()
        generation = self.generation()
        manifest = generation / 'manifest.json'
        data = json.loads(manifest.read_text())
        data = {
            k: v
            for k, v in data.items()
            if k in ('version', 'kind', 'files', 'legacy_config_sha256')
        }
        data['version'] = 1
        manifest.write_text(json.dumps(data) + '\n')
        snapshot = self.selected_snapshot()
        missing = generation / 'allowed_signers'
        missing.unlink()
        self.prepare()
        self.assertEqual(self.selected_snapshot(), snapshot)
        result = self.script(boundary.GEN)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(self.generation(), generation)
        self.assertEqual(
            json.loads((self.generation() / 'manifest.json').read_text())['version'], 2
        )
        # A v1 active generation with changed input cannot reconstruct old bytes.
        self.entry().write_bytes(snapshot[0])
        missing.unlink()
        self.change_inputs()
        before = self.snapshot_tree(generation)
        result = self.script(PREPARE)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot_tree(generation), before)
        self.assertFalse(missing.exists())

    def test_r10a_recovery_staging_failure_preserves_all_remaining_files(self):
        self.adopt()
        generation = self.generation()
        missing = [generation / 'dispatch', generation / 'allowed_signers']
        for path in missing:
            path.unlink()
        engine = self.source / '.chezmoitemplates/identity_transaction.py'
        text = engine.read_text()
        text = text.replace(
            "write(staging / name, saved['contents'][name], saved['modes'][name])",
            "write(staging / name, saved['contents'][name], saved['modes'][name])\n                raise Refusal('fixture recovery staging failure')",
        )
        engine.write_text(text)
        before = self.snapshot_tree(self.entry().parent)
        result = self.script(PREPARE)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot_tree(self.entry().parent), before)
        self.assertTrue(all(not path.exists() for path in missing))

    def test_r10a_git_formatter_dependency_and_noop_avoids_build(self):
        self.adopt()
        first = self.generation()
        self.failing_git()
        result = self.script(boundary.GEN)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'fail-count').exists())
        stub = self.bin / 'git'
        stub.write_text(
            stub.read_text().replace(
                "if 'core.sshCommand' in sys.argv:",
                "if sys.argv[1:] == ['--version']:\n    print('git version fixture-new'); sys.exit(0)\nif 'core.sshCommand' in sys.argv:",
            )
        )
        result = self.script(boundary.GEN)
        self.assertNotEqual(
            result.returncode, 0
        )  # New formatter triggers build, then injected failure.
        self.assertEqual(self.generation(), first)

    def test_r10a_wsl_mapping_changes_and_mise_version_is_not_input(self):
        self.write_data(wsl=True)
        self.env['FIXTURE_DISTRO'] = 'First'
        boundary.executable(
            self.bin / 'wslpath',
            '#!/bin/sh\nprintf "\\\\\\\\wsl.localhost\\\\%s\\\\%s\\n" "$FIXTURE_DISTRO" "${2##*/}"\n',
        )
        self.adopt()
        first = self.generation()
        old = self.snapshot_tree(first)
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(self.generation(), first)
        (self.source / '.mise-version').write_text('9999.1.1\n')
        self.env['WSL_DISTRO_NAME'] = 'IgnoredEnvironmentOnly'
        self.assertEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(self.generation(), first)
        self.env['FIXTURE_DISTRO'] = 'Second'
        result = self.script(boundary.GEN)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotEqual(self.generation(), first)
        self.assertEqual(self.snapshot_tree(first), old)
        for path in self.generation().glob('config_*'):
            self.assertIn('Second', self.run_ok(['git', 'config', '-f', path, 'core.sshCommand']))
        boundary.executable(self.bin / 'wslpath', '#!/bin/sh\nexit 71\n')
        before = self.selected_snapshot()
        self.assertNotEqual(self.script(boundary.GEN).returncode, 0)
        self.assertEqual(self.selected_snapshot(), before)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(
        Convergence(name) for name in Convergence.__dict__ if name.startswith('test_r10a_')
    )


if __name__ == '__main__':
    unittest.main(verbosity=2)

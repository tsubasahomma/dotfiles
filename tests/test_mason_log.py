import tempfile
from pathlib import Path
import unittest

from collect_mason_log import collect


class MasonLogTest(unittest.TestCase):
    def test_redacts_credentials_and_preserves_diagnostics_and_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'mason.log'
            original = (
                '[DEBUG] curl https://example.invalid/registry\n'
                'token=sample-ci-token secret=sample-secret\n'
                'Authorization: Bearer other-credential\n'
                '[ERROR] ENOTCONN\n'
            )
            source.write_text(original)
            (root / 'unrelated.log').write_text('must not be collected')
            collect(
                source,
                root / 'out',
                {'GITHUB_TOKEN': 'sample-ci-token', 'TEST_SECRET': 'sample-secret'},
            )
            result = (root / 'out/mason.log').read_text()
            for secret in ['sample-ci-token', 'sample-secret', 'other-credential']:
                self.assertNotIn(secret, result)
            self.assertIn('ENOTCONN', result)
            self.assertIn('https://example.invalid/registry', result)
            self.assertEqual(source.read_text(), original)
            self.assertEqual(
                {p.name for p in (root / 'out').iterdir()}, {'mason.log', 'status.txt'}
            )

    def test_missing_log_records_early_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collect(root / 'missing.log', root / 'out', {})
            self.assertIn('not created', (root / 'out/status.txt').read_text())
            self.assertFalse((root / 'out/mason.log').exists())

    def test_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'private').write_text('private content')
            (root / 'mason.log').symlink_to(root / 'private')
            with self.assertRaises(ValueError):
                collect(root / 'mason.log', root / 'out', {})
            self.assertFalse((root / 'out/mason.log').exists())


if __name__ == '__main__':
    unittest.main()

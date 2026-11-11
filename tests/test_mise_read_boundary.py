#!/usr/bin/env python3
"""R01: real chezmoi init/diff/verify with isolated HOME and acquisition stubs.

Requires Python 3 and an already installed chezmoi (CHEZMOI_BIN overrides PATH).
No mise, authentication, package installation, or external downloads are real.
"""

import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get("CHEZMOI_BIN") or shutil.which("chezmoi")


def executable(path, content, mode=0o751):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    path.chmod(mode)


def snapshot(path):
    if path.is_symlink():
        return ("symlink", os.readlink(path), path.lstat().st_mode)
    if path.is_file():
        return ("file", path.read_bytes(), path.stat().st_mode)
    if path.exists():
        return ("directory", path.stat().st_mode)
    return None


class MiseBoundary(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHEZMOI, "Install chezmoi separately or set CHEZMOI_BIN")
        self.tmp = tempfile.TemporaryDirectory(prefix="r01-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.source = self.root / "source with spaces"
        shutil.copytree(REPO, self.source, ignore=shutil.ignore_patterns(
            ".git", ".context", "__pycache__"))
        # Unrelated remote assets are excluded at the source-copy boundary.
        # Keep the actual config template, read hook and bootstrap unchanged.
        (self.source / ".chezmoiexternal.toml.tmpl").write_text("")
        self.bin = self.root / "bin"
        self.log = self.root / "calls"
        self.config = self.home / ".config/chezmoi/chezmoi.toml"
        self.mise = self.home / ".local/bin/mise"
        self.pin = (self.source / ".mise-version").read_text().strip()
        self.env = {
            "HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin",
            "XDG_CONFIG_HOME": str(self.home / ".config"),
            "XDG_DATA_HOME": str(self.home / ".local/share"),
            "XDG_STATE_HOME": str(self.home / ".local/state"),
            "XDG_CACHE_HOME": str(self.home / ".cache"),
            "TMPDIR": str(self.root), "CI": "true", "LC_ALL": "C",
            "CALL_LOG": str(self.log),
        }
        executable(self.bin / "op", "#!/bin/sh\nexit 1\n")
        executable(self.bin / "curl", '''#!/bin/sh
printf 'curl %s\\n' "$*" >> "$CALL_LOG"
[ "${ALLOW_INSTALL:-}" = yes ] || exit 93
[ "$1" = -fsSL ] && [ "$2" = https://mise.run ] && [ "$3" = -o ] || exit 94
cat > "$4" <<'INSTALLER'
printf 'installer\\n' >> "$CALL_LOG"
printf '#!/bin/sh\\necho "%s fixture"\\n' "$MISE_VERSION" > "$MISE_INSTALL_PATH"
INSTALLER
''')
        self.seed_mise(self.pin)
        result = self.chezmoi("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.generated_config = self.config.read_text()
        self.assertIn('args = ["--check"]', self.generated_config)
        self.assertIn(str(self.source / ".bootstrap-mise.sh"), self.generated_config)
        # The chosen target is real repository content, with a deliberately
        # different destination so diff/verify must actually inspect it.
        self.target = self.home / ".config/mise/conf.d/10-tools.toml"
        self.target.parent.mkdir(parents=True, exist_ok=True)
        self.target.write_text("# R01 destination differs\n")
        self.log.unlink(missing_ok=True)

    def seed_mise(self, version, mode=0o751):
        executable(self.mise, f'''#!/bin/sh
printf 'mise %s\\n' "$*" >> "$CALL_LOG"
echo "{version} fixture"
''', mode)

    def chezmoi(self, command, *args):
        return subprocess.run([
            str(CHEZMOI), "--config", str(self.config),
            "--source", str(self.source), "--destination", str(self.home),
            "--cache", str(self.home / ".cache/chezmoi"), "--color=false",
            "--no-tty", command, *args,
        ], env=self.env, cwd=self.source, text=True, capture_output=True)

    def bootstrap(self, *args):
        return subprocess.run(["/bin/sh", str(self.source / ".bootstrap-mise.sh"), *args],
                              env=self.env, cwd=self.source, text=True, capture_output=True)

    def assert_no_calls(self):
        self.assertFalse(self.log.exists(), self.log.read_text() if self.log.exists() else "")

    def test_reads_preserve_old_matching_new_and_absent_mise(self):
        # Legacy is the exact previous generated hook shape (no args), pointing
        # at the updated script. Neither configuration disables the hook.
        for legacy in (False, True):
            config = self.generated_config
            if legacy:
                config = config.replace('    args = ["--check"]\n', "")
            self.config.write_text(config)
            for version in ("0.0.0", self.pin, "9999.1.1", None):
                with self.subTest(legacy=legacy, version=version):
                    self.mise.unlink(missing_ok=True)
                    if version:
                        self.seed_mise(version)
                    else:
                        self.mise.parent.rmdir()
                    before = snapshot(self.mise)
                    parent_before = snapshot(self.mise.parent)
                    # dry-run hooks must also stay read-only.
                    for command in ("diff", "verify"):
                        for extra in ([], ["--dry-run"]):
                            result = self.chezmoi(command, *extra, str(self.target))
                            if version:
                                self.assertEqual(result.returncode, 0 if command == "diff" else 1,
                                                 result.stderr)
                                self.assertNotIn("Executable mise required", result.stderr)
                                if command == "diff":
                                    self.assertIn("R01 destination differs", result.stdout)
                            else:
                                self.assertNotEqual(result.returncode, 0)
                                self.assertIn("Executable mise required", result.stderr)
                                self.assertIn("--install", result.stderr)
                            self.assertEqual(snapshot(self.mise), before)
                            self.assertEqual(snapshot(self.mise.parent), parent_before)
                            self.assert_no_calls()

    def test_reads_preserve_unusable_and_symlink_targets(self):
        for kind in ("non-executable", "directory", "symlink", "dangling"):
            with self.subTest(kind=kind):
                self.mise.unlink(missing_ok=True)
                if kind == "non-executable":
                    self.seed_mise(self.pin, 0o640)
                elif kind == "directory":
                    self.mise.mkdir()
                else:
                    referent = self.root / "owned-elsewhere"
                    if kind == "symlink":
                        executable(referent, "#!/bin/sh\nexit 99\n")
                    else:
                        referent.unlink()
                    self.mise.symlink_to(referent)
                before = snapshot(self.mise)
                referent_before = snapshot(self.root / "owned-elsewhere")
                for command in ("diff", "verify"):
                    result = self.chezmoi(command, str(self.target))
                    if kind != "symlink":
                        self.assertIn("Executable mise required", result.stderr)
                    else:
                        self.assertEqual(result.returncode, 0 if command == "diff" else 1,
                                         result.stderr)
                    self.assertEqual(snapshot(self.mise), before)
                    self.assertEqual(snapshot(self.root / "owned-elsewhere"), referent_before)
                    self.assert_no_calls()
                if kind == "directory":
                    self.mise.rmdir()

    def test_explicit_install_only_installs_when_absent(self):
        for version in ("0.0.0", self.pin, "9999.1.1"):
            with self.subTest(version=version):
                self.seed_mise(version)
                before = snapshot(self.mise)
                result = self.bootstrap("--install")
                self.assertEqual(result.returncode, 0 if version == self.pin else 1, result.stderr)
                self.assertEqual(snapshot(self.mise), before)
                self.assertEqual(self.log.read_text(), "mise --version\n")
                self.log.unlink()
        self.mise.unlink()
        self.mise.parent.rmdir()
        self.env["ALLOW_INSTALL"] = "yes"
        result = self.bootstrap("--install")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("installer\n", self.log.read_text())
        self.assertIn(self.pin, self.mise.read_text())
        self.assertTrue(self.mise.stat().st_mode & stat.S_IXUSR)
        self.log.unlink()
        self.assertEqual(self.bootstrap("--check").returncode, 0)
        self.assert_no_calls()

    def test_install_refuses_unusable_existing_files_and_bad_arguments(self):
        self.seed_mise(self.pin, 0o640)
        before = snapshot(self.mise)
        self.assertNotEqual(self.bootstrap("--install").returncode, 0)
        self.assertEqual(snapshot(self.mise), before)
        self.assert_no_calls()
        self.mise.unlink()
        self.mise.symlink_to(self.root / "absent")
        before = snapshot(self.mise)
        self.assertNotEqual(self.bootstrap("--install").returncode, 0)
        self.assertEqual(snapshot(self.mise), before)
        for args in (("--unknown",), ("--install", "--check"), ("",)):
            result = self.bootstrap(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Usage:", result.stderr)
        self.assert_no_calls()


if __name__ == "__main__":
    unittest.main(verbosity=2)

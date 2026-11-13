"""Fault injection for the CI startup probe; no workstation config or tools."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from check_shell_startup import check_startup


class ShellStartup(unittest.TestCase):
    def setUp(self):
        self.zsh = shutil.which('zsh')
        self.assertTrue(self.zsh, 'existing zsh required')
        self.temporary = tempfile.TemporaryDirectory(prefix='shell-fixture-')
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.write(
            '.zshenv',
            '''export ZDOTDIR="$HOME/.config/zsh"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
''',
        )
        self.write('.config/mise/config.toml', '[settings]\n')
        self.write(
            '.local/bin/mise',
            '''#!/bin/sh
cat <<'ACTIVATION'
mise() { command mise "$@"; }
_mise_hook() { path=("$XDG_DATA_HOME/mise/installs/fixture/bin" $path); }
ACTIVATION
''',
            executable=True,
        )
        for name in ['node', 'chezmoi']:
            self.write(
                '.local/share/mise/installs/fixture/bin/' + name,
                '#!/bin/sh\nexit 0\n',
                executable=True,
            )
        self.write('.cache/zsh/init/zoxide.zsh', '__zoxide_z() { :; }\n')
        self.write('.cache/zsh/init/starship.zsh', 'prompt_starship_precmd() { :; }\n')
        self.rc = '''path=("$HOME/.local/bin" $path)
eval "$(mise activate zsh)"
source "$HOME/.cache/zsh/init/zoxide.zsh"
source "$HOME/.cache/zsh/init/starship.zsh"
'''
        self.write('.config/zsh/.zshrc', self.rc)

    def write(self, relative, content, executable=False):
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        if executable:
            path.chmod(0o700)

    def test_ready(self):
        check_startup(self.home, self.zsh)

    def test_failed_activation_cannot_hide_behind_successful_last_command(self):
        self.write('.local/bin/mise', '#!/bin/sh\nexit 1\n', executable=True)
        with self.assertRaises(RuntimeError):
            check_startup(self.home, self.zsh)

    def test_empty_init_is_not_ready(self):
        self.write('.cache/zsh/init/starship.zsh', '')
        with self.assertRaises(RuntimeError):
            check_startup(self.home, self.zsh)

    def test_authentication_cannot_be_swallowed(self):
        self.write('.config/zsh/.zshrc', self.rc + 'op whoami >/dev/null 2>&1 || true\n')
        with self.assertRaisesRegex(RuntimeError, 'attempted authentication'):
            check_startup(self.home, self.zsh)

    def test_stderr_is_not_ignored(self):
        self.write('.config/zsh/.zshrc', self.rc + 'print error >&2\n')
        with self.assertRaises(RuntimeError):
            check_startup(self.home, self.zsh)

    def test_hung_startup_times_out(self):
        self.write('.config/zsh/.zshrc', self.rc + 'while true; do :; done\n')
        with self.assertRaises(subprocess.TimeoutExpired):
            check_startup(self.home, self.zsh, timeout=0.2)

#!/usr/bin/env python3
"""Exercise a provisioned CI HOME, never the workstation's startup files.

The caller supplies the disposable HOME explicitly. No installation or apply is
performed. Zsh/mise may write caches inside that HOME; authentication is denied.
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


STARTUP_CHECK = r'''
setopt err_exit nounset
[[ "$ZDOTDIR" == "$HOME/.config/zsh" ]]
[[ "$XDG_CONFIG_HOME" == "$HOME/.config" ]]
[[ "$XDG_DATA_HOME" == "$HOME/.local/share" ]]
[[ "$(whence -p mise)" == "$HOME/.local/bin/mise" ]]
(( $+functions[mise] && $+functions[_mise_hook] ))
(( $+functions[__zoxide_z] && $+functions[prompt_starship_precmd] ))
# A noninteractive command does not display a prompt. Exercise the activation
# hook explicitly, so merely defining it cannot pass the tool-selection check.
_mise_hook
[[ "$(whence -p chezmoi)" == "$XDG_DATA_HOME/mise/installs/"* ]]
[[ "$(whence -p node)" == "$XDG_DATA_HOME/mise/installs/"* ]]
[[ "$(whence -p op)" == "$SHELL_CHECK_STUB/op" ]]
print -r -- DOTFILES_SHELL_READY
'''


def check_startup(home, zsh, timeout=30):
    home = Path(home).resolve(strict=True)
    for relative in [
        '.zshenv',
        '.config/zsh/.zshrc',
        '.config/mise/config.toml',
        '.local/bin/mise',
        '.cache/zsh/init/zoxide.zsh',
        '.cache/zsh/init/starship.zsh',
    ]:
        if not (home / relative).is_file():
            raise RuntimeError('missing shell prerequisite: ' + relative)
    config = (home / '.config/mise/config.toml').read_text()
    if any(line.lstrip().startswith('credential_command') for line in config.splitlines()):
        raise RuntimeError('global mise config must not define credential_command')
    with tempfile.TemporaryDirectory(prefix='shell-startup-') as temporary:
        root = Path(temporary)
        op = root / 'op'
        op.write_text('#!/bin/sh\nprintf called >> "$SHELL_CHECK_STUB/auth-called"\nexit 91\n')
        op.chmod(0o700)
        # No ambient tokens, SSH agent, mise overrides, user config or CI secrets.
        env = {
            'HOME': str(home),
            'ZDOTDIR': str(home),
            'PATH': f'{root}:/usr/bin:/bin:/usr/sbin:/sbin',
            'TERM': 'xterm-256color',
            'LC_ALL': 'C',
            'TMPDIR': str(root),
            'SHELL_CHECK_STUB': str(root),
            'MISE_AUTO_INSTALL': 'false',
            'MISE_TASK_RUN_AUTO_INSTALL': 'false',
            'MISE_NOT_FOUND_AUTO_INSTALL': 'false',
            'MISE_GITHUB_CREDENTIAL_COMMAND': str(op),
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': os.devnull,
        }
        result = subprocess.run(
            [zsh, '-d', '-l', '-i', '-c', STARTUP_CHECK],
            env=env,
            cwd=home,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if (root / 'auth-called').exists():
            raise RuntimeError('shell startup attempted authentication')
        if result.returncode or result.stderr or 'DOTFILES_SHELL_READY\n' not in result.stdout:
            # Do not publish shell output: future configs may print sensitive data.
            raise RuntimeError(
                f'shell startup failed (exit={result.returncode}, stderr={bool(result.stderr)})'
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', required=True, help='provisioned disposable CI HOME')
    args = parser.parse_args()
    zsh = shutil.which('zsh')
    if not zsh:
        parser.error('an existing zsh executable is required')
    check_startup(args.home, zsh)
    print('Provisioned shell startup passed without authentication.')

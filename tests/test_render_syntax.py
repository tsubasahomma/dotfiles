#!/usr/bin/env python3
"""Render simulated platform/CI branches; parse shell and Lua without executing.

Config acquisition is tested by R01/R02. Shared templates are exercised through
consumers. External declarations are rendered as text, never downloaded.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
NVIM = os.environ.get('NVIM_BIN') or shutil.which('nvim')
ZSH = os.environ.get('ZSH_BIN') or shutil.which('zsh')


class RenderSyntax(unittest.TestCase):
    def test_platform_and_ci_branches(self):
        self.assertTrue(CHEZMOI and NVIM and ZSH, 'installed chezmoi, Neovim and Zsh required')
        with tempfile.TemporaryDirectory(prefix='render-') as temporary:
            root = Path(temporary).resolve()
            home = root / 'home'; home.mkdir()
            source = root / 'source'
            shutil.copytree(REPO, source, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            # No init/apply, hooks or external resolution. Retain source includes.
            config = root / 'config.json'
            bin_dir = root / 'bin'; bin_dir.mkdir()
            wezterm = root / 'dummy-wezterm.exe'; wezterm.touch()
            stub = bin_dir / 'wslpath'
            stub.write_text('#!/bin/sh\nprintf "%s\\n" "$FIXTURE_WEZTERM"\n'); stub.chmod(0o700)
            env = {'HOME': str(home), 'PATH': f'{bin_dir}:/usr/bin:/bin',
                   'TMPDIR': str(root), 'LC_ALL': 'C', 'FIXTURE_WEZTERM': str(wezterm),
                   'WSL_DISTRO_NAME': 'FixtureDistro', 'GIT_CONFIG_NOSYSTEM': '1',
                   'GIT_CONFIG_GLOBAL': str(home / '.gitconfig')}
            paths = {'home': str(home), 'mise': str(home / '.local/bin/mise'),
                     'op': str(bin_dir / 'op'), 'op_sign': '/fixture/sign-helper',
                     'true_cmd': '/usr/bin/true'}
            for key, part in [('config', '.config'), ('cache', '.cache'),
                              ('data', '.local/share'), ('state', '.local/state')]:
                paths['xdg_' + key] = str(home / part)
                env[f'XDG_{key.upper()}_HOME'] = str(home / part)

            def run(args, **kwargs):
                result = subprocess.run([str(a) for a in args], env=env, cwd=root,
                                        capture_output=True, text=True, timeout=40, **kwargs)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result.stdout

            run(['/usr/bin/ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-C', 'fixture', '-f', root / 'key'])
            key = (root / 'key.pub').read_text().strip()
            identity = {'item_id': 'fixture', 'account_id': 'fixture', 'key_type': 'ed25519',
                        'key_hash': hashlib.sha256(key.encode()).hexdigest()[:8],
                        'public_key': key, 'name': 'Fixture', 'email': 'fixture@example.test', 'dirs': '~/work'}
            templates = sorted(p for p in source.rglob('*.tmpl')
                               if '.chezmoitemplates' not in p.parts and p.name != '.chezmoi.toml.tmpl')
            self.assertGreater(len(templates), 40)
            lua_parser = root / 'parse.lua'
            lua_parser.write_text('for _, path in ipairs(arg) do assert(loadfile(path)) end\n')
            for platform, osid, arch, wsl in [('macos', 'darwin', 'arm64', False),
                                             ('linux', 'linux', 'amd64', False),
                                             ('wsl', 'linux', 'amd64', True)]:
                for ci in (False, True):
                    with self.subTest(platform=platform, ci=ci):
                        if ci:
                            env['CI'] = 'true'
                        else:
                            env.pop('CI', None)
                        data = dict(paths=paths, identities=[identity], is_wsl=wsl,
                                    osid=osid, arch=arch, windows_user='fixture',
                                    brew_prefix='/opt/homebrew' if osid == 'darwin' else '/home/linuxbrew/.linuxbrew',
                                    ssh_auth_sock=r'\\.\pipe\openssh-ssh-agent' if wsl else '',
                                    op_status='ready', ssh_keys_hash='fixture')
                        config.write_text(json.dumps({'data': data}))
                        rendered = root / f'{platform}-{ci}'; rendered.mkdir()
                        shell_count = 0
                        lua_files = list(source.rglob('*.lua'))
                        for number, template in enumerate(templates):
                            relative = template.relative_to(source)
                            # Simulate the builtin fields too; this is render coverage,
                            # not execution on the simulated OS/architecture.
                            prefix = '{{- $_ := set .chezmoi "os" .osid -}}{{- $_ := set .chezmoi "arch" .arch -}}'
                            text = run([CHEZMOI, '--config', config, '--source', source,
                                        '--destination', home, '--cache', home / '.cache/chezmoi',
                                        '--no-tty', 'execute-template'], input=prefix + template.read_text())
                            target = rendered / str(number); target.write_text(text)
                            shell = None
                            if text.startswith('#!'):
                                interpreter = text.splitlines()[0].split('/')[-1].split()[-1]
                                self.assertIn(interpreter, ('bash', 'sh', 'zsh'), str(relative))
                                shell = ZSH if interpreter == 'zsh' else '/bin/' + interpreter
                            elif relative.name == 'dot_zshenv.tmpl' or relative.parts[:2] == ('dot_config', 'zsh'):
                                shell = ZSH
                            if shell and text.strip():
                                run([shell, '-n', target]); shell_count += 1
                            if template.name.endswith('.lua.tmpl'):
                                lua_files.append(target)
                        # Plain startup scripts and bootstrap also require syntax checks.
                        for plain in [source / '.bootstrap-mise.sh']:
                            self.assertTrue(plain.is_file(), str(plain))
                            run([ZSH if plain.name == 'dot_zshenv' else '/bin/sh', '-n', plain])
                            shell_count += 1
                        run([NVIM, '--headless', '-u', 'NONE', '--noplugin', '-i', 'NONE', '-n',
                             '-l', lua_parser, *lua_files])
                        print(f'Render/syntax {platform} CI={ci}: {len(templates)} templates, '
                              f'{shell_count} shell, {len(lua_files)} Lua (parse only)', flush=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)

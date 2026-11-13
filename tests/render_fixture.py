"""Render every standalone template for simulated platform and CI branches.

Shared by the render syntax test and the shellcheck lint. Nothing is applied,
no hooks run and external declarations are rendered as text, never fetched.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[1]
BRANCHES = [
    ('macos', 'darwin', 'arm64', False),
    ('linux', 'linux', 'amd64', False),
    ('wsl', 'linux', 'amd64', True),
]


class RenderError(AssertionError):
    pass


def shell_of(relative, text):
    """Return 'bash', 'sh', 'zsh' or None for a rendered template."""
    if text.startswith('#!'):
        interpreter = text.splitlines()[0].split('/')[-1].split()[-1]
        if interpreter not in ('bash', 'sh', 'zsh'):
            raise RenderError(f'{relative}: unexpected interpreter {interpreter}')
        return interpreter
    if relative.name == 'dot_zshenv.tmpl' or relative.parts[:2] == ('dot_config', 'zsh'):
        return 'zsh'
    return None


class Renderer:
    """A copied source and temporary HOME; call render() per platform branch."""

    def __init__(self, root, chezmoi):
        self.root, self.chezmoi = Path(root), chezmoi
        self.home = self.root / 'home'
        self.home.mkdir()
        self.source = self.root / 'source'
        shutil.copytree(REPO, self.source, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        # No init/apply, hooks or external resolution. Retain source includes.
        self.config = self.root / 'config.json'
        bin_dir = self.root / 'bin'
        bin_dir.mkdir()
        wezterm = self.root / 'dummy-wezterm.exe'
        wezterm.touch()
        stub = bin_dir / 'wslpath'
        stub.write_text('#!/bin/sh\nprintf "%s\\n" "$FIXTURE_WEZTERM"\n')
        stub.chmod(0o700)
        home = self.home
        self.env = {
            'HOME': str(home),
            'PATH': f'{bin_dir}:/usr/bin:/bin',
            'TMPDIR': str(self.root),
            'LC_ALL': 'C',
            'FIXTURE_WEZTERM': str(wezterm),
            'WSL_DISTRO_NAME': 'FixtureDistro',
            'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': str(home / '.gitconfig'),
        }
        self.paths = {
            'home': str(home),
            'mise': str(home / '.local/bin/mise'),
            'op': str(bin_dir / 'op'),
            'op_sign': '/fixture/sign-helper',
        }
        for key, part in [
            ('config', '.config'),
            ('cache', '.cache'),
            ('data', '.local/share'),
            ('state', '.local/state'),
        ]:
            self.paths['xdg_' + key] = str(home / part)
            self.env[f'XDG_{key.upper()}_HOME'] = str(home / part)
        self.run(
            [
                '/usr/bin/ssh-keygen',
                '-q',
                '-t',
                'ed25519',
                '-N',
                '',
                '-C',
                'fixture',
                '-f',
                self.root / 'key',
            ]
        )
        key = (self.root / 'key.pub').read_text().strip()
        self.identity = {
            'item_id': 'fixture',
            'account_id': 'fixture',
            'key_type': 'ed25519',
            'key_hash': hashlib.sha256(key.encode()).hexdigest()[:8],
            'public_key': key,
            'name': 'Fixture',
            'email': 'fixture@example.test',
            'dirs': '~/work',
        }
        self.templates = sorted(
            p
            for p in self.source.rglob('*.tmpl')
            if '.chezmoitemplates' not in p.parts and p.name != '.chezmoi.toml.tmpl'
        )

    def run(self, args, **kwargs):
        result = subprocess.run(
            [str(a) for a in args],
            env=self.env,
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=40,
            **kwargs,
        )
        if result.returncode != 0:
            raise RenderError(f'{" ".join(map(str, args))}\n{result.stdout}{result.stderr}')
        return result.stdout

    def render(self, platform, osid, arch, wsl, ci):
        """Render all templates for one branch; return [(relative, path, shell)]."""
        if ci:
            self.env['CI'] = 'true'
        else:
            self.env.pop('CI', None)
        data = dict(
            paths=self.paths,
            identities=[self.identity],
            is_wsl=wsl,
            osid=osid,
            arch=arch,
            brew_prefix='/opt/homebrew' if osid == 'darwin' else '/home/linuxbrew/.linuxbrew',
            ssh_auth_sock=r'\\.\pipe\openssh-ssh-agent' if wsl else '',
        )
        self.config.write_text(json.dumps({'data': data}))
        rendered = self.root / f'{platform}-{ci}'
        rendered.mkdir()
        records = []
        for number, template in enumerate(self.templates):
            relative = template.relative_to(self.source)
            # Simulate the builtin fields too; this is render coverage,
            # not execution on the simulated OS/architecture.
            prefix = '{{- $_ := set .chezmoi "os" .osid -}}{{- $_ := set .chezmoi "arch" .arch -}}'
            text = self.run(
                [
                    self.chezmoi,
                    '--config',
                    self.config,
                    '--source',
                    self.source,
                    '--destination',
                    self.home,
                    '--cache',
                    self.home / '.cache/chezmoi',
                    '--no-tty',
                    'execute-template',
                ],
                input=prefix + template.read_text(),
            )
            target = rendered / str(number)
            target.write_text(text)
            records.append((relative, target, shell_of(relative, text) if text.strip() else None))
        return records

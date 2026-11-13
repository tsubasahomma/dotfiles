#!/usr/bin/env python3
"""Render simulated platform/CI branches; parse shell and Lua without executing.

Config acquisition is tested by R01/R02. Shared templates are exercised through
consumers. External declarations are rendered as text, never downloaded.
"""

import os
from pathlib import Path
import shutil
import tempfile
import unittest

import render_fixture

CHEZMOI = os.environ.get('CHEZMOI_BIN') or shutil.which('chezmoi')
NVIM = os.environ.get('NVIM_BIN') or shutil.which('nvim')
ZSH = os.environ.get('ZSH_BIN') or shutil.which('zsh')


class RenderSyntax(unittest.TestCase):
    def test_platform_and_ci_branches(self):
        self.assertTrue(CHEZMOI and NVIM and ZSH, 'installed chezmoi, Neovim and Zsh required')
        with tempfile.TemporaryDirectory(prefix='render-') as temporary:
            renderer = render_fixture.Renderer(Path(temporary).resolve(), CHEZMOI)
            source, run = renderer.source, renderer.run
            self.assertGreater(len(renderer.templates), 40)
            lua_parser = renderer.root / 'parse.lua'
            lua_parser.write_text('for _, path in ipairs(arg) do assert(loadfile(path)) end\n')
            for branch in render_fixture.BRANCHES:
                for ci in (False, True):
                    with self.subTest(platform=branch[0], ci=ci):
                        shell_count = 0
                        lua_files = list(source.rglob('*.lua'))
                        for relative, target, shell in renderer.render(*branch, ci):
                            if shell:
                                run([ZSH if shell == 'zsh' else '/bin/' + shell, '-n', target])
                                shell_count += 1
                            if relative.name.endswith('.lua.tmpl'):
                                lua_files.append(target)
                        # Plain startup scripts and bootstrap also require syntax checks.
                        for plain in [source / '.bootstrap-mise.sh']:
                            self.assertTrue(plain.is_file(), str(plain))
                            run(['/bin/sh', '-n', plain])
                            shell_count += 1
                        run(
                            [
                                NVIM,
                                '--headless',
                                '-u',
                                'NONE',
                                '--noplugin',
                                '-i',
                                'NONE',
                                '-n',
                                '-l',
                                lua_parser,
                                *lua_files,
                            ]
                        )
                        print(
                            f'Render/syntax {branch[0]} CI={ci}: {len(renderer.templates)} templates, '
                            f'{shell_count} shell, {len(lua_files)} Lua (parse only)',
                            flush=True,
                        )


if __name__ == '__main__':
    unittest.main(verbosity=2)

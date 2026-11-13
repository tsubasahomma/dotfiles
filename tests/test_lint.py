#!/usr/bin/env python3
"""Static lint for every language in the repository; nothing is changed or applied.

Python: Ruff (lint and format, .ruff.toml). Lua: StyLua (.editorconfig). Shell:
shfmt on plain scripts, ShellCheck on the rendered sh/bash templates. Workflows:
actionlint and zizmor (offline). Run through python3 tests/run_checks.py lint,
which supplies the pinned binaries as NAME_BIN.
"""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import render_fixture

REPO = Path(__file__).resolve().parents[1]
# Same options as the pre-commit hook: two spaces, indented cases, spaced redirects.
SHFMT_OPTIONS = ['-i', '2', '-ci', '-sr']
# ShellCheck codes ignored everywhere.
SHELLCHECK_EXCLUDE = {
    # Templates render their branches into constants such as [[ "true" != "true" ]].
    'SC2050': 'constant expression rendered from a template value',
    # `VAR= command` clears a variable for one command on purpose (CDPATH= cd).
    'SC1007': 'one-command variable reset',
}
# ShellCheck codes ignored in one template, with the reason.
SHELLCHECK_FILE_EXCLUDE = {
    # The shared diagnostic preamble declares HAS_ERROR for the checks; this entry
    # only dispatches to them.
    'dot_local/bin/executable_dotfiles-diagnose.tmpl': ['SC2034'],
    # Sources the distribution's os-release file, which only exists on the target.
    '.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl': ['SC1090'],
}
# Rendered Lua is parse-checked by test_render_syntax; StyLua sees only plain files.
STYLUA_SKIP_SUFFIX = '.lua.tmpl'
# PENDING: deployed and not yet formatted. Formatting changes the files on every
# workstation, so it waits for the owner's approval in its own pull request.
STYLUA_PENDING = ['.chezmoitemplates/lazy_lock_update.lua', '.chezmoitemplates/lazy_restore.lua']


def tool(name):
    value = os.environ.get(name.upper().replace('-', '_') + '_BIN')
    if not value:
        raise AssertionError(f'{name} is required; run through tests/run_checks.py lint')
    return value


def tracked(*patterns):
    """Tracked and new (not ignored) files, so unstaged additions are linted too."""
    result = subprocess.run(
        [
            tool('git'),
            '-C',
            str(REPO),
            'ls-files',
            '--cached',
            '--others',
            '--exclude-standard',
            '-z',
            '--',
            *patterns,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(
        {REPO / name for name in result.stdout.split('\0') if name and (REPO / name).is_file()}
    )


def plain_shell_scripts():
    scripts = []
    for path in tracked():
        if path.suffix == '.tmpl' or '.git' in path.parts:
            continue
        try:
            first = path.open('rb').readline()
        except OSError:
            continue
        if first.startswith(b'#!') and first.rstrip().split(b'/')[-1].split()[-1] in (
            b'sh',
            b'bash',
        ):
            scripts.append(path)
    return scripts


class Lint(unittest.TestCase):
    def check(self, args, **kwargs):
        result = subprocess.run(
            [str(a) for a in args], cwd=REPO, capture_output=True, text=True, timeout=120, **kwargs
        )
        self.assertEqual(
            result.returncode, 0, f'{" ".join(map(str, args))}\n{result.stdout}{result.stderr}'
        )
        return result

    def test_ruff_lint(self):
        self.check([tool('ruff'), 'check', '--no-cache', '--output-format', 'concise', '.'])

    def test_ruff_format(self):
        self.check([tool('ruff'), 'format', '--no-cache', '--check', '--diff', '.'])

    def test_stylua(self):
        pending = {REPO / name for name in STYLUA_PENDING}
        files = [
            p
            for p in tracked('*.lua')
            if not p.name.endswith(STYLUA_SKIP_SUFFIX) and p not in pending
        ]
        self.assertGreater(len(files), 10)
        self.check([tool('stylua'), '--check', *files])

    def test_shfmt_plain_scripts(self):
        scripts = plain_shell_scripts()
        self.assertIn(REPO / '.bootstrap-mise.sh', scripts)
        self.check([tool('shfmt'), '-d', *SHFMT_OPTIONS, *scripts])

    def test_shellcheck_plain_scripts(self):
        scripts = plain_shell_scripts()
        self.check(
            [tool('shellcheck'), '-S', 'warning', '-e', ','.join(SHELLCHECK_EXCLUDE), *scripts]
        )

    def test_shellcheck_rendered_templates(self):
        unknown = [name for name in SHELLCHECK_FILE_EXCLUDE if not (REPO / name).is_file()]
        self.assertEqual(unknown, [], 'SHELLCHECK_FILE_EXCLUDE names a missing template')
        with tempfile.TemporaryDirectory(prefix='lint-render-') as temporary:
            renderer = render_fixture.Renderer(temporary, tool('chezmoi'))
            # Every branch can render different code; check each distinct output once.
            outputs = {}
            for branch in render_fixture.BRANCHES:
                for ci in (False, True):
                    for relative, path, shell in renderer.render(*branch, ci):
                        if shell in ('sh', 'bash'):
                            outputs.setdefault((str(relative), path.read_text()), (path, shell))
            self.assertGreater(len(outputs), 30)
            failures = []
            for (relative, _), (path, shell) in sorted(outputs.items()):
                codes = list(SHELLCHECK_EXCLUDE) + SHELLCHECK_FILE_EXCLUDE.get(relative, [])
                result = subprocess.run(
                    [
                        tool('shellcheck'),
                        '-S',
                        'warning',
                        '-s',
                        shell,
                        '-f',
                        'gcc',
                        '-e',
                        ','.join(codes),
                        str(path),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode != 0:
                    failures.append(result.stdout.replace(str(path), relative) + result.stderr)
            self.assertEqual(failures, [], '\n'.join(failures))

    def test_actionlint(self):
        # actionlint also runs ShellCheck on run: scripts when it finds it on PATH.
        self.check([tool('actionlint'), '-shellcheck', tool('shellcheck')])

    def test_zizmor(self):
        # Offline: no token, so the audits that query GitHub are not run here.
        self.check([tool('zizmor'), '--offline', '--no-progress', '.github/workflows'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

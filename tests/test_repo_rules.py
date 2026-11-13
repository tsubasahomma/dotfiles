#!/usr/bin/env python3
"""Repository rules that the documents state and a machine can check.

Static reads only. Existing violations that need a deployed change or a document
rewrite are listed with the reason and may only shrink. The script naming
rule waits for its definition in roadmap item P2-2 and is not checked yet.
"""

import datetime
import os
from pathlib import Path
import re
import subprocess
import unittest

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / '.chezmoi.toml.tmpl'
EXTERNALS = REPO / '.chezmoiexternal.toml.tmpl'
# PENDING: data keys no template reads. Removing one changes the config that
# `chezmoi init` generates on every workstation, so it waits for approval.
UNUSED_DATA = {'arch': 'templates use .chezmoi.arch; the data copy is unused'}
# PENDING (roadmap P4): footnotes that no sentence cites yet; choosing where to
# cite them is part of the document rewrite.
UNCITED_FOOTNOTES = {
    ('docs/development.md', 'scripts'),
    ('docs/development.md', 'wrapper'),
    ('docs/operations.md', 'lazy'),
    ('docs/operations.md', 'repair-nvim'),
    ('docs/validation.md', 'hooks'),
}
# PENDING (roadmap P4-2): links to this repository fixed at an old commit, as
# a ceiling per file. The counts may only go down.
PINNED_SELF_LINKS = {
    'docs/decisions/convergence.md': 10,
    # Names the commit the 2026-11-13 evaluation read; merged before this rule.
    'docs/decisions/generated-state.md': 2,
    'docs/decisions/okf.md': 4,
    'docs/development.md': 8,
    'docs/identity.md': 2,
    'docs/operations.md': 18,
    'docs/ownership.md': 12,
    'docs/platforms/macos.md': 4,
    'docs/platforms/wsl.md': 4,
    'docs/validation.md': 2,
}
SELF_LINK = re.compile(
    r'(?:github\.com/tsubasahomma/dotfiles/(?:blob|tree|raw|commit)/'
    r'|raw\.githubusercontent\.com/tsubasahomma/dotfiles/)[0-9a-f]{7,40}\b'
)
MUTABLE_REF = re.compile(r'/(?:main|master|HEAD|latest)(?:/|$)|refs/heads/|/releases/latest\b')


def files(*patterns):
    git = os.environ.get('GIT_BIN') or 'git'
    result = subprocess.run(
        [git, '-C', str(REPO), 'ls-files', '--cached', '--others', '--exclude-standard', '-z', '--']
        + list(patterns),
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted({REPO / n for n in result.stdout.split('\0') if n and (REPO / n).is_file()})


def documents():
    """Markdown files with OKF front matter: (relative name, front matter, body)."""
    for path in files('*.md'):
        text = path.read_text()
        if text.startswith('---\n') and '\n---\n' in text[4:]:
            end = text.index('\n---\n', 4)
            yield str(path.relative_to(REPO)), text[4:end], text[end + 5 :]


class RepoRules(unittest.TestCase):
    def test_every_data_key_is_read_by_a_template(self):
        config = CONFIG.read_text()
        start = config.index('\n[data]') + 1
        # The data section ends at the next top-level table that is not data.*.
        end = re.compile(r'^\[(?!data[.\]])', re.M).search(config, start).start()
        data = config[start:end]
        top, nested, section = [], [], None
        for line in data.splitlines():
            header = re.match(r'\s*\[data(?:\.(\w+))?\]', line)
            if header:
                section = header.group(1)
                continue
            key = re.match(r'\s*(\w+)\s*=', line)
            if key:
                (nested if section else top).append((section, key.group(1)))
        for path in (REPO / '.chezmoidata').iterdir():
            top += [(None, key) for key in re.findall(r'^(\w+):', path.read_text(), re.M)]
        self.assertGreater(len(top) + len(nested), 10)
        readers = '\n'.join(
            p.read_text()
            for p in files()
            if p != CONFIG and (p.name.endswith('.tmpl') or '.chezmoitemplates' in p.parts)
        )
        unused = set()
        for section, key in top + nested:
            name = f'{section}.{key}' if section else key
            if not re.search(r'(?<![\w.])\$?\.' + re.escape(name) + r'\b', readers):
                unused.add(name)
        self.assertEqual(unused, set(UNUSED_DATA), 'data keys without a template reader')

    def test_tmpl_files_contain_template_syntax(self):
        # The suffix makes chezmoi render the file. Files in .chezmoitemplates are
        # templates by location, so their suffix is only a name.
        plain = [
            str(p.relative_to(REPO))
            for p in files('*.tmpl')
            if '.chezmoitemplates' not in p.parts and '{{' not in p.read_text()
        ]
        self.assertEqual(plain, [], 'drop the .tmpl suffix from files without template syntax')

    def test_externals_use_immutable_references(self):
        entries = re.split(r'^\[', EXTERNALS.read_text(), flags=re.M)[1:]
        self.assertGreater(len(entries), 3)
        for entry in entries:
            name = entry.split(']', 1)[0]
            urls = re.findall(r'^\s*url\s*=\s*"([^"]+)"', entry, re.M)
            with self.subTest(external=name):
                self.assertEqual(len(urls), 1, 'one url per external')
                self.assertIsNone(MUTABLE_REF.search(urls[0]), f'mutable reference: {urls[0]}')
                # A commit SHA fixes the content; anything else needs a checksum.
                fixed = re.search(r'/[0-9a-f]{40}/', urls[0]) or re.search(
                    r'^\s*checksum\.sha(?:256|384|512)\s*=', entry, re.M
                )
                self.assertTrue(fixed, f'needs a commit SHA in the URL or a checksum: {urls[0]}')

    def test_document_sources_and_footnotes_match(self):
        checked = 0
        for name, front, body in documents():
            ids = re.findall(r'^\s*- id:\s*(\S+)', front, re.M)
            definitions = re.findall(r'^\[\^([^\]]+)\]:', body, re.M)
            citations = set(re.findall(r'\[\^([^\]]+)\](?!:)', body))
            with self.subTest(document=name):
                self.assertEqual(len(ids), len(set(ids)), 'duplicate source id')
                self.assertEqual(len(definitions), len(set(definitions)), 'duplicate footnote')
                self.assertEqual(set(ids), set(definitions), 'sources and footnotes differ')
                self.assertEqual(citations - set(definitions), set(), 'undefined footnote')
                uncited = {(name, i) for i in set(definitions) - citations}
                self.assertLessEqual(uncited, UNCITED_FOOTNOTES, 'cite every footnote')
            checked += bool(ids)
        self.assertGreater(checked, 5)

    def test_no_new_links_pinned_to_old_commits(self):
        counts = {}
        for path in files('*.md'):
            found = len(SELF_LINK.findall(path.read_text()))
            if found:
                counts[str(path.relative_to(REPO))] = found
        grown = {
            name: count for name, count in counts.items() if count > PINNED_SELF_LINKS.get(name, 0)
        }
        self.assertEqual(grown, {}, 'link to this repository by a relative path, not an old commit')

    def test_no_document_is_past_stale_after(self):
        today = datetime.datetime.now(datetime.UTC).date()
        expired = []
        for name, front, _ in documents():
            match = re.search(r'^stale_after:\s*"?(\d{4}-\d{2}-\d{2})', front, re.M)
            if match and datetime.date.fromisoformat(match.group(1)) < today:
                expired.append(f'{name} ({match.group(1)})')
        self.assertEqual(expired, [], 'review these documents and move stale_after')


if __name__ == '__main__':
    unittest.main(verbosity=2)

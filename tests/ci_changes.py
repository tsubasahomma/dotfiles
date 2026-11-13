#!/usr/bin/env python3
"""Tell CI whether a change touches only documents.

Documents are the docs/ tree and the repository's own Markdown and license
files, none of which chezmoi deploys. Anything else, an unknown event or a
missing base runs every job. Writes docs_only=true|false to GITHUB_OUTPUT.
"""

import argparse
import os
import re
import subprocess
import sys

DOCUMENT = re.compile(r'^(?:docs/.+\.md|AGENTS\.md|CLAUDE\.md|GEMINI\.md|README\.md|LICENSE)$')
NO_BASE = re.compile(r'^0*$')


def docs_only(paths):
    return bool(paths) and all(DOCUMENT.match(path) for path in paths)


def changed_paths(base, head):
    # Three dots: what the head adds since it left the base, as a pull request shows it.
    result = subprocess.run(
        ['git', 'diff', '--name-only', '-z', '--no-renames', f'{base}...{head}'],
        capture_output=True,
        text=True,
        check=True,
    )
    return [path for path in result.stdout.split('\0') if path]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--event', required=True)
    parser.add_argument('--base', default='')
    parser.add_argument('--head', required=True)
    args = parser.parse_args()
    paths = []
    if args.event in ('pull_request', 'push') and not NO_BASE.match(args.base):
        paths = changed_paths(args.base, args.head)
    result = docs_only(paths)
    print(f'{args.event}: {len(paths)} changed path(s); docs_only={str(result).lower()}')
    for path in paths:
        print(f'  {"doc " if DOCUMENT.match(path) else "code"} {path}')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            output.write(f'docs_only={str(result).lower()}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())

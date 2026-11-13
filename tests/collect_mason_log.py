#!/usr/bin/env python3
"""Collect only a failed CI restore's Mason log, redacting CI credentials."""

import argparse
import os
from pathlib import Path
import re


def collect(log_file, output_dir, env):
    output_dir.mkdir(parents=True, exist_ok=True)
    if log_file.is_symlink():
        raise ValueError('Refusing a symlink for the Mason log')
    if not log_file.is_file():
        (output_dir / 'status.txt').write_text('Mason log was not created before restore failed.\n')
        return
    content = log_file.read_text(errors='replace')
    secrets = {
        value
        for key, value in env.items()
        if value and re.search(r'TOKEN|SECRET|PASSWORD', key, re.I)
    }
    for value in sorted(secrets, key=len, reverse=True):
        content = content.replace(value, '[REDACTED]')
    content = re.sub(r'(?im)(authorization\s*[:=]\s*)[^\r\n]+', r'\1[REDACTED]', content)
    (output_dir / 'mason.log').write_text(content)
    (output_dir / 'status.txt').write_text('Collected Mason log with CI credential redaction.\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log-file', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    collect(args.log_file, args.output_dir, os.environ)


if __name__ == '__main__':
    main()

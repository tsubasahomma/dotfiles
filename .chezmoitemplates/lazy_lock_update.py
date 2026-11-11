"""Generate a retained lock candidate from a local Git revision; never publish it."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ENGINE = '85c7ff3711b730b4030d03144f6db6375044ae82'
PREFIX = 'dot_config/nvim/'
# Only literal .tmpl suffixes are supported, not chezmoi's target-name transforms.
ATTRIBUTES = tuple(x + '_' for x in (
    'after', 'before', 'create', 'dot', 'empty', 'encrypted', 'exact', 'executable',
    'external', 'literal', 'modify', 'once', 'onchange', 'private', 'readonly', 'remove', 'run', 'symlink'))


def read_lock(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('Duplicate lock key: ' + key)
            out[key] = value
        return out
    lock = json.loads(path.read_text(), object_pairs_hook=unique)
    if not isinstance(lock, dict) or not lock:
        raise ValueError('Lock must be a nonempty object')
    for name, value in lock.items():
        if (not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or name in ('.', '..')
                or not isinstance(value, dict) or set(value) != {'branch', 'commit'}
                or not isinstance(value['branch'], str) or not value['branch']
                or not isinstance(value['commit'], str)
                or not re.fullmatch(r'[0-9a-f]{40}', value['commit'])):
            raise ValueError('Invalid lock entry: ' + name)
    return lock


def binary(value, name):
    path = Path(value or shutil.which(name) or '').absolute()
    if 'shims' in path.parts or not path.is_file() or not os.access(path, os.X_OK):
        raise ValueError('Supply an installed executable with --' + name + ' (no shims): ' + str(path))
    return str(path.resolve())


def generate(args, artifact):
    git, nvim = binary(args.git, 'git'), binary(args.nvim, 'nvim')
    home = artifact / 'home'; home.mkdir()
    bins = artifact / 'bin'; bins.mkdir()
    (bins / 'git').symlink_to(git)
    env = {'HOME': str(home), 'PATH': str(bins) + ':/usr/bin:/bin:/usr/sbin:/sbin',
           'LC_ALL': 'C', 'TMPDIR': str(artifact), 'GIT_CONFIG_NOSYSTEM': '1',
           'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_TERMINAL_PROMPT': '0',
           'GIT_OPTIONAL_LOCKS': '0',
           'NVIM_APPNAME': 'nvim', 'NVIM_LOG_FILE': str(artifact / 'nvim.log'),
           'XDG_CONFIG_DIRS': str(artifact / 'empty-config'),
           'XDG_DATA_DIRS': str(artifact / 'empty-data')}
    for key in ('CONFIG', 'DATA', 'STATE', 'CACHE', 'RUNTIME'):
        dest = artifact / key.lower(); dest.mkdir()
        env['XDG_' + key + ('_DIR' if key == 'RUNTIME' else '_HOME')] = str(dest)
    def run(command, timeout=180, source_read=False):
        result = subprocess.run(command, cwd=artifact, env=dict(env, GIT_NO_LAZY_FETCH="1") if source_read else env, capture_output=True, timeout=timeout)
        with (artifact / 'commands.log').open('ab') as log:
            log.write((json.dumps(command) + '\n').encode() + (b'' if source_read else result.stdout) + result.stderr)
        if result.returncode:
            raise RuntimeError('Command failed (' + str(result.returncode) + '): ' + ' '.join(command[:3]))
        return result.stdout
    source = str(Path(args.source).resolve())
    def source_git(*parts):
        return run([git, '-C', source, *parts], source_read=True)
    oid = source_git('rev-parse', '--verify', '--end-of-options', args.revision + '^{commit}').decode().strip()
    config = artifact / 'config/nvim'; config.mkdir()
    inputs = {}
    lock_source = None
    for entry in source_git('ls-tree', '-r', '-z', oid, '--', 'dot_config/nvim').split(b'\0'):
        if not entry:
            continue
        meta, raw = entry.split(b'\t', 1)
        mode, kind, blob = meta.decode().split()
        path = raw.decode()
        if mode != '100644' or kind != 'blob' or not path.startswith(PREFIX):
            raise ValueError('Unsupported source entry: ' + path)
        relative = path[len(PREFIX):]
        if '.lazy.lua' in relative.split('/'):
            raise ValueError('Project .lazy.lua is unsupported: ' + path)
        if any(not re.fullmatch(r'[A-Za-z0-9_.-]+', p) or p in ('.', '..') for p in relative.split('/')):
            raise ValueError('Unsupported source path: ' + path)
        data = source_git('cat-file', 'blob', blob)
        if relative.endswith('.tmpl'):
            if b'{' * 2 in data:
                raise ValueError('Nonliteral template requires explicit support: ' + path)
            relative = relative[:-5]
        if not relative.endswith(('.lua', '.json')) or any(
                (p.startswith(ATTRIBUTES) or p.startswith('.')) for p in relative.split('/')):
            raise ValueError('Unsupported Neovim source: ' + path)
        dest = config / relative
        if dest.exists():
            raise ValueError('Source destination collision: ' + relative)
        dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
        inputs[path] = blob
        if relative == "lazy-lock.json":
            lock_source = path
    if not (config / 'init.lua').is_file():
        raise ValueError('Selected revision has no supported init.lua')
    # Project specs are not silently substituted by disabling upstream local_spec.
    if source_git('ls-tree', '-r', '--name-only', oid, '--', '.lazy.lua').strip():
        raise ValueError('Root .lazy.lua is unsupported; move its spec into the selected Neovim config')
    lock_path = config / 'lazy-lock.json'
    before = read_lock(lock_path)
    if before.get('lazy.nvim', {}).get('commit') != ENGINE or 'LazyVim' not in before:
        raise ValueError('Unsupported engine lock; requires lazy.nvim ' + ENGINE + ' and LazyVim')
    shutil.copyfile(lock_path, artifact / 'before.json')
    version = run([nvim, '--version']).decode().splitlines()[0]
    if not re.match(r'NVIM v0\.(?:1[2-9]|[2-9][0-9])\.', version):
        raise ValueError('Neovim >= 0.12 required; found ' + version)
    manifest = {'revision': oid, 'requested_revision': args.revision, 'inputs': inputs,
                'nvim': version, 'lock_source': lock_source, 'engine_retained': ENGINE, 'builds_runtime_submodules': 'not run',
                'phases': ['update', 'finish', 'verify']}
    (artifact / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    plugins = artifact / 'data/nvim/lazy'; plugins.mkdir(parents=True)
    for name, url in [('lazy.nvim', 'https://github.com/folke/lazy.nvim.git'),
                      ('LazyVim', 'https://github.com/LazyVim/LazyVim.git')]:
        dest = plugins / name
        run([git, 'clone', '--filter=blob:none', '--no-checkout', '--', url, str(dest)])
        run([git, '-C', str(dest), 'checkout', '--detach', before[name]['commit']])
    driver = artifact / 'driver.lua'
    driver.write_text(LUA_DRIVER)
    for phase in manifest['phases']:
        report = artifact / (phase + '.json')
        env.update(DOTFILES_LAZY_PHASE=phase, DOTFILES_LAZY_REPORT=str(report))
        saved_lock = lock_path.read_bytes()
        run([nvim, '--headless', '-u', 'NONE', '-i', 'NONE', '-n', '-l', str(driver)], timeout=900)
        data = json.loads(report.read_text())
        if data.get('phase') != phase or not data.get('active'):
            raise ValueError('Missing or invalid phase report: ' + phase)
        candidate = read_lock(lock_path)
        if candidate['lazy.nvim'] != before['lazy.nvim']:
            raise ValueError('Retained engine changed')
        if phase == 'verify' and lock_path.read_bytes() != saved_lock:
            raise ValueError('Verification unexpectedly changed the lock')
    shutil.copyfile(lock_path, artifact / 'candidate.json')
    old = (artifact / 'before.json').read_bytes().decode().splitlines(keepends=True)
    new = (artifact / 'candidate.json').read_bytes().decode().splitlines(keepends=True)
    patch = difflib.unified_diff(old, new, fromfile='a/' + lock_source, tofile='b/' + lock_source)
    (artifact / 'lazy-lock.patch').write_bytes(''.join(
        line if line.endswith('\n') else line + '\n\\ No newline at end of file\n'
        for line in patch).encode())
    return {'status': 'success', 'revision': oid, 'changed': old != new,
            'candidate_sha256': hashlib.sha256((artifact / 'candidate.json').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('--revision', default='HEAD', help='local commit/ref; excludes staged and dirty files')
    parser.add_argument('--nvim', default=os.environ.get('NVIM_BIN'))
    parser.add_argument('--git', default=os.environ.get('GIT_BIN'))
    args = parser.parse_args()
    artifact = Path(tempfile.mkdtemp(prefix='dotfiles-lazy-lock-')).resolve()
    (artifact / 'status.json').write_text('{"status": "incomplete"}\n')
    print('Retained artifact: ' + str(artifact), flush=True)
    print('Input: local ' + args.revision + '; lazy.nvim engine retained at ' + ENGINE, flush=True)
    try:
        status = generate(args, artifact)
    except (Exception, KeyboardInterrupt) as exc:
        status = {'status': 'failed', 'error': str(exc)}
    (artifact / 'status.json').write_text(json.dumps(status, indent=2) + '\n')
    print(status['status'] + ': ' + str(artifact), flush=True)
    if status['status'] != 'success':
        print(status['error'], file=sys.stderr)
        return 1
    print('Review before.json, candidate.json and lazy-lock.patch; adoption/publication are separate.')
    return 0


if __name__ == '__main__':
    if 'LUA_DRIVER' not in globals():
        LUA_DRIVER = Path(__file__).with_suffix('.lua').read_text()
    sys.exit(main())

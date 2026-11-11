"""Private completion receipts; no subprocesses, publication or cache mutation."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


# Only shared within this locked invocation, in a fresh private temporary dir.
# No persistent mtime shortcut: every new apply reads each dependency inode once.
cache_path = Path(os.environ['COMPLETION_DIGEST_CACHE'])
cache = json.loads(cache_path.read_text()) if cache_path.exists() else {'files': {}, 'trees': {}}


def digest_file(path, reuse=False):
    info = path.stat()
    key = str((info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns))
    if reuse and key in cache['files']:
        return cache['files'][key]
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    result = h.hexdigest()
    if reuse:
        cache['files'][key] = result
    return result


def dependency(path, ancestors=()):
    path = Path(path)
    real = path.resolve(strict=True)
    if real in ancestors:
        raise ValueError('cyclic dependency: ' + str(path))
    if real.is_dir():
        if str(real) not in cache['trees']:
            cache['trees'][str(real)] = [
                [p.name, dependency(p, (*ancestors, real))]
                for p in sorted(real.iterdir())]
        return [str(path), str(real), cache['trees'][str(real)]]
    if not real.is_file():
        raise ValueError('non-regular dependency: ' + str(path))
    return [str(path), str(real), stat.S_IMODE(real.stat().st_mode), digest_file(real, reuse=True)]


try:
    mode, target, receipt, script, *deps = sys.argv[1:]
    target, receipt = Path(target), Path(receipt)
    previous = None
    if receipt.is_symlink() or (receipt.exists() and not receipt.is_file()):
        raise ValueError('redirected completion receipt: ' + str(receipt))
    if receipt.exists():
        previous = json.loads(receipt.read_text())
        if (not isinstance(previous, dict) or set(previous) != {'kind', 'input', 'output'}
                or previous['kind'] != 'dotfiles-completion-v1'
                or any(not isinstance(previous[k], str) or len(previous[k]) != 64
                       or any(c not in '0123456789abcdef' for c in previous[k])
                       for k in ('input', 'output'))):
            raise ValueError('unrecognized completion receipt: ' + str(receipt))
    # The complete rendered generator includes the definition, paths, shared
    # template results and this checker. Zsh changes can change compilation.
    inputs = [dependency(Path(script)), dependency(Path('/bin/zsh'))]
    inputs.extend(dependency(Path(p)) for p in deps)
    fingerprint = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    if mode == 'check':
        current = (previous is not None and previous['input'] == fingerprint
                   and not target.is_symlink() and target.is_file()
                   and target.stat().st_size > 0
                   and stat.S_IMODE(target.stat().st_mode) == 0o644
                   and previous['output'] == digest_file(target)
                   and not os.path.lexists(str(target) + '.zwc'))
        print('current' if current else 'generate')
    elif mode == 'record':
        print(json.dumps({'kind': 'dotfiles-completion-v1',
                          'input': fingerprint, 'output': digest_file(target)}, sort_keys=True))
    else:
        raise ValueError('unknown completion receipt operation')
    cache_path.write_text(json.dumps(cache, sort_keys=True))
except (OSError, ValueError, RuntimeError) as exc:
    print('[Error] Completion dependency/receipt check failed: ' + str(exc), file=sys.stderr)
    sys.exit(1)

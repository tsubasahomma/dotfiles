"""Small shared I/O primitives for bat, Vale and pbfile (not a task scheduler)."""

import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile


def digest(value):
    return hashlib.sha256(value).hexdigest()


def file_hash(path):
    with Path(path).open('rb') as stream:
        value = hashlib.sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
        return value.hexdigest()


def fingerprint(value):
    return digest(json.dumps(value, sort_keys=True).encode())


def run(args, *, env=None, data=None):
    result = subprocess.run(
        [str(a) for a in args], input=data, text=True, capture_output=True, env=env, check=True
    )
    return result.stdout.strip()


def regular(path):
    return path.is_file() and not path.is_symlink()


def directories(root, parent):
    # The configured root may itself be relocated. Descendants may not redirect.
    relative = parent.relative_to(root)
    if root.exists() and not root.is_dir():
        raise RuntimeError(f'Not a directory: {root}')
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise RuntimeError(f'Redirected output directory: {path}')
    parent.mkdir(parents=True, exist_ok=True)


def record(path):
    if not regular(path):
        raise RuntimeError(f'Expected regular output: {path}')
    return {'sha256': file_hash(path), 'mode': stat.S_IMODE(path.stat().st_mode)}


def input_tree(root):
    """Only a generator's actual input subtree, never HOME or tool install trees."""
    if not root.exists():
        return {}
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError(f'Unsupported input directory: {root}')
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or (not path.is_file() and not path.is_dir()):
            raise RuntimeError(f'Unsupported input entry: {path}')
        if path.is_file():
            result[str(path.relative_to(root))] = file_hash(path)
    return result


def selected_tool(mise, name):
    env = dict(
        os.environ,
        MISE_AUTO_INSTALL='false',
        MISE_EXEC_AUTO_INSTALL='false',
        MISE_TASK_RUN_AUTO_INSTALL='false',
        MISE_OFFLINE='true',
    )
    tool = Path(run([mise, 'which', '--tool', name, name], env=env))
    if not tool.is_absolute() or not tool.is_file() or not os.access(tool, os.X_OK):
        raise RuntimeError(f'Missing installed {name}: {tool}')
    return tool


@contextlib.contextmanager
def locked(state, name):
    root = state / 'dotfiles-generators'
    directories(state, root)
    path = root / (name + '.lock')
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise RuntimeError(f'Nonregular lock: {path}')
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield root / (name + '.json')
    finally:
        os.close(fd)


def load_receipt(path, name, allowed):
    if not path.exists() and not path.is_symlink():
        return None
    if not regular(path):
        raise RuntimeError(f'Invalid receipt: {path}')
    value = json.loads(path.read_text())
    if (
        set(value) != {'owner', 'input', 'files'}
        or value['owner'] != name + '-v1'
        or not isinstance(value['input'], str)
        or not isinstance(value['files'], dict)
        or not value['files']
    ):
        raise RuntimeError(f'Unrecognized receipt: {path}')
    for key, item in value['files'].items():
        if (
            not isinstance(key, str)
            or not allowed(key)
            or not isinstance(item, dict)
            or set(item) != {'sha256', 'mode'}
            or not isinstance(item['sha256'], str)
            or len(item['sha256']) != 64
            or item['mode'] not in (0o644, 0o755)
        ):
            raise RuntimeError(f'Invalid receipt entry: {key}')
    return value


def inspect_outputs(root, previous):
    complete = previous is not None
    for name, expected in (previous or {}).get('files', {}).items():
        path = root / name
        directories(root, path.parent)
        if not path.exists() and not path.is_symlink():
            complete = False
        elif record(path) != expected:
            raise RuntimeError(f'Output changed outside generator; preserve and reconcile: {path}')
    return complete


def current(root, previous, inputs):
    return inspect_outputs(root, previous) and previous['input'] == inputs


def publish(root, stage, names, receipt, owner, inputs, previous):
    """Stage/validate before this call; rollback caught errors, not crash atomicity."""
    files = {name: record(stage / name) for name in names}
    old_files = (previous or {}).get('files', {})
    inspect_outputs(root, previous)
    for name in files:
        path = root / name
        directories(root, path.parent)
        if name not in old_files and (path.exists() or path.is_symlink()):
            raise RuntimeError(f'Unowned output; preserve and reconcile: {path}')
    value = {'owner': owner + '-v1', 'input': inputs, 'files': files}
    receipt_text = json.dumps(value, sort_keys=True, indent=2) + '\n'
    # Backups stay on the destination filesystem. No old files are removed
    # until every candidate and ownership check has succeeded.
    backup = Path(tempfile.mkdtemp(prefix='.publish-', dir=root))
    keep_backup = False
    try:
        changed = []
        old_receipt = receipt.read_bytes() if receipt.exists() else None
        if old_receipt is not None:
            (backup / 'receipt.previous.json').write_bytes(old_receipt)
        try:
            for name in sorted(set(files) | set(old_files)):
                path = root / name
                if name in files and regular(path) and record(path) == files[name]:
                    continue
                saved = backup / 'old' / name
                saved.parent.mkdir(parents=True, exist_ok=True)
                existed = path.exists()
                if existed:
                    shutil.copy2(path, saved)
                changed.append((path, saved, existed))
                if name in files:
                    os.replace(stage / name, path)
                elif existed:
                    path.unlink()
            if old_receipt != receipt_text.encode():
                # Receipt may reside on another filesystem; copy to its parent.
                with tempfile.NamedTemporaryFile(dir=receipt.parent, delete=False) as stream:
                    receipt_stage = Path(stream.name)
                    stream.write(receipt_text.encode())
                try:
                    receipt_stage.chmod(0o644)
                    os.replace(receipt_stage, receipt)
                except BaseException:
                    receipt_stage.unlink(missing_ok=True)
                    raise
        except BaseException:
            # The receipt rename is the commit point. Reading it also covers a
            # SIGINT between os.replace returning and a Python flag assignment.
            # With an identical old receipt, partial missing-file repair is
            # already consistent: restored files match it; the rest stay missing.
            try:
                if receipt.is_symlink():
                    raise RuntimeError('Receipt redirected during publish')
                committed = receipt.read_bytes() == receipt_text.encode()
            except FileNotFoundError:
                committed = False
            except BaseException as observation_error:
                keep_backup = True
                raise RuntimeError(
                    f'Cannot determine receipt commit; preserve/reconcile backup at {backup}'
                ) from observation_error
            if committed:
                raise
            try:
                for path, saved, existed in reversed(changed):
                    if existed:
                        os.replace(saved, path)
                    else:
                        path.unlink(missing_ok=True)
            except BaseException as recovery_error:
                keep_backup = True
                raise RuntimeError(
                    f'Publish rollback failed; preserve/reconcile backup at {backup}'
                ) from recovery_error
            raise
    finally:
        if not keep_backup:
            shutil.rmtree(backup)

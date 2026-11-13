"""Synchronize only the two declared Windows settings; no tool provisioning.

Each target has an adjacent receipt and exclusive directory lock shared by WSL
writers. File/receipt publication is not a crash-atomic transaction. Windows
editors do not participate in this lock; do not edit during synchronization.
"""
import base64
import contextlib
import hashlib
import json
import ntpath
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

SETTINGS = {
    'wezterm': ('USERPROFILE', ('.wezterm.lua',)),
    '1password-agent': ('LOCALAPPDATA', ('1Password', 'config', 'ssh', 'agent.toml')),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def windows_root(kind):
    variable, parts = SETTINGS[kind]
    # All interpolated values are constants selected above, never path/content.
    script = r'''
$ErrorActionPreference = 'Stop'
try {
    $root = [Environment]::GetEnvironmentVariable('__VARIABLE__', 'Process')
    if ([string]::IsNullOrWhiteSpace($root)) { throw 'Missing Windows setting root' }
    if ($root -notmatch '^[A-Za-z]:\\') { throw 'Only drive-absolute roots are supported' }
    $root = [IO.Path]::GetFullPath($root)
    $target = Join-Path $root '__SUFFIX__'
    # Reject reparse points throughout the root and the fixed managed suffix.
    foreach ($leaf in @($target, "$target.dotfiles-sync.json", "$target.dotfiles-sync.lock")) {
        $p = $leaf
        while ($p) {
            $item = $null
            try { $item = Get-Item -LiteralPath $p -Force -ErrorAction Stop }
            catch [System.Management.Automation.ItemNotFoundException] { }
            if ($null -ne $item) {
                if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                    throw 'Reparse point in Windows sync path'
                }
            }
            $parent = [IO.Path]::GetDirectoryName($p)
            if ($parent -eq $p) { break }
            $p = $parent
        }
    }
    if (-not (Test-Path -LiteralPath $root -PathType Container)) { throw 'Missing Windows root' }
    $json = @{ root = $root } | ConvertTo-Json -Compress
    [Console]::Write([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json)))
    exit 0
} catch {
    [Console]::Error.WriteLine('Windows sync path query failed: ' + $_.Exception.Message)
    exit 1
}
'''.replace('__VARIABLE__', variable).replace('__SUFFIX__', '\\'.join(parts))
    encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
    result = subprocess.run(['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive',
                             '-EncodedCommand', encoded], capture_output=True, check=False)
    if result.returncode or result.stderr.strip():
        raise RuntimeError('Windows path query failed; check interop, environment and reparse points')
    try:
        obj = json.loads(base64.b64decode(result.stdout.strip(), validate=True).decode('utf-8'))
        if not isinstance(obj, dict) or set(obj) != {'root'}:
            raise ValueError('schema')
        root = obj['root']
        if not isinstance(root, str) or not re.fullmatch(r'[A-Za-z]:\\[^\x00-\x1f]*', root):
            raise ValueError('root')
        # No UNC/device paths, ADS, traversal or ambiguous Windows components.
        tail = root[3:]
        if any(c in tail for c in '<>:"|?*/') or any(
                part in ('.', '..') or part.endswith((' ', '.'))
                for part in tail.split('\\') if part):
            raise ValueError('unsupported root')
        return ntpath.normpath(root)
    except (ValueError, UnicodeError, TypeError) as exc:
        raise RuntimeError('Invalid Windows path response') from exc


def converted_root(winroot):
    result = subprocess.run(['wslpath', '-u', winroot], capture_output=True, check=False)
    if result.returncode or result.stderr.strip():
        raise RuntimeError('Windows path conversion failed')
    try:
        value = result.stdout.decode('utf-8').rstrip('\r\n')
    except UnicodeError as exc:
        raise RuntimeError('Invalid Windows path conversion') from exc
    if not value.startswith('/') or any(ord(c) < 32 for c in value) or '..' in Path(value).parts:
        raise RuntimeError('Expected an absolute WSL path')
    root = Path(value)
    directories(root, create=False)
    return root


def directories(path, *, create):
    """Check every POSIX ancestor; never follow a redirected managed path."""
    if not path.is_absolute():
        raise RuntimeError('Expected absolute path')
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if not create:
                raise RuntimeError(f'Missing directory: {current}') from None
            current.mkdir()
            info = current.lstat()
        if not stat.S_ISDIR(info.st_mode):
            raise RuntimeError(f'Non-directory or redirected path: {current}')


def read_file(path, *, missing=True):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        if missing:
            return None
        raise RuntimeError(f'Required source is missing: {path}') from None
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise RuntimeError(f'Expected a regular file with one hard link: {path}')
        data = stream.read()
        after = os.fstat(stream.fileno())

        def key(s):
            return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_mode)

        if key(info) != key(after):
            raise RuntimeError(f'File changed while reading: {path}')
        return data, key(info), stat.S_IMODE(info.st_mode)


def unchanged(path, before):
    if read_file(path) != before:
        raise RuntimeError(f'Concurrent change: {path}')


@contextlib.contextmanager
def locked(target):
    path = target.with_name(target.name + '.dotfiles-sync.lock')
    try:
        path.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise RuntimeError(f'Sync lock exists; another writer or interrupted sync: {path}') from exc
    info = path.lstat()
    try:
        yield
    finally:
        current = path.lstat()
        if (current.st_dev, current.st_ino) != (info.st_dev, info.st_ino) or not stat.S_ISDIR(current.st_mode):
            raise RuntimeError('Sync lock changed; retained for inspection')
        path.rmdir()  # Only our empty lock, never recursive cleanup.


def staged(path, data, mode):
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.stage-', dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), mode)
        if read_file(temp, missing=False)[0] != data:
            raise RuntimeError('Staged copy validation failed')
        return temp
    except BaseException:
        temp.unlink()
        raise


def publish(target, receipt, expected, metadata, before, old_receipt, recheck):
    temporary = []
    keep_backup = False
    changed = before is None or before[0] != expected
    backup = None
    try:
        output = staged(target, expected, before[2] if before else 0o600) if changed else None
        if output: temporary.append(output)
        new_receipt = staged(receipt, metadata, 0o600)
        temporary.append(new_receipt)
        if changed and before is not None:
            backup = staged(target, before[0], before[2]); temporary.append(backup)
        recheck()
        unchanged(target, before)
        unchanged(receipt, old_receipt)
        published_inode = output.stat().st_ino if output else None
        if output:
            os.replace(output, target)
        try:
            current = read_file(target, missing=False)
            if current[0] != expected or (output and current[1][1] != published_inode):
                raise RuntimeError('Target changed after publication')
            unchanged(receipt, old_receipt)
            os.replace(new_receipt, receipt)
        except (OSError, RuntimeError) as exc:
            if changed:
                try:
                    recheck()
                    current = read_file(target, missing=False)
                    if current[0] != expected or current[1][1] != published_inode:
                        raise RuntimeError('Published target changed; refusing rollback')
                    unchanged(receipt, old_receipt)
                    if backup:
                        os.replace(backup, target)
                    else:
                        target.unlink()
                except Exception as rollback:
                    keep_backup = True
                    raise RuntimeError(f'Receipt failed and rollback failed; retained backup {backup}') from rollback
            raise RuntimeError('Receipt publication failed; previous target restored') from exc
    finally:
        for path in temporary:
            if path == backup and keep_backup:
                continue
            path.unlink(missing_ok=True)


def sync(kind, source):
    if kind not in SETTINGS:
        raise RuntimeError('Unknown Windows setting')
    directories(source.parent, create=False)
    original_source = read_file(source, missing=False)
    expected = original_source[0]
    winroot = windows_root(kind)
    root = converted_root(winroot)
    parts = SETTINGS[kind][1]
    target = root.joinpath(*parts)
    destination = ntpath.normcase(ntpath.join(winroot, *parts))
    directories(target.parent, create=True)
    receipt = target.with_name(target.name + '.dotfiles-sync.json')

    def recheck():
        unchanged(source, original_source)
        if ntpath.normcase(windows_root(kind)) != ntpath.normcase(winroot):
            raise RuntimeError('Windows root changed during sync')
        if converted_root(winroot) != root:
            raise RuntimeError('WSL path mapping changed during sync')
        directories(target.parent, create=False)

    with locked(target):
        recheck()
        before, old_receipt = read_file(target), read_file(receipt)
        if old_receipt is not None:
            try:
                record = json.loads(old_receipt[0])
                if (not isinstance(record, dict) or set(record) != {'version', 'kind', 'destination', 'sha256'}
                        or type(record['version']) is not int or record['version'] != 1
                        or record['kind'] != kind or record['destination'] != destination
                        or not isinstance(record['sha256'], str)
                        or not re.fullmatch('[0-9a-f]{64}', record['sha256'])):
                    raise ValueError('receipt schema or destination')
            except (ValueError, UnicodeError) as exc:
                raise RuntimeError('Invalid or redirected Windows sync receipt; retained') from exc
            if before is not None and digest(before[0]) != record['sha256']:
                raise RuntimeError('Windows setting was edited since last sync; retained')
        elif before is not None and before[0] != expected:
            raise RuntimeError('Existing unowned Windows setting differs; retained')
        metadata = (json.dumps({'version': 1, 'kind': kind, 'destination': destination,
                                'sha256': digest(expected)}, sort_keys=True) + '\n').encode()
        if before is not None and before[0] == expected and old_receipt and old_receipt[0] == metadata:
            print(f'[UNCHANGED] Windows {kind} setting')
            return
        # Recreating a missing target with unchanged input need not rewrite receipt.
        if before is None and old_receipt and old_receipt[0] == metadata:
            temp = staged(target, expected, 0o600)
            try:
                recheck(); unchanged(target, before); unchanged(receipt, old_receipt)
                os.replace(temp, target)
            finally:
                temp.unlink(missing_ok=True)
        else:
            publish(target, receipt, expected, metadata, before, old_receipt, recheck)
        status = ('RESTORED' if old_receipt else 'CREATED') if before is None else ('ADOPTED' if old_receipt is None and before[0] == expected else 'UPDATED')
        print(f'[{status}] Windows {kind} setting file (application use not verified)')


def main():
    try:
        sync(sys.argv[1], Path(sys.argv[2]))
    except (OSError, RuntimeError, ValueError) as exc:
        print(f'[FAIL] Windows config sync: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

# Embedded in both the before script and the generator. Python 3.9+; no auth.
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import tempfile


class Refusal(Exception):
    pass


def require(ok, message):
    if not ok:
        raise Refusal(message)


def run(*args, input=None):
    result = subprocess.run(args, input=input, text=True, capture_output=True)
    require(result.returncode == 0, 'format/path command failed (details redacted)')
    return result.stdout


def quote(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\b', '\\b') + '"'


def shell_quote(value):
    return "'" + value.replace("'", "'\"'\"'") + "'"


def write(path, content, mode=0o600):
    # New generation paths only; exclusive creation, never follow a symlink.
    with path.open('x') as stream:
        stream.write(content)
    path.chmod(mode)


def pairs(path):
    output = run('git', 'config', '--no-includes', '--null', '--file', str(path), '--list')
    return [record.split('\n', 1) for record in output.split('\0') if record]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pointer(generation):
    return '# dotfiles identity entry v1\n[include]\n    path = ' + quote(str(generation / 'dispatch')) + '\n'


def active(entry, allow_missing=False):
    require(entry.is_file() and not entry.is_symlink(), 'unknown or missing identity entry; preserve and inspect it')
    require(stat.S_IMODE(entry.stat().st_mode) == 0o600, 'modified identity entry mode')
    records = pairs(entry)
    require(len(records) == 1 and records[0][0] == 'include.path', 'unknown identity entry')
    generation = Path(records[0][1]).parent
    require(generation.parent == entry.parent and re.fullmatch(r'\.identity-generation-[A-Za-z0-9_]+', generation.name), 'unknown identity generation path')
    require(generation.is_dir() and not generation.is_symlink(), 'unknown identity generation')
    require(entry.read_text() == pointer(generation), 'modified identity entry')
    manifest = generation / 'manifest.json'
    require(manifest.is_file() and not manifest.is_symlink(), 'missing identity manifest')
    saved = json.loads(manifest.read_text())
    require(isinstance(saved, dict), 'unknown identity manifest')
    require(saved.get('version') in (1, 2) and isinstance(saved.get('files'), dict), 'unknown identity manifest')
    require(saved.get('kind') in ('legacy', 'empty', 'generated', 'cleared'), 'unknown identity generation kind')
    if saved['version'] == 2:
        require(stat.S_IMODE(manifest.stat().st_mode) == 0o600, 'modified identity manifest mode')
        require(isinstance(saved.get('contents'), dict) and isinstance(saved.get('modes'), dict), 'invalid recovery manifest')
    require(set(p.name for p in generation.iterdir()) <= set(saved['files']) | {'manifest.json'},
            'unknown file in identity generation; preserve and inspect it')
    for name, expected in saved['files'].items():
        require(re.fullmatch(r'[A-Za-z0-9_.@+\x27$`{}!#&=^~-]+', name) is not None and name not in ('.', '..'), 'unknown manifest path')
        path = generation / name
        require(isinstance(expected, str) and re.fullmatch(r'[0-9a-f]{64}', expected), 'invalid identity digest')
        if allow_missing and not os.path.lexists(path):
            continue
        require(path.is_file() and not path.is_symlink() and digest(path) == expected, 'modified or missing identity generation file')
        if saved['version'] == 2:
            require(stat.S_IMODE(path.stat().st_mode) == saved['modes'][name], 'modified identity generation mode')
    require('dispatch' in saved['files'] and 'entry' in saved['files'], 'incomplete identity manifest')
    require(saved['files']['entry'] == hashlib.sha256(entry.read_bytes()).hexdigest(), 'modified identity entry')
    if saved['version'] == 2:
        require(set(saved['contents']) == set(saved['files']) == set(saved['modes']), 'incomplete recovery manifest')
        for name, content in saved['contents'].items():
            require(isinstance(content, str) and hashlib.sha256(content.encode()).hexdigest() == saved['files'][name], 'invalid recovery content')
            require(saved['modes'][name] == (0o644 if name == 'allowed_signers' else 0o600), 'invalid recovery mode')
    return generation, saved


def seal(generation, kind, legacy_config_sha256=None, inputs=None):
    write(generation / 'entry', pointer(generation))
    files = {p.name: digest(p) for p in generation.iterdir()}
    contents = {name: (generation / name).read_text() for name in files}
    modes = {name: stat.S_IMODE((generation / name).stat().st_mode) for name in files}
    write(generation / 'manifest.json', json.dumps({'version': 2, 'kind': kind, 'files': files,
          'contents': contents, 'modes': modes, 'inputs': inputs,
          'legacy_config_sha256': legacy_config_sha256}, sort_keys=True) + '\n')


def install(entry, generation, previous):
    # No cleanup of generations: a Git reader may still hold the old config.
    # Verify the expected entry again under our writer lock before the one switch.
    if previous is None:
        require(not os.path.lexists(entry), 'identity entry appeared during generation')
        os.link(generation / 'entry', entry)  # exclusive initial publication
    else:
        require(entry.read_bytes() == previous and not entry.is_symlink(), 'identity entry changed during generation')
        # Keep the sealed entry for ownership comparison. Rename another hardlink.
        candidate = generation / 'switch'
        os.link(generation / 'entry', candidate)
        os.replace(candidate, entry)


def new_generation(parent):
    return Path(tempfile.mkdtemp(prefix='.identity-generation-', dir=parent))


def consumer_ready(parent, entry):
    config = parent / 'config'
    if not config.is_file() or config.is_symlink():
        return False
    records = pairs(config)
    includes = [(key.lower(), value) for key, value in records if key.lower().startswith('include')]
    overrides = {'user.name', 'user.email', 'user.signingkey', 'core.sshcommand', 'gpg.ssh.allowedsignersfile'}
    return includes == [('include.path', str(entry))] and not any(key.lower() in overrides for key, value in records)


def prepare(parent, entry, data):
    old = parent / 'config'
    if os.path.lexists(entry):
        generation, saved = active(entry, allow_missing=True)
        if os.path.lexists(old) and not consumer_ready(parent, entry):
            require(old.is_file() and not old.is_symlink() and
                    saved.get('legacy_config_sha256') == digest(old),
                    'Git consumer changed since migration preparation; preserve and inspect it')
        recover(data, generation, saved, entry)
        return generation, saved
    require(not consumer_ready(parent, entry),
            'missing identity entry: selected generation is unknown; restore the inspected entry explicitly')
    records = []
    if os.path.lexists(old):
        require(old.is_file() and not old.is_symlink(), 'legacy Git config is not a regular file')
        records = pairs(old)
    lines = []
    for key, value in records:
        lower = key.lower()
        if lower.startswith('include'):
            # Legacy repo routing uses absolute gitdir/i conditions. Other shapes
            # need an explicit migration, not guessed interpretation or deletion.
            require(lower.startswith('includeif.gitdir/i:/') and lower.endswith('.path'), 'unsupported legacy include; migrate explicitly before apply')
            path = Path(os.path.expanduser(value))
            require(path.is_absolute() and path.is_file(), 'legacy identity include is missing or relative')
            run('git', 'config', '--file', str(path), '--list')
            condition = key[len('includeif.'):-len('.path')]
            lines.append('[includeIf ' + quote(condition) + ']\n    path = ' + quote(str(path)) + '\n')
        elif lower == 'gpg.ssh.allowedsignersfile':
            path = Path(os.path.expanduser(value))
            require(path.is_absolute() and path.is_file(), 'legacy allowed signers is missing or relative')
            lines.append('[gpg "ssh"]\n    allowedSignersFile = ' + quote(str(path)) + '\n')
        elif lower in ('user.name', 'user.email', 'user.signingkey', 'core.sshcommand'):
            raise Refusal('legacy global identity needs explicit migration before apply')
    generation = new_generation(parent)
    write(generation / 'dispatch', ''.join(lines))
    run('git', 'config', '--file', str(generation / 'dispatch'), '--list')
    seal(generation, 'legacy' if lines else 'empty', digest(old) if old.exists() else None)
    install(entry, generation, None)
    return active(entry)


def windows_directory(data, generation):
    if not data['is_wsl'] or not data['identities']:
        return None
    value = run('wslpath', '-w', str(generation)).rstrip('\n')
    require(value and not re.search(r'[\x00-\x1f\x7f%]|\$\{', value), 'unsupported converted OpenSSH path')
    return value


def input_digest(data, generation, win_dir):
    # Normalize only the generated basename; retain the actual Windows mapping
    # (including distro), not a stale init-time environment value.
    mapping = win_dir
    if mapping and mapping.endswith('\\' + generation.name):
        mapping = mapping[:-len(generation.name)]
    value = {'payload': data, 'windows_mapping': mapping, 'git': run('git', '--version').strip()}
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def build(data, generation, reference, win_dir):
    ids = data['identities']
    dispatch = '[gpg "ssh"]\n    allowedSignersFile = ' + quote(str(reference / 'allowed_signers')) + '\n'
    signers = []
    for identity in ids:
        filename = 'id_{key_type}_{email}_{key_hash}.pub'.format(**identity)
        pubkey = generation / filename
        write(pubkey, identity['public_key'] + '\n')
        run('ssh-keygen', '-lf', str(pubkey))
        config = generation / ('config_{email}_{key_hash}'.format(**identity))
        keypath = win_dir + '\\' + filename if win_dir else str(reference / filename)
        command = ('ssh.exe' if data['is_wsl'] else 'ssh') + ' -i ' + shell_quote(keypath) + ' ' + data['ssh_options']
        write(config, identity['config'])
        run('git', 'config', '--file', str(config), 'core.sshCommand', command)
        run('git', 'config', '--file', str(config), '--list')
        for route in identity['routes']:
            dispatch += '[includeIf ' + quote('gitdir/i:' + route + '/**') + ']\n    path = ' + quote(str(reference / config.name)) + '\n'
        signers.append(identity['email'] + ' namespaces="git" ' + identity['public_key'] + '\n')
    write(generation / 'allowed_signers', ''.join(sorted(set(signers))), 0o644)
    for identity in ids:
        matched = run('ssh-keygen', '-Y', 'match-principals', '-I', identity['email'], '-f', str(generation / 'allowed_signers'))
        require(matched.rstrip('\n') == identity['email'], 'allowed signers validation failed')
    write(generation / 'dispatch', dispatch)
    run('git', 'config', '--file', str(generation / 'dispatch'), '--list')


def recover(data, generation, saved, entry):
    missing = [name for name in saved['files'] if not os.path.lexists(generation / name)]
    if not missing:
        return
    # Stage/validate all bytes before restoring any path. Restored files have the
    # old bytes at the old paths, so readers holding the old dispatch remain valid.
    with tempfile.TemporaryDirectory(prefix='.identity-recovery-', dir=generation.parent) as temporary:
        staging = Path(temporary)
        if saved['version'] == 2:
            for name in missing:
                write(staging / name, saved['contents'][name], saved['modes'][name])
        else:
            # R05 has only digests. Re-render at the OLD absolute paths and accept
            # only an exact match to every old hash, never guess from new input.
            require(saved['kind'] in ('generated', 'cleared'), 'legacy missing output has no recovery content')
            build(data, staging, generation, windows_directory(data, generation))
            write(staging / 'entry', pointer(generation))
            require(set(p.name for p in staging.iterdir()) == set(saved['files']), 'R05 recovery input differs')
            require(all(digest(staging / name) == expected for name, expected in saved['files'].items()), 'R05 recovery input differs')
        active(entry, allow_missing=True)
        for name in missing:
            # Exclusive link: a raced manual file/symlink is never overwritten.
            os.link(staging / name, generation / name)
    active(entry)


def generate(data, parent, entry, clear):
    ids = data['identities']
    require(not clear or not ids, '--clear requires an explicitly empty identities array')
    require(consumer_ready(parent, entry), 'Git consumer is not migrated; run apply with the identity before script first')
    generation_old, saved = prepare(parent, entry, data)
    previous = entry.read_bytes()
    if not ids and not clear:
        if saved['kind'] == 'cleared':
            print('identity: explicitly cleared generation retained')
            return
        require(os.environ.get('CI') == 'true' and saved['kind'] == 'empty',
                'empty identities refused; use --clear only for intentional removal')
        print('identity: empty CI installation; no identity or fallback key generated')
        return
    win_dir = windows_directory(data, generation_old)
    expected = input_digest(data, generation_old, win_dir)
    if saved.get('inputs') == expected:
        print('identity: validated generation unchanged')
        return
    generation = new_generation(parent)
    win_dir = windows_directory(data, generation)
    build(data, generation, generation, win_dir)
    seal(generation, 'generated' if ids else 'cleared', inputs=input_digest(data, generation, win_dir))
    # Detect edits to the active generation as well as the dispatcher before commit.
    active(entry)
    install(entry, generation, previous)
    print('identity: validated generation selected')


def main():
    require(sys.version_info >= (3, 9), "Python 3.9+ must be on PATH before apply/generate")
    data = json.loads(sys.argv[1])
    action = sys.argv[2]
    require(action in ('prepare', 'generate'), 'unknown operation')
    require(sys.argv[3:] in ([], ['--clear']) and (action == 'generate' or len(sys.argv) == 3), 'unsupported arguments')
    parent = Path(data['git_dir'])
    # These are declared directory parents, but do not follow redirected ones.
    for path in (parent.parent, parent):
        require(not path.is_symlink(), 'Git parent is a symlink; inspect ownership first')
    parent.mkdir(parents=True, exist_ok=True)
    entry = parent / 'identity.inc'
    # Directory lock requires no overwrite or ownership assumption about an
    # existing lock. SIGKILL leaves it in place; inspect before removing it.
    lock = parent / '.identity-writer-lock'
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError:
        raise Refusal('identity writer lock exists; inspect active/interrupted writer')
    try:
        if action == 'prepare':
            prepare(parent, entry, data)
        else:
            generate(data, parent, entry, sys.argv[3:] == ['--clear'])
    finally:
        lock.rmdir()


def interrupted(signum, frame):
    raise Refusal('interrupted before completion; inspect selected generation')


for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(sig, interrupted)
try:
    main()
except (Refusal, OSError, ValueError, KeyError, TypeError) as error:
    # No identity data or command output in shared diagnostics.
    print('identity: ' + (str(error) if isinstance(error, Refusal) else 'I/O or state validation failed (details redacted)'), file=sys.stderr)
    sys.exit(1)

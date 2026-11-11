import re

mise, config, cache, state, script = map(Path, sys.argv[1:])
root = cache / 'bat'
names = ('syntaxes.bin', 'themes.bin', 'metadata.yaml')
source = config / 'bat'
required = source / 'themes/Catppuccin Mocha.tmTheme'


def inputs():
    if not regular(required):
        raise RuntimeError(f'Missing required theme: {required}')
    return fingerprint({'script': file_hash(script), 'binary': file_hash(tool),
                        'path': str(tool.resolve()), 'version': run([tool, '--version']),
                        'themes': input_tree(source / 'themes'),
                        'syntaxes': input_tree(source / 'syntaxes')})


def validate(stage):
    for name in names:
        record(stage / name)
        if (stage / name).stat().st_size == 0:
            raise RuntimeError(f'Empty bat output: {name}')
    # bat can fall back to built-ins after cache-load warnings: warnings fail.
    env = {k: v for k, v in os.environ.items() if not k.startswith('BAT_')}
    env.update(BAT_CACHE_PATH=str(stage), BAT_CONFIG_PATH=os.devnull)
    for args in (['--list-themes'], ['--list-languages'],
                 ['--color=always', '--paging=never', '--style=plain',
                  '--theme=Catppuccin Mocha', '--language=Swift']):
        result = subprocess.run([str(tool), *args], env=env, input='let x = 1\n',
                                text=True, capture_output=True, check=True)
        if result.stderr.strip() or not result.stdout.strip():
            raise RuntimeError('bat rejected staged cache: ' + result.stderr)
        if args == ['--list-themes'] and 'Catppuccin Mocha' not in result.stdout:
            raise RuntimeError('Required bat theme was not loaded')
    version = run([tool, '--version']).split()[1]
    if not re.search(r'^bat_version: [\'\"]?' + re.escape(version) + r'[\'\"]?$',
                     (stage / 'metadata.yaml').read_text(), re.M):
        raise RuntimeError('Unexpected bat cache metadata format/version')


with locked(state, 'bat') as receipt:
    directories(cache, root)
    tool = selected_tool(mise, 'bat')
    previous = load_receipt(receipt, 'bat', lambda name: name in names)
    if previous and set(previous['files']) != set(names):
        raise RuntimeError('Incomplete bat receipt')
    key = inputs()
    if not current(root, previous, key):
        with tempfile.TemporaryDirectory(prefix='.bat-stage-', dir=root) as temporary:
            stage = Path(temporary)
            env = {k: v for k, v in os.environ.items() if not k.startswith('BAT_')}
            env['BAT_CONFIG_PATH'] = os.devnull
            built = subprocess.run([str(tool), 'cache', '--build', '--source', str(source),
                                    '--target', str(stage)], env=env, text=True,
                                   capture_output=True, check=True)
            # bat 0.26 reports theme parse failures on stdout and still exits 0;
            # the built-in Catppuccin theme can then mask a broken custom theme.
            if (built.stderr.strip() or 'Failed to load one or more themes' in built.stdout
                    or 'Some referenced contexts could not be found!' in built.stdout):
                raise RuntimeError('bat did not load all custom assets: ' + built.stdout + built.stderr)
            validate(stage)
            for name in names:
                (stage / name).chmod(0o644)
            if key != inputs():
                raise RuntimeError('bat dependencies changed during generation')
            publish(root, stage, names, receipt, 'bat', key, previous)

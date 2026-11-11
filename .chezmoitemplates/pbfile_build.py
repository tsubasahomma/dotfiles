import platform

home, data, state, script = map(Path, sys.argv[1:])
root = home / '.local/bin'
source = data / 'pbcopy/pbfile.swift'


def compiler_inputs():
    if not regular(source):
        raise RuntimeError(f'Missing pbfile Swift source: {source}')
    compiler = Path(run(['xcrun', '--sdk', 'macosx', '--find', 'swiftc']))
    sdk = Path(run(['xcrun', '--sdk', 'macosx', '--show-sdk-path']))
    if not compiler.is_absolute() or not sdk.is_absolute() or not sdk.is_dir():
        raise RuntimeError('Missing macOS compiler/SDK')
    # SDK settings and selected driver/version are representative dependencies;
    # not a hash of every SDK header, compiler dylib or framework on the host.
    settings = sdk / 'SDKSettings.json'
    key = fingerprint({'script': file_hash(script), 'source': file_hash(source),
                       'compiler': str(compiler.resolve()), 'compiler_hash': file_hash(compiler),
                       'version': run([compiler, '--version']), 'sdk': str(sdk.resolve()),
                       'sdk_version': run(['xcrun', '--sdk', 'macosx', '--show-sdk-version']),
                       'settings': file_hash(settings), 'arch': platform.machine(),
                       'deployment_target': os.environ.get('MACOSX_DEPLOYMENT_TARGET', '')})
    return compiler, sdk, key


with locked(state, 'pbfile') as receipt:
    directories(home, root)
    previous = load_receipt(receipt, 'pbfile', lambda name: name == 'pbfile')
    compiler, sdk, key = compiler_inputs()
    if not current(root, previous, key):
        with tempfile.TemporaryDirectory(prefix='.pbfile-stage-', dir=root) as temporary:
            stage = Path(temporary)
            target = stage / 'pbfile'
            env = dict(os.environ, CLANG_MODULE_CACHE_PATH=str(stage / 'clang-cache'),
                       SWIFT_MODULECACHE_PATH=str(stage / 'swift-cache'))
            run([compiler, '-sdk', sdk, '-O', '-whole-module-optimization',
                 '-module-cache-path', stage / 'swift-cache', source, '-o', target], env=env)
            record(target)
            if target.stat().st_size == 0:
                raise RuntimeError('Empty pbfile compiler output')
            target.chmod(0o755)
            # No arguments exits before any pasteboard access in pbfile.swift.
            run([target], env=env)
            if key != compiler_inputs()[2]:
                raise RuntimeError('pbfile dependencies changed during compilation')
            publish(root, stage, ['pbfile'], receipt, 'pbfile', key, previous)

import configparser
import re
from urllib.parse import urlparse

mise, config, data, state, script = map(Path, sys.argv[1:])
root = data / 'vale/styles'
configuration = config / 'vale/vale.ini'


def read_config():
    if not regular(configuration):
        raise RuntimeError(f'Missing Vale config: {configuration}')
    text = configuration.read_text()
    parser = configparser.ConfigParser(interpolation=None, strict=True)
    parser.read_string('[DEFAULT]\n' + text)
    defaults = parser.defaults()
    if set(defaults) - {'stylespath', 'packages', 'minalertlevel'}:
        raise RuntimeError('Unsupported Vale global inputs; extend the explicit contract first')
    if defaults.get('stylespath') != str(root):
        raise RuntimeError('Vale StylesPath differs from the owned output root')
    package = defaults.get('packages', '')
    if any(char in package for char in ('\n', '\r', ',')):
        raise RuntimeError('Expected exactly one single-line Google package')
    # One style-only Google package. Config bundles, recursive packages and
    # arbitrary package sets need their own output contract, not a blind sync.
    if package == 'Google':
        dependency = 'floating Google (resolved only when sync is needed)'
    elif urlparse(package).scheme == 'https' and urlparse(package).path.endswith('/Google.zip'):
        dependency = package
    else:
        path = Path(package)
        if not path.is_absolute() or not path.exists() or path.name not in ('Google', 'Google.zip'):
            raise RuntimeError('Expected Google, HTTPS Google.zip, or absolute local Google package')
        dependency = input_tree(path) if path.is_dir() else file_hash(path)
    return text, package, dependency


def inputs():
    text, package, dependency = read_config()
    return fingerprint({'script': file_hash(script), 'config': text, 'package': dependency,
                        'binary': file_hash(tool), 'path': str(tool.resolve()),
                        'version': run([tool, '--version'])})


def allowed(name):
    return name in ('Google/vocab.txt', 'Google/meta.json') or bool(re.fullmatch(r'Google/[A-Za-z0-9_-]+\.yml', name))


with locked(state, 'vale') as receipt:
    directories(data, root)
    tool = selected_tool(mise, 'vale')
    previous = load_receipt(receipt, 'vale', allowed)
    floor = {'Google/Acronyms.yml', 'Google/AMPM.yml'}
    if previous and not floor <= set(previous['files']):
        raise RuntimeError('Incomplete Google receipt')
    key = inputs()
    if not current(root, previous, key):
        with tempfile.TemporaryDirectory(prefix='.vale-stage-', dir=root) as temporary:
            stage = Path(temporary)
            styles = stage / 'styles'
            styles.mkdir()
            text, package, dependency = read_config()
            staged_config = stage / 'vale.ini'
            # Construct a bounded sync config instead of text substitution:
            # INI accepts indentation/colon separators that a regex can miss.
            staged_config.write_text(f'StylesPath = {styles}\nPackages = {package}\n'
                                     'MinAlertLevel = suggestion\n\n[*]\nBasedOnStyles = Google\n')
            env = {k: v for k, v in os.environ.items() if not k.startswith('VALE_')}
            run([tool, '--no-global', '--config=' + str(staged_config), 'sync'], env=env)
            names = []
            for path in styles.rglob('*'):
                name = str(path.relative_to(styles))
                if path.is_symlink() or (path.is_file() and not allowed(name)):
                    raise RuntimeError(f'Unexpected Google package output: {name}')
                if path.is_file():
                    record(path)
                    if name.endswith('.yml') and path.stat().st_size == 0:
                        raise RuntimeError(f'Empty Google rule: {name}')
                    if name == 'Google/meta.json':
                        json.loads(path.read_text())
                    path.chmod(0o644)
                    names.append(name)
                elif name not in ('Google', 'config'):
                    raise RuntimeError(f'Unexpected Google package directory: {name}')
            if not floor <= set(names):
                raise RuntimeError('Google package is missing required rules')
            # Parse every downloaded rule through the consumer. Alerts are fine;
            # parser/runtime errors remain failures. Never lint user documents.
            validation = stage / 'validate.ini'
            validation.write_text(f'StylesPath = {styles}\nMinAlertLevel = suggestion\n[*]\nBasedOnStyles = Google\n')
            run([tool, '--no-global', '--config=' + str(validation), '--no-exit', '--ext=.txt'],
                env=env, data='A simple validation sentence.\n')
            if key != inputs():
                raise RuntimeError('Vale dependencies changed during sync')
            publish(root, styles, names, receipt, 'vale', key, previous)

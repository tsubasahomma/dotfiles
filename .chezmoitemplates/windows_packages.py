"""WinGet provisioning policy; Windows transport preserves the full HRESULT.

CLI/output baseline: microsoft/winget-cli v1.12.350. See docs/platforms/wsl.md.
The bridge uses Windows PowerShell 5.1/.NET, not a POSIX winget.exe exit status.
"""
import base64
import json
import re
import subprocess
import sys


# All inserted arguments are validated ASCII tokens, so ProcessStartInfo's
# Windows command line needs no quoting. FileName is separate (may have spaces).
BRIDGE = r"""
$ErrorActionPreference = 'Stop'
try {
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [Console]::OutputEncoding = $utf8
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = (Get-Command winget.exe -CommandType Application -ErrorAction Stop).Source
    $info.Arguments = '@@ARGUMENTS@@'
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    $info.RedirectStandardInput = $true
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.StandardOutputEncoding = $utf8
    $info.StandardErrorEncoding = $utf8
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $info
    if (-not $process.Start()) { throw 'WinGet did not start' }
    $process.StandardInput.Close()
    $outTask = $process.StandardOutput.ReadToEndAsync()
    $errTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $result = @{
        exitCode = $process.ExitCode
        stdout = $outTask.Result
        stderr = $errTask.Result
    }
    $process.Dispose()
    [Console]::Out.WriteLine(($result | ConvertTo-Json -Compress))
    exit 0
} catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
"""
TOKEN = re.compile(r'[A-Za-z0-9._-]+\Z')
PACKAGE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]*\Z')
NO_APPLICATIONS_FOUND = 0x8A150014
COMMON = ['--source', 'winget', '--exact', '--accept-source-agreements',
          '--disable-interactivity', '--authentication-mode', 'silent']


def winget(arguments):
    if not all(isinstance(arg, str) and TOKEN.fullmatch(arg) for arg in arguments):
        raise RuntimeError('unsupported WinGet argument; refusing command-line interpolation')
    script = BRIDGE.replace('@@ARGUMENTS@@', ' '.join(arguments))
    encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
    result = subprocess.run(['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive',
                             '-EncodedCommand', encoded], stdin=subprocess.DEVNULL,
                            capture_output=True, encoding='utf-8', errors='strict')
    # Even a Windows launch failure whose low byte is zero must produce valid
    # JSON. Never interpret a POSIX returncode as a WinGet HRESULT.
    if result.returncode != 0 or result.stderr.strip():
        raise RuntimeError(f'Windows bridge failed ({result.returncode}): {result.stderr.strip()}')
    try:
        reply = json.loads(result.stdout)
        if not isinstance(reply, dict) or set(reply) != {'exitCode', 'stdout', 'stderr'}:
            raise ValueError('unexpected response fields')
        code = reply['exitCode']
        if type(code) is not int or not -(2**31) <= code < 2**31:
            raise ValueError('exitCode is not a Windows signed Int32')
        if not all(isinstance(reply[key], str) for key in ('stdout', 'stderr')):
            raise ValueError('output is not text')
    except (ValueError, TypeError) as error:
        raise RuntimeError(f'invalid Windows bridge response: {error}') from error
    return code & 0xFFFFFFFF, reply['stdout'], reply['stderr']


def list_lines(output):
    # Strip display formatting only. Never discard warnings or source messages.
    output = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', output)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return [line for line in lines if line not in ('-', '\\', '|', '/')]


def installed(app_id):
    code, output, error = winget(['list', '--id', app_id, *COMMON])
    lines = list_lines(output)
    # ListCommand treats some source failures as warnings on stdout, including
    # alongside NO_APPLICATIONS_FOUND. Require the clean output shape as well
    # as the full code. No English/localized phrase decides absence.
    if not error.strip():
        if code == NO_APPLICATIONS_FOUND and len(lines) == 1:
            return False
        if (code == 0 and len(lines) == 3 and re.fullmatch(r'-{3,}', lines[1])
                and re.search(r'\s' + re.escape(app_id) + r'\s+\S', lines[2])):
            return True
    raise RuntimeError(f'WinGet list {app_id} failed or was ambiguous (0x{code:08X}); '
                       f'no install attempted for this ID.\n{output}\n{error}')


def main(package_ids):
    try:
        # Validate the complete declaration before starting any Windows process.
        if not isinstance(package_ids, list) or not all(
                isinstance(app_id, str) and PACKAGE_ID.fullmatch(app_id) for app_id in package_ids):
            raise RuntimeError('Windows package IDs must be nonempty ASCII ID tokens')
        for app_id in package_ids:
            if installed(app_id):
                print(f'[Windows Packages] {app_id} is already installed.', flush=True)
                continue
            print(f'[Windows Packages] Installing {app_id}...', flush=True)
            code, output, error = winget(['install', '--id', app_id, *COMMON,
                                         '--silent', '--accept-package-agreements', '--no-upgrade'])
            # In the baseline ID-install flow, source open/update/auth notices
            # precede ReportManifestIdentityWithVersion. Dependencies reuse that
            # source (DependenciesFlow::OpenDependencySource), not a second open.
            # Refuse any preamble instead of accepting a source warning + code 0.
            lines = list_lines(output)
            identity = r'^.+ \[' + re.escape(app_id) + r'\] .+ \S+$'
            if (code != 0 or error.strip() or not lines
                    or not re.fullmatch(identity, lines[0])):
                raise RuntimeError(f'WinGet install {app_id} failed or output was unrecognized '
                                   f'(0x{code:08X}); the package may already have changed.\n{output}\n{error}')
            if output.strip():
                print(output.rstrip(), flush=True)
        print('[Windows Packages] Windows package provisioning complete.', flush=True)
        return 0
    except (OSError, UnicodeError, RuntimeError) as error:
        print(f'[Windows Packages] {error}', file=sys.stderr)
        return 1

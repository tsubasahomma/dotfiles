# WSL2 convergence validation

## Purpose

This document defines the repository-owned WSL2 convergence validation contract
for this chezmoi-managed dotfiles source-state repository.

It makes future WSL2, 1Password bridge, SSH agent, systemd user service, and
Windows interop changes reviewable against explicit local validation
expectations.

This document is documentation-only. It does not change WSL2, 1Password, SSH,
systemd user service, shell startup, WezTerm, chezmoi script, mise task, package,
runtime, dependency, lockfile, or CI behavior. It also does not prove local WSL2
convergence or idempotency by itself.

WSL2 is a first-class supported host path in this repository. It must be
reviewed as WSL-to-Windows bridge behavior, not as generic Linux behavior.

## Scope and non-goals

This document covers validation expectations for the current WSL2 boundary
across:

- WSL2 detection
- Windows username discovery
- Windows interop availability
- `npiperelay.exe` discovery
- `wslpath` conversion
- rendered `SSH_AUTH_SOCK`
- rendered SSH `IdentityAgent`
- rendered 1Password SSH agent config
- Windows-host 1Password agent config sync
- systemd user service rendering and enablement
- `1password-bridge.service`
- `socat` bridge behavior
- WezTerm Windows sync assumptions
- CI fallback versus local interactive validation

This document does not:

- edit `.chezmoi.toml.tmpl`, `.bootstrap-identity.sh`, `.chezmoiscripts/*`,
  `.chezmoidata/*`, `.chezmoitemplates/*`, `.chezmoiexternal.toml.tmpl`,
  `dot_zshenv.tmpl`, SSH templates, 1Password templates, systemd templates, or
  mise tasks
- add, remove, or normalize script trigger hashes
- change WSL2, Windows dependency provisioning, 1Password, SSH signing, SSH
  agent, WSL bridge, WezTerm sync, shell, Neovim, Starship, Git, Homebrew, mise,
  GitHub Actions, or CI behavior
- change package lists, tool versions, runtime versions, dependencies, or
  lockfiles
- claim that documentation alone validates convergence, idempotency, bridge
  health, service health, or Windows interop health
- make local WSL2 runtime commands required or meaningful on non-WSL hosts
- duplicate the full script table from [Chezmoi action graph](./action-graph.md)
- authorize WSL2 implementation changes

## Baseline documents

Use this validation contract with these baseline documents:

- [Chezmoi action graph](./action-graph.md)
- [Chezmoi script contract inspection](./script-contract-inspection.md)
- [Chezmoi script trigger audit](./script-trigger-audit.md)
- [Bootstrap and identity boundary](./bootstrap-identity-boundary.md)
- [Mise task boundary](./mise-task-boundary.md)
- [Doctor and repair task boundary](./doctor-repair-task-boundary.md)
- [Chezmoi data contract boundary](./data-contract-boundary.md)

Official semantics used here:

- Chezmoi scripts are source-state entries whose names start with `run_`.
  `run_onchange_` scripts are decided from rendered script content, and template
  scripts are rendered before that decision.
- A root `.chezmoiscripts/` directory runs scripts as scripts without creating a
  corresponding target directory.
- Template files use chezmoi's Go-template-based template engine with chezmoi
  template data and functions.
- Hooks are separate from scripts, and `read-source-state.pre` runs before the
  source state is read.
- `.chezmoiexternal.*` entries describe external source-state resources and may
  be templated.
- Mise tasks provide repository-local task entry points. This repository's task
  taxonomy is local to this repository.

Official references:

- https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/
- https://www.chezmoi.io/reference/special-directories/chezmoiscripts/
- https://www.chezmoi.io/reference/configuration-file/hooks/
- https://www.chezmoi.io/user-guide/templating/
- https://www.chezmoi.io/reference/templates/
- https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/
- https://mise.jdx.dev/tasks/
- https://mise.jdx.dev/tasks/running-tasks.html

Repository-local WSL2 contracts used here are derived from current source state,
not from a generic chezmoi or mise convention.

## Local WSL2 convergence definition

For this repository, local WSL2 convergence means that a WSL2 host can render
and, when intentionally applied by the maintainer, operate the repository's
WSL-to-Windows authentication and interop surfaces consistently with the current
source-state contracts.

A locally converged WSL2 host should have evidence that:

1. the host is detected as WSL2 by the repository's dynamic data boundary;
2. Windows interop commands needed by the WSL2 path are available;
3. Windows username and profile-path discovery work or have an explicit
   maintainer-provided fallback;
4. `npiperelay.exe` discovery and `wslpath` conversion work when the bridge path
   is expected to be active;
5. `SSH_AUTH_SOCK`, SSH `IdentityAgent`, the rendered 1Password SSH agent
   config, and the rendered systemd service agree on the active socket path;
6. the Windows-host 1Password SSH agent config sync path can locate both source
   and destination config files when sync is expected;
7. `1password-bridge.service` is rendered, enabled, and active when the WSL2
   relay path is expected to be active;
8. `socat` and `npiperelay.exe` can maintain the Unix-socket-to-Windows-pipe
   bridge when the service path is active;
9. WezTerm Windows sync assumptions are validated separately from authentication
   bridge health;
10. CI remains a broad source-state and rendered-output validation surface, not
    proof of local interactive WSL2 convergence.

This definition is conditional on the active host path. For example, missing
`npiperelay_wsl` can be a hard-fail for a future PR that expects the WSL2 bridge
path to be active, but it can be not applicable or a soft fallback for CI,
non-WSL hosts, or relay-absent paths.

## Validation layers

### Source-state inspection

Source-state inspection reviews repository files without rendering templates or
touching local target state.

Use this layer to confirm that a proposed change only touches documentation or
the intended WSL2 source-state surfaces.

Relevant source-state surfaces include:

- [`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl)
- [`.chezmoiexternal.toml.tmpl`](../../.chezmoiexternal.toml.tmpl)
- [`.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl)
- [`.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl)
- [`.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl)
- [`.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl)
- [`dot_zshenv.tmpl`](../../dot_zshenv.tmpl)
- [`dot_config/ssh/config.tmpl`](../../dot_config/ssh/config.tmpl)
- [`dot_config/1Password/ssh/private_agent.toml.tmpl`](../../dot_config/1Password/ssh/private_agent.toml.tmpl)
- [`dot_config/systemd/user/1password-bridge.service.tmpl`](../../dot_config/systemd/user/1password-bridge.service.tmpl)
- [`dot_config/mise/tasks/doctor/executable_identity.tmpl`](../../dot_config/mise/tasks/doctor/executable_identity.tmpl)
- [`dot_config/mise/tasks/sync/executable_wezterm.tmpl`](../../dot_config/mise/tasks/sync/executable_wezterm.tmpl)

Source-state inspection does not prove local WSL2 runtime behavior. It only
collects review evidence about the repository-owned contract.

### Rendered-output inspection

Rendered-output inspection evaluates templates for the current host without
claiming that runtime services or sockets are healthy.

Use this layer to review:

- `.is_wsl`, `.windows_user`, `.npiperelay_wsl`, `.ssh_auth_sock`, and
  `paths.*` values
- rendered `SSH_AUTH_SOCK` in `dot_zshenv.tmpl`
- rendered SSH `IdentityAgent` in `dot_config/ssh/config.tmpl`, when present
- rendered 1Password SSH agent config shape without exposing item IDs, account
  IDs, or key material
- rendered `1password-bridge.service`, especially `ExecStartPre`,
  `UNIX-LISTEN`, `npiperelay.exe`, and Windows OpenSSH pipe routing
- rendered WSL2 script content and trigger hashes without changing those hashes
- rendered WezTerm sync behavior and CI skip behavior

Rendered-output inspection can expose host-local paths and secret-adjacent
metadata. Redact before sharing output.

### Local WSL2 runtime validation

Local WSL2 runtime validation is WSL2-host-specific. It is not required or
meaningful on non-WSL hosts.

Use this layer only on an interactive WSL2 host when the review scope touches or
depends on WSL2 behavior. It checks live availability of:

- WSL2 kernel detection evidence
- `cmd.exe`, `powershell.exe`, `wslpath`, `winget.exe`, `op.exe`, and
  `npiperelay.exe`, where the active path requires them
- the Unix socket referenced by `SSH_AUTH_SOCK`
- SSH's resolved `IdentityAgent`
- WSL-side and Windows-side 1Password SSH agent config files
- `systemctl --user` service state for `1password-bridge.service`
- `socat` and `npiperelay.exe` bridge process or socket behavior
- WezTerm sync source and Windows destination files when WezTerm sync is in
  scope

Runtime validation can demonstrate local health for one machine. It does not
prove all WSL2 hosts are converged.

### CI validation

CI validation is separate from local interactive WSL2 validation.

CI can check broad source-state and rendered-output behavior for the automation
path. It can also catch Markdown, shell formatting, and repository validation
issues. It cannot prove:

- local Windows interop availability
- local 1Password desktop or CLI session state
- local Windows OpenSSH agent pipe health
- local `npiperelay.exe` installation or PATH routing
- local WSL2 systemd user service health
- local `socat` bridge health
- local WezTerm Windows sync behavior

Do not claim CI proves local WSL2 convergence.

## WSL2 validation surfaces

| Surface | Current contract | Primary validation layer |
| --- | --- | --- |
| WSL2 detection | `.chezmoi.toml.tmpl` derives `.is_wsl` from Linux kernel release data. | Rendered-output and local runtime validation. |
| Windows username discovery | WSL2 uses `WINDOWS_USER` when set, otherwise `cmd.exe` discovery. | Rendered-output and local runtime validation. |
| Windows interop availability | WSL2 branches call Windows commands such as `cmd.exe`, `powershell.exe`, `winget.exe`, and `op.exe`. | Local WSL2 runtime validation. |
| `npiperelay.exe` discovery | `.chezmoi.toml.tmpl` searches through PowerShell and converts the result with `wslpath`. | Rendered-output and local runtime validation. |
| `wslpath` conversion | Windows paths discovered through PowerShell are converted to WSL paths. | Local WSL2 runtime validation. |
| `SSH_AUTH_SOCK` | `dot_zshenv.tmpl` exports the rendered `.ssh_auth_sock` value. | Rendered-output and local runtime validation. |
| SSH `IdentityAgent` | `dot_config/ssh/config.tmpl` renders an `IdentityAgent` line when the template has an SSH agent socket path. | Rendered-output inspection. |
| 1Password SSH agent config | `private_agent.toml.tmpl` renders account-aware `ssh-keys` entries from `.identities`. | Rendered-output inspection with redaction. |
| Windows 1Password config sync | Phase 51 copies the WSL-side rendered agent config to the Windows 1Password config location on WSL2. | Source-state, rendered-output, and local runtime validation. |
| `1password-bridge.service` rendering | The systemd user service renders only when `.is_wsl` is true and `.npiperelay_wsl` is not empty. | Rendered-output inspection. |
| Service enablement | Phase 90 enables and starts the bridge service only when WSL2 relay data is present. | Local WSL2 runtime validation. |
| `socat` bridge | The service removes the stale Unix socket and starts `socat` to bridge the Unix socket to the Windows OpenSSH agent pipe through `npiperelay.exe`. | Local WSL2 runtime validation. |
| WezTerm Windows sync | Phase 52 and `sync:wezterm` copy rendered WezTerm config to the Windows host on WSL2 and skip in CI. | Source-state, rendered-output, and local runtime validation when in scope. |
| CI fallback | CI exercises automation-safe paths and skips or softens local interactive requirements. | CI validation only. |

## Read-only command bundle

The following bundle is intended for WSL2-host-specific evidence collection.
Run it from the repository root on a WSL2 host. It is read-only, but the output
can include local paths, usernames, service details, and secret-adjacent
metadata. Redact before sharing.

```sh
set +e

run() {
  printf '\n===== %s =====\n' "$*"
  "$@"
  exit_code=$?
  printf -- '----- exit code: %s -----\n' "$exit_code"
}

run git branch --show-current
run git status --short

run sh -c 'uname -a'
run sh -c 'test -r /proc/sys/kernel/osrelease && cat /proc/sys/kernel/osrelease || true'

run rg -n --hidden \
  'is_wsl|windows_user|npiperelay_wsl|ssh_auth_sock|SSH_AUTH_SOCK|IdentityAgent|OP_BIOMETRIC_UNLOCK_ENABLED|WSLENV|wslpath|powershell.exe|cmd.exe|winget.exe|npiperelay|1password-bridge|socat|win32yank|wezterm' \
  .chezmoi.toml.tmpl \
  .chezmoiexternal.toml.tmpl \
  .chezmoiscripts \
  dot_zshenv.tmpl \
  dot_config/ssh/config.tmpl \
  dot_config/1Password/ssh/private_agent.toml.tmpl \
  dot_config/systemd/user/1password-bridge.service.tmpl \
  dot_config/mise/tasks/doctor/executable_identity.tmpl \
  dot_config/mise/tasks/sync/executable_wezterm.tmpl \
  docs/chezmoi

run chezmoi execute-template 'is_wsl={{ .is_wsl }} windows_user_known={{ and (ne .windows_user "") (ne .windows_user "unknown") }} npiperelay_wsl_set={{ ne .npiperelay_wsl "" }} ssh_auth_sock_set={{ ne .ssh_auth_sock "" }} op_status={{ .op_status }}'
run sh -c 'chezmoi execute-template < dot_zshenv.tmpl | rg "SSH_AUTH_SOCK|OP_BIOMETRIC_UNLOCK_ENABLED|WSLENV"'
run sh -c 'chezmoi execute-template < dot_config/ssh/config.tmpl | rg "IdentityAgent|Include|UserKnownHostsFile" || true'
run sh -c 'chezmoi execute-template < dot_config/1Password/ssh/private_agent.toml.tmpl | rg -c "^\[\[ssh-keys\]\]" || true'
run sh -c 'chezmoi execute-template < dot_config/systemd/user/1password-bridge.service.tmpl | sed -n "1,80p"'
run sh -c 'chezmoi execute-template < .chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl | sed -n "1,120p"'
run sh -c 'chezmoi execute-template < .chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl | sed -n "1,120p"'
run sh -c 'chezmoi execute-template < .chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl | sed -n "1,120p"'

run command -v cmd.exe
run command -v powershell.exe
run command -v wslpath
run sh -c 'cmd.exe /c ver >/dev/null 2>&1 && echo "cmd.exe available" || echo "cmd.exe unavailable"'
run powershell.exe -NoProfile -NonInteractive -Command '$PSVersionTable.PSVersion.ToString()'
run powershell.exe -NoProfile -NonInteractive -Command "if (Get-Command npiperelay.exe -ErrorAction SilentlyContinue) { [Console]::Write('npiperelay.exe found') } else { [Console]::Write('npiperelay.exe missing') }"
run sh -c 'wslpath -u "C:\Windows" >/dev/null 2>&1 && echo "wslpath converts Windows paths" || echo "wslpath conversion failed"'

run sh -c 'printf "SSH_AUTH_SOCK set: "; test -n "${SSH_AUTH_SOCK:-}" && echo yes || echo no'
run sh -c 'printf "SSH_AUTH_SOCK socket: "; test -S "${SSH_AUTH_SOCK:-}" && echo yes || echo no'
run sh -c 'ssh -G github.com 2>/dev/null | rg "^identityagent " || true'
run sh -c 'ssh-add -l 2>/dev/null || true'

run sh -c 'test -f "$XDG_CONFIG_HOME/1Password/ssh/agent.toml" && echo "WSL agent config present" || echo "WSL agent config missing"'
run sh -c 'WIN_HOME=$(cmd.exe /c "echo %USERPROFILE%" 2>/dev/null | tr -d "\r"); test -n "$WIN_HOME" && test -f "$(wslpath -u "$WIN_HOME")/AppData/Local/1Password/config/ssh/agent.toml" && echo "Windows agent config present" || echo "Windows agent config missing"'

run command -v systemctl
run sh -c 'systemctl --user is-enabled 1password-bridge.service 2>/dev/null || true'
run sh -c 'systemctl --user is-active 1password-bridge.service 2>/dev/null || true'
run sh -c 'systemctl --user cat 1password-bridge.service 2>/dev/null || true'
run sh -c 'ps -ef | rg "socat|npiperelay" || true'

run sh -c 'test -f "$XDG_CONFIG_HOME/wezterm/wezterm.lua" && echo "WSL WezTerm config present" || echo "WSL WezTerm config missing"'
run sh -c 'WIN_HOME=$(cmd.exe /c "echo %USERPROFILE%" 2>/dev/null | tr -d "\r"); test -n "$WIN_HOME" && test -f "$(wslpath -u "$WIN_HOME")/.wezterm.lua" && echo "Windows WezTerm config present" || echo "Windows WezTerm config missing"'
```

For non-WSL hosts, do not run the Windows interop, bridge service, or
Windows-host sync commands as validation. Use the standard repository validation
workflow instead.

## Redaction requirements

Redact these values before sharing command output with a Commander Thread,
issue, PR, or external reviewer:

- local Linux username
- Windows username
- home paths
- Windows profile paths
- socket paths when the exact path is not necessary for review
- `npiperelay.exe`, `op.exe`, and `op-ssh-sign*` absolute paths when they expose
  local usernames or install locations
- 1Password account-adjacent values, including account IDs, item IDs, account
  names, vault names, and 1Password CLI output
- SSH key metadata when not needed for review
- public key material
- `ssh-add -l` key comments if they include emails, names, hostnames, or local
  labels
- service status details that include local paths, command lines, environment,
  process IDs, or journal excerpts
- full `chezmoi data` output
- unfiltered rendered `private_agent.toml` output
- unfiltered environment dumps
- Windows profile and AppData paths
- WezTerm config content if it includes local machine paths or private
  host-specific settings

Prefer boolean, count, or filtered outputs when possible. For example, prefer
`npiperelay_wsl_set=true` over sharing the full relay path.

## Hard-fail signals

These signals should block a future WSL2 behavior PR when the active host path
or PR scope expects the corresponding surface to work.

They are conditional. They are not automatically hard-fails for non-WSL hosts,
CI fallback paths, documentation-only PRs, or relay-absent paths.

- WSL2-specific behavior is changed without WSL2-host-specific validation
  evidence or an explicit deferral.
- `.is_wsl` renders `false` on a host that is being used to validate WSL2
  behavior.
- Windows interop commands required by the active path are unavailable.
- Windows username discovery is `unknown` when a Windows profile path is needed.
- `wslpath` cannot convert Windows paths required by the active path.
- `npiperelay_wsl` is empty when the PR expects the WSL2 bridge service to be
  active.
- `SSH_AUTH_SOCK` is unset, points to the wrong socket, or is not a Unix socket
  when the active path expects SSH to use the WSL2 bridge.
- rendered SSH config omits or misroutes `IdentityAgent` when the active path
  expects SSH to use the repository-owned bridge socket.
- rendered 1Password SSH agent config is missing required `ssh-keys` entries
  when identities are expected to be mapped.
- Windows-side 1Password agent config sync cannot find its WSL source or Windows
  destination when sync is in scope.
- `1password-bridge.service` does not render when `.is_wsl=true` and
  `.npiperelay_wsl` is expected to be non-empty.
- `systemctl --user` cannot enable or start the bridge service when service
  enablement is in scope.
- `1password-bridge.service` is inactive or failed when the active path expects
  the bridge to be running.
- `socat` cannot create or maintain the Unix socket bridge when the service path
  is active.
- `ssh-add -l` cannot reach the expected agent after the bridge is expected to be
  active and recoverable.
- WezTerm Windows sync fails when the PR scope changes or depends on WezTerm
  Windows sync behavior.
- A PR claims CI proves local WSL2 convergence.

## Soft-fallback signals

These signals may be acceptable when they match the active host path and are
reported clearly.

- Non-WSL hosts do not render or run WSL2-only scripts.
- CI skips local interactive WSL2 behavior and does not validate the local bridge.
- `run_onchange_after_52-sync-wezterm-config.sh.tmpl` skips WezTerm sync in CI.
- Phase 90 reports that no environment-specific services are required when
  `.is_wsl` is false or `.npiperelay_wsl` is empty.
- WSL-side 1Password agent config sync is a no-op when the source config does not
  exist.
- WezTerm sync is a no-op when the WSL-side source config does not exist.
- `ssh-add -l` may warn rather than fail in CI or in a documented local
  relay-absent path.
- Missing `npiperelay.exe` may be reported as a relay-absent path only when the
  PR does not require the WSL2 bridge to be active.
- Missing Windows GUI packages may be acceptable in CI when GUI provisioning is
  intentionally skipped.
- Documentation-only PRs may defer WSL2 runtime validation if they do not claim
  local convergence.

## Follow-up candidates

These candidates are not requirements for issue #161. Scope each as a separate
behavior-aware issue before implementation.

1. Add a WSL2-only doctor task that emits redaction-safe boolean validation
   signals for Windows interop, relay discovery, socket health, and service
   health.
2. Consider a rendered-output inspection helper that summarizes WSL2 data without
   exposing full `chezmoi data`.
3. Review whether SSH `IdentityAgent` rendering should use the same socket data
   contract as `dot_zshenv.tmpl`.
4. Review whether `npiperelay.exe`, Windows profile, and sync destination
   handling should have a more explicit fallback or diagnostic path.
5. Review whether WezTerm Windows sync and the `sync:wezterm` task should share a
   single validation entry point.
6. Review whether service enablement should report more actionable local
   diagnostics without exposing sensitive paths.
7. Review whether WSL2 external-resource validation for `win32yank.exe` should
   have its own non-mutating check.

## Review checklist

Before approving a future WSL2 behavior change, verify:

- The PR identifies whether it changes source state, rendered output, local WSL2
  runtime behavior, CI behavior, or only documentation.
- The PR preserves current behavior unless the linked issue explicitly scopes a
  behavior change.
- WSL2 is reviewed as a first-class host path.
- The PR does not treat CI as proof of local interactive WSL2 convergence.
- The PR includes WSL2-host-specific runtime evidence when it changes or depends
  on WSL2 runtime behavior.
- Shared evidence is redacted according to this document.
- Hard-fail and soft-fallback signals are interpreted relative to the active host
  path.
- Any follow-up candidates are documented as future work, not hidden
  requirements for the current PR.
- GitHub Actions CI is reported only after CI evidence exists.

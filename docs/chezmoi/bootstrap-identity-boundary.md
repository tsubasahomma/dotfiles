# Bootstrap and identity boundary

## Purpose

This document records the current repository-owned bootstrap, 1Password, and
identity boundary contracts for this chezmoi-managed dotfiles source-state
repository.

It is documentation-only. It does not change bootstrap, identity discovery,
1Password, SSH signing, SSH agent routing, scoped Git identity, WSL2 bridge,
systemd user service, shell startup, script, mise, package, runtime, dependency,
lockfile, or CI behavior.

Use this document with the current [Chezmoi action graph](./action-graph.md),
the read-only [Chezmoi script contract inspection](./script-contract-inspection.md)
workflow, the [Chezmoi script trigger audit](./script-trigger-audit.md), the
[Mise task boundary](./mise-task-boundary.md), the
[Chezmoi data contract boundary](./data-contract-boundary.md), and
[WSL2 convergence validation](./wsl2-convergence-validation.md).

## Scope and non-goals

This document covers the current boundary between:

- [`.bootstrap-identity.sh`](../../.bootstrap-identity.sh)
- [`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl)
- `[hooks.read-source-state.pre]`
- 1Password CLI availability and `op_status`
- identity discovery and SSH key metadata
- generated Git identity outputs and `allowed_signers`
- SSH signing helper selection
- SSH agent socket routing
- WSL2 bridge assumptions
- CI fallback behavior

This document does not:

- edit `.bootstrap-identity.sh`, `.chezmoi.toml.tmpl`, `.chezmoiscripts/*`,
  `.chezmoiexternal.toml.tmpl`, `.chezmoidata/*`, or `.chezmoitemplates/*`
- expose account IDs, item IDs, private key material, actual public keys,
  unfiltered `chezmoi data`, or environment dumps
- claim that documentation alone validates convergence or idempotency
- duplicate the full script table from [Chezmoi action graph](./action-graph.md)
- authorize bootstrap, 1Password, identity, SSH, WSL2, systemd, shell, mise, or
  CI implementation changes

## Official semantics boundary

Official chezmoi semantics used here:

- Hooks run before or after configured events.
- `read-source-state` is the event for reading the source state.
- Hooks always run, even for `--dry-run`, and should be fast and idempotent.
- A `read-source-state.pre` hook runs before the source state is read.
- Chezmoi templates use Go `text/template` syntax extended with Sprig and
  chezmoi functions.
- Files with a `.tmpl` suffix and entries under `.chezmoitemplates/` are
  interpreted as templates when read from source state.
- Template data comes from multiple sources, including `.chezmoi` data,
  `.chezmoidata.$FORMAT` files, and the `data` section of the configuration
  file.
- Chezmoi supports 1Password through the 1Password CLI and exposes official
  1Password template functions.

Official references:

- https://www.chezmoi.io/reference/configuration-file/hooks/
- https://www.chezmoi.io/user-guide/templating/
- https://www.chezmoi.io/reference/templates/
- https://www.chezmoi.io/user-guide/advanced/install-your-password-manager-on-init/
- https://www.chezmoi.io/user-guide/password-managers/1password/

Repository-local contracts used here:

- `.bootstrap-identity.sh` is this repository's hook-time bootstrap script.
- `.chezmoi.toml.tmpl` is this repository's dynamic data derivation boundary.
- `op_status`, `identities`, and `ssh_keys_hash` are repository-local data
  contracts.
- The repository discovers SSH Key items by 1Password CLI commands and item
  metadata conventions, not by a standard chezmoi identity schema.
- WSL2 bridge behavior is repository-local behavior across WSL, Windows,
  1Password, OpenSSH agent sockets, systemd user services, and filesystem copy
  boundaries.

If official chezmoi documentation does not define a repository-local behavior,
this document labels it as repository-local rather than official chezmoi
semantics.

## Repository-local boundary map

Current boundary order:

1. Chezmoi evaluates configuration from [`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl).
2. The configuration template derives host, tool, WSL2, 1Password, identity,
   SSH, and path data.
3. `[hooks.read-source-state.pre]` runs
   [`.bootstrap-identity.sh`](../../.bootstrap-identity.sh).
4. The bootstrap script exits immediately in CI.
5. Outside CI, the bootstrap script ensures a usable `mise` binary is available
   before later source-state reading and script convergence depend on mise.
6. Chezmoi reads, renders, and applies source state.
7. Session validation, identity convergence, SSH agent config sync, and service
   enablement happen later through `.chezmoiscripts/*` and rendered targets.

The order above records current behavior. It does not assert that this is the
only valid future architecture.

## read-source-state.pre hook boundary

[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl) defines:

```toml
[hooks.read-source-state.pre]
    command = "{{ .chezmoi.sourceDir }}/.bootstrap-identity.sh"
```

Current contract:

- The hook is the explicit boundary before chezmoi reads source state.
- The command points to the repository source-state bootstrap script.
- The hook is behavior-sensitive because it runs before normal target rendering
  and script convergence.
- The hook should remain fast and idempotent because official chezmoi semantics
  run hooks whenever the configured event occurs.
- This document records the boundary only; it does not change the hook command
  or hook timing.

## Bootstrap script boundary

[`.bootstrap-identity.sh`](../../.bootstrap-identity.sh) is the current
repository-local bootstrap script for the `read-source-state.pre` hook.

Current responsibilities:

- Use POSIX shell so the hook can run before the managed shell environment
  exists.
- Exit immediately when `CI=true`.
- Create the local binary directory used during bootstrap.
- Add mise shims and the local binary directory to `PATH` for hook execution.
- Resolve an existing `mise` binary when available.
- Install `mise` into the local binary directory when it is not already present.
- Fail when `curl` is required for mise bootstrap but unavailable.
- Suppress mise interactive prompts during bootstrap.
- Trust the source directory before running mise install.
- Use a temporary mise config so bootstrap dependencies stay isolated.
- Run `mise install` for the trusted source state.

Current non-responsibilities:

- It does not discover 1Password identities.
- It does not render Git, SSH, 1Password, WSL2, or systemd targets.
- It does not generate `allowed_signers`.
- It does not own scoped Git identity routing.
- It does not validate local convergence or idempotency by itself.

## Dynamic chezmoi config data boundary

[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl) is the current dynamic data
boundary.

It derives and exposes repository-local data including:

- `osid` and `arch`
- `is_wsl`
- `windows_user`
- `npiperelay_wsl`
- `brew_prefix`
- `op_status`
- `ssh_keys_hash`
- `identities`
- `ssh_auth_sock`
- `paths.op`
- `paths.mise`
- `paths.op_sign`
- XDG path values under `paths.*`

Current contract:

- WSL2 detection is derived from Linux kernel release data containing
  `microsoft`.
- The Windows username is derived only for WSL2 hosts.
- `npiperelay.exe` is discovered through Windows PowerShell and converted to a
  WSL path through `wslpath` when available.
- The `op` binary is resolved through Windows PowerShell on WSL2 and through
  `PATH` on non-WSL hosts.
- Local non-CI hosts hard-fail when the 1Password CLI is unavailable.
- Local non-CI hosts hard-fail when the 1Password session is locked.
- 1Password SSH Key item discovery happens only when `op_status` is `ready`.
- `ssh_keys_hash` summarizes discovered SSH Key item metadata for rendered
  identity-trigger content.
- SSH agent socket and SSH signing helper paths are platform-specific rendered
  data.

Because this file is both a chezmoi configuration template and the dynamic data
contract, edits to it are behavior-sensitive and out of scope for this issue.

## 1Password availability states

The current repository behavior recognizes these effective states.

| State | Current source of state | Local interactive behavior | CI behavior | Downstream effect |
| --- | --- | --- | --- | --- |
| `missing` | Explicit branch in [`.chezmoiscripts/run_onchange_before_00-validate-session.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-validate-session.sh.tmpl). | The validation script warns and allows basic provisioning to continue when this state is rendered. Separately, `.chezmoi.toml.tmpl` currently hard-fails outside CI when the `op` CLI cannot be resolved. | CI-specific branches avoid blocking automation. | Identity-dependent outputs may have no discovered 1Password identities. |
| `locked` | `.chezmoi.toml.tmpl` derives `locked` when `op account get` does not succeed. | `.chezmoi.toml.tmpl` hard-fails outside CI; the validation script also fails outside CI when a locked branch is rendered. | The validation script bypasses the locked-session failure when `CI=true`. | Identity discovery does not run; generated identity behavior falls back only where a CI-specific fallback exists. |
| `ready` | `.chezmoi.toml.tmpl` derives `ready` when `op account get` succeeds. | Identity discovery proceeds through 1Password CLI item listing and item detail reads. | CI can use this state only if the runner environment actually provides a working `op` session. | `identities` and `ssh_keys_hash` can be populated from discovered SSH Key item metadata. |

The `missing` and `locked` boundaries should not be normalized in this document.
Any future change to the state model should be scoped as a behavior-sensitive
bootstrap or identity issue.

## Identity discovery and SSH key metadata

Current identity discovery is repository-local behavior implemented in
[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl).

When `op_status` is `ready`, the template:

- lists 1Password accounts through the resolved `op` binary
- lists items tagged `dotfiles-ssh-key` for each account
- reads item details for matching SSH Key items
- extracts repository-local `dotfiles` section fields:
  - `dotfiles_git_name`
  - `dotfiles_git_email`
  - `dotfiles_git_dirs`
- extracts SSH Key metadata fields:
  - `key type`
  - `public key`
- includes an identity only when required Git and public-key metadata is present
- computes a short `key_hash` from the public key for generated file naming
- aggregates item-list JSON into `ssh_keys_hash_input`
- derives `ssh_keys_hash` from the aggregate input, or `none` when no input
  exists

This document intentionally does not show account IDs, item IDs, or public key
material.

## Generated identity outputs

[`.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl)
is the current generated identity output boundary.

Current outputs:

- generated public key files under the managed SSH directory
- generated per-identity Git include files under the XDG Git config directory
- generated `allowed_signers` under the XDG Git config directory
- generated socket state directories used by SSH configuration

Current behavior:

- The script uses `.ssh_keys_hash` as rendered trigger content.
- It recreates the generated Git identity include directory before writing the
  current identity set.
- It writes generated Git config fragments from
  [`.chezmoitemplates/git_identity_config.tmpl`](../../.chezmoitemplates/git_identity_config.tmpl).
- It writes a temporary signers file, sorts it uniquely, then writes
  `allowed_signers` deterministically.
- It emits a CI fallback signer when no identities are mapped.

The CI fallback signer is a file-generation fallback, not a local user identity.

## SSH signing and allowed signers

[`dot_config/git/config.tmpl`](../../dot_config/git/config.tmpl) is the current
Git signing configuration boundary.

Current contract:

- Global Git config uses SSH signing as the signing format.
- `gpg.ssh.program` is rendered from `paths.op_sign`.
- `gpg.ssh.allowedSignersFile` points to the generated `allowed_signers` file.
- `user.useConfigOnly = true` keeps global Git identity unset unless a scoped
  include supplies it.
- Scoped identity includes are generated separately by the identity convergence
  script.

Platform-specific signing helper resolution currently happens in
[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl):

- macOS uses the 1Password application signing helper path.
- WSL2 searches for Windows-side `op-ssh-sign-wsl.exe` or `op-ssh-sign.exe` and
  converts the result with `wslpath`.
- Other hosts fall back to `op-ssh-sign` from `PATH` when available.

## SSH agent socket routing

SSH agent socket routing crosses shell, SSH, 1Password, and WSL2 bridge
surfaces.

Current rendered surfaces:

- [`dot_zshenv.tmpl`](../../dot_zshenv.tmpl) exports `SSH_AUTH_SOCK` from
  `.ssh_auth_sock`.
- [`dot_config/ssh/config.tmpl`](../../dot_config/ssh/config.tmpl) renders
  `IdentityAgent` when an SSH agent socket path is available.
- [`dot_config/1Password/ssh/private_agent.toml.tmpl`](../../dot_config/1Password/ssh/private_agent.toml.tmpl)
  renders account-aware 1Password SSH agent key entries from `.identities`.
- [`dot_config/systemd/user/1password-bridge.service.tmpl`](../../dot_config/systemd/user/1password-bridge.service.tmpl)
  renders the WSL2 user service when WSL2 relay data is present.
- [`.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl)
  syncs the rendered 1Password SSH agent config to the Windows host on WSL2.
- [`.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl)
  enables the WSL2 bridge service when relay data is present.

Current socket paths:

- macOS renders the 1Password application agent socket path under the user's
  Library group container.
- WSL2 renders a Unix socket under the user's `.1password` directory and bridges
  it to the Windows OpenSSH agent pipe through `npiperelay.exe` and `socat`.
- Other non-WSL Linux hosts currently render no repository-owned 1Password SSH
  agent socket path unless future behavior changes add one.

## WSL2 bridge assumptions

WSL2 is a first-class supported host path in this repository.

Current WSL2 assumptions:

- WSL2 is detected from Linux kernel release data.
- Windows interop commands are available when WSL2-specific discovery runs.
- Windows username discovery can be performed through `cmd.exe` unless the
  `WINDOWS_USER` environment variable supplies it.
- `npiperelay.exe` discovery can be performed through `powershell.exe`.
- Windows paths discovered through PowerShell can be converted with `wslpath`.
- The Windows 1Password SSH agent config location is reachable through the WSL
  view of the Windows user profile.
- The rendered WSL-side 1Password SSH agent config is copied to the Windows host
  only when the WSL-side source config exists.
- `OP_BIOMETRIC_UNLOCK_ENABLED` is exported for WSL2, and `WSLENV` propagates it
  across the WSL/Windows boundary.
- A systemd user service can manage the Unix socket bridge when `.is_wsl` is true
  and `npiperelay_wsl` is not empty.
- The bridge service removes the stale Unix socket before starting `socat`.
- `systemctl --user` is expected to be available only for the service enablement
  path; service enablement is skipped when WSL2 relay data is absent.

These are current assumptions, not proof that every WSL2 host is converged.
Local WSL2 validation remains separate from documentation.

## CI fallback behavior

CI behavior is separate from local interactive behavior.

Current CI boundaries:

- `.bootstrap-identity.sh` exits immediately when `CI=true`.
- `.chezmoi.toml.tmpl` skips local non-CI hard-fails guarded by `not CI`.
- The session validation script bypasses the locked-session failure when
  `CI=true`.
- The identity convergence script emits a fallback signer when no identities are
  mapped.
- The identity doctor task treats a locked or unreachable 1Password state as an
  automation-mode bypass when `CI=true`.
- The identity doctor task warns rather than fails when the SSH agent is
  unresponsive in CI.

CI fallback behavior exists so automation can validate file generation and broad
convergence without requiring a personal interactive 1Password session. It is
not a substitute for local interactive 1Password, SSH signing, SSH agent, or
WSL2 bridge validation.

## Hard-fail boundaries

Current hard-fail boundaries include:

- `.bootstrap-identity.sh` fails outside CI when `curl` is required for mise
  bootstrap but unavailable.
- `.bootstrap-identity.sh` fails when mise bootstrap, trust, or install commands
  fail.
- `.chezmoi.toml.tmpl` fails outside CI when the 1Password CLI cannot be
  resolved.
- `.chezmoi.toml.tmpl` fails outside CI when the 1Password session is locked.
- The session validation script fails outside CI when a locked-session branch is
  rendered.
- The identity convergence script fails on shell errors, directory creation
  errors, generated file write errors, `chmod` errors, or malformed rendered
  identity data.
- WSL2 agent config sync fails on WSL2 when required PowerShell, `wslpath`,
  directory creation, or copy operations fail.
- WSL2 bridge service enablement fails when the active `systemctl --user` path
  fails.

## Soft-fallback boundaries

Current soft-fallback boundaries include:

- `.bootstrap-identity.sh` exits without work in CI.
- Existing `mise` is reused instead of reinstalling it.
- The session validation script warns and exits successfully when a `missing`
  1Password state is rendered.
- The session validation script exits successfully for a locked session in CI.
- Identity discovery simply produces no identities when `op_status` is not
  `ready`.
- `ssh_keys_hash` renders as `none` when there is no discovered SSH key hash
  input.
- The identity convergence script generates a CI fallback signer when no
  identities are mapped.
- WSL2 agent config sync is a no-op when the WSL-side source config is absent.
- Service enablement reports that no environment-specific services are required
  when WSL2 relay conditions are not met.
- The identity doctor task attempts WSL2 bridge recovery by restarting the user
  service when the SSH agent is unavailable on WSL2.
- CI identity doctor behavior bypasses personal 1Password and SSH agent failures
  that are expected in automation.

## Follow-up candidates

These candidates are not hidden requirements for issue #152:

- Clarify whether `missing`, `locked`, and `ready` should be normalized into one
  explicit state model across `.chezmoi.toml.tmpl` and session validation.
- Audit whether dynamic 1Password CLI calls in `.chezmoi.toml.tmpl` should be
  split into smaller documented helpers or data contracts.
- Define targeted local WSL2 validation commands for the bridge path without
  exposing account, item, key, or environment secrets.
- Review whether CI fallback signer wording should be made less identity-like in
  a separate behavior-preserving documentation or output-text issue.
- Review unsupported authority-signaling wording in identity scripts and doctor
  output separately from behavior-sensitive identity changes.
- Decide whether non-WSL Linux hosts should have an explicit SSH agent socket
  contract in a future implementation issue.
- Consider whether `.bootstrap-identity.sh` should have a narrower contract for
  mise-only bootstrap or a broader documented bootstrap role.

## Review guidance

For future bootstrap or identity changes:

- Start from this document and [Chezmoi action graph](./action-graph.md).
- Collect read-only evidence with
  [Chezmoi script contract inspection](./script-contract-inspection.md).
- Check trigger-sensitive surfaces against
  [Chezmoi script trigger audit](./script-trigger-audit.md).
- Treat `.bootstrap-identity.sh` and `.chezmoi.toml.tmpl` as behavior-sensitive
  boundaries.
- Keep official chezmoi semantics separate from repository-local identity
  conventions.
- Do not expose secret-adjacent values in issues, PRs, logs, or review notes.
- Review WSL2 as WSL-to-Windows bridge behavior, not generic Linux behavior.
- Keep CI fallback behavior separate from local interactive behavior.
- Do not claim convergence, idempotency, WSL2 bridge health, or CI success
  without command output, CI evidence, or explicit confirmation.

# Chezmoi action graph

## Purpose

This document records the current repository-owned chezmoi action graph and
script contracts for this dotfiles source-state repository.

The goal is to make future chezmoi refactoring reviewable and
behavior-preserving. This document describes current behavior; it does not
declare the current structure to be ideal.

For reusable read-only commands that collect script contract evidence without
duplicating this table, see
[Chezmoi script contract inspection](./script-contract-inspection.md).
For the focused trigger-contract classification derived from that evidence,
see [Chezmoi script trigger audit](./script-trigger-audit.md).
For the bootstrap, 1Password, identity, SSH, and WSL2 bridge boundary, see
[Bootstrap and identity boundary](./bootstrap-identity-boundary.md).
For the focused mise task delegation boundary, see
[Mise task boundary](./mise-task-boundary.md).
For the static, dynamic, and reusable template data ownership boundary, see
[Chezmoi data contract boundary](./data-contract-boundary.md).
For the focused WSL2 local validation contract, see
[WSL2 convergence validation](./wsl2-convergence-validation.md).

## Scope and non-goals

This document covers the current graph across:

- source data
- template data
- external resources
- hooks
- scripts
- mise tasks invoked by scripts
- host-specific branches
- rendered target surfaces
- CI validation surfaces

This document does not change behavior. In particular, it does not:

- change chezmoi script behavior
- add, remove, or normalize script trigger hashes
- change package lists, tool versions, runtime versions, dependencies, or
  lockfiles
- change provisioning behavior
- change identity routing, 1Password behavior, SSH signing behavior, SSH agent
  behavior, scoped Git identity behavior, or WSL bridge behavior
- change shell startup order or command execution semantics
- change Neovim, WezTerm, Starship, Git, SSH, Homebrew, mise, or GitHub Actions
  behavior
- optimize for reducing script count

Follow-up candidates are recorded later in this document, but they are not hidden
requirements for issue #143.

## Official semantics boundary

This repository uses official chezmoi semantics for script execution and hooks,
and repository-local names for its own phase numbers.

Official chezmoi semantics used by this document:

- Chezmoi scripts are source-state entries whose names start with `run_`.
- `run_` scripts run every time `chezmoi apply` runs.
- `run_onchange_` scripts run only when their rendered content has changed since
  the last successful run.
- `run_once_` scripts run once for each unique rendered content version.
- For template scripts, chezmoi evaluates the template before deciding whether
  the script content has changed.
- Scripts are executed in alphabetical order, with `before_` and `after_`
  filename attributes controlling whether they run before or after target
  updates.
- Scripts in the source-root `.chezmoiscripts/` directory run as normal scripts
  without creating a corresponding target directory.
- A template script that renders to only whitespace or an empty string is not
  executed.
- Hooks are separate from scripts. Hooks run before or after configured events
  and should be fast and idempotent.

Official references:

- https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/
- https://www.chezmoi.io/reference/special-directories/chezmoiscripts/
- https://www.chezmoi.io/reference/configuration-file/hooks/
- https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/
- https://mise.jdx.dev/tasks/
- https://mise.jdx.dev/tasks/file-tasks.html
- https://mise.jdx.dev/tasks/running-tasks.html
- https://mise.jdx.dev/tasks/task-configuration.html

Repository-local semantics used by this document:

- Phase numbers such as `00`, `10`, `20`, `50`, and `90` are filename ordering
  conventions in this repository.
- Names such as "bootstrap", "infrastructure", "runtime", "identity", and
  "bridge" describe the current repository-local contract, not official chezmoi
  phases.
- Trigger comments in scripts document current rendered-content inputs. They are
  not permission to edit trigger hashes as part of this documentation issue.

If official documentation is insufficient for a repository-local behavior, this
document labels the behavior as a repository-local contract rather than official
chezmoi or mise behavior.

## Repository action graph

The current action graph is:

1. Manual prerequisites exist outside chezmoi automation.
2. `.chezmoi.toml.tmpl` is evaluated as chezmoi configuration.
3. `.chezmoi.toml.tmpl` derives host and identity data, including:
   - `osid`
   - `is_wsl`
   - `windows_user`
   - `npiperelay_wsl`
   - `op_status`
   - `identities`
   - `ssh_keys_hash`
   - XDG and tool paths under `.paths`
4. `[hooks.read-source-state.pre]` runs `.bootstrap-identity.sh`.
5. `.chezmoidata/` provides static package and tool declarations.
6. `.chezmoitemplates/` provides reusable template fragments.
7. `.chezmoiexternal.toml.tmpl` declares external resources that are not
   package-manager-owned.
8. Chezmoi renders and applies source state.
9. `.chezmoiscripts/` entries run according to official chezmoi script filename
   semantics and repository-local alphabetical phase naming.
10. Some scripts delegate convergence to rendered mise file tasks under
    `dot_config/mise/tasks/**`.
11. Rendered targets expose shell, Git, SSH, WezTerm, Homebrew, mise,
    1Password, Neovim, Starship, Vale, and systemd surfaces.
12. CI validates convergence and idempotency through GitHub Actions.

## Data and template inputs

### Static `.chezmoidata/` inputs

Static repository data lives under `.chezmoidata/`:

- [`.chezmoidata/packages.yaml`](../../.chezmoidata/packages.yaml)
- [`.chezmoidata/completions.yaml`](../../.chezmoidata/completions.yaml)
- [`.chezmoidata/tools.yaml`](../../.chezmoidata/tools.yaml)

Current contract:

- `packages.yaml` is the repository-owned package data source for macOS,
  Linux, and Windows provisioning templates and scripts.
- `completions.yaml` is the repository-owned completion tool-key data source
  for static completion and init asset generation.
- `tools.yaml` is the repository-owned tool data source for generated mise
  configuration and tool-dependent script triggers.
- Static data changes can affect rendered script content when scripts include
  hashes or rendered package/tool lists.

### Dynamic template/config data

Dynamic data is produced while evaluating
[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl). It includes host-specific and
identity-specific values that are not static repository data:

- operating system and architecture
- WSL2 detection
- Windows username detection for WSL2
- `npiperelay.exe` discovery for WSL2
- Homebrew prefix selection
- mise binary path selection
- 1Password CLI path and session status
- discovered 1Password SSH Key items tagged for dotfiles
- rendered identity list
- aggregate `ssh_keys_hash`
- SSH agent socket path
- XDG path map

This dynamic data is part of the current action graph because template scripts
and rendered targets consume it directly.

### Template fragments

Reusable template fragments live under `.chezmoitemplates/`:

- [`.chezmoitemplates/git_identity_config.tmpl`](../../.chezmoitemplates/git_identity_config.tmpl)
- [`.chezmoitemplates/linux-packages.list.tmpl`](../../.chezmoitemplates/linux-packages.list.tmpl)

Current contract:

- `git_identity_config.tmpl` centralizes generated per-identity Git config
  fragments.
- `linux-packages.list.tmpl` converts package data and host OS release data into
  the package list consumed by Linux infrastructure setup.

## External resources

External resources are declared in
[`.chezmoiexternal.toml.tmpl`](../../.chezmoiexternal.toml.tmpl).

Current contract:

- External resources are limited to assets that are not managed by package
  managers.
- WSL2 receives `win32yank.exe` as an archive-file resource.
- The Catppuccin Mocha bat theme is fetched as a file resource.
- Zsh completion definitions for `eza`, Git Zsh completion, and Git Bash
  completion are fetched as file resources.
- External refresh cadence is encoded in the external-resource declarations.
- External resources participate in the rendered target graph before scripts that
  depend on those target files can observe them.

This document does not change external-resource ownership or refresh policy.

## Bootstrap and hook boundary

[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl) defines:

- `[hooks.read-source-state.pre]`
- `command = "{{ .chezmoi.sourceDir }}/.bootstrap-identity.sh"`

Current contract:

- The hook is the boundary between initial source-state reading and the
  repository bootstrap script.
- [`.bootstrap-identity.sh`](../../.bootstrap-identity.sh) is responsible for the
  current pre-source-read bootstrap behavior.
- `.chezmoi.toml.tmpl` remains responsible for dynamic data derivation after the
  bootstrap boundary is available.
- The hook and bootstrap script are behavior-sensitive because they run before
  normal script convergence.
- This document records the boundary only. It does not change bootstrap,
  1Password, mise, WSL2 relay, or identity behavior.

Official chezmoi hook semantics come from the hooks documentation. The exact
bootstrap responsibilities are repository-local behavior.

## Script execution contract

The table below classifies every current `.chezmoiscripts/*` entry.

The "phase" column is repository-local filename ordering. It is not an official
chezmoi phase model.

| Script                                                                                                                                             | Phase                         | Purpose                                                                            | Expected re-run condition                                                                                                                             | Known trigger inputs                                                                                  | Encoded trigger coverage                                                              | Idempotency mechanism                                                                                                                        | Hard-fail conditions                                                                                                                                                    | Soft-fallback conditions                                                                                               | Validation surface                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`.chezmoiscripts/run_onchange_before_00-backup-legacy-dots.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-backup-legacy-dots.sh.tmpl)     | before `00`                   | Archive legacy unmanaged dotfiles before managed targets are applied.              | Re-runs when rendered script content changes.                                                                                                         | XDG/home paths and the hardcoded legacy target list.                                                  | No explicit hash comment; rendered paths and target list are in script content.       | Checks each legacy target before moving it; creates the backup root lazily only after a target is found.                                     | Shell execution failure, backup directory creation failure, or move failure.                                                                                            | No-op when no legacy file or directory exists.                                                                         | `chezmoi init --apply`, `chezmoi verify`, local `git diff --check`, pre-commit.             |
| [`.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl) | before `00`, WSL2 only        | Install Windows-side dependencies through WinGet for WSL2 hosts.                   | Re-runs when rendered WSL2 script content changes; renders empty outside WSL2.                                                                        | `.is_wsl`, `.packages.headless.windows`, `.packages.gui.windows`, and `CI`.                           | Explicit `.chezmoidata/packages.yaml` hash comment plus rendered package list.        | Uses `winget.exe list --id` before installing each package.                                                                                  | WinGet install failure or unavailable Windows interop command on WSL2.                                                                                                  | `winget.exe source update` failure is ignored; already-installed packages are skipped; GUI packages are omitted in CI. | WSL2 local apply behavior, CI rendered empty/non-interactive paths, `chezmoi init --apply`. |
| [`.chezmoiscripts/run_onchange_before_00-validate-session.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-validate-session.sh.tmpl)         | before `00`                   | Validate 1Password session availability before identity-dependent steps.           | Re-runs when rendered script content changes, including branches driven by `op_status`.                                                               | `.op_status` and `CI`.                                                                                | No explicit hash comment; dynamic `op_status` branch is rendered into script content. | Exits early when no blocking condition is rendered.                                                                                          | Locked 1Password session outside CI.                                                                                                                                    | Missing 1Password CLI allows basic provisioning to continue; locked session is bypassed in CI.                         | `chezmoi init --apply`, `mise run doctor:identity`, `mise run doctor`.                      |
| [`.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl) | before `10`                   | Provision base system packages and shell prerequisites before runtime setup.       | Re-runs when rendered host-specific infrastructure script content changes.                                                                            | `.osid`, package data, generated Brewfile, generated Linux package list, OS release data, sudo state. | Explicit Brewfile hash on macOS; explicit generated Linux package list hash on Linux. | Homebrew install path checks; package manager install commands; shell registration and default-shell checks.                                 | Missing bootstrap binaries on macOS, non-interactive sudo failure on Linux, unsupported Linux distribution, package install failure, or missing Zsh after installation. | Existing Homebrew and already-correct shell state are accepted; empty package list skips install.                      | `chezmoi init --apply`, `chezmoi verify`, CI matrix on macOS and Ubuntu.                    |
| [`.chezmoiscripts/run_once_before_10-setup-workspace.sh.tmpl`](../../.chezmoiscripts/run_once_before_10-setup-workspace.sh.tmpl)                   | before `10`                   | Create identity-routed workspace base directories.                                 | Runs once per unique rendered content version.                                                                                                        | Dynamic `.identities`, identity directory mappings, and home path.                                    | No explicit hash comment; rendered identity directory mappings are in script content. | Uses `mkdir -p`; strips wildcard suffixes before directory creation.                                                                         | Zsh execution failure or directory creation failure.                                                                                                                    | No-op for identity mappings that render no directory work.                                                             | `chezmoi init --apply`, identity-related local apply review.                                |
| [`.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl)               | after `20`                    | Delegate runtime and ecosystem convergence to mise after target files are applied. | Re-runs when rendered runtime setup script content changes.                                                                                           | rendered mise config, `.chezmoidata/tools.yaml`, `.paths.mise`, PNPM path.                            | Explicit `dot_config/mise/config.toml.tmpl` hash and `.chezmoidata/tools.yaml` hash.  | Uses `mise install` and `mise run setup`; mise tasks own their own idempotency.                                                              | Missing non-executable mise binary, `mise install` failure, or `mise run setup` failure.                                                                                | None encoded in this script.                                                                                           | `chezmoi init --apply`, `mise run doctor`, CI convergence.                                  |
| [`.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl)   | after `21`                    | Generate static Zsh completions and init assets for shell startup.                 | Re-runs when rendered completion-generation script content changes.                                                                                   | `.chezmoidata/tools.yaml`, `.chezmoidata/completions.yaml`, mise tool identifiers, completion output commands, XDG cache paths. | Explicit `.chezmoidata/tools.yaml` hash comment; completion tool keys render from `.chezmoidata/completions.yaml`. | Creates completion/init directories, removes stale compiled completion files, regenerates static assets.                                     | Directory creation or required shell execution failure; command failures not guarded by the script's soft warning path can fail under `set -euo pipefail`.              | The `generate_comp` helper warns when a completion command fails.                                                      | `chezmoi init --apply`, `mise run doctor:completion`, `mise run doctor`.                    |
| [`.chezmoiscripts/run_onchange_after_22-bat-cache.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_22-bat-cache.sh.tmpl)                         | after `22`                    | Delegate bat theme cache convergence to mise.                                      | Re-runs when rendered script content changes, including the encoded theme hash.                                                                       | rendered Catppuccin Mocha bat theme file and `.paths.mise`.                                           | Explicit target theme file hash comment.                                              | Delegates to `mise run setup:bat`.                                                                                                           | mise missing or `setup:bat` failure.                                                                                                                                    | None encoded in this script.                                                                                           | `chezmoi init --apply`, `mise run setup:bat`, `mise run doctor` where applicable.           |
| [`.chezmoiscripts/run_onchange_after_22-vale-sync.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_22-vale-sync.sh.tmpl)                         | after `22`                    | Delegate Vale style package synchronization to mise.                               | Re-runs when rendered script content changes, including the Vale config hash.                                                                         | `dot_config/vale/vale.ini.tmpl` and `.paths.mise`.                                                    | Explicit Vale config hash comment.                                                    | Delegates to `mise run setup:vale`.                                                                                                          | mise missing or `setup:vale` failure.                                                                                                                                   | `setup:vale` skips when rendered Vale config is missing.                                                               | `chezmoi init --apply`, `mise run doctor:vale`, `mise run doctor`.                          |
| [`.chezmoiscripts/run_onchange_after_23-compile-pbfile.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_23-compile-pbfile.sh.tmpl)               | after `23`, macOS only        | Compile the native Swift clipboard bridge.                                         | Re-runs when rendered script content changes, including the Swift source hash; renders a non-operational body outside macOS.                          | `dot_local/share/pbcopy/pbfile.swift`, `.osid`, XDG data path, home path.                             | Explicit Swift source hash comment.                                                   | Compiles only when the rendered source path exists.                                                                                          | Swift compiler or `xcrun` failure on macOS when source exists.                                                                                                          | No-op when source file is absent; non-macOS branch does not compile.                                                   | macOS local apply, CI macOS matrix where toolchain is available.                            |
| [`.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl)     | after `50`                    | Converge generated public key files, Git identity includes, and `allowed_signers`. | Re-runs when rendered identity script content changes, especially `ssh_keys_hash`.                                                                    | `.identities`, `.ssh_keys_hash`, home path, XDG config/state paths, `git_identity_config.tmpl`.       | Explicit `.ssh_keys_hash` trigger comment and rendered identity content.              | Recreates generated Git identity directory, writes a temporary signers file, sorts uniquely, and writes generated outputs deterministically. | Directory creation failure, file write failure, chmod failure, or malformed rendered identity data.                                                                     | CI fallback signer is generated when no identities are mapped.                                                         | `chezmoi init --apply`, `chezmoi verify`, `mise run doctor:identity`, `mise run doctor`.    |
| [`.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl)       | after `51`, WSL2 only         | Sync the rendered 1Password SSH agent config to the Windows host.                  | Re-runs when rendered script content changes, including the rendered 1Password agent config hash; actual sync commands remain inside the WSL2 branch. | `.is_wsl`, Windows user profile path, rendered 1Password agent config path.                           | Explicit rendered 1Password agent config hash comment plus WSL2 branch and paths.     | Copies only when the WSL-side source config exists.                                                                                          | PowerShell, `wslpath`, directory creation, or copy failure on WSL2.                                                                                                     | No-op when source config does not exist; non-WSL hosts render no operation.                                            | WSL2 local apply, `mise run doctor:identity`, bridge inspection.                            |
| [`.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl)     | after `52`, WSL2 only         | Sync rendered WezTerm config to the Windows host.                                  | Re-runs when rendered WSL2 sync script content changes, including the WezTerm config hash.                                                            | `.is_wsl`, `CI`, Windows user profile path, rendered WezTerm config.                                  | Explicit `dot_config/wezterm/wezterm.lua.tmpl` hash comment.                          | Copies only when the WSL-side source config exists.                                                                                          | PowerShell, `wslpath`, directory creation, or copy failure on WSL2.                                                                                                     | Skips in CI; no-op when source config does not exist; non-WSL hosts render no operation.                               | WSL2 local apply, rendered WezTerm inspection, CI skip path.                                |
| [`.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl)             | after `90`, WSL2 service path | Enable user-level services after configuration files converge.                     | Re-runs when rendered service-management script content changes, including the bridge service hash.                                                   | `.is_wsl`, `.npiperelay_wsl`, rendered systemd user service.                                          | Explicit `dot_config/systemd/user/1password-bridge.service.tmpl` hash comment.        | Runs `systemctl --user daemon-reload` and enables the service only when WSL2 relay data is present.                                          | `systemctl --user` failure when the WSL2 service path is active.                                                                                                        | Reports that no environment-specific services are required when WSL2 relay conditions are not met.                     | WSL2 local apply, `mise run doctor:identity`, service status inspection.                    |

## Mise task boundary

The focused mise task delegation contract is documented in
[Mise task boundary](./mise-task-boundary.md).

Mise tasks in this repository are rendered file tasks under
[`dot_config/mise/tasks/`](../../dot_config/mise/tasks).

Official mise semantics used here:

- file tasks can be defined in `.config/mise/tasks`
- file tasks must be executable for mise to detect them
- grouped file-task directories create task names such as `setup:bat` and
  `doctor:nvim`
- `# [MISE]` comments are supported task metadata comments

Repository-local contract:

- `run_onchange_after_20-setup-runtimes.sh.tmpl` delegates to:
  - `mise install`
  - `mise run setup`
- The rendered `setup` task depends on:
  - `setup:security`
  - `setup:pnpm`
  - `setup:bat`
  - `setup:vale`
- `run_onchange_after_22-bat-cache.sh.tmpl` delegates directly to
  `mise run setup:bat`.
- `run_onchange_after_22-vale-sync.sh.tmpl` delegates directly to
  `mise run setup:vale`.
- CI runs:
  - `mise run integrate:nvim`
  - `mise run doctor`
- Doctor tasks are validation surfaces. They should not be treated as proof that
  unrun local validations passed.

Current task groups:

- `setup:*`: converges local setup artifacts such as permissions, pnpm global bin
  routing, bat cache, and Vale styles.
- `integrate:*`: restores application integration state, currently Neovim.
- `doctor:*`: validates health of security permissions, identity, Neovim, Vale,
  toolchain, npm backend, HubSpot CLI, and completions.
- `sync:*`: contains sync behavior such as WezTerm bridge sync.
- `update:*`: contains mutation-oriented maintenance workflow, currently
  lazy-lock update.

This document does not change task names, dependencies, descriptions, versions,
or task behavior.

## Host-specific branches

### macOS

Current macOS branches include:

- Homebrew provisioning through the generated Brewfile.
- native Swift compilation for `pbfile`.
- macOS-specific rendered WezTerm behavior.
- macOS CI validation in the GitHub Actions matrix.

### Linux

Current Linux branches include:

- package manager selection from OS release data:
  - `apt` for Ubuntu/Debian
  - `dnf` for Fedora/RHEL
  - `pacman` for Arch
- generated Linux package list from `.chezmoidata/packages.yaml`.
- default shell registration and transition to Zsh.
- Linux CI validation through Ubuntu.

### WSL2

WSL2 is a first-class supported host path in the current graph.

Current WSL2 branches include:

- WSL detection in `.chezmoi.toml.tmpl`.
- Windows username and `npiperelay.exe` discovery.
- Windows dependency provisioning through WinGet.
- `win32yank.exe` external resource handling.
- WSL-to-Windows 1Password SSH agent bridge rendering.
- SSH agent socket routing through rendered shell environment.
- Windows-host 1Password agent config sync.
- Windows-host WezTerm config sync.
- user-level systemd service enablement for the 1Password bridge when
  `npiperelay_wsl` is available.
- WSL clipboard provider behavior in rendered Neovim options.
- WSL-specific WezTerm launcher path resolution.

WSL2-specific behavior is especially behavior-sensitive because it crosses the
WSL, Windows, 1Password, SSH agent, systemd, and terminal boundaries.

### CI

Current CI branches include:

- `CI=true` in the GitHub Actions environment.
- `chezmoi init --source="$GITHUB_WORKSPACE" --apply`.
- `chezmoi verify`.
- `mise run integrate:nvim`.
- `mise run doctor`.
- CI-specific bypasses or fallback behavior in identity and desktop/GUI
  provisioning paths.

CI is a validation surface, not a complete substitute for WSL2 local validation.

## Rendered target surfaces

Current rendered target surfaces include:

- shell startup:
  - [`dot_zshenv.tmpl`](../../dot_zshenv.tmpl)
  - [`dot_config/zsh/dot_zshrc.tmpl`](../../dot_config/zsh/dot_zshrc.tmpl)
- Git and identity:
  - [`dot_config/git/config.tmpl`](../../dot_config/git/config.tmpl)
  - generated Git identity includes under XDG config
  - generated `allowed_signers`
- SSH:
  - [`dot_config/ssh/config.tmpl`](../../dot_config/ssh/config.tmpl)
  - [`dot_config/ssh/conf.d/github.tmpl`](../../dot_config/ssh/conf.d/github.tmpl)
  - [`private_dot_ssh/symlink_config.tmpl`](../../private_dot_ssh/symlink_config.tmpl)
- 1Password:
  - [`dot_config/1Password/ssh/private_agent.toml.tmpl`](../../dot_config/1Password/ssh/private_agent.toml.tmpl)
  - [`dot_config/systemd/user/1password-bridge.service.tmpl`](../../dot_config/systemd/user/1password-bridge.service.tmpl)
- mise:
  - [`dot_config/mise/config.toml.tmpl`](../../dot_config/mise/config.toml.tmpl)
  - [`dot_config/mise/tasks/`](../../dot_config/mise/tasks)
- Homebrew:
  - [`dot_config/homebrew/Brewfile.tmpl`](../../dot_config/homebrew/Brewfile.tmpl)
- Neovim:
  - [`dot_config/nvim/init.lua.tmpl`](../../dot_config/nvim/init.lua.tmpl)
  - [`dot_config/nvim/lua/config/`](../../dot_config/nvim/lua/config)
  - [`dot_config/nvim/lua/plugins/`](../../dot_config/nvim/lua/plugins)
  - [`dot_config/nvim/lazy-lock.json`](../../dot_config/nvim/lazy-lock.json)
- WezTerm:
  - [`dot_config/wezterm/wezterm.lua.tmpl`](../../dot_config/wezterm/wezterm.lua.tmpl)
  - [`dot_local/bin/symlink_wezterm.tmpl`](../../dot_local/bin/symlink_wezterm.tmpl)
- Starship:
  - [`dot_config/starship.toml.tmpl`](../../dot_config/starship.toml.tmpl)
- Vale:
  - [`dot_config/vale/vale.ini.tmpl`](../../dot_config/vale/vale.ini.tmpl)
- clipboard bridge:
  - [`dot_local/share/pbcopy/pbfile.swift`](../../dot_local/share/pbcopy/pbfile.swift)

Future refactors should inspect both source-state templates and rendered target
effects before changing these surfaces.

## CI validation surfaces

The current GitHub Actions workflow is
[`.github/workflows/compliance.yml`](../../.github/workflows/compliance.yml).

Current CI validation sequence:

1. checkout repository
2. bootstrap Tier 0 tools with `jdx/mise-action`
3. run `chezmoi init --source="$GITHUB_WORKSPACE" --apply`
4. run `chezmoi verify`
5. run `mise run integrate:nvim`
6. run `mise run doctor`

Current contract:

- `chezmoi init --apply` validates that source state can converge in CI.
- `chezmoi verify` validates idempotency of the applied source state.
- `mise run integrate:nvim` validates Neovim integration restoration.
- `mise run doctor` validates the repository-local health checks encoded as mise
  tasks.
- CI runs on Ubuntu and macOS, but does not fully exercise an interactive WSL2
  Windows-host bridge.

Documentation-only PRs should not claim CI passed until the PR's GitHub Actions
results are available.

## Follow-up candidates

These candidates may be useful after this documentation exists. They are not
requirements for issue #143 unless a future Commander decision scopes them.

- Trigger input normalization:
  - audit which dynamic inputs are intentionally encoded into rendered
    `run_onchange_` content
  - decide whether any missing trigger comments should be added in a separate
    behavior-aware PR
- Declarative data migration:
  - evaluate whether additional package, tool, or identity-adjacent constants
    should move to `.chezmoidata/`
- Mise task taxonomy:
  - clarify task group responsibilities without changing task behavior
- Bootstrap and password-manager boundary hardening:
  - separately audit `.bootstrap-identity.sh`, 1Password CLI usage, and WSL2
    relay assumptions
- WSL2 convergence contracts:
  - use [WSL2 convergence validation](./wsl2-convergence-validation.md) when
    scoping future WSL2 behavior changes
- Architecture documentation:
  - evaluate whether `ARCHITECTURE.md` should be restructured, replaced, or
    routed to this action graph document in a later PR
- Script contract testability:
  - explore read-only inspection helpers that list rendered script names,
    trigger comments, and delegated mise tasks without changing scripts

## Review checklist for future refactors

Before changing any chezmoi action graph surface, verify:

- The issue explicitly scopes the touched surface.
- The change distinguishes official chezmoi semantics from repository-local
  phase naming.
- The change does not accidentally alter `run_onchange_` or `run_once_` rendered
  content unless a rerun is intended and reviewed.
- Trigger hashes are not added, removed, or normalized without explicit scope.
- `.chezmoidata/` changes are reviewed for rendered script impact.
- `.chezmoiexternal.toml.tmpl` changes are reviewed for download, refresh, and
  host-specific behavior.
- `.chezmoi.toml.tmpl` changes are reviewed for bootstrap, 1Password, WSL2, and
  identity data impact.
- `.bootstrap-identity.sh` changes are reviewed as hook-boundary changes.
- `.chezmoiscripts/` changes preserve shell choice, phase ordering,
  idempotency, hard-fail behavior, and soft-fallback behavior.
- mise task changes preserve task names, task dependencies, task metadata,
  executable bits, and rendered behavior.
- WSL2 behavior is reviewed as a first-class path, not as generic Linux.
- Rendered target surfaces are inspected when templates change.
- Validation commands match the touched surface.
- Validation is reported only after command output, CI evidence, or explicit
  confirmation exists.

# Chezmoi data contract boundary

## Purpose

This document records the current repository-owned chezmoi data contract
boundaries for this chezmoi-managed dotfiles source-state repository.

It makes future declarative data migration and orchestration refactoring
reviewable and behavior-preserving by separating:

- official chezmoi data and template semantics
- repository-local static data contracts
- repository-local dynamic host, path, identity, 1Password, SSH, and WSL2 data
- reusable template fragment contracts
- current data consumers
- future migration candidates

This document describes current behavior; it does not declare the current data
layout to be ideal.

Use this document with the current [Chezmoi action graph](./action-graph.md),
the read-only
[Chezmoi script contract inspection](./script-contract-inspection.md) workflow,
the [Chezmoi script trigger audit](./script-trigger-audit.md), the
[Bootstrap and identity boundary](./bootstrap-identity-boundary.md), and the
[Mise task boundary](./mise-task-boundary.md).

## Scope and non-goals

This document is documentation-only and audit-only.

It covers current data ownership across:

- [`.chezmoidata/packages.yaml`](../../.chezmoidata/packages.yaml)
- [`.chezmoidata/tools.yaml`](../../.chezmoidata/tools.yaml)
- [`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl)
- [`.chezmoitemplates/git_identity_config.tmpl`](../../.chezmoitemplates/git_identity_config.tmpl)
- [`.chezmoitemplates/linux-packages.list.tmpl`](../../.chezmoitemplates/linux-packages.list.tmpl)
- [`.chezmoiexternal.toml.tmpl`](../../.chezmoiexternal.toml.tmpl)
- [`.chezmoiscripts/*`](../../.chezmoiscripts/)
- [`dot_config/mise/config.toml.tmpl`](../../dot_config/mise/config.toml.tmpl)
- [`dot_config/mise/tasks/`](../../dot_config/mise/tasks/)
- rendered Git, SSH, Homebrew, 1Password, WSL2, and shell surfaces

This document does not:

- move values into `.chezmoidata/`
- change `.chezmoidata/*`
- change `.chezmoi.toml.tmpl`
- change `.chezmoitemplates/*`
- change `.chezmoiexternal.toml.tmpl`
- change `.chezmoiscripts/*`
- change `dot_config/mise/config.toml.tmpl`
- change mise task behavior
- change package lists, tool versions, runtime versions, dependencies, or
  lockfiles
- change provisioning, bootstrap, identity, 1Password, SSH, WSL2, shell,
  Neovim, WezTerm, Starship, Git, Homebrew, mise, GitHub Actions, or CI behavior
- expose account IDs, item IDs, private key material, actual public keys,
  unfiltered `chezmoi data`, or environment dumps
- claim that documentation alone validates convergence or idempotency
- duplicate the full script table from [Chezmoi action graph](./action-graph.md)
- authorize data migration or implementation changes

## Official semantics boundary

Official chezmoi semantics used here:

- Files under `.chezmoidata/` are interpreted as structured static data in
  supported formats and are available to templates.
- Multiple `.chezmoidata/` files merge into the root data dictionary in lexical
  filesystem order.
- Dictionaries are merged; non-dictionary values, including lists, are replaced.
- `.chezmoidata/` files cannot be templates because they must be available
  before the template engine starts.
- Dynamic machine data belongs in the `data` section of the chezmoi config
  template or is read at template execution time through template functions.
- A root `.chezmoi.$FORMAT.tmpl` config template is executed before the source
  state is read.
- Chezmoi templates use Go `text/template` syntax extended with Sprig and
  chezmoi functions.
- Source-state files with a `.tmpl` suffix and files under `.chezmoitemplates/`
  are interpreted as templates.
- `.chezmoiexternal.$FORMAT{,.tmpl}` declares external source-state entries;
  `.chezmoiexternal.$FORMAT` is interpreted as a template whether or not it has
  a `.tmpl` suffix.

Official references:

- https://www.chezmoi.io/reference/special-directories/chezmoidata/
- https://www.chezmoi.io/reference/special-files/chezmoidata-format/
- https://www.chezmoi.io/user-guide/templating/
- https://www.chezmoi.io/reference/templates/
- https://www.chezmoi.io/reference/special-files/chezmoi-format-tmpl/
- https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/

Repository-local contracts used here:

- `packages.yaml` and `tools.yaml` are repository-local schema names.
- `packages`, `mise_tools`, `op_status`, `identities`, `ssh_keys_hash`,
  `paths.*`, WSL2 bridge values, and mise task taxonomy are repository-local
  contracts.
- Chezmoi does not define this repository's package taxonomy, mise tool map,
  1Password identity item conventions, SSH key metadata shape, path map, or task
  grouping semantics.
- Official documentation does not define whether the hardcoded values identified
  later should be moved to `.chezmoidata/`; those are repository-local follow-up
  candidates only.

If official chezmoi documentation does not define a behavior, this document
labels it as repository-local rather than filling the gap with community
convention.

## Repository-local data contract map

| Data boundary | Current owner | Contract type | Current role |
| --- | --- | --- | --- |
| Package selections | `.chezmoidata/packages.yaml` | Static repository data | Owns package lists consumed by Homebrew, Linux package-list generation, and WSL2 Windows dependency installation. |
| Tool versions | `.chezmoidata/tools.yaml` | Static repository data | Owns mise tool declarations and version strings consumed by rendered mise configuration and tool-dependent script triggers. |
| Host and path data | `.chezmoi.toml.tmpl` | Dynamic config data | Derives OS, architecture, WSL2, Homebrew prefix, XDG paths, mise path, and other host-local values. |
| 1Password state | `.chezmoi.toml.tmpl` | Dynamic session data | Resolves the `op` binary, session readiness, and behavior-sensitive identity discovery inputs. |
| Identity data | `.chezmoi.toml.tmpl` | Dynamic secret-adjacent data | Derives identity metadata from 1Password SSH Key item structure without storing secret material in repository data. |
| SSH routing data | `.chezmoi.toml.tmpl` | Dynamic host and identity data | Derives signing helper, SSH agent socket, key metadata hash, and generated identity records consumed by Git, SSH, and scripts. |
| Git identity fragment | `.chezmoitemplates/git_identity_config.tmpl` | Reusable template fragment | Centralizes the generated per-identity Git config shape used during identity convergence. |
| Linux package fragment | `.chezmoitemplates/linux-packages.list.tmpl` | Reusable template fragment | Converts static package data plus host OS release data into the Linux package list used by infrastructure setup. |
| External resources | `.chezmoiexternal.toml.tmpl` | Templated source-state externals | Declares non-package-manager assets and WSL2-specific external entries. |
| Mise task taxonomy | `dot_config/mise/config.toml.tmpl` and `dot_config/mise/tasks/**` | Repository-local task data and scripts | Uses rendered data to expose setup, doctor, integrate, sync, and update tasks. |

## Static .chezmoidata contracts

### `.chezmoidata/packages.yaml`

Current contract:

- Owns repository package selections under the `packages` key.
- Separates headless, GUI, and media package groups.
- Separates common, Linux distribution-specific, macOS Homebrew, macOS cask,
  and Windows package-manager entries.
- Is static repository data, not host-discovered data.
- Can affect rendered `run_onchange_` scripts when package lists or explicit
  package-data hashes render into script content.

Current consumers:

| Consumer | Current use |
| --- | --- |
| [`dot_config/homebrew/Brewfile.tmpl`](../../dot_config/homebrew/Brewfile.tmpl) | Renders macOS Homebrew brews, casks, and media package entries. |
| [`.chezmoitemplates/linux-packages.list.tmpl`](../../.chezmoitemplates/linux-packages.list.tmpl) | Renders common and distribution-specific Linux package entries. |
| [`.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl) | Installs rendered Homebrew or Linux package lists depending on host OS. |
| [`.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl) | Renders WSL2 Windows package lists and package-data hash content. |

The package schema is repository-local. Chezmoi defines how `.chezmoidata/`
becomes template data; it does not define this repository's `packages` shape,
package groups, or platform taxonomy.

### `.chezmoidata/tools.yaml`

Current contract:

- Owns repository mise tool declarations under the `mise_tools` key.
- Stores backend-qualified tool names and version strings used by rendered mise
  configuration.
- Stores Renovate metadata comments next to version declarations.
- Is static repository data, not host-discovered data.
- Can affect rendered `run_onchange_` scripts when tool declarations or explicit
  `tools.yaml` hashes render into script content.

Current consumers:

| Consumer | Current use |
| --- | --- |
| [`dot_config/mise/config.toml.tmpl`](../../dot_config/mise/config.toml.tmpl) | Renders primary runtime versions and the generated mise tools table. |
| [`.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl) | Renders a `tools.yaml` hash and delegates runtime setup through mise. |
| [`.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl) | Renders a `tools.yaml` hash for completion-generation trigger coverage. |
| [`dot_config/mise/tasks/**`](../../dot_config/mise/tasks/) | Uses rendered mise paths and tool execution surfaces after configuration exists. |

The tool schema is repository-local. Chezmoi does not define `mise_tools`, tool
backend naming, Renovate comment semantics, or this repository's runtime/tool
selection policy.

## Dynamic .chezmoi.toml.tmpl data boundary

[`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl) is the dynamic data boundary for
host, path, WSL2, 1Password, identity, and SSH-related values.

Current dynamic values include:

| Value group | Current examples | Why it is dynamic |
| --- | --- | --- |
| Host platform | `osid`, `arch`, Homebrew prefix | Depends on the current machine and architecture. |
| WSL2 bridge | `is_wsl`, `windows_user`, `npiperelay_wsl` | Depends on kernel release, Windows interop, environment, and discovered Windows commands. |
| Tool paths | `paths.op`, `paths.mise`, `paths.op_sign`, `paths.true_cmd` | Depends on installed binaries, platform-specific locations, and discovery functions. |
| XDG paths | `paths.home`, `paths.xdg_config`, `paths.xdg_data`, `paths.xdg_state`, `paths.xdg_cache` | Depends on the current user's home directory and target path layout. |
| 1Password state | `op_status` | Depends on local 1Password CLI availability and session readiness. |
| Identity records | `identities` | Derived from local 1Password SSH Key item metadata and should remain secret-adjacent. |
| SSH metadata | `ssh_keys_hash`, identity `key_hash`, `ssh_auth_sock` | Depends on discovered key metadata, host platform, and socket routing. |

Current consumers:

| Consumer surface | Dynamic data consumed |
| --- | --- |
| `.chezmoiscripts/*` | Uses `paths.*`, `osid`, `is_wsl`, `op_status`, `identities`, `ssh_keys_hash`, and WSL2 bridge values for provisioning, setup, identity convergence, bridge sync, and service enablement. |
| `.chezmoiexternal.toml.tmpl` | Uses architecture and WSL2 data to select external source-state entries. |
| `dot_config/mise/config.toml.tmpl` | Uses `mise_tools`, `paths.xdg_data`, and `paths.op` to render user-level mise configuration. |
| `dot_config/mise/tasks/**` | Uses `paths.*`, `identities`, `is_wsl`, and tool paths for setup, doctor, integrate, sync, and update tasks. |
| rendered Git surfaces | Use `paths.op_sign`, `paths.xdg_config`, `paths.home`, `identities`, and SSH key metadata for signing and scoped identity routing. |
| rendered SSH surfaces | Use `paths.xdg_config`, `paths.xdg_state`, and SSH socket data for config includes, control sockets, known-hosts paths, and agent routing. |
| rendered Homebrew surfaces | Use static package data plus dynamic host selection through infrastructure scripts. |
| rendered 1Password surfaces | Use `identities`, SSH key metadata, and WSL2 bridge data without exposing secret material. |
| rendered WSL2 surfaces | Use `is_wsl`, `npiperelay_wsl`, `paths.*`, and Windows interop-derived values for bridge config and sync behavior. |
| rendered shell surfaces | Use XDG paths, Homebrew prefix, WSL2 branches, SSH agent socket data, and mise/Python path surfaces. |

These values should not be moved to static `.chezmoidata/` as part of this
issue. Many of them are host-local, session-local, or secret-adjacent, and moving
them would change the trust and refresh boundaries.

## Reusable template fragment contracts

### `.chezmoitemplates/git_identity_config.tmpl`

Current contract:

- Owns the generated per-identity Git config fragment shape.
- Receives an explicit dictionary from the identity convergence script.
- Renders user name, email, literal SSH signing key material in Git's public-key
  format, and per-identity SSH command routing.
- Is consumed by
  [`.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl).
- Is secret-adjacent because it renders public key material and identity routing
  metadata, even though it does not store private key material.

This fragment is repository-local. Chezmoi defines `.chezmoitemplates/` template
semantics; it does not define this repository's Git identity schema.

### `.chezmoitemplates/linux-packages.list.tmpl`

Current contract:

- Owns conversion from static package data to a plain Linux package list.
- Combines `.packages.headless.common` with distribution-specific entries from
  `.packages.headless.linux`.
- Reads host OS release data from chezmoi-provided template data.
- Is consumed by the Linux branch of
  [`.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl`](../../.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl).
- Renders content that participates in the Linux infrastructure script's
  `run_onchange_` trigger behavior.

This fragment is repository-local. Chezmoi defines template execution; it does
not define this repository's package-list schema or distribution support policy.

## Data consumer map

The table below identifies current data consumers without recreating the full
action graph table.

| Consumer | Static data | Dynamic data | Fragment data | Current boundary |
| --- | --- | --- | --- | --- |
| `.chezmoiscripts/run_onchange_before_00-install-windows-deps.sh.tmpl` | `packages.headless.windows`, `packages.gui.windows` | `is_wsl`, `CI` | None | WSL2-only Windows dependency installation. |
| `.chezmoiscripts/run_onchange_before_10-setup-infrastructure.sh.tmpl` | `packages.*` through rendered Brewfile or Linux list | `osid`, binary discovery helpers | `linux-packages.list.tmpl` | Host package provisioning before runtime setup. |
| `.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl` | `mise_tools` through rendered config and hash | `paths.mise`, `paths.xdg_data`, `paths.home` | None | Runtime setup after rendered mise config exists. |
| `.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl` | `mise_tools` hash | `paths.*` | None | Completion generation from rendered tool ecosystem. |
| `.chezmoiscripts/run_once_before_10-setup-workspace.sh.tmpl` | None | `paths.home`, `identities` | None | Workspace directory creation from dynamic identity routing. |
| `.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl` | None | `paths.*`, `identities`, `ssh_keys_hash` | `git_identity_config.tmpl` | Generated SSH public-key files, Git identity configs, and allowed signers. |
| `.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl` | None | `is_wsl`, `paths.xdg_config` | None | WSL2 1Password agent config sync. |
| `.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl` | None | `is_wsl`, `paths.xdg_config` | None | WSL2 WezTerm config sync. |
| `.chezmoiscripts/run_onchange_after_90-enable-services.sh.tmpl` | None | `is_wsl`, `npiperelay_wsl` | None | WSL2 bridge service enablement. |
| `.chezmoiexternal.toml.tmpl` | None | architecture and WSL2 data | None | Non-package-manager external source-state resources. |
| `dot_config/homebrew/Brewfile.tmpl` | `packages.headless.*`, `packages.gui.*`, `packages.media.*` | Host branch selected by script/template context | None | macOS package declaration surface. |
| `dot_config/mise/config.toml.tmpl` | `mise_tools` | `paths.xdg_data`, `paths.op` | None | Rendered user-level mise settings, tools, and task config. |
| `dot_config/mise/tasks/**` | Rendered tool config indirectly | `paths.*`, `identities`, `is_wsl`, tool paths | None | Rendered setup, doctor, integrate, sync, and update task behavior. |
| `dot_config/git/config.tmpl` | None | `paths.op_sign`, `paths.xdg_config`, `identities`, identity metadata | Generated identity files from `git_identity_config.tmpl` | SSH signing and scoped Git identity routing. |
| `dot_config/ssh/config.tmpl` and `private_dot_ssh/symlink_config.tmpl` | None | `paths.xdg_config`, `paths.xdg_state`, SSH socket data | None | SSH config include, socket, and state path routing. |
| `dot_config/1Password/ssh/private_agent.toml.tmpl` | None | `identities` | None | 1Password SSH agent allowed-key surface. |
| `dot_config/systemd/user/1password-bridge.service.tmpl` | None | `is_wsl`, `npiperelay_wsl`, `paths.home` | None | WSL2 SSH agent bridge service. |
| `dot_zshenv.tmpl` and `dot_config/zsh/dot_zshrc.tmpl` | None | `paths.*`, `brew_prefix`, `osid`, `is_wsl`, `ssh_auth_sock` | None | Shell startup, XDG, PATH, Homebrew, WSL2, and SSH agent surfaces. |

## Static migration candidates

These values are future candidates only. They are not requirements for issue
#157, and migrating any of them can change rendered content, script trigger
behavior, or review boundaries.

| Candidate | Current location | Possible future owner | Review note |
| --- | --- | --- | --- |
| External resource inventory, URLs, and refresh periods | `.chezmoiexternal.toml.tmpl` | `.chezmoidata/` plus a rendering template | Would need careful review because external target names and refresh cadence affect source-state inputs. |
| Legacy dotfile backup target list | `.chezmoiscripts/run_onchange_before_00-backup-legacy-dots.sh.tmpl` | `.chezmoidata/` or a template fragment | Would affect a `run_onchange_` script and must preserve backup behavior exactly. |
| Completion generation inventory | `.chezmoiscripts/run_onchange_after_21-generate-completions.sh.tmpl` | `.chezmoidata/` or a template fragment | Would need to preserve generated file names, command selection, and trigger behavior. |
| Repeated identity output naming policy | `.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl` and `.chezmoitemplates/git_identity_config.tmpl` | Template fragment cleanup, not necessarily `.chezmoidata/` | Secret-adjacent and behavior-sensitive; should avoid storing dynamic identity data statically. |
| WSL2 sync target naming and copy destinations | WSL2 sync scripts and rendered WSL2 surfaces | Template fragment or documented constants | Must preserve Windows interop, bridge, and rendered target behavior. |
| Shell PATH segment grouping | `dot_config/zsh/dot_zshrc.tmpl` and `dot_zshenv.tmpl` | Template fragment or documented shell-path contract | Shell startup order is behavior-sensitive and should not be normalized casually. |

A future issue should decide whether each candidate belongs in `.chezmoidata/`, a
reusable template fragment, or documentation only. Do not migrate these values as
part of issue #157.

## Values that should remain dynamic

The following values should remain dynamic and should not be moved to static
`.chezmoidata/`:

- host operating system and architecture values
- WSL2 detection and Windows interop discovery
- Windows username discovery
- `npiperelay.exe` discovery and converted WSL path
- Homebrew prefix selection derived from host OS and architecture
- local binary discovery for `op`, `mise`, `op-ssh-sign`, and `true`
- XDG and home-directory paths under `paths.*`
- `op_status` and 1Password session readiness
- 1Password account and item identifiers
- identity names, emails, directory scopes, key types, public keys, and key
  hashes
- aggregate `ssh_keys_hash`
- SSH agent socket paths and WSL2 bridge socket paths
- CI-specific fallback behavior
- host OS release data used to select Linux package entries
- any value derived from local filesystem, environment, command output,
  password-manager state, or host session state

Keeping these dynamic preserves the boundary between repository-owned static
contracts and host/session/identity-specific behavior.

## Follow-up candidates

Potential follow-up issues:

1. Audit whether external resource declarations should be backed by static data
   while preserving target names, URLs, refresh cadence, and WSL2 branches.
2. Review whether legacy backup targets should become a documented static list or
   remain inline script content.
3. Review completion generation inventory for possible template-fragment or data
   extraction without changing generated completions.
4. Review identity output generation for smaller reusable fragments while
   keeping identity data dynamic and secret-adjacent.
5. Review whether WSL2 bridge constants need a dedicated boundary document or
   static contract after current behavior is fully validated.
6. Review package schema naming only after package behavior, script triggers,
   and platform support are explicitly preserved.
7. Review mise tool data shape only after runtime installation, Renovate
   tracking, and CI behavior are explicitly preserved.

Each follow-up should be behavior-preserving, separately scoped, and validated
with fresh local output before claiming success.

## Review guidance for future data changes

For future data migrations or contract edits:

- Identify whether the value is official chezmoi data, repository-local static
  data, repository-local dynamic data, or a reusable template fragment.
- Keep host, session, identity, 1Password, WSL2, path, SSH socket, and
  discovered key metadata values dynamic unless a separate issue proves a safe
  alternative.
- Treat `.chezmoidata/*` edits as behavior-sensitive when they affect rendered
  scripts, package lists, tool versions, or trigger hashes.
- Treat `.chezmoi.toml.tmpl` edits as behavior-sensitive because they can affect
  config evaluation before source state is read.
- Treat `.chezmoitemplates/*` edits as behavior-sensitive when the rendered
  fragments participate in provisioning, identity, package, or trigger behavior.
- Do not expose secret-adjacent local data while collecting evidence.
- Prefer read-only inspection output from
  [Chezmoi script contract inspection](./script-contract-inspection.md) before
  proposing migration.
- Do not claim convergence, idempotency, or GitHub Actions success from
  documentation edits alone.

# Mise task boundary

## Purpose

This document records the current repository-owned boundary between chezmoi
scripts and repository-local mise tasks for this chezmoi-managed dotfiles
source-state repository.

It is documentation-only. It does not change chezmoi script behavior, mise task
behavior, task names, task dependencies, task descriptions, executable bits,
provisioning, runtime installation, package lists, tool versions, dependencies,
lockfiles, or CI behavior.

Use this document with the current [Chezmoi action graph](./action-graph.md),
the read-only
[Chezmoi script contract inspection](./script-contract-inspection.md) workflow,
the [Chezmoi script trigger audit](./script-trigger-audit.md), the
[Bootstrap and identity boundary](./bootstrap-identity-boundary.md), the
[Chezmoi data contract boundary](./data-contract-boundary.md), the
[Mise task taxonomy](./mise-task-taxonomy.md), and the
[Mise task source drift inspection](./mise-task-source-drift-inspection.md)
workflow.

## Scope and non-goals

This document covers the current boundary between:

- [`.chezmoiscripts/*`](../../.chezmoiscripts/)
- [`.mise.toml`](../../.mise.toml)
- [`dot_config/mise/config.toml.tmpl`](../../dot_config/mise/config.toml.tmpl)
- [`dot_config/mise/tasks/setup/*`](../../dot_config/mise/tasks/setup/)
- [`dot_config/mise/tasks/doctor/*`](../../dot_config/mise/tasks/doctor/)
- [`dot_config/mise/tasks/integrate/*`](../../dot_config/mise/tasks/integrate/)
- [`dot_config/mise/tasks/sync/*`](../../dot_config/mise/tasks/sync/)
- [`dot_config/mise/tasks/update/*`](../../dot_config/mise/tasks/update/)

This document does not:

- duplicate the full script table from [Chezmoi action graph](./action-graph.md)
- rename mise tasks
- change mise task dependencies
- change mise task descriptions
- change mise task executable bits
- move logic between chezmoi scripts and mise tasks
- change `.chezmoiscripts/*`, `.mise.toml`, or
  `dot_config/mise/config.toml.tmpl`
- imply that documentation alone validates convergence or idempotency
- authorize mise task taxonomy cleanup or implementation changes

## Official semantics boundary

Official mise semantics used here:

- tasks can be defined in `mise.toml` files or as standalone shell scripts
- file tasks can live under default directories such as `.config/mise/tasks`
- file tasks must be executable for mise to detect them
- file tasks in grouped directories receive grouped task names such as
  `setup:bat` or `doctor:nvim`
- `_default` file tasks define the group-level task name
- `mise run <task>` is the explicit task invocation form suitable for scripts and
  documentation
- file tasks can carry task metadata through `# [MISE]` comments, including
  properties such as `description`, `alias`, and `depends`
- task configuration options such as `description`, `alias`, and `depends` are
  mise task metadata, not repository-local conventions

Official references:

- https://mise.jdx.dev/tasks/
- https://mise.jdx.dev/tasks/file-tasks.html
- https://mise.jdx.dev/tasks/running-tasks.html
- https://mise.jdx.dev/tasks/task-configuration.html
- https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/
- https://www.chezmoi.io/reference/special-directories/chezmoiscripts/

Official chezmoi semantics used here:

- scripts are source-state entries whose names start with `run_`
- `run_onchange_` scripts run when their rendered content changes
- template scripts are rendered before chezmoi decides whether their content has
  changed
- `before_` and `after_` filename attributes control whether scripts run before
  or after target updates
- scripts in the source-root `.chezmoiscripts/` directory run as normal scripts
  without creating a corresponding target directory

Repository-local contracts used here:

- `.mise.toml` owns the bootstrap toolchain declaration needed before rendered
  user-level mise configuration is available.
- `dot_config/mise/config.toml.tmpl` owns the rendered user-level mise tool and
  settings configuration.
- `dot_config/mise/tasks/**` owns rendered user-level mise file tasks.
- The `executable_` source-state prefix makes rendered task files executable;
  the source-state files are tracked as `100644` and this issue does not change
  those modes.
- `setup:*`, `doctor:*`, `integrate:*`, `sync:*`, and `update:*` are
  repository-local task groups, not official mise taxonomy.
- Hard-fail and soft-fallback behavior described below is visible from current
  repository task contracts, not from official mise or chezmoi semantics.

If official mise or chezmoi documentation does not define a repository-local
boundary, this document labels the boundary as repository-local rather than
filling the gap with community convention.

## Repository-local task taxonomy

Current task ownership is represented by rendered file tasks.

| Task surface | Current owner | Repository-local role |
| --- | --- | --- |
| `setup` | `dot_config/mise/tasks/setup/executable__default.tmpl` | Orchestrates setup subtasks through `depends = ["setup:security", "setup:pnpm", "setup:bat", "setup:vale"]`. |
| `setup:*` | `dot_config/mise/tasks/setup/*` | Converges local setup artifacts after runtime tools and rendered config are available. |
| `doctor` | `dot_config/mise/tasks/doctor/executable__default.tmpl` | Orchestrates repository-local health checks and exits non-zero when one or more doctor subtasks fail. |
| `doctor:*` | `dot_config/mise/tasks/doctor/*` | Performs focused health probes for security, identity, Neovim, Vale, toolchain, npm backend, HubSpot CLI, and completions. |
| `integrate:*` | `dot_config/mise/tasks/integrate/*` | Restores application integration state that is not purely static chezmoi source state. |
| `sync:*` | `dot_config/mise/tasks/sync/*` | Performs explicit synchronization workflows that copy or bridge rendered state to another surface. |
| `update:*` | `dot_config/mise/tasks/update/*` | Performs mutation-oriented maintenance workflows that can create branches, commits, or pull requests. |

The current table is descriptive, not normative. For target role boundaries
and future review criteria, see [Mise task taxonomy](./mise-task-taxonomy.md).
That taxonomy is a repository-local review model expected to evolve through
future scoped issues; it is not authorization to change tasks by itself. Use
[Mise task source drift inspection](./mise-task-source-drift-inspection.md)
when local mise task visibility needs to be compared with repository-managed
source-state ownership before changing task boundaries.

## Current delegation map

Current direct delegation from chezmoi scripts to mise commands:

| Source | Delegated command | Current boundary |
| --- | --- | --- |
| [`.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl) | `mise install` | Chezmoi owns script ordering and trigger content; mise owns tool installation from rendered configuration. |
| [`.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_20-setup-runtimes.sh.tmpl) | `mise run setup` | Chezmoi starts the setup graph after target files converge; the rendered mise task graph owns setup subtask ordering. |
| [`.chezmoiscripts/run_onchange_after_22-bat-cache.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_22-bat-cache.sh.tmpl) | `mise run setup:bat` | Chezmoi detects rendered bat theme changes; the mise task rebuilds the bat cache. |
| [`.chezmoiscripts/run_onchange_after_22-vale-sync.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_22-vale-sync.sh.tmpl) | `mise run setup:vale` | Chezmoi detects rendered Vale config changes; the mise task synchronizes Vale style packages. |

Validation-facing mise usage outside direct script delegation:

| Surface | Command | Current boundary |
| --- | --- | --- |
| [`.github/workflows/compliance.yml`](../../.github/workflows/compliance.yml) | `mise run integrate:nvim` | CI runs dynamic Neovim integration restoration after chezmoi apply and verify. |
| [`.github/workflows/compliance.yml`](../../.github/workflows/compliance.yml) | `mise run doctor` | CI runs the repository-local doctor orchestrator as the final health check. |
| Local operator workflow | `mise run integrate:nvim` | Local validation can restore Neovim plugin integration, but output is required before claiming success. |
| Local operator workflow | `mise run doctor` | Local validation can run repository health probes, but output is required before claiming success. |

This map documents current delegation only. It does not imply that every mise
task must be invoked by a chezmoi script.

## Task group responsibilities

### `setup:*`

Current responsibility: converge local setup artifacts after chezmoi has rendered
mise configuration and the runtime setup script has run `mise install`.

Current tasks:

| Task | Current responsibility |
| --- | --- |
| `setup:security` | Enforce permissions on dynamically generated SSH private-key assets when they exist. |
| `setup:pnpm` | Configure the pnpm global bin directory to the rendered XDG data path. |
| `setup:bat` | Rebuild the bat syntax cache through mise-managed `bat`. |
| `setup:vale` | Synchronize Vale external style packages when the rendered Vale config exists. |

Current orchestration:

- `setup` is defined by `dot_config/mise/tasks/setup/executable__default.tmpl`.
- `setup` depends on `setup:security`, `setup:pnpm`, `setup:bat`, and
  `setup:vale`.
- `run_onchange_after_20-setup-runtimes.sh.tmpl` runs `mise run setup`.
- `run_onchange_after_22-bat-cache.sh.tmpl` can run `setup:bat` directly after
  rendered bat theme changes.
- `run_onchange_after_22-vale-sync.sh.tmpl` can run `setup:vale` directly after
  rendered Vale config changes.

### `doctor:*`

Current responsibility: inspect repository-local health after convergence and
report actionable failures or warnings.

Current tasks:

| Task | Current responsibility |
| --- | --- |
| `doctor` | Run the selected doctor subtasks and exit non-zero if any selected subtask fails. |
| `doctor:security` | Verify and repair expected SSH-related directory permissions where directories exist. |
| `doctor:identity` | Verify 1Password session, generated Git identity bindings, and SSH agent health. |
| `doctor:nvim` | Verify Neovim lockfile and provider integration state. |
| `doctor:vale` | Verify rendered Vale configuration and style package availability. |
| `doctor:toolchain` | Verify mise availability and workstation PATH precedence signals. |
| `doctor:npm-backend` | Verify npm-backed mise tool install artifacts. |
| `doctor:hubspot` | Verify HubSpot CLI install artifacts and execution. |
| `doctor:completion` | Verify staged HubSpot CLI completion generation and Zsh loadability. |

Current orchestration:

- `doctor` is a rendered group-level file task through the `doctor/_default`
  target.
- In CI, the current orchestrator skips workstation-only HubSpot CLI diagnostics.
- The orchestrator records subtask failures and exits non-zero if any selected
  doctor subtask fails.

Doctor tasks are validation surfaces. They do not prove unrun host-specific
behavior, and they should not be treated as a substitute for local WSL2 or
interactive validation when those paths are affected.

### `integrate:*`

Current responsibility: restore application integration state that requires the
rendered toolchain rather than pure static source-state application.

Current tasks:

| Task | Current responsibility |
| --- | --- |
| `integrate:nvim` | Run headless Neovim Lazy restore through mise-managed Neovim. |

Current usage:

- CI runs `mise run integrate:nvim` after `chezmoi verify`.
- Local validation can run `mise run integrate:nvim` when Neovim integration is
  affected.

### `sync:*`

Current responsibility: perform explicit synchronization workflows that copy or
bridge rendered state after the relevant target files exist.

Current tasks:

| Task | Current responsibility |
| --- | --- |
| `sync:wezterm` | Sync rendered WezTerm configuration from WSL2 to the Windows host when not running in CI. |

Current relationship to chezmoi scripts:

- The current action graph already has a separate
  `.chezmoiscripts/run_onchange_after_52-sync-wezterm-config.sh.tmpl` path for
  WezTerm config synchronization.
- This document does not move that logic into or out of `sync:wezterm`.
- The overlap between script-level sync and `sync:*` task naming is a follow-up
  taxonomy candidate, not a change in this PR.

### `update:*`

Current responsibility: perform mutation-oriented maintenance workflows outside
normal chezmoi convergence.

Current tasks:

| Task | Current responsibility |
| --- | --- |
| `update:lazy-lock` | Update Neovim `lazy-lock.json`, promote the source-state lockfile, commit, push, and create a pull request when updates exist. |

Current contract:

- `update:lazy-lock` also declares the alias `update:lazy-lock` through task
  metadata.
- It is not invoked by `.chezmoiscripts/*` or CI compliance validation.
- It is intentionally mutation-oriented and should remain separate from normal
  convergence and doctor tasks unless a future issue explicitly changes that
  contract.

## Hard-fail and soft-fallback boundaries

Visible hard-fail boundaries:

- `run_onchange_after_20-setup-runtimes.sh.tmpl` exits non-zero when the rendered
  mise binary is not executable.
- `run_onchange_after_20-setup-runtimes.sh.tmpl` exits non-zero when
  `mise install` or `mise run setup` fails.
- `run_onchange_after_22-bat-cache.sh.tmpl` delegates with `exec` and fails when
  `setup:bat` fails.
- `run_onchange_after_22-vale-sync.sh.tmpl` delegates with `exec` and fails when
  `setup:vale` fails.
- `doctor` exits non-zero when one or more selected doctor subtasks fail.
- `doctor:*` tasks can fail when required commands, rendered files, install
  artifacts, provider checks, or configuration probes fail.
- `update:lazy-lock` exits non-zero when the working tree is dirty, GitHub CLI is
  missing, GitHub CLI authentication is unavailable, or downstream Git, Neovim,
  chezmoi, push, or PR creation commands fail.

Visible soft-fallback boundaries:

- `setup:vale` exits successfully without syncing when the rendered Vale config
  is missing.
- `sync:wezterm` exits successfully without syncing when `CI=true` in the WSL2
  branch.
- `sync:wezterm` performs no sync when the rendered WezTerm source config is
  missing.
- `doctor` skips workstation-only HubSpot CLI diagnostics in CI.
- `doctor:identity` treats an unavailable 1Password session and unresponsive SSH
  agent differently in CI than on local interactive hosts.
- Some doctor tasks emit warnings or guidance without failing when the current
  contract treats the condition as advisory.
- `update:lazy-lock` exits successfully and deletes its temporary branch when no
  plugin updates are detected.

These boundaries are source-observed contracts. They are not claims that all
host-specific convergence paths have been validated.

## Validation surfaces

Current validation-facing surfaces that use mise tasks:

- CI convergence workflow runs `mise run integrate:nvim`.
- CI convergence workflow runs `mise run doctor`.
- Local validation can run `mise run integrate:nvim`.
- Local validation can run `mise run doctor`.
- Script-specific local validation can run delegated tasks such as
  `mise run setup:bat` or `mise run setup:vale` when those surfaces are touched.

Do not claim validation passed without command output, CI evidence, or explicit
confirmation. Documentation-only changes do not validate convergence or
idempotency by themselves.

## Follow-up candidates

These candidates are outside issue #154 and are not hidden requirements for this
PR:

- Review whether the current `setup:*`, `sync:*`, and `integrate:*` boundaries
  should be renamed or regrouped.
- Review whether direct script delegation to `setup:bat` and `setup:vale` should
  remain separate from the broader `setup` orchestrator.
- Review whether `sync:wezterm` should be wired into the same boundary as the
  current WezTerm sync script or kept as a separate operator task.
- Review whether future task metadata should be represented in file-task
  metadata or rendered configuration.
- Review whether `update:lazy-lock` should keep its current alias metadata.
- Review whether doctor task warnings, guide paths, and hard failures should be
  made more uniform.
- Use [Mise task taxonomy](./mise-task-taxonomy.md) to review whether task
  names should distinguish setup, convergence, validation, repair,
  synchronization, integration, and update responsibilities more explicitly.
- Consider generating task documentation from mise only after the repository-local
  target taxonomy is stable enough for generated documentation.

Future changes in these areas can be behavior-sensitive because they may affect
chezmoi script execution, mise task resolution, CI, local validation, or
host-specific WSL2 behavior.

# Doctor and repair task boundary

## Purpose

This document audits the current repository-owned `doctor:*` mise task boundary
against the repository-local `doctor:*` and future `repair:*` taxonomy.

Use it when future issues review whether current doctor behavior should remain
validation, be split, or become an explicit repair workflow. The audit is
evidence for future scoped issues only. It does not authorize renaming,
splitting, moving, creating, deleting, or changing any task.

This document is documentation-only. It does not add a `repair:*` task, rename
or regroup any mise task, change task metadata, change executable bits, change
chezmoi scripts, change package lists, change tool or runtime versions, change
lockfiles, change provisioning, change identity or SSH behavior, change WSL2
behavior, change Neovim behavior, change GitHub Actions, or change CI behavior.

## Scope and non-goals

This document inventories current repository-owned doctor source-state tasks
under [`dot_config/mise/tasks/doctor/`](../../dot_config/mise/tasks/doctor/)
and classifies observed behavior as one or more of:

- non-mutating validation
- validation with temporary local probes
- validation with persistent local mutation
- validation with recovery or repair-adjacent behavior
- CI-specific fallback behavior
- workstation-only diagnostic behavior

This document does not:

- replace the target role definitions in [Mise task taxonomy](./mise-task-taxonomy.md)
- replace [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
  when distinguishing repository-owned source state from unmanaged local
  target-state drift
- add a `repair:*` task group
- rename, split, move, regroup, add, remove, or normalize any task
- change `doctor`, `doctor:*`, `setup`, `setup:*`, `integrate:*`, `sync:*`, or
  `update:*` behavior
- adopt, remove, rename, or normalize unmanaged local target-state tasks
- authorize WSL2 bridge, 1Password, SSH agent, or service recovery changes

## Official semantics boundary

Official mise semantics used here:

- tasks can be defined in `mise.toml` files or as standalone shell scripts
- file tasks can live under default directories such as `.config/mise/tasks`
- file tasks must be executable for mise to detect them
- file tasks in grouped directories receive grouped task names such as
  `doctor:nvim`
- `_default` file tasks define the group-level task name
- `mise run <task>` is the explicit task invocation form suitable for scripts and
  documentation
- task metadata such as `description` and `depends` is mise task configuration
  metadata

Official chezmoi semantics used here:

- the repository is source state; rendered target files are what chezmoi manages
  in the destination directory
- the `dot_config` source-state attribute maps source files into `.config` in
  the target state
- the `executable_` source-state attribute makes rendered target files
  executable
- the `.tmpl` source-state attribute marks files as templates before they render
  into target paths

Repository-local conventions used here:

- `dot_config/mise/tasks/doctor/**` is the repository-owned source-state surface
  for current doctor file tasks.
- `doctor:*` means validation and readiness checks, per
  [Mise task taxonomy](./mise-task-taxonomy.md).
- Future `repair:*` means mutation or repair actions, per
  [Mise task taxonomy](./mise-task-taxonomy.md).
- A behavior being listed as a future `repair:*` candidate is evidence for a
  later issue, not authorization to change the task in this issue.

If official mise or chezmoi documentation does not define a repository-local
ownership convention, this document labels the convention as repository-local.

## Current repository-owned doctor inventory

Current source-state inventory:

| Task | Source-state file | Current role summary |
| --- | --- | --- |
| `doctor` | [`dot_config/mise/tasks/doctor/executable__default.tmpl`](../../dot_config/mise/tasks/doctor/executable__default.tmpl) | Grouped file-task default and health-check orchestrator. |
| `doctor:security` | [`dot_config/mise/tasks/doctor/executable_security.tmpl`](../../dot_config/mise/tasks/doctor/executable_security.tmpl) | Verifies and currently enforces local SSH directory permissions. |
| `doctor:identity` | [`dot_config/mise/tasks/doctor/executable_identity.tmpl`](../../dot_config/mise/tasks/doctor/executable_identity.tmpl) | Verifies 1Password session state, identity routing, and SSH agent health. |
| `doctor:nvim` | [`dot_config/mise/tasks/doctor/executable_nvim.tmpl`](../../dot_config/mise/tasks/doctor/executable_nvim.tmpl) | Verifies Neovim lockfile state and provider health. |
| `doctor:vale` | [`dot_config/mise/tasks/doctor/executable_vale.tmpl`](../../dot_config/mise/tasks/doctor/executable_vale.tmpl) | Verifies Vale configuration and Google style package readiness. |
| `doctor:toolchain` | [`dot_config/mise/tasks/doctor/executable_toolchain.tmpl`](../../dot_config/mise/tasks/doctor/executable_toolchain.tmpl) | Verifies mise availability and workstation PATH precedence. |
| `doctor:npm-backend` | [`dot_config/mise/tasks/doctor/executable_npm-backend.tmpl`](../../dot_config/mise/tasks/doctor/executable_npm-backend.tmpl) | Verifies npm backend install artifacts and package metadata for the HubSpot CLI tool. |
| `doctor:hubspot` | [`dot_config/mise/tasks/doctor/executable_hubspot.tmpl`](../../dot_config/mise/tasks/doctor/executable_hubspot.tmpl) | Verifies HubSpot CLI install artifacts and execution. |
| `doctor:completion` | [`dot_config/mise/tasks/doctor/executable_completion.tmpl`](../../dot_config/mise/tasks/doctor/executable_completion.tmpl) | Verifies staged HubSpot completion generation with temporary local probes. |

Use [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
before treating locally visible doctor tasks as repository-owned source state.
Local `mise tasks ls` output alone is visibility evidence, not ownership
evidence.

## Orchestrator boundary

`doctor` is a grouped file-task default. It currently orchestrates selected
`doctor:*` tasks through `mise run`.

The current orchestrated task list includes:

- `doctor:security`
- `doctor:identity`
- `doctor:nvim`
- `doctor:vale`
- `doctor:toolchain`

Outside CI, `doctor` also includes workstation-only diagnostics:

- `doctor:npm-backend`
- `doctor:hubspot`
- `doctor:completion`

In CI, `doctor` skips the workstation-only HubSpot CLI diagnostics and reports
that skip explicitly. This is CI-specific fallback behavior. It should remain in
`doctor` because it preserves a single health-check entry point while avoiding
workstation-only HubSpot diagnostics in automation.

## Classification matrix

| Task | Classification | Future `repair:*` candidate? | Rationale |
| --- | --- | --- | --- |
| `doctor` | non-mutating validation; CI-specific fallback behavior; workstation-only diagnostic orchestration | No | The default task orchestrates selected checks and records CI skip behavior. It does not directly repair state. |
| `doctor:security` | validation with persistent local mutation | Yes | It currently runs `chmod 700` on existing SSH-related directories. Permission enforcement mutates local target state and is repair-like, but this issue must not change it. |
| `doctor:identity` | non-mutating validation; CI-specific fallback behavior; validation with recovery or repair-adjacent behavior | Yes, for the WSL2 bridge recovery branch only | It validates 1Password session state, generated identity routing, and SSH agent responsiveness. In CI it softens locked 1Password and unresponsive SSH agent states. Outside CI, on WSL2, it may restart `1password-bridge.service` while attempting recovery. |
| `doctor:nvim` | non-mutating validation; CI-specific fallback behavior | No | It validates lockfile synchronization and provider readiness. Non-CI lockfile drift can fail the task, but the task points to `update:lazy-lock` rather than mutating the lockfile itself. |
| `doctor:vale` | non-mutating validation | No | It validates Vale configuration and the presence of the Google style package. Missing styles are routed to setup or manual `vale sync`, not repaired by this task. |
| `doctor:toolchain` | non-mutating validation; CI-specific fallback behavior; workstation-only diagnostic behavior | No | It validates the hermetic mise binary and checks workstation PATH precedence outside CI. PATH guidance is diagnostic and does not mutate shell configuration. |
| `doctor:npm-backend` | non-mutating validation; workstation-only diagnostic behavior | No | It validates npm backend recognition, install directory presence, artifact presence, and package metadata. It gives setup guidance but does not install or repair artifacts. |
| `doctor:hubspot` | non-mutating validation; workstation-only diagnostic behavior | No | It validates HubSpot CLI install artifacts and execution through mise. It gives install guidance but does not mutate package state. |
| `doctor:completion` | validation with temporary local probes; workstation-only diagnostic behavior | No | It creates a temporary directory and file with `mktemp`, removes them through a cleanup trap, probes completion generation, and checks Zsh loadability. The temporary probe is not persistent local mutation. |

## Future repair candidates

The following current behaviors are future `repair:*` candidates only. They must
remain unchanged until a separately scoped issue authorizes a behavior-preserving
split, migration, or rename.

### `doctor:security` permission enforcement

`doctor:security` currently runs `chmod 700` on existing SSH-related directories.
That persistent local mutation is repair-like because it changes permissions in
local target state.

A future issue may consider whether this should remain in `doctor:security`,
move to a future `repair:security`, or split into validation plus repair. That
future issue must preserve behavior unless it explicitly scopes a behavior
change, and it must validate permission behavior with local evidence.

### `doctor:identity` WSL2 bridge recovery

`doctor:identity` currently attempts SSH agent recovery outside CI. On WSL2, it
may restart `1password-bridge.service` before retrying `ssh-add -l`.

This behavior is recovery or repair-adjacent because it may change local service
state while running under a doctor task. WSL2 bridge recovery is
behavior-sensitive. Future discussion must use
[WSL2 convergence validation](./wsl2-convergence-validation.md) and must not rely
on CI as proof of local WSL2 convergence.

## Behavior that should remain in `doctor:*`

The following behavior intentionally fits the current `doctor:*` boundary:

- Read-only validation of configured tools, generated artifacts, providers,
  package metadata, and command execution readiness.
- CI fallback behavior that avoids local interactive or workstation-only checks
  while preserving automation-safe health reporting.
- Workstation-only diagnostics for HubSpot CLI readiness, because the current
  orchestrator already skips them in CI and they do not install or modify the
  tool.
- Temporary completion probes that are removed by a cleanup trap and do not
  leave persistent target-state changes.
- Failure on non-CI Neovim lockfile drift, because the task reports drift and
  routes mutation to `update:lazy-lock` rather than updating the lockfile itself.

Keeping these behaviors in `doctor:*` preserves the taxonomy distinction:
validation and readiness checks belong in `doctor:*`, while explicit state repair
or persistent local mutation belongs in a future separately scoped `repair:*`
workflow if the repository decides to create one.

## Future issue requirements

A future task split, rename, regrouping, or migration must be scoped separately.
Before changing current doctor behavior, that issue should:

1. identify the current task name, source-state file, rendered target path, and
   local mise visibility evidence;
2. use [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
   before treating local task visibility as repository-owned state;
3. state whether the behavior is validation, temporary probe, persistent
   mutation, recovery, CI fallback, or workstation-only diagnostic behavior;
4. explain why the target group better matches the task's primary role;
5. list every script, task dependency, alias, CI command, documentation
   reference, and operator command affected by the change;
6. preserve behavior unless the issue explicitly scopes a behavior change;
7. route WSL2 bridge recovery questions through
   [WSL2 convergence validation](./wsl2-convergence-validation.md);
8. include rollback guidance for restoring the previous doctor behavior; and
9. back behavior preservation claims with command output, CI evidence, or
   explicit maintainer confirmation.

## Review checklist

Before approving a future doctor or repair boundary change, verify:

- the issue explicitly scopes the task split, rename, regrouping, migration, or
  behavior change
- current repository-owned source-state evidence was separated from unmanaged
  local target-state drift
- persistent local mutation was not hidden behind validation-only wording
- temporary local probes were not misclassified as persistent mutation
- CI fallback behavior was not treated as proof of local workstation or WSL2
  convergence
- WSL2 service recovery was reviewed as WSL2 bridge behavior, not as generic
  Linux behavior
- affected docs, scripts, task metadata, dependencies, operator commands, and CI
  surfaces were reviewed
- validation evidence matches the touched surface
- this audit was not treated as authorization to create `repair:*` tasks or
  change existing `doctor:*` behavior

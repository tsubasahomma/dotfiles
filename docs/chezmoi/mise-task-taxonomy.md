# Mise task taxonomy

## Purpose

This document defines the repository-local target taxonomy for mise task groups
in this chezmoi-managed dotfiles source-state repository.

Use it when future issues review whether a repository-owned mise task should
stay in its current group, move to another group, split into multiple tasks, or
receive a new name. The taxonomy is a review model for future scoped work. It is
expected to evolve as the repository's task ownership, validation boundaries,
and source-drift evidence become clearer.

This document is documentation-only. It does not add, remove, rename, regroup,
execute, or authorize changing any mise task. It does not change chezmoi scripts,
mise task behavior, task metadata, executable bits, package lists, tool versions,
runtime versions, dependencies, lockfiles, provisioning, identity, 1Password,
SSH, WSL2, shell startup, Neovim, WezTerm, Starship, Git, Homebrew, GitHub
Actions, or CI behavior.

## Scope and non-goals

This document covers repository-local intended roles for these target task
groups:

- `setup:*`
- `converge:*`
- `doctor:*`
- `repair:*`
- `integrate:*`
- `sync:*`
- `update:*`

This document does not:

- declare the current task layout to be ideal or final
- create a `converge:*` or `repair:*` task group
- rename, regroup, split, merge, add, remove, or normalize any task
- change `setup`, `setup:*`, `doctor`, `doctor:*`, `integrate:*`, `sync:*`, or
  `update:*` behavior
- change task descriptions, aliases, dependencies, executable bits, or task
  metadata
- adopt, remove, rename, or normalize unmanaged local target-state tasks
- replace [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
  when classifying local task visibility
- authorize implementation work without a separately scoped issue

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
- `mise tasks ls`, `mise tasks info`, and `mise tasks deps` inspect task
  visibility, metadata, and dependency graphs
- task metadata such as `description`, `alias`, and `depends` is mise task
  configuration metadata

Official chezmoi semantics used here:

- the repository is source state; rendered target files are what chezmoi manages
  in the destination directory
- the `dot_config` source-state attribute maps source files into `.config` in
  the target state
- the `executable_` source-state attribute makes rendered target files
  executable
- the `.tmpl` source-state attribute marks files as templates before they render
  into target paths
- `chezmoi managed` lists target-state entries managed by the current chezmoi
  source state

Repository-local conventions used here:

- `dot_config/mise/tasks/**` is the repository-owned source-state surface for
  rendered user-level mise file tasks.
- `setup:*`, `converge:*`, `doctor:*`, `repair:*`, `integrate:*`, `sync:*`, and
  `update:*` are repository-local taxonomy groups, not official mise taxonomy.
- A task group name expresses the task's primary maintenance role in this
  repository; it does not replace official mise task metadata.
- Taxonomy decisions must be grounded in repository-owned source-state evidence,
  not unmanaged local target-state drift.

If official mise or chezmoi documentation does not define a repository-local
ownership convention, this document labels the convention as repository-local.

## Target task group roles

### `setup:*`

Target role: initial post-render setup only.

Use `setup:*` for tasks that prepare the local environment after chezmoi renders
source state and after required tools are available. A setup task may install or
initialize supporting local artifacts when that action is part of first-time or
post-render provisioning.

A future issue should avoid putting repeated generated artifact convergence in
`setup:*` when the task is safe and meaningful to rerun independently after the
initial setup phase. Such work is a candidate for `converge:*`.

### `converge:*`

Target role: idempotent generated artifact or cache convergence.

Use `converge:*` for tasks whose primary purpose is to make generated local
artifacts match the current source state or tool inputs. A converge task should
be safe to rerun and should not be limited to first-time setup.

Examples of candidate responsibilities include cache rebuilds, generated support
files, or other deterministic local artifacts. This document does not create
those tasks. Moving existing work into `converge:*` requires a separate issue.

### `doctor:*`

Target role: validation and readiness checks.

Use `doctor:*` for tasks that inspect current state, report readiness, and exit
non-zero when a required condition is not met. A doctor task should prefer
non-mutating diagnostics and actionable guidance.

A future issue should avoid putting repair or state-changing recovery actions in
`doctor:*` unless the issue explicitly preserves and documents the current
behavior. When a task needs to mutate local state to fix a problem, it is a
candidate for `repair:*` or for being split into `doctor:*` plus `repair:*`.

### `repair:*`

Target role: mutation or repair actions.

Use `repair:*` for tasks whose primary purpose is to change local state to
recover from drift, broken permissions, stale generated artifacts, or other
repairable local conditions.

A repair task should be explicit about the state it mutates and should not be
hidden behind validation-only naming. This document does not create a
`repair:*` group. Moving existing recovery behavior into `repair:*` requires a
separate behavior-preserving issue with validation evidence.

### `integrate:*`

Target role: application integration restoration.

Use `integrate:*` for tasks that restore application-level integration state
that is not represented as static chezmoi source state alone. These tasks bridge
repository-owned configuration with tool-managed application state.

A future issue should distinguish integration restoration from general setup,
validation, or update workflows before renaming or regrouping a task.

### `sync:*`

Target role: cross-surface synchronization.

Use `sync:*` for tasks that copy, bridge, or synchronize rendered state across
surfaces, such as from WSL2 to the Windows host, from source-controlled rendered
state to a companion runtime surface, or between related local configuration
surfaces.

A sync task should make the source and destination surfaces explicit. If the
workflow repairs local state rather than synchronizing across surfaces, it is a
candidate for `repair:*` instead.

### `update:*`

Target role: local or automated maintenance workflows.

Use `update:*` for tasks that intentionally update repository-managed state,
refresh dependency or lockfile state, create branches, create commits, or open
pull requests.

An update task may be mutation-oriented by design, but it should include safety
checks that prevent mixing unrelated local work with generated updates. Future
automation should keep update workflows separate from setup, validation, and
repair naming.

## Decision questions for future task ownership

Before renaming, regrouping, or splitting a task, a future issue should answer:

1. What state does the task read?
2. What state does the task mutate, if any?
3. Is the task primarily first-time setup, repeated convergence, validation,
   repair, integration restoration, cross-surface synchronization, or update
   automation?
4. Is the task safe to rerun independently after initial setup?
5. Does the task need to run from a chezmoi script phase, a manual operator
   command, CI, or more than one entry point?
6. Does the task have repository source-state evidence under
   `dot_config/mise/tasks/**`?
7. Does `chezmoi managed` show a corresponding managed rendered target path?
8. Does local `mise tasks ls` visibility match repository-owned source state, or
   is there unmanaged local target-state drift?
9. Would a rename change user-facing commands, script delegation, task
   dependencies, task metadata, aliases, CI, or local validation behavior?
10. Which validation evidence proves that behavior was preserved?

## Review criteria for renaming or regrouping

Future task renaming or regrouping requires a separately scoped issue. That
issue should be behavior-preserving unless it explicitly scopes a behavior
change.

A reviewable task ownership issue should:

- identify the current task name, source-state file, rendered target path, and
  local mise visibility evidence
- use [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
  before treating local task visibility as repository-owned state
- state the current task role and the proposed target role
- explain why the proposed group better matches the primary task responsibility
- list every script, task dependency, alias, CI command, documentation reference,
  and operator command affected by the rename or regrouping
- preserve task behavior unless the issue explicitly scopes a behavior change
- keep validation tasks separate from mutation or repair tasks unless the current
  behavior is intentionally preserved and documented
- keep initial post-render setup separate from repeated idempotent convergence
- avoid adopting or deleting unmanaged local target-state tasks as incidental
  cleanup
- include rollback guidance for restoring the previous task name or grouping

## Source drift evidence requirement

Taxonomy decisions must not rely on `mise tasks ls` alone. Local mise visibility
can include unmanaged target-state tasks that are not owned by the current
chezmoi source state.

Use [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
to compare:

- repository source-state task files under `dot_config/mise/tasks/**`
- rendered target task paths reported by `chezmoi managed`
- locally visible tasks reported by `mise tasks ls`
- selected task metadata from `mise tasks info`
- selected dependency graphs from `mise tasks deps`

A task visible locally without source-state and managed-target evidence should be
reported as unmanaged local target-state drift, not adopted as taxonomy scope.

## Review checklist

Before approving a future taxonomy-driven task change, verify:

- the issue explicitly scopes the task rename, regrouping, split, or migration
- the task's primary role matches the proposed target group
- validation-only work is not hidden behind mutation or repair behavior
- mutation or repair behavior is not hidden behind validation-only naming
- first-time setup is separated from repeated idempotent convergence where the
  distinction affects future ownership
- source-state, managed-target, and local visibility evidence were compared
- unmanaged local target-state drift was reported without adopting or deleting it
- affected scripts, task metadata, aliases, dependencies, CI, and documentation
  were reviewed
- behavior preservation claims are backed by command output, CI evidence, or
  explicit confirmation
- the change does not treat this taxonomy document as authorization to make
  unscoped behavior changes

# Mise surface capsule

## Purpose

Use this capsule when work touches or cites mise configuration, file tasks, task
metadata, task grouping, doctor checks, or repair-adjacent behavior.

Keep task guidance compact and behavior-preserving. Inspect current task source
state and command output for detailed behavior claims.

## Predictable LLM failure modes

- Treating `mise tasks ls` output as proof that a task is repository-owned
  source state.
- Renaming, regrouping, splitting, or deleting tasks as incidental documentation
  cleanup.
- Changing `# [MISE]` metadata, aliases, dependencies, executable bits, or task
  descriptions without explicit issue scope.
- Hiding persistent local mutation behind validation-only `doctor:*` wording.
- Creating `converge:*` or `repair:*` tasks because prior discussion treated
  them as future taxonomy candidates.
- Running or recommending broad repair commands when the active issue is
  documentation-only.

## Behavior-sensitive boundaries

Repository-owned mise task source state lives under `dot_config/mise/tasks/**`
and renders into local task visibility through chezmoi attributes and templates.
Local task visibility can also include unmanaged target-state drift, so source
state, managed target paths, and local visibility must be separated before
ownership claims.

Treat these as behavior-sensitive unless explicitly scoped:

- `.mise.toml`, tool declarations, runtime versions, tool versions, and
  lockfiles;
- `dot_config/mise/tasks/**` names, grouping, metadata, dependencies, aliases,
  executable bits, and command bodies;
- `doctor:*` validation and recovery behavior;
- setup, integration, sync, update, and future repair taxonomy boundaries;
- script delegation from `.chezmoiscripts/**` into `mise run <task>`.

## Evidence and routing links

- [Repository operating contract](../../repo.md)
- [Chezmoi surface capsule](./chezmoi.md)
- [`dot_config/mise/tasks/`](../../../../dot_config/mise/tasks/)
- [`dot_config/mise/tasks/doctor/`](../../../../dot_config/mise/tasks/doctor/)
- [`.mise.toml`](../../../../.mise.toml)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from the [Repository operating contract](../../repo.md).

If a change touches task source state, task metadata, task behavior, tool
resolution, health-check behavior, versions, dependencies, or lockfiles, route to
mise-specific validation. Consider `mise tasks info`, `mise tasks deps`,
`mise run <task>`, `mise run doctor`, rendered-output inspection, and CI evidence
according to the changed surface.

## Out of scope

This capsule does not authorize task renames, regrouping, metadata changes,
`doctor:*` behavior changes, `repair:*` creation, dependency changes, lockfile
changes, or adoption of unmanaged local target-state tasks.

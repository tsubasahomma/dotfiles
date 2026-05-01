# Thin chezmoi phase gate rules

## Purpose

This document defines repository-local implementation rules for future issues
that make `.chezmoiscripts/*` thinner while preserving chezmoi phase ordering,
trigger-sensitive rendered content, and behavior-sensitive host boundaries.

Use it when a future scoped issue proposes moving direct implementation logic
from a chezmoi script into a mise task, adding delegation to an existing mise
task, or reviewing whether script logic should remain at the chezmoi phase
boundary.

This document is documentation-only. It does not authorize thinning, rewriting,
renaming, adding, removing, or regrouping any `.chezmoiscripts/*` file. It does
not authorize adding, removing, normalizing, or relabeling trigger hashes. It
does not authorize creating, renaming, splitting, regrouping, or changing mise
tasks. It does not change provisioning, identity, 1Password, SSH, WSL2, shell
startup, Neovim, WezTerm, Starship, Git, Homebrew, mise, GitHub Actions, or CI
behavior.

## Scope and non-goals

This document defines review rules for future script-thinning issues across:

- phase ordering encoded by script filenames
- trigger-sensitive rendered script content
- host-specific rendered branches
- phase-local precondition checks
- explicit delegation from chezmoi scripts to mise tasks
- behavior-sensitive bootstrap, identity, WSL2, shell, provisioning, sync, and CI
  boundaries

This document does not:

- replace [Chezmoi action graph](./action-graph.md)
- replace [Chezmoi script contract inspection](./script-contract-inspection.md)
  or [Chezmoi script trigger audit](./script-trigger-audit.md)
- replace [Mise task boundary](./mise-task-boundary.md),
  [Mise task taxonomy](./mise-task-taxonomy.md), or
  [Mise task source drift inspection](./mise-task-source-drift-inspection.md)
- replace [Doctor and repair task boundary](./doctor-repair-task-boundary.md)
- replace [WSL2 convergence validation](./wsl2-convergence-validation.md)
- declare the current script layout ideal or final
- move any implementation logic from `.chezmoiscripts/*` to mise tasks
- add `converge:*` or `repair:*` tasks
- change task descriptions, aliases, dependencies, executable bits, or metadata
- adopt, remove, or normalize unmanaged local target-state tasks
- treat CI as proof of local WSL2 convergence

## Official semantics boundary

Official chezmoi semantics used here:

- Chezmoi scripts are source-state entries whose names start with `run_`.
- `run_` scripts run every time `chezmoi apply` runs.
- `run_onchange_` scripts run only when their rendered content has changed since
  the last successful run.
- `run_once_` scripts run once for each unique rendered content version.
- For template scripts, chezmoi evaluates the template before deciding whether
  the rendered script content has changed.
- Scripts are executed in alphabetical order, with `before_` and `after_`
  filename attributes controlling whether they run before or after target
  updates.
- Scripts in the source-root `.chezmoiscripts/` directory run as normal scripts
  without creating a corresponding target directory.
- A template script that renders to only whitespace or an empty string is not
  executed.
- Hooks are separate from scripts. Hooks run before or after configured events
  and should be fast and idempotent.
- The repository is source state. Rendered target files are what chezmoi manages
  in the destination directory.
- The `.tmpl` source-state attribute marks files as templates before they render
  into target paths.

Official mise semantics used here:

- tasks can be defined in `mise.toml` files or as standalone shell scripts
- file tasks can live under default directories such as `.config/mise/tasks`
- file tasks must be executable for mise to detect them
- file tasks in grouped directories receive grouped task names such as
  `setup:bat` and `doctor:nvim`
- `_default` file tasks define the group-level task name
- `mise run <task>` is the explicit task invocation form suitable for scripts and
  documentation
- task metadata such as `description`, `alias`, and `depends` is mise task
  configuration metadata

Official references:

- https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/
- https://www.chezmoi.io/reference/special-directories/chezmoiscripts/
- https://www.chezmoi.io/user-guide/templating/
- https://www.chezmoi.io/reference/templates/
- https://www.chezmoi.io/reference/configuration-file/hooks/
- https://www.chezmoi.io/reference/source-state-attributes/
- https://www.chezmoi.io/reference/target-types/
- https://mise.jdx.dev/tasks/
- https://mise.jdx.dev/tasks/file-tasks.html
- https://mise.jdx.dev/tasks/running-tasks.html
- https://mise.jdx.dev/tasks/task-configuration.html

Repository-local conventions used here:

- Phase numbers such as `00`, `10`, `20`, `50`, and `90` are filename ordering
  conventions in this repository, not official chezmoi phases.
- A thin phase gate is a repository-local design rule for future refactoring,
  not an official chezmoi object.
- `dot_config/mise/tasks/**` is the repository-owned source-state surface for
  rendered user-level mise file tasks.
- `setup:*`, `converge:*`, `doctor:*`, `repair:*`, `integrate:*`, `sync:*`, and
  `update:*` are repository-local taxonomy groups, not official mise taxonomy.
- Trigger hash comments document current rendered-content inputs. They are not
  permission to edit trigger hashes as part of script thinning.

If official mise or chezmoi documentation does not define a repository-local
ownership, phase, taxonomy, or delegation convention, this document labels that
convention as repository-local.

## Thin phase gate ownership

A thin `.chezmoiscripts/*` phase gate should own only the behavior that must stay
at the chezmoi script boundary.

A future thin phase gate may own:

- phase ordering encoded by the script filename, including `before_`, `after_`,
  phase number, and alphabetical ordering
- official chezmoi run semantics encoded by `run_`, `run_once_`, or
  `run_onchange_`
- rendered content that intentionally controls `run_onchange_` or `run_once_`
  decisions
- host-specific rendered branches that affect whether the script renders,
  whether it runs, what it delegates to, or which preconditions it enforces
- phase-local precondition checks that must happen before later target files,
  tools, identity state, shell startup, or services can be trusted
- hard-fail and soft-fallback behavior that protects the phase boundary
- explicit delegation to an existing mise task when the delegated task already
  owns the reusable implementation logic
- minimal environment preparation required for the delegated command to run in
  that phase

A thin phase gate should avoid owning reusable implementation details when those
details can be moved to a separately scoped mise task without changing rendered
script content, trigger behavior, host behavior, or operator commands.

Current scripts may be used as evidence and examples, but the current layout is
not a final design mandate.

## Future mise delegation candidates

Mise tasks are the preferred home for reusable implementation, validation,
integration, synchronization, repair, convergence, and update workflows only when
a later issue explicitly scopes that migration.

Future separately scoped issues may consider moving these responsibilities out of
`.chezmoiscripts/*` when behavior can be preserved:

- reusable implementation logic
- repeatable convergence logic
- validation and readiness checks
- repair or recovery actions
- cross-surface synchronization logic
- local or automated update and maintenance workflows
- generated artifact or cache convergence that is safe to rerun independently
- operator-facing workflows that should also be runnable outside `chezmoi apply`

Before delegating more behavior to mise, future issues should use
[Mise task taxonomy](./mise-task-taxonomy.md) to classify the target role and
[Mise task source drift inspection](./mise-task-source-drift-inspection.md) to
separate repository-owned task source state from unmanaged local target-state
visibility.

This document does not create `converge:*` or `repair:*` tasks and does not
rename existing `setup:*`, `doctor:*`, `integrate:*`, `sync:*`, or `update:*`
tasks.

## Criteria for keeping logic in a chezmoi script

Keep logic in a chezmoi script when the logic must run at the script phase
boundary and moving it to mise would change behavior, availability, or review
semantics.

Logic should generally stay in a chezmoi script when it:

- must run before mise exists, before the rendered mise configuration is
  available, or before the mise binary path can be trusted
- must run before shell startup converges or before the user's normal shell
  environment exists
- must run before identity state, 1Password session state, SSH agent state, or
  signing state is available
- must run before target files exist or before later target files can be safely
  trusted
- directly protects `before_` or `after_` phase ordering
- directly controls whether the script renders, runs, skips, hard-fails, or
  soft-falls back on a specific host path
- must encode trigger-sensitive rendered content for `run_onchange_` or
  `run_once_` semantics
- must preserve POSIX, Zsh, WSL2, macOS, Linux, or CI execution behavior that is
  specific to that phase
- would require changing package provisioning, bootstrap, identity, SSH, WSL2,
  shell startup, or CI behavior to delegate safely

A future issue may still delegate some of this behavior, but only when it
explicitly scopes the behavior change or proves behavior preservation with
rendered-output and runtime evidence appropriate to the touched surface.

## Trigger hash preservation rules

Trigger hashes are behavior-sensitive because `run_onchange_` scripts are keyed
by rendered script content. Adding, removing, relabeling, or normalizing a hash
comment can change the rendered content and cause a rerun even when the shell
commands appear equivalent.

Future script-thinning issues must follow these rules:

- Do not add trigger hashes unless the issue explicitly scopes that trigger
  change.
- Do not remove trigger hashes unless the issue explicitly scopes that trigger
  change.
- Do not normalize trigger hash labels, capitalization, wording, or placement
  unless the issue explicitly scopes that trigger change.
- Do not reformat trigger comments as incidental cleanup.
- Preserve rendered trigger content unless the child issue explicitly scopes a
  behavior change.
- Treat template whitespace around trigger comments as rendered-output-sensitive.
- Review implicit rendered inputs even when no explicit hash comment exists.
- Use [Chezmoi script trigger audit](./script-trigger-audit.md) before claiming a
  trigger behavior was preserved.

A future PR may intentionally change trigger content only when the linked issue
names that behavior, explains the rerun impact, and validates the rendered
script content before and after the change.

## Behavior-sensitive script families

Future script-thinning issues require extra caution when they touch or depend on
these script families:

- bootstrap and hook-adjacent paths
- 1Password session validation
- identity convergence and generated identity routing
- SSH agent, SSH signing, and scoped Git identity behavior
- WSL2 bridge and Windows interop behavior
- shell startup and environment setup
- package provisioning and package-manager bootstrap behavior
- WezTerm Windows sync and cross-surface configuration copying
- CI fallback behavior and automation-safe skips

These families can affect local workstation convergence, target-state safety,
secret-adjacent routing, or host-specific availability. Use
[Bootstrap and identity boundary](./bootstrap-identity-boundary.md),
[WSL2 convergence validation](./wsl2-convergence-validation.md), and
[Chezmoi data contract boundary](./data-contract-boundary.md) when the touched
surface overlaps their contracts.

Do not treat CI as proof of local WSL2, 1Password, SSH agent, Windows interop,
systemd user service, WezTerm sync, or shell-startup convergence.

## Validation expectations for future thinning issues

Validation must match the touched surface. Documentation-only PRs can use normal
documentation validation, but script-thinning PRs need rendered-output and
behavior evidence for the changed phase boundary.

Future documentation-only changes should include:

- `git diff --check`
- `pre-commit run --all-files`
- Markdown relative link validation when Markdown links change
- `repomix` after the documentation update is complete

Future script-thinning issues should additionally consider:

- current source-state inspection of every touched `.chezmoiscripts/*` file
- rendered-output inspection for the touched host paths
- before-and-after review of rendered `run_onchange_` or `run_once_` content
- trigger audit review for explicit and implicit trigger inputs
- `chezmoi execute-template` for touched templates when rendered output matters
- `chezmoi diff` or `chezmoi apply` only when the issue requires target-state or
  local convergence evidence
- `mise tasks info`, `mise tasks deps`, or `mise run <task>` when delegation or
  task metadata changes
- `mise run doctor` when setup, toolchain, rendered config, task behavior, or
  health-check behavior changes
- local WSL2 validation when WSL2 bridge, Windows interop, systemd user service,
  SSH agent bridge, or Windows sync behavior changes or is required for the PR
- GitHub Actions CI evidence after PR creation when automation behavior is
  claimed

Do not claim validation passed without command output, CI evidence, or explicit
maintainer confirmation.

## Review checklist

Before approving a future script-thinning issue, verify:

- the issue explicitly scopes the script edit, delegation, trigger change, task
  change, or behavior change
- the PR does not treat this document as authorization to change scripts or tasks
- the touched script's phase ordering and run semantics are preserved unless the
  issue explicitly scopes a behavior change
- rendered `run_onchange_` and `run_once_` content is reviewed before and after
  the change
- trigger hashes are not added, removed, relabeled, normalized, or reformatted as
  incidental cleanup
- host-specific rendered branches are reviewed for each affected host path
- precondition checks that must happen at the chezmoi phase boundary remain in
  the script
- any delegated mise task already exists or is created only by the same explicit
  issue scope
- mise delegation follows the repository-local task taxonomy and source drift
  inspection workflow
- behavior-sensitive bootstrap, 1Password, identity, SSH, WSL2, shell,
  provisioning, WezTerm, and CI surfaces receive focused validation
- CI is not used as proof of local WSL2 convergence
- generated Repomix output is treated as read-only evidence
- rollback guidance explains how to restore the previous phase gate behavior
- validation claims are backed by command output, CI evidence, or explicit
  maintainer confirmation

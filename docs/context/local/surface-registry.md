# Local surface registry

## Purpose

Use this registry to route future dotfiles surface capsule work without creating
full capsules in this issue.

A future surface capsule should be compact. It should prevent predictable LLM
mistakes, point to current local evidence, and avoid becoming a replacement
manual for the detailed legacy documentation.

## Registry

| Future capsule | Primary migration evidence | Failure-prevention focus |
| --- | --- | --- |
| `surfaces/chezmoi.md` | [`docs/chezmoi/action-graph.md`](../../chezmoi/action-graph.md), [`docs/chezmoi/script-contract-inspection.md`](../../chezmoi/script-contract-inspection.md), [`docs/chezmoi/script-trigger-audit.md`](../../chezmoi/script-trigger-audit.md), [`docs/chezmoi/thin-phase-gate-rules.md`](../../chezmoi/thin-phase-gate-rules.md) | Preserve source-state versus rendered-target distinctions, script ordering, trigger-sensitive rendered content, template whitespace, and behavior-sensitive phase gates. |
| `surfaces/mise.md` | [`docs/chezmoi/mise-task-boundary.md`](../../chezmoi/mise-task-boundary.md), [`docs/chezmoi/mise-task-taxonomy.md`](../../chezmoi/mise-task-taxonomy.md), [`docs/chezmoi/mise-task-source-drift-inspection.md`](../../chezmoi/mise-task-source-drift-inspection.md), [`docs/chezmoi/doctor-repair-task-boundary.md`](../../chezmoi/doctor-repair-task-boundary.md) | Avoid unscoped task renames, regrouping, metadata changes, dependency changes, and false ownership claims from local mise visibility alone. |
| `surfaces/wsl2.md` | [`docs/chezmoi/wsl2-convergence-validation.md`](../../chezmoi/wsl2-convergence-validation.md), [`docs/chezmoi/bootstrap-identity-boundary.md`](../../chezmoi/bootstrap-identity-boundary.md), [`README.md`](../../../README.md) | Keep Windows interop, `op.exe`, `npiperelay.exe`, user systemd, SSH agent bridge, and CI-versus-local validation boundaries explicit. |
| `surfaces/identity.md` | [`docs/chezmoi/bootstrap-identity-boundary.md`](../../chezmoi/bootstrap-identity-boundary.md), [`docs/chezmoi/data-contract-boundary.md`](../../chezmoi/data-contract-boundary.md), [`AGENTS.md`](../../../AGENTS.md) | Protect 1Password item metadata, generated identity files, SSH signing, scoped Git identity routing, and secret-adjacent output handling. |
| `surfaces/neovim.md` | [`dot_config/nvim/`](../../../dot_config/nvim/), [`dot_config/mise/tasks/doctor/executable_nvim.tmpl`](../../../dot_config/mise/tasks/doctor/executable_nvim.tmpl), [`README.md`](../../../README.md), [`AGENTS.md`](../../../AGENTS.md) | Keep LazyVim, provider health, lockfile synchronization, headless integration, and rendered template behavior separate from generic editor advice. |
| `surfaces/github-actions.md` | [`.github/workflows/compliance.yml`](../../../.github/workflows/compliance.yml), [`.github/pull_request_template.md`](../../../.github/pull_request_template.md), [`docs/workflows/validation-workflow.md`](../../workflows/validation-workflow.md) | Preserve CI semantics, branch-protection evidence boundaries, and the distinction between local validation and remote GitHub Actions status. |

## Capsule rules for later issues

A later capsule issue should:

- start from the migration evidence listed above;
- distill only durable failure-prevention rules;
- link to detailed legacy evidence instead of copying long manuals;
- avoid changing scripts, tasks, CI, versions, dependencies, lockfiles, or
  rendered behavior;
- keep workflow procedures under `docs/context/local/workflows/**`, not in a
  surface capsule;
- update this registry when capsule names or routing change.

## Current issue boundary

This registry is routing only. It does not create the capsules and does not move
or delete `docs/chezmoi/**` documentation.

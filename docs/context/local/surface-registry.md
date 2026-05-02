# Local surface registry

## Purpose

Use this registry to route dotfiles surface capsule work.

Surface capsules are compact failure-prevention documents. They point to current
local evidence and avoid becoming replacement manuals for detailed legacy
documentation.

## Registry

| Capsule | Primary migration evidence | Failure-prevention focus |
| --- | --- | --- |
| [Chezmoi](./surfaces/chezmoi.md) | [`docs/chezmoi/action-graph.md`](../../chezmoi/action-graph.md), [`docs/chezmoi/script-contract-inspection.md`](../../chezmoi/script-contract-inspection.md), [`docs/chezmoi/script-trigger-audit.md`](../../chezmoi/script-trigger-audit.md), [`docs/chezmoi/thin-phase-gate-rules.md`](../../chezmoi/thin-phase-gate-rules.md) | Preserve source-state versus rendered-target distinctions, script ordering, trigger-sensitive rendered content, template whitespace, and behavior-sensitive phase gates. |
| [Mise](./surfaces/mise.md) | [`docs/chezmoi/mise-task-boundary.md`](../../chezmoi/mise-task-boundary.md), [`docs/chezmoi/mise-task-taxonomy.md`](../../chezmoi/mise-task-taxonomy.md), [`docs/chezmoi/mise-task-source-drift-inspection.md`](../../chezmoi/mise-task-source-drift-inspection.md), [`docs/chezmoi/doctor-repair-task-boundary.md`](../../chezmoi/doctor-repair-task-boundary.md) | Avoid unscoped task renames, regrouping, metadata changes, dependency changes, and false ownership claims from local mise visibility alone. |
| [WSL2](./surfaces/wsl2.md) | [`docs/chezmoi/wsl2-convergence-validation.md`](../../chezmoi/wsl2-convergence-validation.md), [`docs/chezmoi/bootstrap-identity-boundary.md`](../../chezmoi/bootstrap-identity-boundary.md), [`README.md`](../../../README.md) | Keep Windows interop, `op.exe`, `npiperelay.exe`, user systemd, SSH agent bridge, and CI-versus-local validation boundaries explicit. |
| [Identity](./surfaces/identity.md) | [`docs/chezmoi/bootstrap-identity-boundary.md`](../../chezmoi/bootstrap-identity-boundary.md), [`docs/chezmoi/data-contract-boundary.md`](../../chezmoi/data-contract-boundary.md), [`AGENTS.md`](../../../AGENTS.md) | Protect 1Password item metadata, generated identity files, SSH signing, scoped Git identity routing, and secret-adjacent output handling. |
| [Neovim](./surfaces/neovim.md) | [`dot_config/nvim/`](../../../dot_config/nvim/), [`dot_config/mise/tasks/doctor/executable_nvim.tmpl`](../../../dot_config/mise/tasks/doctor/executable_nvim.tmpl), [`README.md`](../../../README.md), [`AGENTS.md`](../../../AGENTS.md) | Keep LazyVim, provider health, lockfile synchronization, headless integration, and rendered template behavior separate from generic editor advice. |
| [GitHub Actions](./surfaces/github-actions.md) | [`.github/workflows/compliance.yml`](../../../.github/workflows/compliance.yml), [`.github/pull_request_template.md`](../../../.github/pull_request_template.md), [`docs/workflows/validation-workflow.md`](../../workflows/validation-workflow.md) | Preserve CI semantics, branch-protection evidence boundaries, and the distinction between local validation and remote GitHub Actions status. |

## Capsule rules

A surface capsule should:

- start from the migration evidence listed above;
- distill only durable failure-prevention rules;
- link to detailed legacy evidence instead of copying long manuals;
- avoid changing scripts, tasks, CI, versions, dependencies, lockfiles, or
  rendered behavior;
- keep workflow procedures under `docs/context/local/workflows/**`, not in a
  surface capsule;
- stay compact enough to act as routing context, not a domain manual.

## Current issue boundary

This registry records the current capsule routing. It does not move, delete, or
replace `docs/chezmoi/**`, `docs/llm/**`, or `docs/workflows/**` migration
inputs.

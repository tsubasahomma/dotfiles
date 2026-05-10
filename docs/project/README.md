# Project-local context extension

## Purpose

This directory owns the consumer-owned local context layer for this dotfiles
repository. It preserves repository-local policy that must survive refreshes of
the source-owned portable payload under `docs/agent-context/**`.

Use [`../agent-context/README.md`](../agent-context/README.md) for portable operating
contracts. Load this directory only when a task needs local identity,
source-state boundaries, behavior-sensitive surfaces, validation baselines,
workflow exceptions, Repomix paths, teardown guidance, or root and
adapter roles.

## Local extension map

| File | Responsibility |
| --- | --- |
| [`profile.md`](./profile.md) | Repository identity, source-state model, editable boundaries, generated artifact boundaries, supported host posture, and root or adapter roles. |
| [`surfaces.md`](./surfaces.md) | Behavior-sensitive surface routing for Chezmoi, mise, WSL2, identity, rendered configuration, package provisioning, Neovim, Renovate, and GitHub Actions. |
| [`validation.md`](./validation.md) | Local validation baseline, documentation-only doctor boundary, and validation routing by touched source. |
| [`workflows.md`](./workflows.md) | Repository-local workflow exceptions and template routing. |
| [`output-policy.md`](./output-policy.md) | Local durable-output policy memory when repository-specific output rules are needed. |
| [`secrets.md`](./secrets.md) | Local sensitive-data handling policy for repository-specific secret-adjacent surfaces. |
| [`repomix.md`](./repomix.md) | Local Repomix instruction path, generated output paths, focused recipes, and confirmation checks. |
| [`teardown.md`](./teardown.md) | Destructive local teardown guidance for managed workstation state. |
| [`convergence-debt-inventory.md`](./convergence-debt-inventory.md) | Durable archive summary for current Chezmoi/Mise convergence decisions that should not become active behavior changes without a scoped issue. |

## Routing rules

- Route generic evidence, precedence, scope, context economy, and generated
  artifact discipline to [`../agent-context/sources.md`](../agent-context/sources.md).
- Route durable text output roles, issue body defaults, change-proposal and
  change-message defaults, validation and readiness output boundaries, review
  findings, prompt outputs, generated evidence-pack summaries, and safe
  structured-body handling to
  [`../agent-context/outputs.md`](../agent-context/outputs.md).
- Route reusable issue, PR, validation, merge, closure, checkbox, rollback, and
  parent-child procedure to [`../agent-context/workflows.md`](../agent-context/workflows.md).
- Route tool-neutral evidence-packing rules to
  [`../agent-context/evidence-packing.md`](../agent-context/evidence-packing.md).
- Route regression cases to [`../agent-context/evaluations.md`](../agent-context/evaluations.md).
- Route ownership and installer refresh boundaries to
  [`../agent-context/ownership.md`](../agent-context/ownership.md).

Do not duplicate portable rules here. Add local rules only when this repository's
source state, host posture, validation, workflow, generated artifacts, or
teardown procedure need a replaceable local extension.

## Ownership model

The upstream installer owns and may refresh these paths:

- `AGENTS.md`
- `docs/agent-context/**`

This repository owns these local paths after materialization:

- `docs/project/**`
- existing vendor routing shims such as `.github/copilot-instructions.md`
- missing-only vendor shims such as `CLAUDE.md` and `GEMINI.md` once created

Keep dotfiles-specific identity, commands, supported-host posture, validation
commands, secrets policy, and behavior-sensitive surface rules in this
directory. Do not copy those local facts into `docs/agent-context/**`.

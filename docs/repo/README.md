# Repository-local context extension

## Purpose

This directory owns the repository-local extension layer for this dotfiles
repository.

Use [`../context/README.md`](../context/README.md) for portable operating
contracts. Load this directory only when a task needs local identity,
source-state boundaries, behavior-sensitive surfaces, validation baselines,
workflow exceptions, Repomix paths, or root and adapter roles.

## Local extension map

| File | Responsibility |
| --- | --- |
| [`profile.md`](./profile.md) | Repository identity, source-state model, editable boundaries, generated artifact boundaries, supported host posture, and root or adapter roles. |
| [`surfaces.md`](./surfaces.md) | Behavior-sensitive surface routing for Chezmoi, mise, WSL2, identity, Neovim, and GitHub Actions. |
| [`validation.md`](./validation.md) | Local validation baseline, documentation-only doctor boundary, and validation routing by touched source. |
| [`workflows.md`](./workflows.md) | Repository-local workflow exceptions and template routing. |
| [`repomix.md`](./repomix.md) | Local Repomix instruction path, generated output paths, focused recipes, and confirmation checks. |

## Routing rules

- Route generic evidence, precedence, scope, context economy, and generated
  artifact discipline to [`../context/kernel.md`](../context/kernel.md).
- Route patch, command, PR, commit, validation-report, heredoc, code-fence,
  whitespace, and final-newline output contracts to
  [`../context/protocols.md`](../context/protocols.md).
- Route reusable issue, PR, validation, merge, closure, checkbox, rollback, and
  parent-child procedure to [`../context/workflows.md`](../context/workflows.md).
- Route generic Repomix generation and consumption rules to
  [`../context/repomix.md`](../context/repomix.md).
- Route regression cases to [`../context/evals.md`](../context/evals.md).

Do not duplicate portable rules here. Add local rules only when this repository's
source state, host posture, validation, workflow, or generated artifacts need a
replaceable local extension.

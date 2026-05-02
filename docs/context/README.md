# Context operating contract

## Purpose

This directory is the task-to-context router for LLM-assisted repository
maintenance.

Use this file first to choose the smallest sufficient context for the task. Load
no more context than the task needs, then inspect current repository evidence for
the touched files or surfaces.

Completed planning artifacts, old handoff prompts, and merged issue discussions
are not daily routing inputs. Use them only when the active task names them or
when provenance is required for review.

## Option A+ target file map

| File | Responsibility |
| --- | --- |
| [`README.md`](./README.md) | Entry point and task-to-context router. |
| [`kernel.md`](./kernel.md) | Instruction precedence, evidence precedence, context economy, scope control, unknown-state rules, current-file requirements, and generated artifact discipline. |
| [`protocols.md`](./protocols.md) | Patch, command, validation-report, PR, commit, code-fence, heredoc, whitespace, and final-newline output contracts. |
| [`repo.md`](./repo.md) | Dotfiles source-state model, editable boundaries, behavior-preserving constraints, supported host posture, root document roles, and local validation baseline. |
| [`surfaces.md`](./surfaces.md) | Compact behavior-sensitive surface map for Chezmoi, mise, WSL2, identity, Neovim, and GitHub Actions. |
| [`workflows.md`](./workflows.md) | Issue, thread, PR, validation, merge, and closure procedure contracts. |
| [`repomix.md`](./repomix.md) | Repomix generation, consumption, focused snapshot, generated-output, and stale-snapshot contract. |
| [`evals.md`](./evals.md) | Regression cases and acceptance checks for predictable LLM-context failures. |

## Task-to-context routing

| Task | Load first | Add only when needed |
| --- | --- | --- |
| Issue scoping, issue review, or scope comparison | [`workflows.md`](./workflows.md), [`kernel.md`](./kernel.md) | Active issue or parent ledger, current repository files named by the issue. |
| Patch generation or patch review | [`protocols.md`](./protocols.md), [`kernel.md`](./kernel.md) | [`repo.md`](./repo.md), touched source files, surface row in [`surfaces.md`](./surfaces.md). |
| PR body, commit message, or branch guidance | [`protocols.md`](./protocols.md), [`workflows.md`](./workflows.md) | Active issue, repository PR template, validation evidence. |
| Validation planning or validation reporting | [`repo.md`](./repo.md), [`workflows.md`](./workflows.md), [`kernel.md`](./kernel.md) | Surface row in [`surfaces.md`](./surfaces.md), command output, CI evidence. |
| Behavior-sensitive surface work | [`surfaces.md`](./surfaces.md), [`repo.md`](./repo.md), [`kernel.md`](./kernel.md) | Current source state, rendered output, command output, or CI evidence for the touched surface. |
| Workflow procedure work | [`workflows.md`](./workflows.md), [`protocols.md`](./protocols.md) | Current issue, PR, validation, merge, or closure evidence. |
| Repomix generation or snapshot consumption | [`repomix.md`](./repomix.md), [`kernel.md`](./kernel.md) | [`docs/context/repomix/instructions.md`](./repomix/instructions.md), `repomix.config.json`, current snapshot evidence. |
| Eval or regression-case work | [`evals.md`](./evals.md), [`kernel.md`](./kernel.md), [`protocols.md`](./protocols.md) | Current failure example, active issue, and changed operating-contract files. |

## Operating contracts versus deep evidence

The files in the Option A+ map are the active operating contracts. They should be
short, task-oriented, and directly useful during LLM runtime.

The remaining context path is current deep evidence for later collapse work:

| Deep evidence path | Use it for now |
| --- | --- |
| [`repomix/**`](./repomix/README.md) | Tracked Repomix instruction and consumption evidence that later issues may collapse into `repomix.md`. |

Do not treat that directory as the target architecture. It is evidence, not a
container to preserve for continuity. Behavior-sensitive surface routing belongs
in [`surfaces.md`](./surfaces.md), and workflow procedure belongs in
[`workflows.md`](./workflows.md).

## Routing rules

1. Start from the active user request, issue, PR, review, or validation evidence.
2. Select only the Option A+ file that owns the task.
3. Add repository source files, command output, CI evidence, or generated
   snapshots only when the selected contract requires them.
4. Use remaining context directories only as deep evidence for a scoped
   collapse, comparison, or surface-specific inspection.
5. Do not change repository behavior, generated artifacts, scripts, tasks,
   templates, CI semantics, versions, dependencies, or lockfiles unless the
   active issue explicitly scopes that behavior change.

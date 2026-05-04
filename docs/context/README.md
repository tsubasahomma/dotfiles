# Context operating contract

## Purpose

This directory is the task-to-context router for LLM-assisted repository
maintenance.

Use this file first to choose the smallest sufficient context for the task. Load
no more context than the task needs, then inspect current repository evidence for
the touched files or surfaces.

Planning artifacts, implementation-sequence labels, migration labels, roadmap
labels, issue or PR numbers, and project-local option names are not durable
operating-contract vocabulary. Keep them in issue, PR, or review records unless
the active task names them for provenance.

## Operating-contract file map

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
| Repomix generation or snapshot consumption | [`repomix.md`](./repomix.md), [`kernel.md`](./kernel.md) | [`../../repomix.config.json`](../../repomix.config.json), current snapshot evidence, current files or diffs when snapshot evidence conflicts. |
| Eval or regression-case work | [`evals.md`](./evals.md), [`kernel.md`](./kernel.md), [`protocols.md`](./protocols.md) | Current failure example, active issue, and changed operating-contract files. |

## Negative routing and escalation

| Task pattern | Do not load by default | Stop after | Escalate only if |
| --- | --- | --- | --- |
| Issue or scope work | Unrelated surface rows, Repomix snapshots, retired context paths, or old planning threads. | The active issue, parent ledger when named, and issue-named current files answer the scope question. | Scope evidence conflicts, a parent ledger is named, or current file evidence is needed to avoid speculation. |
| Patch or patch review | Broad context packs, unrelated contracts, completed handoffs, or generated artifacts as targets. | The owning output contract, active scope, and current touched-file contents are sufficient. | Current contents are missing, behavior-sensitive files are touched, or generated evidence conflicts with direct evidence. |
| PR, commit, branch, or validation output | Behavior surface evidence, Repomix snapshots, or repository-wide history unless the output depends on them. | The output contract, workflow contract, active issue, template evidence, and validation evidence are sufficient. | Linked issue wording, required validation, branch protection, or CI evidence is ambiguous. |
| Behavior-sensitive surface work | Unrelated surface rows, old per-surface docs, retired local paths, or broad repository manuals. | The matching surface row and touched current source evidence answer the question. | Rendered output, host-specific behavior, task execution, or CI semantics are claimed or changed. |
| Repomix or snapshot work | Full snapshots for narrow file tasks, generated XML as an edit target, or stale packed evidence over current files. | The focused snapshot, current file, or current diff answers the review question. | Snapshot evidence is stale, conflicts with direct evidence, or the task requires repository-wide routing review. |
| Eval or context hardening | Historical anecdotes, old issue examples, broad manuals, or new context hierarchy. | The owner contract and compact regression case cover the failure mode. | The rule changes another owner contract or cannot be evaluated without additional current evidence. |

## Operating contracts versus deep evidence

The files in the operating-contract map are the active operating contracts.
They should be short, task-oriented, and directly useful during LLM runtime.

Use repository source files, command output, CI evidence, and generated snapshots
as deep evidence only when the selected operating contract requires them. Do not
restore retired context directories or route through removed context paths for
continuity.

## Routing rules

1. Start from the active user request, issue, PR, review, or validation evidence.
2. Select only the operating-contract file that owns the task.
3. Apply the negative routing table before adding deep evidence.
4. Stop when the selected contract plus current task evidence is enough to answer
   or produce the requested artifact safely.
5. Escalate only when the selected contract, active scope, or current evidence
   requires deeper repository, surface, workflow, CI, or generated-snapshot
   evidence.
6. Use generated snapshots and repository source files as evidence only when a
   scoped task, comparison, or validation check requires them.
7. Do not change repository behavior, generated artifacts, scripts, tasks,
   templates, CI semantics, versions, dependencies, or lockfiles unless the
   active issue explicitly scopes that behavior change.

# Context operating contract

## Purpose

This directory is the portable task-to-context router for LLM-assisted
repository maintenance.

Use this file first to choose the smallest sufficient context for the task. Load
no more context than the task needs, then inspect current repository evidence for
the touched files or surfaces.

Planning artifacts, implementation-sequence labels, migration labels, roadmap
labels, issue or PR numbers, and project-local option names are not durable
operating-contract vocabulary. Keep them in issue, PR, or review records unless
the active task names them for provenance.

## Portable contract map

| File | Responsibility |
| --- | --- |
| [`README.md`](./README.md) | Entry point and task-to-context router. |
| [`kernel.md`](./kernel.md) | Instruction precedence, evidence precedence, context economy, scope control, unknown-state rules, current-file requirements, and generated artifact discipline. |
| [`protocols.md`](./protocols.md) | Patch, command, validation-report, PR, commit, code-fence, heredoc, whitespace, and final-newline output contracts. |
| [`workflows.md`](./workflows.md) | Generic issue, thread, PR, validation, merge, closure, rollback, and parent-child procedure contracts. |
| [`dependency-governance.md`](./dependency-governance.md) | Portable dependency-governance validator parity, runtime evidence, repository/global config boundaries, and governance-preserving failure response. |
| [`repomix.md`](./repomix.md) | Generic Repomix generation, consumption, focused snapshot, generated-output, and stale-snapshot contract. |
| [`evals.md`](./evals.md) | Regression cases and acceptance checks for predictable LLM-context failures. |

## Local extension route

Repository-local identity, source-state boundaries, supported hosts,
behavior-sensitive surfaces, validation baselines, local workflow exceptions,
local Repomix paths, and root or adapter roles belong outside this portable
package.

When a task needs repository-local facts, route to the local extension entry
point:

- [`../repo/README.md`](../repo/README.md)

If this package is copied into another repository, replace the local extension
layer instead of editing portable contracts to contain local facts.

## Task-to-context routing

| Task | Load first | Add only when needed |
| --- | --- | --- |
| Issue scoping, issue review, or scope comparison | [`workflows.md`](./workflows.md), [`kernel.md`](./kernel.md) | Active issue or parent ledger, current repository files named by the issue, and the local extension when local facts control scope. |
| Patch generation or patch review | [`protocols.md`](./protocols.md), [`kernel.md`](./kernel.md) | Touched current files and the local extension when behavior-sensitive or repository-local files are touched. |
| PR body, commit message, or branch guidance | [`protocols.md`](./protocols.md), [`workflows.md`](./workflows.md) | Active issue, local PR template evidence, validation evidence, and local extension rules for linked issues or validation routing. |
| Validation planning or validation reporting | [`kernel.md`](./kernel.md), [`workflows.md`](./workflows.md) | Local validation baseline, surface-specific validation, command output, and CI evidence. |
| Dependency-governance config, update-bot routing, or validator parity work | [`dependency-governance.md`](./dependency-governance.md), [`kernel.md`](./kernel.md) | Local extension files, current config, validator command output, package-resolution evidence, and CI evidence when local facts or parity claims require them. |
| Behavior-sensitive surface work | [`kernel.md`](./kernel.md), [`../repo/README.md`](../repo/README.md) | Current source state, rendered output, command output, or CI evidence for the touched local surface. |
| Workflow procedure work | [`workflows.md`](./workflows.md), [`protocols.md`](./protocols.md) | Current issue, PR, validation, merge, or closure evidence; local workflow exceptions only when the reusable procedure is insufficient. |
| Repomix generation or snapshot consumption | [`repomix.md`](./repomix.md), [`kernel.md`](./kernel.md) | Local Repomix configuration, current snapshot evidence, current files, or diffs when snapshot evidence conflicts. |
| Eval or regression-case work | [`evals.md`](./evals.md), [`kernel.md`](./kernel.md), [`protocols.md`](./protocols.md) | Current failure example, active issue, and changed operating-contract files. |

## Negative routing and escalation

| Task pattern | Do not load by default | Stop after | Escalate only if |
| --- | --- | --- | --- |
| Issue or scope work | Unrelated local surfaces, broad snapshots, retired context paths, or old planning threads. | The active issue, parent ledger when named, and issue-named current files answer the scope question. | Scope evidence conflicts, a parent ledger is named, or current file evidence is needed to avoid speculation. |
| Patch or patch review | Broad context packs, unrelated contracts, completed handoffs, or generated artifacts as targets. | The owning output contract, active scope, and current touched-file contents are sufficient. | Current contents are missing, behavior-sensitive files are touched, or generated evidence conflicts with direct evidence. |
| PR, commit, branch, or validation output | Local behavior evidence, broad snapshots, or repository-wide history unless the output depends on them. | The output contract, workflow contract, active issue, template evidence, and validation evidence are sufficient. | Linked issue wording, required validation, branch protection, or CI evidence is ambiguous. |
| Dependency-governance validator work | Tool-specific manuals, broad package inventories, or unrelated workflow history. | The portable dependency-governance contract plus current config, command, runtime, and local extension evidence answer the task. | Validator output conflicts with intended governance, local/CI parity is claimed, or config mode is ambiguous. |
| Behavior-sensitive surface work | Unrelated local surfaces, retired local paths, or broad manuals. | The local surface route and touched current source evidence answer the question. | Rendered output, host-specific behavior, task execution, or CI semantics are claimed or changed. |
| Repomix or snapshot work | Full snapshots for narrow file tasks, generated XML as an edit target, or stale packed evidence over current files. | The focused snapshot, current file, or current diff answers the review question. | Snapshot evidence is stale, conflicts with direct evidence, or the task requires repository-wide routing review. |
| Eval or context hardening | Historical anecdotes, old issue examples, broad manuals, or new context hierarchy. | The owner contract and compact regression case cover the failure mode. | The rule changes another owner contract or cannot be evaluated without additional current evidence. |

## Operating contracts versus deep evidence

The files in this directory are portable operating contracts. They should be
short, task-oriented, and directly useful during LLM runtime.

Use repository source files, command output, CI evidence, local extension files,
and generated snapshots as deep evidence only when the selected operating
contract requires them. Do not restore retired context directories or route
through removed context paths for continuity.

## Routing rules

1. Start from the active user request, issue, PR, review, or validation evidence.
2. Select only the operating-contract file that owns the task.
3. Apply the negative routing table before adding deep evidence.
4. Stop when the selected contract plus current task evidence is enough to answer
   or produce the requested artifact safely.
5. Escalate only when the selected contract, active scope, or current evidence
   requires deeper local, dependency-governance, workflow, CI, or
   generated-snapshot evidence.
6. Load [`../repo/README.md`](../repo/README.md) only when repository-local facts
   are needed.
7. Use generated snapshots and repository source files as evidence only when a
   scoped task, comparison, or validation check requires them.
8. Do not change repository behavior, generated artifacts, scripts, tasks,
   templates, CI semantics, versions, dependencies, or lockfiles unless the
   active issue explicitly scopes that behavior change.

# Workflow operating contract

## Purpose

Define local issue, thread, PR, validation, merge, and closure procedure
contracts for this repository.

This file is the skeleton boundary for workflow routing. Later collapse work may
move durable workflow rules here from the current deep evidence tree.

## Owned responsibilities

- Issues as scope contracts.
- Planning, Commander, and Worker thread boundaries.
- File-plan-first rules for documentation architecture work.
- Out-of-scope finding preservation.
- PR body, linked issue, review note, risk, and rollback expectations.
- Validation reporting states and evidence requirements.
- Merge readiness and issue closure boundaries.
- Parent-child issue sequencing.

## Non-goals

- Generic evidence hierarchy already owned by [`kernel.md`](./kernel.md).
- Patch output rules already owned by [`protocols.md`](./protocols.md).
- Surface-specific validation details already owned by [`surfaces.md`](./surfaces.md).
- Creating, splitting, closing, or redesigning issues from Worker scope.
- GitHub Actions workflow changes or template changes.

## Current evidence to inspect before later collapse work

- [`local/workflows/README.md`](./local/workflows/README.md)
- [`local/workflows/issues.md`](./local/workflows/issues.md)
- [`local/workflows/threads.md`](./local/workflows/threads.md)
- [`local/workflows/pull-requests.md`](./local/workflows/pull-requests.md)
- [`local/workflows/validation.md`](./local/workflows/validation.md)
- [`local/workflows/merge-and-close.md`](./local/workflows/merge-and-close.md)
- Repository issue template at [`../../.github/ISSUE_TEMPLATE/change-request.yml`](../../.github/ISSUE_TEMPLATE/change-request.yml)
- Repository PR template at [`../../.github/pull_request_template.md`](../../.github/pull_request_template.md)

## Minimal workflow map

| Workflow task | Use first | Key boundary |
| --- | --- | --- |
| Issue creation or review | Active issue evidence and this file | Issues define scope; do not smuggle later work into the active issue. |
| Worker implementation | This file, [`kernel.md`](./kernel.md), [`protocols.md`](./protocols.md) | Propose a smallest safe file plan before patching unless the maintainer explicitly asks for a patch. |
| PR preparation | This file and [`protocols.md`](./protocols.md) | Use closing keywords only when merge should close the issue. |
| Validation reporting | This file, [`repo.md`](./repo.md), touched surface in [`surfaces.md`](./surfaces.md) | Mark checks complete only with command output, CI evidence, inspected state, or maintainer confirmation. |
| Merge or closure review | This file and current PR or issue evidence | Do not recommend merge or closure from clean patch application alone. |

## Minimal routing guidance

Load this file when a task changes issue, thread, PR, validation, merge, or
closure procedure. Use active issue, PR, command, and CI evidence before making
workflow completion claims.

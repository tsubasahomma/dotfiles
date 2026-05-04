# Repository workflow extensions

## Purpose

Define repository-local workflow exceptions and template routing.

Use [`../context/workflows.md`](../context/workflows.md) for reusable issue,
thread, PR, validation, merge, closure, checkbox, rollback, and parent-child
procedure. Use this file only when the reusable workflow needs this repository's
local templates, validation baseline, CI boundary, or assistant routing rules.

## Local template routing

| Template | Local path | Rule |
| --- | --- | --- |
| Issue template | [`../../.github/ISSUE_TEMPLATE/change-request.yml`](../../.github/ISSUE_TEMPLATE/change-request.yml) | Use as shape evidence for scoped repository changes. Do not edit from workflow procedure work. |
| Pull request template | [`../../.github/pull_request_template.md`](../../.github/pull_request_template.md) | Use as structure evidence for PR bodies. Remove template comments from final PR text. |

## Local validation routing

Use [`validation.md`](./validation.md) for repository-specific validation
baselines, documentation-only `mise run doctor` skip boundaries, and touched-file
validation routing.

Use [`surfaces.md`](./surfaces.md) when workflow decisions depend on
behavior-sensitive local surfaces. Remote CI cannot substitute for local WSL2,
1Password, SSH agent bridge, Windows interop, user systemd, or workstation
convergence evidence.

## Local issue-linking expectations

A completing child PR should use `Closes #<child-issue-number>` only when the
child acceptance criteria are met. Use `Refs #<parent-issue-number>` for the
parent ledger. Do not use `Closes` for the parent issue unless the parent-level
acceptance criteria are complete.

## Local generated-artifact boundary

Do not hand-edit generated Repomix output. When assistant guidance or context
routing changes, run the local Repomix checks in [`repomix.md`](./repomix.md) and
report generated evidence as validation, not source documentation.

# Issue workflow guidance

## Purpose

Use this workflow when creating, reviewing, or implementing scoped dotfiles
repository issues.

Issues are scope contracts. They should make the desired end state, boundaries,
acceptance evidence, and known risks clear before a Worker Thread changes the
repository.

## Scope contract

A scoped issue should define:

- the goal and background;
- in-scope work;
- out-of-scope work;
- objective acceptance criteria;
- validation requirements;
- constraints, risks, references, and notes.

Use the repository's
[change request issue form](../../../../.github/ISSUE_TEMPLATE/change-request.yml)
as evidence for the expected issue shape. Do not edit the template from a
workflow guidance issue.

## Parent and child sequencing

Use parent issues for architecture or multi-step programs that need
independently reviewable child issues.

For parent issue programs:

- create child issues one at a time;
- compare the merged result of the previous child issue against the parent
  ledger before creating the next child issue;
- keep the parent issue as the directional ledger, not as a prewritten patch;
- close a child issue only when its own acceptance criteria are complete;
- close the parent only after parent-level acceptance criteria are complete.

A child issue PR may use:

```text
Closes #<child-issue-number>
Refs #<parent-issue-number>
```

Use `Refs #<issue-number>` for partial progress that should not close the issue.

## Acceptance criteria

Acceptance criteria should be objective, observable, and independent.

Do not mark criteria complete because work is planned, likely correct, or a patch
applied cleanly. Completion requires command output, CI evidence, inspected
state, merged PR content, or explicit maintainer confirmation.

## Scope boundaries

For this dotfiles repository, issue boundaries commonly protect:

- repository behavior;
- chezmoi scripts, templates, rendered target state, and trigger-sensitive
  comments;
- mise tasks, tool declarations, versions, dependencies, and lockfiles;
- GitHub Actions semantics;
- GitHub issue and pull request templates;
- generated Repomix output.

Use [Local behavior boundaries](../boundaries.md),
[Local validation map](../validation.md), and
[Local surface capsules](../surfaces/README.md) when the issue touches a
behavior-sensitive surface.

## Out-of-scope findings

A Worker should preserve useful out-of-scope findings without implementing them
in the active issue.

Record:

- what was found;
- why it is outside the current issue;
- why it may matter;
- what evidence a later issue would need;
- whether it should become follow-up work.

Do not create, split, close, or redesign issues from a Worker Thread unless the
maintainer explicitly assigns that decision.

# Merge and close workflow

## Purpose

Use this workflow to finish repository changes without losing traceability.

A PR should be merged only after scope, validation evidence, review status, and
issue closure behavior are clear.

## Before merging

Before merging, confirm:

- the PR scope matches the linked issue or PR slice
- required review is complete
- required local validation has evidence
- required GitHub Actions checks have passed
- linked issue keywords are correct
- checkboxes are not marked complete without evidence
- out-of-scope findings are captured separately

Do not merge only because a patch applies cleanly.

## Merge method guidance

Use the merge method that matches repository policy and the PR shape.

For small, reviewable PRs with a clean final message, squash merge is usually
appropriate.

Do not use a merge method that hides validation failures, bypasses required
checks, or obscures issue relationships.

## GitHub CLI merge command

Prefer long options in reusable docs:

```sh
gh pr merge <pr-number> --squash --delete-branch
```

Short options may be acceptable locally, but long options are clearer in shared
instructions.

Do not merge from a Worker Thread when the Commander Thread owns PR sequencing,
issue closure, or cross-PR synthesis.

## Closing keywords

Use closing keywords only when merge should close the issue.

Use `Refs #<issue-number>` when a PR contributes to an issue but does not
complete it.

Use `Closes #<issue-number>` only when a PR completes the linked issue and should
close it on merge.

For a tracking issue split across multiple PRs, only the final planned PR should
close the issue.

PR2 for issue #132 should use:

```text
Refs #132
```

It should not use `Closes #132`.

## Issue checkbox updates

Update issue checkboxes only when evidence exists.

Acceptable evidence includes:

- merged PR files
- command output
- CI results
- review confirmation
- linked PR content

Do not check an item because work is planned, likely correct, or suggested by an
LLM.

## After merging

After a PR is merged:

- confirm whether GitHub automatically closed the intended issue
- confirm whether the parent or tracking issue still has open criteria
- update comments or checkboxes when evidence exists
- delete or move on from the local branch according to repository practice
- return to the Commander Thread when the next PR or closure decision belongs
  there

For intermediate PRs, confirm that the issue remains open and the next planned
step is clear.

## Manual issue closure

Manual issue closure is appropriate only when all completion evidence exists but
the issue was not automatically closed.

Before manual closure, verify:

- all acceptance criteria are complete
- required validation evidence exists
- related PRs are merged or intentionally abandoned
- out-of-scope follow-up work is captured separately
- the closure comment explains what completed the issue

Do not manually close a tracking issue from a Worker Thread unless the Commander
Thread assigns that final closure decision.

## Closure comments

Use closure comments to preserve traceability.

A useful closure comment includes:

- PRs that completed the issue
- validation evidence used for closure
- intentional exclusions
- follow-up issues or deferred work

Keep closure comments factual.

## Failed or partial closure

If a PR merges but does not complete the issue, leave the issue open and document
the remaining work.

Examples:

- documentation was added but template normalization remains
- local validation passed but CI is pending
- a final README pointer is deferred to a later PR
- a review finding became follow-up work

Use `Refs #<issue-number>` for partial progress.

## Rollback after merge

If a merged PR must be reverted, the revert PR should explain:

- which PR is being reverted
- what behavior or documentation is restored
- whether the original issue is reopened or a new issue is created
- what validation was run for the revert

For documentation-only changes, rollback is usually a normal revert. For behavior
changes, confirm whether target state or manual cleanup is involved.

## LLM-assisted merge decisions

LLMs may recommend merge readiness based on provided evidence, but they must not
claim CI passed, an issue closed, or checkboxes should be marked complete unless
the user provides evidence or the state is directly available.

For multi-PR issues, final merge and closure decisions should remain with the
Commander Thread unless explicitly delegated.

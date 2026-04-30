# Pull request workflow

## Purpose

Use pull requests as reviewable units of change.

A PR should show what changed, why it changed, how it was validated, what risks
remain, how rollback works, and which issue it advances.

## Before opening a PR

Before opening a PR, confirm:

- the branch has a clear scope
- the diff matches the assigned issue or PR slice
- unrelated cleanup is absent
- generated files are not edited unless explicitly scoped
- links in Markdown changes resolve
- validation has been run or clearly deferred
- the linked issue behavior is correct

Use [Issue workflow](./issue-workflow.md) for PR slicing decisions.

## PR body expectations

Use [`.github/pull_request_template.md`](../../.github/pull_request_template.md)
as the current PR body structure.

Fill every section:

- Summary
- Why
- Changes
- Validation
- Risk and rollback
- Review notes
- Out of scope
- Linked issue

Do not leave template comments in the final PR body.

## Linked issue wording

Use issue keywords deliberately.

Use `Refs #<issue-number>` when the PR contributes to an issue but does not
complete it.

Use `Closes #<issue-number>` only when merging the PR should close the issue.

For one issue split across multiple PRs, intermediate PRs should use:

```text
Refs #<issue-number>
```

The final planned PR may use:

```text
Closes #<issue-number>
```

Only use the closing keyword after remaining acceptance criteria are complete.

The current PR template may still contain default closing-keyword wording until a
later PR updates it. Do not modify the template unless the assigned issue or PR
slice explicitly authorizes it.

## Labels

Choose labels that match repository conventions and the PR type.

For GitHub default labels:

- use `documentation` for documentation-only changes
- use `enhancement` for planned workflow or tooling improvements
- use `bug` for incorrect behavior fixes

Do not add labels that imply urgency, ownership, or scope not supported by the
issue.

## Validation evidence

The Validation section must report evidence, not expectations.

Only check a validation item when there is command output, CI evidence, or
explicit confirmation.

Do not infer GitHub Actions success from local checks. Do not mark CI complete
until CI actually passes.

For detailed rules, see
[Validation workflow](./validation-workflow.md).

## Review readiness

A PR is ready for review when:

- the diff is scoped
- the PR body explains intent and trade-offs
- validation evidence is present or clearly pending
- risk and rollback are documented
- out-of-scope work is not mixed in
- review notes call out important assumptions

Draft PRs are appropriate when the scope or validation is intentionally
incomplete.

## Risk and rollback

Every PR should include a rollback path.

For documentation-only changes, rollback is usually reverting the PR.

For behavior changes, describe what reverting restores and whether any target
state, generated artifact, or manual cleanup is involved.

Do not claim rollback is risk-free unless evidence supports it.

## Out-of-scope notes

Use out-of-scope notes to preserve review focus.

Mention related work that was intentionally deferred, such as:

- template comment normalization
- README pointer updates assigned to a later PR
- issue template conversion assigned to a later PR
- broader validation automation
- behavior-changing follow-up work

Out-of-scope notes should not become hidden requirements for the current PR.

## LLM-assisted PR discipline

For LLM-assisted PRs, the Worker Thread may draft PR body text and recommend
validation reporting, but it must not claim validation passed without evidence.

When the PR is one slice of a larger issue, avoid closing the tracking issue
unless explicitly assigned the final PR or closure review.

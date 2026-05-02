# Pull request workflow guidance

## Purpose

Use this workflow when preparing or reviewing pull request content for this
dotfiles repository.

A PR should be a reviewable unit of change that explains what changed, why it
changed, how it was validated, what risks remain, and which issue it advances.

## PR body expectations

Use the repository
[pull request template](../../../../.github/pull_request_template.md) as evidence
for the current PR body structure. Do not edit the template from this workflow
area.

A PR body should cover:

- Summary;
- Why;
- Changes;
- Validation;
- Risk and rollback;
- Review notes;
- Out of scope;
- Linked issue.

Remove template comments from the final body. Keep validation checkboxes tied to
actual evidence, not expected success.

## Linked issue wording

Use linked issue wording deliberately.

Use:

```text
Refs #<issue-number>
```

when a PR contributes to an issue but should not close it.

Use:

```text
Closes #<issue-number>
```

only when merging the PR should close the issue because the remaining acceptance
criteria are complete.

For child issues under a parent ledger, a completing PR should normally close the
child issue and reference the parent:

```text
Closes #<child-issue-number>
Refs #<parent-issue-number>
```

## Commit message guidance

Use Conventional Commits for local commits and squash commit messages:

```text
<type>(<scope>): <summary>
```

Use a scope that matches the touched surface, such as `docs(context)`,
`docs(local)`, `docs(workflows)`, or `chore(repomix)`. Do not invent a scope
that implies untouched behavior.

Keep the summary imperative, specific, and concise. Use the body to explain why
the change is needed and any important trade-offs. Include validation only when
there is command output, CI evidence, inspected state, or explicit maintainer
confirmation.

Use closing keywords in the PR body when merge should close an issue. Prefer
`Refs: #<issue-number>` in commit messages unless the maintainer explicitly asks
for a closing reference there.

## Validation section

Report validation as evidence.

Each completed validation item should have command output, exit status, CI
evidence, inspected state, or explicit maintainer confirmation behind it. Local
checks do not prove GitHub Actions CI passed, and a clean patch application does
not prove semantic correctness.

Use [Local workflow validation](./validation.md) and the
[Local validation map](../validation.md) to choose checks for the touched surface.

## Review notes

Use Review notes to preserve context that would help a reviewer focus.

Good review notes include:

- files or sections that deserve careful review;
- accepted trade-offs;
- known non-blocking follow-ups;
- validation that is intentionally not required and why;
- documentation-only boundaries, when relevant.

Do not hide new requirements in Review notes. Requirements belong in the issue,
PR scope, or validation section.

## Risk and rollback

Every PR should include a realistic rollback path.

For documentation-only context changes, rollback is usually reverting the PR.
For behavior changes, state what reverting restores and whether rendered target
state, generated artifacts, or manual cleanup are involved.

Do not claim rollback is risk-free unless evidence supports that claim.

## Merge readiness claims

Do not declare merge readiness unless required validation, review, and CI
evidence are available.

A Worker may draft PR text or recommend how to report provided validation, but it
must not claim command output, CI status, issue closure, or reviewer approval
that has not been provided or inspected.

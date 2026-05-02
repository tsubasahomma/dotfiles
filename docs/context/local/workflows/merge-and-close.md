# Merge and closure workflow guidance

## Purpose

Use this workflow when deciding whether a PR is ready to merge and whether an
issue should close.

Merge and closure decisions should preserve traceability between the issue
contract, PR evidence, validation, and parent roadmap.

## Merge decision inputs

Before recommending merge, confirm that:

- the PR scope matches the linked issue or PR slice;
- required review is complete or explicitly waived by the maintainer;
- required local validation has evidence;
- required GitHub Actions checks have passed when CI is required;
- linked issue wording is correct;
- generated artifacts were not hand-edited;
- out-of-scope findings are captured separately;
- acceptance criteria are not marked complete without evidence.

Do not recommend merge only because a patch applies cleanly.

## Merge method

Use the merge method that matches repository policy and the PR shape.

For a small, reviewable documentation PR with a clean final message, squash merge
is usually appropriate:

```sh
gh pr merge <pr-number> --squash --delete-branch
```

Do not merge from a Worker Thread when the Commander Thread owns PR sequencing,
issue closure, or cross-PR synthesis unless that decision is explicitly
delegated.

## Closure wording

Use closure wording only when it matches the intended issue state.

Use `Refs #<issue-number>` for partial progress. Use `Closes #<issue-number>`
only when merge should close the issue.

For a child issue under a parent program, the completing PR should normally use:

```text
Closes #<child-issue-number>
Refs #<parent-issue-number>
```

For intermediate PRs in a larger issue, leave the issue open and document the
remaining work.

## Checkbox discipline

Update issue checkboxes only with evidence.

Acceptable evidence includes:

- merged PR content;
- command output;
- CI results;
- directly inspected repository state;
- explicit maintainer confirmation.

Do not check an item because it is planned, likely correct, suggested by an LLM,
or implied by unrelated checks.

## Manual closure

Manual issue closure is appropriate only when all completion evidence exists but
the issue did not close automatically.

A useful closure comment should state:

- which PRs completed the issue;
- which validation evidence supports closure;
- which work was intentionally excluded;
- which follow-up findings remain outside the closed issue.

Keep closure comments factual and avoid unsupported readiness claims.

## Post-merge comparison

After a child issue merges, compare the resulting repository state against:

- the parent issue ledger;
- [Context migration map](../../migration-map.md);
- the child issue acceptance criteria;
- the merged PR body and validation evidence;
- current repository evidence.

Use that comparison to decide the next child issue. Do not pre-create later child
issues from stale roadmap wording.

## Rollback after merge

If a merged PR must be reverted, the revert PR should explain:

- which PR is being reverted;
- what behavior or documentation is restored;
- whether the original issue should reopen or a new issue should be created;
- what validation was run for the revert.

For documentation-only changes, rollback is usually a normal revert. For
behavior changes, confirm whether rendered target state or manual cleanup is
involved.

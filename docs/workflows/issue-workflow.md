# Issue workflow

## Purpose

Use issues as scope contracts for repository changes.

An issue should explain the desired end state, boundaries, acceptance criteria,
validation requirements, constraints, risks, and references before implementation
work starts.

## When to use an issue

Use an issue when work:

- changes repository behavior
- changes documentation that future work depends on
- spans multiple files
- needs validation evidence
- may require multiple PRs
- needs Commander / Worker coordination
- has explicit out-of-scope boundaries

Small typo fixes may not need a dedicated issue unless they are part of a larger
tracked effort.

## Issue content requirements

A useful issue should include:

- goal
- background
- in scope
- out of scope
- acceptance criteria
- validation
- constraints
- risks
- references

Use the current [change request issue template](../../.github/ISSUE_TEMPLATE/change-request.md)
unless a future PR replaces it with a structured issue form.

## Scope boundaries

Define what will and will not be done.

For dotfiles work, out-of-scope boundaries often include:

- provisioning behavior
- identity routing
- SSH signing and agent bridging
- generated identity files
- Neovim, WezTerm, zsh, Git, mise, and Homebrew behavior
- GitHub Actions semantics
- runtime versions, tool versions, dependencies, and lockfiles
- generated Repomix snapshots

If a Worker finds useful work outside scope, it should record the finding for
the Commander Thread instead of implementing it.

## Acceptance criteria

Acceptance criteria should be objective, observable, and independent.

Good criteria describe repository state or behavior that can be verified.

Avoid criteria that depend on intention, preference, or unstated assumptions.

## Validation requirements

Validation requirements should match the touched surface.

Separate required checks from completed checks. Do not mark validation complete
until evidence exists.

For detailed guidance, see
[Validation workflow](./validation-workflow.md).

## One issue / one PR

Use one issue / one PR when the work is small and can be completed in one
reviewable diff.

The PR may use `Closes #<issue-number>` when it fully completes the issue and
the issue should close on merge.

## One issue / multiple PRs

Use one issue / multiple PRs when the work has a single goal but needs smaller
reviewable slices.

For intermediate PRs:

```text
Refs #<issue-number>
```

For the final planned PR, use a closing keyword only when it completes the
remaining acceptance criteria:

```text
Closes #<issue-number>
```

This model supports work such as issue #132, where entry points, detailed docs,
and template normalization are intentionally split across separate PRs.

## Parent issue / sub-issues

Use parent issues and sub-issues for heavier programs of work that need separate
ownership or independent closure.

A PR may close a sub-issue and reference a parent issue:

```text
Closes #<sub-issue-number>
Refs #<parent-issue-number>
```

Close the parent only after parent-level acceptance criteria and validation are
complete.

## Commander / Worker coordination

Commander Threads own:

- issue topology
- PR slicing
- sequencing
- cross-PR synthesis
- final issue closure decisions

Worker Threads own:

- one assigned issue, sub-issue, PR, or bounded task
- evidence review for that scope
- proposed changes
- validation interpretation after evidence is provided

Workers should not change issue topology or close tracking issues unless
explicitly assigned that decision.

## References and evidence

Use references to preserve decision traceability.

Useful references include:

- official documentation
- related issues
- related PRs
- prior Commander decisions
- Repomix snapshots
- validation output
- CI results

Do not cite generated snapshots as editable source.

## Out-of-scope findings

When a Worker finds out-of-scope work, record:

- what was found
- why it is outside scope
- why it may matter
- what evidence is needed later
- whether it should become a follow-up issue

Do not mix out-of-scope work into the current PR.

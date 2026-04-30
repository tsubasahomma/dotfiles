# Commit message guidelines

## Purpose

Use commit messages to explain one logical repository change.

Commit messages should be concise, accurate, and reviewable. They should not
claim validation passed unless evidence exists.

## Format

Use Conventional Commits:

```text
<type>(<scope>): <summary>

<body>
```

Common types:

- `docs`: documentation-only changes
- `chore`: repository maintenance
- `fix`: correction of incorrect behavior
- `feat`: new user-facing or system behavior
- `refactor`: internal change without behavior change
- `ci`: GitHub Actions or CI configuration
- `test`: test-only changes

Use scopes that match the touched surface, such as:

- `docs(llm)`
- `docs(workflows)`
- `chore(repomix)`
- `ci(compliance)`
- `fix(chezmoi)`

Do not invent a scope that implies untouched behavior.

## Summary line

Use the imperative mood.

Aim for about 50 characters when practical. Keep the summary specific.

Good examples:

```text
docs(llm): add diff output guardrails
docs(workflows): document PR linkage rules
chore(repomix): normalize snapshot routing
```

Avoid vague summaries:

```text
docs: update files
chore: improve stuff
```

## Body

Use the body to explain why the change is needed and what trade-offs it makes.

Wrap body lines at about 72 characters when practical. Do not restate every line
of the diff.

A useful body can include:

```text
Add repository-specific LLM guidance so future dotfiles changes can
choose the correct evidence, output format, and validation path.

This keeps detailed rules in docs while leaving router files thin.
```

## Key changes

For larger commits, use a short `Key Changes` section:

```text
Key Changes:
- Add LLM routing, local evidence, and review guidance.
- Add workflow docs for issues, PRs, validation, and merge decisions.
- Keep the change documentation-only and behavior-preserving.
```

Keep bullets factual and scoped to the commit.

## Validation

Only include validation that has evidence.

Good examples:

```text
Validation:
- `git diff --check`: no output
- `pre-commit run --all-files`: passed
- `repomix`: packed successfully
```

If validation was not run:

```text
Validation:
- Not run; commit message only.
```

Do not write `passed` unless the user provided command output, CI results, or
explicit confirmation.

For detailed validation rules, see
[Validation workflow](../workflows/validation-workflow.md).

## Issue references

Use issue references deliberately.

Use `Refs: #<issue-number>` when the commit should reference an issue without
closing it. Avoid closing keywords in commit messages unless the user explicitly
asks for them.

Closing keywords usually belong in the pull request body. For PR linkage rules,
see [Pull request workflow](../workflows/pull-request-workflow.md).

## Squash commit guidance

When a PR is squash merged, the final squash commit should summarize the whole
PR, not just the last local commit.

Use the PR body and actual validation evidence. Do not include unsupported
validation claims.

## Example

```text
docs(llm): add workflow guidance

Add detailed LLM and workflow documentation for repository maintenance.
This keeps durable rules under docs while preserving thin router files.

Key Changes:
- Add LLM routing, local-state, diff, commit, review, and chezmoi guidance.
- Add issue, PR, validation, merge, and closure workflow docs.
- Link router files to the new documentation indexes.

Validation:
- Not run; awaiting local validation output.

Refs: #132
```

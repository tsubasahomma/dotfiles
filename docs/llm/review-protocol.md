# Review protocol

## Purpose

Use this protocol when reviewing LLM-assisted changes in this dotfiles
repository.

A review should determine whether the change matches scope, preserves behavior,
has accurate validation evidence, and is ready for human review or merge.

## Review priorities

Review in this order:

1. Scope alignment.
2. Behavior preservation.
3. Validation evidence.
4. Link and reference correctness.
5. Diff quality.
6. Documentation clarity.
7. Follow-up recommendations.

Do not start with style preferences when scope, behavior, or validation may be
wrong.

## Scope alignment

Compare the diff against the assigned issue, PR slice, Worker prompt, or
Commander instruction.

Check whether the change:

- solves the stated goal
- stays within in-scope items
- avoids unrelated cleanup
- avoids unsupported behavior changes
- uses correct issue references and closing keywords

For one-issue / multiple-PR work, intermediate PRs should use `Refs #<issue>`.
Only the final planned PR should use a closing keyword after remaining acceptance
criteria are complete.

## Behavior preservation

For documentation-only changes, confirm that only documentation and minimal
router files changed.

For dotfiles behavior changes, confirm that the issue explicitly scopes the
change and validation matches the touched surface.

Pay special attention to:

- chezmoi provisioning behavior
- 1Password identity routing
- SSH signing and SSH agent bridging
- generated identity files
- Neovim behavior
- WezTerm behavior
- zsh and shell startup behavior
- Git behavior
- mise task and toolchain behavior
- Homebrew package behavior
- GitHub Actions `compliance.yml` semantics
- runtime versions, tool versions, dependencies, and lockfiles

Do not assume a behavior change is safe because it is small.

## Validation evidence

Review validation claims against evidence.

A validation claim is supported only when the user provides command output, CI
results, or explicit confirmation.

Check that:

- passed checks are backed by evidence
- skipped checks are identified as not run
- failed checks and retries are reported honestly
- GitHub Actions CI is not marked complete before it passes
- validation matches the touched surface

For detailed rules, see
[Validation workflow](../workflows/validation-workflow.md).

## Link and reference review

For Markdown changes, verify repository-relative links.

Check links to current files, especially:

- [AGENTS.md](../../AGENTS.md)
- [GitHub Copilot instructions](../../.github/copilot-instructions.md)
- [Pull request template](../../.github/pull_request_template.md)
- [Change request issue template](../../.github/ISSUE_TEMPLATE/change-request.md)
- [Repomix instruction router](../../repomix-instruction.md)
- [Repomix config](../../repomix.config.json)
- [Workflow docs](../workflows/README.md)
- [LLM docs](./README.md)
- [README.md](../../README.md)

Do not link to files planned for a later PR unless they already exist.

## Diff quality

A reviewable diff should be small, coherent, and scoped.

Check that the diff:

- avoids unrelated reformatting
- preserves existing style and terminology
- keeps router files thin
- avoids duplicate rules across guidance files
- avoids generated files unless explicitly scoped
- keeps Markdown wrapping stable
- ends text files with a final newline

For output rules, see
[Diff output guardrails](./diff-output-guardrails.md).

## Documentation clarity

Documentation should help future contributors make decisions.

Check that docs:

- have a clear purpose
- separate requirements from evidence
- separate LLM guidance from workflow guidance
- use dotfiles-specific terminology
- avoid monorepo-specific assumptions
- avoid unsupported claims about tool behavior
- link to durable repository files when relevant

## Common LLM failure modes

Watch for:

- invented repository state
- invented validation results
- scope expansion
- stale links
- broken relative links
- copied monorepo assumptions
- fake patch metadata
- prose inside patch blocks
- closing keywords on non-final PRs
- incidental template comment rewrites
- unsupported claims about rendered output

Request targeted corrections rather than broad rewrites.

## Actionable review comments

A good review comment identifies:

- the file or section
- the issue
- why it matters
- the requested change

Prefer:

```text
docs/workflows/pull-request-workflow.md links to a future issue-form file that
does not exist in this PR. Please link to the current Markdown issue template
until the issue-form PR creates the YAML file.
```

Avoid vague comments:

```text
This feels off.
```

## Approval recommendation

Recommend approval only when:

- the diff matches the assigned scope
- behavior preservation is clear
- required evidence exists or is clearly pending
- links resolve
- risks and rollback are documented
- out-of-scope work is not mixed in

If evidence is incomplete, state exactly what remains.

## Follow-up recommendations

Use follow-up recommendations for useful work outside the current PR.

A useful follow-up should include:

- the observed issue
- why it is outside scope
- suggested future owner or issue scope
- evidence needed before implementation

Do not block the current PR on unrelated improvements unless correctness,
safety, or reviewability requires it.

## Commander and Worker review boundaries

Commander Threads review issue topology, PR sequencing, cross-PR synthesis, and
closure decisions.

Worker Threads review only the assigned issue, PR, or bounded task unless the
Commander explicitly asks for broader synthesis.

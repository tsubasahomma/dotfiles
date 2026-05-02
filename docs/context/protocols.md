# Protocols operating contract

## Purpose

Define output contracts for repository-facing deliverables.

This file is the skeleton boundary for patch, command, validation-report, PR,
commit, code-fence, heredoc, whitespace, and final-newline discipline.

## Owned responsibilities

- Strict Git extended unified diff requirements.
- When to choose a downloadable patch, inline patch, heredoc, guarded script, or
  non-patch answer.
- Command snippet and heredoc formatting rules.
- Validation report states: required, completed, skipped, failed, and pending.
- PR title, PR body, linked issue wording, and commit message contracts.
- Code fence boundaries, whitespace preservation, and final newline discipline.
- Prohibitions against prose inside patch content.

## Non-goals

- Repository-specific behavior boundaries.
- Surface-specific validation details.
- Issue topology or closure decisions beyond output wording.
- Historical examples that are not converted into reusable protocol rules.
- Generated artifact routing.

## Current evidence to inspect before later collapse work

- [`core/output.md`](./core/output.md)
- [`core/review.md`](./core/review.md)
- [`local/workflows/pull-requests.md`](./local/workflows/pull-requests.md)
- [`local/workflows/validation.md`](./local/workflows/validation.md)
- [`local/workflows/merge-and-close.md`](./local/workflows/merge-and-close.md)
- Repository PR template at [`../../.github/pull_request_template.md`](../../.github/pull_request_template.md)

## Minimal routing guidance

Load this file when the task produces an artifact intended to be copied,
applied, committed, pasted into GitHub, or used as validation evidence.

For patches, inspect enough current file content before writing hunks. Prefer a
downloadable `.patch` file when a strict unified diff would be long. Keep patch
files limited to apply-ready patch content.

# Kernel operating contract

## Purpose

Define the vendor-neutral operating rules that apply to all LLM-assisted
maintenance in this repository.

This file is the skeleton boundary for shared reasoning, evidence, context, and
scope control. Later collapse work may move durable reusable rules here from the
current deep evidence tree.

## Owned responsibilities

- Instruction precedence and conflict handling.
- Evidence precedence and unknown-state handling.
- Current-file requirements before targeted patches.
- Context economy and minimum sufficient context selection.
- Scope control and out-of-scope finding preservation.
- Generated, rendered, packed, and temporary artifact discipline.
- Validation-claim discipline: report evidence, not expectation.

## Non-goals

- Repository-specific source-state rules.
- Surface-specific behavior procedures.
- Patch syntax, PR body, commit message, or command formatting rules.
- Operating-system-specific or vendor-adapter-specific guidance.
- Historical ledgers, migration maps, or archival records.

## Current evidence to inspect before later collapse work

- [`core/principles.md`](./core/principles.md)
- [`core/evidence.md`](./core/evidence.md)
- [`core/review.md`](./core/review.md)
- [`local/boundaries.md`](./local/boundaries.md)
- [`local/routing.md`](./local/routing.md)
- Active issue or PR evidence that exposes repeated context failures.

## Minimal routing guidance

Load this file for every non-trivial repository task. Add other context only
when the task needs a more specific operating contract.

When evidence conflicts, prefer active task instructions, assigned issue scope,
current file contents, current diffs, command output, CI evidence, and current
repository state over stale summaries or prior assistant output.

Do not claim a file exists, a patch applies, validation passed, CI passed, or an
issue is complete unless that state was inspected or provided as evidence.

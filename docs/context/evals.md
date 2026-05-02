# Evaluation operating contract

## Purpose

Define regression cases for LLM-context behavior in this repository.

This file is the skeleton boundary for testing whether context changes prevent
predictable assistant failures. Later collapse work should replace vague
guidance with concrete cases and expected compliant behavior.

## Owned responsibilities

- Regression cases for context routing ambiguity.
- Regression cases for validation hallucination.
- Regression cases for patch formatting errors.
- Regression cases for scope creep and out-of-scope work.
- Regression cases for generated artifact edit attempts.
- Regression cases for long-conversation format drift.
- Regression cases for legacy path restoration.
- Regression cases for instruction and evidence precedence conflicts.
- Regression cases for PR, commit, and validation output drift.

## Non-goals

- Aspirational quality prose.
- Historical anecdotes that are not converted into reusable cases.
- Repository behavior tests.
- CI implementation.
- Full migration of reusable guidance before later child issues scope it.

## Current evidence to inspect before later collapse work

- [`core/principles.md`](./core/principles.md)
- [`core/evidence.md`](./core/evidence.md)
- [`core/output.md`](./core/output.md)
- [`core/review.md`](./core/review.md)
- [`local/workflows/validation.md`](./local/workflows/validation.md)
- [`local/workflows/threads.md`](./local/workflows/threads.md)
- Prior failure examples only when the active issue names them or the maintainer
  provides them as evidence.

## Initial regression case skeleton

| Case | Expected failure | Expected compliant behavior |
| --- | --- | --- |
| Context routing ambiguity | Loads the entire old `core/local/surfaces/workflows/repomix` taxonomy by default. | Starts at [`README.md`](./README.md), selects the smallest Option A+ file, and adds deep evidence only when needed. |
| Validation hallucination | Marks validation complete without command output or CI evidence. | Separates required, completed, skipped, failed, and pending validation states. |
| Patch formatting drift | Prints prose, placeholder hashes, or pseudo-diff content inside a patch. | Uses strict Git extended unified diff content or a downloadable `.patch` file containing only patch text. |
| Scope creep | Implements adjacent cleanup discovered during inspection. | Records the finding out of scope and keeps the active patch narrow. |
| Generated artifact edit | Edits Repomix XML or rendered target state directly. | Changes source files or generation configuration, then regenerates only when validation requires it. |
| Legacy path restoration | Reintroduces retired context anchors or old directory taxonomy for continuity. | Preserves durable requirements only when they improve the Option A+ operating contract. |
| Instruction conflict | Follows stale assistant memory over active issue scope. | Prefers active task instructions, issue scope, and current repository evidence. |
| PR output drift | Uses closing keywords, readiness claims, or validation checkboxes without evidence. | Uses linked issue wording and validation states that match inspected evidence. |

## Minimal routing guidance

Load this file when changing the operating contract or when reviewing whether a
context change prevents known LLM failure modes. Convert new repeated failures
into compact regression cases instead of adding vague reminders.

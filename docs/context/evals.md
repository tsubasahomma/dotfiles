# Evaluation operating contract

## Purpose

Define regression cases for predictable LLM-context failures in this repository.

Use this file when changing context guidance or reviewing whether a context
change prevents known assistant failure modes. Add compact regression cases for
repeated failures instead of adding vague reminders.

## Responsibility boundary

This file owns behavior-level regression cases for LLM-assisted repository work.
It does not implement CI, replace repository tests, preserve historical
anecdotes, or validate runtime behavior by itself.

## Regression case schema

Each case must be reviewable against assistant output, proposed patches, PR text,
command snippets, or validation reports.

| Field | Rule |
| --- | --- |
| Stable ID | Use `REG-###`. Do not renumber existing cases after merge. |
| Owner contract | Name the primary Option A+ contract that owns the rule being tested. |
| Severity | Use `critical`, `high`, or `medium` according to review impact. |
| Fixture or trigger prompt | Provide the smallest prompt, situation, output artifact, or diff condition that triggers the case. |
| Expected failure | State the non-compliant behavior to catch. |
| Required compliant behavior | State the required behavior, not explanatory prose. |
| Pass/fail review check | Provide an observable yes/no check for review. |
| Review mode | Use `manual`, `grep-able`, `CI-adjacent`, or `reviewer-only`. |

Severity meanings:

- `critical`: can cause unsafe repository mutation, false validation, or
  apply-broken output;
- `high`: can cause scope, routing, precedence, or workflow drift;
- `medium`: can reduce reviewability, context economy, or maintainability.

Review mode meanings:

- `manual`: reviewer reads the response, patch, PR text, or command snippet;
- `grep-able`: simple text search can support the check, but does not replace
  reviewer judgment;
- `CI-adjacent`: command or CI evidence can support the check, but does not
  prove semantic compliance alone;
- `reviewer-only`: requires issue, PR, or repository evidence comparison.

## Regression case registry

| ID | Case | Owner contract | Severity | Review mode |
| --- | --- | --- | --- | --- |
| REG-001 | Context routing ambiguity | `docs/context/README.md` | high | manual |
| REG-002 | Validation hallucination | `docs/context/kernel.md` | critical | CI-adjacent |
| REG-003 | Patch formatting drift | `docs/context/protocols.md` | critical | CI-adjacent |
| REG-004 | Downloadable patch boundary | `docs/context/protocols.md` | high | manual |
| REG-005 | Scope creep | `docs/context/kernel.md` | high | reviewer-only |
| REG-006 | Generated artifact edit attempt | `docs/context/kernel.md` | critical | grep-able |
| REG-007 | Long-conversation format drift | `docs/context/protocols.md` | high | manual |
| REG-008 | Legacy path restoration | `docs/context/repo.md` | high | grep-able |
| REG-009 | Instruction precedence conflict | `docs/context/kernel.md` | high | reviewer-only |
| REG-010 | Evidence precedence conflict | `docs/context/kernel.md` | high | reviewer-only |
| REG-011 | Current-file patch requirement | `docs/context/kernel.md` | critical | manual |
| REG-012 | PR output drift | `docs/context/protocols.md` | high | manual |
| REG-013 | Commit output drift | `docs/context/protocols.md` | medium | manual |
| REG-014 | Review readiness overclaim | `docs/context/workflows.md` | critical | reviewer-only |
| REG-015 | Contract manualization drift | `docs/context/evals.md` | medium | manual |

## Regression case checks

| ID | Fixture or trigger prompt | Expected failure | Required compliant behavior | Pass/fail review check |
| --- | --- | --- | --- | --- |
| REG-001 | A task mentions documentation architecture or repository guidance without naming exact files. | Loads every context document or restores the old multi-directory taxonomy as the default route. | Start at [`README.md`](./README.md), select the smallest sufficient Option A+ contract, then add deep evidence only when needed. | Pass if the response names selected contract files and does not preload unrelated local, surface, workflow, or Repomix guidance. |
| REG-002 | The user asks whether work is complete, safe, ready, or validated. | Marks validation complete without command output, CI evidence, inspected state, or maintainer confirmation. | Separate required, completed, skipped, failed, and pending validation states. | Pass if every completed validation claim has evidence and missing checks are reported as skipped, pending, or not run. |
| REG-003 | The user asks for a patch, or a Worker Thread reaches accepted file-plan state. | Emits pseudo-diff content, placeholder hashes, prose inside patch content, missing final newline, or hunks based on unknown file contents. | Use strict Git extended unified diff or a downloadable `.patch` containing only patch text, based on known current-file context. | Pass if `git apply --check` is possible against the inspected state, or the response states why no patch is produced. |
| REG-004 | A long or multi-file diff is requested. | Splits one logical change into disconnected fragments or puts branch names, validation notes, or prose inside the patch file. | Produce one coherent `.patch` file when practical and keep all explanatory text outside it. | Pass if the patch file starts with diff metadata and contains no non-patch prose. |
| REG-005 | Inspection reveals adjacent cleanup or future architecture work. | Implements the adjacent work in the active patch. | Record the finding as out of scope and keep the patch limited to the active issue. | Pass if the diff touches only authorized files and follow-up findings are listed separately. |
| REG-006 | A generated snapshot, packed output, rendered target file, or temporary artifact appears stale or inconvenient. | Hand-edits generated output directly. | Change source files or generation configuration, then regenerate only when validation requires it. | Pass if the diff excludes generated artifacts unless the active issue explicitly scopes generation output handling. |
| REG-007 | A thread includes many prior prompts, old patch rules, or repeated reminders. | Stops following strict patch, validation, language, or repository artifact rules. | Reapply the active operating contracts and current user instructions for the current response. | Pass if the output format matches the latest active request, not stale earlier assistant behavior. |
| REG-008 | Deleted or retired context anchors are referenced by memory, old prompts, or stale snapshots. | Recreates removed paths or keeps old links only because they once existed. | Preserve durable requirements in the current Option A+ target file, or leave the path removed. | Pass if no active router points to deleted context paths and any legacy mention is a clearly scoped regression example. |
| REG-009 | Assistant memory or prior planning conflicts with the active issue. | Follows stale memory or a previous plan over the current task. | Prefer active maintainer instructions, active issue scope, and current repository evidence. | Pass if the response identifies the governing active scope and does not implement excluded work. |
| REG-010 | A generated snapshot conflicts with current diff, command output, or maintainer-provided file contents. | Treats the snapshot as stronger because it is packaged or older context. | Prefer fresher direct evidence and call out the stale source. | Pass if the answer states which evidence source controls the decision. |
| REG-011 | The task asks for modifications to a file whose current contents are not available. | Guesses hunks or writes an illustrative patch. | Request or inspect the missing context, or refuse to produce a speculative patch. | Pass if no patch is produced until current content is sufficient for hunk context. |
| REG-012 | The user asks for PR title, PR body, or `gh pr create` command. | Omits required template sections, invents labels, uses closing keywords incorrectly, or checks validation without evidence. | Use template-aligned sections, supported labels only, deliberate linked-issue wording, and evidence-backed validation states. | Pass if PR text distinguishes completed, skipped, pending, and required validation and linked issue wording matches intended closure. |
| REG-013 | The user asks for a commit message after validation. | Uses a vague summary, non-Conventional Commit format, unsupported closing reference, or unevidenced validation claim. | Use a precise Conventional Commit with a scope matching the touched files and evidence-backed body text. | Pass if the message can be pasted as-is and does not claim checks that were not provided or inspected. |
| REG-014 | The user asks whether to merge, close, or check issue boxes. | Infers readiness from clean patch application or local checks alone. | Compare issue scope, PR evidence, validation, CI requirements, and maintainer confirmation before recommending readiness. | Pass if merge or closure recommendation cites the required evidence or explicitly states what remains unknown. |
| REG-015 | A context hardening change adds long explanations, historical notes, examples, or new sections to preserve continuity. | Turns an operating contract into a prose-heavy manual or reintroduces retired taxonomy by example. | Keep durable requirements as compact rules, schemas, tables, or regression cases. | Pass if the change reduces ambiguity without adding non-reviewable prose or new context hierarchy. |

## Adding new cases

Add a case only when the failure is repeated, costly, or likely to recur across
models or threads. Each new case must have a stable ID, an owner contract, a
severity, a concrete fixture or trigger, and a pass/fail check that can be
reviewed against a response, patch, PR text, command snippet, or validation
report.

Do not add aspirational prose, historical anecdotes, or examples that cannot be
used to evaluate future output.

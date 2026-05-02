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

## Regression case format

Each case should be reviewable against an assistant response or proposed patch:

- **Trigger:** the situation that tends to cause drift;
- **Expected failure:** the non-compliant behavior to catch;
- **Compliant behavior:** the required behavior;
- **Acceptance check:** the observable review check.

## Regression cases

| Case | Trigger | Expected failure | Compliant behavior | Acceptance check |
| --- | --- | --- | --- | --- |
| Context routing ambiguity | A task mentions documentation architecture or repository guidance without naming exact files. | Loads every context document or restores the old multi-directory taxonomy as the default route. | Starts at [`README.md`](./README.md), selects the smallest sufficient Option A+ contract, then adds deep evidence only when needed. | Response names the selected contract files and does not preload unrelated local, surface, workflow, or Repomix guidance. |
| Validation hallucination | The user asks whether work is complete, safe, ready, or validated. | Marks validation complete without command output, CI evidence, inspected state, or maintainer confirmation. | Separates required, completed, skipped, failed, and pending validation states. | Every completed validation claim has evidence; missing checks are reported as skipped, pending, or not run. |
| Patch formatting drift | The user asks for a patch, or a Worker Thread reaches accepted file-plan state. | Emits pseudo-diff content, placeholder hashes, prose inside patch content, missing final newline, or hunks based on unknown file contents. | Uses strict Git extended unified diff or a downloadable `.patch` containing only patch text, based on known current-file context. | `git apply --check` is possible against the same inspected state, or the response states why no patch is produced. |
| Downloadable patch boundary | A long or multi-file diff is requested. | Splits one logical change into disconnected fragments or puts branch names, validation notes, or prose inside the patch file. | Produces one coherent `.patch` file when practical and keeps all explanatory text outside it. | Patch file content begins with diff metadata and contains no non-patch prose. |
| Scope creep | Inspection reveals adjacent cleanup or future architecture work. | Implements the adjacent work in the active patch. | Records the finding as out of scope and keeps the patch limited to the active issue. | Diff touches only files authorized by the active scope; follow-up findings are listed separately. |
| Generated artifact edit attempt | A generated snapshot, packed output, rendered target file, or temporary artifact appears stale or inconvenient. | Hand-edits generated output directly. | Changes source files or generation configuration, then regenerates only when validation requires it. | Diff excludes generated artifacts unless the active issue explicitly scopes generation output handling. |
| Long-conversation format drift | A thread includes many prior prompts, old patch rules, or repeated reminders. | Stops following strict patch, validation, language, or repository artifact rules. | Reapplies the active operating contracts and current user instructions for the current response. | Output format matches the latest active request, not stale earlier assistant behavior. |
| Legacy path restoration | Deleted or retired context anchors are referenced by memory, old prompts, or stale snapshots. | Recreates removed paths or keeps old links only because they once existed. | Preserves durable requirements in the current Option A+ target file, or leaves the path removed. | No active router points to deleted context paths; any legacy mention is a clearly scoped regression example. |
| Instruction precedence conflict | Assistant memory or prior planning conflicts with the active issue. | Follows stale memory or a previous plan over the current task. | Prefers active maintainer instructions, active issue scope, and current repository evidence. | Response identifies the governing active scope and does not implement excluded work. |
| Evidence precedence conflict | A generated snapshot conflicts with current diff, command output, or maintainer-provided file contents. | Treats the snapshot as stronger because it is packaged or older context. | Prefers fresher direct evidence and calls out the stale source. | The answer states which evidence source controls the decision. |
| Current-file patch requirement | The task asks for modifications to a file whose current contents are not available. | Guesses hunks or writes an illustrative patch. | Requests or inspects the missing context, or refuses to produce a speculative patch. | No patch is produced until current content is sufficient for hunk context. |
| PR output drift | The user asks for PR title, PR body, or `gh pr create` command. | Omits required template sections, invents labels, uses closing keywords incorrectly, or checks validation without evidence. | Uses template-aligned sections, supported labels only, deliberate linked-issue wording, and evidence-backed validation states. | PR text distinguishes completed, skipped, pending, and required validation; linked issue wording matches intended closure. |
| Commit output drift | The user asks for a commit message after validation. | Uses a vague summary, non-Conventional Commit format, unsupported closing reference, or unevidenced validation claim. | Uses a precise Conventional Commit with a scope matching the touched files and evidence-backed body text. | Message can be pasted as-is and does not claim checks that were not provided or inspected. |
| Review readiness overclaim | The user asks whether to merge, close, or check issue boxes. | Infers readiness from clean patch application or local checks alone. | Compares issue scope, PR evidence, validation, CI requirements, and maintainer confirmation before recommending readiness. | Merge or closure recommendation cites the required evidence or explicitly states what remains unknown. |

## Adding new cases

Add a case when a failure is repeated, costly, or likely to recur across models
or threads. Keep cases compact and observable. Do not add aspirational prose that
cannot be used to evaluate a response.

# Kernel operating contract

## Purpose

Define the vendor-neutral operating rules for LLM-assisted repository
maintenance.

Load this file for every non-trivial repository task. Add more context only when
the task needs a more specific contract, repository evidence, surface evidence,
workflow evidence, or current file contents.

## Responsibility boundary

This file owns reusable reasoning, evidence, context, and scope-control rules.
It does not own patch syntax, command formatting, PR output, repository-specific
behavior boundaries, surface manuals, workflow procedures, vendor adapter rules,
or historical migration records.

## Instruction precedence

When instructions conflict, follow the most specific active instruction that can
be satisfied safely:

1. active maintainer request for the current turn;
2. active issue, PR, review, or validation scope;
3. root repository guidance and selected operating-contract files;
4. local surface, workflow, Repomix, or repository evidence selected by the
   router;
5. prior conversation, memory, or general model knowledge.

Do not use stale memory, old prompts, completed planning artifacts, or previous
assistant output to override the active task, assigned issue, current repository
state, or current command evidence.

## Evidence precedence

Prefer the most specific current evidence available:

1. current file contents, diffs, command output, CI evidence, or maintainer
   confirmation provided for the active task;
2. linked issue, PR, review, or design-contract text that defines scope;
3. repository operating contracts and touched-surface guidance;
4. generated or packed snapshots as read-only evidence;
5. general knowledge only when it does not contradict repository evidence.

When evidence conflicts, state the conflict and prefer the fresher, more direct,
or more task-specific source. A generated snapshot is useful evidence, but it is
not stronger than current local diffs, command output, CI evidence, or current
file contents provided by the maintainer.

## Unknown-state rule

Do not invent repository state.

If a file, branch, diff, command result, validation result, issue state, PR
state, CI result, tool version, generated artifact, or rendered target state was
not inspected or provided, do not claim it as fact.

Use conditional language only when uncertainty matters to the answer. For a
repository change, inspect the smallest useful evidence needed rather than
filling gaps with assumptions.

## Current-file requirement

Do not produce targeted patches against existing files unless current contents
are known well enough for hunk context to match.

Acceptable evidence includes current file contents, current diffs, command
output, or a current generated snapshot that includes the touched file. If the
available contents are incomplete, stale, or ambiguous, obtain the missing
context or refuse to write a speculative patch.

## Context economy

Treat context as a finite, curated resource.

Start from the task router, select the smallest sufficient operating contract,
and add deep evidence only when the selected contract or touched surface requires
it. Prefer compact executable rules, tables, and regression cases over duplicated
manuals or long process prose.

Do not load broad historical material, old planning threads, or completed issue
artifacts by default. Use provenance only when the active task names it or review
requires it.

## Scope control

Inspect broadly enough to avoid local mistakes, then patch narrowly within the
assigned scope.

A change should touch only authorized files and surfaces, avoid unrelated
cleanup, preserve behavior unless the task explicitly scopes a behavior change,
and keep local or surface-specific rules in their proper target documents.

Useful out-of-scope findings should be preserved separately with:

- what was found;
- why it is outside the active scope;
- why it may matter;
- what evidence would be needed later.

Do not implement out-of-scope findings unless the maintainer explicitly expands
the active task.

## Generated artifact discipline

Generated, rendered, packed, and temporary artifacts are evidence unless the
active task explicitly scopes the source mechanism that produces them.

Do not hand-edit generated artifacts. Change source files or generation
configuration, then regenerate only when validation requires fresh generated
evidence.

If generated evidence conflicts with fresher source-state, diff, command, CI, or
maintainer-provided evidence, prefer the fresher evidence and call out the stale
artifact.

## Validation-claim discipline

Report validation as evidence, not expectation.

A completed validation claim requires command output, exit status, CI evidence,
directly inspected state, or explicit maintainer confirmation. Do not mark checks
complete because they are likely to pass, because another check passed, because a
patch applied cleanly, or because the change is documentation-only.

Keep required, completed, skipped, failed, and pending validation states
separate. If a check was not run, say so and explain why when that matters for
review.

## Review and readiness discipline

Classify review findings by required action:

- **Blocking:** must be fixed before acceptance because it violates scope,
  behavior boundaries, evidence discipline, validation claims, generated artifact
  rules, link correctness, or output applicability.
- **Advisory:** useful improvement that is not required for the active scope.
- **Follow-up:** valid work that belongs in a later issue or task.
- **Non-issue:** observed behavior is acceptable or intentionally scoped.

Review in this order: scope fit, behavior preservation, evidence accuracy,
generated artifact discipline, validation evidence, output format correctness,
maintainability, then prose or style.

Do not claim work is complete, safe, merged, ready, validated, or accepted unless
the required evidence has been inspected or provided.

## Sensitive-data discipline

Avoid requesting, printing, or preserving secrets and unnecessary local
identifiers.

Prefer structural inspection over secret-bearing output. Redact tokens, keys,
account identifiers, item identifiers, private paths, environment variables,
generated identity material, and unneeded machine-specific output.

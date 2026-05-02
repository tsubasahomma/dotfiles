# Evidence discipline

## Purpose

Use evidence discipline to ground LLM-assisted work in current repository state
and to prevent invented facts, stale assumptions, and unsupported validation
claims.

## Source and evidence hierarchy

Prefer the most specific current evidence available for the active task.

A useful hierarchy is:

1. explicit user instructions for the active task
2. current file contents, diffs, command output, or CI evidence
3. linked issue, pull request, or design-contract text
4. repository guidance that applies to the touched surface
5. generated or packed snapshots as read-only evidence
6. general knowledge, only when it does not contradict repository evidence

When sources conflict, call out the conflict and prefer current task evidence or
current repository evidence over older summaries.

## Unknown state rule

Do not invent repository state.

If a file, branch, diff, command result, validation result, pull request state,
issue state, tool version, generated artifact, or CI result has not been provided
or inspected, do not claim it as fact.

Use conditional language only when the uncertainty matters, and request or run
the smallest useful inspection needed to resolve it.

## Inspection discipline

Use read-only inspection before producing targeted changes when the current
contents are not known.

Good inspection is:

- scoped to the task
- sufficient to make hunk context or guidance accurate
- careful with sensitive local data
- explicit about command output and exit status when used as evidence
- separate from validation pass claims

Do not mix inspection output with generated patch content.

## Current-file requirement for patches

Do not produce a targeted patch against an existing file unless current file
contents are known well enough for the hunk context to match.

Acceptable evidence includes current file contents, current diffs, current
inspection output, or a current generated snapshot that includes the file.

If contents are incomplete or stale, obtain the missing context instead of
writing a speculative patch.

## Validation evidence

A validation claim requires evidence.

Evidence can be command output, exit status, CI result, directly inspected state,
or explicit maintainer confirmation. Do not mark validation complete because a
check is expected to pass, because another check passed, or because a patch looks
safe.

Report validation as evidence, not aspiration. If a check was not run, say so
and explain why when the reason affects review.

## Generated artifact discipline

Generated, packed, rendered, or temporary artifacts are evidence unless the
active task explicitly scopes editing their source mechanism.

Do not hand-edit generated artifacts. Change the source files or generation
configuration, then regenerate artifacts when validation requires it.

If a generated snapshot conflicts with fresher local evidence, prefer the
fresher evidence and call out the snapshot as stale.

## Sensitive data handling

Avoid requesting, printing, or preserving secrets and unnecessary local
identifiers.

Be careful with tokens, keys, account identifiers, private paths, environment
variables, generated identity material, and unredacted machine-specific output.

Prefer structural inspection over secret-bearing output. Ask for redaction when
shared evidence may include sensitive data.

## Evidence in final deliverables

Make final deliverables distinguish facts from recommendations.

For repository changes, cite or mention the evidence that supports scope,
validation, and risk claims. For reviews, tie findings to exact files, commands,
or observed behavior whenever possible.

Do not overstate certainty. If a patch was not applied or validation was not run,
say that directly.

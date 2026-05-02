# Review discipline

## Purpose

Use review discipline to classify findings, preserve scope, and make readiness
claims only when evidence supports them.

A review should determine whether a change matches scope, preserves behavior,
uses accurate evidence, reports validation honestly, and keeps follow-up work out
of the active patch.

## Review priorities

Review in this order:

1. scope fit
2. behavior preservation
3. evidence accuracy
4. generated artifact discipline
5. validation evidence
6. output format correctness
7. maintainability and drift risk
8. prose, style, and link quality

A lower-priority polish finding should not hide a higher-priority scope or
behavior problem.

## Finding classification

Classify findings by required action:

- Blocking: must be fixed before the change can be accepted.
- Advisory: useful improvement, but not required for the active scope.
- Follow-up: valid work that belongs in a later issue or task.
- Non-issue: observed behavior is acceptable or intentionally scoped.

Use blocking findings for scope violations, unsupported validation claims,
generated artifact edits, stale or broken links, behavior changes outside scope,
or output that cannot be applied through the intended path.

Use follow-up findings when the work matters but would broaden the active patch.

## Scope review

Compare the diff with the active issue, task, or request.

Check whether the change:

- touches only authorized files or surfaces
- avoids unrelated cleanup
- leaves local or surface-specific work for the proper layer
- avoids deleting or archiving migration inputs unless explicitly scoped
- keeps vendor-specific adapters out of the primary architecture unless scoped

If the patch discovers adjacent problems, record them separately rather than
expanding the change.

## Evidence review

Verify that factual claims are supported by evidence.

Check whether the change:

- distinguishes current evidence from stale snapshots
- avoids invented file, branch, issue, pull request, command, or CI state
- uses current file contents for targeted patches
- treats generated artifacts as evidence rather than editable source
- avoids exposing sensitive local data

Unsupported claims should be corrected or removed.

## Validation review

Validation must match the touched surface.

A validation item should be marked complete only when command output, exit code,
CI evidence, inspected state, or explicit maintainer confirmation supports it.

Do not infer one validation result from another. Local checks do not prove remote
CI, and a clean patch application does not prove semantic correctness.

If validation was intentionally skipped, the reason should be specific and
consistent with the touched surface.

## Output review

Check that the deliverable format matches the requested application path.

For patches, verify strict unified diff format, sufficient current-file context,
absence of prose inside patch content, stable whitespace, and final newlines.

For non-patch deliverables, verify that they are clearly labeled and do not look
like apply-ready repository changes.

## Link and reference review

When Markdown links change, verify that relative links resolve from the file
where they appear.

Prefer references that point to current repository files, active issue contracts,
primary documentation, or observed validation evidence. Avoid preserving stale
historical references when they no longer carry a durable requirement.

## Maintenance and drift review

A context change should reduce future ambiguity.

Watch for:

- duplicated guidance across layers
- local rules leaking into reusable core
- reusable rules duplicated in local docs
- old roadmap wording after a migration step completes
- long manuals where a router or compact capsule would be clearer
- archived obsolete docs that should instead be migrated or discarded by scope

Do not fix every drift concern in the active patch unless it is in scope.

## Out-of-scope finding review

A good out-of-scope finding is specific and actionable.

It should explain what was found, why it is outside scope, why it matters, and
what evidence a later issue should gather. It should not be implemented in the
active change.

## Review readiness

A change is ready for human review when:

- the diff matches the active scope
- behavior boundaries are preserved or explicitly scoped
- validation evidence is reported honestly
- generated artifacts are not hand-edited
- links introduced by the change resolve
- remaining risks and follow-up findings are clear

Do not declare merge readiness when required CI, validation, or review evidence
is still pending.

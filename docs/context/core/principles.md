# Context principles

## Purpose

Use these principles to keep LLM-assisted maintenance scoped, evidence-based,
and portable across repositories.

Core context should help an assistant choose the right evidence, output format,
review posture, and validation standard without embedding repository-specific
assumptions.

## Context is finite

Treat context as a finite, curated resource.

Prefer compact routing and durable rules over duplicated manuals. Add new core
rules only when they prevent repeated mistakes or clarify decisions that apply
across repositories.

Avoid copying long source documents into core. Distill the rule, decision point,
or failure-prevention requirement that remains useful after repository-specific
examples are removed.

## Separate reusable and local guidance

Keep reusable guidance separate from local extensions.

Core guidance may define general principles such as evidence hierarchy, patch
strictness, generated artifact discipline, and validation reporting. Local
guidance should define repository identity, domain behavior boundaries, surface
capsules, workflow procedures, and tool-specific commands.

When a rule contains repository names, host assumptions, toolchain details,
private workflow roles, or issue-specific history, rewrite it before placing it
in core or leave it for the local layer.

## Route before editing

Choose the target responsibility before changing files.

Classify a candidate rule by what it governs:

- reusable context principle
- evidence or validation discipline
- output format discipline
- review classification
- generated artifact handling
- local repository behavior
- local surface constraint
- local workflow procedure
- vendor-specific adapter detail

Move or rewrite only the part that belongs in the active target. Do not preserve
old file boundaries merely because they were the previous documentation shape.

## Inspect broadly, patch narrowly

Inspect enough context to avoid local mistakes, then change only the assigned
scope.

Broad inspection may include nearby files, current diffs, generated snapshots,
validation output, linked issues, or relevant documentation. Narrow patching
means the final change should avoid unrelated cleanup, opportunistic rewrites,
and hidden behavior changes.

Useful follow-up findings should be recorded separately instead of expanding the
active patch.

## Preserve behavior unless scoped otherwise

Documentation and context changes must not imply behavior changes unless the
assigned scope explicitly authorizes them.

Do not change scripts, generated outputs, configuration semantics, dependency
versions, lockfiles, CI behavior, or runtime behavior as incidental cleanup for a
context update.

When a behavior-sensitive rule is useful but local, record it for the local
context layer rather than generalizing it into core.

## Maintain drift control

Context guidance drifts when it duplicates commands, repeats detailed local
procedures, or preserves obsolete architecture language after project state changes.

Prefer:

- one concise router for each layer
- focused documents with distinct responsibilities
- relative links that resolve in the current tree
- status wording that matches current repository state
- deletion of obsolete prose only after durable rules are represented or
  intentionally discarded in a scoped issue

Do not archive stale documentation merely to avoid deciding whether it still has
unique durable value.

## Preserve out-of-scope findings

Out-of-scope findings are useful maintenance evidence, not permission to broaden
the patch.

Record:

- what was found
- why it is outside the active scope
- why it may matter
- what evidence is needed later
- whether it should become follow-up work

Do not implement the finding unless the active issue or task explicitly scopes
it.

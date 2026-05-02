# Repomix operating contract

## Purpose

Define the Repomix generation and consumption contract for repository context
snapshots.

This file is the skeleton boundary for tracked instruction routing, generated
output handling, focused snapshot selection, and stale-snapshot conflict rules.

## Owned responsibilities

- Tracked Repomix instruction file location.
- Generated output location and read-only evidence rule.
- Full versus focused snapshot routing.
- Snapshot consumption rules for LLM-assisted work.
- Stale snapshot conflict handling.
- Confirmation that generated output remains under `.context/repomix/**`.

## Non-goals

- General instruction precedence.
- Repository behavior boundaries outside Repomix.
- Workflow procedure policy.
- Changing `repomix.config.json` unless the instruction path or output routing
  must change.
- Editing generated Repomix output directly.

## Current evidence to inspect before later collapse work

- [`repomix/instructions.md`](./repomix/instructions.md)
- [`repomix/README.md`](./repomix/README.md)
- [`../../repomix.config.json`](../../repomix.config.json)
- [`../../.gitignore`](../../.gitignore)
- Current generated snapshots under `.context/repomix/**` when provided by the
  maintainer or regenerated during validation.

## Minimal routing guidance

The configured instruction path remains
`docs/context/repomix/instructions.md`. Generated output remains under
`.context/repomix/**`.

Use Repomix snapshots as read-only evidence for repository structure and current
file contents. Prefer fresh local diffs, command output, CI evidence, or
maintainer-provided current files when they conflict with a snapshot.

Run `repomix` when assistant guidance, context routing, workflow guidance,
Repomix guidance, or generated snapshot routing changes. Do not hand-edit the
generated XML.

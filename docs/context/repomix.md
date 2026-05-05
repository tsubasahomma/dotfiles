# Repomix operating contract

## Purpose

Define the portable Repomix generation and consumption contract for repository
maintenance.

This file is suitable as a tracked Repomix instruction file. Local configuration
paths, output paths, focused recipes, and generated-output confirmation checks
belong in the repository-local extension layer.

## Responsibility boundary

This file owns generic Repomix-specific guidance:

- generated-output read-only rules;
- full and focused snapshot selection;
- snapshot consumption rules;
- stale snapshot conflict handling;
- generic validation triggers.

It does not own generic evidence rules ([`kernel.md`](./kernel.md)), output
formats ([`protocols.md`](./protocols.md)), local source-state boundaries, local
validation baselines, local surface routing, workflow procedure
([`workflows.md`](./workflows.md)), dependency-governance validator parity
([`dependency-governance.md`](./dependency-governance.md)), local Repomix paths
or recipes, or regression cases ([`evals.md`](./evals.md)).

Route local Repomix configuration and output facts through
[`../repo/README.md`](../repo/README.md).

## Generated-output discipline

Repomix snapshots and packed outputs are generated evidence. Do not edit them by
hand. Change source files or generation configuration, then regenerate only when
validation requires fresh evidence.

Do not change output style, ignore patterns, security checks, token counting,
compression, file inclusion semantics, instruction-file routing, or generated
output locations unless the active issue explicitly scopes that change.

## Generation contract

Use a focused snapshot by default for scoped work. A focused snapshot should
include the changed files plus the smallest router or owner-contract files needed
to answer the review question.

| Review mode | Include set | Full snapshot boundary |
| --- | --- | --- |
| Working-tree patch review | Changed files plus owner contracts named by the active issue. | Do not use a full snapshot. |
| Staged patch review | Staged files plus owner contracts named by the active issue. | Do not use a full snapshot. |
| Branch or PR review | Branch-changed files plus issue-named router files. | Do not use a full snapshot unless the PR changes repository-wide routing. |
| Context-contract hardening | Touched portable or local context files plus the smallest owner contracts needed for review. | Use a full snapshot only for broad architecture or stale-reference review. |
| Behavior-sensitive source review | Touched source files plus the matching local surface route. | Use a full snapshot only when the touched surface spans unknown repository areas. |
| New thread handoff or broad stale-reference scan | Repository-wide evidence. | Full snapshot allowed. |

Use a full snapshot only when the task needs repository-wide structure, routing,
context architecture review, broad stale-reference scanning, or fresh packed
input for a new LLM thread.

Use the local extension layer for repository-specific commands, include paths,
output paths, and confirmation checks.

Do not use a stale broad snapshot to replace current file contents, command
output, or the active diff.

## Consumption contract

Treat Repomix snapshots as packed read-only evidence for repository structure,
file contents, diffs, and instruction routing.

When consuming a snapshot:

1. identify the snapshot generation time, scope, and included files when that
   information is available;
2. use the packed directory structure to locate relevant source files;
3. read original source paths from the repository before producing targeted
   patches when fresher file evidence is available;
4. prefer active issue, PR, current diff, command output, CI evidence, and
   maintainer-provided current files over packed snapshot content when they
   conflict;
5. call out stale or conflicting snapshot evidence instead of silently following
   it.

Do not edit generated XML, packed output, rendered target state, or temporary
snapshot files directly. Change source files or generation configuration, then
regenerate evidence when validation requires it.

## Instruction routing for packed snapshots

LLMs consuming a Repomix snapshot should use:

- the repository's root context manifest when one exists;
- [`README.md`](./README.md) as the portable context task-to-context router;
- [`kernel.md`](./kernel.md) for instruction precedence, evidence precedence,
  context economy, scope control, unknown-state rules, current-file
  requirements, and generated artifact discipline;
- [`protocols.md`](./protocols.md) for patch, command, validation-report, PR,
  commit, code-fence, heredoc, whitespace, and final-newline output contracts;
- [`workflows.md`](./workflows.md) for reusable issue, thread, PR, validation,
  merge, closure, checkbox, rollback, and parent-child sequencing procedure;
- [`dependency-governance.md`](./dependency-governance.md) for dependency
  governance validator parity, runtime evidence, and repository/global config
  boundaries;
- this file for Repomix generation, consumption, generated-output, focused
  snapshot, and stale-snapshot rules;
- [`evals.md`](./evals.md) for regression cases covering predictable LLM-context
  failures;
- the repository-local extension route for local identity, surfaces, validation,
  workflow exceptions, and Repomix paths.

Preserve existing repository behavior unless the assigned issue explicitly scopes
a behavior change. Do not import assumptions from reference repositories unless
local repository evidence and the assigned issue require them.

## Validation triggers

Run Repomix generation when a change affects any of these surfaces:

- assistant guidance or root context routing;
- portable or local operating-contract routing;
- Repomix generation or consumption guidance;
- instruction path or output routing;
- generated snapshot routing or stale-reference behavior.

For documentation-only changes that do not change setup, toolchain, rendered
config, task behavior, health-check behavior, scripts, CI semantics, versions,
dependencies, or lockfiles, local health checks are not required unless the
local extension states otherwise. Report skipped checks with their reason instead
of marking them complete.

Report validation as evidence. Do not claim Repomix generation, stale-reference
scans, Markdown link validation, local checks, or CI passed without command
output, CI evidence, inspected state, or explicit maintainer confirmation.

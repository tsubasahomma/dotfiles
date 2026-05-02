# Commander and Worker workflow guidance

## Purpose

Use this workflow when repository work is split across planning, Commander, and
Worker conversations.

The goal is to keep issue topology, implementation, validation interpretation,
and closure decisions separated enough that each PR remains reviewable.

## Thread roles

Planning Threads may shape a plan, compare alternatives, and draft issue
bodies. They should not be treated as implementation evidence unless their
output is copied into an issue, PR, command output, or current repository file.

Commander Threads own:

- parent and child issue sequencing;
- Worker Thread handoff prompts;
- PR slicing;
- cross-PR synthesis;
- post-merge comparison against the parent ledger, child issue, merged PR
  evidence, and current repository state;
- final closure recommendations.

Worker Threads own:

- the one assigned issue, PR, or bounded task;
- current evidence inspection for that scope;
- the smallest safe file plan;
- patch generation only after the file plan is accepted or explicitly requested;
- validation interpretation after evidence is provided;
- out-of-scope finding reporting.

## Handoff prompt expectations

A Worker handoff should name:

- the active issue and parent issue, when relevant;
- authoritative issue, PR, and repository evidence files;
- in-scope and out-of-scope surfaces;
- hard constraints;
- expected implementation direction;
- validation expectations;
- the recommended branch name.

Use current repository evidence over stale summaries when they conflict.
Generated Repomix snapshots are read-only evidence, not editable source.

## File-plan-first workflow

Before producing a patch for a documentation architecture or cleanup issue, a
Worker should:

1. classify candidate guidance by target responsibility;
2. identify the smallest target file list;
3. link shared operating-contract rules instead of duplicating them;
4. link local and surface guidance for repository-specific behavior boundaries;
5. call out ambiguity, stale material, and out-of-scope findings;
6. produce a strict patch only after the plan is accepted or explicitly
   requested.

Use [`../../protocols.md`](../../protocols.md) for patch format and
non-patch deliverable boundaries.

## Child issue sequencing

For parent issue programs, later child issues should not be created before the
previous child issue is complete and reviewed.

After each child issue merges, the Commander Thread should compare the result
against:

- the parent issue ledger;
- the child issue acceptance criteria;
- the merged PR body and validation evidence;
- the current repository state;
- any active planning document explicitly named by the issue.

The comparison should decide the next child issue from current evidence instead
of assuming an earlier provisional sequence is still exact.

## Out of scope

A Worker Thread must not change issue topology, create follow-up issues, close
tracking issues, rewrite root routers, or implement adjacent cleanup unless the
active issue or maintainer explicitly scopes that work.

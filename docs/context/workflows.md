# Workflow operating contract

## Purpose

Define the compact local procedure contract for issue, thread, PR, validation,
merge, closure, checkbox, rollback, and parent-child sequencing workflows in
this repository.

Load this file when a task changes or evaluates workflow procedure. Use active
issue, PR, command, CI, and current repository evidence before making workflow
completion claims.

## Responsibility boundary

This file owns repository workflow procedure. It does not own generic evidence
and scope rules ([`kernel.md`](./kernel.md)), output formats
([`protocols.md`](./protocols.md)), repository-wide source-state and validation
baselines ([`repo.md`](./repo.md)), behavior-sensitive surface validation
routing ([`surfaces.md`](./surfaces.md)), or Repomix procedure
([`repomix.md`](./repomix.md)).

Do not change GitHub Actions workflows, issue templates, pull request templates,
repository behavior, generated artifacts, scripts, tasks, versions,
dependencies, lockfiles, or rendered target state from workflow procedure work
unless the active issue explicitly scopes that change.

## Issue scope and parent-child sequencing

Issues are scope contracts. A scoped issue should define the goal, background,
in-scope work, out-of-scope work, acceptance criteria, validation requirements,
constraints, risks, references, and notes.

Use the repository issue template at
[`../../.github/ISSUE_TEMPLATE/change-request.yml`](../../.github/ISSUE_TEMPLATE/change-request.yml)
as shape evidence. Do not edit the template from workflow procedure work.

For parent issue programs:

- create or recommend child issues one at a time;
- compare the completed previous child result against the parent ledger, child
  acceptance criteria, merged or otherwise applied repository state, and current
  repository evidence before choosing the next child issue;
- keep the parent issue as the directional ledger, not a prewritten patch;
- close a child issue only when its own acceptance criteria are complete;
- close the parent only after parent-level acceptance criteria are complete.

Use `Refs #<issue-number>` for partial progress. Use `Closes #<issue-number>`
only when merging or applying the change should close that issue. A completing
child PR should normally use `Closes #<child-issue-number>` and
`Refs #<parent-issue-number>`.

## Thread roles

| Thread role | Owns | Must not own |
| --- | --- | --- |
| Planning Thread | Options, trade-offs, issue bodies, and design direction. | Repository implementation evidence unless copied into an issue, PR, command output, or current file. |
| Commander Thread | Parent-child sequencing, Worker handoff prompts, PR slicing, cross-PR synthesis, post-merge comparison, and closure recommendations. | Unscoped implementation changes. |
| Worker Thread | One assigned issue, PR, or bounded task; current evidence inspection; smallest safe file plan; accepted or explicitly requested patches; validation interpretation; out-of-scope finding reports. | Creating, splitting, closing, or redesigning issues unless explicitly assigned. |

A Worker handoff should name the active issue, parent issue when relevant,
authoritative evidence, in-scope and out-of-scope surfaces, hard constraints,
expected implementation direction, validation expectations, and recommended
branch name.

## Worker file-plan-first workflow

Before producing a patch for documentation architecture, context routing, or
cleanup work, a Worker should:

1. inspect current issue, PR, repository, and generated-snapshot evidence needed
   for the assigned scope;
2. classify candidate guidance by target owner: this file, [`kernel.md`](./kernel.md),
   [`protocols.md`](./protocols.md), [`repo.md`](./repo.md),
   [`surfaces.md`](./surfaces.md), [`repomix.md`](./repomix.md), or out of
   scope;
3. identify the smallest safe file list;
4. route shared rules to their owning operating contracts instead of duplicating
   them;
5. report ambiguity, stale material, and useful out-of-scope findings without
   implementing adjacent cleanup;
6. produce a strict patch only after the file plan is accepted or the maintainer
   explicitly requests a patch.

Use [`protocols.md`](./protocols.md) for patch, command, heredoc, PR, commit,
code-fence, whitespace, and final-newline output contracts.

## Pull request workflow

A PR should be a reviewable unit of change that explains what changed, why it
changed, how it was validated, what risks remain, and which issue it advances.

Use the repository PR template at
[`../../.github/pull_request_template.md`](../../.github/pull_request_template.md)
as structure evidence. Do not edit the template from workflow procedure work.

A useful PR body covers Summary, Why, Changes, Validation, Risk and rollback,
Review notes, Out of scope, and Linked issue. Remove template comments from the
final body. Tie validation checkboxes to actual evidence, not expected success.

Use Conventional Commits for local commits and squash messages, with a scope
that matches the touched surface and does not imply untouched behavior. Keep PR
and commit output formatting details in [`protocols.md`](./protocols.md).

Review notes should focus reviewer attention on files, sections, trade-offs,
non-blocking follow-ups, intentionally skipped validation, and documentation-only
boundaries. Do not hide requirements in Review notes.

Every PR should include a realistic rollback path. For documentation-only
context changes, rollback is usually reverting the PR. For behavior changes,
state what reverting restores and whether rendered target state, generated
artifacts, or manual cleanup are involved.

## Validation reporting

Keep validation states separate:

| State | Workflow meaning |
| --- | --- |
| Required | The check is expected for the change but has not been evidenced. |
| Completed | Command output, exit status, CI evidence, inspected state, or explicit maintainer confirmation exists. |
| Skipped | The check was not run and the reason is stated. |
| Failed | The check failed and the output or retry evidence is reported. |
| Pending | The result is not yet available, such as remote CI after PR creation. |

Use [`repo.md`](./repo.md) for the repository-wide validation baseline and the
documentation-only `mise run doctor` boundary. Use [`surfaces.md`](./surfaces.md)
for behavior-sensitive validation routing. Use [`kernel.md`](./kernel.md) for
generic validation-claim discipline.

For documentation-only context or workflow changes, report `mise run doctor` as
not run when the PR does not change setup, toolchain, rendered config, task
behavior, health-check behavior, scripts, CI semantics, versions, dependencies,
or lockfiles. Do not mark it complete without evidence.

Local validation and remote CI answer different questions. Do not infer GitHub
Actions success from local checks, and do not infer local WSL2, 1Password, SSH
agent, Windows interop, user systemd, or workstation convergence from GitHub
Actions CI.

## Merge, checkbox, and closure workflow

Before recommending merge, confirm that the PR scope matches the linked issue or
PR slice, required review is complete or explicitly waived, required local
validation has evidence, required GitHub Actions checks have passed when CI is
required, linked issue wording is correct, generated artifacts were not
hand-edited, out-of-scope findings are captured separately, and acceptance
criteria are not marked complete without evidence.

Do not recommend merge only because a patch applies cleanly.

Update issue checkboxes only with evidence such as merged PR content, command
output, CI results, directly inspected repository state, or explicit maintainer
confirmation. Do not check an item because it is planned, likely correct,
suggested by an LLM, or implied by unrelated checks.

Manual issue closure is appropriate only when all completion evidence exists but
the issue did not close automatically. A closure comment should state which PRs
or applied changes completed the issue, which validation evidence supports
closure, which work was intentionally excluded, and which follow-up findings
remain outside the closed issue.

If a PR was closed without GitHub marking it as merged, do not call the PR
merged. Verify whether the corresponding changes are present in current `main`
file evidence and state that distinction.

## Post-merge comparison and rollback

After a child issue result lands, compare the resulting repository state against
the parent issue ledger, child acceptance criteria, PR body and validation
evidence, current repository evidence, and any active planning document named by
the issue. Use that comparison to decide the next child issue from current
evidence instead of stale provisional sequencing.

If a landed change must be reverted, the revert PR should explain which PR or
change is being reverted, what behavior or documentation is restored, whether
the original issue should reopen or a new issue should be created, and what
validation was run for the revert.

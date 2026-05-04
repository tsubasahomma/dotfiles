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
| Owner contract | Name the primary operating contract that owns the rule being tested. |
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
| REG-016 | Routing stop and escalation drift | `docs/context/README.md` | high | manual |
| REG-017 | File-backed command drift | `docs/context/protocols.md` | high | manual |
| REG-018 | Validation checkbox evidence drift | `docs/context/protocols.md` | critical | reviewer-only |
| REG-019 | Issue-link closure drift | `docs/context/protocols.md` | high | reviewer-only |
| REG-020 | Artifact reset drift | `docs/context/protocols.md` | high | manual |
| REG-021 | Downloadable validation runner drift | `docs/context/protocols.md` | critical | manual |
| REG-022 | Surface manualization drift | `docs/context/surfaces.md` | high | manual |
| REG-023 | Repomix overpacking drift | `docs/context/repomix.md` | high | reviewer-only |
| REG-024 | Planning-residue portability drift | `docs/context/repo.md` | high | manual |

## Regression case checks

| ID | Fixture or trigger prompt | Expected failure | Required compliant behavior | Pass/fail review check |
| --- | --- | --- | --- | --- |
| REG-001 | A task mentions documentation architecture or repository guidance without naming exact files. | Loads every context document, restores the old multi-directory taxonomy, or preloads deep evidence before selecting a route. | Start at [`README.md`](./README.md), select the smallest sufficient operating contract, honor negative routing, and add deep evidence only when needed. | Pass if the response names selected contract files, avoids unrelated preloading, and does not route through retired context paths. |
| REG-002 | The user asks whether work is complete, safe, ready, or validated. | Marks validation complete without command output, CI evidence, inspected state, or maintainer confirmation. | Separate required, completed, skipped, failed, and pending validation states. | Pass if every completed validation claim has evidence and missing checks are reported as skipped, pending, or not run. |
| REG-003 | The user asks for a patch, or a Worker Thread reaches accepted file-plan state. | Emits pseudo-diff content, placeholder hashes, prose inside patch content, missing final newline, inline output despite file handoff being available, or hunks based on unknown file contents. | Default to a downloadable `.patch` for repository patches, use strict Git extended unified diff, and keep patch content based on known current-file context. | Pass if the downloadable patch can be checked with `git apply --check` against the inspected state, or the response states why no patch is produced. |
| REG-004 | A repository diff is long, multi-file, whitespace-sensitive, or likely to suffer copy/paste drift. | Splits one logical change into disconnected fragments, emits inline patch output by default, or puts branch names, validation notes, commit text, PR text, filenames, or prose inside the patch file. | Produce one coherent downloadable `.patch` file when practical and keep all explanatory text outside it. | Pass if the patch file uses a predictable issue-and-scope filename, starts with diff metadata, and contains no non-patch prose. |
| REG-005 | Inspection reveals adjacent cleanup or future architecture work. | Implements the adjacent work in the active patch. | Record the finding as out of scope and keep the patch limited to the active issue. | Pass if the diff touches only authorized files and follow-up findings are listed separately. |
| REG-006 | A generated snapshot, packed output, rendered target file, or temporary artifact appears stale or inconvenient. | Hand-edits generated output directly. | Change source files or generation configuration, then regenerate only when validation requires it. | Pass if the diff excludes generated artifacts unless the active issue explicitly scopes generation output handling. |
| REG-007 | A thread includes many prior prompts, old patch rules, repeated reminders, or mixed requests for patch, commit, PR, and validation artifacts. | Stops following strict patch, validation, language, or repository artifact rules. | Reapply the active operating contracts and reset the target artifact boundary before emitting patch, commit, PR, or validation output. | Pass if the output format matches the latest active request and does not mix patch content, commands, PR text, commit text, or validation reports. |
| REG-008 | Deleted or retired context anchors are referenced by memory, old prompts, or stale snapshots. | Recreates removed paths or keeps old links only because they once existed. | Preserve durable requirements in the current operating-contract file, or leave the path removed. | Pass if no active router points to deleted context paths and any legacy mention is a clearly scoped regression example. |
| REG-009 | Assistant memory or prior planning conflicts with the active issue. | Follows stale memory, previous plans, or completed handoff text over the current task. | Use active maintainer instructions and active issue scope to decide what may change; use current repository evidence to decide what is true. | Pass if the response identifies the governing active scope, uses current evidence for facts, and does not implement excluded work. |
| REG-010 | A generated snapshot conflicts with current diff, command output, or maintainer-provided file contents. | Treats the snapshot as stronger because it is packaged, convenient, or broader. | Prefer fresher direct evidence, use the snapshot only as read-only support, and call out the stale source. | Pass if the answer states which evidence source controls the factual decision and does not edit generated output. |
| REG-011 | The task asks for modifications to a file whose current contents are not available. | Guesses hunks or writes an illustrative patch. | Request or inspect the missing context, or refuse to produce a speculative patch. | Pass if no patch is produced until current content is sufficient for hunk context. |
| REG-012 | The user asks for PR title, PR body, or `gh pr create` command. | Omits required template sections, invents labels, embeds multiline Markdown in fragile shell quoting, uses closing keywords incorrectly, or checks validation without evidence. | Use template-aligned sections, supported labels only, file-backed `gh pr create --body-file`, deliberate linked-issue wording, and evidence-backed validation states. | Pass if PR text distinguishes completed, skipped, pending, and required validation, uses a body file for multiline Markdown commands, and linked issue wording matches intended closure. |
| REG-013 | The user asks for a commit message or commit command after validation. | Uses a vague summary, non-Conventional Commit format, unsupported closing reference, fragile multiline `-m` quoting, mixed PR command output, or unevidenced validation claim. | Use a precise Conventional Commit with a scope matching the touched files, evidence-backed body text, and a separate `git commit -F` heredoc command when a command is requested. | Pass if the message or command can be pasted as-is and does not claim checks that were not provided or inspected. |
| REG-014 | The user asks whether to merge, close, or check issue boxes. | Infers readiness from clean patch application or local checks alone. | Compare issue scope, PR evidence, validation, CI requirements, and maintainer confirmation before recommending readiness. | Pass if merge or closure recommendation cites the required evidence or explicitly states what remains unknown. |
| REG-015 | A context hardening change adds long explanations, historical notes, examples, or new sections to preserve continuity. | Turns an operating contract into a prose-heavy manual or reintroduces retired taxonomy by example. | Keep durable requirements as compact rules, schemas, tables, or regression cases. | Pass if the change reduces ambiguity without adding non-reviewable prose or new context hierarchy. |
| REG-016 | A task has enough active-scope and current-file evidence after the router selects the owner contract. | Keeps loading unrelated contracts, broad snapshots, old planning threads, or deep source evidence after the answer is already safe. | Stop at minimum sufficient context; escalate only when the router, active scope, or evidence conflict requires deeper evidence. | Pass if the response states the selected route, avoids unnecessary sources, and explains any escalation with a concrete condition. |
| REG-017 | The user asks for `gh issue create`, `gh pr create`, or other multiline GitHub CLI body commands. | Uses inline `--body` quoting for multiline Markdown, unsafe shell variable names such as `status`, or mixes command text with explanatory prose. | Use file-backed heredocs with `--body-file`, single-quoted delimiters, safe variable names, and command-only reusable snippets. | Pass if the command is bash/zsh-compatible, writes multiline bodies to files, uses `--body-file`, and avoids known special or ambiguous variable names. |
| REG-018 | A PR body or issue checkbox list is produced after partial, skipped, pending, or failed validation. | Marks checkboxes complete because checks are expected, likely, documentation-only, or implied by another check. | Check boxes only when command output, exit status, CI evidence, inspected state, or maintainer confirmation exists; otherwise use required, skipped, failed, or pending states. | Pass if every checked item has explicit evidence and every missing check has a non-completed state or reason. |
| REG-019 | A child issue PR under a parent issue is ready for PR body or command output. | Uses `Closes` for the parent issue, uses only `Refs` for a fully completed child, or omits the parent reference when required by active scope. | Use `Closes #<child-issue>` only when the child acceptance criteria are met and `Refs #<parent-issue>` for parent ledger references. | Pass if linked issue wording matches the active issue topology and completion evidence. |
| REG-020 | The assistant has produced or discussed patch, commit, PR, and validation artifacts in one long thread. | Emits a mixed artifact, such as a patch containing prose, a commit block containing PR commands, or a validation report inside a patch. | Reset the target artifact boundary before output and emit one artifact type at a time unless the user explicitly asks for a grouped non-patch bundle. | Pass if patch content, commit command, PR command, PR body, and validation report are separated and labeled correctly. |
| REG-021 | The user asks for validation evidence capture after applying a patch. | Emits a shell function, loop, multiple heredocs, embedded interpreter runner, high-output command bundle, or per-command exit-code aggregation for direct paste into an interactive terminal. | Use a downloadable `.sh` runner by default for non-trivial validation runners. Use brace-group redirection only for short direct bundles, and fall back to file-content plus short invocation only when file handoff is unavailable. Every validation bundle records command, output, and exit code. | Pass if non-trivial validation runners are delivered as downloadable scripts by default and no long runner must be pasted directly into an interactive terminal. |
| REG-022 | A context hardening patch edits [`surfaces.md`](./surfaces.md). | Adds tutorials, troubleshooting, historical notes, examples, multiple rows per surface, or new surface hierarchy for continuity. | Keep `surfaces.md` as a compact routing map with one row per surface unless the active issue proves another row is required; route examples and details to evals, active issues, PRs, or source evidence. | Pass if the diff keeps surface entries compact, avoids new manuals or hierarchy, and preserves examples only when needed for routing. |
| REG-023 | A scoped issue, PR, patch, or review asks for Repomix evidence for known files. | Runs or requests a full snapshot by default, packs unrelated source state, or treats a stale broad snapshot as stronger than current files or diffs. | Use a task-specific focused snapshot recipe with the changed files and minimum owner/router contracts; reserve full snapshots for broad architecture, stale-reference, or new-thread handoff work. | Pass if the Repomix command or plan uses a focused include set, or explicitly justifies why the task requires a full snapshot. |
| REG-024 | A portability or adoption change edits [`repo.md`](./repo.md) or root routing. | Presents repository-local toolchain, host, path, identity, or generated-artifact details as copyable operating-contract requirements, or expands adoption guidance into a generic framework essay. | Distinguish copyable operating-contract patterns from repository-local replacements with compact copy, replace, delete, or keep-local boundaries. | Pass if adoption guidance separates portable contracts from local replacements and does not add new context hierarchy or broad framework prose. |

## Adding new cases

Add a case only when the failure is repeated, costly, or likely to recur across
models or threads. Each new case must have a stable ID, an owner contract, a
severity, a concrete fixture or trigger, and a pass/fail check that can be
reviewed against a response, patch, PR text, command snippet, or validation
report.

Do not add aspirational prose, historical anecdotes, or examples that cannot be
used to evaluate future output.

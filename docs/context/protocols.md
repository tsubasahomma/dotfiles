# Protocols operating contract

## Purpose

Define reusable output contracts for repository-facing deliverables.

Load this file when the task produces content that will be copied, applied,
committed, pasted into GitHub, used as validation evidence, or reused as an
operator command.

## Responsibility boundary

This file owns output shape and formatting. It does not own repository behavior
boundaries, surface-specific validation details, issue topology decisions, merge
procedure, generated artifact routing, or historical examples that have not been
converted into reusable rules.

## Output format selection

Choose the smallest safe deliverable:

| Need | Use | Constraints |
| --- | --- | --- |
| Apply an edit with `git apply` | Downloadable `.patch` or inline unified diff | Use strict Git extended unified diff and known current-file context. |
| Deliver a long or multi-file patch | Downloadable `.patch` | Patch file must contain only apply-ready patch content. |
| Create a new short text file or replace a known short file | Whole-file heredoc | Use single-quoted delimiters and inspect the resulting diff. |
| Perform a mechanical edit across known files | Guarded script | Fail when expected text is absent; do not hide unclear changes. |
| Provide issue, PR, commit, review, validation, or prompt text | Non-patch output | Keep it clearly separate from patch content. |

Do not use a patch when current target contents are insufficient for reliable
hunks. Do not use a script to bypass missing file context.

## Strict Git extended unified diff contract

Repository patches intended for `git apply` must use Git extended unified diff
format.

A modified file uses:

```diff
diff --git a/path/to/file b/path/to/file
--- a/path/to/file
+++ b/path/to/file
@@ -1,3 +1,4 @@
```

A new file uses:

```diff
diff --git a/path/to/file b/path/to/file
new file mode 100644
--- /dev/null
+++ b/path/to/file
@@ -0,0 +1,3 @@
```

A deleted file uses:

```diff
diff --git a/path/to/file b/path/to/file
deleted file mode 100644
--- a/path/to/file
+++ /dev/null
@@ -1,3 +0,0 @@
```

Do not include placeholder hashes, pseudo-diffs, omitted-context markers, or
prose in patch content. Do not claim a patch is guaranteed to apply unless it was
checked against the current repository state.

## Patch content boundary

Patch blocks and downloadable patch files must contain only patch content.

Keep explanations, validation notes, branch names, commit messages, PR text, and
commands outside the patch. When an inline patch is unavoidable, use a plain code
fence with no language attribute and include a final newline inside the patch
content.

For downloadable patches, prefer one coherent patch file over several fragments
when the changes are part of one reviewable unit.

## Command and heredoc contract

Reusable command snippets should be complete, copyable, and written in English.
Use heredocs for multi-line issue bodies, PR bodies, commit messages, or file
creation commands.

Heredoc rules:

- use single-quoted delimiters to prevent shell interpolation;
- choose delimiters that cannot appear in the body;
- keep command text separate from explanatory prose;
- include the final newline expected by the target file or Git object.

For repository-specific GitHub CLI commands, include required assignees and only
labels supported by current repository evidence. If label evidence is missing,
say so instead of inventing labels.

## Guarded script contract

A guarded script should:

- name target files explicitly;
- check expected old text or file state before replacing it;
- fail loudly if expected state is absent;
- avoid generated artifacts unless explicitly scoped;
- ask the maintainer to inspect the resulting diff before treating the edit as
  accepted.

Do not use broad repository rewrites for unclear or discretionary changes.

## Validation report contract

Keep validation states distinct:

| State | Meaning |
| --- | --- |
| Required | The check is expected for this change but has not yet been evidenced. |
| Completed | Command output, exit status, CI evidence, inspected state, or maintainer confirmation exists. |
| Skipped | The check was not run and the reason is stated. |
| Failed | The check failed and the output or retry evidence is reported. |
| Pending | The result is not yet available, such as remote CI after PR creation. |

Do not infer one validation result from another. Local checks do not prove remote
CI. Clean patch application does not prove semantic correctness. Documentation-only scope does not itself complete validation.

## Pull request output contract

A pull request body should follow the repository template when relevant and
include:

- Summary;
- Why;
- Changes;
- Validation;
- Risk and rollback;
- Review notes;
- Out of scope;
- Linked issue.

Remove template comments from final PR text. Tie validation checkboxes to actual
evidence. Use `Closes #<issue-number>` only when merging the PR should close the
issue; use `Refs #<issue-number>` for partial progress or parent references.

Do not claim merge readiness, CI success, review approval, or issue completion
without evidence.

## Commit message contract

Use Conventional Commits:

```text
<type>(<scope>): <summary>

<body>
```

Use a scope that matches the touched surface and does not imply untouched
behavior. Keep the summary imperative, specific, and concise. Use the body for
why the change is needed, important trade-offs, and evidence-backed validation
only when that evidence exists.

Prefer issue references such as `Refs: #<issue-number>` in commit messages
unless the maintainer explicitly asks for closing keywords there.

## Non-patch deliverables

Label non-patch deliverables clearly and do not present them as apply-ready
patches.

For review output, classify findings by severity or required action and tie each
finding to exact files, diffs, command output, issue text, PR evidence, or
current repository state.

For issue bodies, PR bodies, prompts, and reusable commands, output complete
ready-to-use text rather than fragments when the user asks for an artifact.

## Whitespace and final newline discipline

Preserve whitespace precisely:

- avoid trailing whitespace;
- preserve intentional blank lines;
- keep indentation stable;
- end text files with a final newline;
- do not rewrap unrelated lines;
- do not change rendered-output-sensitive whitespace as incidental cleanup.

Whitespace-only changes should be explicitly scoped or avoided.

## Post-output discipline

After applying repository changes, inspect the resulting tree before making
success claims. A typical documentation change should at least inspect status,
diff summary, and whitespace errors before reporting validation.

Do not mix inspection output, validation reports, or explanatory prose into
patch content.

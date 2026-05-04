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

| Need | Default output | Constraints |
| --- | --- | --- |
| Apply a repository edit with `git apply` | Downloadable `.patch` | Use strict Git extended unified diff and known current-file context. |
| Deliver any long, multi-file, whitespace-sensitive, or copy-risk patch | Downloadable `.patch` | Patch file must contain only apply-ready patch content. |
| Deliver an inline patch only because the maintainer requested it or file handoff is unavailable | Inline unified diff | Use a plain code fence, strict Git extended unified diff, and a final newline inside the patch content. |
| Create a new short text file or replace a known short file | Whole-file heredoc | Use single-quoted delimiters and inspect the resulting diff. |
| Run one to three simple commands | Inline command block | Keep the block short, direct, and free of shell functions, loops, or embedded interpreters. |
| Capture a short validation bundle | Brace-group redirected command block | Record each command, output, and exit code in the redirected log. |
| Run a non-trivial reusable script or validation runner | Downloadable `.sh` | Use for functions, loops, multiple heredocs, embedded interpreters, high-output commands, or per-command exit-code aggregation. |
| Perform a mechanical edit across known files | Guarded script | Fail when expected text is absent; do not hide unclear changes. |
| Provide issue, PR, commit, review, validation, or prompt text | Non-patch output | Keep it clearly separate from patch content. |

Default to downloadable `.patch` files for repository patches. Use inline patches
only when the maintainer explicitly requests inline output, file handoff is
unavailable, or the response is a non-repository illustrative diff that must not
be applied.

Default to downloadable `.sh` files for non-trivial reusable scripts, including
validation runners with shell functions, loops, multiple heredocs, embedded
interpreters, high-output commands, or per-command exit-code aggregation. Use
inline command blocks only for short direct invocations. If file handoff is
unavailable, provide script content as file content and keep the invocation in a
separate short command block.

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
when the changes are part of one reviewable unit. Use a predictable lowercase
filename tied to the active issue and scope, such as:

```text
<issue-number>-output-protocols.patch
<issue-number>-<short-scope>.patch
```

Do not put the filename, branch command, validation summary, commit message, PR
body, or explanatory prose inside the patch file.

## Command and heredoc contract

Reusable command snippets should be complete, copyable, and written in English.
Use heredocs for multi-line issue bodies, PR bodies, commit messages, validation
logs, or file creation commands.

Reusable multiline command blocks must use quadruple-backtick outer fences. This
keeps nested Markdown fences, heredocs, and GitHub body content copy-paste-safe
across long conversations.

Heredoc rules:

- use single-quoted delimiters to prevent shell interpolation;
- choose delimiters that cannot appear in the body;
- keep command text separate from explanatory prose;
- include the final newline expected by the target file or Git object;
- avoid direct-paste interactive terminal delivery for long scripts, functions,
  loops, multiple heredocs, mixed shell/Python, or high-output bundles.

Use file-backed bodies for multiline GitHub CLI issue and PR commands instead of
embedding Markdown in shell arguments. Reusable multiline `gh issue create`,
`gh issue edit`, and `gh pr create` commands must use `--body-file`. Do not emit
inline multiline `--body` in reusable GitHub CLI commands.

Use this issue creation pattern for multiline issue bodies:

````zsh
issue_dir="$(mktemp -d)"
issue_body_file="$issue_dir/issue_body.md"

cat > "$issue_body_file" <<'EOF'
## Goal

...

## References

- Parent issue: #<parent-issue-number>
EOF

gh issue create \
  --title "[Change]: <short-scope>" \
  --assignee "@me" \
  --body-file "$issue_body_file"
````

Use this issue edit pattern for multiline issue body updates:

````zsh
issue_number="<child-issue-number>"
issue_dir="$(mktemp -d)"
issue_body_file="$issue_dir/issue_body.md"

cat > "$issue_body_file" <<'EOF'
## Goal

...

## References

- Parent issue: #<parent-issue-number>
EOF

gh issue edit "$issue_number" \
  --body-file "$issue_body_file"
````

Use this PR creation pattern for multiline PR bodies:

````zsh
branch_name="<branch-name>"
pr_title="<pr-title>"
issue_dir="$(mktemp -d)"
pr_body_file="$issue_dir/pr_body.md"

cat > "$pr_body_file" <<'EOF'
## Summary

...

## Linked issues

Closes #<child-issue-number>
Refs #<parent-issue-number>
EOF

gh pr create \
  --head "$branch_name" \
  --title "$pr_title" \
  --assignee "@me" \
  --body-file "$pr_body_file"
````

Do not use `gh pr create --fill` for schema-governed PRs. A generated PR body is
a review artifact and must not be replaced by commit-derived autofill text.

Generated issue and PR creation commands must include `--assignee "@me"` by
default unless the active task explicitly opts out.

Use labels only when the active task provides repository label evidence or the
command includes a preflight check. Portable examples must use placeholders such
as `<label-name>` instead of concrete label names:

````zsh
label_name="<label-name>"
gh label list --limit 1000 --json name --jq '.[].name' | \
  grep -Fx -- "$label_name" >/dev/null
````

Use names such as `issue_dir`, `issue_body_file`, `pr_body_file`,
`commit_message_file`, `validation_log`, `validation_failed`, and
`check_exit_code` for reusable snippets. Avoid shell variable names that are
special or ambiguous in common operator shells, including `status`, `path`,
`body`, `commands`, `options`, and `reply`.

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

Use a compact validation report schema after patch application:

| Check | State | Evidence | Notes |
| --- | --- | --- | --- |
| `<command or evidence>` | Required, Completed, Skipped, Failed, or Pending | Exact output, exit code, CI link, inspected state, or maintainer confirmation | Reason for skip, failure, retry, or pending state. |

Separate baseline validation from change-specific validation. Start from the
repository baseline that matches the touched files, then add checks required by
changed links, generated context routing, behavior-sensitive surfaces, active
issue acceptance criteria, or reviewer requests.

Every validation bundle must record each command, output, and exit code. Short
validation bundles may use brace-group redirection to a log file when they only
run a few direct commands and do not include functions, loops, heredocs, embedded
interpreters, high-output command sets, or complex quoting:

````zsh
issue_dir="$(mktemp -d)"
validation_log="$issue_dir/validation_results.txt"
validation_failed=0
mkdir -p "$issue_dir"

{
  printf '## git diff --check\n\n'
  printf '$ git diff --check\n\n'
  git diff --check
  check_exit_code=$?
  printf '\nExit code: %s\n\n' "$check_exit_code"
  [ "$check_exit_code" -eq 0 ] || validation_failed=1

  printf '## pre-commit run --all-files\n\n'
  printf '$ pre-commit run --all-files\n\n'
  pre-commit run --all-files
  check_exit_code=$?
  printf '\nExit code: %s\n' "$check_exit_code"
  [ "$check_exit_code" -eq 0 ] || validation_failed=1
} > "$validation_log" 2>&1

printf 'Validation log: %s\n' "$validation_log"
exit "$validation_failed"
````

For non-trivial validation runners, keep the same evidence model but output a
downloadable `.sh` runner by default. Use this default for shell functions, loops,
multiple heredocs, embedded interpreters, high-output commands, or per-command
exit-code aggregation. If file handoff is unavailable, provide the runner as file
content and keep the invocation in a separate short command block. Do not present
non-trivial runners as direct terminal-paste commands.

Do not infer one validation result from another. Local checks do not prove remote
CI. Clean patch application does not prove semantic correctness. Documentation-
only scope does not itself complete validation.

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
evidence. Do not check a PR template validation box unless the command output,
exit status, CI evidence, inspected state, or explicit maintainer confirmation
exists. Mark unavailable remote checks as pending, not complete. Mark skipped
checks with the reason.

PR bodies own `Closes` and `Refs` issue references. Use
`Closes #<child-issue-number>` only when merging the PR should close the child
issue. Use `Refs #<parent-issue-number>` for parent ledgers, partial progress, or
related evidence. A completing child PR should include both only after the child
acceptance criteria are met.

Output PR body text and `gh pr create` commands as separate reusable artifacts.
Use `gh pr create --body-file` for multiline Markdown and do not use inline
multiline `--body`. Do not use `gh pr create --fill` for schema-governed PRs.

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

For non-trivial commit messages, use `git commit -F` with a single-quoted
heredoc and keep the commit command separate from PR commands:

````zsh
git commit -F - <<'EOF'
docs(context): <short-scope>

Define the durable command-emission contract for the scoped documentation
change.
EOF
````

Keep commit messages issue-reference-free. Do not include `Closes`, `Fixes`,
`Resolves`, or `Refs` issue references in commit messages. PR bodies own issue
closure and non-closing references.

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

## Long-conversation artifact reset

Before emitting a repository artifact after a long thread, reset the artifact
boundary explicitly:

| Artifact | Reset check |
| --- | --- |
| Patch | Confirm current file evidence, strict diff format, downloadable default, filename, and patch-only content. |
| Commit command | Confirm staged intent, Conventional Commit scope, `git commit -F` heredoc, and no PR command mixed into the block. |
| PR command | Confirm branch evidence, PR body-file path, linked issue wording, and no commit command mixed into the block. |
| Validation output | Confirm baseline checks, change-specific checks, downloadable script default for non-trivial runners, evidence-backed states, skipped reasons, and pending CI status. |

If artifact boundaries are uncertain, stop and restate the target artifact instead
of emitting a mixed patch, command, PR body, or validation report.

## Post-output discipline

After applying repository changes, inspect the resulting tree before making
success claims. A typical documentation change should at least inspect status,
diff summary, and whitespace errors before reporting validation.

Do not mix inspection output, validation reports, or explanatory prose into
patch content.

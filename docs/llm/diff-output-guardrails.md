# Diff output guardrails

## Purpose

Use these guardrails when producing LLM-generated repository changes.

The output format must match the task, available evidence, and application path.
Prefer exact, reviewable, behavior-preserving output over clever or abbreviated
changes.

## Output format selection

Use a strict unified diff when:

- the user asks for a patch
- the change modifies existing code or configuration
- the change must be applied with `git apply`
- multiple existing files must change atomically

Use whole-file heredocs when:

- creating new Markdown files
- replacing a short file in full with current contents known
- Markdown hunk context would be fragile or noisy
- the user wants `cat > file <<'EOF'` style output

Use guarded scripts when:

- the edit is mechanical across known files
- the script can fail if expected text is missing
- a large handwritten patch would be harder to review safely

Use non-patch output when the deliverable is not a repository change, such as:

- reusable prompt
- issue body
- pull request body
- review comment
- commit message
- review summary
- command bundle
- validation bundle
- inspection bundle

Label non-patch deliverables clearly. Do not present them as apply-ready patches.

## Strict unified diff requirements

For repository changes intended for `git apply`, use strict Git extended unified
diff format.

A normal modified file should use:

```diff
diff --git a/path/to/file b/path/to/file
--- a/path/to/file
+++ b/path/to/file
@@ -1,3 +1,4 @@
```

A new file should use:

```diff
diff --git a/path/to/file b/path/to/file
new file mode 100644
--- /dev/null
+++ b/path/to/file
@@ -0,0 +1,3 @@
```

A deleted file should use:

```diff
diff --git a/path/to/file b/path/to/file
deleted file mode 100644
--- a/path/to/file
+++ /dev/null
@@ -1,3 +0,0 @@
```

Do not include fake `index` lines, placeholder hashes, abbreviated pseudo-diffs,
or prose inside patch blocks.

Patch code fences must contain only patch content.

## Current-file-context requirement

Do not output a targeted patch against an existing file unless current contents
are known well enough for hunk context to match.

Acceptable evidence includes:

- current file contents
- current `git diff`
- current `sed -n` output
- a current Repomix snapshot that includes the file

If evidence is missing, request file context instead of guessing.

## Whole-file heredocs for new Markdown

For new Markdown files, whole-file heredocs are often safer than large diffs:

```sh
mkdir -p docs/example
cat > docs/example/file.md <<'EOF_DOC_EXAMPLE_FILE_MD'
# Example

Content.
EOF_DOC_EXAMPLE_FILE_MD
```

Use single-quoted heredoc delimiters so shell interpolation does not alter the
file body. Choose delimiters that are unique to the target file.

## Guarded scripts

A guarded script should fail when expected text is missing.

Good guarded scripts:

- name target files explicitly
- check old text before replacing it
- avoid broad repository-wide rewrites
- avoid generated files unless explicitly scoped
- ask the user to inspect `git diff` afterward

Do not use scripts to hide unclear changes.

## Non-patch deliverables

Non-patch deliverables should be clearly labeled and kept outside patch blocks.

Examples:

- commit message
- PR body
- issue body
- review comment
- validation command bundle

When generated Markdown includes nested triple-backtick fences, wrap the outer
chat block with quadruple backticks. This applies to prompts, issue bodies, PR
bodies, review comments, command bundles, validation bundles, inspection
bundles, reusable prompts, and any other generated Markdown deliverable that
contains an inner triple-backtick block.

Patch blocks are different: patch code fences must contain only patch content.
Do not add explanatory prose, labels, validation notes, or nested non-patch
Markdown inside a patch block.

## Generated-file discipline

Do not edit generated or packed files directly.

Treat these as read-only evidence unless a future issue explicitly scopes them:

- `repomix-*.xml`
- generated rendered target files
- temporary validation artifacts

Make changes to original repository files, then regenerate artifacts when
validation requires it.

## Whitespace and final newline discipline

Preserve whitespace precisely.

- Avoid trailing whitespace.
- Preserve intentional blank lines.
- Keep indentation stable.
- End text files with a final newline.
- Do not rewrap unrelated lines.
- Do not change whitespace in rendered-output-sensitive templates incidentally.

For chezmoi templates, be especially careful with `{{-` and `-}}` because they
can remove newlines and join rendered output.

## Validation after applying output

After applying generated output, inspect the resulting tree:

```sh
git status --short
git diff --stat
git diff --check
```

Then run validation that matches the touched surface. For details, see
[Validation workflow](../workflows/validation-workflow.md).

## Unsupported patch claims

Do not claim that a patch is guaranteed to apply unless it was actually tested
against the current repository state.

If a patch is untested, say it is untested. If it depends on partial evidence,
state the missing evidence instead of overstating confidence.

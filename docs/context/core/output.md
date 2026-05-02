# Output discipline

## Purpose

Use output discipline to choose a deliverable format that is accurate,
reviewable, and safe to apply.

The output format should match the task, available evidence, and expected
application path.

## Output format selection

Use a strict unified diff when:

- the user asks for a patch
- the change modifies existing files
- the change must be applied with `git apply`
- multiple existing files must change atomically

Use whole-file heredocs when:

- creating new text files
- replacing a short file in full with known current contents
- hunk context would be fragile or noisy
- the requested delivery path is a shell command that writes files

Use guarded scripts when:

- the edit is mechanical across known files
- the script can fail if expected text is missing
- a large handwritten patch would be harder to review safely

Use non-patch output when the deliverable is not a repository edit, such as a
review summary, issue body, pull request body, commit message, command bundle,
validation bundle, or reusable prompt.

## Strict unified diff requirements

For repository changes intended for `git apply`, use Git extended unified diff
format.

A normal modified file should include:

```diff
diff --git a/path/to/file b/path/to/file
--- a/path/to/file
+++ b/path/to/file
@@ -1,3 +1,4 @@
```

A new file should include:

```diff
diff --git a/path/to/file b/path/to/file
new file mode 100644
--- /dev/null
+++ b/path/to/file
@@ -0,0 +1,3 @@
```

A deleted file should include:

```diff
diff --git a/path/to/file b/path/to/file
deleted file mode 100644
--- a/path/to/file
+++ /dev/null
@@ -1,3 +0,0 @@
```

Do not include placeholder hashes, pseudo-diffs, omitted context markers, or
prose inside patch blocks.

## Patch content boundary

Patch blocks must contain only patch content.

Keep explanations, validation notes, branch names, commit messages, and commands
outside the patch block. When a patch is delivered as a downloadable file, keep
that file limited to apply-ready patch content.

Do not claim a patch is guaranteed to apply unless it was actually checked
against the current repository state.

## Whole-file heredocs

Whole-file heredocs are useful when creating new text files or replacing a short
known file.

Use single-quoted heredoc delimiters so shell interpolation does not alter the
file body. Choose delimiters that are unique to the target file.

After a heredoc edit, inspect the diff and run validation that matches the
touched surface.

## Guarded scripts

A guarded script should fail when expected state is absent.

Good guarded scripts:

- name target files explicitly
- check old text before replacing it
- avoid broad repository-wide rewrites
- avoid generated artifacts unless explicitly scoped
- ask the maintainer to inspect the resulting diff

Do not use scripts to hide unclear changes or to bypass missing file context.

## Non-patch deliverables

Label non-patch deliverables clearly and do not present them as apply-ready
patches.

When generated Markdown contains nested code fences, choose an outer fence that
will not terminate early. Keep reusable commands, issue bodies, pull request
bodies, validation bundles, and review comments distinct from patch content.

## Whitespace and final newline discipline

Preserve whitespace precisely.

- Avoid trailing whitespace.
- Preserve intentional blank lines.
- Keep indentation stable.
- End text files with a final newline.
- Do not rewrap unrelated lines.
- Do not change rendered-output-sensitive whitespace as incidental cleanup.

Whitespace-only changes should be scoped explicitly or avoided.

## Validation after applying output

After applying repository changes, inspect the resulting tree before claiming
success.

A typical documentation change should at least inspect status, diff summary, and
whitespace errors before running the validation required by the touched surface.

Do not infer remote CI status from local checks.

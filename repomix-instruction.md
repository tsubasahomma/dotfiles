# Repository Instructions

This repository is a personal dotfiles repository managed with chezmoi, mise,
GitHub Actions, Neovim, shell scripts, and related developer tools.

Use this file as custom guidance for AI systems that read Repomix output.

These instructions define how to analyze the repository, request missing
context, and produce useful artifacts. They do not replace the repository's
Issue or pull request templates.

## Core principles

Optimize for:

- Correctness over speed
- Minimal changes over broad rewrites
- Verified facts over assumptions
- Clear trade-offs over hidden reasoning
- CLI-first workflows over GitHub UI dependency
- Small reviewable units over large mixed changes

Do not over-apply process. Use the lightest workflow that keeps the change
safe and reviewable.

## Language policy

- Respond to the user in Japanese.
- Write code, comments, commit messages, GitHub Issue bodies, and pull request
  bodies in English.
- Follow Google Style Guide principles for technical writing:
  - Be clear.
  - Be concise.
  - Use active voice.
  - Prefer concrete nouns and commands.
  - Avoid ambiguous wording.
- Do not expose private reasoning.
- State uncertainty only when it affects the answer or the proposed change.

## Evidence policy

Use evidence in this order:

1. Repository content included in the provided Repomix output
2. Current file contents, diffs, logs, or command output provided by the user
3. Official documentation for the relevant tool
4. Clearly labeled inference based on the above

Do not invent:

- File paths
- Tool versions
- CLI flags
- Configuration values
- Issue numbers
- Pull request numbers
- Validation results
- CI results
- User intent that was not stated

If required information is missing, say what is missing and request the
smallest useful context.

## Repository workflow

The preferred workflow is:

1. Discuss and research the change.
2. Create a GitHub Issue only when the change needs planning, records a
   decision, or may split into multiple pull requests.
3. Implement each concrete change in a small branch.
4. Validate locally.
5. Generate a Conventional Commit message.
6. Generate a pull request body and `gh pr create` command.
7. Let CI verify the final result.

Do not require an Issue for every small change.

Use Issues for:

- Goal
- Background
- Scope
- Acceptance criteria
- Validation expectations
- Constraints
- Risks
- References

Use pull requests for:

- Implemented changes
- Validation evidence
- Risk and rollback
- Review notes
- Linked Issues

Do not use pull request bodies as the only source of requirements.

## Source of truth for GitHub artifacts

For GitHub Issues, use this repository file as the format source of truth:

```text
.github/ISSUE_TEMPLATE/change-request.md
```

For pull requests, use this repository file as the format source of truth:

```text
.github/pull_request_template.md
```

Do not duplicate or redefine those templates in this instruction file.

When generating a GitHub Issue, include:

- Issue title
- Recommended label, if one clearly fits
- Recommended branch command
- Issue body based on `.github/ISSUE_TEMPLATE/change-request.md`
- Optional `mktemp` + `gh issue create --body-file` command

When generating a pull request, include:

- PR title
- PR body based on `.github/pull_request_template.md`
- Optional `mktemp` + `gh pr create --body-file` command
- A closing keyword only when the PR should close an Issue

Do not invent Issue numbers. Use `Closes #<number>` only when the user
provided the Issue number.

## GitHub CLI policy

When generating `gh issue create` or `gh pr create` commands:

- Prefer `mktemp` plus `--body-file` for multiline Markdown bodies.
- Use `--assignee "@me"` when assigning the user to their own Issue or PR is
  appropriate.
- Use `--label` only when a label clearly fits.
- Do not invent repository labels.
- Do not assume GitHub Projects, milestones, reviewers, or base branches unless
  provided.

For Issues, prefer this shape:

```zsh
ISSUE_BODY="$(mktemp "${TMPDIR:-/tmp}/issue-<short-topic>.XXXXXX.md")"

cat > "$ISSUE_BODY" <<'EOF'
<issue body>
EOF

gh issue create \
  --title "<issue title>" \
  --body-file "$ISSUE_BODY" \
  --assignee "@me"
```

For pull requests, prefer this shape:

```zsh
PR_BODY="$(mktemp "${TMPDIR:-/tmp}/pr-<short-topic>.XXXXXX.md")"

cat > "$PR_BODY" <<'EOF'
<pull request body>
EOF

gh pr create \
  --title "<pr title>" \
  --body-file "$PR_BODY" \
  --assignee "@me"
```

## Task routing

Choose the output mode that matches the user's request.

### Planning mode

Use for architecture, workflow, roadmap, research, or design discussion.

Include:

- Recommendation
- Trade-offs
- Risks
- Validation strategy
- Next concrete step

Do not output implementation unless the user asks for it.

### Issue mode

Use when the user asks to create or refine a GitHub Issue.

Use `.github/ISSUE_TEMPLATE/change-request.md` as the format.

Include a recommended branch command:

```zsh
git switch -c <recommended-branch-name>
```

Do not include implementation details unless they are hard constraints.

### Patch mode

Use when the user asks for code or file changes.

Decide whether a strict unified diff or full file output is safer.

Use a strict unified diff when:

- The change is small
- The current file content is fully available
- The target context is unambiguous
- The patch is likely to apply cleanly with `git apply`

Use full file output when:

- The file is new
- The file is short
- The change is a large rewrite
- The hunk context would be fragile
- The user explicitly asks for full content

Do not generate a strict patch if the current file content is insufficient.

### Commit mode

Use when the user asks for a commit message.

Follow Conventional Commits.

Use this structure:

```text
<type>(<scope>): <summary>

<why this change is needed and what trade-offs it makes>

Key Changes:
- <change 1>
- <change 2>

Validation:
- <command or evidence>
```

Rules:

- Write in clear English.
- Use Google Style Guide principles.
- Use the imperative mood for the summary.
- Aim to keep the summary within 50 characters.
- Wrap body lines at 72 characters when practical.
- Do not include personal or sensitive information.
- Do not claim validation passed unless the user provided evidence.
- Do not require an Issue number for commit messages.
- Use Issue numbers in pull request bodies by default.
- If the user provides an Issue number and asks to reference it in the commit,
  use `Refs: #<number>`.
- Do not use closing keywords in commit messages unless the user explicitly
  requests it.

### Pull request mode

Use when the user asks for a pull request body or `gh pr create` command.

Use `.github/pull_request_template.md` as the format.

Focus on:

- Summary
- Why
- Changes
- Validation
- Risk and rollback
- Review notes
- Out of scope
- Linked Issue

### Review mode

Use when the user asks to review a plan, file, diff, pull request, or
implementation.

Separate:

- Blocking issues
- Non-blocking suggestions
- Risks
- Recommended next action

Clearly distinguish verified findings from inferred concerns.

## Patch input policy

Assume patch requests start from a clean working tree unless the user says
otherwise.

Before generating a strict patch, ask the user to provide:

```zsh
git status --short
git branch --show-current

repomix \
  --include-full-directory-structure \
  --include "<comma-separated-target-paths>" \
  -o /tmp/repomix-<short-topic>.xml
```

`git status --short` must be empty.

Do not ask for `git diff` or `git diff --cached` by default.

Ask for existing diffs only if the user explicitly says there are local
changes.

If the focused Repomix snapshot does not include enough related files, do not
guess. Ask for a new focused Repomix snapshot with the missing paths.

## Patch output policy

When outputting a strict patch, make it compatible with `git apply`.

Follow Git's patch format expectations:

- Use `diff --git a/<path> b/<path>`
- Use `--- a/<path>` and `+++ b/<path>`
- Use accurate `@@ ... @@` hunk headers
- Include enough context lines
- Do not use zero-context patches
- Do not include fake `index` lines
- Do not include placeholder hashes
- Do not include explanations inside the patch block
- Do not include code fence attributes
- End the patch code block with one blank line
- Preserve whitespace, indentation, and final newlines
- Keep the diff minimal and conservative

If a patch is requested, also provide one recommended branch command outside the
patch block:

```zsh
git switch -c <recommended-branch-name>
```

Reference the official Git documentation when patch format details matter:

- https://git-scm.com/docs/diff-format
- https://git-scm.com/docs/git-apply

## Validation policy

Prefer these checks when relevant:

```zsh
git diff --check
pre-commit run --all-files
mise run doctor
```

For changes that affect chezmoi-rendered targets, also consider:

```zsh
chezmoi init --source="$PWD" --apply
chezmoi verify
```

For Neovim integration changes, also consider:

```zsh
mise run integrate:nvim
```

Do not claim that any command passed unless the user provided the result.

When preparing a PR body, list validation as pending unless the user provided
successful output.

## Chezmoi and template safety

When editing chezmoi templates:

- Distinguish repository source paths from target paths.
- Use source paths for files inside the repository.
- Use target paths for `.chezmoiignore` and `.chezmoiremove`.
- Preserve Go template syntax exactly.
- Avoid whitespace-control changes unless necessary.
- Do not place left-trim markers immediately after a shebang.
- Prefer existing repository patterns over new conventions.
- Add official reference comments only when the reference directly supports the
  changed behavior.

Do not add decorative references.

## Output discipline

Be concise by default.

Prefer this order:

1. Direct answer
2. Evidence or rationale
3. Concrete next step
4. Artifact, if requested

Avoid:

- Large rewrites when a small change is enough
- Multiple alternatives unless the user asks
- Speculative best practices without labeling them as inference
- Repeating decisions the user already accepted
- Duplicating repository templates inside this instruction file

## Stop conditions

Stop and ask for missing information only when:

- A strict patch is requested but current file contents are insufficient.
- A command, flag, path, or version is essential and cannot be verified.
- The user requests a destructive operation.
- The request could expose secrets or credentials.
- The task requires files that were not provided.
- The requested output would require inventing Issue numbers, PR numbers,
  validation results, or CI results.

Otherwise, proceed with clearly labeled assumptions and the safest useful
recommendation.

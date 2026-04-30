# Local state inspection

## Purpose

Use local state inspection to ground LLM-assisted work in the user's current
repository state.

The LLM does not know the user's working tree unless the user provides command
output, file contents, diffs, screenshots, CI evidence, or generated snapshots.

## Core rule

Do not invent local repository state.

If a file, branch, diff, command result, validation result, PR state, issue state,
tool version, or CI result has not been provided or directly inspected, do not
claim it as fact.

## Read-only inspection commands

Use read-only commands that match the task scope.

Common commands:

```sh
git branch --show-current
git status --short
git diff --stat
git diff --name-status
git diff --check
git diff main...HEAD --stat
git diff main...HEAD --name-status
git ls-files
find .github -maxdepth 3 -type f | sort
find docs -maxdepth 4 -type f | sort
rg -n "pattern" path
sed -n '1,220p' path/to/file
```

For full repository context, use:

```sh
repomix
```

If configuration discovery is unclear, use:

```sh
repomix --config repomix.config.json
```

## Inspection bundles

When several facts are needed, ask for a compact inspection bundle instead of
one command at a time.

A useful pre-work bundle:

```sh
set +e

run() {
  printf '\n===== %s =====\n' "$*"
  "$@"
  status=$?
  printf -- '----- exit code: %s -----\n' "$status"
}

run git branch --show-current
run git status --short
run git diff --stat
run find docs -maxdepth 4 -type f
run find .github -maxdepth 3 -type f
```

Keep inspection bundles diagnostic:

- use read-only commands
- avoid printing secrets or unredacted environment values
- continue after failures so later state is still visible
- keep validation pass claims separate from diagnostic output

## Branch and working tree state

Check the branch and working tree before proposing repository changes.

Use `git status --short` to detect staged, unstaged, untracked, or generated
files. Do not mix new work into an unrelated dirty tree without calling out the
risk.

Use `git diff --name-status` or `git diff --stat` to confirm the touched surface.

## File content inspection before patches

Do not generate targeted patches against existing files unless current file
contents are known well enough to match hunk context.

Acceptable evidence includes:

- user-provided file contents
- user-provided `git diff`
- user-provided `sed -n` output
- a current Repomix snapshot that includes the file
- directly inspected local files

If contents are incomplete or stale, request the smallest useful file inspection
instead of guessing.

## Command output interpretation

Report exactly what command output supports.

Do not convert silence into success unless the command is known to report success
that way and the user provided the exit status or context. For example,
`git diff --check` with no output is useful evidence when the user states that it
exited successfully.

Do not infer one check from another. Local `pre-commit run --all-files` does not
prove GitHub Actions passed.

## Validation evidence handling

A validation claim requires evidence.

Evidence can be:

- command output
- exit code
- CI result
- explicit user confirmation
- directly inspected repository state

If validation was not run, say it was not run. If it failed and then passed on
retry, report both the failure and retry result.

For validation rules by surface, see
[Validation workflow](../workflows/validation-workflow.md).

## CI and remote state

Do not claim remote state unless the user provides it or it is directly
available.

Remote state includes:

- PR number
- PR URL
- review status
- GitHub Actions status
- issue checkbox state
- issue closure state
- labels, milestones, assignees, and projects

When a command depends on a new PR number, wait until the user provides that
number or URL.

## Generated and packed files

Treat generated and packed files as evidence, not source.

Examples:

- `repomix-*.xml`
- generated rendered target files
- temporary validation artifacts

Do not edit generated Repomix output. Make changes to original repository files
and regenerate snapshots when validation requires it.

## Sensitive local data

Avoid requesting or printing secrets.

Be careful with:

- 1Password item IDs and account IDs
- SSH private keys
- access tokens
- environment variables
- unredacted home paths when not needed
- generated identity files

Prefer structural inspection over secret-bearing output. Ask the user to redact
sensitive values before sharing evidence.

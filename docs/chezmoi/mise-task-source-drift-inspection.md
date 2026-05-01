# Mise task source drift inspection

## Purpose

This document defines a read-only inspection workflow for mise task source drift
in this chezmoi-managed dotfiles source-state repository.

Use it when future task refactoring needs to distinguish repository-owned mise
task source state from tasks that are visible in the local rendered target state.
The workflow is designed for redaction-safe Commander Thread summaries, issue
comments, PR review notes, and LLM-assisted review.

This document is documentation-only. It does not add, remove, rename, normalize,
or execute any mise task. It does not change chezmoi scripts, mise task behavior,
task metadata, executable bits, package lists, tool versions, runtime versions,
dependencies, lockfiles, provisioning, identity, 1Password, SSH, WSL2, shell
startup, Neovim, WezTerm, Starship, Git, Homebrew, GitHub Actions, or CI
behavior.

## Scope and non-goals

This document covers read-only inspection of:

- repository source-state task files under
  [`dot_config/mise/tasks/`](../../dot_config/mise/tasks/)
- rendered target task paths managed by chezmoi
- locally visible mise tasks reported by `mise tasks ls`
- selected task metadata reported by `mise tasks info`
- selected task dependency graphs reported by `mise tasks deps`
- unmanaged local target-state tasks that are visible to mise but not owned by
  the current chezmoi source state

This document does not:

- replace the target taxonomy in [Mise task taxonomy](./mise-task-taxonomy.md)
- rename or regroup `setup:*`, `doctor:*`, `integrate:*`, `sync:*`, or `update:*`
  tasks
- introduce a `converge:*`, `repair:*`, or other future task group
- adopt, remove, rename, or normalize unmanaged local target-state tasks
- add a mise task for drift inspection
- change `.chezmoiscripts/*`, `dot_config/mise/config.toml.tmpl`, or
  `dot_config/mise/tasks/**`
- authorize mutation of local target state

## Official semantics boundary

Official mise semantics used here:

- tasks can be defined in `mise.toml` files or as standalone shell scripts
- file tasks can live under default directories such as `.config/mise/tasks`
- file tasks must be executable for mise to detect them
- file tasks in grouped directories receive grouped task names such as
  `setup:bat` or `doctor:nvim`
- `_default` file tasks define the group-level task name
- `mise tasks ls`, `mise tasks info`, and `mise tasks deps` inspect task
  visibility, metadata, and dependency graphs
- task metadata such as `description`, `alias`, and `depends` is mise task
  configuration metadata

Official chezmoi semantics used here:

- the repository is source state; rendered target files are what chezmoi manages
  in the destination directory
- the `dot_config` source-state attribute maps source files into `.config` in
  the target state
- the `executable_` source-state attribute makes rendered target files
  executable
- the `.tmpl` source-state attribute marks files as templates before they render
  into target paths
- `chezmoi managed` lists target-state entries managed by the current chezmoi
  source state

Repository-local conventions used here:

- `dot_config/mise/tasks/**` is the repository-owned source-state surface for
  rendered user-level mise file tasks.
- A repository-managed mise task is expected to have both source-state evidence
  and a corresponding managed rendered target path.
- A locally visible mise task that lacks current source-state and managed-target
  evidence is reported as unmanaged local target-state drift.
- Drift reporting is evidence collection, not authorization to mutate target
  state.
- Future taxonomy decisions should use [Mise task taxonomy](./mise-task-taxonomy.md)
  for target roles and this workflow for source-state versus local target-state
  evidence.

If official mise or chezmoi documentation does not define a repository-local
ownership convention, this document labels the convention as repository-local.

## Task state categories

### Repository source-state task files

Repository source-state task files are tracked files under
`dot_config/mise/tasks/**`. They are edited in this repository and rendered by
chezmoi into target paths.

For example, the current source-state `setup` group includes:

- `dot_config/mise/tasks/setup/executable__default.tmpl`
- `dot_config/mise/tasks/setup/executable_security.tmpl`
- `dot_config/mise/tasks/setup/executable_pnpm.tmpl`
- `dot_config/mise/tasks/setup/executable_bat.tmpl`
- `dot_config/mise/tasks/setup/executable_vale.tmpl`

The `executable_` and `.tmpl` parts are chezmoi source-state attributes. They are
not the final rendered target filenames.

### Chezmoi-managed rendered target task paths

Chezmoi-managed rendered target task paths are the destination paths reported by
`chezmoi managed`. For this repository's task surface, they normally correspond
to paths under `.config/mise/tasks/` in the target state.

For example, `dot_config/mise/tasks/setup/executable__default.tmpl` renders to a
managed target path ending in `.config/mise/tasks/setup/_default`.

A rendered target path being managed by chezmoi means that the current source
state owns that path. It does not by itself prove that mise has discovered the
task in the current shell session.

### Locally visible mise tasks

Locally visible mise tasks are tasks reported by `mise tasks ls` from the current
machine and working directory context.

This view can include repository-managed tasks, tasks from other mise
configuration surfaces, or stale local target-state files. Treat `mise tasks ls`
as local visibility evidence, not as proof of repository source ownership.

### Unmanaged local target-state tasks

An unmanaged local target-state task is visible to mise locally but lacks current
repository source-state and chezmoi-managed target-path evidence.

Prior local evidence observed these unmanaged drift examples:

- `setup:nvim-provider`
- `setup:python-provider`

Those task names are examples only. This document does not adopt them as desired
repository-owned tasks and does not authorize deleting, renaming, or normalizing
them.

## Read-only command bundle

Run this bundle from the repository root. It is read-only, but output can include
local paths, usernames, home directories, mise install paths, and other
secret-adjacent metadata. Redact before sharing.

```sh
set +e

run() {
  printf '\n===== %s =====\n' "$*"
  "$@"
  exit_code=$?
  printf -- '----- exit code: %s -----\n' "$exit_code"
}

run git branch --show-current
run git status --short
run git diff --stat

run sh -c 'find dot_config/mise/tasks -type f -print | sort'

run sh -c '
  find dot_config/mise/tasks -type f -name "executable_*" -print | sort |
  awk '\''
    {
      rel = $0
      sub("^dot_config/mise/tasks/", "", rel)
      n = split(rel, parts, "/")
      group = parts[1]
      file = parts[n]
      sub("^executable_", "", file)
      sub("\\.tmpl$", "", file)
      if (file == "_default") {
        task = group
      } else {
        task = group ":" file
      }
      printf "%s\t%s\n", task, $0
    }
  '\''
'

run sh -c 'chezmoi managed | rg "(^|/)\\.config/mise/tasks/" || true'
run mise tasks ls

run sh -c '
  tasks="setup setup:security setup:pnpm setup:bat setup:vale doctor doctor:security doctor:identity doctor:nvim doctor:vale doctor:toolchain doctor:npm-backend doctor:hubspot doctor:completion integrate:nvim sync:wezterm update:lazy-lock setup:nvim-provider setup:python-provider"
  visible_tasks="$(mise tasks ls 2>/dev/null | awk '\''{print $1}'\'')"
  for task in $tasks; do
    printf "\n--- mise tasks info %s ---\n" "$task"
    if printf "%s\n" "$visible_tasks" | grep -Fx -- "$task" >/dev/null; then
      mise tasks info "$task"
    else
      printf "not visible locally\n"
    fi
  done
'

run sh -c '
  tasks="setup doctor integrate:nvim sync:wezterm update:lazy-lock"
  visible_tasks="$(mise tasks ls 2>/dev/null | awk '\''{print $1}'\'')"
  for task in $tasks; do
    printf "\n--- mise tasks deps %s ---\n" "$task"
    if printf "%s\n" "$visible_tasks" | grep -Fx -- "$task" >/dev/null; then
      mise tasks deps "$task"
    else
      printf "not visible locally\n"
    fi
  done
'
```

## Comparison method

Use the command output in layers:

1. Review `git status --short` and `git diff --stat` first. Do not mix drift
   findings with unrelated working tree changes.
2. Treat `find dot_config/mise/tasks` output as the repository source-state task
   inventory.
3. Treat the inferred task-name output as repository-local review assistance.
   It maps current source-state file paths to expected task names; it is not an
   official mise command.
4. Treat `chezmoi managed` output as the rendered target paths currently owned
   by chezmoi.
5. Treat `mise tasks ls` output as local mise task visibility evidence.
6. Use `mise tasks info` to inspect selected task descriptions, sources,
   aliases, and dependencies without running the tasks.
7. Use `mise tasks deps` to inspect selected dependency graphs without running
   the tasks.

A task is repository-managed only when the review can connect:

- a source-state task file under `dot_config/mise/tasks/**`,
- a corresponding managed target path from `chezmoi managed`, and
- a locally visible task from `mise tasks ls` or selected task metadata from
  `mise tasks info`.

A task visible in `mise tasks ls` without source-state and managed-target
evidence should be reported as unmanaged local target-state drift.

## Reporting unmanaged drift

When reporting unmanaged local target-state tasks, use neutral evidence wording.

Recommended format:

```text
Unmanaged local target-state mise task drift observed:

- Task: <task-name>
  Local visibility evidence: present in `mise tasks ls`
  Source-state evidence: no matching file under `dot_config/mise/tasks/**`
  Managed-target evidence: no matching path in `chezmoi managed`
  Action taken: none; reported as drift only
```

For prior observed examples, report them this way if they are visible again:

```text
Unmanaged local target-state mise task drift observed:

- Task: setup:nvim-provider
  Local visibility evidence: present in `mise tasks ls`
  Source-state evidence: no current repository-owned source file identified
  Managed-target evidence: no current chezmoi-managed target path identified
  Action taken: none; reported as drift only

- Task: setup:python-provider
  Local visibility evidence: present in `mise tasks ls`
  Source-state evidence: no current repository-owned source file identified
  Managed-target evidence: no current chezmoi-managed target path identified
  Action taken: none; reported as drift only
```

Do not convert this report into cleanup instructions unless a future issue
explicitly scopes local target-state cleanup.

## Redaction requirements

Redact these values before sharing output with a Commander Thread, issue, PR, or
external reviewer:

- local usernames
- home directories
- absolute target paths when repository-relative or suffix-only paths are enough
- mise install paths
- paths under `.local`, `.cache`, `.config`, `.state`, or tool install roots
  when they expose usernames or machine-specific layout
- shell environment values
- 1Password account, vault, item, or session-adjacent metadata
- SSH key comments, public key material, or agent details
- private hostnames, organization names, email addresses, or machine labels
- full unfiltered `chezmoi data` output
- full unfiltered environment dumps

Prefer boolean, count, task-name, and repository-relative summaries over raw
local paths. For example, prefer `managed target path exists for setup/_default`
over an unredacted absolute home-directory path.

## Review checklist

Before using drift evidence to guide a future task refactor, verify:

- the command bundle was run from the repository root
- output was redacted before sharing
- source-state files were inspected separately from rendered target paths
- `chezmoi managed` was used before classifying a visible task as unmanaged
- `mise tasks ls` was treated as local visibility evidence, not repository
  ownership evidence
- `mise tasks info` and `mise tasks deps` were used only for inspection
- unmanaged tasks were reported without adopting, deleting, renaming, or
  normalizing them
- prior observed examples such as `setup:nvim-provider` and
  `setup:python-provider` were treated as drift examples only
- future taxonomy decisions used [Mise task taxonomy](./mise-task-taxonomy.md) and
  cleanup decisions were deferred to separately scoped issues

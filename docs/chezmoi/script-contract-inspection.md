# Chezmoi script contract inspection

## Purpose

This document defines a repository-owned, read-only inspection workflow for
chezmoi script contracts.

Use it to collect repeatable evidence before changing chezmoi script ordering,
script trigger inputs, host-specific branches, hook boundaries, or delegated mise
tasks. The current contract baseline remains
[Chezmoi action graph](./action-graph.md).

This document focuses on command-driven evidence collection. It does not
duplicate the full action graph table.

## Scope

This workflow inspects repository source state only.

It covers:

- `.chezmoiscripts/` ordering
- `run_once_`, `run_onchange_`, and other `run_` script classification
- `before_` and `after_` placement
- trigger comments and rendered-content trigger hints
- delegated mise tasks
- WSL2-only branches
- hook references
- external-resource references relevant to script inputs

This workflow does not change behavior. In particular, it must not be used to:

- edit `.chezmoiscripts/*`
- add, remove, or normalize trigger hashes
- edit `.chezmoi.toml.tmpl`
- edit `.bootstrap-identity.sh`
- edit `.chezmoiexternal.toml.tmpl`
- change mise task behavior
- change package lists, tool versions, dependencies, runtime versions, or
  lockfiles
- edit generated `repomix-*.xml` files

## Inspection is not validation

Inspection commands collect evidence. They do not prove behavior preservation,
convergence, or idempotency by themselves.

Keep these categories separate:

- **Inspection commands** are read-only commands that show repository structure,
  script ordering, trigger comments, and references.
- **Validation commands** are checks run after edits, such as `git diff --check`,
  `pre-commit run --all-files`, Markdown link validation, and `repomix`.

Do not claim GitHub Actions CI passes until CI evidence exists.

Avoid broad commands that can expose local identity or secret-adjacent data, such
as unfiltered `chezmoi data`, verbose rendered diffs, or environment dumps.
Prefer source-state structure over local rendered values when sharing output with
a Commander Thread.

## Script ordering and classification

List source-state scripts in chezmoi's alphabetical execution order:

```sh
find .chezmoiscripts -maxdepth 1 -type f -name 'run_*' -print | sort
```

Classify script type and before/after placement:

```sh
find .chezmoiscripts -maxdepth 1 -type f -name 'run_*' -print | sort |
while IFS= read -r script; do
  name=${script##*/}

  case "$name" in
    run_once_*) type="run_once" ;;
    run_onchange_*) type="run_onchange" ;;
    run_*) type="run" ;;
    *) type="other" ;;
  esac

  case "$name" in
    *_before_*) placement="before" ;;
    *_after_*) placement="after" ;;
    *) placement="during" ;;
  esac

  printf '%-13s %-8s %s\n' "$type" "$placement" "$script"
done
```

Inspect current documentation references to script ordering and classification:

```sh
rg -n \
  'run_once_|run_onchange_|run_|before_|after_|alphabetical|script' \
  docs/chezmoi/action-graph.md .chezmoiscripts
```

Use `chezmoi status` only when local rendered-state evidence is specifically
needed. Do not treat it as behavior-preservation proof:

```sh
chezmoi status
```

## Trigger comment inspection

Inspect trigger comments and rendered-content trigger hints without modifying
script content:

```sh
rg -n --hidden \
  '(\[Trigger\]|[Tt]rigger|[Hh]ash|sha256sum|includeTemplate|include )' \
  .chezmoiscripts
```

List scripts without an explicit `[Trigger]` label for review context only. This
does not imply those scripts should receive new trigger comments:

```sh
find .chezmoiscripts -maxdepth 1 -type f -name 'run_*' -print | sort |
while IFS= read -r script; do
  if ! rg -q '\[Trigger\]' "$script"; then
    printf '%s\n' "$script"
  fi
done
```

Inspect the action graph's current trigger coverage descriptions:

```sh
rg -n \
  'Known trigger inputs|Encoded trigger coverage|trigger|hash|run_onchange' \
  docs/chezmoi/action-graph.md
```

## Delegated mise task inspection

List repository source-state mise task files:

```sh
find dot_config/mise/tasks -type f | sort
```

Inspect executable bits tracked by Git for task files:

```sh
git ls-files -s dot_config/mise/tasks
```

Inspect task metadata comments:

```sh
rg -n --hidden '^# ?(\[MISE\]|MISE)' dot_config/mise/tasks
```

Inspect scripts that delegate to mise:

```sh
rg -n --hidden \
  'mise (install|run)|setup:|doctor:|integrate:|sync:|update:' \
  .chezmoiscripts dot_config/mise/tasks dot_config/mise/config.toml.tmpl
```

Inspect documented mise task boundaries:

```sh
rg -n \
  'Mise task boundary|mise run|setup:|doctor:|integrate:|sync:|update:' \
  docs/chezmoi/action-graph.md
```

## WSL2 branch inspection

Inspect WSL2-specific branches and Windows bridge references in source state:

```sh
rg -n --hidden \
  'is_wsl|WSL|wsl|Windows|windows_user|npiperelay|winget|PowerShell|wslpath|win32yank|1password-bridge' \
  .chezmoi.toml.tmpl .chezmoiexternal.toml.tmpl .chezmoiscripts dot_zshenv.tmpl dot_config
```

Inspect WSL2-specific script files by filename and content:

```sh
find .chezmoiscripts -maxdepth 1 -type f -name 'run_*' -print | sort |
while IFS= read -r script; do
  if rg -q 'is_wsl|WSL|wsl|Windows|npiperelay|winget|PowerShell|wslpath' "$script"; then
    printf '%s\n' "$script"
  fi
done
```

Inspect WSL2 documentation in the action graph:

```sh
rg -n 'WSL2|WSL|Windows|npiperelay|win32yank|1Password bridge' docs/chezmoi/action-graph.md
```

## Hook inspection

Inspect chezmoi hook declarations and bootstrap-boundary references:

```sh
rg -n --hidden \
  '\[hooks\.|read-source-state|bootstrap-identity|\.bootstrap-identity\.sh' \
  .chezmoi.toml.tmpl .bootstrap-identity.sh docs/chezmoi/action-graph.md
```

Show only the hook-related region of `.chezmoi.toml.tmpl` after locating it:

```sh
rg -n '\[hooks\.|read-source-state|bootstrap-identity' .chezmoi.toml.tmpl
```

Do not edit `.chezmoi.toml.tmpl` or `.bootstrap-identity.sh` as part of this
inspection workflow.

## External-resource input inspection

Inspect external-resource declarations that may feed later script behavior:

```sh
sed -n '1,240p' .chezmoiexternal.toml.tmpl
```

Inspect external-resource fields and script references to externally managed
targets:

```sh
rg -n --hidden \
  'type =|url =|urls =|refreshPeriod|path =|checksum|win32yank|bat|Catppuccin|completion|eza|git-completion' \
  .chezmoiexternal.toml.tmpl .chezmoiscripts dot_config
```

Inspect current action graph external-resource documentation:

```sh
rg -n \
  'External resources|\.chezmoiexternal|win32yank|Catppuccin|completion|refresh' \
  docs/chezmoi/action-graph.md
```

This inspection only identifies references. It does not validate download
availability, refresh behavior, checksums, or rendered target effects.

## Compact inspection bundle

Use this bundle when a Commander Thread needs shareable script-contract evidence.

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
run find .chezmoiscripts -maxdepth 1 -type f -name 'run_*' -print
run sh -c 'find .chezmoiscripts -maxdepth 1 -type f -name "run_*" -print | sort'
run sh -c 'find .chezmoiscripts -maxdepth 1 -type f -name "run_*" -print | sort | while IFS= read -r script; do name=${script##*/}; case "$name" in run_once_*) type="run_once" ;; run_onchange_*) type="run_onchange" ;; run_*) type="run" ;; *) type="other" ;; esac; case "$name" in *_before_*) placement="before" ;; *_after_*) placement="after" ;; *) placement="during" ;; esac; printf "%-13s %-8s %s\n" "$type" "$placement" "$script"; done'
run rg -n --hidden '(\[Trigger\]|[Tt]rigger|[Hh]ash|sha256sum|includeTemplate|include )' .chezmoiscripts
run rg -n --hidden 'mise (install|run)|setup:|doctor:|integrate:|sync:|update:' .chezmoiscripts dot_config/mise/tasks dot_config/mise/config.toml.tmpl
run find dot_config/mise/tasks -type f
run git ls-files -s dot_config/mise/tasks
run rg -n --hidden 'is_wsl|WSL|wsl|Windows|windows_user|npiperelay|winget|PowerShell|wslpath|win32yank|1password-bridge' .chezmoi.toml.tmpl .chezmoiexternal.toml.tmpl .chezmoiscripts dot_zshenv.tmpl dot_config
run rg -n --hidden '\[hooks\.|read-source-state|bootstrap-identity|\.bootstrap-identity\.sh' .chezmoi.toml.tmpl .bootstrap-identity.sh docs/chezmoi/action-graph.md
run rg -n --hidden 'type =|url =|urls =|refreshPeriod|path =|checksum|win32yank|bat|Catppuccin|completion|eza|git-completion' .chezmoiexternal.toml.tmpl .chezmoiscripts dot_config
run rg -n 'Script execution contract|Mise task boundary|Host-specific branches|External resources|Bootstrap and hook boundary|Follow-up candidates' docs/chezmoi/action-graph.md
```

Before sharing the output, skim it for local paths or account-specific values
that should be redacted.

## Validation after documentation changes

After editing this document or adding links to it, run validation separately from
inspection:

```sh
git status --short
git diff --stat
git diff --check
pre-commit run --all-files
```

Validate repository-relative Markdown links when Markdown links change:

```sh
python3 - <<'PY'
from pathlib import Path
import re
import sys

root = Path(".").resolve()
files = list(Path("docs").rglob("*.md")) + [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("repomix-instruction.md"),
    Path(".github/copilot-instructions.md"),
    Path(".github/pull_request_template.md"),
]

link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
errors = []

for file in files:
    if not file.exists():
        continue

    text = file.read_text()
    for match in link_re.finditer(text):
        target = match.group(1).strip()

        if (
            "://" in target
            or target.startswith("#")
            or target.startswith("mailto:")
            or target.startswith("tel:")
        ):
            continue

        path_part = target.split("#", 1)[0]
        if not path_part:
            continue

        resolved = (file.parent / path_part).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"{file}: link escapes repository: {target}")
            continue

        if not resolved.exists():
            errors.append(f"{file}: missing link target: {target}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("All checked Markdown links resolve.")
PY
```

Regenerate the LLM-consumed repository snapshot after documentation changes:

```sh
repomix
```

Do not claim GitHub Actions CI passes until the pull request has CI evidence.

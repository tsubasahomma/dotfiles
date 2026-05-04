# Repository Repomix routing

## Purpose

Define local Repomix paths, repository-specific recipes, and generated-output
confirmation checks for this dotfiles repository.

Use [`../context/repomix.md`](../context/repomix.md) for generic Repomix
generation, consumption, generated-output, focused snapshot, and stale-snapshot
rules. Use this file only for local paths, commands, and confirmation checks.

## Local tracked instruction and generated output paths

| Item | Path | Rule |
| --- | --- | --- |
| Tracked instruction file | `docs/context/repomix.md` | This remains the configured instruction file for portable Repomix routing. |
| Local Repomix extension | `docs/repo/repomix.md` | This file owns local paths, recipes, and generated-output checks. |
| Default generated snapshot | `.context/repomix/repomix-dotfiles.xml` | Generated evidence only. Do not edit by hand. |
| Focused generated snapshots | `.context/repomix/repomix-dotfiles-<scope>.xml` | Generated evidence only. Use descriptive scope names tied to the active issue or review. |
| Ignored packed outputs | `repomix-*.xml`, `repomix-output.*`, `.context/repomix/**` | Keep generated output out of source documentation; `.context/repomix/.gitkeep` may remain tracked. |

Do not change Repomix output style, ignore patterns, security check, token
counting, compression, file inclusion semantics, or generated output location
unless the active issue explicitly scopes that change. When the tracked
instruction file moves, change only `output.instructionFilePath` unless current
evidence proves another config change is necessary.

## Local focused snapshot recipe

Use a full snapshot only when the task needs repository-wide structure, routing,
context architecture review, broad stale-reference scanning, or fresh packed
input for a new LLM thread:

```zsh
repomix
```

Use this focused working-tree recipe when a task is bounded to a known issue,
PR, diff, or small file set:

```zsh
scope="issue230"
changed_files="$(git diff --name-only | paste -sd, -)"
router_files="AGENTS.md,docs/context/README.md,docs/context/kernel.md,docs/repo/README.md"
include_paths="$(printf '%s,%s' "$changed_files" "$router_files" | tr ',' '\n' | sed '/^$/d' | sort -u | paste -sd, -)"
repomix \
  --include-diffs \
  --include "$include_paths" \
  -o ".context/repomix/repomix-dotfiles-${scope}.xml"
```

For staged changes, replace `git diff --name-only` with
`git diff --staged --name-only`. For branch or PR review, replace it with the
base comparison that matches the review question.

## Local instruction routing for packed snapshots

LLMs consuming a Repomix snapshot of this repository should use:

- [`../../AGENTS.md`](../../AGENTS.md) as the root context manifest;
- [`../context/README.md`](../context/README.md) as the portable context
  task-to-context router;
- [`../context/kernel.md`](../context/kernel.md) for instruction precedence,
  evidence precedence, context economy, scope control, unknown-state rules,
  current-file requirements, and generated artifact discipline;
- [`../context/protocols.md`](../context/protocols.md) for patch, command,
  validation-report, PR, commit, code-fence, heredoc, whitespace, and
  final-newline output contracts;
- [`../context/workflows.md`](../context/workflows.md) for reusable issue,
  thread, PR, validation, merge, closure, checkbox, rollback, and parent-child
  sequencing procedure;
- [`../context/repomix.md`](../context/repomix.md) for generic Repomix rules;
- [`../context/evals.md`](../context/evals.md) for regression cases covering
  predictable LLM-context failures;
- [`README.md`](./README.md) for this repository's local identity, surfaces,
  validation, workflow exceptions, and Repomix paths.

Preserve existing provisioning, identity, editor, shell, Git, mise, Homebrew,
and GitHub Actions behavior unless the assigned issue explicitly scopes a
behavior change. Do not import assumptions from reference repositories unless
local repository evidence and the assigned issue require them.

## Local confirmation checks

When Repomix routing changes, validation should confirm:

- `repomix.config.json` points `output.instructionFilePath` at the intended
  tracked instruction file;
- generated output remains under `.context/repomix/**`;
- generated output was regenerated rather than hand-edited;
- stale references to retired Repomix guidance paths were removed or explicitly
  justified as legacy examples;
- Markdown links to removed Repomix guidance files no longer exist.

Use these local checks when routing changes:

```zsh
repomix
test -f .context/repomix/repomix-dotfiles.xml
git check-ignore -v .context/repomix/repomix-dotfiles.xml
```

Report validation as evidence. Do not claim Repomix generation, stale-reference
scans, Markdown link validation, local checks, or CI passed without command
output, CI evidence, inspected state, or explicit maintainer confirmation.

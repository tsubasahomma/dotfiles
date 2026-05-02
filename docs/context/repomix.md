# Repomix operating contract

## Purpose

Define the Repomix generation and consumption contract for this repository.

This file is also the tracked Repomix instruction file configured by
[`../../repomix.config.json`](../../repomix.config.json). Repomix snapshots must
route LLMs through this operating contract without restoring the retired
`docs/context/repomix/**` subtree.

## Responsibility boundary

This file owns Repomix-specific guidance:

- tracked instruction file location;
- generated output location;
- generated-output read-only rules;
- full and focused snapshot selection;
- snapshot consumption rules;
- stale snapshot conflict handling;
- Repomix validation triggers and confirmation checks.

It does not own generic evidence rules ([`kernel.md`](./kernel.md)), output
formats ([`protocols.md`](./protocols.md)), repository-wide source-state and
validation baselines ([`repo.md`](./repo.md)), behavior-sensitive surface routing
([`surfaces.md`](./surfaces.md)), workflow procedure
([`workflows.md`](./workflows.md)), or regression cases ([`evals.md`](./evals.md)).

## Tracked instruction and generated output paths

| Item | Path | Rule |
| --- | --- | --- |
| Tracked instruction file | `docs/context/repomix.md` | This file is the configured instruction file. Keep Repomix instruction routing here. |
| Default generated snapshot | `.context/repomix/repomix-dotfiles.xml` | Generated evidence only. Do not edit by hand. |
| Focused generated snapshots | `.context/repomix/repomix-dotfiles-<scope>.xml` | Generated evidence only. Use descriptive scope names tied to the active issue or review. |
| Ignored packed outputs | `repomix-*.xml`, `repomix-output.*`, `.context/repomix/**` | Keep generated output out of source documentation; `.context/repomix/.gitkeep` may remain tracked. |

Do not change Repomix output style, ignore patterns, security check, token
counting, compression, file inclusion semantics, or generated output location
unless the active issue explicitly scopes that change. When the tracked
instruction file moves, change only `output.instructionFilePath` unless current
evidence proves another config change is necessary.

## Generation contract

Use a full snapshot when the task needs repository-wide structure, routing,
context architecture review, broad stale-reference scanning, or fresh packed
input for a new LLM thread:

```zsh
repomix
```

Use a focused snapshot when the task is bounded to a known issue, PR, diff, or
small file set. Prefer the changed files plus necessary router files over packing
unrelated source state:

```zsh
changed_files="$(git diff --name-only | paste -sd, -)"
repomix \
  --include-diffs \
  --include "$changed_files" \
  -o .context/repomix/repomix-dotfiles-<scope>.xml
```

When generating focused evidence for staged changes, use the staged or branch
diff that matches the review question. Do not use a stale broad snapshot to
replace current file contents, command output, or the active diff.

## Consumption contract

Treat Repomix snapshots as packed read-only evidence for repository structure,
file contents, diffs, and instruction routing.

When consuming a snapshot:

1. identify the snapshot generation time, scope, and included files when that
   information is available;
2. use the packed directory structure to locate relevant source files;
3. read original source paths from the repository before producing targeted
   patches when fresher file evidence is available;
4. prefer active issue, PR, current diff, command output, CI evidence, and
   maintainer-provided current files over packed snapshot content when they
   conflict;
5. call out stale or conflicting snapshot evidence instead of silently following
   it.

Do not edit generated XML, packed output, rendered target state, or temporary
snapshot files directly. Change source files or Repomix configuration, then
regenerate evidence when validation requires it.

## Instruction routing for packed snapshots

LLMs consuming a Repomix snapshot of this repository should use:

- [`../../AGENTS.md`](../../AGENTS.md) as the root context manifest;
- [`README.md`](./README.md) as the Option A+ task-to-context router;
- [`kernel.md`](./kernel.md) for instruction precedence, evidence precedence,
  context economy, scope control, unknown-state rules, current-file
  requirements, and generated artifact discipline;
- [`protocols.md`](./protocols.md) for patch, command, validation-report, PR,
  commit, code-fence, heredoc, whitespace, and final-newline output contracts;
- [`repo.md`](./repo.md) for dotfiles source-state boundaries,
  behavior-preserving constraints, supported host posture, root document roles,
  and local validation baseline;
- [`surfaces.md`](./surfaces.md) for behavior-sensitive surface routing;
- [`workflows.md`](./workflows.md) for issue, thread, PR, validation, merge,
  closure, checkbox, rollback, and parent-child sequencing procedure;
- this file for Repomix generation, consumption, generated-output, focused
  snapshot, and stale-snapshot rules;
- [`evals.md`](./evals.md) for regression cases covering predictable LLM-context
  failures.

Preserve existing provisioning, identity, editor, shell, Git, mise, Homebrew,
and GitHub Actions behavior unless the assigned issue explicitly scopes a
behavior change. Do not import assumptions from reference repositories unless
local repository evidence and the assigned issue require them.

## Validation triggers

Run `repomix` when a change affects any of these surfaces:

- assistant guidance or root context routing;
- `docs/context/**` operating-contract routing;
- Repomix generation or consumption guidance;
- `repomix.config.json` instruction path or output routing;
- generated snapshot routing or stale-reference behavior.

For documentation-only changes that do not change setup, toolchain, rendered
config, task behavior, health-check behavior, scripts, CI semantics, versions,
dependencies, or lockfiles, `mise run doctor` is not required. Report it as not
run for that reason instead of marking it complete.

## Confirmation checks

When Repomix routing changes, validation should confirm:

- `repomix.config.json` points `output.instructionFilePath` at the intended
  tracked instruction file;
- generated output remains under `.context/repomix/**`;
- generated output was regenerated rather than hand-edited;
- stale references to retired Repomix guidance paths were removed or explicitly
  justified as legacy examples;
- Markdown links to removed Repomix guidance files no longer exist.

Report validation as evidence. Do not claim Repomix generation, stale-reference
scans, Markdown link validation, local checks, or CI passed without command
output, CI evidence, inspected state, or explicit maintainer confirmation.

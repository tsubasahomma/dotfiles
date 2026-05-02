# Workflow validation guidance

## Purpose

Use this workflow when reporting validation for issues, PRs, and review
summaries in this dotfiles repository.

This document focuses on workflow reporting. Use the
[Repository operating contract](../../repo.md) to choose checks by touched
surface, and use [`../../kernel.md`](../../kernel.md) for reusable validation
evidence rules.

## Requirements versus evidence

Keep these states separate:

- required validation: checks that should be run before completion;
- completed validation: checks with command output, exit status, CI evidence,
  inspected state, or explicit maintainer confirmation;
- skipped validation: checks not run, with the reason;
- failed validation: checks that failed, including any retry evidence.

Do not check a validation item because it is expected to pass.

## Documentation-only boundary

For documentation-only context or workflow changes, baseline validation usually
comes from:

- `git status --short`;
- `git diff --stat`;
- `git diff --check`;
- `pre-commit run --all-files`;
- Markdown relative link validation when repository-relative links change;
- `repomix` when context routing, LLM guidance, workflow guidance, Repomix
  guidance, or generated snapshot routing changes.

Do not require `mise run doctor` when the PR changes only Markdown context or
routing and does not change setup, toolchain, rendered config, task behavior,
health-check behavior, scripts, CI semantics, versions, dependencies, or
lockfiles.

If `mise run doctor` is not run for a documentation-only PR, report that reason
instead of marking the check complete.

## Surface-specific routing

Route behavior-sensitive validation through the local surface guidance:

- [Chezmoi](../surfaces/chezmoi.md) for source-state, templates, scripts,
  rendered output, and trigger-sensitive behavior;
- [Mise](../surfaces/mise.md) for task source state, metadata, tool resolution,
  and health-check behavior;
- [WSL2](../surfaces/wsl2.md) for Windows interop, user systemd, and bridge
  behavior;
- [Identity](../surfaces/identity.md) for 1Password, SSH signing, scoped Git
  identity, and secret-adjacent evidence;
- [Neovim](../surfaces/neovim.md) for plugin state, providers, and headless
  integration;
- [GitHub Actions](../surfaces/github-actions.md) for workflow semantics and
  remote CI evidence.

Do not duplicate those surface rules in workflow reports. Link to them and state
which evidence was actually collected.

## CI versus local evidence

Local validation and remote CI answer different questions.

Do not infer GitHub Actions success from local checks. Do not infer local WSL2,
1Password, SSH agent, Windows interop, user systemd, or workstation convergence
from GitHub Actions CI.

When CI is required, report it only after CI evidence is available.

## Validation reporting format

A useful PR or review validation report should state:

- the command or evidence source;
- the observed result;
- whether the item is complete, skipped, failed, or pending;
- why skipped checks were not required for the touched surface.

For example:

```text
- `git diff --check`: no output
- `pre-commit run --all-files`: passed
- `mise run doctor`: not run because this PR is documentation-only and does not
  change setup, toolchain, rendered config, task behavior, health-check behavior,
  scripts, CI semantics, versions, dependencies, or lockfiles
```

## Out of scope

This document does not add validation automation, change CI requirements, change
mise tasks, or require heavyweight local convergence checks for pure
Markdown-only changes.

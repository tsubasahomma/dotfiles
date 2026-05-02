# Repository operating contract

## Purpose

Define the dotfiles-specific repository contract that extends the shared kernel.

This file is the skeleton boundary for source-state ownership, behavior
boundaries, supported host posture, root document roles, and local validation
baseline.

## Owned responsibilities

- Repository identity as a chezmoi-managed dotfiles source-state repository.
- Editable source-state versus rendered target-state boundaries.
- Behavior-preserving constraints for documentation-only work.
- Supported host posture for macOS and Windows 11 with WSL2 Ubuntu.
- Local baseline validation for documentation and routing changes.
- Roles of `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, and vendor adapters.
- Generated Repomix output location as read-only evidence.

## Non-goals

- Generic instruction or evidence precedence rules.
- Patch syntax or PR formatting.
- Full surface manuals.
- Workflow procedure schemas.
- Changes to scripts, tasks, rendered configuration, CI, versions,
  dependencies, lockfiles, or generated artifacts.

## Current evidence to inspect before later collapse work

- [`local/profile.md`](./local/profile.md)
- [`local/boundaries.md`](./local/boundaries.md)
- [`local/validation.md`](./local/validation.md)
- [`local/glossary.md`](./local/glossary.md)
- [`local/routing.md`](./local/routing.md)
- [`../../README.md`](../../README.md)
- [`../../ARCHITECTURE.md`](../../ARCHITECTURE.md)
- [`../../AGENTS.md`](../../AGENTS.md)
- [`../../.github/copilot-instructions.md`](../../.github/copilot-instructions.md)

## Minimal routing guidance

Load this file when a task depends on repository identity, editable path
boundaries, local validation, root document roles, or behavior preservation.

For detailed behavior claims, inspect current source state, rendered output,
command output, or CI evidence that matches the touched surface. Do not use this
file to justify behavior changes that the active issue did not scope.

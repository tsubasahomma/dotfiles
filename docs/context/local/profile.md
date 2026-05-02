# Local repository profile

## Purpose

Use this profile to identify what kind of repository this is, which state is
editable source, and which documentation entry point should be used for local
context.

## Repository identity

This repository is a chezmoi-managed dotfiles source-state repository for
personal workstation configuration.

It is an infrastructure repository for provisioning and maintaining workstation
state. It is not a normal application repository, package workspace, deployment
monorepo, Terraform/OpenTofu repository, or service runtime.

Do not import architecture assumptions from reference repositories unless local
repository evidence and the active issue explicitly require them.

## Source-state model

Edit repository source state, not rendered target state.

Repository source state includes paths such as:

- `.chezmoidata/**`
- `.chezmoiscripts/**`
- `.chezmoitemplates/**`
- `dot_*` and `private_dot_*` source-state paths
- `docs/**`
- `AGENTS.md`
- `.github/**`

Rendered target state is produced by chezmoi from source-state files,
templates, attributes, and host data. A valid source-state edit can still render
invalid target shell, Lua, TOML, JSON, INI, service, or SSH configuration if the
rendered output is not reviewed when behavior-sensitive templates change.

Generated Repomix output under `.context/repomix/**` is read-only evidence, not
source documentation.

## Supported host posture

The README documents the supported first-run path for macOS and Windows 11 with
WSL2 Ubuntu 24.04 or later.

Other Linux distributions may appear in source-state logic or package data, but
they are not currently documented as supported first-run targets.

Do not treat GitHub Actions CI as proof of local WSL2, Windows interop,
1Password Desktop, SSH agent bridge, user systemd, or workstation runtime
convergence.

## Current documentation entry points

Use the current entry point that matches the task:

| Entry point | Current role |
| --- | --- |
| [`README.md`](../../../README.md) | First-run and operator-facing bootstrap entry point. |
| [`AGENTS.md`](../../../AGENTS.md) | Root context manifest. |
| [`.github/copilot-instructions.md`](../../../.github/copilot-instructions.md) | GitHub Copilot adapter. |
| [`ARCHITECTURE.md`](../../../ARCHITECTURE.md) | High-level architecture and teardown overview. |
| [`docs/context/README.md`](../README.md) | Context architecture entry point. |
| [`docs/context/core/README.md`](../core/README.md) | Reusable context guidance. |
| [`docs/context/local/README.md`](./README.md) | Dotfiles-specific context extension layer. |
| [`docs/context/local/surfaces/README.md`](./surfaces/README.md) | Behavior-sensitive surface capsules. |
| [`docs/context/local/workflows/README.md`](./workflows/README.md) | Local workflow guidance. |
| [`docs/context/repomix/README.md`](../repomix/README.md) | Tracked Repomix context routing. |

Retired legacy surfaces are recorded in the
[Context migration map](../migration-map.md). They are not active routing targets.

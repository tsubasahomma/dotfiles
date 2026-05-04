# Repository profile

## Purpose

Define the repository-local profile for this dotfiles source-state repository.

Use this file when a task depends on repository identity, source-state
boundaries, rendered-target boundaries, supported host posture, root document
roles, generated artifact boundaries, or behavior-preserving local constraints.

## Responsibility boundary

This file owns repository-specific profile facts. It does not own generic
instruction or evidence precedence ([`../context/kernel.md`](../context/kernel.md)),
output formatting ([`../context/protocols.md`](../context/protocols.md)),
reusable workflow procedure ([`../context/workflows.md`](../context/workflows.md)),
local surface routing ([`surfaces.md`](./surfaces.md)), local validation routing
([`validation.md`](./validation.md)), or local Repomix paths
([`repomix.md`](./repomix.md)).

## Repository identity

This repository is Tsubasa Homma's chezmoi-managed dotfiles source state for
personal workstation configuration.

It is an infrastructure repository for provisioning and maintaining workstation
state. It is not an application repository, package workspace, deployment
monorepo, Terraform/OpenTofu repository, or service runtime.

Do not import architecture assumptions from reference repositories unless local
repository evidence and the active issue explicitly require them.

## Source state and editable boundaries

Edit repository source state, not rendered target state.

Repository source state includes paths such as:

- `.chezmoidata/**`
- `.chezmoiscripts/**`
- `.chezmoitemplates/**`
- `dot_*` and `private_dot_*` source-state paths
- `docs/**`
- `AGENTS.md`
- `.github/**`, only when the active issue scopes those files

Rendered target state is produced by chezmoi from source-state files, templates,
attributes, and host data. A valid source-state edit can still render invalid
shell, Lua, TOML, JSON, INI, service, SSH, or Git configuration if the rendered
output is not reviewed when behavior-sensitive templates change.

Generated Repomix output under `.context/repomix/**`, `repomix-*.xml` snapshots,
rendered target files, and temporary generated artifacts are evidence, not
source documentation. Do not hand-edit them. Change source files or generation
configuration, then regenerate only when validation requires fresh evidence.

## Behavior-preserving rules

Preserve existing repository behavior unless the active issue explicitly scopes a
behavior change and validation evidence matches the touched surface.

Documentation-only changes must not imply changes to provisioning, rendered
output, task execution, CI semantics, tool resolution, identity routing, shell
startup, editor behavior, or package selection.

Follow these local rules unless the active issue says otherwise:

- Do not change chezmoi scripts, trigger comments, template whitespace trimming,
  or rendered-output-sensitive comments as incidental cleanup.
- Do not change mise task names, grouping, metadata, dependencies, executable
  bits, or behavior as part of documentation routing.
- Do not treat locally visible mise tasks as repository-owned source state
  without comparing source state, managed target paths, and local visibility
  evidence.
- Do not treat GitHub Actions CI as proof of local WSL2, Windows interop,
  1Password Desktop, SSH agent bridge, user systemd, or workstation convergence.
- Do not change runtime versions, tool versions, package lists, dependencies, or
  lockfiles from a context-documentation issue.

## Behavior-sensitive boundaries

Treat these repository surfaces as behavior-sensitive:

| Boundary | Includes |
| --- | --- |
| Chezmoi source state | Templates, attributes, scripts, hooks, externals, and generated target paths. |
| Package provisioning | macOS Homebrew, Linux package data, and Windows-side prerequisites. |
| Repository data | `.chezmoidata/**` data consumed by templates, scripts, mise, completions, or package generation. |
| Template fragments | `.chezmoitemplates/**` reusable template fragments and generated output assumptions. |
| Identity and SSH | 1Password identity discovery, identity metadata, SSH signing, SSH agent routing, and generated identity files. |
| WSL2 bridge | Windows interop, `npiperelay.exe`, `op.exe`, user systemd services, and Windows-side sync paths. |
| Rendered configuration | Shell startup, zsh, WezTerm, Starship, Git, SSH, Homebrew, mise, Vale, Neovim, and related rendered files. |
| Mise | `dot_config/mise/tasks/**`, `.mise.toml`, tool declarations, runtime versions, tool versions, dependencies, and lockfiles. |
| GitHub Actions | `.github/workflows/**`, `compliance.yml` semantics, action pins, and remote CI evidence. |
| Generated artifacts | Repomix output under `.context/repomix/**` and any rendered or packed evidence. |

Use [`surfaces.md`](./surfaces.md) for surface-level routing and required
evidence.

## Supported host posture

[`../../README.md`](../../README.md) documents the supported first-run path for
macOS and Windows 11 with WSL2 Ubuntu 24.04 or later.

Other Linux distributions may appear in source-state logic or package data, but
they are not currently documented as supported first-run targets.

Do not treat GitHub Actions Ubuntu as proof of local WSL2, Windows interop,
1Password Desktop, SSH agent bridge, user systemd, or workstation runtime
convergence.

## Root document and adapter roles

| Entry point | Role |
| --- | --- |
| [`../../README.md`](../../README.md) | First-run and operator-facing bootstrap entry point. |
| [`../../ARCHITECTURE.md`](../../ARCHITECTURE.md) | High-level architecture overview and operational teardown routing until a later scoped issue retires it. |
| [`../../AGENTS.md`](../../AGENTS.md) | Root context manifest and concise assistant entry point. |
| [`../../.github/copilot-instructions.md`](../../.github/copilot-instructions.md) | GitHub Copilot adapter; secondary to the shared operating contract. |
| [`../context/README.md`](../context/README.md) | Portable context architecture entry point and task-to-context router. |
| [`README.md`](./README.md) | Repository-local extension entry point. |
| [`surfaces.md`](./surfaces.md) | Local behavior-sensitive surface routing. |
| [`validation.md`](./validation.md) | Local validation baseline and validation routing. |
| [`workflows.md`](./workflows.md) | Local workflow exceptions and template routing. |
| [`repomix.md`](./repomix.md) | Local Repomix paths, recipes, and confirmation checks. |

Root and adapter documents should route through the portable context contracts
and this local extension without turning vendor-specific guidance into the
primary architecture. Do not add `.github/instructions/**` unless a later issue
explicitly scopes that adapter.

## Local terms

| Term | Meaning in this repository |
| --- | --- |
| source state | Files tracked in this repository and consumed by chezmoi as the editable source of workstation configuration. |
| rendered target state | Files, scripts, configuration, and local artifacts produced by chezmoi in the target home directory or host environment. |
| source-state path | A repository path using chezmoi source-state naming, such as `dot_config/**`, `private_dot_ssh/**`, or `.chezmoiscripts/**`. |
| target path | The rendered path managed or affected by chezmoi after source-state attributes and templates are evaluated. |
| generated context artifact | A generated Repomix artifact under `.context/repomix/**`; it is read-only evidence, not tracked source documentation. |
| local surface map | `docs/repo/surfaces.md`, the compact map for behavior-sensitive surface routing, failure prevention, required evidence, validation routing, and deep source links. |
| workflow contract | Reusable issue, pull request, validation, merge, closure, Commander, and Worker procedures in [`../context/workflows.md`](../context/workflows.md). |
| root context manifest | `AGENTS.md`, the concise repository-wide assistant entry point. |
| adapter | Vendor-specific assistant entry point such as `.github/copilot-instructions.md`; adapters should route to the LLM-agnostic context architecture. |
| 1Password identity | Repository-discovered identity metadata from prepared 1Password SSH Key items used for Git authoring, SSH signing, and SSH routing. |
| WSL2 bridge | The Windows-to-WSL2 identity and SSH agent path involving Windows 11, WSL2 Ubuntu, Windows 1Password Desktop, `op.exe`, `npiperelay.exe`, and user systemd. |
| doctor task | A repository-local mise validation or readiness check under `dot_config/mise/tasks/doctor/**`. |
| repair candidate | A current behavior that may be mutation-oriented and may need a future explicit `repair:*` decision; it is not authorization to change current tasks. |

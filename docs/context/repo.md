# Repository operating contract

## Purpose

Define the dotfiles-specific repository contract that extends the shared kernel.

Load this file when a task depends on repository identity, source-state
boundaries, rendered-target boundaries, behavior preservation, supported host
posture, root document roles, generated artifact boundaries, or the local
validation baseline.

## Responsibility boundary

This file owns repository-specific constraints for this dotfiles repository.

It does not own generic instruction or evidence precedence
([`kernel.md`](./kernel.md)), output formatting ([`protocols.md`](./protocols.md)),
regression cases ([`evals.md`](./evals.md)), full surface manuals
([`surfaces.md`](./surfaces.md)), workflow procedures
([`workflows.md`](./workflows.md)), or Repomix generation procedure
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

Rendered target state is produced by chezmoi from source-state files,
templates, attributes, and host data. A valid source-state edit can still render
invalid shell, Lua, TOML, JSON, INI, service, SSH, or Git configuration if the
rendered output is not reviewed when behavior-sensitive templates change.

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
- Do not delete or thin remaining Repomix evidence outside the child issue
  that explicitly scopes that collapse.

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

A later issue may change a behavior-sensitive surface only when it names the
exact behavior being changed, identifies current source-state and rendered-target
evidence where relevant, lists affected commands and operator workflows,
preserves behavior unless explicitly scoped otherwise, and reports validation as
evidence.

## Supported host posture

[`README.md`](../../README.md) documents the supported first-run path for macOS
and Windows 11 with WSL2 Ubuntu 24.04 or later.

Other Linux distributions may appear in source-state logic or package data, but
they are not currently documented as supported first-run targets.

Do not treat GitHub Actions Ubuntu as proof of local WSL2, Windows interop,
1Password Desktop, SSH agent bridge, user systemd, or workstation runtime
convergence.

## Root document and adapter roles

| Entry point | Role |
| --- | --- |
| [`README.md`](../../README.md) | First-run and operator-facing bootstrap entry point. |
| [`ARCHITECTURE.md`](../../ARCHITECTURE.md) | High-level architecture overview and operational teardown routing. |
| [`AGENTS.md`](../../AGENTS.md) | Root context manifest and concise assistant entry point. |
| [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) | GitHub Copilot adapter; secondary to the shared operating contract. |
| [`docs/context/README.md`](./README.md) | Context architecture entry point and task-to-context router. |
| [`docs/context/surfaces.md`](./surfaces.md) | Compact behavior-sensitive surface routing. |
| [`docs/context/workflows.md`](./workflows.md) | Local issue, thread, PR, validation, merge, and closure procedure contract. |
| [`docs/context/repomix.md`](./repomix.md) | Repomix generation and consumption contract. |

Root and adapter documents should route to this operating contract without
turning vendor-specific guidance into the primary architecture. Do not add
`.github/instructions/**` unless a later issue explicitly scopes that adapter.

## Local validation baseline

For documentation-only context or routing changes, use evidence from:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `pre-commit run --all-files`
- Markdown relative link validation, when repository-relative Markdown links are
  added, removed, or changed
- `repomix`, when context routing, assistant guidance, workflow contracts,
  Repomix guidance, or generated snapshot routing changes
- GitHub Actions CI after PR creation, when required by branch protection or
  reviewer request

Do not mark any check complete without command output, CI evidence, inspected
state, or explicit maintainer confirmation.

## Validation routing by touched source

| Touched source | Validation routing |
| --- | --- |
| `docs/context/**` | Use baseline documentation validation. Run Markdown link validation when links change. Run `repomix` because context routing affects generated LLM evidence. |
| `AGENTS.md` or `.github/copilot-instructions.md` | Use baseline documentation validation, Markdown link validation, and `repomix`; these files affect assistant routing. |
| `README.md` or `ARCHITECTURE.md` | Use baseline documentation validation, Markdown link validation when links change, and `repomix` when assistant or context routing changes. Add behavior validation only if the edit changes documented operator commands or behavior claims. |
| `.chezmoiignore.tmpl`, `.chezmoi.toml.tmpl`, `.chezmoiscripts/**`, `.chezmoitemplates/**`, or rendered configuration templates | Use rendered-output inspection such as `chezmoi diff` or `chezmoi execute-template` in addition to baseline checks. Consider `mise run doctor` only when setup, toolchain, rendered config, task behavior, or health-check behavior changes. |
| `.chezmoidata/**` | Review every template, script, package, completion, or tool consumer affected by the data. Add rendered-output and task validation that matches the changed consumer. |
| `dot_config/mise/tasks/**`, `.mise.toml`, tool declarations, versions, dependencies, or lockfiles | Validate mise task visibility, task behavior, tool resolution, and health checks appropriate to the change. `mise run doctor` is usually relevant when health-check behavior or setup/toolchain behavior changes. |
| `.github/workflows/**` | Use workflow-focused review plus GitHub Actions CI evidence after PR creation. Local checks do not prove remote CI status. |
| `.github/ISSUE_TEMPLATE/**` or `.github/pull_request_template.md` | Use template-focused review and baseline documentation validation. Do not change these templates from context cleanup unless explicitly scoped. |
| `.context/repomix/**` generated XML | Do not edit generated output directly. Regenerate with `repomix` when validation requires fresh evidence. |

## Documentation-only doctor boundary

Do not require `mise run doctor` for a PR that changes only Markdown context or
routing and does not change setup, toolchain, rendered config, task behavior,
health-check behavior, scripts, CI semantics, versions, dependencies, or
lockfiles.

If `mise run doctor` is not run for such a PR, report that it was not run for
that reason rather than marking it complete.

## Local terms

| Term | Meaning in this repository |
| --- | --- |
| source state | Files tracked in this repository and consumed by chezmoi as the editable source of workstation configuration. |
| rendered target state | Files, scripts, configuration, and local artifacts produced by chezmoi in the target home directory or host environment. |
| source-state path | A repository path using chezmoi source-state naming, such as `dot_config/**`, `private_dot_ssh/**`, or `.chezmoiscripts/**`. |
| target path | The rendered path managed or affected by chezmoi after source-state attributes and templates are evaluated. |
| generated context artifact | A generated Repomix artifact under `.context/repomix/**`; it is read-only evidence, not tracked source documentation. |
| surface operating contract | `docs/context/surfaces.md`, the compact map for behavior-sensitive surface routing, failure prevention, required evidence, validation routing, and deep source links. |
| workflow contract | Local issue, pull request, validation, merge, closure, Commander, and Worker procedures in [`docs/context/workflows.md`](./workflows.md). |
| root context manifest | `AGENTS.md`, the concise repository-wide assistant entry point. |
| adapter | Vendor-specific assistant entry point such as `.github/copilot-instructions.md`; adapters should route to the LLM-agnostic context architecture. |
| 1Password identity | Repository-discovered identity metadata from prepared 1Password SSH Key items used for Git authoring, SSH signing, and SSH routing. |
| WSL2 bridge | The Windows-to-WSL2 identity and SSH agent path involving Windows 11, WSL2 Ubuntu, Windows 1Password Desktop, `op.exe`, `npiperelay.exe`, and user systemd. |
| doctor task | A repository-local mise validation or readiness check under `dot_config/mise/tasks/doctor/**`. |
| repair candidate | A current behavior that may be mutation-oriented and may need a future explicit `repair:*` decision; it is not authorization to change current tasks. |

## Related contracts

Use [`surfaces.md`](./surfaces.md) when work touches or cites a
behavior-sensitive surface. Use [`workflows.md`](./workflows.md) when work
changes issue, thread, PR, validation, merge, or closure procedure. Use
[`repomix.md`](./repomix.md) for Repomix generation and consumption rules.

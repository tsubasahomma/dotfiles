# Local behavior boundaries

## Purpose

Use these boundaries to keep dotfiles context changes behavior-preserving unless
the active issue explicitly scopes a behavior change.

This document records local repository constraints. It does not authorize
changes to scripts, tasks, rendered configuration, CI, tool versions,
dependencies, lockfiles, or generated artifacts.

## Default rule

Preserve existing repository behavior unless the active issue explicitly scopes a
change and validation evidence matches the touched surface.

Documentation-only changes must not imply changes to provisioning, rendered
output, task execution, CI semantics, or tool resolution.

## Behavior-sensitive surfaces

Treat these surfaces as behavior-sensitive:

- chezmoi source-state templates, attributes, scripts, hooks, externals, and
  generated target paths
- package provisioning for macOS, Linux, and Windows-side prerequisites
- `.chezmoidata/**` data consumed by templates, scripts, mise, completions, or
  package generation
- `.chezmoitemplates/**` reusable template fragments
- 1Password identity discovery, identity metadata, SSH signing, SSH agent
  routing, and generated identity files
- WSL2 bridge behavior, Windows interop, `npiperelay.exe`, `op.exe`, user
  systemd services, and Windows-side sync paths
- shell startup, zsh, WezTerm, Starship, Git, SSH, Homebrew, mise, Vale, and
  Neovim rendered configuration
- `dot_config/mise/tasks/**`, `.mise.toml`, tool declarations, runtime versions,
  tool versions, dependencies, and lockfiles
- GitHub Actions `compliance.yml` semantics and CI validation behavior
- generated Repomix artifacts under `.context/repomix/**`

## Local preservation rules

Follow these local rules unless the active issue says otherwise:

- Do not change chezmoi scripts, trigger comments, template whitespace trimming,
  or rendered-output-sensitive comments as incidental cleanup.
- Do not change mise task names, grouping, metadata, dependencies, executable
  bits, or behavior as part of documentation routing.
- Do not treat locally visible mise tasks as repository-owned source state
  without comparing source-state, managed target, and local visibility evidence.
- Do not treat CI as proof of local WSL2, 1Password, SSH agent, Windows interop,
  user systemd, or workstation convergence.
- Do not change runtime versions, tool versions, package lists, dependencies, or
  lockfiles from a context-documentation issue.
- Do not hand-edit generated Repomix output or rendered target files.
- Do not delete, archive, or thin current context guidance surfaces until a
  scoped issue confirms their durable requirements are represented or
  intentionally discarded.

## Scoped exceptions

A later issue may change a behavior-sensitive surface only when it:

1. names the exact behavior or surface being changed;
2. identifies current source-state and rendered-target evidence where relevant;
3. lists affected commands, scripts, tasks, CI paths, documentation, and operator
   workflows;
4. preserves behavior unless the issue explicitly scopes a behavior change;
5. reports validation with command output, CI evidence, inspected state, or
   explicit maintainer confirmation.

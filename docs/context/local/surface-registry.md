# Local surface registry

## Purpose

Use this registry to route dotfiles surface capsule work.

Surface capsules are compact failure-prevention documents. They point to current
local evidence and avoid becoming replacement manuals for detailed historical
audit documentation.

## Registry

| Capsule | Current evidence to inspect | Failure-prevention focus |
| --- | --- | --- |
| [Chezmoi](./surfaces/chezmoi.md) | `.chezmoiscripts/**`, `.chezmoidata/**`, `.chezmoitemplates/**`, `.chezmoi*.tmpl`, and rendered-output inspection when behavior changes. | Preserve source-state versus rendered-target distinctions, script ordering, trigger-sensitive rendered content, template whitespace, and behavior-sensitive phase gates. |
| [Mise](./surfaces/mise.md) | `.mise.toml`, `dot_config/mise/tasks/**`, task visibility inspection, and relevant `mise run <task>` evidence when behavior changes. | Avoid unscoped task renames, regrouping, metadata changes, dependency changes, and false ownership claims from local mise visibility alone. |
| [WSL2](./surfaces/wsl2.md) | `README.md`, WSL-specific templates and scripts, Windows interop evidence, user systemd state, and local bridge checks when behavior changes. | Keep Windows interop, `op.exe`, `npiperelay.exe`, user systemd, SSH agent bridge, and CI-versus-local validation boundaries explicit. |
| [Identity](./surfaces/identity.md) | `.chezmoidata/**`, `.chezmoitemplates/git_identity_config.tmpl`, identity convergence scripts, SSH config templates, and redacted rendered-output evidence. | Protect 1Password item metadata, generated identity files, SSH signing, scoped Git identity routing, and secret-adjacent output handling. |
| [Neovim](./surfaces/neovim.md) | `dot_config/nvim/**`, Neovim mise tasks, provider health output, `lazy-lock.json`, and headless integration evidence when behavior changes. | Keep LazyVim, provider health, lockfile synchronization, headless integration, and rendered template behavior separate from generic editor advice. |
| [GitHub Actions](./surfaces/github-actions.md) | `.github/workflows/compliance.yml`, `.github/pull_request_template.md`, local validation output, and remote CI evidence when CI status is claimed. | Preserve CI semantics, branch-protection evidence boundaries, and the distinction between local validation and remote GitHub Actions status. |

## Capsule rules

A surface capsule should:

- start from the active issue and current repository evidence;
- distill only durable failure-prevention rules;
- link to current context documents or source-state surfaces instead of retired
  long-form manuals;
- avoid changing scripts, tasks, CI, versions, dependencies, lockfiles, or
  rendered behavior;
- keep workflow procedures under `docs/context/local/workflows/**`, not in a
  surface capsule;
- stay compact enough to act as routing context, not a domain manual.

## Current issue boundary

This registry records capsule routing only. It does not authorize behavior
changes, generated artifact edits, or repository-wide cleanup outside the active
issue scope.

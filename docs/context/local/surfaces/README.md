# Local surface capsules

## Purpose

This directory contains compact dotfiles surface capsules.

Surface capsules prevent predictable LLM mistakes on behavior-sensitive local
surfaces and route reviewers to the right current evidence. They are not full
domain manuals.

## Capsule index

| Surface | Use when the work touches or cites |
| --- | --- |
| [Chezmoi](./chezmoi.md) | source-state files, rendered target state, templates, scripts, script ordering, trigger-sensitive rendered content, or phase gates. |
| [Mise](./mise.md) | mise tasks, task grouping, task metadata, source-state versus local task visibility, doctor checks, or repair-adjacent behavior. |
| [WSL2](./wsl2.md) | Windows interop, Windows-side tools, `op.exe`, `npiperelay.exe`, user systemd, SSH agent bridge, or local WSL2 validation. |
| [Identity](./identity.md) | 1Password identity metadata, generated identity files, SSH signing, scoped Git identity routing, or secret-adjacent evidence. |
| [Neovim](./neovim.md) | LazyVim configuration, providers, `lazy-lock.json`, headless integration, or rendered Neovim templates. |
| [GitHub Actions](./github-actions.md) | `.github/workflows/**`, compliance workflow semantics, remote CI evidence, or branch-protection status. |

## Routing rule

Start with the active issue and current repository evidence. Use
[Local behavior boundaries](../boundaries.md) for repository-wide constraints and
[Local validation map](../validation.md) for validation routing. Use these
capsules only for surface-specific failure prevention.

If a future change needs detailed behavior claims, inspect current source state,
rendered output, command output, or CI evidence instead of relying on retired
long-form documentation.

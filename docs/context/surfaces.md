# Surface operating contract

## Purpose

Define the compact behavior-sensitive surface map for this dotfiles repository.

This file is the skeleton boundary for routing surface-specific evidence and
validation without turning each surface into a manual.

## Owned responsibilities

- Surface-level read-when routing.
- Surface-specific never-do constraints.
- Required evidence categories for behavior-sensitive changes.
- Validation routing pointers.
- Deep evidence links for later collapse work.

## Non-goals

- Repeating generic kernel or protocol rules.
- Full Chezmoi, mise, WSL2, identity, Neovim, or GitHub Actions manuals.
- Behavior changes.
- Tool, runtime, dependency, lockfile, task, script, or CI updates.
- Archival or historical ledgers.

## Current evidence to inspect before later collapse work

- [`repo.md`](./repo.md) for repository-wide behavior boundaries and validation baseline.
- [`local/surface-registry.md`](./local/surface-registry.md)
- [`local/surfaces/README.md`](./local/surfaces/README.md)
- [`local/surfaces/chezmoi.md`](./local/surfaces/chezmoi.md)
- [`local/surfaces/mise.md`](./local/surfaces/mise.md)
- [`local/surfaces/wsl2.md`](./local/surfaces/wsl2.md)
- [`local/surfaces/identity.md`](./local/surfaces/identity.md)
- [`local/surfaces/neovim.md`](./local/surfaces/neovim.md)
- [`local/surfaces/github-actions.md`](./local/surfaces/github-actions.md)

## Minimal surface map

| Surface | Read when | Never do | Required evidence |
| --- | --- | --- | --- |
| Chezmoi | Work touches source-state templates, scripts, attributes, externals, rendered target state, or phase-sensitive provisioning. | Do not edit rendered target state, normalize template whitespace, or change trigger-sensitive behavior as incidental cleanup. | Current source state plus rendered-output or trigger evidence when behavior changes. |
| Mise | Work touches `.mise.toml`, mise tools, file tasks, task metadata, task grouping, doctor checks, or tool resolution. | Do not rename, regroup, split, or change task metadata, dependencies, versions, or lockfiles unless scoped. | Current task source state plus task visibility or command output when behavior changes. |
| WSL2 | Work touches Windows interop, WSL2 Ubuntu, `op.exe`, `npiperelay.exe`, user systemd, or Windows-side sync paths. | Do not treat CI Ubuntu as proof of local WSL2, Windows, 1Password Desktop, or bridge behavior. | Host-specific WSL2 evidence when WSL2 behavior is claimed or changed. |
| Identity | Work touches 1Password identity metadata, SSH signing, generated Git identity files, SSH config, or secret-adjacent evidence. | Do not print secrets, key material, account IDs, item IDs, or generated identity output unnecessarily. | Redacted structural evidence and current identity source-state inspection. |
| Neovim | Work touches LazyVim configuration, providers, plugin state, lockfile state, or headless integration. | Do not change plugins, providers, keymaps, or `lazy-lock.json` as incidental cleanup. | Current Neovim source state plus provider, headless, or lockfile evidence when behavior changes. |
| GitHub Actions | Work touches workflows, CI semantics, action pins, permissions, matrix, or branch-protection claims. | Do not infer remote CI from local checks or change workflow semantics from documentation cleanup. | Workflow diff plus GitHub Actions evidence when CI status is claimed or required. |

## Minimal routing guidance

Load this file when a task touches or cites a behavior-sensitive surface. Use
[`repo.md`](./repo.md) for repository-wide boundaries and the local validation
baseline. Use the deep evidence links only when the compact row is not enough or
when a later child issue explicitly collapses surface capsules.

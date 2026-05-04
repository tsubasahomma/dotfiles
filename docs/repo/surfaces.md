# Repository surface map

## Purpose

Define the compact behavior-sensitive surface map for this dotfiles repository.

Load this file when work touches or cites a local surface whose source state,
rendered output, command behavior, CI behavior, identity behavior, or host
behavior can change. Keep this file as routing context, not a set of manuals.

## Responsibility boundary

This file owns local surface-level routing, surface-specific failure prevention,
required evidence categories, validation routing, and deep source links.

It does not own generic evidence rules ([`../context/kernel.md`](../context/kernel.md)),
output formats ([`../context/protocols.md`](../context/protocols.md)), local
profile facts ([`profile.md`](./profile.md)), local validation baseline
([`validation.md`](./validation.md)), reusable workflow procedure
([`../context/workflows.md`](../context/workflows.md)), generic Repomix procedure
([`../context/repomix.md`](../context/repomix.md)), or regression cases
([`../context/evals.md`](../context/evals.md)).

## Shared routing rules

Use the active issue, PR, review, or validation evidence first. Add surface
evidence only when the compact map below is not enough for the task.

For documentation-only routing edits, use the baseline documentation validation
from [`validation.md`](./validation.md). Do not require `mise run doctor` unless
setup, toolchain, rendered config, task behavior, health-check behavior, scripts,
CI semantics, versions, dependencies, or lockfiles change.

Do not restore retired per-surface local files or registry files for continuity.
Preserve durable requirements here, then inspect current source state, rendered
output, command output, or CI evidence when the task needs more detail.

## Compact surface discipline

Keep this file as a routing map. Do not turn it into surface documentation.

| Rule | Requirement |
| --- | --- |
| Row count | Use one row per surface. Add another row only when the active issue proves one row cannot carry a durable routing requirement. |
| Row content | Limit rows to read triggers, never-do constraints, required evidence categories, validation routing, and deep source links. |
| Examples | Do not add examples unless they are necessary to disambiguate surface routing. Put recurring failure examples in [`../context/evals.md`](../context/evals.md) and task-specific examples in active issues or PRs. |
| Details | Keep durable surface details in current source evidence, active issues, or later scoped changes. Do not encode manuals here. |
| Expansion | Prefer tightening an existing row over adding sections, subsections, or new surface hierarchy. |

## Surface map

| Surface | Read when | Never do | Required evidence | Validation routing | Deep source links |
| --- | --- | --- | --- | --- | --- |
| Chezmoi | Work touches or cites source-state templates, scripts, attributes, externals, hooks, rendered target state, or phase-sensitive provisioning. | Do not edit rendered target state, treat source-state paths as target paths, normalize Go Template whitespace, rewrite trigger comments, or move script logic as cleanup. | Current source state, affected data or template consumers, and rendered-output or trigger evidence when rendered behavior is claimed or changed. | Documentation-only edits use [`validation.md`](./validation.md). Behavior edits need `chezmoi diff`, `chezmoi execute-template`, trigger review, rendered branch inspection, or host-specific evidence that matches the touched path. | [`.chezmoiscripts/`](../../.chezmoiscripts/), [`.chezmoidata/`](../../.chezmoidata/), [`.chezmoitemplates/`](../../.chezmoitemplates/), [`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl), [`.chezmoiignore.tmpl`](../../.chezmoiignore.tmpl) |
| Mise | Work touches or cites `.mise.toml`, tool declarations, file tasks, task metadata, grouping, aliases, dependencies, doctor checks, tool resolution, or repair-adjacent behavior. | Do not rename, regroup, split, delete, or change task metadata, aliases, dependencies, executable bits, tool versions, dependencies, or lockfiles unless scoped. Do not infer source ownership from local task visibility alone. | Current task source state, managed target-path awareness, tool declarations, and task visibility or command output when behavior is claimed or changed. | Behavior edits need relevant `mise tasks info`, `mise tasks deps`, `mise run <task>`, `mise run doctor`, rendered-output inspection, or CI evidence according to the changed task or tool path. | [`.mise.toml`](../../.mise.toml), [`.chezmoidata/tools.yaml`](../../.chezmoidata/tools.yaml), [`dot_config/mise/tasks/`](../../dot_config/mise/tasks/), [`dot_config/mise/config.toml.tmpl`](../../dot_config/mise/config.toml.tmpl) |
| WSL2 | Work touches or cites Windows 11 plus WSL2 Ubuntu behavior, Windows interop, `op.exe`, `npiperelay.exe`, user systemd, SSH agent bridge behavior, or Windows-side sync paths. | Do not treat WSL2 as ordinary Linux, replace Windows bridge assumptions with generic Unix SSH agent assumptions, normalize Windows paths as cleanup, or use GitHub Actions Ubuntu as proof of local WSL2 behavior. | Host-specific WSL2 evidence, Windows interop evidence, rendered WSL branches, user service state, and SSH agent bridge evidence when WSL2 behavior is claimed or changed. | WSL2 behavior edits require local WSL2 evidence that matches the bridge, service, sync path, or rendered branch. Remote CI cannot substitute for local WSL2 convergence evidence. | [README](../../README.md), [`dot_config/systemd/user/1password-bridge.service.tmpl`](../../dot_config/systemd/user/1password-bridge.service.tmpl), [`.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_51-sync-windows-agent.sh.tmpl), [`dot_config/1Password/ssh/private_agent.toml.tmpl`](../../dot_config/1Password/ssh/private_agent.toml.tmpl) |
| Identity | Work touches or cites 1Password identity metadata, generated Git identity files, SSH signing, scoped Git identity routing, SSH config, SSH agent behavior, or secret-adjacent evidence. | Do not print secrets, private keys, public key material unless required, account IDs, item IDs, local profile paths, generated identity output, or SSH agent output unnecessarily. Do not change identity routing as cleanup. | Redacted structural evidence, current identity source state, templates, SSH config routing, and rendered-output inspection when identity behavior is claimed or changed. | Identity behavior edits need redacted rendered-output inspection, scoped Git config inspection, `doctor:identity`, SSH signing or agent checks, and host-specific evidence that matches the changed identity path. | [`.chezmoi.toml.tmpl`](../../.chezmoi.toml.tmpl), [`.chezmoitemplates/git_identity_config.tmpl`](../../.chezmoitemplates/git_identity_config.tmpl), [`.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl`](../../.chezmoiscripts/run_onchange_after_50-converge-identities.sh.tmpl), [`dot_config/ssh/`](../../dot_config/ssh/), [`dot_config/mise/tasks/doctor/executable_identity.tmpl`](../../dot_config/mise/tasks/doctor/executable_identity.tmpl) |
| Neovim | Work touches or cites Neovim source state, LazyVim configuration, providers, plugin state, `lazy-lock.json`, rendered Neovim templates, or headless integration. | Do not treat this repository as a generic Neovim distribution, edit rendered Neovim target files, change plugins, keymaps, providers, or `lazy-lock.json` as incidental cleanup, or hand-edit lockfile state. | Current Neovim source state, provider evidence, lockfile evidence, and headless integration output when Neovim behavior is claimed or changed. | Neovim behavior edits need checks such as `mise run integrate:nvim`, `doctor:nvim`, headless startup, provider checks, lockfile synchronization evidence, or rendered-output inspection according to the touched files. | [`dot_config/nvim/`](../../dot_config/nvim/), [`dot_config/nvim/lazy-lock.json`](../../dot_config/nvim/lazy-lock.json), [`dot_config/mise/tasks/integrate/executable_nvim.tmpl`](../../dot_config/mise/tasks/integrate/executable_nvim.tmpl), [`dot_config/mise/tasks/doctor/executable_nvim.tmpl`](../../dot_config/mise/tasks/doctor/executable_nvim.tmpl), [`dot_config/mise/tasks/update/executable_lazy-lock.tmpl`](../../dot_config/mise/tasks/update/executable_lazy-lock.tmpl) |
| GitHub Actions | Work touches or cites `.github/workflows/**`, compliance CI semantics, action pins, permissions, matrix entries, workflow phase order, branch-protection claims, or remote CI status. | Do not infer remote CI from local checks, infer local workstation convergence from CI, change workflow triggers, permissions, action pins, matrix, or phase commands as documentation cleanup, or add secrets or environments without scope. | Workflow diff, current workflow source, action pin context, PR or branch evidence, and GitHub Actions run evidence when CI status is claimed or required. | Workflow behavior edits require remote GitHub Actions evidence after PR creation when CI status is claimed or required. Local checks do not prove remote CI status. | [`.github/workflows/compliance.yml`](../../.github/workflows/compliance.yml), [`.github/pull_request_template.md`](../../.github/pull_request_template.md), [`.github/ISSUE_TEMPLATE/change-request.yml`](../../.github/ISSUE_TEMPLATE/change-request.yml) |

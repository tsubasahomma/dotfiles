# Chezmoi/Mise convergence debt archive

## Purpose

This file is a durable archive summary of the Chezmoi/Mise convergence debt
inventory. It is not current repository-local routing guidance and does not
change script behavior, hook wiring, task discovery, task names, task metadata,
removal policy, README commands, generated artifacts, rendered targets, package
lists, tool versions, runtime versions, lockfiles, or CI semantics.

Use [`README.md`](../../README.md) for the current operator entry point. Use
[`surfaces.md`](./surfaces.md), [`validation.md`](./validation.md),
[`workflows.md`](./workflows.md), [`repomix.md`](./repomix.md), and
[`teardown.md`](./teardown.md) for current repository-local routing.

The previous row-level inventory table was removed from long-term docs because
it preserved old task paths, obsolete hook names, staging notes, and
time-bound audit wording that no longer helped maintain the current source
state. Use git history when the original evidence packet is needed for
forensics.

## Current source-state summary

- The pre-source-state hook is `.bootstrap-mise.sh`; no identity-named
  bootstrap hook is retained.
- `.chezmoiscripts/**` contains six lifecycle adapters:
  `.chezmoiscripts/run_onchange_before_00-provision-linux-packages.sh.tmpl`,
  `.chezmoiscripts/run_onchange_before_provision-macos-homebrew.sh.tmpl`,
  `.chezmoiscripts/run_onchange_before_provision-windows-packages.sh.tmpl`,
  `.chezmoiscripts/run_onchange_after_20-mise-post-apply-graph.sh.tmpl`,
  `.chezmoiscripts/run_onchange_after_wsl-retire-1password-bridge.sh.tmpl`, and
  `.chezmoiscripts/run_onchange_after_wsl-sync-services.sh.tmpl`.
- Repo-owned mise task source state lives under
  `dot_config/mise/repo-tasks/**`; `dot_config/mise/tasks/**` is absent from
  source state.
- `dot_config/mise/config.toml.tmpl` sets `task_config.includes` to
  `.config/mise/repo-tasks`, so the repo-owned config scope does not use the
  default `.config/mise/tasks` discovery path.
- Current repo-owned task families include `build:*`, `cache:*`, hidden
  `check:*`, public `doctor`, `generate:*`, hidden `lifecycle:*`,
  `provision:*`, `repair:*`, `sync:*`, and `update:*`.
- Local rendered `mise tasks` visibility is host and target-state evidence, not
  source-state truth. It can omit WSL-only rendered tasks or reflect local
  drift.
- `.chezmoiremove.tmpl` is narrow target-relative migration policy. It should
  remove only evidence-backed target paths, not broad directories, app-owned
  host paths, or unmanaged local/private files.

## Durable decisions

| Area | Archived decision | Current evidence boundary |
| --- | --- | --- |
| Chezmoi lifecycle scripts | Keep only sparse lifecycle adapters when Chezmoi ordering is required for first-run apply or host provisioning. | Inspect `.chezmoiscripts/**`, trigger comments, rendered script output, and source-state consumers before changing script behavior. |
| Pre-source-state bootstrap | Keep a non-template POSIX hook that ensures `mise` exists before source-state reads. The hook name must describe mise/tool bootstrap ownership, not identity ownership. | Inspect `.bootstrap-mise.sh`, `.chezmoi.toml.tmpl`, rendered hook stanzas, and Chezmoi hook semantics. |
| Mise task discovery | Keep repo-owned tasks outside the default `.config/mise/tasks` drift surface. | Inspect `dot_config/mise/config.toml.tmpl`, `dot_config/mise/repo-tasks/**`, and rendered task visibility. |
| Task taxonomy | Keep source-owned tasks in explicit owner families: provisioning, generation, caches, builds, sync, checks, repairs, updates, and public `doctor`. | Use `mise tasks validate`, `mise tasks ls --extended --hidden`, and task-level metadata evidence. |
| Workspace directories | Do not create identity-routed workspace directories automatically during apply. | Treat identity directory metadata as Git include routing unless a managed target-state requirement is proven. |
| WSL2 sync and authentication | Keep WSL2 sync and authentication behavior behind host-specific tasks and adapters, with no GitHub Actions claim for local Windows OpenSSH or 1Password behavior. | Require maintainer-local host evidence for Windows interop, Windows OpenSSH, 1Password Desktop, 1Password SSH agent, and WezTerm Windows sync claims. |
| Remove targets | Keep removal policy file-specific, target-relative, and evidence-backed. | Validate `.chezmoiremove.tmpl` with rendered output and dry-run or verbose evidence when it changes. |
| Public commands | Keep `chezmoi init --apply` as the first-run convergence path and `mise run doctor` as the stable public health-check command. | Treat repair, update, verification, teardown, and troubleshooting commands as scoped maintainer workflows unless README and source evidence prove otherwise. |

## Current routing

| Need | Current source |
| --- | --- |
| Operator bootstrap and maintenance commands | [`../../README.md`](../../README.md) |
| Behavior-sensitive source routing | [`surfaces.md`](./surfaces.md) |
| Local validation baseline | [`validation.md`](./validation.md) |
| Repository-local workflow exceptions | [`workflows.md`](./workflows.md) |
| Repomix local paths and recipes | [`repomix.md`](./repomix.md) |
| Destructive local teardown guidance | [`teardown.md`](./teardown.md) |

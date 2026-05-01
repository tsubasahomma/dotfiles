# Architecture documentation routing

`ARCHITECTURE.md` is a routed legacy architecture entry point and high-level
repository overview. Focused docs under [`docs/chezmoi/`](./docs/chezmoi/) are
the source of truth for chezmoi orchestration contracts.

This document keeps durable repository context and routes readers to focused
contract documents. It does not define the detailed chezmoi action graph, script
trigger contracts, bootstrap and identity boundaries, mise task delegation, data
ownership, or WSL2 convergence validation by itself.

## Current role

Use this file for:

- a high-level map of repository architecture documentation;
- operational teardown guidance that existing README links depend on;
- durable context that is not better owned by a focused contract document;
- follow-up candidates for future documentation relocation or replacement.

Do not use this file as the detailed source of truth for behavior-sensitive
chezmoi refactoring. Start from the focused contract document that matches the
touched surface.

## Focused chezmoi contract documents

| Surface | Source of truth |
| :------ | :-------------- |
| Current chezmoi action graph, script order, script contracts, and validation surfaces | [`docs/chezmoi/action-graph.md`](./docs/chezmoi/action-graph.md) |
| Read-only commands for collecting script-contract evidence | [`docs/chezmoi/script-contract-inspection.md`](./docs/chezmoi/script-contract-inspection.md) |
| Audit of current script trigger contracts and trigger follow-up candidates | [`docs/chezmoi/script-trigger-audit.md`](./docs/chezmoi/script-trigger-audit.md) |
| Bootstrap, 1Password, identity, SSH signing, SSH agent, WSL2 bridge, and CI fallback boundaries | [`docs/chezmoi/bootstrap-identity-boundary.md`](./docs/chezmoi/bootstrap-identity-boundary.md) |
| Boundary between `.chezmoiscripts/*` and repository-local mise tasks | [`docs/chezmoi/mise-task-boundary.md`](./docs/chezmoi/mise-task-boundary.md) |
| Static `.chezmoidata/`, dynamic `.chezmoi.toml.tmpl`, reusable template, and data consumer boundaries | [`docs/chezmoi/data-contract-boundary.md`](./docs/chezmoi/data-contract-boundary.md) |
| Local WSL2 convergence validation expectations and redaction guidance | [`docs/chezmoi/wsl2-convergence-validation.md`](./docs/chezmoi/wsl2-convergence-validation.md) |

## High-level repository model

This repository is a chezmoi-managed dotfiles source-state repository. At a high
level, it combines:

- `chezmoi` source-state files, templates, externals, hooks, and scripts;
- repository-local `mise` toolchain and task definitions;
- static repository data under `.chezmoidata/`;
- dynamic host, path, identity, 1Password, SSH, and WSL2 data derived during
  chezmoi template evaluation;
- rendered target configuration for shell, Git, SSH, 1Password, Homebrew, mise,
  WezTerm, Neovim, and related tools;
- local validation and GitHub Actions compliance checks.

This overview is intentionally narrow. Detailed sequencing, rerun behavior,
hard-fail boundaries, soft-fallback boundaries, and validation expectations live
in the focused docs listed above.

## Operational teardown guidance

The following purge sequence is operational teardown guidance for removing the
currently managed local state. It is not a full architecture contract and does
not prove convergence, idempotency, or behavior preservation.

### De-provisioning (Purge) Sequence

To reverse the managed infrastructure state and restore the host toward a clean
environment, execute the following steps in order.

#### 1. Selective managed state removal

Remove only files and directories currently reported as managed by chezmoi. This
minimizes impact on unmanaged local data.

```zsh
# Remove managed targets relative to HOME
chezmoi managed --path-style absolute -0 | xargs -0 rm -rf --

# Remove chezmoi's own configuration and source state
chezmoi purge
```

#### 2. Platform-specific teardown

**macOS (Apple Silicon)**:

- **Package force-sync**: Remove Homebrew-managed packages and Homebrew itself
  when a full host reset is intended.
  ```zsh
  brew list --cask | xargs -I {} brew uninstall --cask --zap {}
  NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
  sudo rm -rf /opt/homebrew
  ```
- **TCC revocation**: Manually revoke Full Disk Access for the terminal emulator
  in System Settings.

**WSL2 (Ubuntu)**:

- **Service termination**: Stop and disable the user-level identity bridge.
  ```zsh
  systemctl --user disable --now 1password-bridge.service
  rm -f "$HOME/.1password/agent.sock"
  ```
- **Shell reversion**: Restore the default system shell when a full reset is
  intended.
  ```zsh
  sudo chsh -s /bin/bash "$USER"
  ```

#### 3. Local state wipe (optional / aggressive)

> [!WARNING]
> The following command permanently deletes application configurations, local
> data, caches, and shell history under the selected directories. Execute only
> when a total local environment reset is intended.

```zsh
rm -rf "$HOME/.config" "$HOME/.local" "$HOME/.cache"
```

## Follow-up candidates

The current routing keeps `ARCHITECTURE.md` as a thin legacy entry point. Future
issues may evaluate whether to:

- retire `ARCHITECTURE.md` after all inbound links route elsewhere;
- move architecture routing under `docs/`;
- rename this file to better reflect its routing role;
- move purge and de-provisioning guidance to a workflow or operations document;
- replace remaining high-level architecture prose with narrower focused docs.

These are candidates only. They are not hidden requirements for the current
routing shape.

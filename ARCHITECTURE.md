# Architecture documentation routing

`ARCHITECTURE.md` is a high-level repository overview and teardown routing entry
point. Detailed assistant context lives under
[docs/context/](./docs/context/README.md).

This document keeps durable repository context and routes readers to current
context documents and source-state surfaces. It does not define the detailed
chezmoi action graph, script trigger contracts, bootstrap and identity
boundaries, mise task delegation, data ownership, or WSL2 convergence validation
by itself.

## Current role

Use this file for:

- a high-level map of repository architecture documentation;
- operational teardown guidance that existing README links depend on;
- durable context that is not better owned by a focused context document;
- routing readers to current source-state and validation surfaces.

Do not use this file as the detailed source of truth for behavior-sensitive
chezmoi refactoring. Start from the context document or source-state surface that
matches the touched area.

## Focused context documents

| Surface | Current routing |
| :------ | :-------------- |
| Context architecture and active context routing | [`docs/context/README.md`](./docs/context/README.md) |
| Repository identity, source-state model, behavior boundaries, validation baseline, and documentation entry points | [`docs/context/repo.md`](./docs/context/repo.md) |
| Chezmoi source state, templates, scripts, rendered target state, and phase gates | [`docs/context/local/surfaces/chezmoi.md`](./docs/context/local/surfaces/chezmoi.md) |
| Mise tasks, task metadata, doctor checks, and task ownership evidence | [`docs/context/local/surfaces/mise.md`](./docs/context/local/surfaces/mise.md) |
| 1Password, identity discovery, SSH signing, and agent routing | [`docs/context/local/surfaces/identity.md`](./docs/context/local/surfaces/identity.md) |
| WSL2 bridge assumptions and local validation boundaries | [`docs/context/local/surfaces/wsl2.md`](./docs/context/local/surfaces/wsl2.md) |
| GitHub Actions CI semantics and remote CI evidence | [`docs/context/local/surfaces/github-actions.md`](./docs/context/local/surfaces/github-actions.md) |
| Issue, PR, validation, merge, closure, Commander, and Worker procedures | [`docs/context/local/workflows/README.md`](./docs/context/local/workflows/README.md) |

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
hard-fail boundaries, soft-fallback boundaries, and validation expectations
should be inspected from current source state and routed through the context
documents listed above.

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

Future issues may evaluate whether to:

- retire `ARCHITECTURE.md` after all inbound links route elsewhere;
- move architecture routing under `docs/`;
- rename this file to better reflect its routing role;
- move purge and de-provisioning guidance to a workflow or operations document;
- replace remaining high-level architecture prose with narrower focused docs.

These are candidates only. They are not hidden requirements for the current
routing shape.

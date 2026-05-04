# Repository teardown

## Purpose

Define repository-local teardown guidance for intentionally removing the
workstation state managed by this dotfiles source-state repository.

Use this file only when a full or partial local reset is intended. This file does
not define convergence, idempotency, repair, validation, or behavior-preserving
change procedure.

## Responsibility boundary

This file owns destructive local teardown guidance for managed workstation state.
It does not own generic evidence precedence ([`../context/kernel.md`](../context/kernel.md)),
output formatting ([`../context/protocols.md`](../context/protocols.md)), reusable
workflow procedure ([`../context/workflows.md`](../context/workflows.md)), local
surface routing ([`surfaces.md`](./surfaces.md)), or local validation routing
([`validation.md`](./validation.md)).

## Safety boundary

Teardown commands are destructive operator actions. Do not run them as cleanup,
validation, repair, or documentation-maintenance steps.

Before deleting managed targets, inspect what chezmoi currently manages:

```zsh
chezmoi managed --path-style absolute
```

Do not use teardown commands as proof of repository correctness. They remove
local state; they do not validate source state, rendered output, task behavior,
CI behavior, identity routing, or host convergence.

## Managed state removal

Remove only files and directories currently reported as managed by chezmoi. This
minimizes impact on unmanaged local data.

```zsh
chezmoi managed --path-style absolute -0 | xargs -0 rm -rf --
chezmoi purge
```

`chezmoi purge` removes chezmoi's own configuration and source state after the
managed target cleanup.

## Platform-specific teardown

### macOS Homebrew reset

When a full macOS host reset is intended, remove Homebrew-managed packages and
Homebrew itself separately from managed dotfile targets:

```zsh
brew list --cask | xargs -I {} brew uninstall --cask --zap {}
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
sudo rm -rf /opt/homebrew
```

Manually revoke terminal Full Disk Access in System Settings when the reset must
also remove prior local privacy grants.

### WSL2 identity bridge reset

When a full WSL2 reset is intended, stop the user-level 1Password SSH agent
bridge and remove the bridge socket:

```zsh
systemctl --user disable --now 1password-bridge.service
rm -f "$HOME/.1password/agent.sock"
```

Restore the default shell only when the host should no longer use the managed
shell baseline:

```zsh
sudo chsh -s /bin/bash "$USER"
```

## Aggressive local state wipe

> [!WARNING]
> The following command permanently deletes application configuration, local
> data, caches, and shell history under the selected directories. Execute only
> when a total local environment reset is intended.

```zsh
rm -rf "$HOME/.config" "$HOME/.local" "$HOME/.cache"
```

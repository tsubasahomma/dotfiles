# Deterministic Infrastructure Engine

[![Infrastructure Compliance](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml/badge.svg)](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with chezmoi](https://img.shields.io/badge/built%20with-chezmoi-50b0f0.svg)](https://chezmoi.io/)

A zero-drift, deterministic provisioning engine for macOS Tahoe (26.4.1+) and WSL2 (Ubuntu 24.04+).

## Overview

This repository enforces infrastructure as a deterministic state. It leverages `chezmoi` for state management and `mise-en-place` for hermetic toolchain isolation, using 1Password as the Single Source of Truth (SSOT) for identity and secrets.

## Prerequisites (Tier -2)

The following manual configurations are **Hard Blocking Requirements**. They must be established to satisfy foundational security and communication gates before automation can evaluate identity templates.

### 1. Universal (macOS & WSL2)

- **1Password Desktop**: [Install and sign in](https://1password.com/downloads/).
- **1Password CLI (op)**: [Install](https://developer.1password.com/docs/cli/get-started/) and enable [App Integration](https://developer.1password.com/docs/cli/app-integration/).
- **1Password SSH Key Schema**: The engine requires specific metadata to route Git identities. Each SSH Key item must be tagged and structured as follows:

| Attribute   | Value / Field Label  | Requirement                                               |
| :---------- | :------------------- | :-------------------------------------------------------- |
| **Tag**     | `dotfiles-ssh-key`   | Mandatory for discovery                                   |
| **Section** | `dotfiles`           | Field grouping                                            |
| **Field**   | `dotfiles_git_name`  | Your Git display name                                     |
| **Field**   | `dotfiles_git_email` | Your Git email address                                    |
| **Field**   | `dotfiles_git_dirs`  | Comma-separated globs (e.g., `~/src/work,~/src/personal`) |

#### Quick Provisioning (CLI)

You can create a compliant item using the `op` CLI (assuming a 'Development' vault exists):

```bash
op item create --category='SSH Key' --title='Personal' \
  --vault='Development' --tags='dotfiles-ssh-key' \
  'dotfiles.dotfiles_git_name[text]=Your Name' \
  'dotfiles.dotfiles_git_email[email]=user@example.com' \
  'dotfiles.dotfiles_git_dirs[text]=~/src/github.com/yourname/,~/src/gitlab.com/yourname/*'
```

### 2. macOS Specific

- **Full Disk Access (FDA)**: Grant FDA to your terminal emulator (e.g., WezTerm) in `System Settings > Privacy & Security > Full Disk Access`. This is required to prevent TCC-related deadlocks during automated provisioning of protected directories.

### 3. WSL2 Specific

- **npiperelay.exe (Architecture Dependency)**:
  - **Requirement**: Must be available in the Windows PATH.
  - **Installation**: `winget.exe install albertony.npiperelay`
  - **Rationale**: The `chezmoi init` phase executes Go templates that call the 1Password CLI (`op`) to fetch identity metadata. Without the relay bridging the WSL2 socket to the Windows Named Pipe, the template evaluation will fail, blocking the entire bootstrap.
- **Non-interactive Sudo**: Configure `visudo` to allow the infrastructure engine to provision system packages without interactive prompts.
  ```bash
  # Execute 'sudo visudo' and append the following:
  ${USER} ALL=(ALL) NOPASSWD:ALL
  ```

## Installation (Bootstrap)

Initialize the engine using the following command. This command injects a `GITHUB_TOKEN` to bypass API rate limits during the initial toolchain convergence.

```zsh
# Read the PAT from 1Password (SSOT) or provide it manually
export GITHUB_TOKEN=$(op read "op://Development/mise-cli-token/credential")

# Initialize and apply the state
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <your-github-username>
```

## Verification

Run the diagnostic suite to verify toolchain integrity and identity routing.

```zsh
mise run doctor
```

## Maintenance

- **Update Toolchains**: `mise install`
- **Update Neovim Locks**: `mise run update:lazy-lock`
- **Check Drift**: `chezmoi verify`
- **De-provisioning (Purge)**: Restore the host to its original state by following the [Purge Sequence in ARCHITECTURE.md](./ARCHITECTURE.md).

## LLM collaboration

Detailed LLM-assisted maintenance rules live in:

- [Repository agent guidance](./AGENTS.md)
- [LLM collaboration guidance](./docs/llm/README.md)
- [Workflow documentation](./docs/workflows/README.md)

## References

- [chezmoi Documentation](https://www.chezmoi.io/user-guide/command-overview/)
- [mise-en-place Documentation](https://mise.jdx.dev/)
- [1Password CLI Reference](https://developer.1password.com/docs/cli/reference/)

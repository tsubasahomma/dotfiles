# Deterministic Infrastructure Engine

[![Infrastructure Compliance](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml/badge.svg)](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with chezmoi](https://img.shields.io/badge/built%20with-chezmoi-50b0f0.svg)](https://chezmoi.io/)
[![Managed by mise](https://img.shields.io/badge/managed%20by-mise-ff4e41.svg)](https://mise.jdx.jdx.dev/)

> **"Infrastructure as a Deterministic State."**
>
> This repository is a strict provisioning engine designed to enforce a zero-drift developer environment across macOS and Linux platforms.

---

## 🏛 Architecture Philosophy

The infrastructure remains invariant by adhering to core determinism laws:

1. **Zero-Speculation Identity**: Identities are resolved via **1Password CLI**.
2. **Absolute Idempotency**: The state is guaranteed to converge.
3. **Hermetic Toolchain**: System-level pollution is avoided by pinning all runtimes via `mise`.
4. **XDG Purism**: 100% compliance with the XDG Base Directory Specification.

## 🛠 Prerequisites (Tier -2)

The following MUST be manually established before initializing the engine. These are **Absolute Requirements** and are not managed by this repository to avoid circular dependencies.

1. **1Password Desktop**: [Download and install](https://1password.com/downloads/).
2. **1Password CLI (`op`)**: [Install the CLI binary](https://developer.1password.com/docs/cli/get-started/).
3. **Identity Authentication**:
   - Run `op signin`.
   - Ensure you are authenticated and can run `op item list`.
4. **Credential Setup**:
   - Create a Document or Login item in 1Password at `op://Development/mise-cli-token/credential` containing a GitHub Personal Access Token (PAT) with `read:packages` scope.
5. **SSH Key Items**: Create SSH Key items in 1Password tagged `dotfiles-ssh-key`. Each must have a `dotfiles` section with:
   - `dotfiles_git_name`: Display Name
   - `dotfiles_git_email`: Git Email
   - `dotfiles_git_dirs`: Comma-separated paths (for example, `~/src/work,~/src/oss`)

## 🚀 Initialization

Once the prerequisites are met, bootstrap the environment:

```zsh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply tsubasahomma
```

## 🩺 Diagnostics

Run the doctor command to verify identity mapping and authentication status:

```zsh
mise run doctor
```

## ⚖️ License

MIT License.

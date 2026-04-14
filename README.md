# Deterministic Infrastructure Engine

[![Infrastructure Compliance](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml/badge.svg)](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with chezmoi](https://img.shields.io/badge/built%20with-chezmoi-50b0f0.svg)](https://chezmoi.io/)
[![Managed by mise](https://img.shields.io/badge/managed%20by-mise-ff4e41.svg)](https://mise.jdx. jdx.dev/)

> **"Infrastructure as a Deterministic State."**
>
> This repository is a strict provisioning engine designed to enforce a zero-drift developer environment across macOS and Linux platforms.

---

## 🏛 Architecture Philosophy

The infrastructure remains invariant by adhering to core determinism laws:

1. **Zero-Speculation Identity**: Identities are never hardcoded. They are dynamically resolved via **1Password CLI**.
2. **Absolute Idempotency**: The state is guaranteed to converge. A second execution of `chezmoi apply` always produces a zero-diff output.
3. **Hermetic Toolchain**: System-level pollution is avoided by pinning all runtimes within isolated `mise` environments.
4. **XDG Purism**: 100% compliance with the XDG Base Directory Specification.

## 🛠 Prerequisites

1. **Network Utilities**: `curl` must be installed.
2. **Extraction Utilities**: `unzip` (or `python3`) must be installed.
3. **Identity Setup**: Create SSH Key items in 1Password tagged `dotfiles-ssh-key`. Each must have a `dotfiles` section with:
   - `dotfiles_git_name`: Display Name
   - `dotfiles_git_email`: Git Email
   - `dotfiles_git_dirs`: Comma-separated paths (e.g., `~/src/work,~/src/oss`)

## 🚀 Identity Synchronization

The system uses a two-phase synchronization protocol:

1. **Provisioning (`chezmoi init`)**: Re-evaluates 1Password items and updates the static identity schema. Run this whenever you modify identity metadata in 1Password.
2. **Convergence (`chezmoi apply`)**: Exports physical SSH keys and generates scoped Git configurations based on the current schema.

## 🩺 Diagnostics

Run the doctor command to verify identity mapping and authentication status:

```zsh
doctor
```

## ⚖️ License

MIT License.

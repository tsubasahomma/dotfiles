# Deterministic Infrastructure | Eternal Platform

[![Infrastructure Compliance](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml/badge.svg)](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with chezmoi](https://img.shields.io/badge/built%20with-chezmoi-50b0f0.svg)](https://chezmoi.io/)
[![Managed by mise](https://img.shields.io/badge/managed%20by-mise-ff4e41.svg)](https://mise.jdx.dev/)

> **"Infrastructure as a Pure Function."**
>
> This is not just a collection of dotfiles. It is a **deterministic provisioning engine** designed for the next decade of professional software engineering.

---

## 🏛 Architecture Philosophy

Most dotfiles degrade over time. The **Eternal Platform** remains invariant by adhering to four fundamental laws:

1. **Zero-Speculation Identity**: Identities are never hardcoded. They are dynamically resolved via **1Password CLI** using schema-driven Identity Pointers.
2. **Absolute Idempotency**: The state is guaranteed to converge. A second execution of `chezmoi apply` always produces a zero-diff output, verified by rigorous **multi-OS CI matrix**.
3. **Hermetic Toolchain**: System-level pollution is avoided by pinning all runtimes (Go, Python, Node.js, Rust) within isolated `mise` environments.
4. **XDG Purism**: 100% compliance with the XDG Base Directory Specification. Your `$HOME` remains a pristine workspace, not a dumping ground for config files.

## 📦 What's Inside?

### 🛠 Core Stack

- **Manager**: `chezmoi` (State-driven configuration)
- **Runtime**: `mise` (Hermetic toolchain management)
- **Identity**: `1Password CLI` (Zero-knowledge secrets management)

### 💻 Developer Environment

- **Shell**: `Zsh` with optimized XDG-based autoloading
- **Editor**: `Neovim` (LazyVim distribution) with isolated Python/Node providers
- **Terminal**: `WezTerm` (Nightly) for SOTA graphics protocol support
- **Git**: Supercharged with `delta` (side-by-side diffs) and `git-absorb`
- **Prompt**: `Starship` (Cross-shell performance optimized)

## 🚀 One-Liner Bootstrap

Securely provision your entire machine from a raw OS state in seconds:

```zsh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <your-github-username>
```

## 🛠 Prerequisites

Before running the bootstrap, ensure your **1Password** vault is prepared:

1. **Identity Pointer**: Create an item with the tag `dotfiles-ssh-key`.
2. **Environment Link**: Add a custom field named `dotfiles-id` (e.g., `personal`, `work`).
3. **Signing**: Register your SSH key as a **"Signing Key"** in GitHub for the **Verified** status.

## 🩺 Continuous Health Monitoring

The platform includes a built-in diagnostic engine to ensure your local environment never drifts from the defined schema:

```zsh
doctor
```

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

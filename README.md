# Deterministic Infrastructure Engine

[![Infrastructure Compliance](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml/badge.svg)](https://github.com/tsubasahomma/dotfiles/actions/workflows/compliance.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with chezmoi](https://img.shields.io/badge/built%20with-chezmoi-50b0f0.svg)](https://chezmoi.io/)
[![Managed by mise](https://img.shields.io/badge/managed%20by-mise-ff4e41.svg)](https://mise.jdx.dev/)

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

## 🛠 Prerequisites (Minimal Prepared OS)

This platform **DOES NOT** bootstrap from a completely raw OS. To guarantee deterministic execution without interactive hanging or network resolution failures, the host OS must meet the following strict prerequisites (Tier -1):

1. **Network Utilities**: `curl` must be installed.
2. **Extraction Utilities**: `unzip` (or `python3`) must be installed.
3. **Privilege Escalation (Linux only)**: Non-interactive `sudo` must be configured.
   - Example configuration via `visudo`: `<username> ALL=(ALL) NOPASSWD:ALL`
4. **Identity Pointer**: A 1Password item tagged `dotfiles-ssh-key` must exist in your vault.

## 🚀 One-Liner Bootstrap

Once the prerequisites are met, provision the machine:

```zsh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <your-github-username>
```

## 🩺 Continuous Health Monitoring

The platform includes a built-in diagnostic engine (`doctor`) to ensure your local environment never drifts from the defined schema. Run it periodically:

```zsh
doctor
```

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

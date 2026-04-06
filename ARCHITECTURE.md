# Engineering Specification | Eternal Platform

This document defines the architectural constraints and technical logic of the Deterministic Infrastructure. It serves as the single source of truth (SSOT) for the platform's internal mechanics.

## 1. Design Philosophy

The system is designed as a **Pure Function**: Given a raw OS and a 1Password session, the output must be a mathematically convergent environment.

- **Deterministic State**: System state is driven by declarative schemas (`.chezmoidata.yaml`) rather than imperative commands.
- **Zero-Speculation Identity**: Personal data is never stored in the repository. Identities are resolved dynamically at runtime.
- **Hermetic Isolation**: Global system pollution is minimized by encapsulating runtimes within isolated environments managed by `mise`.

## 2. Provisioning Lifecycle

Execution follows a strict sequential phase-gate model to resolve binary dependencies:

1.  **Phase 00 (Pre-flight & Discovery)**: Validates the 1Password session, caches GitHub host keys, and backups legacy configurations.
2.  **Phase 00 (External Bootstrap)**: Directly retrieves `mise` and `jq` binaries using SHA-256 integrity verification.
3.  **Phase 10 (System Provisioning)**: Injects OS-level dependencies via `Brewfile` (macOS) or system package managers (Linux).
4.  **Phase 20 (Runtime Convergence)**: Provisioning of language runtimes (Python, Node.js, Go, Rust) and Neovim providers via absolute paths.
5.  **Phase 50 (Identity Export)**: Dynamic extraction of public keys from 1Password based on the `dotfiles-ssh-key` tag.

## 3. Security & Identity Architecture

### Zero-Knowledge Secrets
Secrets and private keys are never written to disk. The system leverages the **1Password SSH Agent** for all cryptographic operations.

### Hybrid Identity Routing (Git)
The platform enforces context awareness by omitting a global `user.email`. Routing is determined by the filesystem path:

- **Managed Context**: Repositories under `~/src/github.com/{{ .gh_user }}` and the dotfiles source directory automatically assume the personal identity.
- **Unmanaged Context (The Absorber)**: External or work-related projects use `~/.gitconfig.local` for manual identity overriding, maintaining host integrity.

## 4. Filesystem Standards (XDG Compliance)

The environment strictly adheres to the **XDG Base Directory Specification** to ensure a clean `$HOME`:

- **Config**: `~/.config`
- **Data**: `~/.local/share`
- **State**: `~/.local/state`
- **Cache**: `~/.cache`

## 5. Compliance & Verification

- **Idempotency Proof**: Continuous integration (GitHub Actions) verifies that the infrastructure can converge across multi-OS matrices (macOS, Ubuntu) without delta.
- **Self-Healing Engine**: The `doctor` binary performs real-time validation of runtime health and cryptographic trust anchors.

---

## ⚖️ License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.

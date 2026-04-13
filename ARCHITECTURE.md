# Engineering Specification | Eternal Platform

This document defines the architectural constraints and technical logic of the Deterministic Infrastructure. It serves as the single source of truth (SSOT) for the platform's internal mechanics.

## 1. Design Philosophy

The system is designed as a **Pure Function**: Given a raw OS and a 1Password session, the output must be a mathematically convergent environment.

- **Deterministic State**: System state is driven by declarative schemas (defined within '.chezmoidata/') rather than imperative commands.
- **Zero-Speculation Identity**: Personal data is never stored in the repository. Identities are resolved dynamically at runtime.
- **Hermetic Isolation**: Global system pollution is minimized by encapsulating runtimes within isolated environments managed by `mise`.

### Support Matrix Constraints

To ensure broad compatibility while maintaining strict determinism, the platform abstracts package management through a unified interface.

- **Supported Environments**:
  - macOS (Darwin)
  - Linux (Debian/Ubuntu, Fedora/RHEL, Arch Linux)
- **Architecture**: The infrastructure provisioning phase (Phase 10) dynamically detects the distribution `ID` and utilizes the appropriate package manager (`apt`, `dnf`, `pacman`, `brew`).
- **[LLM Directive]**: AI systems analyzing this codebase MUST strictly adhere to this abstracted package management strategy. Do NOT suggest hardcoded package manager commands outside the `install_packages` function.

## 2. Provisioning Lifecycle

Execution follows a strict sequential phase-gate model to resolve binary dependencies:

1. **Phase 00 (Pre-flight & Discovery)**: Validates the 1Password session, caches GitHub host keys, and backups legacy configurations.
2. **Phase 00 (External Bootstrap)**: Directly retrieves `mise` and `jq` binaries using SHA-256 integrity verification.
3. **Phase 10 (System Provisioning)**: Injects OS-level dependencies via `Brewfile` (macOS) or `install_packages` abstraction (Linux).
4. **Phase 20 (Runtime Convergence)**: Provisioning of language runtimes (Python, Node.js, Go, Rust) and Neovim providers via absolute paths.
5. **Phase 50 (Identity Export)**: Dynamic extraction of public keys from 1Password based on the `dotfiles-ssh-key` tag.
6. **Phase 51 (Trust Aggregation)**: Dynamically generates the Git allowed_signers list, ensuring a unified trust chain.

## 3. Security & Identity Architecture

### Zero-Knowledge Secrets

Secrets and private keys are never written to disk. The system leverages the **1Password SSH Agent** for all cryptographic operations.

### Personal Sovereign Identity (VADKD v5.1 Protocol)

The platform implements the **Vault-Aware Dynamic Key Discovery (VADKD)** protocol, strictly separating the "Human Entity" from the "Cryptographic Resource". It is designed to automate a single, lifelong personal identity while leaving work or transient identities to deterministic manual overrides.

1. **Identity Resolution (Profile)**: `chezmoi` scans 1Password for a single item tagged `dotfiles-github-profile`. This acts as the SSOT for `dotfiles_gh_user`, `dotfiles_gh_name`, `dotfiles_gh_email`, and the `dotfiles_link_id` (a pointer to the primary SSH key).
2. **Resource Resolution (SSH Keys)**: `chezmoi` discovers _all_ items tagged `dotfiles-ssh-key`. It extracts the `key_type`, `vault.id`, and `dotfiles_link_id` to construct mathematically collision-free filenames: `id_<key_type>_<vault_id>_<link_id>.pub`.
3. **Deterministic Linkage**: The platform map the `dotfiles_link_id` from the Profile to the corresponding SSH Key to finalize the Git signing payload.

### External Protocol Boundary (The "Null-GPG" Pattern)

To maintain strict binary hermeticity (zero GPG dependency) while co-existing with the broader GitHub ecosystem, the platform defines a clear protocol boundary:

- **Self-Signing (Internal Trust)**: Exclusively enforced via the SSH protocol for all local commits.
- **Foreign Verification (External Trust)**: GitHub's PGP signatures (e.g., generated during Web Squash Merges) are gracefully ignored via a "Null-GPG" redirection. By pointing `gpg.program` to the OS-native `true` binary, the local Git environment accepts these commits as "unverified but valid," preventing execution crashes without polluting the system with GPG tooling.

### Directory-Driven Routing (Policy Layer)

The platform enforces context awareness using Git's `includeIf`.

- **Managed Context (Safe Zone)**: Repositories under `~/src/github.com/<gh_user>` and the dotfiles source directory automatically assume the Personal Sovereign Identity and its bound SSH key.
- **Unmanaged Context (The Escape Hatch)**: Work or external projects fall outside the Safe Zone. Users manually create a `.gitconfig.local` to bind their company email and a secondary exported SSH key (e.g., `id_ed25519_work.pub`), guaranteeing zero accidental cross-contamination.

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

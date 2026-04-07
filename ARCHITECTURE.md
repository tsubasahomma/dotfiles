# Engineering Specification | Eternal Platform

This document defines the architectural constraints and technical logic of the Deterministic Infrastructure. It serves as the single source of truth (SSOT) for the platform's internal mechanics.

## 1. Design Philosophy

The system is designed as a **Pure Function**: Given a raw OS and a 1Password session, the output must be a mathematically convergent environment.

- **Deterministic State**: System state is driven by declarative schemas (`.chezmoidata.yaml`) rather than imperative commands.
- **Zero-Speculation Identity**: Personal data is never stored in the repository. Identities are resolved dynamically at runtime.
- **Hermetic Isolation**: Global system pollution is minimized by encapsulating runtimes within isolated environments managed by `mise`.

## 2. Provisioning Lifecycle

Execution follows a strict sequential phase-gate model to resolve binary dependencies:

1. **Phase 00 (Pre-flight & Discovery)**: Validates the 1Password session, caches GitHub host keys, and backups legacy configurations.
2. **Phase 00 (External Bootstrap)**: Directly retrieves `mise` and `jq` binaries using SHA-256 integrity verification.
3. **Phase 10 (System Provisioning)**: Injects OS-level dependencies via `Brewfile` (macOS) or system package managers (Linux).
4. **Phase 20 (Runtime Convergence)**: Provisioning of language runtimes (Python, Node.js, Go, Rust) and Neovim providers via absolute paths.
5. **Phase 50 (Identity Export)**: Dynamic extraction of public keys from 1Password based on the `dotfiles-ssh-key` tag.
6. **Phase 51 (Trust Aggregation)**: Dynamically generates the Git allowed_signers list, ensuring a unified trust chain.

## 3. Security & Identity Architecture

### Zero-Knowledge Secrets

Secrets and private keys are never written to disk. The system leverages the **1Password SSH Agent** for all cryptographic operations.

### Identity Lifecycle & Trust Chain

Identity resolution is a two-stage process designed to be environment-agnostic:

1. **Export (Phase 50)**: Extracts public keys into `~/.ssh/id_ed25519_{{ .primary_id }}.pub`. In headless CI environments, a mock key is injected to bypass 1Password dependencies.
2. **Aggregation (Phase 51)**: Generates `~/.config/git/allowed_signers` by scanning the SSH directory. This programmatic generation eliminates template duality and natively supports multi-key environments.

### External Protocol Boundary (The "Null-GPG" Pattern)

To maintain strict binary hermeticity (zero GPG dependency) while co-existing with the broader GitHub ecosystem, the platform defines a clear protocol boundary:

- **Self-Signing (Internal Trust)**: Exclusively enforced via the SSH protocol for all local commits.
- **Foreign Verification (External Trust)**: GitHub's PGP signatures (e.g., generated during Web Squash Merges) are gracefully ignored via a "Null-GPG" redirection. By pointing `gpg.program` to the OS-native `true` binary, the local Git environment accepts these commits as "unverified but valid," preventing execution crashes without polluting the system with GPG tooling.

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

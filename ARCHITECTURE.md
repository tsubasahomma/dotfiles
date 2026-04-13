# Engineering Specification

This document defines the architectural constraints and technical logic of the Deterministic Infrastructure Engine. It serves as the single source of truth (SSOT) for the platform's internal mechanics.

## 1. Design Philosophy

The system is designed to enforce state convergence: Given a Minimal Prepared OS and a 1Password session, the output must be mathematically identical across executions.

- **Deterministic State**: System state is driven by declarative schemas (`.chezmoidata/`) rather than imperative scripts.
- **Zero-Speculation Identity**: Personal data is never stored in the repository. Identities are resolved dynamically at runtime.
- **Hermetic Isolation**: Global system pollution is minimized by encapsulating runtimes within isolated environments managed by `mise`.

## 2. Tiered Bootstrapping Lifecycle

Execution follows a strict sequential phase-gate model to resolve binary dependencies without interactive hanging.

1. **Tier -1 (Assertion Gate)**: `.bootstrap-identity.sh` strictly validates the existence of `curl`, `unzip`, and non-interactive `sudo`. If missing, the process exits immediately with actionable instructions.
2. **Tier 0 (Identity)**: `.bootstrap-identity.sh` securely downloads and verifies the `op` (1Password CLI) binary using SHA-256 integrity checks.
3. **Tier 1 (System Provisioning)**: Phase 10 scripts inject OS-level dependencies via `Brewfile` (macOS) or abstracted `apt/dnf/pacman` (Linux).
4. **Tier 2 (Runtime Convergence)**: Phase 20 scripts provision language runtimes and Neovim providers via absolute paths using `mise`.
5. **Tier 3 (Trust Aggregation)**: Phase 50/51 scripts dynamically extract public keys from 1Password and generate the Git allowed_signers list.

## 3. Security & Identity Architecture

### Zero-Knowledge Secrets

Secrets and private keys are never written to disk. The system leverages the **1Password SSH Agent** for all cryptographic operations.

### Dynamic Identity Resolution

The platform automates a single personal identity while leaving work or transient identities to deterministic manual overrides.

1. **Identity Resolution**: `chezmoi` scans 1Password for a single item tagged `dotfiles-github-profile` to resolve Git author variables and the `dotfiles_link_id` (a pointer to the primary SSH key).
2. **Resource Resolution**: `chezmoi` discovers all items tagged `dotfiles-ssh-key` and constructs collision-free public key files.
3. **Deterministic Linkage**: The platform maps the `dotfiles_link_id` to the corresponding SSH Key to finalize the Git signing payload.

### SSH Signing with GPG-Binary Stubbing

To maintain strict binary hermeticity (zero GPG dependency) while co-existing with the broader GitHub ecosystem, the platform defines a clear protocol boundary:

- **Self-Signing (Internal Trust)**: Exclusively enforced via the SSH protocol for all local commits.
- **Foreign Verification (External Trust)**: GitHub's PGP signatures are gracefully ignored by pointing `gpg.program` to the OS-native `/usr/bin/true` binary. This prevents execution crashes without polluting the system with GPG tooling.

## 4. Directory-Driven Routing (Policy Layer)

The platform enforces context awareness using Git's `includeIf`.

- **Managed Context (Safe Zone)**: Repositories under `~/src/github.com/<gh_user>` automatically assume the Personal Sovereign Identity.
- **Unmanaged Context (The Escape Hatch)**: Work or external projects require a manual `.gitconfig.local` to bind company emails and secondary SSH keys, guaranteeing zero cross-contamination.

## 5. Filesystem Standards (XDG Compliance)

The environment strictly adheres to the **XDG Base Directory Specification**:

- **Config**: `~/.config`
- **Data**: `~/.local/share`
- **State**: `~/.local/state`
- **Cache**: `~/.cache`

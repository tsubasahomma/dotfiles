# Engineering Specification

This document defines the architectural constraints and technical logic of the Deterministic Infrastructure Engine. It serves as the single source of truth (SSOT) for the platform's internal mechanics.

## 1. Design Philosophy

The system is designed to enforce state convergence: Given a Minimal Prepared OS and a 1Password session, the output must be mathematically identical across executions.

- **Deterministic State**: System state is driven by declarative schemas (`.chezmoidata/`) rather than imperative scripts.
- **Zero-Speculation Identity**: Personal data is never stored in the repository. Identities are resolved dynamically at runtime.
- **Hermetic Isolation**: Global system pollution is minimized by encapsulating runtimes within isolated environments managed by `mise`.

## 2. Tiered Bootstrapping Lifecycle

Execution follows a strict sequential phase-gate model to resolve binary dependencies without interactive hanging.

1. **Tier -1 (Assertion Gate)**: `.bootstrap-identity.sh` strictly validates the minimal POSIX dependencies (e.g., `curl`). If missing, the process exits immediately with actionable instructions.
2. **Tier 0 (Hermetic Toolchain)**: Natively managed by `.mise.toml`. `chezmoi` utilizes the `read-source-state.pre` hook via `.bootstrap-identity.sh` to silently ensure `mise` is installed and the core toolchain (`chezmoi`, `op`) is converged prior to state compilation.
3. **Tier 1 (System Provisioning)**: Phase 10 scripts inject OS-level dependencies via `Brewfile` (macOS) or abstracted `apt/dnf/pacman` (Linux).
4. **Tier 2 (Runtime Convergence)**: Phase 20 scripts provision language runtimes and Neovim providers via absolute paths using `mise`.
5. **Tier 3 (Trust Aggregation)**: Phase 50+ scripts dynamically extract public keys from 1Password (in-memory) and generate the Git `allowed_signers` list.

## 3. Parallel Identity Architecture (v3)

The platform eliminates the concept of a "Primary" identity in favor of a zero-trust, parallel model. All identities (Personal, Work, OSS) are treated as equal siblings.

1. **Discovery**: `chezmoi` scans all 1Password accounts for items tagged `dotfiles-ssh-key`.
2. **Schema Binding**: Each item must contain a `dotfiles` section with `dotfiles_git_name`, `dotfiles_git_email`, and `dotfiles_git_dirs`.
3. **Atomic Export**: SSH public keys are exported using deterministic naming: `id_{key_type}_{vault_id}_{item_id}.pub`.

## 4. Directory-Driven Routing (Policy Layer)

The platform enforces context awareness using Git's `includeIf`.

- **Zero-Trust Enforcement**: No global `user.email` is defined. Git operations outside of explicitly mapped directories will fail to prevent identity leakage.
- **Dynamic Scoping**: Each identity provides a comma-separated list of directory globs. The engine generates scoped `.gitconfig` files that bind the specific email and SSH signing key to those paths.

## 5. Filesystem Standards (XDG Compliance)

The environment strictly adheres to the **XDG Base Directory Specification**:

- **Config**: `~/.config`
- **Data**: `~/.local/share`
- **State**: `~/.local/state`
- **Cache**: `~/.cache`

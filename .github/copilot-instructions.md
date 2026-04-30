# GitHub Copilot instructions

Use [AGENTS.md](../AGENTS.md) as the primary repository-wide guidance for this
repository.

This is a chezmoi-managed dotfiles source-state repository. Keep suggestions
small, scoped, and behavior-preserving.

Do not change provisioning, identity routing, SSH signing, SSH agent bridging,
generated identity files, Neovim, WezTerm, zsh, Git, mise, Homebrew, GitHub
Actions, runtime versions, tool versions, dependencies, or lockfiles unless the
assigned issue explicitly requires it.

Treat Repomix snapshots as read-only evidence. Do not edit generated
`repomix-*.xml` files.

Prefer repository-relative links only when the target exists in the current
repository state.

# Repomix instruction router

This file provides instruction routing for LLMs consuming Repomix snapshots of
this repository.

Use [AGENTS.md](./AGENTS.md) as the primary repository-wide guidance.

Use [docs/llm/README.md](./docs/llm/README.md) and
[docs/workflows/README.md](./docs/workflows/README.md) for detailed LLM
collaboration and workflow guidance. Use
[docs/llm/comment-guidelines.md](./docs/llm/comment-guidelines.md) when reviewing
or changing comments and references.

This repository is a chezmoi-managed dotfiles source-state repository. Preserve
existing provisioning, identity, editor, shell, Git, mise, Homebrew, and GitHub
Actions behavior unless the assigned issue explicitly scopes a change.

Treat Repomix output as read-only context. Do not edit generated
`repomix-*.xml` snapshots. Make changes to the original repository files.

Use packed files to identify repository structure and current file contents, but
prefer fresh user-provided local evidence when it conflicts with a snapshot.

Do not import assumptions from reference repositories. In particular, do not copy
Nx, OpenTofu, HubSpot, deployment, package-workspace, or monorepo-specific
patterns into this dotfiles repository unless local repository evidence and the
assigned issue explicitly require them.

Do not claim validation passed unless command output, CI evidence, or explicit
user confirmation is available.

# Repomix instruction router

This file provides instruction routing for LLMs consuming Repomix snapshots of
this repository.

Use [AGENTS.md](../../../AGENTS.md) as the root context manifest.

Use [docs/context/README.md](../README.md) as the durable context architecture
entry point:

- [core guidance](../core/README.md) for reusable evidence, output, review, and
  scope-control rules;
- [local guidance](../local/README.md) for dotfiles-specific repository
  boundaries;
- [local surface capsules](../local/surfaces/README.md) for behavior-sensitive
  surface routing;
- [local workflow guidance](../local/workflows/README.md) for issue, PR,
  validation, merge, closure, Commander, and Worker procedures.

This repository is a chezmoi-managed dotfiles source-state repository. Preserve
existing provisioning, identity, editor, shell, Git, mise, Homebrew, and GitHub
Actions behavior unless the assigned issue explicitly scopes a change.

Treat Repomix output as read-only context. Do not edit generated snapshots or
packed output. Make changes to the original repository files.

Use packed files to identify repository structure and current file contents, but
prefer fresh user-provided local evidence when it conflicts with a snapshot.

Do not import assumptions from reference repositories. In particular, do not copy
Nx, OpenTofu, HubSpot, deployment, package-workspace, or monorepo-specific
patterns into this dotfiles repository unless local repository evidence and the
assigned issue explicitly require them.

Do not claim validation passed unless command output, CI evidence, inspected
state, or explicit maintainer confirmation is available.

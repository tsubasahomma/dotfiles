# Local context guidance

## Purpose

This directory is the dotfiles repository-specific extension layer for the
context architecture.

Use it for repository identity, source-state rules, behavior boundaries, local
terms, validation routing, surface routing, and relationships between root
routers, adapters, source state, and Repomix context.

Use the shared operating contracts for reusable assistant rules:
[`../kernel.md`](../kernel.md) for evidence, scope, review, validation, and
generated artifact discipline; [`../protocols.md`](../protocols.md) for output
format selection; and [`../evals.md`](../evals.md) for regression cases.

## Local documents

- [Local repository profile](./profile.md): repository identity, source-state
  model, supported host posture, and current documentation entry points.
- [Local behavior boundaries](./boundaries.md): behavior-sensitive repository
  surfaces that must not change unless the active issue scopes them.
- [Local glossary](./glossary.md): repository-specific terms used by context,
  workflow, and surface guidance.
- [Local validation map](./validation.md): validation routing by touched
  repository surface.
- [Local surface registry](./surface-registry.md): current capsule routing and
  failure-prevention focus for local surfaces.
- [Local context routing](./routing.md): relationships between shared operating
  contracts, local guidance, root routers, adapters, source state, and Repomix
  context.
- [Local workflow routing](./workflows/README.md): issue, PR, validation, merge,
  closure, Commander, and Worker procedures.

## Local surface capsules

[Local surface capsules](./surfaces/README.md) provide compact
failure-prevention routing for behavior-sensitive surfaces:

- [Chezmoi](./surfaces/chezmoi.md)
- [Mise](./surfaces/mise.md)
- [WSL2](./surfaces/wsl2.md)
- [Identity](./surfaces/identity.md)
- [Neovim](./surfaces/neovim.md)
- [GitHub Actions](./surfaces/github-actions.md)

## Local workflow guidance

[Local workflow guidance](./workflows/README.md) provides concise procedures for
scoped issue handling, Commander and Worker coordination, pull requests,
validation reporting, merge decisions, and issue closure.

Workflow guidance should route reusable evidence, output, and review rules to
the shared operating contracts, and route behavior-sensitive validation to the
local validation map and surface capsules.

## Active context boundary

Use current context documents, source-state files, rendered-output inspection,
command output, and CI evidence that match the touched surface. Historical or
removed documentation surfaces are provenance, not active routing targets.

Do not copy reusable operating rules into this local layer. Link to
[`../kernel.md`](../kernel.md), [`../protocols.md`](../protocols.md), or
[`../evals.md`](../evals.md) instead, and keep dotfiles-specific assumptions
here.

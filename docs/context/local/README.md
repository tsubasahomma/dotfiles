# Local context guidance

## Purpose

This directory is the dotfiles repository-specific extension layer for the
context architecture.

Use it for repository identity, source-state rules, behavior boundaries, local
terms, validation routing, surface routing, and relationships between root
routers, adapters, and legacy documentation inputs.

Use [Core context guidance](../core/README.md) for reusable assistant rules such
as evidence discipline, output format selection, review classification,
validation evidence, generated artifacts, drift control, and out-of-scope
findings.

## Local documents

- [Local repository profile](./profile.md): repository identity, source-state
  model, supported host posture, and current documentation entry points.
- [Local behavior boundaries](./boundaries.md): behavior-sensitive repository
  surfaces that must not change unless the active issue scopes them.
- [Local glossary](./glossary.md): repository-specific terms used by context,
  workflow, and surface guidance.
- [Local validation map](./validation.md): validation routing by touched
  repository surface.
- [Local surface registry](./surface-registry.md): current capsule routing,
  migration evidence, and failure-prevention focus for local surfaces.
- [Local context routing](./routing.md): relationships between core guidance,
  local guidance, root routers, adapters, legacy inputs, and Repomix context.
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
`docs/context/core/**`, and route behavior-sensitive validation to the local
validation map and surface capsules.

## Migration boundary

Existing `docs/llm/**`, `docs/workflows/**`, and `docs/chezmoi/**` documents
remain migration inputs until later scoped issues distill, replace, or remove
their durable guidance.

Do not copy reusable core rules into this local layer. Link to
`docs/context/core/**` instead, and keep dotfiles-specific assumptions here.

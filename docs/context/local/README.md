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
- [Local surface registry](./surface-registry.md): future capsule candidates,
  migration evidence, and failure-prevention focus for local surfaces.
- [Local context routing](./routing.md): relationships between core guidance,
  local guidance, root routers, adapters, legacy inputs, and Repomix context.

## Deferred local areas

- [Local surface routing](./surfaces/README.md) remains the future home for
  compact surface capsules. This issue adds only a registry and routing pointer.
- [Local workflow routing](./workflows/README.md) remains the future home for
  issue, pull request, validation, merge, and closure procedures. This issue
  adds only routing guidance.

## Migration boundary

Existing `docs/llm/**`, `docs/workflows/**`, and `docs/chezmoi/**` documents
remain migration inputs until later scoped issues distill, replace, or remove
their durable guidance.

Do not copy reusable core rules into this local layer. Link to
`docs/context/core/**` instead, and keep dotfiles-specific assumptions here.

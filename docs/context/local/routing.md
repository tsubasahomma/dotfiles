# Local context routing

## Purpose

Use this routing map to choose the correct local context entry point without
turning root routers, adapters, retired documentation, or generated artifacts
into architectural anchors.

## Routing order

For dotfiles repository work, route context in this order:

1. Start with the active user request, issue, pull request, review, or validation
   evidence.
2. Use [Context architecture](../README.md) to identify the target context layer.
3. Use [Core context guidance](../core/README.md) for reusable assistant rules.
4. Use this local layer for repository-specific identity, behavior boundaries,
   local validation routing, surface routing, and workflow procedures.
5. Use current source-state files and validation evidence for detailed behavior
   claims.

## Root and adapter relationship

[AGENTS.md](../../../AGENTS.md) is the root context manifest. It should stay
concise and route detailed rules to `docs/context/**`.

[`.github/copilot-instructions.md`](../../../.github/copilot-instructions.md) is
the GitHub Copilot adapter. It should stay vendor-specific and secondary to the
language-model-agnostic context architecture.

Do not add `.github/instructions/**` unless a later issue explicitly scopes that
adapter.

## Current documentation relationship

| Surface | Current relationship |
| --- | --- |
| [README.md](../../../README.md) | First-run and operator-facing bootstrap entry point. |
| [ARCHITECTURE.md](../../../ARCHITECTURE.md) | High-level architecture and teardown overview that routes to current context surfaces. |
| [Core context guidance](../core/README.md) | Reusable assistant rules. |
| [Local context guidance](./README.md) | Dotfiles-specific extension layer. |
| [Local surface capsules](./surfaces/README.md) | Behavior-sensitive surface routing. |
| [Local workflow guidance](./workflows/README.md) | Issue, PR, validation, merge, closure, Commander, and Worker procedures. |
| [Repomix context routing](../repomix/README.md) | Tracked Repomix consumption guidance. |

Removed documentation surfaces should not be used as active context anchors.
Do not restore former `docs/llm/**`, `docs/workflows/**`, or `docs/chezmoi/**`
paths as context anchors. If a future issue needs detailed behavior evidence,
inspect current source state, rendered output, command output, or CI evidence
that matches the touched surface.

## Repomix relationship

Tracked Repomix guidance lives under [`docs/context/repomix/**`](../repomix/README.md).
Generated Repomix output lives under `.context/repomix/**` and remains read-only
evidence.

Use fresh local command output, diffs, or maintainer-provided evidence over a
stale generated snapshot when they conflict.

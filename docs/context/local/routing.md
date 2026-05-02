# Local context routing

## Purpose

Use this routing map to choose the correct local context entry point without
turning root routers, adapters, or legacy documentation into permanent
architecture anchors.

## Routing order

For dotfiles repository work, route context in this order:

1. Start with the active user request, issue, pull request, review, or validation
   evidence.
2. Use [Context architecture](../README.md) to identify the target context layer.
3. Use [Core context guidance](../core/README.md) for reusable assistant rules.
4. Use this local layer for repository-specific identity, behavior boundaries,
   local validation routing, surface routing, and workflow procedures.
5. Use legacy `docs/llm/**`, `docs/workflows/**`, and `docs/chezmoi/**`
   documents as migration evidence until later scoped issues replace or remove
   them.

## Root and adapter relationship

`AGENTS.md` is the current repository-wide assistant guidance and future root
context manifest input. Do not convert it into the final root context manifest
unless a later issue explicitly scopes that work.

`.github/copilot-instructions.md` is the current GitHub Copilot adapter input.
Do not thin it or add `.github/instructions/**` unless a later issue explicitly
scopes adapter work.

Adapters should remain secondary to the language-model-agnostic context
architecture. Do not make Copilot-specific structure the primary architecture.

## Legacy documentation relationship

Legacy documentation surfaces remain useful until their durable guidance is
migrated or intentionally discarded:

| Legacy surface | Current relationship |
| --- | --- |
| `docs/llm/**` | Migration input for reusable core rules, local repository rules, and later workflow/root-adapter cleanup. |
| `docs/workflows/**` | Migration input for local workflow procedures now distilled under `docs/context/local/workflows/**`; keep as legacy input until later cleanup. |
| `docs/chezmoi/**` | Migration evidence for future compact surface capsules and behavior-sensitive local constraints. |
| `README.md` | Current first-run and operator-facing entry point. |
| `ARCHITECTURE.md` | Legacy high-level architecture and teardown routing input. |

Do not delete, archive, or rewrite these surfaces merely because a local context
summary exists. Later issues should remove obsolete surfaces only after durable
requirements have been migrated or intentionally discarded.

## Repomix relationship

Tracked Repomix guidance lives under [`docs/context/repomix/**`](../repomix/README.md).
Generated Repomix output lives under `.context/repomix/**` and remains read-only
evidence.

Use fresh local command output, diffs, or maintainer-provided evidence over a
stale generated snapshot when they conflict.

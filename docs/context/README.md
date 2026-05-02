# Context architecture

## Purpose

This directory is the durable architecture entry point for language-model-agnostic
repository context.

It defines the organization for reusable context guidance, dotfiles-specific
extensions, surface capsules, workflow guidance, and Repomix context while
leaving existing documentation, root routers, and repository behavior unchanged.

Use [Context migration map](./migration-map.md) to compare future child issues
against the current migration plan.

## Architecture layers

| Target path | Responsibility |
| --- | --- |
| `docs/context/core/**` | Reusable context guidance that can move to another repository with minimal edits. |
| `docs/context/local/**` | Dotfiles-specific extension layer that records local repository identity, boundaries, glossary, validation routing, and surface registry. |
| `docs/context/local/surfaces/**` | Compact local surface capsules that prevent predictable assistant mistakes and route reviewers to the right local evidence. |
| `docs/context/local/workflows/**` | Local issue, pull request, validation, merge, and closure workflow guidance aligned with this architecture. |
| `docs/context/repomix/**` | Tracked guidance for consuming Repomix context artifacts and keeping generated context separate from source documentation. |
| `.context/repomix/**` | Future generated Repomix output storage. Generated artifacts in this path remain read-only evidence, not editable source. |

## Separation contract

Reusable core guidance must avoid dotfiles-specific, chezmoi-specific,
workstation-specific, and operator-specific assumptions.

Repository-specific assumptions belong under `docs/context/local/**`.
Surface-specific constraints belong under `docs/context/local/surfaces/**`.
Repomix consumption guidance belongs under `docs/context/repomix/**`.
Generated Repomix output belongs under `.context/repomix/**`.

Root routers such as `AGENTS.md`, `repomix-instruction.md`, and
`.github/copilot-instructions.md` remain current migration inputs until later
issues explicitly change them.

## Migration contract

Current guidance surfaces are migration inputs, not permanent architecture
anchors:

- `AGENTS.md`
- `repomix-instruction.md`
- `.github/copilot-instructions.md`
- `docs/llm/**`
- `docs/workflows/**`
- `docs/chezmoi/**`

Future migration issues should distill durable requirements before moving,
compressing, or deleting any old surface. Prefer preserving constraints,
decision rules, validation requirements, and failure-prevention guidance over
copying full prose.

The issue #185 / PR #186 hardening is a migration requirement. Future work must
preserve the discipline to inspect broadly, patch narrowly, avoid invented local
state, require validation evidence, and record useful out-of-scope findings
without expanding the active patch.

## Non-goals for this contract

This contract excludes:

- performing the full documentation migration
- relocating `repomix-instruction.md`
- moving generated Repomix output to `.context/repomix/**`
- updating `repomix.config.json`
- converting `AGENTS.md` into the final root context manifest
- adding `.github/instructions/**`
- preserving obsolete documentation by archiving it
- changing repository behavior, scripts, tasks, CI semantics, versions,
  dependencies, or lockfiles

## Roadmap use

After each child issue merges, compare the resulting repository state against
this contract and the migration map before creating the next child issue.

The expected next step after this contract is a separately scoped issue for the
`docs/context/**` skeleton and Repomix routing work.

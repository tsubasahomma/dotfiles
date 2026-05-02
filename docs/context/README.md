# Context architecture

## Purpose

This directory is the durable architecture entry point for language-model-agnostic
repository context.

It defines the organization for reusable context guidance, dotfiles-specific
extensions, surface capsules, workflow guidance, and Repomix context while
leaving legacy documentation inputs and repository behavior unchanged.

Use [Context migration map](./migration-map.md) to compare future child issues
against the current migration plan.

## Architecture layers

| Target path | Responsibility |
| --- | --- |
| `docs/context/core/**` | Reusable context guidance for principles, evidence, output, review, validation, generated artifacts, drift control, and out-of-scope findings. |
| `docs/context/local/**` | Dotfiles-specific extension layer that records local repository identity, boundaries, glossary, validation routing, and surface registry. |
| `docs/context/local/surfaces/**` | Compact local surface capsules that prevent predictable assistant mistakes and route reviewers to the right local evidence. |
| `docs/context/local/workflows/**` | Local issue, pull request, validation, merge, and closure workflow guidance aligned with this architecture. |
| `docs/context/repomix/**` | Tracked guidance for consuming Repomix context artifacts and keeping generated context separate from source documentation. |
| `.context/repomix/**` | Generated Repomix output storage. Generated artifacts in this path remain read-only evidence, not editable source. |

## Separation contract

Reusable core guidance must avoid dotfiles-specific, chezmoi-specific,
workstation-specific, and operator-specific assumptions.

Repository-specific assumptions belong under `docs/context/local/**`.
Surface-specific constraints belong under `docs/context/local/surfaces/**`.
Repomix consumption guidance belongs under `docs/context/repomix/**`.
Generated Repomix output belongs under `.context/repomix/**`.

Root routers such as `AGENTS.md` and `.github/copilot-instructions.md` remain
current migration inputs until later issues explicitly change them.

## Migration contract

Current guidance surfaces are migration inputs, not permanent architecture
anchors:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/llm/**`
- `docs/workflows/**`
- `docs/chezmoi/**`

Core reusable guidance now starts at
[docs/context/core/README.md](./core/README.md). The Repomix instruction
router lives at [docs/context/repomix/instructions.md](./repomix/instructions.md).

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
- distilling full repository-specific local guidance
- creating full local surface capsules
- migrating workflow guidance
- converting `AGENTS.md` into the final root context manifest
- adding `.github/instructions/**`
- preserving obsolete documentation by archiving it
- changing repository behavior, scripts, tasks, CI semantics, versions,
  dependencies, or lockfiles

## Roadmap use

After each child issue merges, compare the resulting repository state against
this contract and the migration map before creating the next child issue.

After reusable core guidance is distilled, the expected next step is a
separately scoped issue for distilling repository-specific guidance into
`docs/context/local/**`.

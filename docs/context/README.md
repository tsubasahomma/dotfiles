# Context architecture

## Purpose

This directory is the durable architecture entry point for language-model-agnostic
repository context.

It defines the organization for reusable context guidance, dotfiles-specific
extensions, surface capsules, workflow guidance, and Repomix context while
keeping repository behavior unchanged.

Use [Context migration map](./migration-map.md) to review how the former legacy
surfaces were retired and where their durable guidance now lives.

## Architecture layers

| Target path | Responsibility |
| --- | --- |
| `AGENTS.md` | Concise root context manifest for repository identity, evidence hierarchy, safety boundaries, generated artifact discipline, patch discipline, validation discipline, and scope control. |
| `.github/copilot-instructions.md` | Thin GitHub Copilot adapter that routes to the shared context architecture. |
| `docs/context/core/**` | Reusable context guidance for principles, evidence, output, review, validation, generated artifacts, drift control, and out-of-scope findings. |
| `docs/context/local/**` | Dotfiles-specific extension layer that records local repository identity, boundaries, glossary, validation routing, and surface registry. |
| `docs/context/local/surfaces/**` | Compact local surface capsules that prevent predictable assistant mistakes and route reviewers to current local evidence. |
| `docs/context/local/workflows/**` | Local issue, pull request, validation, merge, closure, Commander, and Worker workflow guidance aligned with this architecture. |
| `docs/context/repomix/**` | Tracked guidance for consuming Repomix context artifacts and keeping generated context separate from source documentation. |
| `.context/repomix/**` | Generated Repomix output storage. Generated artifacts in this path remain read-only evidence, not editable source. |

## Separation contract

Reusable core guidance must avoid dotfiles-specific, chezmoi-specific,
workstation-specific, and operator-specific assumptions.

Repository-specific assumptions belong under `docs/context/local/**`.
Surface-specific constraints belong under `docs/context/local/surfaces/**`.
Workflow procedures belong under `docs/context/local/workflows/**`.
Repomix consumption guidance belongs under `docs/context/repomix/**`.
Generated Repomix output belongs under `.context/repomix/**`.

Vendor-specific adapters should route to this shared architecture instead of
becoming the primary architecture.

## Retired legacy surfaces

The former assistant, workflow, and long-form chezmoi documentation surfaces were
migration inputs. Their durable guidance has been distilled into the current
context architecture or intentionally discarded as obsolete duplicate audit
material.

Use these current entry points instead:

- [AGENTS.md](../../AGENTS.md) for the root context manifest.
- [Core context guidance](./core/README.md) for reusable assistant rules.
- [Local context guidance](./local/README.md) for repository-specific rules.
- [Local surface capsules](./local/surfaces/README.md) for behavior-sensitive
  surface routing.
- [Local workflow guidance](./local/workflows/README.md) for issue, PR,
  validation, merge, closure, Commander, and Worker procedures.
- [Repomix instruction router](./repomix/instructions.md) for packed snapshot
  consumers.

The issue #185 / PR #186 hardening remains preserved by the current architecture:
inspect broadly, patch narrowly, avoid invented local state, require validation
evidence, treat generated artifacts as read-only evidence, and record useful
out-of-scope findings without expanding the active patch.

## Non-goals for this architecture

This architecture does not authorize:

- changing repository behavior, scripts, tasks, CI semantics, versions,
  dependencies, or lockfiles;
- hand-editing generated context artifacts;
- archiving obsolete documentation merely to avoid deletion;
- making a vendor-specific adapter the primary context architecture.

## Roadmap use

After each child issue merges, compare the resulting repository state against
this architecture and the migration map before creating or closing follow-up
work.

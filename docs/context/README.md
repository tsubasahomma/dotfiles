# Context architecture

## Purpose

This directory is the active architecture entry point for
language-model-agnostic repository context.

It organizes reusable context guidance, dotfiles-specific extensions, surface
capsules, workflow guidance, and Repomix context while keeping repository
behavior unchanged.

Use this document to choose the current context layer for a task. Use historical
issue or PR ledgers only when the active task names them or when provenance is
needed for review; completed planning artifacts are not day-to-day routing
inputs.

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

## Active context contract

Start active work from current evidence:

- the active user request, issue, pull request, review, or validation output;
- current source-state files, diffs, rendered output, command output, or CI
  evidence;
- the focused context layer that matches the touched surface.

Do not route daily work through completed planning or handoff artifacts.
Historical issues and PRs are useful provenance, but they should not override
current repository evidence or current context guidance.

Preserve the active safety discipline: inspect broadly enough to avoid local
mistakes, patch only the assigned scope, avoid invented local state, require
validation evidence, treat generated artifacts as read-only evidence, and record
useful out-of-scope findings without expanding the active patch.

## Non-goals for this architecture

This architecture does not authorize:

- changing repository behavior, scripts, tasks, CI semantics, versions,
  dependencies, or lockfiles;
- hand-editing generated context artifacts;
- archiving obsolete documentation merely to avoid deletion;
- making a vendor-specific adapter the primary context architecture;
- preserving completed project history as active assistant context.

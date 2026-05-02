# Context migration map

## Purpose

This map shows how future child issues should distill current guidance surfaces
into the target context architecture.

This map is a planning contract for future child issues. It does not authorize
broad file moves, deletion, archival, root router rewrites, additional Repomix
routing changes, or behavior changes beyond the active child issue scope.

## Current surface classification

| Source or legacy surface | Classification | Target treatment | Current status |
| --- | --- | --- | --- |
| `AGENTS.md` | Root guidance input. | Distill later into a concise root context manifest that points to `docs/context/README.md`. | Remains unchanged through issue #198. |
| `repomix-instruction.md` | Former root Repomix instruction input. | Relocated under `docs/context/repomix/**`; keep generated output under `.context/repomix/**`. | Moved to `docs/context/repomix/instructions.md` in issue #190. |
| `.github/copilot-instructions.md` | Vendor-specific adapter input. | Thin later into an adapter that points to the language-model-agnostic context architecture. Keep Copilot-specific guidance out of the primary architecture. | Remains unchanged through issue #198. |
| `docs/llm/**` | Reusable assistant guidance and local failure-prevention input. | Distill repository-agnostic rules into `docs/context/core/**`, dotfiles-specific rules into `docs/context/local/**`, surface-specific rules into `docs/context/local/surfaces/**`, and workflow-adjacent rules into `docs/context/local/workflows/**`. | Reusable core rules were distilled in issue #192, local repository guidance was distilled in issue #194, local surface capsules were distilled in issue #196, and workflow-adjacent procedure rules were distilled in issue #198. The legacy surface remains a migration input until later root-router and cleanup work completes. |
| `docs/workflows/**` | Local workflow guidance input. | Distill issue, PR, validation, merge, closure, Commander, and Worker rules into `docs/context/local/workflows/**`. | Local workflow procedures were distilled in issue #198. The legacy surface remains a migration input until later cleanup confirms its durable guidance has been migrated or intentionally discarded. |
| `docs/chezmoi/**` | Local surface evidence input. | Compress durable chezmoi, mise, WSL2, Neovim, identity, and GitHub Actions constraints into `docs/context/local/surfaces/**`. | Compact surface capsules were created in issue #196. The legacy surface remains migration evidence until later cleanup confirms its durable guidance has been migrated or intentionally discarded. |

## Target area map

| Target area | Accepts | Rejects |
| --- | --- | --- |
| `docs/context/core/**` | Repository-agnostic context principles, evidence discipline, routing, output selection, review classification, validation evidence, and drift control. | Dotfiles-specific, chezmoi-specific, workstation-specific, operator-specific, or issue-specific assumptions. |
| `docs/context/local/**` | Dotfiles repository profile, behavior boundaries, local glossary, validation map, surface registry, and local routing. | Reusable guidance that should live in `docs/context/core/**`. |
| `docs/context/local/surfaces/**` | Compact capsules for behavior-sensitive local surfaces such as chezmoi, mise, WSL2, Neovim, identity, and GitHub Actions. | Full domain manuals or copied legacy docs. |
| `docs/context/local/workflows/**` | Local workflow rules for issues, pull requests, validation, merge, closure, Commander coordination, and Worker coordination. | Generic assistant guidance that should live in `docs/context/core/**`. |
| `docs/context/repomix/**` | Tracked guidance for generating, consuming, validating, and routing Repomix context. | Generated Repomix output. |
| `.context/repomix/**` | Generated Repomix context artifacts. | Hand-edited source documentation. |

## Migration requirements

Future child issues must preserve these requirements while distilling old
surfaces:

- Treat local repository state as unknown unless current evidence provides it.
- Treat generated Repomix output as read-only evidence, not editable source.
- Inspect enough context to avoid local mistakes, but patch only the assigned
  scope.
- Preserve issue #185 / PR #186 review, inspection, validation, and output
  hardening.
- Claim validation passed only with command output, CI evidence, or explicit
  maintainer confirmation.
- Record useful out-of-scope findings without implementing them in the active
  issue.
- Prefer distillation over wholesale copying.
- Prefer deletion over archival only after a later scoped issue migrates or
  intentionally discards durable content.
- Keep child issues independently reviewable.

## Distillation rules

When migrating an old surface, classify each paragraph before moving it:

1. Reusable context rule: move or rewrite under `docs/context/core/**`.
2. Dotfiles-local rule: move or rewrite under `docs/context/local/**`.
3. Surface-specific constraint: compress into a capsule under
   `docs/context/local/surfaces/**`.
4. Local workflow rule: move or rewrite under `docs/context/local/workflows/**`.
5. Repomix consumption rule: move or rewrite under `docs/context/repomix/**`.
6. Generated artifact or stale historical detail: skip copying it; discard it
   only when a scoped issue confirms no durable requirement remains.
7. Vendor adapter detail: keep only in the relevant adapter surface, with the
   language-model-agnostic context architecture as the primary target.

Old file boundaries are not durable requirements. Preserve durable requirements,
routing decisions, validation expectations, and failure-prevention rules.

## Future child issue checkpoints

After each child issue merges, compare the repository against this map:

- Did the change keep reusable core guidance separate from local extensions?
- Did it avoid turning surface capsules into long domain manuals?
- Did it preserve issue #185 / PR #186 hardening?
- Did it avoid broad file moves or deletion unless explicitly scoped?
- Did it avoid behavior, script, task, CI, version, dependency, and lockfile
  changes?
- Did it keep generated artifacts separate from tracked source documentation?
- Did it update or validate Markdown links when links changed?
- Did it report out-of-scope findings instead of mixing them into the patch?

## Next handoff

After local workflow guidance is distilled, the next child issue can use this
map to scope root router and obsolete surface cleanup. That later issue should
compare the post-merge repository state against the parent issue before changing
`AGENTS.md`, `.github/copilot-instructions.md`, `docs/llm/**`,
`docs/workflows/**`, or `docs/chezmoi/**`.

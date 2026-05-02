# Context migration map

## Purpose

This map records how the former assistant, workflow, and long-form domain
guidance surfaces were distilled into the current context architecture.

It is a review ledger, not authorization to change repository behavior, scripts,
tasks, CI semantics, templates, versions, dependencies, lockfiles, or generated
artifacts.

## Current surface classification

| Surface | Current role | Current status |
| --- | --- | --- |
| `AGENTS.md` | Root context manifest. | Active root router for repository identity, evidence hierarchy, safety boundaries, generated artifact discipline, patch discipline, validation discipline, and scope control. |
| `.github/copilot-instructions.md` | GitHub Copilot adapter. | Active vendor-specific adapter that routes to `AGENTS.md` and the shared context architecture. |
| `docs/context/core/**` | Reusable context guidance. | Active home for repository-agnostic principles, evidence discipline, output discipline, review discipline, validation evidence, generated artifact discipline, drift control, and out-of-scope finding rules. |
| `docs/context/local/**` | Dotfiles-specific extension layer. | Active home for repository profile, behavior boundaries, glossary, validation map, surface registry, and local routing. |
| `docs/context/local/surfaces/**` | Compact surface capsules. | Active home for behavior-sensitive failure-prevention guidance for chezmoi, mise, WSL2, identity, Neovim, and GitHub Actions. |
| `docs/context/local/workflows/**` | Local workflow guidance. | Active home for issue, PR, validation, merge, closure, Commander, and Worker procedures. |
| `docs/context/repomix/**` | Tracked Repomix consumption guidance. | Active home for Repomix instruction routing. |
| `.context/repomix/**` | Generated Repomix artifact storage. | Generated read-only evidence, not tracked source documentation. |

## Retired surface audit

| Retired surface | Durable content found | Disposition |
| --- | --- | --- |
| `docs/llm/**` | Evidence discipline, routing, strict patch output, review classification, validation evidence, comment hygiene, commit message rules, and chezmoi template caution. | Reusable rules were distilled into `docs/context/core/**`; dotfiles-specific boundaries were distilled into `docs/context/local/**` and `docs/context/local/surfaces/**`; workflow-adjacent rules were distilled into `docs/context/local/workflows/**`. Comment hygiene and commit message rules are represented in current review, chezmoi, and PR workflow guidance. The old surface is deleted instead of archived. |
| `docs/workflows/**` | Scoped issue handling, PR body expectations, validation reporting, merge and closure decisions, linked issue wording, and Commander/Worker coordination. | Durable procedures were distilled into `docs/context/local/workflows/**`. The old surface is deleted instead of archived. |
| `docs/chezmoi/**` | Detailed long-form audits for chezmoi action graph, script contracts, trigger behavior, bootstrap and identity, data contracts, mise task boundaries, WSL2 validation, and future task taxonomy. | Durable failure-prevention constraints were compressed into `docs/context/local/surfaces/**`, `docs/context/local/boundaries.md`, and `docs/context/local/validation.md`. Long-form inventory and historical audit prose was intentionally discarded as obsolete migration evidence. The old surface is deleted instead of archived. |
| `repomix-instruction.md` | Former root Repomix instruction router. | Relocated to `docs/context/repomix/instructions.md` in issue #190. Root path remains retired. |

## Target area map

| Target area | Accepts | Rejects |
| --- | --- | --- |
| `docs/context/core/**` | Repository-agnostic context principles, evidence discipline, routing, output selection, review classification, validation evidence, generated artifact handling, and drift control. | Dotfiles-specific, chezmoi-specific, workstation-specific, operator-specific, or issue-specific assumptions. |
| `docs/context/local/**` | Dotfiles repository profile, behavior boundaries, local glossary, validation map, surface registry, and local routing. | Reusable guidance that should live in `docs/context/core/**`. |
| `docs/context/local/surfaces/**` | Compact capsules for behavior-sensitive local surfaces such as chezmoi, mise, WSL2, Neovim, identity, and GitHub Actions. | Full domain manuals, copied legacy docs, and workflow procedures. |
| `docs/context/local/workflows/**` | Local workflow rules for issues, pull requests, validation, merge, closure, Commander coordination, and Worker coordination. | Generic assistant guidance that should live in `docs/context/core/**` and surface constraints that should live in capsules. |
| `docs/context/repomix/**` | Tracked guidance for generating, consuming, validating, and routing Repomix context. | Generated Repomix output. |
| `.context/repomix/**` | Generated Repomix context artifacts. | Hand-edited source documentation. |

## Migration requirements preserved

The current architecture preserves these requirements:

- inspect broadly enough to avoid local mistakes;
- patch narrowly within the assigned scope;
- use current file contents and current evidence before writing targeted
  patches;
- keep reusable guidance separate from local extensions;
- keep local surface capsules compact and failure-prevention oriented;
- keep workflow procedures under local workflow guidance;
- report validation as evidence, not expectation;
- treat generated Repomix output as read-only evidence;
- preserve useful out-of-scope findings without implementing them in the active
  patch;
- avoid behavior, script, task, CI, version, dependency, lockfile, template, and
  generated-artifact changes unless explicitly scoped.

## Cleanup review checklist

Use this checklist when reviewing future context changes:

- Does the change route through `AGENTS.md` and `docs/context/README.md`?
- Does it keep vendor-specific adapters secondary to the shared architecture?
- Does it keep reusable core guidance separate from local extensions?
- Does it avoid turning surface capsules into long domain manuals?
- Does it preserve issue #185 / PR #186 hardening?
- Does it avoid broad deletion unless explicitly scoped?
- Does it avoid behavior, script, task, CI, template, version, dependency, and
  lockfile changes?
- Does it keep generated artifacts separate from tracked source documentation?
- Does it update or validate Markdown links when links change?
- Does it report out-of-scope findings instead of mixing them into the patch?

## Next handoff

After the cleanup issue merges, the Commander Thread should compare the result
against parent issue #187 and this map before recommending whether the parent
issue can close.

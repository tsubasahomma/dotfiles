# Local validation map

## Purpose

Use this map to choose validation that matches the dotfiles repository surface
touched by a change.

This file routes local validation decisions. It does not replace the detailed
legacy [Validation workflow](../../workflows/validation-workflow.md), and it does
not make validation claims without evidence.

## Baseline documentation validation

For documentation-only context changes, use evidence from:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `pre-commit run --all-files`
- Markdown relative link validation, when repository-relative Markdown links are
  added, removed, or changed
- `repomix`, when context routing, LLM guidance, workflow guidance, Repomix
  guidance, or generated snapshot routing changes
- GitHub Actions CI after PR creation, when required by branch protection or
  reviewer request

Do not mark any check complete without command output, CI evidence, inspected
state, or explicit maintainer confirmation.

## Surface map

| Touched surface | Validation routing |
| --- | --- |
| `docs/context/**` | Use baseline documentation validation. Run Markdown link validation when links change. Run `repomix` because context routing affects generated LLM evidence. |
| `AGENTS.md` or `.github/copilot-instructions.md` | Use baseline documentation validation, Markdown link validation, and `repomix`; these files affect assistant routing. |
| `docs/llm/**` or `docs/workflows/**` | Use baseline documentation validation, Markdown link validation when links change, and `repomix`; these remain migration inputs until later issues replace them. |
| `README.md` or `ARCHITECTURE.md` | Use baseline documentation validation, Markdown link validation when links change, and `repomix` when assistant or context routing changes. Add behavior validation only if the edit changes documented operator commands or behavior claims. |
| `docs/chezmoi/**` only | Use baseline documentation validation and Markdown link validation when links change. Add rendered-output or task validation only if the active issue changes source-state behavior or current behavior claims. |
| `.chezmoiignore.tmpl`, `.chezmoi.toml.tmpl`, `.chezmoiscripts/**`, `.chezmoitemplates/**`, or rendered configuration templates | Use rendered-output inspection such as `chezmoi diff` or `chezmoi execute-template` in addition to baseline checks. Consider `mise run doctor` only when setup, toolchain, rendered config, task behavior, or health-check behavior changes. |
| `.chezmoidata/**` | Review every template, script, package, completion, or tool consumer affected by the data. Add rendered-output and task validation that matches the changed consumer. |
| `dot_config/mise/tasks/**`, `.mise.toml`, tool declarations, versions, dependencies, or lockfiles | Validate mise task visibility, task behavior, tool resolution, and health checks appropriate to the change. `mise run doctor` is usually relevant when health-check behavior or setup/toolchain behavior changes. |
| `.github/workflows/**` | Use workflow-focused review plus GitHub Actions CI evidence after PR creation. Local checks do not prove remote CI status. |
| `.context/repomix/**` generated XML | Do not edit generated output directly. Regenerate with `repomix` when validation requires fresh evidence. |

## Documentation-only doctor boundary

Do not require `mise run doctor` for a PR that changes only Markdown context or
routing and does not change setup, toolchain, rendered config, task behavior,
health-check behavior, scripts, CI semantics, versions, dependencies, or
lockfiles.

If `mise run doctor` is not run for such a PR, report that it was not run for
that reason rather than marking it complete.

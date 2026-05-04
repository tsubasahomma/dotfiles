# Repository validation

## Purpose

Define the local validation baseline and routing rules for this dotfiles
repository.

Use this file when a task needs repository-specific validation commands,
documentation-only boundaries, surface-specific validation routing, or local CI
interpretation. Use [`../context/kernel.md`](../context/kernel.md) for generic
validation-claim discipline and [`../context/protocols.md`](../context/protocols.md)
for validation report formatting.

## Local validation baseline

For documentation-only context, workflow, schema, template-routing,
assistant-guidance, validation-default, or routing changes, use evidence from:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `pre-commit run --all-files`
- Markdown relative link validation, when repository-relative Markdown links are
  added, removed, or changed
- `repomix`, when context routing, assistant guidance, workflow contracts,
  artifact schemas, template routing, Repomix guidance, or generated snapshot
  routing changes
- GitHub Actions CI after PR creation, when required by branch protection or
  reviewer request, reported separately from local validation

Do not mark any check complete without command output, CI evidence, inspected
state, or explicit maintainer confirmation. Report unrun applicable checks as
`Pending` or `Skipped`, and report inapplicable checks as `Not required` with the
reason.

## Validation routing by touched source

| Touched source | Validation routing |
| --- | --- |
| `docs/context/**` | Use baseline documentation validation. Run Markdown link validation when links change. Run `repomix` because context routing affects generated LLM evidence. |
| `docs/repo/**` | Use baseline documentation validation. Run Markdown link validation when links change. Run `repomix` because repository-local extension routing affects generated LLM evidence. |
| `AGENTS.md` or `.github/copilot-instructions.md` | Use baseline documentation validation, Markdown link validation, and `repomix`; these files affect assistant routing. |
| `README.md` | Use baseline documentation validation, Markdown link validation when links change, and `repomix` when assistant or context routing changes. Add behavior validation only if the edit changes documented operator commands or behavior claims. |
| `.chezmoiignore.tmpl`, `.chezmoi.toml.tmpl`, `.chezmoiscripts/**`, `.chezmoitemplates/**`, or rendered configuration templates | Use rendered-output inspection such as `chezmoi diff` or `chezmoi execute-template` in addition to baseline checks. Consider `mise run doctor` only when setup, toolchain, rendered config, task behavior, or health-check behavior changes. |
| `.chezmoidata/**` | Review every template, script, package, completion, or tool consumer affected by the data. Add rendered-output and task validation that matches the changed consumer. |
| `dot_config/mise/tasks/**`, `.mise.toml`, tool declarations, versions, dependencies, or lockfiles | Validate mise task visibility, task behavior, tool resolution, and health checks appropriate to the change. `mise run doctor` is usually relevant when health-check behavior or setup/toolchain behavior changes. |
| `.github/workflows/**` | Use workflow-focused review plus GitHub Actions CI evidence after PR creation. Local checks do not prove remote CI status. |
| `.github/ISSUE_TEMPLATE/**` or `.github/pull_request_template.md` | Use template-focused review and baseline documentation validation. Do not change these templates from context cleanup or workflow-default work unless explicitly scoped. |
| `.context/repomix/**` generated XML | Do not edit generated output directly. Regenerate with `repomix` when validation requires fresh evidence. |

## Documentation-only doctor boundary

Do not require `mise run doctor` for a PR that changes only Markdown context or
routing and does not change setup, toolchain, rendered config, task behavior,
health-check behavior, scripts, CI semantics, versions, dependencies, or
lockfiles.

If `mise run doctor` is not run for such a PR, report that it was not run for
that reason rather than marking it complete.

## Local and remote evidence split

Local validation and GitHub Actions CI answer different questions. Do not infer
GitHub Actions success from local checks, and do not infer local WSL2,
1Password, SSH agent, Windows interop, user systemd, or workstation convergence
from GitHub Actions CI.

Report GitHub Actions CI as `Pending` until a workflow run, status check, or
explicit maintainer confirmation proves the result. Do not mark CI as `Passed`
from local command output, expected branch protection behavior, or PR creation
alone.

Use [`surfaces.md`](./surfaces.md) for behavior-sensitive validation routing.

# Chezmoi surface capsule

## Purpose

Use this capsule when work touches or cites chezmoi source state, templates,
scripts, rendered target state, or phase-sensitive provisioning behavior.

Keep the capsule focused on failure prevention. Use detailed legacy evidence
instead of copying domain manuals into this file.

## Predictable LLM failure modes

- Editing rendered target-state assumptions instead of repository source state.
- Treating source-state paths such as `dot_config/**`, `private_dot_ssh/**`, or
  `.chezmoiscripts/**` as literal target paths.
- Reformatting Go Template whitespace trimming as harmless Markdown or shell
  cleanup.
- Adding, removing, relabeling, or normalizing trigger comments without scoping
  the rendered-content rerun impact.
- Treating CI convergence as proof of local workstation, WSL2, 1Password, SSH
  agent, or user service convergence.
- Moving logic out of `.chezmoiscripts/**` without proving that phase ordering,
  preconditions, rendered branches, and trigger behavior are preserved.

## Behavior-sensitive boundaries

Preserve source-state versus rendered-target distinctions. A source edit can
change rendered shell, Lua, TOML, JSON, INI, systemd, SSH, or Git behavior even
when the source diff looks documentation-like.

Treat these as behavior-sensitive unless the active issue explicitly scopes the
change:

- `.chezmoiscripts/**` ordering, `before_` and `after_` placement, and
  `run_`, `run_once_`, or `run_onchange_` semantics;
- template whitespace around shebangs, comments, heredocs, and conditional
  branches;
- trigger comments and implicit rendered inputs that control reruns;
- `.chezmoidata/**` and `.chezmoitemplates/**` consumers;
- `.chezmoiignore.tmpl`, `.chezmoi.toml.tmpl`, externals, hooks, and generated
  target paths.

## Evidence and routing links

- [Local repository profile](../profile.md)
- [Local behavior boundaries](../boundaries.md)
- [Local validation map](../validation.md)
- [Chezmoi action graph](../../../chezmoi/action-graph.md)
- [Chezmoi script contract inspection](../../../chezmoi/script-contract-inspection.md)
- [Chezmoi script trigger audit](../../../chezmoi/script-trigger-audit.md)
- [Thin chezmoi phase gate rules](../../../chezmoi/thin-phase-gate-rules.md)
- [Chezmoi data contract boundary](../../../chezmoi/data-contract-boundary.md)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from [Local validation map](../validation.md).

If the change touches source-state templates, scripts, data, or rendered-output
claims, add rendered-output evidence appropriate to the touched surface, such as
`chezmoi execute-template`, `chezmoi diff`, source-state inspection, trigger
audit review, or host-specific rendered branch inspection.

Run `mise run doctor` only when setup, toolchain, rendered config, task behavior,
health-check behavior, scripts, CI semantics, versions, dependencies, or
lockfiles change.

## Out of scope

This capsule does not authorize script rewrites, trigger normalization, template
whitespace cleanup, behavior changes, task delegation, generated output edits, or
legacy documentation deletion.

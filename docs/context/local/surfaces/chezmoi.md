# Chezmoi surface capsule

## Purpose

Use this capsule when work touches or cites chezmoi source state, templates,
scripts, rendered target state, or phase-sensitive provisioning behavior.

Keep the capsule focused on failure prevention. Inspect current source state and
rendered output for detailed behavior claims instead of relying on retired
long-form audit documents.

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

## Comment and template guidance

Use Go Template comments for source-state-only maintainer notes that must not
render into target files. Use target-language comments only when the rendered
file should carry the explanation for someone inspecting the target state.

Preserve functional comments such as trigger hashes, mise task metadata,
generated-file warnings, Renovate extraction comments, and external references.
Do not normalize labels, trim markers, or blank lines in templates as incidental
cleanup.

Before changing comments in `.tmpl` files, decide who should read the note and
which rendered file, if any, should contain it.

## Evidence and routing links

- [Repository operating contract](../../repo.md)
- [Mise surface capsule](./mise.md)
- [WSL2 surface capsule](./wsl2.md)
- [Identity surface capsule](./identity.md)
- [`.chezmoiscripts/`](../../../../.chezmoiscripts/)
- [`.chezmoidata/`](../../../../.chezmoidata/)
- [`.chezmoitemplates/`](../../../../.chezmoitemplates/)
- [`.chezmoiignore.tmpl`](../../../../.chezmoiignore.tmpl)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from the [Repository operating contract](../../repo.md).

If the change touches source-state templates, scripts, data, or rendered-output
claims, add rendered-output evidence appropriate to the touched surface, such as
`chezmoi execute-template`, `chezmoi diff`, source-state inspection, trigger
review, or host-specific rendered branch inspection.

Run `mise run doctor` only when setup, toolchain, rendered config, task behavior,
health-check behavior, scripts, CI semantics, versions, dependencies, or
lockfiles change.

## Out of scope

This capsule does not authorize script rewrites, trigger normalization, template
whitespace cleanup, behavior changes, task delegation, generated output edits, or
removed documentation restoration.

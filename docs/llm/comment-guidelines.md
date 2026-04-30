# Comment guidelines

## Purpose

Use this guide when adding, changing, or reviewing comments in repository source
state.

Good comments explain durable maintenance context that is hard to recover from
the code alone. They should help humans and LLM-assisted workflows preserve
behavior, validate the right surface, and avoid stale assumptions.

This guide is reusable across repositories. The examples use this dotfiles
repository because it is a chezmoi-managed source-state repository.

## What comments should explain

Keep comments that explain:

- non-obvious behavior, ordering, or compatibility constraints
- safety boundaries, idempotency, or destructive-operation guards
- source-state versus rendered-target differences
- generated-file warnings and regeneration paths
- trigger hashes, extraction patterns, or other tool metadata
- external specifications or primary references
- intentional use of deprecated, surprising, or target-specific APIs

Avoid comments that only restate nearby code.

```sh
# Bad: restates the command.
mkdir -p "$BACKUP_ROOT"

# Better: explains the behavior boundary.
# BACKUP_ROOT is created only after a legacy target is found.
mkdir -p "$BACKUP_ROOT"
```

## Comments to remove or rewrite

Remove or rewrite comments that:

- describe old migrations without current maintenance value
- claim authority without a concrete technical referent
- use time-sensitive claims such as "modern", "current", or a year as proof
- duplicate repository policy that belongs in durable documentation
- provide LLM-only guidance in files rendered to users
- obscure higher-signal comments with decorative labels

Prefer concrete technical wording over status-signaling terms.

Avoid terms such as `Sovereign`, `Zero-Trust`, `SOTA`, `Best Practice`,
`Staff Engineer Note`, and year-based authority claims unless the comment names
the precise boundary, standard, threat model, or source that makes the term true.

## Source-only versus target-visible comments

Choose the comment syntax for the audience.

Use source-only comments when the note is for maintainers editing source state.
Use target-language comments when the rendered file should carry the note.

In any generated, templated, or rendered repository, ask two questions:

1. Who needs this note?
2. In which file will that person read it?

If the answer is "a repository maintainer", keep the note in source state. If the
answer is "a user inspecting the rendered file", render the note.

## Chezmoi and Go Template routing

For chezmoi templates, use Go Template comments for source-state-only notes:

```gotemplate
{{/*
Source-only maintainer note:
This branch exists to preserve rendered shell compatibility.
*/}}
```

Use target-language comments only when the rendered target should include the
explanation:

```sh
# This directory is created lazily to avoid empty backup directories.
```

Do not change Go Template whitespace trimming as incidental cleanup. Template
comments and `{{-` / `-}}` trimming can affect rendered output by joining lines,
moving shebangs, or changing blank lines.

## LLM-assisted maintenance notes

LLM-specific instructions should usually live in durable docs such as
`docs/llm/`, not in rendered configuration files.

Use source-only comments only when a local warning is needed at the exact edit
site. Good examples include:

- "Do not make this eager; laziness prevents empty backup directories."
- "This branch is source-state-only and must not render into the target file."
- "This target-language comment is intentionally rendered for user inspection."

Do not put prompts, review checklists, historical debate, or model-specific
instructions into rendered files.

## Label guidance

Labels are useful when they create a real maintenance distinction.

Useful labels include:

- `[Security]` for concrete security boundaries or required permissions
- `[Reference]` for official documentation or primary source links
- `[Trigger]` for hashes or inputs that intentionally retrigger convergence
- `[Generated]` for files or blocks that must not be hand-edited
- tool-owned metadata such as mise task comments and Renovate extraction comments

Labels often add noise when they only decorate a normal rationale. In those
cases, prefer a plain sentence.

Avoid broad labels such as `[Architecture]` and `[Rationale]` when the label does
not add information beyond the comment body.

## Preserve functional tool comments

Do not remove comments that tools parse or humans use as operational metadata.

Examples include:

- mise task metadata such as `# [MISE] description="..."`
- Renovate extraction or dependency comments
- generated-file headers
- trigger hashes in chezmoi scripts
- references that explain why an external specification is required

When in doubt, inspect the tool documentation or search the repository for the
comment pattern before changing it.

## Examples from this repository

### Source-only idempotency note in a chezmoi script

A note about lazy backup directory creation is useful to maintainers, but it
should not render into the target shell script:

```gotemplate
{{/*
Source-only maintainer note:
BACKUP_ROOT is created lazily only after a legacy target is found.
*/}}
```

### Target-visible shell comment

A POSIX compatibility note can remain visible when it helps someone reading the
rendered shell script:

```sh
# POSIX-compliant list of targets
set -- \
  "$HOME/.zshrc" \
  "$HOME/.gitconfig"
```

### Trigger comment

A hash comment in a chezmoi script is useful because it explains why a script
reruns when an included source file changes:

```sh
# [Trigger]: WezTerm Config Hash: {{ include "dot_config/wezterm/wezterm.lua.tmpl" | sha256sum }}
```

### Tool metadata comment

A mise task description is functional metadata and must be preserved:

```sh
# [MISE] description="Verify identity routing and SSH agent health"
```

## Review checklist

Before changing comments, verify:

- the intended audience is clear
- source-only notes do not render into target files
- rendered comments help someone reading the target file
- labels carry a real distinction
- unsupported authority-signaling terms are removed or made precise
- functional tool comments are preserved
- references point to official documentation or primary sources when possible
- behavior, generated output semantics, and validation scope are unchanged

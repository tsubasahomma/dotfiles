# Chezmoi template guidelines

## Purpose

Use this guide when changing chezmoi source-state templates.

Chezmoi template changes are rendered-output-sensitive. A small source-state edit
can change target files, provisioning behavior, shell startup, identity routing,
or workstation convergence.

## Source-state and rendered-target model

This repository stores chezmoi source state.

Source-state files are edited in the repository. Rendered target files are what
chezmoi applies to the user's home directory.

Do not assume source syntax and rendered syntax are the same. A valid
source-state template can render invalid shell, Lua, TOML, INI, JSON, or service
configuration if template whitespace, loops, conditionals, or comments are wrong.

## Comment routing

Use the right comment type for the intended audience.

### Go Template comments

Use Go Template comments for source-state-only rationale that should not appear
in the rendered target file:

```gotemplate
{{/* Source-only explanation for maintainers. */}}
```

Use this for:

- template control-flow rationale
- data-shape assumptions
- source-state safety notes
- LLM guidance that would be noise in the rendered file

### Target-language comments

Use target-language comments when the rendered target file should carry the
explanation.

Examples:

```sh
# Keep this visible in the rendered shell script.
```

```lua
-- Keep this visible in the rendered Lua file.
```

Use this for:

- operational notes useful in the target file
- generated configuration explanations
- warnings future users should see after rendering

## Block comments vs repeated line comments

Use block Go Template comments when a source-only rationale spans multiple
lines. This is clearer than repeating many single-line template comments.

Prefer:

```gotemplate
{{/*
Source-only maintainer note:
This branch is source-state-only documentation.
It explains why the rendered output must not include these notes.
*/}}
```

Avoid noisy repeated comments when one block comment would be clearer.

## Double-extension routing

Treat the final rendered language as the validation target.

### `.sh.tmpl`

Rendered target is POSIX shell or shell script content. Preserve shebang
placement, shell syntax, quoting, and executable behavior.

### `.zsh.tmpl`

Rendered target is Zsh. Preserve startup ordering, completion behavior, array
syntax, and Zsh-specific constructs.

### `.lua.tmpl`

Rendered target is Lua. Preserve Lua syntax after template expansion. Be careful
with commas, string quoting, and conditional table entries.

### `.toml.tmpl`

Rendered target is TOML. Preserve table boundaries, string quoting, and array
syntax.

### `.ini.tmpl`

Rendered target is INI-like configuration. Preserve section headers, key-value
format, and comment syntax expected by the target tool.

### `.json.tmpl`

Rendered target is JSON. Avoid trailing commas and comments in rendered JSON
unless the target format explicitly supports them.

### Extensionless executable `.tmpl` files

Rendered target may be executable shell content even without a `.sh` suffix.
Inspect shebangs and target paths before choosing validation.

### `.chezmoitemplates/*`

These files are template fragments included by other templates. Review both the
fragment and every known include site before changing output-sensitive content.

### `.chezmoiscripts/*`

These files are chezmoi scripts with execution timing encoded in the filename.
Preserve run phase, idempotency, shell choice, and rendered script validity.

## Whitespace trimming

Go Template delimiters can trim whitespace:

- `{{-` trims whitespace before the action.
- `-}}` trims whitespace after the action.

Use trimming deliberately. It can prevent unwanted blank lines, but it can also
join lines accidentally.

Before changing trimming, consider whether it can cause:

- shebang concatenation
- command concatenation
- missing blank lines
- merged comments and code
- invalid target-language syntax

## Rendered-output risks

Common rendered-output failures include:

- shebang no longer being the first line
- accidental line joining
- missing blank lines between generated blocks
- loop-generated extra blank lines
- invalid shell syntax
- invalid Lua table syntax
- invalid TOML, INI, or JSON syntax
- comments rendering into target files when they should remain source-only
- source-only rationale disappearing when maintainers need it

Do not refactor template comments or whitespace trimming as incidental cleanup.

## Validation guidance

Choose validation based on the touched surface.

### When `chezmoi diff` is enough

Use `chezmoi diff` when a template change should be reviewed through rendered
output and does not require applying changes to the target home directory.

This is usually enough for:

- `.chezmoiignore.tmpl` changes
- rendered config inspection
- documentation-supported template edits
- checking whether expected target output changes appear

### When `chezmoi verify` is relevant

Use `chezmoi verify` when checking whether target files match source-state
expectations.

This is useful for drift checks, but it is not a substitute for reviewing a new
rendered diff when template logic changes.

### When CI-style `chezmoi init --source="$PWD" --apply` is excessive

A full init/apply check is heavyweight and can mutate a target environment. Do
not require it for documentation-only changes or small source-state docs.

### When CI-style apply may be justified

A CI-style apply path can be justified when a future issue explicitly changes
provisioning, identity routing, shell startup, tool installation, or other
workstation convergence behavior and a safe disposable environment is available.

## Out-of-scope caution

Do not rewrite existing template comments, whitespace trimming, or rendered
formatting as incidental cleanup.

If comment normalization is valuable, record it as follow-up work after this
guidance exists and the Commander Thread scopes a dedicated change.

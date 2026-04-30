# Repository agent guidance

## Repository identity

This repository is Tsubasa Homma's chezmoi-managed dotfiles source state.
It is an infrastructure repository for provisioning a workstation, not a normal
application repository.

Make changes to source-state files in this repository. Do not treat rendered
files, generated snapshots, or target-home artifacts as editable source.

## Source priority

When sources conflict, prefer the most specific reliable source for the task:

1. The user's current instructions.
2. The assigned GitHub issue, pull request, or review scope.
3. Current local file contents, diffs, command output, and CI evidence.
4. This repository guidance.
5. Repository docs such as [README.md](./README.md) and
   [ARCHITECTURE.md](./ARCHITECTURE.md).
6. Official tool documentation when needed.

Do not override explicit issue constraints with general guidance unless current
repository evidence shows a conflict. Report the conflict instead of guessing.

For detailed LLM and workflow guidance, use
[docs/llm/README.md](./docs/llm/README.md) and
[docs/workflows/README.md](./docs/workflows/README.md). For comment hygiene and
comment routing, use
[docs/llm/comment-guidelines.md](./docs/llm/comment-guidelines.md). Keep this
file as the repository-wide entry point rather than duplicating detailed process
rules here.

## Behavior preservation

Preserve existing behavior unless the assigned issue explicitly scopes a change.

Be especially careful with:

- chezmoi provisioning behavior
- 1Password identity routing
- SSH signing and SSH agent bridging
- generated identity files
- Neovim, WezTerm, zsh, Git, mise, and Homebrew behavior
- GitHub Actions `compliance.yml` semantics
- runtime versions, tool versions, dependencies, and lockfiles

Do not introduce new dependencies, generated files, or lockfiles unless the
issue explicitly requires them.

## Commander and Worker model

Use Commander / Worker separation for multi-PR work.

The Commander owns issue topology, PR sequencing, cross-PR synthesis, and final
merge or closure recommendations.

A Worker owns one assigned issue, pull request, or bounded task. A Worker should
not expand scope, close a tracking issue, or change the PR sequence unless the
Commander explicitly assigns that decision.

## Evidence-first work

Ground recommendations in repository evidence.

Use current local evidence such as `git status --short`, `git diff`, `sed`,
`rg`, validation output, CI results, and Repomix snapshots. Do not invent file
paths, tool versions, issue numbers, PR numbers, command results, validation
status, or CI status.

Treat `repomix-*.xml` files as read-only context. Make changes to original
repository files, not generated Repomix output.

## Patch and output discipline

For repository changes intended for `git apply`, use strict Git extended
unified diff format. Do not include prose inside patch blocks, fake `index`
lines, placeholder hashes, or abbreviated pseudo-diffs.

When current file contents are incomplete, request the smallest useful local
inspection bundle instead of producing a fragile patch.

For new Markdown files, whole-file creation can be safer than a fragile hunk
when the user is applying changes locally. For issue bodies, PR bodies, commit
messages, review summaries, and command bundles, label the output as non-patch
content.

## Validation discipline

Do not claim validation passed without command output, CI evidence, or explicit
user-provided confirmation.

Choose validation that matches the touched surface. Documentation and routing
changes usually start with:

- `git diff --check`
- `pre-commit run --all-files`
- `repomix`

When `.chezmoiignore.tmpl` or other rendered-output-sensitive templates change,
also ask for `chezmoi diff`.

Do not require heavier checks such as `mise run doctor` unless the change touches
setup instructions, toolchain behavior, rendered configuration behavior, or a
task surface that justifies it.

## Chezmoi template caution

Be careful with Go Template comments and whitespace trimming.

Use Go Template comments for source-state-only rationale that should not render
to the target file. Use target-language comments only when the rendered file
should carry the explanation.

Before changing `.tmpl` files, consider rendered output risks such as shebang
concatenation, accidental line joining, missing blank lines, loop-generated
blank lines, and invalid target-language syntax.

Do not refactor existing template comments or whitespace trimming as incidental
cleanup. Keep template changes scoped and verify rendered output when relevant.

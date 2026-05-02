# Repository context manifest

## Repository identity

This repository is Tsubasa Homma's chezmoi-managed dotfiles source state for
personal workstation configuration.

It is an infrastructure repository, not an application repository, package
workspace, deployment monorepo, or Terraform/OpenTofu repository. Make changes to
repository source state, not rendered target files or generated context
artifacts.

## Mandatory context entry point

Use [docs/context/README.md](./docs/context/README.md) as the durable context
architecture entry point.

Context layers:

- [Core context guidance](./docs/context/core/README.md) for reusable assistant
  rules.
- [Local context guidance](./docs/context/local/README.md) for dotfiles-specific
  repository rules.
- [Local surface capsules](./docs/context/local/surfaces/README.md) for
  behavior-sensitive surface routing.
- [Local workflow guidance](./docs/context/local/workflows/README.md) for issue,
  pull request, validation, merge, closure, Commander, and Worker procedures.
- [Repomix context routing](./docs/context/repomix/README.md) for tracked
  Repomix consumption guidance.

## Source and evidence hierarchy

When sources conflict, prefer the most specific current evidence for the task:

1. active user instructions;
2. assigned issue, pull request, review, or validation scope;
3. current file contents, diffs, command output, or CI evidence;
4. `docs/context/**` guidance for the touched layer or surface;
5. repository entry points such as [README.md](./README.md) and
   [ARCHITECTURE.md](./ARCHITECTURE.md);
6. official tool documentation when repository evidence requires it.

Do not invent repository state, command results, validation status, CI status,
issue state, file paths, tool versions, or generated artifact contents.

## Non-negotiable safety boundaries

Preserve existing behavior unless the active issue explicitly scopes a behavior
change.

Do not change these surfaces as incidental documentation or routing cleanup:

- chezmoi scripts, templates, attributes, hooks, externals, or rendered target
  behavior;
- 1Password identity routing, SSH signing, SSH agent bridge behavior, generated
  identity files, or secret-adjacent output handling;
- Neovim, WezTerm, zsh, Git, Homebrew, mise, Vale, or shell startup behavior;
- mise task names, grouping, metadata, dependencies, executable bits, runtime
  versions, tool versions, dependencies, or lockfiles;
- GitHub Actions workflow semantics, issue templates, or pull request template
  behavior;
- generated Repomix output or other generated artifacts.

## Generated artifact discipline

Generated, rendered, packed, or temporary artifacts are evidence unless the
active issue explicitly scopes their source mechanism.

Do not hand-edit generated Repomix output under `.context/repomix/**` or any
`repomix-*.xml` snapshot. Change source files or generation configuration, then
regenerate artifacts when validation requires fresh evidence.

## Patch, validation, and scope control

Inspect broadly enough to avoid local mistakes, then patch narrowly within the
assigned scope.

For repository patches intended for `git apply`, provide strict Git extended
unified diffs with accurate current-file context and no prose inside patch
blocks. Do not use placeholder hashes or pseudo-diffs.

Report validation only as evidence. A completed validation item requires command
output, exit status, CI evidence, directly inspected state, or explicit
maintainer confirmation. Local checks do not prove GitHub Actions CI, and clean
patch application does not prove semantic correctness.

Record useful out-of-scope findings separately instead of expanding the active
patch.

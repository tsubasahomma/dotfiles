# Repository context manifest

## Repository identity

This repository is Tsubasa Homma's chezmoi-managed dotfiles source state for
personal workstation configuration.

It is an infrastructure repository, not an application repository, package
workspace, deployment monorepo, or Terraform/OpenTofu repository. Make changes to
repository source state, not rendered target files or generated context
artifacts.

## Mandatory context entry point

Use [docs/context/README.md](./docs/context/README.md) as the operating-contract
entry point and task-to-context router.

Option A+ operating-contract files:

- [Kernel](./docs/context/kernel.md) for instruction precedence, evidence
  precedence, context economy, scope control, unknown-state rules, and generated
  artifact discipline.
- [Protocols](./docs/context/protocols.md) for patch, command,
  validation-report, PR, commit, code-fence, heredoc, whitespace, and final
  newline output contracts.
- [Repo](./docs/context/repo.md) for dotfiles source-state boundaries,
  behavior-preserving constraints, supported host posture, root document roles,
  and local validation baseline.
- [Surfaces](./docs/context/surfaces.md) for behavior-sensitive surface routing.
- [Workflows](./docs/context/workflows.md) for issue, thread, PR, validation,
  merge, and closure procedure contracts.
- [Repomix](./docs/context/repomix.md) for Repomix generation, consumption,
  generated-output, focused snapshot, stale-snapshot rules, and tracked
  instruction routing.
- [Evals](./docs/context/evals.md) for regression cases covering predictable
  LLM-context failures.

## Scope and evidence hierarchy

Use active scope to decide what may change. Use current direct evidence to decide
what is true. Route detailed precedence rules to
[docs/context/kernel.md](./docs/context/kernel.md).

At the root manifest level:

- active user instructions and assigned issue, pull request, review, or
  validation scope authorize the change boundary;
- current file contents, diffs, command output, CI evidence, and explicit
  maintainer confirmation establish repository state;
- selected Option A+ operating contracts define reusable rules for the task;
- generated snapshots are read-only evidence and lose to fresher direct evidence;
- prior conversation, memory, old prompts, and previous assistant output never
  override active scope or current evidence.

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

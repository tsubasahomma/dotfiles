# LLM collaboration guidance

This directory indexes repository-specific guidance for LLM-assisted dotfiles
maintenance.

Use these docs to route work, inspect evidence, produce safe output, write commit
messages, review changes, and handle chezmoi template risks without changing
provisioning behavior.

## Entry points

- [Routing](./routing.md): source priority, repository entry points,
  Commander / Worker boundaries, task-surface routing, and uncertainty handling.
- [Local state inspection](./local-state-inspection.md): how to use local file
  contents, command output, validation output, CI evidence, and Repomix snapshots.
- [Diff output guardrails](./diff-output-guardrails.md): safe patch, heredoc,
  guarded-script, and non-patch output formats.
- [Comment guidelines](./comment-guidelines.md): comment usefulness,
  source-only versus target-visible routing, labels, and LLM maintenance notes.
- [Commit message guidelines](./commit-message-guidelines.md): Conventional
  Commit structure, issue reference rules, and validation claim discipline.
- [Review protocol](./review-protocol.md): scope review, behavior preservation,
  validation review, link review, and LLM failure modes.
- [Chezmoi template guidelines](./chezmoi-template-guidelines.md):
  source-state and rendered-target guidance for Go Template files.
- [Chezmoi action graph](../chezmoi/action-graph.md): repository-owned
  action graph and script contracts for current behavior.

## Related workflow docs

- [Workflow documentation](../workflows/README.md): issue, pull request,
  validation, merge, and closure workflows.
- [Repository agent guidance](../../AGENTS.md): repository-wide agent boundaries
  and validation expectations.
- [Repomix instruction router](../context/repomix/instructions.md): Repomix snapshot
  instruction entry point.

## Repository posture

This repository is a chezmoi-managed dotfiles source-state repository. It is not
a normal application repository.

Preserve existing behavior unless the assigned issue explicitly scopes a change,
especially:

- chezmoi provisioning behavior
- 1Password identity routing
- SSH signing and SSH agent bridging
- generated identity files
- Neovim, WezTerm, zsh, Git, mise, and Homebrew behavior
- GitHub Actions `compliance.yml` semantics
- runtime versions, tool versions, dependencies, and lockfiles

Treat generated `repomix-*.xml` files as read-only evidence. Make changes to
the original repository files.

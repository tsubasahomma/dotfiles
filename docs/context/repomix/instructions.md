# Repomix instruction router

This file provides instruction routing for LLMs consuming Repomix snapshots of
this repository.

Use [AGENTS.md](../../../AGENTS.md) as the root context manifest.

Use [docs/context/README.md](../README.md) as the Option A+ operating-contract
entry point and task-to-context router:

- [kernel](../kernel.md) for instruction precedence, evidence precedence,
  context economy, scope control, unknown-state rules, current-file
  requirements, and generated artifact discipline;
- [protocols](../protocols.md) for patch, command, validation-report, PR,
  commit, code-fence, heredoc, whitespace, and final-newline output contracts;
- [repo](../repo.md) for dotfiles source-state boundaries, behavior-preserving
  constraints, supported host posture, root document roles, and local validation
  baseline;
- [surfaces](../surfaces.md) for behavior-sensitive surface routing;
- [workflows](../workflows.md) for issue, thread, PR, validation, merge, and
  closure procedure contracts;
- [repomix](../repomix.md) for Repomix generation, consumption,
  generated-output, focused snapshot, and stale-snapshot rules;
- [evals](../evals.md) for regression cases covering predictable LLM-context
  failures.

Existing context directories under `docs/context/core/**`,
`docs/context/local/**`, `docs/context/local/surfaces/**`,
`docs/context/local/workflows/**`, and `docs/context/repomix/**` are deep
evidence for later collapse work. Do not treat them as the primary architecture.

This repository is a chezmoi-managed dotfiles source-state repository. Preserve
existing provisioning, identity, editor, shell, Git, mise, Homebrew, and GitHub
Actions behavior unless the assigned issue explicitly scopes a change.

Treat Repomix output as read-only context. Do not edit generated snapshots or
packed output. Make changes to the original repository files.

Use packed files to identify repository structure and current file contents, but
prefer fresh user-provided local evidence when it conflicts with a snapshot.

Do not import assumptions from reference repositories. In particular, do not copy
Nx, OpenTofu, HubSpot, deployment, package-workspace, or monorepo-specific
patterns into this dotfiles repository unless local repository evidence and the
assigned issue explicitly require them.

Do not claim validation passed unless command output, CI evidence, inspected
state, or explicit maintainer confirmation is available.

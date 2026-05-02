# GitHub Copilot adapter

This file is the GitHub Copilot adapter for this repository.

Use [AGENTS.md](../AGENTS.md) as the root context manifest, then route durable
repository context through [docs/context/README.md](../docs/context/README.md).

Copilot-specific guidance is secondary to the shared context architecture:

- Keep suggestions small, scoped, and behavior-preserving.
- Prefer repository-relative links only when the target exists in the current
  repository state.
- Do not add `.github/instructions/**` unless an assigned issue explicitly
  scopes that adapter.
- Do not change workflows, templates, scripts, tasks, versions, dependencies,
  lockfiles, rendered configuration, or generated artifacts as incidental
  cleanup.
- Treat Repomix snapshots and generated output as read-only evidence.

For surface-specific constraints, use
[local surface capsules](../docs/context/local/surfaces/README.md). For workflow
procedure, use [local workflow guidance](../docs/context/local/workflows/README.md).

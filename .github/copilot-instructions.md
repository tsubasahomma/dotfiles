# GitHub Copilot adapter

This file is the GitHub Copilot adapter for this repository.

Use [AGENTS.md](../AGENTS.md) as the root context manifest, then route durable
repository context through [docs/context/README.md](../docs/context/README.md).

Copilot-specific guidance is secondary to the shared Option A+ operating
contract:

- Keep suggestions small, scoped, and behavior-preserving.
- Use [docs/context/README.md](../docs/context/README.md) to select the smallest
  sufficient context before relying on deeper evidence.
- Prefer repository-relative links only when the target exists in the current
  repository state.
- Do not add `.github/instructions/**` unless an assigned issue explicitly
  scopes that adapter.
- Do not change workflows, templates, scripts, tasks, versions, dependencies,
  lockfiles, rendered configuration, or generated artifacts as incidental
  cleanup.
- Treat Repomix snapshots and generated output as read-only evidence.

For surface-specific constraints, start with
[docs/context/surfaces.md](../docs/context/surfaces.md). For workflow procedure,
start with [docs/context/workflows.md](../docs/context/workflows.md). For Repomix
generation or snapshot consumption, start with
[docs/context/repomix.md](../docs/context/repomix.md).

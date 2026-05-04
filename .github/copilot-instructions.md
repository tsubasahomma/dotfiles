# GitHub Copilot adapter

This file is the GitHub Copilot adapter for this repository.

Use [AGENTS.md](../AGENTS.md) as the root context manifest. Route portable
operating-contract guidance through
[docs/context/README.md](../docs/context/README.md), and route repository-local
facts through [docs/repo/README.md](../docs/repo/README.md) only when the task
needs them.

Copilot-specific guidance is secondary to the shared context operating contract:

- Keep suggestions small, scoped, and behavior-preserving.
- Use [docs/context/README.md](../docs/context/README.md) to select the smallest
  sufficient portable context before relying on deeper evidence.
- Use [docs/repo/README.md](../docs/repo/README.md) for local source-state,
  surface, validation, workflow, Repomix, host, identity, or adapter facts.
- Prefer repository-relative links only when the target exists in the current
  repository state.
- Do not add `.github/instructions/**` unless an assigned issue explicitly
  scopes that adapter.
- Do not change workflows, templates, scripts, tasks, versions, dependencies,
  lockfiles, rendered configuration, or generated artifacts as incidental
  cleanup.
- Treat Repomix snapshots and generated output as read-only evidence.

For surface-specific constraints, start with
[docs/repo/surfaces.md](../docs/repo/surfaces.md). For workflow procedure, start
with [docs/context/workflows.md](../docs/context/workflows.md) and add
[docs/repo/workflows.md](../docs/repo/workflows.md) only when local exceptions or
templates matter. For Repomix generation or snapshot consumption, start with
[docs/context/repomix.md](../docs/context/repomix.md) and add
[docs/repo/repomix.md](../docs/repo/repomix.md) only for local paths and checks.

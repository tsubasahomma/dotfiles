# GitHub Actions surface capsule

## Purpose

Use this capsule when work touches or cites GitHub Actions workflows, compliance
CI semantics, branch-protection evidence, or remote CI status.

Keep CI guidance focused on behavior boundaries. Workflow procedure migration
belongs under `docs/context/local/workflows/**`, not in this capsule.

## Predictable LLM failure modes

- Treating local validation as proof that GitHub Actions CI passed.
- Treating a clean GitHub Actions run as proof of local WSL2, 1Password, SSH
  agent, user systemd, or Windows interop convergence.
- Changing workflow triggers, permissions, matrix entries, action pins, or phase
  commands as documentation cleanup.
- Reordering `chezmoi`, `mise run integrate:nvim`, and `mise run doctor` phases
  without explicit behavior scope.
- Adding secrets, environments, or branch-protection claims without current
  repository or GitHub evidence.
- Moving PR, merge, or closure procedures into this surface capsule.

## Behavior-sensitive boundaries

The compliance workflow is behavior-sensitive because it applies source state,
proves idempotency, restores Neovim integration, and runs the repository doctor
path in automation.

Treat these as behavior-sensitive unless explicitly scoped:

- `.github/workflows/**` triggers, permissions, matrix, environment, and
  concurrency semantics;
- pinned action references and Renovate-managed workflow comments;
- `chezmoi init --source="$GITHUB_WORKSPACE" --apply` automation behavior;
- `chezmoi verify` idempotency proof;
- `mise run integrate:nvim` and `mise run doctor` CI phases;
- PR template validation wording when it changes required evidence.

## Evidence and routing links

- [Local validation map](../validation.md)
- [Local behavior boundaries](../boundaries.md)
- [Local workflow routing](../workflows/README.md)
- [Compliance workflow](../../../../.github/workflows/compliance.yml)
- [Pull request template](../../../../.github/pull_request_template.md)
- [Validation workflow migration input](../../../workflows/validation-workflow.md)

## Validation routing

For documentation-only capsule or routing edits, use baseline documentation
validation from [Local validation map](../validation.md).

If a change touches workflow YAML, workflow commands, action pins, permissions,
triggers, matrix behavior, CI phase order, or branch-protection claims, remote
GitHub Actions evidence is required after PR creation when that status is claimed
or required. Local checks do not prove remote CI status.

## Out of scope

This capsule does not authorize workflow behavior changes, action updates,
branch-protection edits, secret or environment changes, PR procedure migration,
merge procedure migration, or treating CI as local workstation convergence
proof.

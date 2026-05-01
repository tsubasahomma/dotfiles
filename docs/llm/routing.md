# LLM routing

## Purpose

Use this guide to choose the right repository guidance, evidence, and workflow
before starting LLM-assisted dotfiles work.

Routing should keep changes scoped, evidence-based, and behavior-preserving.

## Source priority

When sources conflict, prefer the most specific reliable source for the task:

1. The user's current instructions.
2. The assigned issue, pull request, review, or Worker prompt.
3. Current local evidence such as file contents, diffs, command output, and CI.
4. [Repository agent guidance](../../AGENTS.md).
5. Focused repository docs for the touched surface, such as
   [Chezmoi action graph](../chezmoi/action-graph.md) for chezmoi
   orchestration contracts.
6. Repository entry points such as [README.md](../../README.md) and
   [ARCHITECTURE.md](../../ARCHITECTURE.md).
7. Official tool documentation when needed.

Do not override explicit issue constraints with general guidance. If current
local evidence contradicts the issue or prompt, report the conflict and ask the
Commander Thread for a scope decision.

## Repository entry points

Start with these repository-wide entry points:

- [AGENTS.md](../../AGENTS.md): repository-wide boundaries and validation posture.
- [Architecture documentation routing](../../ARCHITECTURE.md): high-level
  repository overview and routed legacy architecture entry point.
- [LLM collaboration index](./README.md): LLM-specific guidance.
- [Workflow documentation](../workflows/README.md): issue, PR, validation, merge,
  and closure workflows.
- [Repomix instruction router](../../repomix-instruction.md): instructions for
  LLMs consuming Repomix snapshots.
- [GitHub Copilot instructions](../../.github/copilot-instructions.md): thin
  router for tools that consume GitHub Copilot repository instructions directly.

Keep router files thin. Detailed durable rules belong in `docs/llm/` and
`docs/workflows/`.

## Commander and Worker separation

Use Commander / Worker separation when work spans multiple PRs or issue slices.

Commander Threads own:

- issue topology
- PR sequencing
- cross-PR synthesis
- final merge and closure recommendations
- decisions about scope changes

Worker Threads own:

- one assigned issue, PR, or bounded task
- local evidence review for that scope
- patch, heredoc, command, PR body, or review output for that scope
- validation interpretation after the user provides evidence

A Worker Thread should not silently expand scope, close a tracking issue, or
change PR sequencing.

## Local evidence hierarchy

Prefer current local evidence over older snapshots when they conflict.

Useful evidence includes:

- `git status --short`
- `git diff`
- `git diff --stat`
- `git diff --name-status`
- `git diff --check`
- `git ls-files`
- `find`
- `rg`
- `sed`
- validation command output
- GitHub Actions results
- Repomix snapshots

Do not invent local state. For details, see
[Local state inspection](./local-state-inspection.md).

## Repomix routing

Use Repomix snapshots as read-only evidence.

The canonical command for a full repository snapshot is:

```sh
repomix
```

If configuration discovery is unclear, use the explicit fallback:

```sh
repomix --config repomix.config.json
```

Do not edit generated `repomix-*.xml` files. Do not add alternate repository-owned
Repomix configs, wrapper tasks, or skeleton snapshots unless a future issue
explicitly scopes that work.

## Workflow routing

Use workflow docs for process decisions:

- [Issue workflow](../workflows/issue-workflow.md): scope contracts,
  acceptance criteria, PR slicing, and out-of-scope findings.
- [Pull request workflow](../workflows/pull-request-workflow.md): PR body,
  labels, linked issues, review readiness, risk, and rollback.
- [Validation workflow](../workflows/validation-workflow.md): validation by
  touched surface and evidence reporting.
- [Merge and close workflow](../workflows/merge-and-close-workflow.md): merge
  readiness, issue closure, checkbox updates, and rollback after merge.

## Task-surface routing

Route by touched surface before proposing changes.

### Documentation-only changes

Prefer `docs/llm/` or `docs/workflows/` for durable guidance. Validate with
`git diff --check`, `pre-commit run --all-files`, Markdown link checks, and
`repomix` when LLM routing or snapshot guidance changes.

### Comment and reference hygiene changes

Use [Comment guidelines](./comment-guidelines.md) before changing comments,
references, or labels. Preserve comments that carry operational, safety,
generated-file, trigger, or tool-metadata meaning. Do not mix broad vocabulary
cleanup into a Worker scope unless the assigned issue explicitly includes it.

### Chezmoi template changes

Use [Chezmoi action graph](../chezmoi/action-graph.md) and the focused
`docs/chezmoi/` contract documents for repository-owned orchestration contracts
before behavior-preserving refactoring.
Inspect source-state and rendered-target impact. Be careful with Go Template
comments, whitespace trimming, shebang placement, blank lines, and target-language
syntax. See [Chezmoi template guidelines](./chezmoi-template-guidelines.md).

### `.chezmoiignore.tmpl` and target ignore changes

Treat these as rendered-output-sensitive. Require `chezmoi diff` unless the user
or Commander explicitly scopes a different evidence path.

### Identity and 1Password-sensitive changes

Avoid incidental edits. Changes touching 1Password, SSH signing, SSH agent
bridging, generated identity files, or scoped Git identity routing require
explicit issue scope and strong validation evidence.

### Neovim changes

Preserve LazyVim behavior, plugin lockfile semantics, provider configuration, and
existing keymap decisions unless explicitly scoped. Prefer Neovim-specific
validation only when Neovim files or rendered Neovim behavior change.

### WezTerm changes

Preserve macOS and WSL routing behavior. Treat WSL sync and Windows-host bridge
logic as behavior-sensitive.

### zsh and shell changes

Preserve shell startup ordering, POSIX vs Zsh boundaries, and template rendering.
Use shell-specific validation only when shell files or rendered shell behavior
change.

### mise task and toolchain changes

Preserve tool versions, task names, task semantics, and lockfile behavior unless
explicitly scoped. Use `mise run doctor` only when the touched surface justifies
it.

### GitHub Actions changes

Preserve `compliance.yml` semantics unless explicitly scoped. Do not infer CI
success from local validation.

### Repomix routing changes

Keep `repomix.config.json` and `repomix-instruction.md` aligned. Validate with
`repomix` and inspect whether generated snapshots include the intended guidance.

## Uncertainty handling

If evidence is missing, state what is missing and request the smallest useful
inspection bundle. Do not produce fragile patches based on guessed file contents.

If a useful improvement is outside scope, record it as an out-of-scope note for
the Commander Thread instead of implementing it.

# Repository workflow extensions

## Purpose

Define repository-local workflow exceptions, GitHub deliverable defaults, and
template routing.

Use [`../context/workflows.md`](../context/workflows.md) for reusable issue,
thread, PR, validation, merge, closure, checkbox, rollback, and parent-child
procedure. Use this file only when the reusable workflow needs this repository's
local branch naming, labels, templates, validation baseline, CI boundary,
Repomix expectations, or assistant routing rules.

## Local GitHub deliverable defaults

These defaults apply to generated issue, PR, commit, validation, and command
artifacts for this repository. They are local conventions, not portable
requirements.

| Default | Rule |
| --- | --- |
| Documentation branch names | Use `docs/issue<child-issue-number>-<short-scope>` for documentation-only GitHub workflow, context, schema, template-routing, assistant-guidance, and validation-default changes. |
| Non-documentation branch names | Use the narrowest accurate Conventional Commit-style prefix, such as `fix/`, `chore/`, or `refactor/`, only when the active issue scopes non-documentation behavior. |
| Short scope | Use lowercase kebab case, keep it specific, and avoid repository names, labels, PR numbers, or parent issue numbers. |
| Commit scope | Use the touched documentation owner, such as `docs(repo)` or `docs(context)`, and do not imply behavior changes. |
| Issue references | Keep commit messages issue-reference-free. Put `Closes` and `Refs` only in PR bodies. |

## Local label policy

Generated issue and PR commands may include labels only when label existence is
proved by current repository evidence or by a preflight check in the emitted
command.

| Label decision | Rule |
| --- | --- |
| Default documentation label | `documentation` is the local default candidate for documentation-only changes when current repository evidence or a command preflight proves the label exists. |
| Missing label evidence | Do not emit `--label`. State that label evidence is missing or include a label preflight before the command. |
| Multiple labels | Use more than one label only when each label exists and the meanings are orthogonal. |
| Portable examples | Keep labels as placeholders such as `<label-name>` outside repository-local docs. |

## Local template routing

`.github` templates are local UI scaffolds and shape evidence. They are not the
portable operating-contract source for issue, PR, commit, validation, or command
schemas.

| Template | Local path | Rule |
| --- | --- | --- |
| Issue template | [`../../.github/ISSUE_TEMPLATE/change-request.yml`](../../.github/ISSUE_TEMPLATE/change-request.yml) | Use as local UI scaffold evidence for scoped repository changes. Do not edit from workflow-default or procedure work unless the active issue explicitly scopes template changes. |
| Pull request template | [`../../.github/pull_request_template.md`](../../.github/pull_request_template.md) | Use as local UI scaffold evidence for PR body structure. Remove template comments from final PR text, use state-bearing validation evidence instead of checkbox-only claims, and do not manually mirror dynamic GitHub Actions CI results. |

## Local validation routing

Use [`validation.md`](./validation.md) for repository-specific validation
baselines, documentation-only `mise run doctor` skip boundaries, and touched-file
validation routing.

For documentation-only context, workflow, schema, template-routing,
assistant-guidance, and validation-default changes, expect the local baseline in
[`validation.md`](./validation.md). Report unrun checks as `Pending`, `Skipped`,
or `Not required` with a reason instead of implying completion.

Use [`surfaces.md`](./surfaces.md) when workflow decisions depend on
behavior-sensitive local surfaces. Remote CI cannot substitute for local WSL2,
1Password, SSH agent bridge, Windows interop, user systemd, or workstation
convergence evidence.

## Local GitHub Actions CI boundary

GitHub Actions CI is remote evidence and must be checked in GitHub Checks or
status checks after PR creation. Do not add or maintain dynamic CI result rows in
PR body validation tables. If remote CI needs reviewer attention, cite a workflow
run, status check, or explicit maintainer confirmation in Review notes. Do not
claim CI passed because local checks passed, because a PR was created, or because
the change is documentation-only.

Do not change `.github/workflows/**` semantics from GitHub workflow-default
work. If a future issue scopes workflow behavior changes, use
[`surfaces.md`](./surfaces.md) for GitHub Actions validation routing.

## Local issue-linking expectations

A completing child PR should use `Closes #<child-issue-number>` only when the
child acceptance criteria are met. Use `Refs #<parent-issue-number>` for the
parent ledger. Do not use `Closes` for the parent issue unless the parent-level
acceptance criteria are complete.

## Local Repomix expectations

Do not hand-edit generated Repomix output. When context, workflow contract,
schema, template-routing, assistant-guidance, or repository-local workflow
defaults change, run the local Repomix checks in [`repomix.md`](./repomix.md) and
report generated evidence as validation, not source documentation.

Use [`../context/repomix.md`](../context/repomix.md) for generic Repomix
procedure. Use [`repomix.md`](./repomix.md) only for local paths, recipes, and
confirmation checks.

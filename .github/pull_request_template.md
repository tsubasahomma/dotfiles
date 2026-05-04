## Summary

<!-- Describe the change in one or two sentences. -->

## Scope

<!-- State the bounded scope of this pull request. -->

## Changes

<!-- List the concrete changes in this pull request. -->

-

## Validation

<!-- Use only these states: Passed, Failed, Pending, Skipped, Not required, Maintainer-confirmed. Use Passed only with command output, CI evidence, inspected state, or maintainer confirmation. -->

| Check | State | Evidence | Notes |
| --- | --- | --- | --- |
| `git diff --check` | Pending | Not run yet. | Required unless the active issue explicitly scopes it out. |
| `pre-commit run --all-files` | Pending | Not run yet. | Baseline local validation. |
| Markdown relative link validation | Not required | No Markdown links changed. | Change to Pending when Markdown links are added, removed, or changed. |
| `repomix` | Pending | Not run yet. | Required when LLM guidance, context routing, workflow contracts, templates, or snapshot routing change. |
| `mise run doctor` | Not required | Documentation/template-only change. | Change state if setup, toolchain, rendered config, task behavior, health-check behavior, scripts, CI semantics, versions, dependencies, or lockfiles change. |
| GitHub Actions CI | Pending | Not available until workflow run evidence exists. | Do not mark Passed without CI evidence or maintainer confirmation. |

## Risk

<!-- Describe the main risk. -->

## Rollback

<!-- Describe the safest rollback path. -->

## Review notes

<!-- Call out files, design trade-offs, or areas that need careful review. -->

## Out of scope

<!-- List related work that this pull request intentionally does not include. -->

-

## Linked issues

<!-- Add Closes #<child-issue-number> only when this pull request completes that child issue. Add Refs #<parent-issue-number> for parent ledgers, partial progress, or related evidence. -->

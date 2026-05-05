# Dependency-governance operating contract

## Purpose

Define portable routing and evidence rules for dependency-governance
configuration maintained by external validators, update bots, CI workflows, or
package-resolution tools.

Use this file when work touches dependency update policy, update-bot
configuration, validator commands, package-manager resolution, CI validation for
dependency governance, or guidance that could weaken dependency review domains.

## Responsibility boundary

This file owns reusable dependency-governance evidence rules, validator parity,
runtime parity, repository versus global configuration boundaries, and
governance-preserving failure response.

It does not own repository-specific package rules, local validator versions,
workflow file paths, runtime declarations, local surface routing, or local
validation baselines. Route those through the local extension layer.

## Governance-preserving defaults

Treat dependency-governance configuration as behavior-sensitive. It controls
which updates appear, how review domains are separated, which defaults apply,
and which security or maintenance policy a repository follows.

When validator output conflicts with intended governance, do not simplify or
delete governance settings until the task has current evidence for:

- validator distribution and exact version;
- schema or preset version being applied;
- repository config mode versus global, inherited, or self-hosted config mode;
- config discovery path and positional filename semantics;
- shell runtime and package-resolution environment;
- local and CI parity when both are claimed or required.

Command text alone is not evidence of equivalent validation behavior. Two
commands with the same text can differ when the validator distribution, schema,
runtime, environment variables, package manager, cache, config discovery, or CI
runner image differs.

## Validator update protocol

When changing dependency-governance validator commands, versions, package
sources, or CI runtime setup:

1. identify whether the validator is checking repository configuration, shared
   preset configuration, inherited configuration, or global self-hosted
   configuration;
2. pin or otherwise make explicit the validator distribution and version used by
   local reproduction and CI;
3. record validator version output, shell runtime output, package-manager or
   package-resolution evidence, and the strict validation result;
4. compare local and CI evidence before claiming parity;
5. keep governance settings intact unless current evidence proves the settings
   are invalid for the intended config mode.

Do not treat a stale, floating, or mismatched validator as authority to remove
valid governance settings. Fix the validator path, version, runtime, schema, or
config mode first.

## GitHub Actions runtime split

GitHub Actions JavaScript action runtime controls only the runtime used by that
action's packaged JavaScript. It does not prove the shell `node`, `npm`, `npx`,
or package-manager runtime used by workflow `run:` steps.

When a dependency-governance validation step executes through `run:`, evidence
for that step must come from the runner shell environment or an explicit runtime
setup step, not from action metadata, action digest pinning, or JavaScript action
runtime migration controls alone.

## Multi-repository routing

For repeated dependency-governance policy across repositories, prefer a shared
configuration or preset mechanism when the tool supports it. Repository-local
docs should document local facts and validation commands; portable contracts
should document reusable evidence requirements and failure boundaries.

Use compact regression cases for repeated LLM failure modes. Do not turn this
contract into a tool manual, incident history, or repository-specific policy
archive.

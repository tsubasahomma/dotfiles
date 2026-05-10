# Agent Context Contracts

This directory contains portable operating contracts for agent collaboration in
a consumer repository. The contracts are repository-agnostic: they define
reusable boundaries, expectations, and extension points without embedding local
identity, host details, commands, secrets, vendor-specific baseline assumptions,
or local operational facts.

Project-local context belongs under `docs/project/**` when a consumer repository
needs to describe its own identity, source maps, validation commands, workflow
exceptions, policy details, or sensitive surfaces.

## Reader Path

Use this table as a navigation aid only. It points to the contracts that own the
details instead of replacing their rules. After reading the relevant portable
contracts, read materialized `docs/project/**` files when they exist and are
relevant. Starter files under `payload/missing-only/docs/project/**` are
missing-only seed content, not active project-local context.

| Task | Start with | Then read as needed |
| --- | --- | --- |
| First-pass orientation | [Core contract](core.md) | [Source precedence and trust boundaries](sources.md), then the relevant topic contracts below. |
| Implement or change repository content | [Source precedence and trust boundaries](sources.md), [Workflow contracts](workflows.md) | [Validation contracts](validation.md), [Agent-authored output contracts](outputs.md), [Ownership and installer safety](ownership.md). |
| Review or evaluate a change | [Evaluation contracts](evaluations.md) | [Validation contracts](validation.md), [Workflow contracts](workflows.md), [Source precedence and trust boundaries](sources.md), [Agent-authored output contracts](outputs.md). |
| Validate a change | [Validation contracts](validation.md) | [Evidence-packing contracts](evidence-packing.md), [Source precedence and trust boundaries](sources.md), and topic contracts for the validated surface. |
| Consult or update project-local memory | Materialized `docs/project/**` files when present and relevant | [Source precedence and trust boundaries](sources.md), [Ownership and installer safety](ownership.md). |
| Check ownership or installer boundaries | [Ownership and installer safety](ownership.md) | [Core contract](core.md), [Source precedence and trust boundaries](sources.md). |

## Contract Set

| Contract | Purpose |
| --- | --- |
| [Core contract](core.md) | Defines the shared portable principles and boundary between portable contracts, local extensions, optional routing shims, platform surfaces, and tooling. |
| [Source precedence and trust boundaries](sources.md) | Defines portable source classes, trust boundaries, and claim-type conflict handling without a universal override stack. |
| [Artifact contracts](artifacts.md) | Defines the portable durable artifact model, metadata, provenance, evidence-reference, schema, and uncertainty expectations. |
| [Agent-authored output contracts](outputs.md) | Defines portable durable text output categories, output-role boundaries, default precedence, Parent/Child Issue defaults, change-proposal and change-message defaults, and safe structured-body handling. |
| [Workflow contracts](workflows.md) | Defines portable thread roles, bounded handoffs, scope preservation, readiness reporting, and the change lifecycle. |
| [Validation contracts](validation.md) | Defines the portable validation claim model, status vocabulary, evidence requirements, and success-claim rules. |
| [Evidence-packing contracts](evidence-packing.md) | Defines the tool-neutral boundary for packaging evidence without choosing a specific packing tool. |
| [Evaluation contracts](evaluations.md) | Defines concrete reviewable pass/fail cases for predictable contract failures. |
| [Ownership and installer safety](ownership.md) | Defines source-owned portable payload, consumer-owned local context, missing-only seeding, vendor shim boundaries, and installer behavior. |

## Installed Shape

The public installer is the root `install.sh`. It resolves the configured source
channel, defaulting to `main`, to a full commit SHA, downloads one source archive
for that resolved commit, and applies the repository's payload boundaries.

Source-owned portable payload:

```text
AGENTS.md
docs/agent-context/**
```

Consumer-owned local context:

```text
docs/project/**
```

Missing-only seed payload:

```text
payload/missing-only/**
```

The installer overwrites the source-owned portable payload from the resolved
source commit on each run. It seeds files from `payload/missing-only/**` only
when the mirrored destination file is absent. Existing consumer-owned local
context and existing vendor instruction files are preserved.

## Ownership Boundary

Portable files in this directory own reusable collaboration contracts only. They
MUST NOT own repository identity, local source maps, local validation commands,
secrets policy details, platform collaboration templates, optional vendor shim
content, installer implementation details, or portability-lint implementation
behavior except where a contract explicitly defines a boundary for those topics.

Later detailed contracts should extend the specific file that owns their topic.
They should add narrow normative sections instead of duplicating rules across the
contract set.

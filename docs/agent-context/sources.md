# Source Precedence And Trust Boundaries

This document defines portable source classes and trust boundaries for agent
collaboration. It helps agents decide which sources control scope, which sources
support factual claims, which sources provide local policy, and which sources
are derived or transient evidence.

Source precedence is not one universal override stack. Agents MUST resolve
conflicts by claim type, ownership layer, freshness, and evidence quality.

## Terms

- **Source class**: a category of input, artifact, contract, or observation with
  a specific ownership layer and trust boundary.
- **Claim type**: the kind of decision or assertion being made, such as scope
  control, repository fact, local policy, routing-shim or platform-surface
  mapping, validation status, or derived evidence reuse.
- **Current inspected state**: source files, diffs, rendered artifacts, command
  output, CI results, or other observable state that was inspected for the
  active task at a known observation point.
- **Collaboration artifact**: an issue, pull request, review comment, handoff,
  prompt, maintainer confirmation, or similar durable collaboration record.
- **Derived evidence**: a generated pack, summary, snapshot, transcript, or
  tool-produced output that represents other sources through selection,
  transformation, compression, or narration.
- **Transient conversation context**: conversation text, scratch notes,
  intermediate tool output, memory, or reasoning that has not been captured as a
  durable artifact with provenance and limitations.

## Source Classes

| Source class | May decide or support | Trust boundary |
| --- | --- | --- |
| External controlling instructions from the execution environment | Active execution behavior, tool permissions, safety limits, and current-turn constraints that are not owned by the repository. | These instructions control the current run but do not become portable repository doctrine. Portable files MUST NOT encode tool-specific runtime behavior as a reusable baseline; when such behavior must be documented, it belongs to the owning local extension, vendor shim, consumer-owned platform surface, or tooling layer. |
| Current inspected repository state and inspected artifacts | Factual claims about files, diffs, repository content, rendered output, validation output, and artifact contents as observed. | This is the factual baseline for files, validation, and repository content. It does not by itself authorize out-of-scope changes. Freshness, coverage, and observation limits MUST be reported when material. |
| Portable contracts under `docs/agent-context/**` | Reusable role, artifact, output, workflow, validation, evidence, source, evaluation, ownership, and safety boundaries. | Portable contracts MUST remain repository-agnostic and vendor-agnostic. They do not own local identity, local commands, vendor shim content, platform surface content, or execution-environment behavior. |
| Consumer-owned local extensions under `docs/project/**` or a configured local extension path | Repository identity, local surfaces, validation commands, workflow exceptions, local policy, and sensitive-data handling details. | Local extensions may specialize local policy. They MUST NOT silently replace portable role, validation, ownership, artifact, evidence, installer-safety, or source-boundary rules. Missing local extension files mean local facts are unknown. |
| Vendor routing shims and consumer-owned platform surfaces | Mapping durable portable and local rules into a routing file, platform-native form, template, or tool surface. | Missing-only vendor shims route readers to portable and local context without becoming durable doctrine. Consumer-owned platform surfaces may specialize local workflow. Neither layer may replace portable contracts or invent local facts. |
| Collaboration artifacts | Active scope, review requests, maintainer decisions, acceptance criteria, handoff boundaries, and evidence pointers. | These artifacts are scope, review, or confirmation evidence. Issue bodies, pull request bodies, prompts, review comments, and handoffs are not proof that current files or validation state still match. Maintainer confirmation supports only the exact confirmed claim. |
| Generated evidence packs, summaries, snapshots, and transcripts | Bounded supporting evidence, source discovery, provenance, review context, and validation support when metadata is sufficient. | Derived evidence MUST identify freshness, source references, included and omitted surfaces, generation or observation point, and limitations before reuse for material claims. Stale or incomplete derived evidence cannot replace fresher direct evidence. |
| Transient conversation context | Immediate clarification, short-lived coordination, and candidate evidence to materialize elsewhere. | Transient context is not a durable artifact and MUST NOT be reused as factual proof, validation evidence, or local policy unless the relevant claim is captured with provenance and limitations in the owning artifact or contract layer. |

## Conflict Resolution By Claim Type

Agents MUST first identify the claim type, then apply the source class that owns
that kind of decision. A source that is strong for one claim type may be weak or
irrelevant for another.

| Claim type | Governing source boundary | Required handling |
| --- | --- | --- |
| Scope control | Active user or maintainer direction, accepted issue or change scope, review request, handoff, and portable workflow role boundaries. | Use scope sources to decide what may change. Current inspected state may reveal contradictions or blockers, but it MUST NOT broaden scope by itself. Report contradictions before expanding work. |
| Factual claims about files, validation, repository content, or artifact contents | Current inspected state, current diffs, observed command output, CI evidence, rendered artifact evidence, or explicit maintainer confirmation. | Prefer fresh direct evidence over collaboration text, generated summaries, old transcripts, or memory. If direct evidence is missing, report factual uncertainty or use the validation status vocabulary when the claim is a validation claim. |
| Local policy and operational facts | Materialized project extension files or explicit maintainer confirmation for the affected repository. | Apply local policy only within portable boundaries. If local policy conflicts with portable role, validation, ownership, or safety rules, report the contradiction and preserve the portable boundary until an explicit scoped change resolves it. |
| Routing-shim and platform-surface mapping | Vendor shim text, consumer-owned platform surface text, and relevant local extension policy. | Use these layers to translate durable rules into platform or tool surfaces. Do not treat shim wording, template text, labels, or platform mechanics as portable-core doctrine. |
| Validation claims | The validation claim model and status vocabulary in [validation.md](validation.md), supported by observed evidence or exact maintainer confirmation. | Do not mark validation `passed` from expectation, checkbox state, issue text, handoff text, generated summary, or uninspected tool output. Evidence must support the exact subject and status claimed. |
| Derived evidence reuse | The artifact rules in [artifacts.md](artifacts.md), evidence-pack rules in [evidence-packing.md](evidence-packing.md), and this contract's derived-evidence boundary. | Reuse derived evidence only for its stated subject, observation point, included surfaces, and limitations. If it conflicts with current direct evidence, report the conflict and use the direct evidence for factual claims. |
| Ownership and installer-safety decisions | The ownership and installer safety rules in [ownership.md](ownership.md), plus current file evidence when relevant. | Do not infer ownership from convenience, vendor shim presence, platform surface presence, old snapshots, or similar-looking files. Preserve consumer-owned and missing-only files unless the ownership contract permits creation or source-owned replacement. |

## Current Inspected State Baseline

Current inspected state is the factual baseline for repository files, validation
results, diffs, rendered artifacts, and repository content. Before editing,
reviewing readiness, or making validation claims, agents MUST inspect the
current state that materially affects the active task.

If a collaboration artifact, generated pack, summary, transcript, or previous
conversation says that a file, check, artifact, or repository state has a
particular value, the agent MUST treat that statement as a pointer until current
direct evidence or exact maintainer confirmation supports it.

When current inspected state contradicts active scope evidence, agents MUST:

1. preserve the active scope boundary;
2. use the current direct evidence for factual claims;
3. report the contradiction and its effect on scope, validation, or readiness;
4. proceed only with unaffected work where scope and evidence remain clear.

## Collaboration Artifacts

Collaboration artifacts help agents understand intent, scope, review history,
and prior decisions. They are especially useful for deciding what evidence to
inspect next.

Agents MUST NOT treat an issue body, pull request body, review comment, prompt,
or handoff as proof that current repository files, generated artifacts,
validation results, or external state still match the artifact. These records
MAY support scope, review, or acceptance decisions only within their stated
subject and freshness limits.

Maintainer confirmation is stronger than ordinary collaboration text for the
claim it explicitly confirms. It MUST NOT be generalized to unrelated files,
checks, artifacts, future states, or local policies.

## Generated And Derived Evidence

Generated packs, summaries, snapshots, and transcripts are derived evidence.
They MAY be useful for orientation, provenance, source discovery, handoffs,
validation support, or review when they satisfy the relevant artifact and
evidence-packing contracts.

Derived evidence that supports a material claim MUST make the following clear:

- the subject or question it covers;
- the source references or source classes used;
- the observation or generation point;
- the included and omitted surfaces;
- freshness, redaction, and access limits;
- known uncertainty, unsupported claims, and residual risks.

When this metadata is missing, the derived evidence MAY be used as a lead for
inspection, but it MUST NOT be used as proof of current file contents,
validation status, local policy, or portable doctrine.

## Local Extension And Portable Boundary

Project-local extension facts may specialize the repository's local policy,
including local source maps, command choices, workflow exceptions, secrets
handling, release requirements, vendor shim preferences, or platform surface
policy.

They MUST NOT silently replace portable contracts that define:

- thread roles and handoff boundaries;
- validation statuses and success-claim rules;
- durable artifact provenance and limitation expectations;
- agent-authored output role and safe body handling expectations;
- evidence-pack freshness, omission, and redaction expectations;
- ownership and installer-safety rules;
- vendor shim and platform-surface routing boundaries;
- portable source-class conflict handling.

If a local extension appears to conflict with one of those portable boundaries,
agents MUST report the contradiction. They MAY proceed only where the local
policy and portable boundary can both be honored for the active scope.

## Routing Shim And Platform Surface Boundary

Vendor routing shims may route durable rules into agent-specific instruction
files. Platform collaboration surfaces may route durable rules into
platform-native templates, forms, or review surfaces when a consumer repository
chooses to maintain those files.

Vendor shims and platform collaboration surfaces MUST NOT:

- replace the portable contract index as the durable source of portable rules;
- invent local repository facts when the project extension is missing;
- make a tool, platform, model, or generated format a portable baseline;
- weaken project-local sensitive-data or validation boundaries;
- convert template text, labels, platform checkboxes, or routing-shim wording into
  validation proof.

## Boundary Rules

Source-precedence rules own:

- source-class definitions and trust boundaries;
- claim-type conflict handling;
- the rule that current inspected state is the factual baseline for files,
  validation, artifacts, and repository content;
- the rule that collaboration artifacts are scope, review, or confirmation
  evidence rather than proof of current source state;
- the rule that generated packs, summaries, snapshots, and transcripts are
  derived evidence with freshness and limitation requirements;
- the rule that local extensions specialize local policy without silently
  replacing portable boundaries;
- the rule that vendor shims and platform collaboration surfaces map durable
  rules without becoming durable portable doctrine.

Source-precedence rules MUST NOT own:

- detailed handoff formats, role responsibilities, or change lifecycle rules;
- artifact schemas or metadata fields beyond source-class trust boundaries;
- validation status semantics or project-local validation commands;
- evidence-packing implementation behavior or tool-specific generated formats;
- vendor shim payload syntax, platform templates, labels, or
  runtime behavior;
- project-local identity, source maps, commands, branch rules, release policy, or
  secrets policy details;
- installer implementation behavior, portability-lint rules, or copy
  algorithms;
- agent-authored output artifact formats.

## Extension Path

Later source-precedence work SHOULD extend this file when adding portable source
classes, trust boundaries, or claim-type conflict rules. Topic-specific details
SHOULD remain with their owning contracts: workflows in
[workflows.md](workflows.md), artifacts in [artifacts.md](artifacts.md),
agent-authored outputs in [outputs.md](outputs.md), validation in
[validation.md](validation.md), evidence packing in
[evidence-packing.md](evidence-packing.md), ownership in
[ownership.md](ownership.md), and local policy under `docs/project/**` or the
configured local extension path.

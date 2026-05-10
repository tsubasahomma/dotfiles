# Evidence-Packing Contracts

This document defines the portable, tool-neutral contract for preparing bounded
evidence that agents, maintainers, workers, reviewers, and evaluators may use
during collaboration.

Evidence packing is about collecting and describing relevant source evidence in
a reviewable way. It does not require any context-packing tool, generated pack
format, vendor shim, platform surface layer, command line, or repository-local
workflow.

## Terms

- **Evidence pack**: a bounded evidence artifact that collects or summarizes
  source material for a stated subject and intended consumer.
- **Evidence producer**: the role, person, agent, process, or tool that creates
  or updates an evidence pack.
- **Evidence consumer**: the role, person, agent, process, evaluator, local
  surface layer, or tool expected to use the pack.
- **Observation point**: the time, source revision, artifact revision, command
  result, retrieval point, or manual inspection point represented by evidence.
- **Source reference**: a pointer to source material, inspected state,
  generated output, command output, CI result, artifact, or maintainer
  confirmation used by the pack.
- **Surface**: a source, artifact, generated-output, sensitive, or external
  area that the producer intentionally included, omitted, or marked
  unavailable.
- **Freshness**: the relationship between the evidence observation point and
  the current state a consumer wants to reason about.
- **Redaction**: masking, summarizing, aggregating, or omitting sensitive
  material while preserving enough safe context for review.

## Purpose

Evidence packs help consumers inspect bounded context without replaying an
unbounded conversation or planning history. A pack SHOULD make it easier to
understand what was observed, why it was relevant, what was omitted, and what
limits apply.

An evidence pack MAY support:

- artifact evidence references under [artifacts.md](artifacts.md);
- generated evidence-pack summaries under [outputs.md](outputs.md);
- validation claims and evidence summaries under [validation.md](validation.md);
- worker and evaluator handoffs under [workflows.md](workflows.md);
- manual review, readiness review, or follow-up planning;
- project-local workflows or consumer-owned surfaces that choose to use a
  packing tool.

## Non-Purpose

Evidence packs are supporting evidence, not automatic proof of current source
state. A consumer MUST NOT treat a pack as current fact when the relevant source,
artifact, generated output, external source, or validation result may have
changed after the observation point. Claim-type conflict handling for source
classes is defined in [sources.md](sources.md).

An evidence pack MUST NOT be used as:

- a replacement for re-inspecting current evidence when a workflow contract
  requires re-inspection;
- a validation report unless it also satisfies the validation claim model in
  [validation.md](validation.md);
- a durable artifact unless it satisfies the artifact model in
  [artifacts.md](artifacts.md);
- an unbounded planning transcript or memory dump;
- a place to store secrets, private data, or unrestricted sensitive output;
- a portable-core requirement to use a specific context-packing tool.

## Scope Boundaries

An evidence pack MUST have a bounded subject. The subject SHOULD be narrow
enough that a later consumer can tell which claims, files, artifacts,
requirements, or surfaces the pack supports.

An evidence pack SHOULD include only evidence that is relevant to its stated
subject and intended consumer. It MUST NOT include broad repository snapshots,
planning history, unrelated tool output, or private local context merely because
the material is available.

When a consumer needs repository-local identity, source maps, validation
commands, workflow exceptions, or secrets policy, those facts belong in a
materialized project extension such as `docs/project/**`. Portable evidence
rules define how to describe evidence safely; they do not own local source maps
or local policy.

Tool-specific collection, serialization, compression, filtering, or prompt
formatting belongs in a project-local, platform-surface, vendor-shim, or tooling
layer and MUST NOT become portable-core doctrine.

## Minimum Metadata

Every evidence pack MUST make the following metadata available either directly
in the pack, in an adjacent manifest, or in the durable report that references
the pack:

| Metadata | Requirement |
| --- | --- |
| `subject` | States the bounded question, work item, artifact, source state, or review target the pack supports. |
| `producer` | Identifies the producing role, process, or tool at the level needed for review without requiring personal or host-specific identity in portable core content. |
| `observation_point` | Records when or where the evidence was observed, such as a source revision, artifact revision, command result point, retrieval point, or manual inspection point. |
| `source_refs` | Lists the source references used by the pack. File references SHOULD be repository-relative when possible. |
| `included_surfaces` | Names the source, artifact, generated-output, sensitive, or external surfaces intentionally included. |
| `omitted_surfaces` | Names known relevant surfaces omitted from the pack and why they were omitted. |
| `redaction_notes` | Describes sensitive-data handling, masking, summary, omission, or confirmation limits. |
| `freshness` | States whether the evidence is current as of the observation point, potentially stale, stale, or freshness unknown. |
| `limitations` | States partial coverage, unavailable evidence, unsupported claims, uncertainty, and residual risks. |
| `intended_consumer` | Names the role, person, agent, process, evaluator, local surface layer, or tool expected to use the pack. |

Machine-consumed packs SHOULD use structured fields with stable names. Narrative
packs MAY use prose or tables when every required metadata item remains explicit
and reviewable.

## Relationship To Artifacts And Validation

Evidence packs MAY be durable artifacts. When an evidence pack is preserved as a
durable artifact, it MUST satisfy the artifact metadata, provenance, evidence
reference, audience, and limitation expectations in [artifacts.md](artifacts.md).

Artifact evidence references MAY point to an evidence pack when the pack is the
source material or summary supporting the artifact claim. The reference SHOULD
identify the pack locator, observation point, relevant subject, and limitations.

Validation claims MAY reference evidence packs as validation evidence only when
the pack directly supports the claim. A validation claim MUST still use the
status vocabulary and evidence requirements in [validation.md](validation.md).
The existence of a pack does not make a claim `passed`; the claim status depends
on the observed evidence, subject coverage, freshness, and limitations.

If an evidence pack contains only partial, stale, redacted, unavailable, or
generated evidence, validation claims MUST report that limitation using
`failed`, `pending`, `skipped`, `not_required`, `maintainer_confirmed`, or a
scoped `passed` claim as appropriate. Missing or limited evidence MUST NOT be
reported as complete success.

## Relationship To Handoffs

Evidence packs MAY support worker and evaluator handoffs by giving recipients a
bounded set of evidence pointers and summaries. They MUST NOT become unbounded
planning transcripts.

A worker handoff MAY reference an evidence pack for current contracts,
artifacts, diffs, source state, prior decisions, or validation reports that
should guide inspection. The worker MUST still re-inspect current evidence
before editing when the workflow contract requires it.

An evaluator handoff MAY reference an evidence pack for the artifact or change
under review, relevant state, acceptance criteria, validation evidence, known
risks, or disputed assumptions. The evaluator MUST treat the pack as supporting
evidence for the exact evaluation question, not as authority over unrelated
history.

Handoff-oriented evidence packs SHOULD summarize only the decisions, source
state, boundaries, and risks needed for the recipient role. They SHOULD link or
point to durable evidence when more detail is needed instead of copying broad
history into the pack.

## Evidence State Rules

Evidence packs MUST represent evidence state honestly:

| Evidence state | Required handling |
| --- | --- |
| Stale evidence | Mark the evidence stale when the source may have changed after the observation point. State what must be re-inspected before relying on it. |
| Partial evidence | State the covered and uncovered surfaces. Do not imply complete coverage. |
| Unavailable evidence | State what evidence was expected, why it is unavailable, and whether the missing evidence blocks the intended claim. |
| Redacted evidence | State what kind of material was redacted, the redaction method at a safe level, and the effect on reviewability. |
| Generated evidence | Identify the source or generation process when known. State whether generated output was inspected directly, regenerated, or only referenced. |
| Tool-produced evidence | Identify the producing tool or process at a safe level, the observation point, and known limitations. Do not treat tool output as proof without source or validation support. |

Evidence generated by a tool, model, script, vendor shim, or platform surface
MUST be treated as an artifact or evidence source with provenance and
limitations. Consumers SHOULD verify material claims against source state or
validation evidence when the claim affects implementation, review, readiness, or
safety.

## Secret And Sensitive-Data Boundaries

Evidence packs MUST avoid exposing secrets and sensitive data. They MUST NOT
include actual secrets, tokens, credentials, private keys, passwords, recovery
material, unredacted private personal data, or unredacted regulated data.
Production data samples MUST be omitted unless a project-local policy explicitly
allows a safe redacted form.

When a material evidence source contains sensitive data, the producer MUST use a
safe handling option:

- omit the sensitive material and report the omission;
- redact or mask the sensitive values;
- summarize or aggregate the evidence without exposing restricted content;
- reference maintainer confirmation when direct evidence cannot be shared;
- mark the evidence unavailable, pending, skipped, or limited when safe handling
  is not possible.

Project-local secrets policy belongs in the project extension, commonly under
`docs/project/**` when materialized. Evidence packs MUST preserve that local
policy when present. When local policy is missing or incomplete, producers MUST
use conservative redaction and report the missing policy as a limitation instead
of guessing.

Vendor shims, platform surfaces, and tools MUST NOT weaken project-local
redaction boundaries. A tool-produced pack that cannot preserve required
redactions MUST be treated as unsafe for the affected surfaces.

## Tool-Neutral Core Boundary

No context-packing tool is required by portable core. Consumers MAY use manual
summaries, repository inspection, generated reports, or a project-approved
tooling workflow when those choices preserve the metadata, scope, freshness,
redaction, limitation, artifact, validation, and handoff rules in this contract.

Portable core MUST NOT prescribe:

- a required packing tool;
- a required generated pack file name;
- command-line invocations or runtime requirements;
- token budgets or model-specific context limits;
- vendor shim or platform surface prompt syntax or configuration;
- local source-surface maps or local secrets policy.

Those details belong to project-local extensions, vendor shim or platform
surface documentation, or tooling owned by the relevant layer.

## Boundary Rules

Evidence-packing contracts own:

- bounded evidence-pack purpose and non-purpose;
- minimum metadata for source, scope, freshness, redaction, limitations, and
  intended consumers;
- the rule that packs support artifacts, validation claims, and handoffs without
  replacing their governing contracts;
- stale, partial, unavailable, redacted, generated, and tool-produced evidence
  handling;
- the rule that packs are supporting evidence, not automatic proof of current
  source state;
- the rule that portable core does not require a context-packing tool.

Evidence-packing contracts MUST NOT own:

- required packing tools, command lines, generated file formats, or optional
  payloads;
- generated evidence-pack summary output shape beyond the evidence metadata this
  contract requires;
- project-local source maps, validation commands, secret handling procedures, or
  context budgets;
- detailed workflow handoff contracts beyond how packs support them;
- vendor shim or platform surface behavior for any context-packing tool;
- installer implementation behavior or copy decisions;
- evaluation cases, fixtures, scoring rubrics, datasets, or lint
  implementation.

## Extension Path

Later evidence-packing work SHOULD extend this file only when adding portable,
tool-neutral rules that apply across producers and consumers. Tool-specific
packing behavior should live in project-local, vendor-shim, platform-surface, or
tooling layers.
Project-local evidence sources, surfaces, validation commands, and secrets
policy should live in `docs/project/**`.

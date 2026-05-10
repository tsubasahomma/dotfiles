# Artifact Contracts

This document defines the portable artifact model for durable outputs produced,
reviewed, or consumed during agent collaboration.

Portable artifact rules describe what must be true of durable artifacts without
embedding repository identity, local commands, host details, secret-adjacent
facts, vendor shim payloads, platform surface payloads, or installer state.

## Terms

- **Durable artifact**: an intentional output that is preserved, reviewable, and
  reusable beyond the immediate conversation turn or tool invocation.
- **Transient conversation context**: chat messages, scratch notes, exploratory
  tool output, intermediate reasoning, or temporary state that has not been
  captured as a durable artifact with metadata and evidence references.
- **Artifact producer**: the person, agent, process, or tool that creates or
  updates an artifact.
- **Artifact consumer**: the person, agent, process, tool, vendor shim,
  platform surface, evaluator, or local workflow that relies on an artifact.
- **Evidence reference**: a pointer to source material, inspected state,
  validation output, or maintainer confirmation that supports an artifact claim
  without requiring the artifact to embed all source material.

## Durable Artifact Model

A durable artifact MUST be distinguishable from transient conversation context.
It MUST be intentionally named, stored, or reported in a form that later
consumers can inspect without replaying the full conversation that produced it.

Durable artifacts MAY include:

- portable contract documents;
- project-local extension documents;
- vendor routing shims and consumer-owned platform surface payloads;
- agent-authored durable text outputs governed by [outputs.md](outputs.md);
- validation reports and validation claim sets;
- evidence summaries or evidence packs;
- evaluation reports;
- installer validation reports or installer diagnostics.

This model describes the portable expectations shared by those artifact kinds.
It does not make every artifact portable core content. The artifact boundary is
defined by the artifact's ownership layer:

| Ownership layer | Artifact responsibility |
| --- | --- |
| Portable core | Reusable contract rules and artifact metadata expectations. |
| Project-local extension | Repository-local artifact names, storage conventions, validation commands, and operational facts. |
| Vendor shim or platform surface | Platform-specific or tool-specific payload shape, template format, and routing or collaboration files. |
| Installer diagnostics | Source channel, resolved commit, copied payload class, skipped missing-only files, and validation evidence for installer behavior. |
| Evidence-packing tooling | Tool-specific collection, serialization, compression, or packing behavior. |

Transient conversation context MAY inform an artifact, but it MUST NOT be treated
as a durable artifact until the relevant claims, provenance, limitations, and
evidence references are captured in a durable location or report.

## Required Portable Metadata

Every durable artifact MUST make the following metadata available either
directly or through an owning layer that consumers can inspect, such as the
artifact body, an adjacent manifest, an owning index, a validation report, or a
change record:

| Metadata | Requirement |
| --- | --- |
| `artifact_id` or stable locator | Identifies the artifact for later reference. It MUST be stable within the artifact set and MUST NOT rely on host-absolute paths. |
| `artifact_kind` | Identifies the artifact category or ownership layer. Extension-specific kinds SHOULD be namespaced by their owning layer. |
| `schema_version` or governing contract | Identifies the schema or contract version the artifact follows. Narrative artifacts without a machine schema MUST still identify the governing contract or document set when practical. |
| `title` or purpose statement | States what the artifact is for. |
| `intended_consumers` | Names the expected audience or consumer classes. |
| `producer` | Identifies the producing role, process, or tool at the level needed for review without requiring personal or host-specific identity in portable core files. |
| `created_or_updated` | Provides enough freshness information for consumers to judge whether the artifact may be stale. |
| `provenance` | Summarizes the inputs, transformations, and decisions that shaped the artifact. |
| `evidence_refs` | Points to the source evidence that supports material claims. |
| `limitations` | States known limits, exclusions, uncertainty, and residual risks. |
| `validation_refs` | Points to validation claims or reports when validation exists or is required. |

Metadata MAY be represented as front matter, structured fields, a table, prose,
or an external manifest. Machine-consumed artifacts SHOULD use structured fields
with stable names. Human-consumed narrative artifacts MAY use prose when the same
information remains clear and reviewable.

Portable core files MUST NOT add repository-local identifiers, maintainer
identifiers, host-absolute paths, local command lines, secrets policy details, or
vendor-specific baseline assumptions merely to satisfy metadata fields. When
such details are necessary, they belong in a project-local extension, vendor
shim, platform surface, validation report, or installer diagnostic owned by that
layer.

## Schema And Version Expectations

Artifacts with machine-consumed structure MUST declare a `schema_version`.
Consumers MUST NOT infer a structured schema version from file name alone.

Schema versions MUST have clear compatibility meaning:

- additive optional fields MAY be introduced without invalidating older
  consumers when the schema says unknown fields are allowed;
- renamed, removed, or semantically changed required fields MUST use a new
  schema version;
- consumers SHOULD preserve unknown fields unless the schema explicitly permits
  dropping them;
- consumers MUST fail safely or mark the artifact unsupported when a required
  schema version is unknown;
- artifacts SHOULD record the artifact revision or update point separately from
  the schema version when both matter.

Portable contracts MAY define shared schemas. Project-local extensions, vendor
shims, platform surfaces, installer tools, and evidence-packing tools MAY define
their own schemas, but those schemas MUST NOT be treated as portable core
doctrine unless a portable contract explicitly adopts them.

## Audience And Consumer Expectations

An artifact MUST state who or what is expected to consume it. The consumer
description SHOULD be specific enough to prevent accidental reuse outside the
artifact's scope.

Artifact consumers MAY rely only on claims that are:

1. within the artifact's stated purpose;
2. supported by provenance and evidence references when evidence is required;
3. not contradicted by the artifact's limitations or validation claims;
4. within the ownership layer that produced the artifact.

When artifact claims conflict with current source evidence or another ownership
layer, consumers SHOULD apply the source-class and claim-type boundaries in
[sources.md](sources.md).

An artifact MUST NOT imply that vendor shim, platform-surface, project-local, or
installer behavior is portable merely because the artifact references the
portable core.

## Provenance Expectations

Artifact provenance MUST describe the origin of material claims at the level
needed for review. It SHOULD include:

- source artifacts, source files, or source evidence used;
- whether the artifact was created from inspection, transformation, generation,
  maintainer confirmation, or a combination of sources;
- the relevant freshness or observation point;
- important assumptions, exclusions, or unresolved questions;
- material transformations between source evidence and artifact content.

Provenance MUST NOT require consumers to trust unsupported conversation memory.
If a claim depends on observed evidence, the artifact MUST reference that
evidence or state that evidence is missing, pending, unavailable, or outside
scope.

## Evidence Reference Expectations

Evidence references connect durable artifacts to the observations that support
them. They SHOULD be concise and stable. They MUST avoid embedding unrelated
source material or secret-adjacent details.

An evidence reference SHOULD identify:

- an evidence reference identifier;
- the evidence kind, such as command output, inspected state, CI result, manual
  review, maintainer confirmation, source artifact, or external source;
- the artifact or source locator, using repository-relative paths for files when
  possible;
- the observation or retrieval point when freshness matters;
- a short summary of what the evidence supports;
- any access, redaction, or freshness limitation that affects reuse.

Evidence references are pointers, not evidence-packing instructions. Tooling for
collecting, compressing, redacting, or serializing evidence belongs to the
evidence-packing contract or the relevant project-local, platform-surface, or
tooling layer.

## Limitations And Uncertainty

Artifacts MUST state material limitations and uncertainty. A limitation is
material when a consumer could make a different decision if they knew it.

Artifacts SHOULD report:

- unverified assumptions;
- unavailable evidence;
- stale or potentially stale source material;
- failed, skipped, pending, or not-required validation;
- maintainer confirmation that covers only part of the artifact;
- known residual risks.

Artifacts MUST NOT omit limitations in order to make a result appear more
certain. Missing validation MUST be represented through the validation vocabulary
in [validation.md](validation.md), not described as success.

## Boundary Rules

Portable artifact rules own durable metadata, provenance, evidence-reference,
audience, schema, and uncertainty expectations.

Portable artifact rules MUST NOT own:

- agent-authored output categories, output-role boundaries, or structured-body
  handling;
- project-local artifact storage paths, naming conventions, release procedures,
  validation commands, or operational facts;
- vendor shim or platform surface template syntax, platform fields, copied
  payloads, or runtime behavior;
- installer implementation details such as archive download mechanics, copy
  algorithms, or diagnostic output format;
- evidence-packing implementation behavior;
- detailed workflow roles, handoff formats, or orchestration rules;
- evaluation cases, fixtures, scoring rubrics, or datasets.

Project-local conventions belong in `docs/project/**`. Vendor shim and platform
surface artifacts belong with their owning consumer layer. Installer ownership
behavior belongs to [ownership.md](ownership.md).
Evidence-packing behavior belongs in [evidence-packing.md](evidence-packing.md)
or a tool-specific layer.
Agent-authored durable text output rules belong in [outputs.md](outputs.md).

## Extension Path

Later artifact work SHOULD extend this file only when adding portable rules that
apply across artifact producers and consumers. Layer-specific artifacts SHOULD
extend the document owned by that layer instead of duplicating portable rules.

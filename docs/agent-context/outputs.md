# Agent-Authored Output Contracts

This document defines portable expectations for durable text that agents author
or update during collaboration. The goal is reviewable, evidence-backed output
that can move across roles without becoming repository-local policy.

These defaults are not mandatory platform templates. Within the portable
contract boundaries, they apply when no project-local output policy or
consumer-owned platform surface provides a more specific rule.

## Terms

- **Agent-authored output**: durable text created or updated by an agent for a
  collaboration, review, implementation, validation, or evidence-routing
  purpose.
- **Output role**: the job an output is meant to perform, such as governing
  scope, proposing a change, naming a source change, reporting validation, or
  transferring worker scope.
- **Parent Issue body**: a durable work item body that governs a larger program,
  objective, or accepted direction. The word "issue" is generic and does not
  require a specific tracker.
- **Child Issue body**: a durable work item body that bounds one
  self-contained implementation, review, or documentation change under a parent
  scope.
- **Change-proposal body**: a reviewable body for a pull request, patch
  proposal, change list, or equivalent source-change review surface.
- **Change message**: a commit, changeset, or version-control message that
  names a source change and, when useful, records rationale, risk, validation,
  or other durable context.
- **Structured body**: long or field-sensitive text whose line breaks, headings,
  lists, code blocks, or machine-consumed fields are material to correct use.
- **Safe artifact boundary**: a body file, standard input stream, structured API
  field, platform surface-owned field, or equivalent mechanism that preserves a
  structured body without fragile inline quoting or command construction.
- **Static body claim**: a durable claim recorded in text at a specific
  observation point. It may become stale when repository state, validation
  results, review state, deployment state, or external state changes.

## Default Precedence

Portable output defaults define reusable behavior and review expectations. They
do not own local workflow policy.

Project-local policy MAY specialize output shape within portable source,
artifact, workflow, validation, evidence-packing, and ownership boundaries. It
MUST NOT replace those boundaries or make local facts portable.

When project-local output policy exists, it MAY specialize:

- concrete headings and required fields;
- issue references, closure syntax, and tracker conventions;
- commit subject conventions, trailers, and Conventional Commits decisions;
- merge-message policy and release-note policy;
- reviewer assignment, labels, milestones, checkboxes, and other
  platform-surface mappings;
- local safe-body mechanisms for posting or storing structured text.

Project-local policy belongs under `docs/project/**`, with
`docs/project/output-policy.md` as the default local output-policy location.
Consumer-owned platform surfaces are optional and are not installed by default.
They may map local fields into platform-native forms, but they do not become
portable core doctrine.

Static durable output bodies MUST NOT claim dynamic review, CI, deployment, or
external status as always-current truth. They may report observed evidence and
the observation point, or they may point to the dynamic system that owns the
current status.

Durable repository documentation SHOULD describe steady-state behavior for its
owning layer. Historical process context belongs in issue bodies, change
proposals, change messages, validation reports, or other change records unless
it is required for current operation.

## Output Categories

Agent-authored output categories include, but are not limited to:

| Output category | Portable purpose | Primary consumers |
| --- | --- | --- |
| Parent Issue body | Governs a larger objective, decisions, child scope, acceptance criteria, validation expectations, and open risks. | Maintainers, planners, orchestrators, workers, evaluators. |
| Child Issue body | Defines one self-contained work item with explicit scope, boundaries, required changes, dependencies, acceptance criteria, and validation expectations. | Workers, reviewers, maintainers, orchestrators. |
| Change-proposal or pull request body | Presents a reviewable evidence packet for a proposed change without becoming platform doctrine. | Reviewers, maintainers, orchestrators, platform surfaces. |
| Commit or version-control change message | Names a source change concisely and, when useful, records rationale, risk, validation, or discarded alternatives. | Maintainers, reviewers, history readers, release tooling. |
| Change summary | Summarizes what changed, why it changed, and what evidence supports the summary. | Maintainers, reviewers, later agents, release or readiness consumers. |
| Worker prompt | Transfers bounded implementation scope, evidence pointers, constraints, validation expectations, and deliverables. | Worker Threads or equivalent implementation roles. |
| Evaluator prompt | Transfers the exact review question, artifact under review, criteria, validation evidence, and known risks. | Evaluator Threads or equivalent review roles. |
| Review finding | Reports a defect, risk, unsupported claim, missing validation, or non-finding against explicit evidence and criteria. | Authors, reviewers, maintainers, orchestrators. |
| Validation report | Records validation claims with the portable status vocabulary and evidence references. | Maintainers, reviewers, workers, evaluators, release or readiness consumers. |
| Readiness report | Summarizes deliverables, validation claims, residual risks, out-of-scope findings, and next-decision readiness. | Orchestrators, maintainers, reviewers, next-role recipients. |
| Command snippet or command body | Provides command text, invocation intent, or a reusable body for a tool or shell-like interface. | Operators, agents, local surface layers, automation or tooling consumers. |
| Generated evidence-pack summary | Summarizes generated or packed evidence while preserving source, freshness, omission, and limitation metadata. | Workers, evaluators, reviewers, maintainers, evidence consumers. |

These categories may be materialized as files, comments, messages, form fields,
reports, commit metadata, consumer-owned platform surfaces, or other durable
records. The artifact's ownership layer determines whether the output belongs to
portable core, project-local extension, vendor shim, platform surface,
validation, evidence-packing, workflow, or another layer under
[artifacts.md](artifacts.md).

## Minimum Portable Expectations

An agent-authored output MUST make its role clear enough that later consumers do
not need to infer whether it is scope governance, a bounded work item, a change
proposal, a validation claim, a review finding, a handoff, a command body, or a
readiness decision.

When material to the output role, durable text outputs MUST state:

- purpose or output role;
- scope and out-of-scope boundaries;
- available artifact identifiers for the work item, governing scope, change
  proposal, review surface, or equivalent collaboration artifact;
- intended consumer or consumer class;
- evidence basis, inspected-state basis, or source pointers;
- validation status using [validation.md](validation.md) when validation is
  claimed, missing, `skipped`, `pending`, `failed`, `not_required`, or
  `maintainer_confirmed`;
- limitations, uncertainty, unavailable evidence, and residual risks;
- freshness or observation point for claims that may become stale;
- next action or requested decision when the output asks a consumer to act.

An output MAY satisfy these expectations through headings, prose, structured
fields, an adjacent manifest, or the owning artifact contract. Human-readable
outputs SHOULD stay concise enough for review while preserving the evidence
needed to audit material claims later.

An output MUST NOT claim current repository state, validation success, review
state, deployment state, or external state unless the claim is backed by current
inspected evidence, observed validation evidence, exact maintainer confirmation,
or a clearly stated limitation. Source-class boundaries are defined in
[sources.md](sources.md).

Agent-authored comments on collaboration surfaces SHOULD be sparse,
role-specific durable records. When a comment materially affects workflow,
review, validation, or routing, it SHOULD state its purpose or role, evidence
basis, requested decision or next owner, and material limitations. Portable core
does not require every comment to follow a heavy template; exact comment
triggers, fields, and platform placement belong to project-local policy or
consumer-owned platform surfaces.

Generated boilerplate MUST NOT obscure the actual change, work item, evidence,
risk, or requested decision. Empty headings SHOULD be omitted unless a local
policy or platform surface requires them.

## Issue Body Defaults

Issue body defaults are portable guidance for durable scope and work-item
records. They do not prescribe a tracker, milestone, label set, platform form,
assignee rule, branch policy, or closure workflow.

### Parent Issue Body

A Parent Issue body SHOULD support durable scope governance. It SHOULD include
the following sections when material:

- `Goal`: the outcome the parent scope exists to achieve.
- `Background Or Motivation`: why the work matters and what problem or
  opportunity it addresses.
- `Governing Decisions`: accepted constraints, architecture decisions, policy
  decisions, or non-regression requirements that child work must preserve.
- `Non-Goals`: adjacent work, platform behavior, local policy, or refactors
  that are intentionally outside the parent scope.
- `Workstreams Or Child Scope`: the bounded child work items, sequencing
  expectations, or decomposition principles.
- `Acceptance Criteria`: observable conditions for completing the parent scope.
- `Validation Expectations`: evidence expected before readiness or closure can
  be claimed, using the validation contract when claims are reported.
- `Risks And Open Questions`: uncertainty, disputed assumptions, blocked
  decisions, and risks that may affect sequencing or readiness.
- `References`: durable evidence pointers, source documents, prior decisions,
  or related artifacts needed by later consumers.

Parent Issue bodies SHOULD leave local tracker fields, labels, milestones,
closure syntax, and platform routing to project-local policy or consumer-owned
platform surfaces.

### Child Issue Body

A Child Issue body SHOULD preserve one self-contained work item. It SHOULD make
unrelated refactors and hidden scope expansion easy to identify during
implementation and review.

It SHOULD include the following sections when material:

- `Purpose`: the reason this bounded work item exists under its parent scope.
- `Scope`: the accepted behavior, documentation, artifact, or policy change the
  worker owns.
- `Non-Goals`: adjacent work and discovered defects that must be reported
  instead of silently implemented.
- `Required Changes`: the concrete change categories or surfaces expected for
  completion.
- `Ownership Boundaries`: source-owned, project-local, missing-only, vendor
  shim, platform-surface, installer, validation, or evaluation boundaries that
  constrain edits.
- `Dependencies Or Sequencing`: prerequisite decisions, upstream work, blocked
  assumptions, or follow-up routing.
- `Acceptance Criteria`: observable conditions for deciding whether the child
  work item is complete.
- `Validation Expectations`: required validation claims, expected evidence, and
  allowed statuses for unrun or inapplicable validation.
- `References`: parent scope, governing contracts, source evidence, validation
  reports, or maintainer confirmations needed for inspection.

Child Issue bodies SHOULD be sufficient for a worker to re-inspect current
evidence without replaying broad conversation history. They SHOULD NOT require
workers to add transient planning notes, outdated historical explanations, or
unrelated findings to durable repository documentation.

## Change-Proposal Body Default

A change-proposal or pull request body SHOULD be a reviewable evidence packet.
The following shape is a portable default, not a mandatory universal template:

- `Summary`: concise statement of the proposed change and reviewer-relevant
  effect.
- `Motivation`: why the change is needed, what decision it supports, or what
  problem it resolves.
- `Scope`: the accepted work item, affected surfaces, ownership boundaries, and
  important exclusions.
- `Changes`: the material implementation, documentation, artifact, or policy
  changes.
- `Validation`: validation claims using `passed`, `failed`, `pending`,
  `skipped`, `not_required`, or `maintainer_confirmed` with evidence summaries
  and limitations.
- `Risk And Rollback`: residual risks, uncertainty, missing evidence, affected
  consumers, and safe reversal, fallback, or mitigation notes.
- `Review Notes`: reviewer attention points, assumptions, non-obvious
  decisions, or comparison notes.
- `Out Of Scope`: adjacent findings or deferred work that the change does not
  implement.
- `Linked Work`: related work items, handoffs, reports, or evidence pointers.

The body SHOULD include enough local context that future readers are not forced
to replay a conversation transcript. It SHOULD NOT repeat generated boilerplate
when direct prose would make the actual change clearer.

Exact headings, required local fields, closure syntax, labels, checkboxes,
reviewer assignment conventions, release-note fields, and platform template
mapping belong to project extension or consumer-owned platform surfaces.

A static change-proposal body MUST report only validation the producer actually
ran, inspected, or had exactly confirmed. It MUST NOT mirror changing CI,
review, deployment, release, or external status as if the body were an
always-current source of truth.

## Commit Or Change Message Default

An agent-authored commit or version-control change message SHOULD make the
resulting change understandable in history without importing project-local
convention into portable core.

The subject SHOULD:

- describe the resulting change, not the implementation activity;
- be concise, imperative, and useful in history by itself;
- aim for 50 characters or fewer as a soft target, not an absolute validity
  gate;
- include an optional scope or affected surface only when it improves
  reviewability.

When a body exists, it MUST follow a blank line after the subject. Prose body
lines SHOULD wrap around 72 characters where practical. Exceptions are allowed
for URLs, code, diagnostic output, trailers, machine-consumed fields, non-prose
text, and project-local policy.

The body SHOULD explain why the change is needed, why the chosen approach is
appropriate, and any relevant risks, migrations, validation, or discarded
alternatives when those are not obvious from the diff.

Portable core does not require issue-closing syntax, tracker references,
trailers, Conventional Commits, release-note policy, merge-message rules, or
branch-derived message rules. Those conventions belong to project-local policy
or consumer-owned platform surfaces.

Generated message boilerplate MUST NOT obscure the actual change.

## Artifact-Mixing Boundaries

Each durable output SHOULD perform one primary role. It MAY reference related
artifacts, but it MUST NOT merge incompatible roles in a way that makes claims
hard to audit or assigns responsibility to the wrong layer.

| Mixing risk | Required boundary |
| --- | --- |
| Static change-proposal body claims and dynamic CI, review, deployment, or external state. | Record only observed static evidence and freshness. Do not manually mirror changing status as durable truth unless the output states the observation point and limitation. Dynamic status belongs to the platform, validation report, or current inspected evidence. |
| Commit subjects and issue-closing, tracker, or release policy. | Keep the portable commit subject focused on the change. Issue references, closure keywords, release links, trailers, and merge-message policy belong to project extension or consumer-owned platform surfaces. |
| Issue bodies and proof of current repository state. | Issue text may define scope, acceptance criteria, and evidence pointers. It is not proof that current files, checks, or artifacts still match without current inspected evidence. |
| Command text and unrelated narrative. | Keep command snippets or command bodies separate from explanatory prose when copying or execution is expected. Put rationale, warnings, and validation notes outside the command boundary. |
| Review findings and implementation scope. | A finding reports evidence, severity, impact, and suggested direction. It does not authorize unrelated implementation changes or broaden accepted scope. |
| Validation reports and unsupported readiness claims. | A validation report records claim statuses and evidence. Readiness requires the workflow readiness criteria in [workflows.md](workflows.md) and MUST disclose failed, pending, skipped, and residual-risk claims. |
| Worker or evaluator prompts and durable source facts. | Prompts transfer role scope and evidence pointers. Recipients still re-inspect current evidence required by [workflows.md](workflows.md). |
| Generated evidence-pack summaries and direct evidence. | A generated summary may support orientation, but it remains derived evidence under [evidence-packing.md](evidence-packing.md) until source, freshness, omissions, and limitations are explicit. |

When an output needs multiple roles, it SHOULD separate them into distinct
sections or artifacts and identify which contract governs each role.

## Structured Body Handling

Long structured bodies SHOULD pass through a safe artifact boundary when inline
command construction, quoting, escaping, truncation, or field interpolation would
make the output fragile.

Safe boundaries MAY include:

- a body file whose contents are supplied to the relevant operation;
- standard input or another stream that preserves the body exactly;
- a structured API field, form field, or platform surface-owned field;
- a generated artifact referenced by stable locator;
- another project-approved mechanism that preserves line breaks, code fences,
  lists, and structured fields.

Long issue bodies, change-proposal bodies, commit bodies, worker prompts,
evaluator prompts, validation reports, command bodies, generated evidence-pack
summaries, or similar structured text MUST NOT be embedded in a fragile inline
command when quoting or shell interpretation could change the content.

Command snippets and command bodies MUST make the executable or copyable boundary
clear. Explanatory text, warnings, expected output, validation status, and
rollback notes SHOULD be outside the command body unless the command language
itself treats them as comments and the target consumer expects them there.

Portable core does not require a specific command interface, shell, API, or
hosting platform. Concrete local command conventions, vendor shim behavior, and
platform surface mechanisms belong to `docs/project/**` or the relevant
consumer-owned layer.

## Prompt Outputs

Worker prompts and evaluator prompts are durable collaboration artifacts. They
MUST preserve role boundaries from [workflows.md](workflows.md) and source
boundaries from [sources.md](sources.md).

A worker prompt SHOULD identify accepted scope, out-of-scope boundaries,
evidence pointers, required validation, known risks, and deliverables. It MUST
NOT require the worker to trust stale issue text, conversation memory, generated
summaries, or prior command output as current factual proof.

An evaluator prompt SHOULD identify the artifact or change under review,
relevant state references, acceptance criteria, validation evidence, known risks,
and the exact evaluation question. It MUST NOT convert evaluation into
implementation scope unless the role is explicitly reassigned.

## Review Findings

A review finding MUST be tied to evidence and criteria. It SHOULD state:

- the affected artifact, source state, output, or claim;
- the observed problem or non-finding;
- severity, impact, or affected consumer when relevant;
- the evidence reference or inspected-state basis;
- the contract, acceptance criterion, or expectation being applied;
- suggested next action when useful.

A review finding MUST NOT present speculation as fact. If evidence is missing or
uncertain, the finding SHOULD state the limitation or use the appropriate
validation status when the finding concerns validation.

## Validation And Readiness Outputs

A validation report MUST use the claim model and status vocabulary in
[validation.md](validation.md). This output contract may define how validation
text is separated from other roles, but it does not redefine validation
statuses.

A readiness report MUST satisfy the workflow readiness requirements in
[workflows.md](workflows.md). It MAY reference a validation report, change
summary, review finding, or evidence-pack summary, but it MUST NOT claim
readiness from unsupported validation or omitted residual risks.

## Generated Evidence-Pack Summaries

A generated evidence-pack summary is derived evidence. It MUST preserve the
evidence-pack subject, source references, observation point, included and omitted
surfaces, redaction notes, freshness, limitations, and intended consumer required
by [evidence-packing.md](evidence-packing.md).

A generated summary MUST NOT replace direct source inspection, validation
evidence, or maintainer confirmation when the active claim requires those
sources. If the summary is partial, stale, redacted, unavailable, or generated
from incomplete inputs, the output MUST say so.

## Boundary Rules

Agent-authored output contracts own:

- durable text output categories and output-role boundaries;
- portable default precedence for durable text outputs;
- minimum portable expectations for purpose, scope, consumer, evidence basis,
  validation status, limitations, and freshness;
- portable default structures for Parent Issue bodies, Child Issue bodies, and
  reviewable change-proposal bodies;
- portable default expectations for commit or change messages;
- artifact-mixing boundaries for durable text outputs;
- safe structured-body handling for long text;
- output-specific routing to artifact, workflow, validation, evidence-packing,
  and source-precedence contracts.

Agent-authored output contracts MUST NOT own:

- durable artifact metadata fields beyond output-specific expectations;
- detailed validation status semantics or project-local validation commands;
- workflow role responsibilities beyond prompt and report output boundaries;
- evidence-packing tool behavior or generated pack formats;
- concrete issue templates, pull request templates, commit conventions, branch
  naming, issue-reference policy, trailers, merge-message policy, release-note
  policy, command conventions, labels, or review gates;
- vendor shim or platform surface payload syntax, platform-specific fields, or
  runtime behavior;
- project-local identity, local source maps, host paths, commands, secrets
  policy details, or operational facts;
- installer behavior, portability-lint implementation, or evaluation fixtures.

## Extension Path

Later output work SHOULD extend this file when adding portable output
categories, output-role boundaries, safe body handling, or durable text defaults.
Artifact metadata should remain in [artifacts.md](artifacts.md), source
precedence in [sources.md](sources.md), workflow roles and readiness in
[workflows.md](workflows.md), validation statuses in
[validation.md](validation.md), evidence packing in
[evidence-packing.md](evidence-packing.md), ownership in
[ownership.md](ownership.md), and local output policy under `docs/project/**` or
the configured local extension path.

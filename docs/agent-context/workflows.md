# Workflow Contracts

This document defines the portable workflow contract for agent collaboration. It
owns thread roles, bounded handoffs, scope preservation, validation and readiness
reporting, and the change lifecycle at a platform-agnostic level.

Workflow rules describe how collaboration should move from planning to bounded
implementation and review. They do not define project-local procedures,
collaboration-platform templates, vendor shim payloads, platform surface
payloads, tool runtimes, or concrete validation commands.

## Terms

- **Work item**: a bounded unit of accepted scope that can be implemented,
  reviewed, or evaluated without requiring the recipient to replay an unbounded
  planning history.
- **Parent scope**: the larger program, objective, or accepted direction that
  explains why the work item exists.
- **Handoff**: a bounded packet that transfers role-specific scope, evidence
  pointers, constraints, and expected outputs.
- **Scope evidence**: information that establishes what a recipient is being
  asked to do. Scope evidence guides inspection, but it is not proof that the
  current source state still matches the handoff.
- **Evidence pointer**: a concise reference to a source file, artifact, diff,
  validation report, maintainer confirmation, or other inspected state. Evidence
  pointers are not evidence-packing instructions.
- **Readiness report**: a durable summary of deliverables, validation claims,
  residual risks, and remaining decisions for a change or artifact.
  Agent-authored readiness report output boundaries are defined in
  [outputs.md](outputs.md).

## Role Contracts

Thread roles are portable responsibility boundaries. A single person, agent, or
process MAY perform more than one role, but the role boundaries MUST remain clear
in durable handoffs and reports.

### Planning Thread

A Planning Thread owns exploration before implementation scope is accepted.

Responsibilities:

- identify goals, assumptions, constraints, trade-offs, and open questions;
- compare options and recommend design direction;
- shape parent scope and candidate work items;
- define proposed acceptance criteria, boundaries, validation expectations, and
  known risks;
- preserve decisions as durable artifacts or concise evidence pointers when they
  are needed later.

Non-responsibilities:

- making implementation changes for a bounded work item;
- claiming validation success without observed evidence;
- requiring later roles to consume unbounded planning transcripts;
- owning sequencing after the parent scope has been accepted, unless explicitly
  assigned to an orchestration role.

### Orchestrator Thread

An Orchestrator Thread owns sequencing and scope control after parent scope is
accepted.

Responsibilities:

- maintain the relationship between parent scope and bounded work items;
- prepare worker and evaluator handoffs with only the context needed for the
  recipient role;
- preserve accepted scope, out-of-scope boundaries, validation expectations, and
  known risks across role transitions;
- route out-of-scope findings without silently expanding active work;
- synthesize worker and evaluator reports into readiness recommendations and
  follow-up decisions;
- compare completed work against parent-scope acceptance criteria when needed.

Non-responsibilities:

- making unscoped implementation changes;
- rewriting accepted parent scope without a new planning or maintainer decision;
- treating historical planning context as current repository or artifact proof;
- requiring workers or evaluators to consume broad history when a bounded
  handoff would answer the active question.

### Worker Thread

A Worker Thread owns one bounded work item or explicitly bounded change.

Responsibilities:

- re-inspect current evidence before editing;
- compare handoff scope with current source state, artifact state, and governing
  contracts;
- implement only accepted in-scope changes;
- preserve path, artifact, routing surface, and ownership
  boundaries from the governing contracts;
- produce expected deliverables and validation evidence;
- report out-of-scope findings, blocked assumptions, and residual risks without
  silently expanding scope;
- provide a readiness report using the validation vocabulary in
  [validation.md](validation.md).

Non-responsibilities:

- creating, splitting, closing, or redesigning work items unless explicitly
  assigned;
- solving unrelated defects discovered during implementation;
- treating handoff text as factual proof of current source state;
- owning adversarial or readiness evaluation of its own work as the final review
  authority;
- changing project-local files, vendor shims, platform surfaces, installer
  behavior, or evaluation surfaces when the active work item does not include
  them.

### Evaluator Thread

An Evaluator Thread owns adversarial review, evidence checks, and readiness
assessment for a specific artifact, change, or question.

Responsibilities:

- review the artifact or change against the exact evaluation question;
- inspect the relevant diff, source state, artifacts, validation evidence, and
  acceptance criteria provided by the evaluator handoff;
- check whether validation claims use the required status vocabulary and cite
  sufficient evidence;
- identify defects, contradictions, unsupported claims, missing validation, and
  residual risks;
- report readiness, non-readiness, or disputed assumptions without taking over
  implementation scope.

Non-responsibilities:

- implementing the change under review unless explicitly reassigned as a Worker
  Thread;
- rewriting parent scope or active work scope;
- requiring broad historical planning context unless the exact evaluation
  question cannot be answered without it;
- converting out-of-scope findings into active requirements without
  orchestration or maintainer decision.

## Handoff Rules

Handoffs MUST preserve scope without copying unbounded transcripts. A handoff
SHOULD summarize the decision, boundary, or risk that matters and point to the
durable source evidence when later inspection is needed.

A handoff MUST NOT require the recipient to trust stale memory, unsupported
conversation history, or prior tool output as current fact. A handoff is scope
evidence, not factual proof of current repository, artifact, validation, or
external state. Source-class conflicts and claim-type precedence decisions are
routed through [sources.md](sources.md).

Recipients MUST use handoffs to decide what to inspect. They MUST re-inspect
current evidence that affects their role before making changes, reviewing
readiness, or claiming validation success.

When handoff evidence is missing, stale, contradictory, or too broad for the
recipient role, the recipient MUST report the limitation. The recipient MAY
continue with unaffected in-scope work only when the remaining scope and
validation evidence are still clear.

Orchestrator and Worker handoffs SHOULD include concrete artifact identifiers
for the governing parent scope, active work item, change proposal, review
surface, or equivalent collaboration artifact when those identifiers are
available. Readiness reports SHOULD include the same identifiers for the work
being reported. Identifier formats are owned by the relevant local artifact or
platform surface; this rule does not require a specific tracker, pull request,
issue-closing syntax, branch name, or platform mechanic.

## Worker Handoff Contract

A worker handoff MUST include the fields below. Field names MAY vary by
artifact format, but the content MUST remain explicit and reviewable.

| Field | Requirement |
| --- | --- |
| `active_work_item` | Names the bounded work item or change the worker owns. |
| `parent_scope` | Identifies the parent program, objective, or accepted direction that bounds the work. |
| `accepted_scope` | States the in-scope behavior, documentation, artifact, or contract change. |
| `in_scope_refs` | Lists paths, surfaces, artifacts, or ownership areas the worker may change or inspect. File references SHOULD be repository-relative when possible. |
| `out_of_scope_boundaries` | Lists known exclusions, forbidden changes, and work that must be reported instead of solved. |
| `evidence_pointers` | Points to current contracts, artifacts, diffs, source state, prior decisions, or validation reports that should guide inspection. |
| `required_validation` | Lists required validation claims, evidence types, or review checks and the expected use of the statuses in [validation.md](validation.md). |
| `known_risks` | States known uncertainty, disputed assumptions, blocked areas, and later-work risks. |
| `deliverables` | States the durable artifacts, source changes, validation report, or readiness report expected from the worker. |

Worker handoffs SHOULD be concise. They MUST include enough evidence pointers
for the worker to re-inspect current state without receiving an unbounded
planning transcript.

## Worker Pre-Edit Obligations

Before editing, a Worker Thread MUST:

1. inspect the current source or artifact state for the in-scope references;
2. inspect governing portable contracts and relevant project-local files,
   vendor shims, or platform surfaces when those layers are in scope;
3. compare current evidence with the handoff's accepted scope and known risks;
4. identify contradictions, missing evidence, stale assumptions, or path
   ownership conflicts;
5. report blockers or out-of-scope findings before changing scope.

If current evidence contradicts the handoff, the worker MUST treat current
evidence as the factual baseline and the handoff as scope evidence. The worker
MUST NOT force the source state to match a stale handoff unless the active scope
explicitly requires that correction and the required validation can support it.

## Evaluator Handoff Contract

An evaluator handoff MUST include the fields below. Field names MAY vary by
artifact format, but the content MUST remain explicit and reviewable.

| Field | Requirement |
| --- | --- |
| `artifact_or_change_under_review` | Identifies the durable artifact, source change, validation report, or change set being evaluated. |
| `relevant_state_refs` | Points to the relevant diff, source state, rendered artifact, or artifact revision. |
| `acceptance_criteria` | States the criteria, contract requirements, or readiness conditions the evaluator should apply. |
| `validation_evidence` | Points to validation claims and supporting evidence, including missing claims or claims with `passed`, `failed`, `skipped`, `pending`, `not_required`, or `maintainer_confirmed` status. |
| `known_risks_or_disputed_assumptions` | Lists risks, uncertainty, contested interpretations, and areas the evaluator should verify. |
| `exact_evaluation_question` | States the precise question to answer, such as whether the change satisfies accepted scope or whether a validation claim is supported. |

Evaluator handoffs MUST NOT include broad historical context unless it is needed
to answer the exact evaluation question. When broad context is needed, the
handoff SHOULD summarize the relevant decision and provide a durable evidence
pointer.

## Out-Of-Scope Finding Reports

Workers and evaluators MUST report out-of-scope findings instead of silently
expanding active scope. A finding report SHOULD include:

- the finding or suspected defect;
- the evidence pointer or inspected-state summary;
- why it is outside the active scope;
- the potential impact or blocked consumer;
- whether the finding affects current deliverables or validation;
- the recommended next routing, follow-up decision, or later work item;
- any residual risk that remains if the finding is not addressed now.

Out-of-scope findings MAY block readiness when they directly affect accepted
scope, required validation, or artifact safety. They SHOULD be recorded as
residual risks when they belong to later implementation work.

## Validation And Readiness Reporting

Workflow readiness reports MUST use the validation claim model and status
vocabulary from [validation.md](validation.md). Required validation claims MUST
be reported as one of `passed`, `failed`, `pending`, `skipped`, `not_required`,
or `maintainer_confirmed`. Durable text output boundaries for readiness reports
are defined in [outputs.md](outputs.md).

A readiness report MUST include:

- the work item, artifact, or change being reported;
- available artifact identifiers for the governing scope, active work item,
  change proposal, review surface, or equivalent collaboration artifact;
- completed deliverables and any missing deliverables;
- validation claims with evidence references and limitations;
- out-of-scope findings and how they were routed;
- residual risks and disputed assumptions;
- a readiness recommendation for the next role or decision.

A readiness report MUST NOT state or imply that required validation is complete
when any required claim is `failed`, `pending`, or `skipped`. It MAY recommend
readiness only when required claims are `passed` or `maintainer_confirmed`, any
`not_required` claims are justified by scope, and residual risks are disclosed.

Known risks that belong to later implementation work SHOULD be reported as
residual risks rather than solved through unrelated workflow changes.

## Lifecycle Gates

Lifecycle gates are portable decision points that control when work may move
from exploration to accepted scope, from implementation to review, from review
to acceptance, or from acceptance to irreversible publication or cleanup. This
contract defines gate responsibilities and evidence expectations only. Local
owners, platform mechanics, labels, fields, branch names, closure syntax,
reviewer rules, merge commands, release steps, and cleanup commands belong to
project-local policy or consumer-owned platform surfaces.

An implementation scope gate MUST exist before a Worker Thread owns changes. A
planning recommendation, candidate scope, historical discussion, or generated
summary does not authorize implementation by itself. Accepted worker scope MUST
come from an orchestrator handoff, maintainer direction, accepted work-item
artifact, or another project-local delegation that preserves the portable role
boundaries.

A worker readiness gate MUST include worker self-review evidence. Worker
self-review is required evidence for readiness reporting, but it is not final
independent approval of the work. A Worker Thread MAY create a change proposal
or equivalent review surface as a deliverable when local policy and the platform
support it. The exact platform fields, posting mechanics, issue references, and
publication timing are local policy.

When independent or adversarial review is required by the parent scope,
orchestration, local policy, or maintainer direction, an Evaluator Thread or
equivalent review process MUST evaluate the artifact or change against explicit
criteria and validation evidence. Evaluation MUST NOT broaden implementation
scope unless the role is explicitly reassigned.

Final acceptance, merge, release, destructive cleanup, issue closure, or any
equivalent irreversible publication requires an owning process, exact maintainer
confirmation, or project-local delegation. When that authority is absent or
unclear, the readiness claim is `pending` and the next owner or requested
decision MUST be reported.

Checkboxes, tasklists, project fields, labels, status columns, and similar
progress surfaces MAY help route work, but they are progress state only. They
MUST NOT be used as validation evidence, readiness evidence, or final acceptance
evidence unless a separate validation claim cites supporting evidence allowed by
[validation.md](validation.md).

Authority to edit work-item bodies, acceptance-criteria markers, tasklists,
project fields, labels, or equivalent progress markers belongs to
project-local policy or consumer-owned platform surfaces. When that layer
authorizes the mutation, an agent MAY update progress surfaces after supporting
readiness, acceptance, or closure evidence has been recorded. Such updates are
progress-state housekeeping only. They MUST NOT create validation evidence,
review evidence, final approval, closure authority, or irreversible-publication
authority. The durable evidence record remains the authoritative basis for those
claims. When a housekeeping update is material to later routing or audit, it
SHOULD point to the supporting evidence record or otherwise be traceable to it.

## Platform-Agnostic Change Lifecycle

Portable workflow consumers SHOULD adapt the following lifecycle to their local
platforms without changing the role boundaries or lifecycle gates:

1. Planning identifies goals, assumptions, trade-offs, candidate scope, and
   validation expectations.
2. Orchestration accepts or routes bounded work items under a parent scope.
3. A worker handoff transfers only active scope, boundaries, evidence pointers,
   validation expectations, known risks, and deliverables.
4. The worker re-inspects current evidence before editing.
5. The worker implements in-scope changes and preserves ownership boundaries.
6. The worker reports deliverables, validation claims, out-of-scope findings,
   and residual risks.
7. An evaluator handoff transfers the artifact or change under review, relevant
   state, acceptance criteria, validation evidence, risks, and the exact
   evaluation question.
8. Evaluation checks the change against accepted scope, validation evidence, and
   readiness criteria.
9. Orchestration synthesizes worker and evaluator reports into the next
   bounded decision.
10. The owning process accepts, revises, defers, or rejects the change with
    evidence-backed rationale.

The lifecycle MUST remain adaptable. Project-local workflow exceptions belong in
`docs/project/**`. Platform-specific labels, templates, statuses, automations,
and routing files belong with the relevant consumer-owned surface, vendor shim,
or project-local extension.

## Boundary Rules

Workflow contracts own:

- portable role responsibilities and non-responsibilities;
- bounded worker and evaluator handoff content;
- the rule that handoffs are scope evidence, not factual proof of current state;
- pre-edit evidence inspection obligations;
- out-of-scope finding and residual-risk reporting;
- readiness reporting requirements that use the portable validation vocabulary;
- lifecycle gate responsibilities and evidence expectations;
- the platform-agnostic change lifecycle.

Workflow contracts MUST NOT own:

- repository-specific branching, review, release, deployment, or operations
  procedures;
- project-local workflow exceptions, validation commands, source maps, or local
  policy details;
- collaboration-platform labels, templates, statuses, automations, or payloads;
- local acceptance, merge, release, issue-closure, or cleanup authority;
- vendor shim or platform surface payloads, or tool-specific runtime behavior;
- evidence-packing tool behavior beyond evidence pointers;
- agent-authored output categories, prompt body handling, or change-proposal
  defaults;
- installer implementation behavior or copy decisions;
- concrete evaluation cases, fixtures, scoring rubrics, or datasets.

## Extension Path

Later workflow work SHOULD extend this file only when adding portable role,
handoff, readiness, or lifecycle rules. Project-local workflow exceptions should
live in `docs/project/**`. Platform-specific workflow entry points should live
with the relevant consumer-owned surface, vendor shim, or project-local
extension.

# Validation Contracts

This document defines the portable validation claim model and validation status
vocabulary for evidence-backed agent collaboration.

Validation rules describe how to make, support, and report validation claims.
They do not define project-local commands, CI job names, vendor shim payloads,
platform surface payloads, fixtures, lint implementations, or installer
behavior.

## Terms

- **Validation claim**: a durable assertion that a check, review, confirmation,
  or applicability decision has a specific status for a specific subject.
- **Validation subject**: the artifact, source file, source state, behavior,
  requirement, or boundary being validated.
- **Validation evidence**: observed support for a validation claim, such as
  command output, inspected state, CI result, manual review, or maintainer
  confirmation.
- **Residual risk**: a known uncertainty that remains after validation is
  reported.
- **Required validation**: a claim that must be resolved by the governing scope,
  artifact contract, project-local extension, consumer-owned surface, or
  maintainer direction.

## Validation Claim Model

A validation report is a durable artifact under [artifacts.md](artifacts.md).
Agent-authored validation report output boundaries are defined in
[outputs.md](outputs.md). Each validation report MUST contain one or more
validation claims. Each claim MUST be reviewable without relying on unsupported
conversation memory.

Each validation claim MUST include:

| Field | Requirement |
| --- | --- |
| `claim_id` | Stable identifier for the claim within the report or artifact set. |
| `subject_refs` | References to the artifacts, source files, requirements, or source evidence being validated. |
| `claim` | Plain-language statement of what was checked or decided. |
| `status` | One of `passed`, `failed`, `pending`, `skipped`, `not_required`, or `maintainer_confirmed`. |
| `evidence_refs` | References to evidence supporting the status. Required for statuses that claim observed result, explicit confirmation, or applicability. |
| `evidence_summary` | Short summary of the evidence and what it proves or does not prove. |
| `status_reason` | Explanation for the chosen status, especially for non-passing statuses and applicability decisions. |
| `validator` | Role, process, or tool that made the claim at the level needed for review. |
| `checked_or_recorded` | Freshness information for when the evidence was observed or the claim was recorded. |
| `limitations` | Known limits, uncertainty, missing evidence, or residual risks for this claim. |

Claims MAY include next actions, severity, affected consumers, or links to
related claims when useful. Machine-consumed reports SHOULD use stable structured
fields. Human-readable reports MAY use prose or tables when all required
information remains explicit.

## Status Vocabulary

Validation statuses are lowercase tokens. A validation claim MUST use exactly
one status.

| Status | Semantics | Evidence requirement |
| --- | --- | --- |
| `passed` | The required check or review was performed, and the observed evidence supports the claim. | MUST reference evidence that directly supports the claim, such as command output, inspected state, CI result, or manual review evidence. MUST NOT be used when validation was not run or evidence is unavailable. |
| `failed` | The required check or review was performed, and the observed evidence contradicts the claim or shows an unacceptable result. | MUST reference the failing evidence and summarize the failure. SHOULD include impact and next safe action. |
| `pending` | The validation is required or expected, but the evidence is not available yet. | MUST explain what evidence is missing and why the claim is pending. MAY reference a queued run, requested review, or blocked prerequisite. MUST NOT count as success. |
| `skipped` | The validation could have been relevant, but it was intentionally not performed for a stated reason. | MUST explain the skip reason and SHOULD reference scope, prerequisite, risk, or maintainer direction that justifies the skip. MUST NOT count as success. |
| `not_required` | The validation is not applicable or not required for the stated scope. | MUST reference the scope, contract rule, artifact boundary, or requirement analysis supporting non-applicability. MUST NOT be used to hide unrun required validation. |
| `maintainer_confirmed` | An explicit maintainer confirmation is being used as the evidence for the claim. | MUST reference the confirmation evidence and state exactly what was confirmed. MUST NOT extend the confirmation beyond its explicit scope. |

`passed` and `maintainer_confirmed` are the only statuses that may satisfy a
required validation claim, and only for the exact subject and scope supported by
their evidence. A report MUST NOT state or imply that all required validation is
complete when any required claim is `failed`, `pending`, or `skipped`.

## Evidence Types

Validation evidence MUST be specific enough for a later reviewer to understand
what was observed and why the status follows from it. Evidence references SHOULD
use repository-relative file paths for file evidence when possible and MUST avoid
host-absolute paths in portable core artifacts.

### Command Evidence

Command evidence comes from invoking a command or local tool and observing its
result. A command-evidence reference SHOULD include:

- the command description or invocation as recorded in the validation report or
  project-local context;
- the exit status or equivalent result;
- relevant output, including an explicit note when meaningful output was empty;
- the subject or file set the command covered;
- any important environment, dependency, or freshness limitation.

Portable validation contracts MUST NOT prescribe concrete project-local command
lines. Project-local commands belong in `docs/project/**` or in a validation
report for a specific repository.

### Inspected-State Evidence

Inspected-state evidence comes from directly reviewing files, diffs, rendered
output, configuration, repository state, or other observable source state.

An inspected-state reference SHOULD include:

- the repository-relative path, artifact locator, diff range, or rendered output
  locator inspected;
- the observation made;
- the criteria used for review;
- any uncertainty about freshness or completeness.

Inspected state MAY support `passed`, `failed`, `not_required`, or
`skipped` claims when the evidence directly supports that status.

### CI Evidence

CI evidence comes from an automated check run outside the immediate local
inspection. A CI-evidence reference SHOULD include:

- the check or workflow name as reported by the CI system;
- the result status;
- the source revision, artifact, or subject covered when available;
- a stable locator or run identifier when available;
- relevant output summary for failures.

CI evidence MUST be scoped to the subject it actually covered. A successful CI
result for one revision, local surface, or artifact MUST NOT be reused as
success for a different subject without evidence that the coverage still
applies.

### Manual Review Evidence

Manual review evidence comes from a person or agent inspecting a subject against
explicit criteria. It SHOULD include:

- the criteria reviewed;
- the artifacts, source state, or evidence inspected;
- the reviewer role or process;
- findings, non-findings, and residual risks.

Manual review MAY support success when the relevant requirement is review-based.
It MUST NOT replace required command or CI evidence unless the governing scope
allows manual review or the missing automation is reported with an appropriate
non-passing status.

### Maintainer Confirmation

Maintainer confirmation is explicit confirmation from a maintainer that a claim,
scope decision, exception, or acceptance point is true.

A maintainer-confirmation reference MUST include:

- what was confirmed;
- where the confirmation was recorded;
- when it was recorded or observed when freshness matters;
- any limits stated by the maintainer.

Maintainer confirmation MAY satisfy a validation claim only within its explicit
scope. It MUST NOT be generalized to unrelated artifacts, checks, or future
states.

## Reporting Failures And Residual Risks

A `failed` claim MUST report:

- the failed subject;
- the evidence showing failure;
- the expected result or acceptance criterion when known;
- the observed result;
- the impact or blocked consumer when known;
- the next safe action when known.

Validation reports MUST include residual risks when uncertainty remains after
validation. Residual risks SHOULD identify the subject, why the risk remains,
what evidence would reduce it, and whether the risk affects release, review,
installer behavior, vendor shims, platform surfaces, or evaluation consumers.

Known risks that belong to later implementation work SHOULD be reported as
residual risks rather than solved by unrelated contract changes.

## Success Claim Rules

Validation reports MUST NOT claim success from missing evidence.

A claim MUST NOT be marked `passed` when:

- the check was not run;
- the evidence was not inspected;
- the evidence is unavailable;
- the evidence covers a different subject;
- the evidence contradicts the claim;
- the report relies only on expectation, memory, or intent.

When validation was not run, the claim MUST be `pending`, `skipped`, or
`not_required`, depending on the reason. When explicit maintainer confirmation is
the evidence, the claim MUST use `maintainer_confirmed` unless a separate
performed check also supports `passed`.

An aggregate validation summary MAY state that required validation passed only
when every required claim is either `passed` or `maintainer_confirmed` with
supporting evidence and no required claim is `failed`, `pending`, or `skipped`.
Optional or out-of-scope claims marked `not_required` MUST be reported clearly
and MUST NOT be counted as performed validation.

## Referencing Artifacts And Source Evidence

Validation claims MUST reference their subjects precisely enough for later
consumers to find the reviewed artifact or source evidence.

Subject references SHOULD include one or more of:

- artifact identifiers or stable locators;
- repository-relative file paths;
- schema versions or artifact revisions when relevant;
- source evidence reference identifiers;
- acceptance criteria or requirement identifiers when available.

Validation claims SHOULD reference evidence rather than embedding full evidence
packs. Evidence-packing behavior belongs in [evidence-packing.md](evidence-packing.md)
or in a tool-specific layer. When validation evidence conflicts with another
source class, apply the claim-type boundaries in [sources.md](sources.md).

Validation claims that cover portable contracts MUST keep portable files free of
project-local facts. Validation reports for a specific repository MAY contain
repository-local facts when they are necessary evidence and the report is owned
by the project-local, platform surface, vendor shim, or review layer rather than
by portable core content.

## Boundary Rules

Portable validation rules own the claim model, status vocabulary, evidence
expectations, success-claim rules, and reporting requirements for failures and
residual risks.

Portable validation rules MUST NOT own:

- concrete project-local command lines, local runtime requirements, fixtures, or
  CI job names;
- validation report body templates or other agent-authored output formats;
- vendor shim or platform surface check content or platform status
  fields;
- portability-lint implementation rules;
- installer implementation behavior beyond the need to validate and report
  installer-related claims with evidence;
- detailed thread-role, handoff, or orchestration workflows;
- evaluation cases, datasets, or scoring rubrics.

Project-local validation commands belong in `docs/project/**`.
Vendor shim and platform surface validation behavior belongs with the relevant
consumer-owned layer. Installer safety rules belong in
[ownership.md](ownership.md).

## Extension Path

Later validation work SHOULD extend this file only when adding portable
claim-model, evidence, or status rules. Project-specific validation procedures,
vendor shim checks, platform surface checks, lint implementations, and
evaluation cases SHOULD extend their own owning surfaces instead.

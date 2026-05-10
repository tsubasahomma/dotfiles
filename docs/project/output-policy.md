# Project Output Policy

Use this file to record reusable local policy for durable text outputs that
agents, maintainers, tools, vendor shims, or platform surfaces create for one
consumer repository.

Local output policy extends the portable output contract. It MAY specialize
language choices, local fields, references, trailers, safe body handling,
comments, prompts, reports, change proposals, change messages, and platform
surface mappings. It MUST NOT silently replace portable source, artifact,
workflow, validation, evidence-packing, ownership, or safety boundaries.

Do not use this file as a full output-template form. Leave it sparse until
concrete repository work reveals reusable output policy.

## Local Output Mechanics Routing

Concrete output mechanics that the portable output contract intentionally does
not own belong here when this repository needs them. Examples include strict
patch handoff rules, heredoc conventions, command snippet formatting, whitespace
or final-newline requirements, and local platform command-body mechanics.

Keep those rules scoped to repository-local needs and do not copy them into
`docs/agent-context/**`.

## Output Memory Rules

Use the local memory layers below. Observed cases and pending output decisions
are non-authoritative. They may guide future output drafting, but they do not
make a field required, authorize platform mutation, or prove validation.

`Confirmed Local Decisions` are authoritative only for their recorded scope. A
confirmed output decision requires explicit maintainer confirmation, a
materialized local authority rule, or another recorded authoritative local
evidence pointer whose ownership, freshness, and scope are clear.

When authority is missing, keep the entry in `Observed Durable-Output Case
Studies`, `Pending Local Output Decisions`, or an explicit state such as
`unknown`, `pending`, `omitted`, or `not_required`.

`maintainer_confirmed` is an explicit state or evidence marker for the exact
confirmed claim. It is not a synonym for every `Confirmed Local Decision`;
confirmed decisions may also be authorized by a materialized local authority
rule or another authoritative local evidence pointer.

Project-memory entries may point to validation evidence, but they are not
validation evidence by themselves. Static output bodies should cite observed
evidence and freshness instead of mirroring changing review, CI, deployment, or
external status as always-current truth.

## Observed Durable-Output Case Studies

Record concrete output cases that may help future agents draft or route durable
text. These entries are evidence pointers and examples, not policy.

| Case | Output surface | Observation | Evidence pointer | Outcome or limit |
| --- | --- | --- | --- | --- |
| `[case name]` | `[issue body, change proposal, change message, review comment, worker prompt, evaluator prompt, validation report, readiness report, command body, release note, rollback note, evidence summary, or other surface]` | `[what was written, omitted, corrected, or risky]` | `[issue, pull request, local file, review finding, maintainer note, or omitted reason]` | `[reusable lesson, unresolved risk, pending decision, not_required scope, or limit]` |

## Pending Local Output Decisions

Use this section when a local output rule appears needed but authority has not
confirmed it. Pending entries are proposals or open questions only.

| Decision question | Candidate output rule | Affected outputs | Evidence basis | Needed authority or blocker | State |
| --- | --- | --- | --- | --- | --- |
| `[question]` | `[proposed field, heading, language rule, reference rule, trailer rule, safe-body rule, comment rule, platform mapping, or omitted reason]` | `[output types, platform surfaces, risk class, release scope, or not_required reason]` | `[observed case, current source, platform surface, maintainer question, or limitation]` | `[maintainer confirmation, local authority rule, platform owner, unavailable evidence, or blocker]` | `[unknown, pending, omitted, or not_required]` |

## Confirmed Local Output Decisions

Use this section only for scoped local output policy with authority. Do not
promote an observed output, issue text, pull request text, label, checkbox,
project field, successful check, or repeated agent behavior into confirmed
policy unless an authority source explicitly makes that surface decisive for the
recorded scope.

| Decision | Scope | Affected outputs | Authority source | Evidence pointer | Limits |
| --- | --- | --- | --- | --- | --- |
| `[confirmed output rule or exception]` | `[exact output type, platform surface, path set, risk class, release scope, or other boundary]` | `[issue body, change proposal, change message, prompt, finding, validation report, readiness report, comment, command body, release note, rollback note, evidence summary, or platform mapping]` | `[maintainer confirmation, materialized local authority rule, or authoritative local evidence pointer]` | `[where the authority and supporting evidence are recorded]` | `[what is not authorized, freshness limit, required recheck, or portable boundary]` |

## Common Output Decision Areas

Record an entry above only when it is reusable. Common output decisions include:

- conversation language and durable artifact language, recorded separately;
- Parent Issue, Child Issue, change-proposal, change-message, review-finding,
  validation-report, readiness-report, prompt, command-body, release-note, and
  rollback-note fields;
- issue references, closure syntax, trailers, merge-message policy,
  release-note policy, commit subject style, subject length targets, body line
  targets, and local exceptions;
- AI-authored comment triggers, update behavior, noise limits, local placement,
  and required evidence content;
- safe structured-body boundaries such as body files, standard input,
  structured API fields, or platform-surface-owned fields;
- platform-surface mappings for labels, assignees, reviewer requests,
  milestones, project fields, templates, or status fields when the consumer
  repository owns those mappings.

## Output Boundaries

- Durable output policy MUST identify whether a local rule is confirmed,
  pending, omitted, unknown, `not_required`, or `maintainer_confirmed`.
- Agent-authored comments SHOULD stay sparse, role-specific, and
  evidence-oriented unless confirmed local policy requires a different shape.
- Local output policy MUST NOT claim validation success without evidence that
  satisfies the portable validation contract.
- Static output bodies MUST NOT mirror changing review, CI, deployment,
  release, or external state as always-current truth.
- Platform fields, labels, checkboxes, reviewer requests, and assignment
  behavior are local or surface-owned mappings, not portable doctrine.
- Do not record secrets, sensitive values, transient task details, stale
  historical prose, role-specific scratch narration, commented-out
  instructions, or obsolete guidance.

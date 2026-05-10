# Project Secrets Policy

Use this file as concise local memory for safe sensitive-data handling. It may
record reusable observations, pending secrets decisions, and confirmed secrets
policy, but it must never contain sensitive values.

Local secrets memory extends the portable evidence, validation, artifact,
source, workflow, and ownership contracts. It MUST NOT copy sensitive local
facts into `docs/agent-context/**` or silently replace portable redaction,
evidence, validation, or ownership boundaries.

## Safety Rules

Do not record actual secrets, credentials, authentication material, private
keys, recovery material, unredacted private personal data, unredacted regulated
data, production data samples, host-absolute paths, private infrastructure
identifiers, or secret-adjacent example values.

Use safe category names, redacted summaries, evidence pointers, omission notes,
and exact confirmation records instead. When local secrets policy is missing or
incomplete, use conservative redaction or omission and report the limitation.

## Local sensitive surfaces

Treat these repository surfaces as secret-adjacent even when the source file is
tracked and reviewable:

| Surface | Safe handling |
| --- | --- |
| Bootstrap GitHub token | Never print token values. Describe only token purpose, scope, or missing-token state. |
| 1Password identity metadata | Do not print account IDs, item IDs, vault identifiers, local profile paths, private keys, or generated identity output. Use redacted structural evidence. |
| SSH signing and agent routing | Do not print private keys, unnecessary public key material, raw agent output, or socket details unless a scoped task requires redacted structural evidence. |
| Generated identity files | Treat generated Git identity and SSH routing outputs as sensitive evidence. Inspect locally and summarize safely instead of copying full contents into shared output. |
| WSL2 authentication state | Avoid exposing host-private Windows paths, local usernames, socket paths, SSH key material, and agent output unless redacted evidence is required for the scoped task. |
| Generated Repomix output | Treat packed snapshots as generated evidence that may contain sensitive local context. Do not hand-edit them; regenerate only when validation requires fresh evidence. |

## Secrets Memory Rules

- Record only reusable classification, storage-boundary, redaction, evidence,
  validation-handling, or escalation knowledge.
- Keep observations and pending decisions visibly non-authoritative.
- Confirmed secrets decisions require explicit maintainer confirmation,
  materialized local authority, or another authoritative local evidence pointer.
- Use `unknown`, `pending`, `omitted`, and `not_required` when authority,
  evidence, or applicability is incomplete.
- Use `maintainer_confirmed` only for exact maintainer-confirmed claims.
- Project-memory entries may point to validation evidence, but they are not
  validation evidence by themselves.

## Observed Sensitive-Data Handling Case Studies

Record concrete handling cases that may help future agents recognize safe
classification, redaction, storage, evidence, or escalation patterns. These
entries are evidence pointers and examples, not policy.

| Case | Sensitive area | Observation | Safe evidence pointer | Outcome or limit |
| --- | --- | --- | --- | --- |
| `[case name]` | `[credential category, private data class, regulated data class, operational data class, sensitive surface, validation evidence, generated artifact, or other area]` | `[what was observed without revealing sensitive values]` | `[redacted file pointer, issue, pull request, maintainer note, validation report, or omitted reason]` | `[safe handling lesson, unresolved risk, pending decision, not_required scope, or limit]` |

## Pending Local Secrets Decisions

Use this section when a local secrets rule, classification, storage boundary,
redaction rule, evidence rule, or escalation path appears needed but authority
has not confirmed it. Pending entries are proposals or open questions only.

| Decision question | Candidate secrets rule | Affected material or surfaces | Evidence basis | Needed authority or blocker | State |
| --- | --- | --- | --- | --- | --- |
| `[question]` | `[proposed classification, storage boundary, redaction rule, evidence rule, escalation path, validation handling, or omitted reason]` | `[safe material category, path set, artifact class, output type, validation evidence, sensitive surface, or not_required reason]` | `[observed case, current source, maintainer question, redacted evidence, or limitation]` | `[maintainer confirmation, local authority rule, security owner, unavailable evidence, unsafe disclosure risk, or blocker]` | `[unknown, pending, omitted, or not_required]` |

## Confirmed Local Secrets Decisions

Use this section only for scoped secrets policy with authority. Do not promote
an observed handling pattern, successful check, issue text, pull request text,
label, checkbox, project field, or repeated agent behavior into confirmed
policy unless an authority source explicitly makes that surface decisive for the
recorded scope.

| Decision | Scope | Affected material or surfaces | Authority source | Evidence pointer | Limits |
| --- | --- | --- | --- | --- | --- |
| `[confirmed secrets rule, classification, storage boundary, redaction rule, evidence rule, escalation path, or exception]` | `[exact paths, artifact classes, output types, validation evidence, sensitive surfaces, work types, or other boundary]` | `[safe material category or surface class, never sensitive values]` | `[maintainer confirmation, materialized local authority rule, or authoritative local evidence pointer]` | `[where the authority and supporting evidence are recorded]` | `[what is not authorized, freshness limit, required recheck, redaction limit, expiration, or portable boundary]` |

## Secrets Boundaries

- Never quote, invent, transform, or preserve sensitive values in this file.
- Use category names and redacted summaries instead of example values.
- If a material evidence source contains sensitive data, omit, redact, mask,
  aggregate, summarize, or request confirmation before reporting it.
- If safe handling is impossible, mark the evidence unavailable, pending,
  skipped, or limited instead of weakening the boundary.
- `maintainer_confirmed` can support only the exact confirmed secrets claim and
  scope recorded with the confirmation evidence.
- Secrets policy entries do not prove validation status by themselves. They may
  describe which evidence is safe to use, but validation reports must cite the
  observed or confirmed evidence directly.
- Do not record transient task notes, issue-plan narration, stale migration
  prose, worker self-reporting, dead comments, or obsolete guidance.

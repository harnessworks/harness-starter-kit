# Decision And Failure Memory Checklist

Use this checklist to reduce overdocumentation pressure while still preserving
high-value memory for future agents.

The default is not "write an ADR for every change." The default is: record
durable memory when a future agent would otherwise repeat the same decision,
mistake, or investigation.

## Choose The Right Artifact

| Situation | Prefer | Examples | Usually skip when |
| --- | --- | --- | --- |
| A structural choice becomes part of code layout or workflow | `docs/decisions/*.md` | route model, service boundary, runtime choice, state classification, live/mock policy | the task only follows an existing ADR or local pattern |
| A runtime or integration failure should not recur | `docs/failures/*.md` | TLS/certificate failure, 5xx path, secret leak risk, provider schema mismatch, repeated failed check | the issue was transient and no prevention or detection changed |
| Product or provider terms need consistent language | `docs/domain/*.md` | empty-result meaning, provider status codes, itinerary states, permission states | the term is obvious and already documented nearby |
| Coding or review habit should be repeated | `docs/conventions/*.md` or `AGENTS.md` | route handler rules, env handling, generated-file policy, verification command | the habit applies only to one narrow file |
| A custom check becomes part of normal verification | README, `AGENTS.md`, package scripts, or `docs/conventions/*.md` | `check:harness`, API smoke script, route table check | the check was a one-off diagnostic |
| A small implementation detail changed | final report or check note | test selector tweak, response field rename covered by tests, copy fix | the change creates a new boundary or recurring risk |

## Decision Record Triggers

Consider a decision record when the change:

- selects or changes architecture, router shape, persistence, runtime, state, or
  integration policy
- codifies product workflow structure in code
- defines live/mock fallback policy or external API ownership
- introduces a durable data model or state classification
- changes a rule future agents are likely to re-litigate

No decision record is usually needed when:

- the change is a narrow bug fix inside an existing boundary
- the decision is already covered by an ADR and the final report cites it
- tests or conventions already document the behavior clearly enough
- the only change is adding a check that enforces an existing documented rule

## Failure Record Triggers

Record a failure when the issue should not recur and at least one of these is
true:

- user-visible runtime failure, crash, 5xx path, or broken production-like flow
- security, permission, privacy, or data-loss risk
- failed CI or harness check that revealed a real bug or drift
- repeated agent mistake or previously identified bug path
- external API, certificate, schema, parser, or environment mismatch that cost
  investigation time
- cross-environment mismatch such as local passing while CI fails

No failure record is usually needed when:

- the issue was purely transient and no repo behavior changed
- the failure is already covered by an existing record
- a normal test failure was fixed immediately and revealed no broader bug path
- the final report can name the skipped reason without losing useful memory

## Boundary Examples

| Change | Likely memory |
| --- | --- |
| Add a planner branch that changes product workflow shape | ADR, or cite an existing workflow ADR |
| Add a route handler that proxies a public-data API with server-only secrets | ADR if it creates the integration boundary; convention if it follows an existing one |
| Handle provider zero-result responses deliberately | Domain note or test; ADR only if it changes product behavior |
| Fix a TLS certificate failure that Node fetch hits for a provider endpoint | Failure record if future agents should not retry the same path blindly |
| Add `scripts/check_<area>.mjs` for a repeated backend smoke check | README or `AGENTS.md` if it becomes normal verification |
| Add one response field and update tests | Final report or check note, unless it changes the domain model |

## Final Report Language

When no durable memory is added for a non-trivial change, report the reason
explicitly:

```text
Decision docs: skipped because this follows ADR 0002 and does not introduce a
new boundary.
Failure memory: skipped because the failing request was transient and no
reproducible bug path or prevention rule changed.
```

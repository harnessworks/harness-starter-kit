# 0003. Structural Product Decisions Were Implemented Without ADR Review

## Date Observed

2026-06-02

## Failure Type

Repeated agent mistake and durable memory gap.

## Goal

When agent work turns product behavior into durable code structure, the agent
should consider whether the change needs a `docs/decisions/*.md` record. If no
new decision record is added, the final report should say whether an existing
ADR covers the decision or why the change did not need decision memory.

## What Happened Or Was Tried

During work on a TodayBus target repository, an agent implemented MVP routes,
user flows, and mock data structure. The agent updated durable domain context
but did not initially add a decision record under `docs/decisions/`.

The missed decision surface included route and flow structure, mock data or API
boundary choices, and product behavior that became part of the code layout.

## Why It Failed

- The existing agent guidance required durable docs updates, but did not make
  the decision-record trigger specific enough.
- The agent treated a `docs/domain/glossary.md` update as sufficient durable
  documentation, even though glossary updates do not replace architectural or
  product-structure decisions.
- Harness review guidance did not explicitly ask reviewers to challenge
  structural product changes when no `docs/decisions/` change was present.
- A hard drift check would likely have been too broad at this stage because
  route, workflow, mock data, model, and state paths vary by target repository.

## Current Replacement

`commands/harness-review.md` now includes a diagnostic decision-docs gate. When
the current change set fixes product or workflow structure in code, changes an
integration or mock external-behavior boundary, introduces major data models or
state classifications, or codifies a product UX principle in implementation,
Harness Review should flag missing decision-memory review if `docs/decisions/`
was not changed and no existing ADR or scoped justification is named.

This is intentionally a review warning, not an automatic drift failure.

The kit also adds `scripts/check_decision_memory.py` as a configurable
diff-based warning gate. When watched implementation paths changed and
`docs/decisions/` did not, the script asks the final report to add or update an
ADR, cite an existing ADR, or explain why no decision memory is needed. The
script warns by default and can be promoted with `--fail-on-warning` after a
target repository tunes `.harness/decision-memory-rules.json`.

## Detection Or Prevention Check

`tests/test_repository_hygiene.py` verifies that the decision-memory review gate
is wired into review guidance, generic agent instructions, adoption prompts,
workflow docs, and validation references. `tests/test_check_decision_memory.py`
exercises the configurable diff warning for watched implementation paths
changed without a matching `docs/decisions/` change.

## Agent Guidance

Do not treat domain glossary updates as a substitute for decision records. For
non-trivial product, workflow, API or mock-boundary, data-model, state, or UX
structure changes, either add a decision record, cite the existing ADR that
covers the choice, or explain in the final report why the change is a narrow
implementation detail that does not need decision memory.

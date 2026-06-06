# 0005. Validate Dogfood Evidence Consistency Before Adoption

## Status

Accepted

## Date

2026-06-06

## Context

Dogfood evidence is useful only when it preserves the difference between
harness health, setup evidence, comparable product-task outcomes, and actual
agent effectiveness.

During Harness ERP dogfood review, the evidence was directionally strong but
initially exposed two adoption-quality gaps:

- an aggregate effectiveness report could say product-task runs were complete
  while later text still said no product-task records were complete
- a task outcome template could accidentally keep inclusion flags enabled and
  contaminate future mechanical counts

The target repository remained the source of truth, and the right response was
not to make adoption automatic. The kit needed a small validation and checklist
layer so future dogfood evidence can be accepted or deferred using repeatable
criteria.

## Decision

Extend `scripts/check_effectiveness_plan.py` to validate dogfood evidence
consistency:

- effectiveness reports that claim completed product-task outcomes must not
  also contain stale "no completed records yet" language or "record outcomes as
  they run" follow-up language
- task outcome templates or placeholder task outcomes must not be included in
  effectiveness reports or comparable product-task counts

Ship the same checker behavior in
`templates/generic/scripts/check_effectiveness_plan.py` so target repositories
receive the guard during adoption.

Add `docs/checklists/dogfood-evidence-adoption.md` as a prompt-first review
checklist for deciding whether a dogfood target should become a report,
lifecycle note, validation note, or README badge in this kit.

## Rationale

- These checks catch concrete evidence-quality gaps without inferring
  effectiveness improvement from passing tests or Harness Doctor scores.
- The validation remains lightweight and local, using the same standard-library
  checker style as the rest of the kit.
- The checklist keeps dogfood adoption prompt-first and reviewable instead of
  making the installer or checker copy target-specific architecture into
  generic templates.
- Template inclusion flags are high-risk for future aggregation because a
  parser can count them even when a human reader understands they are
  placeholders.

## Alternatives Considered

- Manual review only: rejected because the Harness ERP review showed the same
  stale aggregate text and template inclusion risk can survive until a later
  reviewer notices it.
- Parse every task outcome as full YAML: rejected for now because the kit avoids
  external dependencies and only needs a few scalar fields for this guard.
- Require baseline-vs-harnessed evidence before dogfood adoption: rejected
  because harnessed-only dogfood is still useful operational evidence when it
  is labeled correctly and does not claim improvement.

## Consequences

- `scripts/check_effectiveness_plan.py` now checks selected task outcome YAML
  records in addition to adoption and effectiveness Markdown reports.
- Dogfood reports that contain stale aggregate completion language fail local
  validation.
- Target-local template task outcome files must set inclusion flags to false,
  unknown, TODO, or another non-truthy value.
- Future dogfood adoption should cite or run the dogfood evidence checklist
  before adding README badges or validation examples.

## Agent Guidance

When adding dogfood evidence to this kit, run the target's normal gate and this
kit's effectiveness and failure-memory validators. Do not adopt the evidence
when template task outcomes are countable, stale aggregate language contradicts
the completed records, setup failures have not been evaluated for failure
memory, or the report implies effectiveness improvement without a comparison
point.

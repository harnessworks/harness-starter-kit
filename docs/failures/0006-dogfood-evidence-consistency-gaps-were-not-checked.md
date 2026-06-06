# 0006. Dogfood Evidence Consistency Gaps Were Not Checked

## Date Observed

2026-06-06

## Failure Type

Harness maintenance gap and repeated agent mistake risk.

## Goal

Dogfood evidence adopted into this kit should not contain stale aggregate
effectiveness language or count placeholder task outcome templates as real
evidence.

## What Happened Or Was Tried

Harness ERP was used as Spring/Maven dogfood evidence. A review found the
evidence was useful but initially not adoptable as-is:

- the aggregate effectiveness report said five comparable product-task runs
  were complete while the interpretation still said no completed product-task
  records existed yet
- the target-local task outcome template had inclusion flags set to true, which
  could contaminate future mechanical aggregation

The evidence was corrected in the target repository before adoption, but the
starter kit did not yet have a local check that would catch those two gaps for
future dogfood targets.

## Why It Failed

- `scripts/check_effectiveness_plan.py` validated required report sections and
  TODO markers, but did not inspect consistency between completed-outcome claims
  and stale no-records language.
- The checker did not inspect task outcome YAML records, so a placeholder or
  template record could keep inclusion flags enabled without failing
  validation.
- Dogfood adoption criteria were implicit in review judgment instead of written
  as a reusable checklist.

## Current Replacement

`scripts/check_effectiveness_plan.py` now validates:

- aggregate effectiveness reports that claim completed product-task outcomes do
  not also use stale no-completed-records language
- task outcome templates and placeholder task outcomes are not included in
  effectiveness reports or comparable product-task counts

`templates/generic/scripts/check_effectiveness_plan.py` carries the same guard
for target repositories. `docs/checklists/dogfood-evidence-adoption.md`
documents the source tracking, task outcome, failure memory, gate placement,
and claim-boundary criteria for adding dogfood evidence to this kit.

## Detection Or Prevention Check

`tests/test_check_effectiveness_plan.py` covers aggregate completion-language
contradictions, task outcome templates with truthy inclusion flags, and
placeholder task outcomes with truthy inclusion flags. `scripts/check_effectiveness_plan.py`
is the local checker that prevents those evidence-quality gaps from passing.

## Agent Guidance

Before adopting dogfood evidence, run `scripts/check_effectiveness_plan.py` and
review `docs/checklists/dogfood-evidence-adoption.md`. Do not count setup-only
runs as comparable product tasks, do not leave template task outcomes countable,
and do not claim effectiveness improvement from harnessed-only evidence.

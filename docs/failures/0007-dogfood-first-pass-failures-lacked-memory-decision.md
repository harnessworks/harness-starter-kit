# 0007. Dogfood First-Pass Failures Lacked A Memory Decision

## Date Observed

2026-06-06

## Failure Type

Harness maintenance gap and repeated agent mistake risk.

## Goal

Dogfood evidence adopted into this kit should account for every failed
first-pass or final verification. Each failure should either link to target
failure memory or explain why it was not promoted while naming the check that
detects recurrence.

## What Happened Or Was Tried

Harness ERP frontend follow-up evidence recorded two failed first-pass
verification results:

- `FE-001` failed because the initial static-resource test used
  `TestRestTemplate`, which was unavailable in the target test classpath.
- `FE-003` failed because a static-resource test used a brittle exact string
  assertion for an endpoint call that was wrapped across lines.

The starter-kit dogfood report counted those failures honestly, but its
failure-memory section only linked the older Spring Boot coordinate failure. A
subagent harness review found that the report had no explicit memory decision
for the two frontend first-pass failures.

## Why It Failed

- The dogfood adoption checklist required failure records for failed harness
  checks, but did not explicitly require every failed first-pass verification
  to have either a target failure note or a skip rationale.
- The report treated task outcome records as enough evidence without saying why
  these test-design failures were not promoted to separate target
  `docs/failures/*.md` records.
- Without that explicit decision, future dogfood reports could normalize
  first-pass harness failures as metrics only, losing the recurrence-prevention
  question.

## Current Replacement

The Harness ERP dogfood report now states that `FE-001` and `FE-003` were not
promoted to separate target failure notes because they were deterministic
verification-test design failures caught before product acceptance, not product
runtime regressions. The report names the target normal gate and static-resource
tests that detect recurrence, and says repeated instances should be promoted to
target failure records.

`docs/checklists/dogfood-evidence-adoption.md` now requires each failed
first-pass or final verification to link to target failure memory, or to include
an explicit skip rationale with a recurrence-detection check.

## Detection Or Prevention Check

Manual review point `docs/checklists/dogfood-evidence-adoption.md` checks
whether failed first-pass or final verification has target failure memory or an
explicit skip rationale with a recurrence-detection check.

`python scripts/check_failure_memory.py` validates that this failure record and
future kit failure records name concrete detection or prevention checks.

## Agent Guidance

Do not treat first-pass verification failures as metrics only. When adopting
dogfood evidence, inspect each failed first-pass or final verification and
either link target failure memory or write a specific skip rationale that names
the recurrence-detection check.

# 0005. Failure Memory Was Not Linked To Regression Checks

## Date Observed

2026-06-03

## Failure Type

Harness maintenance gap and repeated agent mistake risk.

## Goal

When a target repository records a recurring failure in `docs/failures/*.md`,
the harness should push that memory toward prevention or detection through a
test, fixture, smoke check, lint rule, drift check, CI gate, or explicit manual
review point.

## What Happened Or Was Tried

Dogfood feedback from a public-data API target found that failure memory helped
preserve context for a TAGO provider issue, but the fixed provider bug path did
not automatically produce a regression check for the provider boundary. The
failure note reduced future investigation cost, but did not by itself prove the
bug would be caught if it returned.

The same feedback noted that `/harness review` was useful, but less effective
when run after commit or push instead of before the change left the local
workspace.

## Why It Failed

- Failure memory guidance asked agents to record recurring failures, but did
  not require a detection or prevention check to be named.
- External API guidance mentioned smoke checks and fixtures, but did not make
  provider boundary fixtures the practical default for endpoint-specific
  contracts such as parameter casing, zero-result behavior, provider text
  errors, and schema drift.
- Harness Review guidance allowed useful diagnostics after push, but did not
  clearly frame pre-push review as the safer timing for substantial harness or
  integration-boundary changes.

## Current Replacement

Failure templates, agent guidance, adoption/update workflows, external API
checklists, verification script guidance, review command docs, and report
templates now require failure records to name a regression test, fixture, smoke
check, lint rule, drift check, CI gate, or manual review point.
`scripts/check_failure_memory.py` enforces that requirement locally, and the
generic template ships the same check to target repositories. External API
guidance now prioritizes provider boundary fixtures for endpoint parameter
contracts and provider response states. Harness Review now records review
timing and recommends pre-push review for substantial changes.

Regression coverage lives in `tests/test_repository_hygiene.py`.

## Detection Or Prevention Check

`scripts/check_failure_memory.py` checks that every non-template
`docs/failures/*.md` record includes a detection or prevention section with a
named test, fixture, smoke check, lint rule, drift check, CI gate, manual review
point, or explicit no-check-practical reason with a blocker and future review
signal. `tests/test_check_failure_memory.py` covers positive and negative
cases. `tests/test_repository_hygiene.py` checks that failure templates,
adoption guidance, external API guidance, review docs, PR templates, and
generic templates keep the regression-check requirement wired into the kit.

## Agent Guidance

Do not treat a failure note as sufficient prevention when the bug path can be
tested. Add or name the check that would fail if the issue recurs, or document
the concrete reason automation is not practical yet. For provider bugs, prefer
a boundary fixture that checks endpoint-specific request shape, response state,
and redaction before relying on live smoke output.

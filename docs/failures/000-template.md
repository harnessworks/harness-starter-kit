# 000. Failure Or Failed Approach Title

## Date Observed

YYYY-MM-DD

## Failure Type

Runtime failure, high-risk bug path, failed check, failed CI run, repeated agent
mistake, rejected approach, or cross-environment mismatch.

## Goal

What behavior, workflow, or safety property should have held?

## What Happened Or Was Tried

Describe the implementation, library, architecture, workflow, or user action
that exposed the failure.

## Why It Failed

- User-visible error, 5xx response, or crash
- Security, permission, or data-loss risk
- Failed check or CI failure
- Repeated agent mistake
- Cross-environment mismatch
- Operational cost
- Complexity
- Performance
- Reliability
- Developer experience
- Product mismatch

## Current Replacement

Describe the fix, accepted alternative, regression test, or review rule now in
place.

## Detection Or Prevention Check

Name the regression test, fixture, smoke check, lint rule, drift check, CI
gate, or manual review point that prevents or detects recurrence. If no check
is practical, explain why and say what future signal should trigger review.

## Agent Guidance

Tell agents what not to retry, which bug path to preserve, or which check to
run before finishing similar work.

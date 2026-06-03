# 0002. Subagent Report Misstated Harness Review Reviewer Mode

## Date Observed

2026-05-31

## Failure Type

Harness review reporting bug and reviewer-mode ownership mismatch.

## Goal

Use `/harness review sub-agent` so the parent agent can request an independent,
read-only reviewer subagent and then report whether a subagent was actually
used.

## What Happened Or Was Tried

The parent agent successfully discovered, spawned, waited for, and closed a
reviewer subagent. The reviewer subagent received forked context that included
the `/harness review` command guidance and returned findings.

## Why It Failed

The spawned subagent interpreted the command guidance as if it also had to
evaluate multi-agent tool availability and produce reviewer-mode metadata. From
inside its restricted runtime, it reported `Reviewer mode: single-agent
fallback` and a fallback reason even though the parent orchestrator had
successfully used a subagent.

This made the report ambiguous: the parent/orchestrator truth was `subagent
used`, but the subagent's own runtime-local assessment said fallback.

## Current Replacement

`commands/harness-review.md` now assigns reviewer-mode and fallback ownership
to the parent or orchestrator agent. The subagent prompt explicitly tells the
reviewer subagent not to assess reviewer mode, fallback reason, or subagent
availability, and to return only findings, missing checks, and risks.

Regression coverage in `tests/test_repository_hygiene.py` checks for this
ownership rule and the restricted subagent prompt language.

## Detection Or Prevention Check

`tests/test_repository_hygiene.py` verifies that reviewer mode and fallback
reason remain parent-orchestrator owned, and that reviewer subagent prompts do
not ask subagents to assess reviewer mode, fallback reason, or subagent
availability.

## Agent Guidance

When running `/harness review sub-agent`, decide `Reviewer mode` and `Fallback
reason` from the parent agent's actual availability check and spawn/wait result.
Do not copy those fields from subagent output. Treat subagent output as review
input only: findings, missing checks, and risks.

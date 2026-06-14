---
name: harness-review
description: Review the current change set from an opposing harness-engineering perspective. Use when the user asks for /harness review, /harness review sub-agent, or a no-edit harness review.
argument-hint: "[sub-agent] [focus]"
---

# Harness Review

Challenge the current change set before completion.

## Steps

1. Read `../../references/package-contract.md`.
2. Read `../../references/review-workflow.md`.
3. If `./harness-starter-kit/commands/harness-review.md` exists in the target,
   prefer that canonical workflow.
4. Inspect the current diff and relevant harness guidance.
5. If the request includes `sub-agent`, use a read-only reviewer subagent only
   when the active runtime permits it. Otherwise fall back and report why.
6. Lead with findings by severity. If there are no actionable findings, say so
   clearly and name residual test gaps or risks.

## Boundaries

- Do not modify files unless the user explicitly asks to apply fixes after the
  review.
- Prioritize bugs, source-of-truth risks, overreach, missing checks, stale
  docs, and durable-memory gaps.

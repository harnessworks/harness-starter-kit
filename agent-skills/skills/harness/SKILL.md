---
name: harness
description: Route Harness Starter Kit workflows. Use when the user invokes /harness with adopt, doctor, update, refresh, review, or review sub-agent, or asks to apply, diagnose, maintain, or review repository harness guidance.
argument-hint: "[adopt|doctor|update|refresh|review] [details]"
---

# Harness

Use this as the command router for Harness Starter Kit workflows.

## Steps

1. Read `../../references/package-contract.md`.
2. Identify the requested subcommand:
   - `adopt`, `apply`, or no subcommand with an adoption request:
     read `../../references/adopt-workflow.md`.
   - `doctor`: read `../../references/doctor-workflow.md`.
   - `update`: read `../../references/update-workflow.md`.
   - `refresh`: read `../../references/refresh-workflow.md`.
   - `review` or `review sub-agent`: read
     `../../references/review-workflow.md`.
3. If the target repository has `./harness-starter-kit`, prefer the matching
   canonical workflow doc from that clone over the bundled reference.
4. Execute the selected workflow exactly according to its mutation boundary:
   diagnostic workflows inspect and report; adoption and update workflows may
   edit only when the user asked for that work.
5. Finish with the workflow's required report shape. For substantial harness
   work, say whether task outcome evidence was recorded or skipped and why.

## Subcommand Map

| Request | Workflow |
| --- | --- |
| `/harness adopt` | Apply prompt-first harness engineering to a target repository. |
| `/harness doctor` | Score durable harness evidence without modifying files. |
| `/harness update` | Refresh a target harness from a confirmed kit source. |
| `/harness refresh` | Review stale, duplicated, obsolete, or unused harness guidance. |
| `/harness review` | Challenge the current diff from a harness-engineering perspective. |
| `/harness review sub-agent` | Try the read-only reviewer subagent path, then fall back if unavailable. |

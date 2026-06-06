# 0006. Trigger Task Outcome Evidence For Substantial Harness Work

## Status

Accepted

## Date

2026-06-06

## Context

The kit already separates harness health from agent effectiveness and provides
task outcome records for comparable observations. Recent discussion identified a
workflow gap: the kit could validate adoption reports and effectiveness reports
without making future agent work consistently decide whether an outcome record
was useful evidence.

Recording every agent turn would create paperwork, add noise to future
effectiveness reports, and risk making `AGENTS.md` guidance too heavy. At the
same time, skipping outcome records for substantial harness work would keep the
project strong on harness-health evidence but weak on operational agent-work
evidence.

## Decision

Add a lightweight evidence decision gate for substantial harness work.

Before the final report, agents should decide whether task outcome evidence is
needed when work changes profiles, check scripts, command workflows, adoption
workflow, dogfood or effectiveness evidence, first-pass verification results,
known failure paths, failed CI or harness checks, cross-environment
mismatches, or high-risk integration behavior.

Trivial docs-only wording, typo, link-label, or formatting changes should not
create task outcome records. The final report should state whether task outcome
evidence was recorded or skipped and why.

For harness-maintenance work, default
`include_in_comparable_product_task_count` to false unless the record is a
comparable product-task run intended for an effectiveness report.

Strengthen `scripts/check_effectiveness_plan.py` so included task outcome
records must contain enough evidence to compare later: repository ref, prompt
reference or hash, run id, reviewer, expected boundary, verification command,
and first-pass verification result.

## Rationale

- A trigger-based gate creates operational evidence without turning every task
  into YAML paperwork.
- The rule keeps maintenance work separate from comparable product-task counts,
  preserving the distinction between setup, harness maintenance, and agent
  effectiveness.
- Requiring core fields only for included task outcomes catches records that
  would contaminate later reports while leaving skipped or placeholder records
  cheap.
- The approach extends ADR 0005's dogfood evidence consistency guard without
  creating a new command or broader automatic workflow.

## Alternatives Considered

- Require a task outcome record for every agent task: rejected because it would
  create low-value records and increase agent overhead.
- Add a new `/harness evidence` command immediately: rejected until more
  outcome records show that a separate command is worth maintaining.
- Keep the rule only in final-report prose: rejected because future agents need
  durable trigger guidance and validators need to reject incomplete included
  records.

## Consequences

- Agent guidance now asks for a record-or-skip evidence decision on substantial
  harness work.
- `docs/evaluation.md` documents an operational loop from observed miss to
  durable harness improvement.
- Included task outcome records with missing comparison fields fail local
  validation.
- Harness-maintenance records can still be included in narrative evidence while
  remaining out of comparable product-task counts.

## Agent Guidance

Use the evidence decision gate as a filter, not a quota. Record task outcomes
for substantial harness work and known miss paths. Skip trivial wording or
formatting changes with a short final-report reason.

When a task outcome is included in an effectiveness report, fill the fields
that make the run comparable. Do not set
`include_in_comparable_product_task_count` to true for harness-maintenance,
adoption setup, or review-cleanup records unless the record is a comparable
product-task run.

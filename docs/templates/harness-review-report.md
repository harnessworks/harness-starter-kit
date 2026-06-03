# Harness Review Report

## Reviewed Changes

- Invocation: TODO: /harness review | /harness review sub-agent
- Branch/status: TODO
- Changed files reviewed: TODO
- Review scope: TODO: current diff, staged diff, PR diff, or described change
- Review timing: TODO: pre-commit, pre-push, post-push, or unknown
- Reviewer mode: TODO: subagent used | single-agent fallback
- Fallback reason: TODO: reason or none

Reviewer mode and fallback reason are parent/orchestrator-owned. Fill them from
the actual availability check and subagent spawn/wait result, not from subagent
output.

## Findings

- TODO: list findings with severity and file/path evidence, or state none.

## Missing Checks

- TODO: list validation, tests, lint, type checks, docs drift checks, structure
  checks, or manual checks that should be run before completion.

## Gate Placement

- Normal completion gate reviewed: TODO: command, package script, CI workflow,
  `scripts/check_harness.py`, or other documented default verification path.
- Deterministic behavior checks: TODO: included in the normal gate, excluded
  with reason, or not applicable.
- Focused/manual checks: TODO: checks kept outside the normal gate and why.

## Durable Memory Assessment

- Decision records: TODO: needed, updated, or skipped with reason.
- Decision-docs gate: TODO: if product or workflow structure, input contract,
  input semantics, state normalization, API request/response shape, fallback
  policy, displayed decision criteria, an integration or mock external-behavior
  boundary, a major data model, a state classification, or a product UX
  principle became code structure without a `docs/decisions/` update, state
  whether an existing ADR covers it or why no decision memory is needed.
- Failure records: TODO: needed, updated, or skipped with reason. For each new
  or updated failure record, name the detection/prevention check: regression
  test, fixture, smoke check, lint rule, drift check, CI gate, or manual review
  point that prevents or detects recurrence, or explain why no check is
  practical.
- Conventions/domain/effectiveness docs: TODO: needed, updated, or skipped with
  reason.

## Overreach Risk

- Source-of-truth preservation: TODO
- Unnecessary automation: TODO
- Conservative templates/profile snippets: TODO
- Installer, policy, CI, pre-commit, or runtime-hook risk: TODO

## Manual Decisions Needed

- TODO: list maintainer decisions needed before applying changes, or state none.

## Recommended Follow-Up

1. TODO
2. TODO
3. TODO

## Diagnostic Boundary

This report is diagnostic. It records review findings and follow-up
recommendations, but it does not apply fixes unless the user explicitly asks for
a follow-up implementation.

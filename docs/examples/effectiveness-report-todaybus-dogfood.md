# TodayBus Harness Effectiveness Aggregate Report

## Target

- Repository: `today-bus`
- PR reviewed: [harnessworks/today-bus#2](https://github.com/harnessworks/today-bus/pull/2)
- Merge commit: `85312c181b294c3419dd0813820c10977dd5005b`
- Evaluation window: 2026-06-04 dogfood PR
- Agent or model: Codex
- Reviewer: wb
- Evaluation mode: harnessed-only initial benchmark
- Harness source: [starter-kit commit 7d6fac27](https://github.com/harnessworks/harness-starter-kit/commit/7d6fac27d69229bfc954b662d24dea9984b1bc50)

## Scope

This report counts only product-task dogfood outcomes from TodayBus PR #2.

Excluded non-comparable setup run:

- TodayBus setup outcome record named `dogfood-effectiveness-20260604-160333.yaml`

Reason for exclusion: the original setup prompt used placeholders instead of a
concrete product task, expected boundary, known failure mode, and required
verification commands. It is useful adoption and setup tracking, but it must not
be counted as product-task effectiveness evidence.

## Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `todaybus-homepage-copy-tightening` | Tighten homepage copy while preserving behavior and visual structure. | App and component copy files plus task outcome record. | Broad UI rewrite, behavior change, or missing outcome record. |
| `todaybus-planner-empty-result-test-hardening` | Add deterministic empty-result planner fallback coverage. | Planner tests plus task outcome record. | Product behavior changes for tests, live API use in deterministic tests, or UI edits. |
| `todaybus-domain-planner-terms-alignment` | Clarify planner terminology in domain docs only. | Domain docs plus task outcome record. | App/test edits for docs-only work, duplicated ADR content, or semantic drift. |

## Results

| Metric | Baseline | Harnessed | Delta |
| --- | --- | --- | --- |
| Product-task outcomes counted | Not available | 3 | Initial benchmark only |
| Wrong-file edits | Not available | 0 observed | Inconclusive; no baseline |
| Repeated known mistakes | Not available | 0 observed | Inconclusive; no baseline |
| First-pass verification success | Not available | 3 / 3 | Initial benchmark only |
| Drift violations detected | Not available | 0 observed | Inconclusive; no baseline |
| Human rework minutes | Not available | Unknown | Not measured |
| Reverted files | Not available | 0 observed | Inconclusive; no baseline |

## Non-Comparable Setup Runs

| Run | Reason excluded | Use in metrics |
| --- | --- | --- |
| `dogfood-effectiveness-20260604-160333` | Placeholder prompt lacked a concrete product task, expected boundary, known failure mode, and required verification commands. | Excluded from comparable product-task count |

## Run Log

| Condition | Task ID | Run | Verification result | Notes |
| --- | --- | --- | --- | --- |
| harnessed-only | `todaybus-homepage-copy-tightening` | `todaybus-001-homepage-copy` | passed | Homepage and form copy changed; product behavior and visual structure were preserved. |
| harnessed-only | `todaybus-planner-empty-result-test-hardening` | `todaybus-002-empty-result-tests` | passed | Deterministic non-network planner fallback coverage was added without behavior changes. |
| harnessed-only | `todaybus-domain-planner-terms-alignment` | `todaybus-003-domain-planner-terms` | passed | Domain terminology was clarified without app, test, decision, or failure-record changes. |

## Changed-Files Consistency

| Task ID | Expected boundary | Actual changed files | Wrong-file edit result |
| --- | --- | --- | --- |
| `todaybus-homepage-copy-tightening` | TodayBus app, component, domain-doc, outcome-record, and optional README paths | [src/app/layout.tsx](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/src/app/layout.tsx), [src/app/page.tsx](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/src/app/page.tsx), [src/components/today-bus/search-form.tsx](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/src/components/today-bus/search-form.tsx), and [todaybus-001-homepage-copy.yaml](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/todaybus-001-homepage-copy.yaml) | 0 observed |
| `todaybus-planner-empty-result-test-hardening` | TodayBus test, library, domain-doc, and outcome-record paths | [tests/planner-branches.test.mjs](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/tests/planner-branches.test.mjs) and [todaybus-002-empty-result-tests.yaml](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/todaybus-002-empty-result-tests.yaml) | 0 observed |
| `todaybus-domain-planner-terms-alignment` | TodayBus domain-doc and outcome-record paths | [docs/domain/glossary.md](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/domain/glossary.md), [docs/domain/tago-api.md](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/domain/tago-api.md), [docs/domain/gumi-bis.md](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/domain/gumi-bis.md), and [todaybus-003-domain-planner-terms.yaml](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/todaybus-003-domain-planner-terms.yaml) | 0 observed |

## Source Records

- Task outcome records reviewed:
  - [TodayBus setup record `dogfood-effectiveness-20260604-160333.yaml`](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/dogfood-effectiveness-20260604-160333.yaml), excluded from product-task counts
  - [TodayBus record `todaybus-001-homepage-copy.yaml`](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/todaybus-001-homepage-copy.yaml)
  - [TodayBus record `todaybus-002-empty-result-tests.yaml`](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/todaybus-002-empty-result-tests.yaml)
  - [TodayBus record `todaybus-003-domain-planner-terms.yaml`](https://github.com/harnessworks/today-bus/blob/85312c181b294c3419dd0813820c10977dd5005b/docs/effectiveness/task-outcomes/todaybus-003-domain-planner-terms.yaml)
- Repository refs compared: [TodayBus PR #2](https://github.com/harnessworks/today-bus/pull/2), merge commit `85312c181b294c3419dd0813820c10977dd5005b`
- Prompt refs compared: local dogfood prompts from 2026-06-04
- Verification commands compared:
  - `npm run check:harness`
  - `npm run test:planner`
  - `git diff --check`
  - local HTTP smoke for the homepage copy run

## Interpretation

### Observed benchmark

The TodayBus dogfood PR produced three harnessed-only product-task observations.
In this window, the agent stayed within the requested task boundaries, avoided
the listed known failure modes, recorded task outcomes, and completed the
required verification commands.

### What improved

No improvement claim is made. This report has no comparable pre-harness
baseline or later comparison window.

### What did not improve

Human rework minutes were not measured, so this report cannot assess whether
review effort decreased. The runs also came from one PR and one short dogfood
window, so session and reviewer effects may be mixed into the result.

### Confounders or limitations

- This is a harnessed-only initial benchmark, not a controlled experiment.
- The setup run is excluded from product-task metrics.
- The sample size is small.
- The reviewer supplied strong boundary, known-failure, and verification
  instructions, so the result does not show how the agent would behave under a
  looser prompt.
- Prompt text and prompt hashes were not preserved as stable artifacts, so the
  prompt references are weaker than the repository and outcome-record refs.

### Narrow claim

This report establishes an initial TodayBus dogfood benchmark for boundary
adherence, first-pass verification, and outcome-record completeness.

It does not prove that harness adoption improved agent effectiveness.

### Human rework interpretation

Human rework is unknown, not 0. Future runs should record reviewer time or
review findings if the project wants to evaluate rework cost.

## Follow-Up

- Next review window: next 3-5 comparable TodayBus product tasks.
- Owner or reviewer: maintainer or dogfood reviewer.
- Related decision or failure records: TodayBus PR #2 task outcome records and
  the repo-local effectiveness tracking decision.
- Harness changes to make next: none required for this report; the starter-kit
  template now separates non-comparable setup runs from comparable product-task
  counts.

# Harness Effectiveness Evaluation

Use this protocol to measure whether harness adoption reduces repeated agent
mistakes in a target repository.

Smoke tests and fixture tests prove that starter-kit files can be installed and
that drift checks can run. They do not prove that the harness improves agent
outcomes. Effectiveness should be measured with comparable tasks before and
after adoption, or with harnessed-only tracking when no baseline is available.

## Two Measurement Layers

Keep these layers separate:

- Harness health: automatically measurable repository evidence, such as durable
  agent instructions, runnable checks, drift scripts, CI wiring, source
  tracking, and complete adoption reports. Harness Doctor and local validation
  checks belong here.
- Agent effectiveness: human-recorded task outcomes, such as wrong-file edits,
  repeated known mistakes, first-pass verification, drift detections, human
  rework, and reverted files. Effectiveness reports and task outcome records
  belong here.

A healthier harness can make better agent outcomes more likely, but it is not
proof of those outcomes. Do not treat a Harness Doctor score, fixture test, or
passing drift check as evidence that agents made fewer mistakes.

## Evaluation Questions

- Did agents edit fewer wrong files?
- Did agents repeat fewer previously documented mistakes?
- Did first-pass verification succeed more often?
- Did drift checks catch architecture or structure violations earlier?
- Did maintainers spend less time reverting or reworking agent changes?

## Conditions

Use one of these modes:

- Baseline versus harnessed: compare the same or similar tasks before and after
  harness adoption.
- Harnessed-only tracking: when no baseline exists, record the next comparable
  agent tasks after adoption and use those results as the initial benchmark.

Record the mode in the effectiveness report. Do not infer improvement from
harnessed-only tracking until there is a later comparison point.

Separate non-comparable setup runs from product-task outcomes. Adoption,
template setup, placeholder-prompt, or other workflow-preparation records can be
useful operational evidence, but they should not enter comparable product-task
counts unless they had a concrete task, expected boundary, known failure mode,
and verification command.

## Metrics

| Metric | Definition | Example observation |
| --- | --- | --- |
| Wrong-file edits | Files changed outside the intended task boundary. | Agent touched generated files while editing UI copy. |
| Repeated mistakes | Mistakes already documented in `AGENTS.md`, `docs/failures`, or decision records. | Agent added direct database access from a route after the rule existed. |
| First-pass verification | Whether documented checks passed before human correction. | `npm test` and `npm run lint` both passed. |
| Drift violations detected | Violations caught by harness checks. | Forbidden import, temporary file, or broken docs link found. |
| Human rework | Maintainer time spent reverting, rewriting, or explaining the same issue. | Reviewer spent 20 minutes undoing misplaced files. |
| Reverted files | Files removed or restored by a human reviewer. | Two generated files reverted from the PR. |

## Protocol

1. Pick 3 to 5 realistic tasks that represent common agent work in the target
   repository.
2. For each task, define the expected file boundary and the known failure mode
   the harness should prevent or surface.
3. Run each task at least 5 times per condition when practical.
4. Use the same task prompt, repository state, verification command, and review
   criteria for each comparable run.
5. Record observable outcomes only. Do not count intentions or explanations as
   successful behavior.
6. Store aggregate results in an effectiveness report using
   `docs/templates/effectiveness-report.md`. For individual manual observations,
   copy `docs/templates/task-outcome.yaml` and store filled records under the
   target repository's docs/effectiveness/task-outcomes directory.
7. For each task outcome record, include the repository ref, prompt reference,
   run id, reviewer, harness source, and verification command so later reviewers
   can tell whether two runs are actually comparable.
8. In aggregate reports, compare expected boundaries with actual changed files,
   distinguish unknown human rework from 0 minutes, and treat
   `include_in_effectiveness_report` as separate from inclusion in comparable
   product-task counts.

## Operational Evidence Loop

Use task outcome records as a lightweight operational loop, not as mandatory
paperwork for every agent turn.

Before the final report for substantial harness work, decide whether a task
outcome record is needed. Record one when the work changes profiles, check
scripts, command workflows, adoption workflow, dogfood evidence, effectiveness
evidence, first-pass verification results, known failure paths, failed CI or
harness checks, cross-environment mismatches, or high-risk integration behavior
such as external APIs, secrets, permissions, command gates, or runtime
verification.

Skip task outcome records for trivial docs-only wording, typo, link-label, or
formatting changes. The final report should still say whether evidence was
recorded or skipped and why.

When a recorded outcome shows a miss, convert the observation into the smallest
durable harness improvement that fits:

| Observation | Durable follow-up |
| --- | --- |
| Wrong-file edit | Directory rule, structure check, or clearer agent instruction |
| Repeated known mistake | Failure record, stronger regression check, or cited existing failure note |
| First-pass verification failure | Test, smoke check, gate-placement update, or validation-command fix |
| Missing decision-memory review | Decision record, existing ADR citation, or tuned decision-memory rule |
| Stale or duplicated guidance | `/harness refresh` candidate |
| Live or fragile check confusion | Focused/manual gate-placement reason |
| Command mismatch | Docs drift fix, command validator coverage, or normal-gate update |

For harness-maintenance work, default
`include_in_comparable_product_task_count` to false. Set it to true only for
comparable product-task runs that are intended to be counted in an effectiveness
report. Once several comparable outcomes exist, aggregate them with
`docs/templates/effectiveness-report.md` and keep setup or maintenance runs
separate from product-task counts.

## Minimum Adoption-Time Plan

When adopting the harness into a new target repository, the agent should fill an
effectiveness measurement plan even if no baseline data exists yet:

- whether baseline data is available
- which tasks should be repeated or tracked
- the primary metric for the target repository
- the review window, such as the next 5 agent PRs
- where future results should be recorded

If measurement is not possible yet, state why and name the next observable event
that will make measurement possible.

## Interpretation

Treat the data as operational evidence, not a controlled scientific study. Small
repositories and changing agents can introduce noise. The useful signal is
whether the same classes of mistakes become less frequent, easier to detect, or
cheaper to correct after the harness becomes part of the repository.

## Example Evidence Passes

- [Small harness outcome evidence report](examples/effectiveness-report-small-evidence.md) records three harnessed task outcomes and summarizes a narrow operational evidence pass without treating Harness Doctor scores or passing checks as proof of agent effectiveness.
- [TodayBus harnessed-only dogfood benchmark](examples/effectiveness-report-todaybus-dogfood.md) records three product-task outcomes, excludes a non-comparable setup run, and treats the result as an initial benchmark rather than proof of effectiveness improvement.
- [Harness ERP Spring/Maven dogfood benchmark](examples/effectiveness-report-harness-erp-dogfood.md) records five initial backend, four backend follow-up, and five frontend follow-up product-task outcomes, one honest boundary miss, frontend first-pass failures, prompt hashes, failure-memory linkage, source tracking, browser smoke, and CI verification evidence while keeping harnessed-only observations separate from effectiveness-improvement claims.

Before adding a new dogfood report to this kit, use
[`docs/checklists/dogfood-evidence-adoption.md`](checklists/dogfood-evidence-adoption.md)
to verify source tracking, task outcomes, failure memory, gate placement, and
claim boundaries.

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
- [Harness ERP Spring/Maven dogfood benchmark](examples/effectiveness-report-harness-erp-dogfood.md) records five backend product-task outcomes, one honest boundary miss, prompt hashes, failure-memory linkage, and source tracking as initial benchmark evidence rather than proof of effectiveness improvement.

Before adding a new dogfood report to this kit, use
[`docs/checklists/dogfood-evidence-adoption.md`](checklists/dogfood-evidence-adoption.md)
to verify source tracking, task outcomes, failure memory, gate placement, and
claim boundaries.

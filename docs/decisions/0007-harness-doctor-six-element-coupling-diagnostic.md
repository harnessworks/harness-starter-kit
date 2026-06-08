# 0007. Extend Harness Doctor To Six-Element Coupling Diagnostics

## Status

Accepted

## Date

2026-06-08

## Context

Harness Doctor originally scored five baseline evidence categories: agent
instructions, feedback loops, durable memory, structural safety, and adoption
clarity. That scan was useful for early adoption, but it did not score the full
repository harness model:

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

The five-category score also made some important relationships implicit. A
check script can represent both a declared constraint and a feedback loop. A
failure record is useful memory only when future agents can find it and when a
regression check, fixture, CI gate, or manual review point can detect
recurrence. Governance signals such as diagnostic-only commands, approval
gates, source tracking, and review timing were reviewed manually but not visible
in the primary score.

At the same time, the kit must preserve the distinction between harness health
and agent effectiveness. A Doctor score should show durable repository
readiness and coupling gaps. It must not claim that agents make fewer mistakes
unless task outcome records or effectiveness reports provide that evidence.

## Decision

Extend Harness Doctor from a five-category baseline scan to a six-element
diagnostic over Instructions, Constraints, Feedback, Memory, Evaluation, and
Governance.

Doctor should report:

- an overall harness health score
- per-element scores
- signal status for each element
- first-class coupling findings between elements
- an explicit note that Proven/effectiveness signals remain unmeasured unless
  task outcome or effectiveness evidence exists

Use different signal names for structural and control elements:

| Element type | Elements | Signals |
| --- | --- | --- |
| Structural | Instructions, Constraints, Memory | Stated or Recorded, Routed or Enforced or Operationalized, Proven |
| Control | Feedback, Evaluation, Governance | Exists, Coverage, Proven |

Do not include Proven effectiveness in the initial score. Report it as
unmeasured unless durable task outcome or effectiveness evidence exists.

Treat check scripts as a Constraint and Feedback join:

- the rule or invariant represented by the script belongs to Constraints
- the execution path, CI wiring, local command, or report output belongs to
  Feedback

Report coupling findings as first-class output. Initial finding types are:

- orphan Constraint: a declared invariant exists without a feedback binding
- orphan Feedback: a check or workflow signal exists without a clear local
  rule, script, or purpose
- unoperationalized Memory: durable memory exists without instruction, check,
  review, or recurrence-detection linkage
- unevaluated Memory: decisions or failures exist without task outcome or
  effectiveness evidence
- ungoverned change type: risky change categories lack a documented approval,
  review, or maintenance path
- promotion gap: repeated failure memory may need promotion into instructions,
  conventions, constraints, or checks

Keep Harness Doctor diagnostic by default. A future or current CLI gate such as
`--min-score` or `--fail-on critical-coupling` may be supported, but must be
off unless explicitly requested by the caller.

## Rationale

- The six-element model is the kit's repository-local operating model and is
  easier for target repositories to act on than a runtime-layer taxonomy.
- Coupling findings are more actionable than a flat score because they point to
  broken loops between rules, checks, memory, evaluation, and governance.
- Keeping Proven outside the initial score preserves the existing claim
  boundary: Doctor scores harness health, not agent effectiveness.
- Explicitly modeling check scripts as Constraint and Feedback joins avoids
  double-counting while still surfacing whether a rule is only declared or is
  actually wired into a feedback path.
- Optional gates let CI consumers fail on concrete health gaps without turning
  the default diagnostic command into a policy enforcer.

## Consequences

- `scripts/harness_doctor.py` reports six elements instead of the old five
  categories.
- `commands/harness-doctor.md`, the scoring rubric, and example reports must
  describe the six-element score and coupling findings.
- Tests must cover the new report contract, diagnostic non-modification
  behavior, coupling finding detection, and optional gate behavior.
- Existing references that say Doctor does not prove agent effectiveness remain
  true and should be preserved.
- The implementation should avoid pretending to inspect runtime-only execution
  sandboxes or tool protocols. It may score only repository-visible execution
  assumptions such as local commands, CI wiring, scripts, and documented
  approval paths.

## Known Limits And Follow-Up

- Early coupling findings are necessarily heuristic. A warning should identify
  the durable evidence it found and the review question it raises instead of
  claiming certainty beyond the repository scan.
- Promotion gaps are especially hard to infer mechanically and should start as
  manual-review findings.
- Equal element weighting should be the default until enough task outcome and
  dogfood evidence exists to justify different weights.
- Proven effectiveness can be integrated later without changing the structural
  probes if task outcome records become numerous and consistent enough.

## Agent Guidance

When changing Doctor behavior, keep the score focused on durable repository
health. Do not count passing checks, fixture coverage, or Harness Doctor scores
as proof of reduced agent mistakes. If a finding points to a repeated failure,
connect it to a regression test, fixture, smoke check, lint rule, drift check,
CI gate, or manual review point before treating it as closed.

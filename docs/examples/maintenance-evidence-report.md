# Harness Maintenance Evidence Report

## Target

- Repository: [harnessworks/harness-starter-kit](https://github.com/harnessworks/harness-starter-kit)
- Stack and framework: Python and Markdown harness kit
- Evaluation date or window: 2026-06-06 through 2026-06-07
- Agent or model: Codex with primary-agent and subagent review loops
- Evaluation mode: harness-maintenance evidence aggregation

## Primary Metric

The primary metric for this pass is whether task outcome records helped expose
maintenance-work quality signals that are worth preserving across future
harness changes.

This report reviews substantial harness-maintenance records only. It does not
count these records as product-task effectiveness evidence and does not claim
that the harness reduces agent mistakes in target repositories.

## Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `harness-starter-kit-004` | Add a task outcome evidence decision gate. | Agent instructions, evaluation docs, decision memory, checker, tests, and one task outcome record. | Evidence becomes mandatory paperwork or contaminates comparable product-task counts. |
| `harness-starter-kit-005` | Validate root `make` and `just` command references. | Failure/effectiveness checkers, template copies, focused tests, decision/roadmap docs, and one task outcome record. | Fake `make` or `just` commands look concrete but are not declared in the target repository. |
| `harness-starter-kit-006` | Validate Maven, Gradle, and Go command references. | Failure/effectiveness checkers, template copies, focused tests, decision/roadmap docs, and one task outcome record. | Maven, Gradle, or Go commands look concrete but do not match root project markers or wrappers. |

## Results

| Metric | Harness-maintenance observations | Interpretation |
| --- | ---: | --- |
| Records reviewed | 3 | Enough for a first maintenance aggregation, not enough to add a new command. |
| Comparable product-task outcomes counted | 0 | Correct; all three records are harness-maintenance observations. |
| Wrong-file edits | 0 observed | The expected-boundary fields were useful for scope review. |
| Repeated known mistakes | 0 observed | No record repeated a documented failure as the final outcome. |
| First-pass verification success | 1 passed, 2 failed-then-passed | The loop surfaced real implementation and evidence gaps before completion. |
| Drift violations detected | 0 recorded | Drift checks passed after fixes; no structural drift became a recorded miss. |
| Human rework minutes | 0 recorded | These records used agent review/fix loops; they do not measure maintainer rework cost. |
| Reverted files | 0 recorded | No final reverted-file cleanup was needed. |
| Real-project smoke evidence | 1 record | The third checker pilot moved beyond synthetic fixtures for Go and Spring Maven/Gradle. |

## Run Log

| Condition | Task ID | Verification result | Review signal preserved |
| --- | --- | --- | --- |
| harness-maintenance | `harness-starter-kit-004` | passed | The record confirms trigger-based evidence and keeps maintenance work out of comparable product-task counts. |
| harness-maintenance | `harness-starter-kit-005` | failed-then-passed | The record preserves regex/test gaps, task-outcome false-inclusion validation, make precedence, just parameter parsing, and final validation scope. |
| harness-maintenance | `harness-starter-kit-006` | failed-then-passed | The record preserves missing full-validation evidence, Go marker ambiguity, wrapper flavor mismatch, case sensitivity, Windows subpath false positives, stale roadmap language, and real Go/Spring smoke validation. |

## Source Records

- Task outcome records reviewed:
  - [`004-evidence-decision-gate.yaml`](task-outcomes/004-evidence-decision-gate.yaml)
  - [`005-make-just-command-validation.yaml`](task-outcomes/005-make-just-command-validation.yaml)
  - [`006-maven-gradle-go-command-validation.yaml`](task-outcomes/006-maven-gradle-go-command-validation.yaml)
- Related decision records:
  - [`0004-link-failure-memory-to-regression-checks.md`](../decisions/0004-link-failure-memory-to-regression-checks.md)
  - [`0006-trigger-task-outcome-evidence-for-substantial-harness-work.md`](../decisions/0006-trigger-task-outcome-evidence-for-substantial-harness-work.md)
- Related failure records:
  - [`0005-failure-memory-was-not-linked-to-regression-checks.md`](../failures/0005-failure-memory-was-not-linked-to-regression-checks.md)
  - [`0007-dogfood-first-pass-failures-lacked-memory-decision.md`](../failures/0007-dogfood-first-pass-failures-lacked-memory-decision.md)
- Repository refs compared:
  - `13fa9d822b1627243d91a50700c188ff4d32470d`
  - `e98b6f40f134bcacbab0bb9cb12178f1e071bb63`
  - `d3b9732922457ca1cd388145e4aab01773976563`
- Verification commands compared:
  - `python3 -m unittest tests.test_check_effectiveness_plan`
  - `python3 -m unittest tests.test_repository_hygiene`
  - `python3 -m unittest tests.test_check_failure_memory tests.test_check_effectiveness_plan tests.test_repository_hygiene`
  - `python3 -m unittest discover -s tests`
  - `python3 -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/check_failure_memory.py scripts/check_decision_memory.py scripts/harness_doctor.py`
  - `python3 scripts/check_docs_drift.py`
  - `python3 scripts/check_structure.py`
  - `python3 scripts/check_encoding_hygiene.py`
  - `python3 scripts/check_effectiveness_plan.py`
  - `python3 scripts/check_failure_memory.py`
  - `python3 scripts/check_decision_memory.py`
  - `python3 scripts/harness_doctor.py --target .`

## Interpretation

### What the evidence loop did well

- It preserved why checker changes were made, not just which files changed.
- It forced harness-maintenance records to stay out of comparable product-task
  counts.
- It made first-pass verification failures visible instead of letting the final
  passing state erase the review trail.
- It created stable follow-up language for command-reference validation limits.
- It encouraged stronger validation on the third checker pilot, including real
  temporary Go and Spring Framework Maven/Gradle projects.

### What the evidence loop did not prove

- It did not prove product-agent effectiveness or reduced mistake rates in a
  target repository.
- It did not measure maintainer rework cost; `human_rework_minutes: 0` should
  be interpreted as "no recorded human rework", not as a productivity result.
- It did not yet test the evidence shape on profile updates, governance-command
  refinements, or dogfood adoption updates.

### Harness changes justified by this pass

- Keep the task outcome gate trigger-based. The current records are useful when
  substantial work changes checks, workflows, runtime verification, or evidence
  boundaries.
- Do not add `/harness evidence` yet. Three maintenance records are enough to
  show the loop can work, but they are not varied enough to justify a command.
- Add a small `Task Outcome Evidence` line to report templates only after at
  least one non-checker pilot confirms the wording is still useful.
- Prefer future pilots that are not checker-only: a profile update,
  governance-command refinement, or dogfood adoption/update.

### Narrow claim

This pass provides operational evidence that task outcome records are useful
for preserving review findings and validation scope during substantial
harness-maintenance work.

It does not prove that harness adoption improves agent effectiveness in target
repositories.

## Follow-Up

- Next review window: after at least two more substantial harness changes, with
  at least one profile update or dogfood adoption/update.
- Owner or reviewer: maintainer or harness reviewer.
- Recommended next pilot: strengthen one profile with fixture-backed smoke
  coverage and record whether the task outcome shape still captures useful
  review evidence.
- Defer: `/harness evidence` command, until the next pilots show repeated
  manual reporting pain or a stable minimum field set.

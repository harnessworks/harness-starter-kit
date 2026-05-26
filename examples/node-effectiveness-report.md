# Example Effectiveness Report: Node JavaScript Target

This is an illustrative report shape for the sample Node.js target. The numbers
below are example observations, not benchmark claims for all repositories.

## Target

- Repository: `sample-task-tracker`
- Stack and framework: Node.js ES modules
- Evaluation date or window: example 5-run baseline and 5-run harnessed window
- Agent or model: coding agent under the same task prompt
- Evaluation mode: baseline versus harnessed

## Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| NODE-1 | Add a small math utility and test. | `src/` and `test/` only. | Editing docs or package metadata unnecessarily. |
| NODE-2 | Update README usage text. | `README.md` only. | Touching source files during a docs-only task. |
| NODE-3 | Add a failing-test fix. | Minimal source and matching test file. | Leaving temporary debug files behind. |

## Results

| Metric | Baseline | Harnessed | Delta |
| --- | ---: | ---: | ---: |
| Wrong-file edits | 6 | 2 | -4 |
| Repeated mistakes | 4 | 1 | -3 |
| First-pass verification success | 2/5 | 4/5 | +2 |
| Drift violations detected | 0 | 3 | +3 |
| Human rework minutes | 45 | 15 | -30 |
| Reverted files | 5 | 1 | -4 |

## Run Log

| Condition | Task ID | Run | Verification result | Notes |
| --- | --- | ---: | --- | --- |
| Baseline | NODE-1 | 1 | Failed | Added a utility but left `src/temp_debug.js`. |
| Baseline | NODE-2 | 2 | Passed after review | Edited source during a docs-only task. |
| Harnessed | NODE-1 | 1 | Failed fast | `scripts/check_structure.py` caught `src/temp_debug.js`. |
| Harnessed | NODE-2 | 2 | Passed | README-only boundary was preserved. |
| Harnessed | NODE-3 | 3 | Passed | Source and test changes stayed scoped. |

## Interpretation

- What improved: wrong-file edits, temporary-file drift, and first-pass
  verification success improved in this example window.
- What did not improve: one harnessed run still required human review for an
  overbroad source edit.
- Confounders or limitations: small sample size, illustrative task set, and no
  guarantee that future tasks are equally comparable.
- Harness changes to make next: add a docs-only task checklist and keep the
  temporary-file structure check wired into the local check command.

## Follow-Up

- Next review window: next 5 comparable Node.js agent changes.
- Owner or reviewer: target repository maintainer.
- Related decision or failure records:
  `docs/failures/001-temp-debug-files.md` and
  `docs/decisions/001-adopt-agent-harness.md`.

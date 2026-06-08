# Harness Doctor Example Reports

These examples show the expected Doctor v2 report shape. Scores are
illustrative baseline health scans; real scores must come from inspecting
durable repository evidence and reviewing content quality.

## Weak Repository Example

```text
Harness Doctor Report

Score: 43/100 (six-element baseline coupling scan)
Grade: D (baseline)

Verdict:
This repository has a README and a test command, but most harness loops still
depend on human memory. Instructions are thin, constraints are not wired into a
feedback path, memory is missing, and governance is mostly unstated.

Element Breakdown:
- Instructions: 45/100 | Stated partial · Routed weak · Proven unmeasured
- Constraints: 20/100 | Stated weak · Enforced missing · Proven unmeasured
- Feedback: 55/100 | Exists partial · Coverage weak · Proven unmeasured
- Memory: 10/100 | Recorded missing · Operationalized missing · Proven unmeasured
- Evaluation: 35/100 | Exists weak · Coverage missing · Proven unmeasured
- Governance: 40/100 | Exists partial · Coverage weak · Proven unmeasured

Coupling Findings:
- warning Orphan Constraint: README says generated files should not be edited,
  but no ignore rule, drift check, CI gate, or manual review point was found.
- warning Ungoverned Change Type: no approval path was found for deleting,
  moving, or overwriting project files.

Evidence:
- README.md includes a quickstart and `npm test`.
- package.json defines a test script.
- No AGENTS.md, CLAUDE.md, Cursor rules, or Copilot instructions were found.
- No `docs/decisions` or `docs/failures` records were found.
- No structure, docs drift, failure-memory, or decision-memory checks were
  found.

Missing Or Weak Baseline Items:
- Instructions: add an agent instruction entry point with exact commands and
  boundaries.
- Constraints: add at least one project-specific structural or drift rule.
- Memory: add decision or failure memory when a recurring mistake appears.
- Governance: document approval requirements for destructive or broad changes.

Non-Scored Manual Review:
- Proven effectiveness: unmeasured; no task outcome or effectiveness report was
  found.
- Runtime execution/tooling: out of scope except for repository-visible local
  commands.

Top Risks:
1. New agents may miss project-specific constraints because durable agent
   instructions are missing.
2. Repeated mistakes may recur because failures and rejected approaches are not
   recorded.
3. Temporary files or misplaced generated files may drift into the repository
   because no structural check exists.

Recommended Next Actions:
1. Add AGENTS.md with project overview, exact commands, boundaries, forbidden
   actions, and safety notes.
2. Add docs/failures or docs/decisions when the next repeated mistake or
   architectural choice appears.
3. Add lightweight docs and structure drift checks, then wire them into CI or a
   local validation command.
```

## Stronger Repository Example

```text
Harness Doctor Report

Score: 84/100 (six-element baseline coupling scan)
Grade: B+ (baseline)

Verdict:
This repository has a strong practical harness. A new agent can find project
rules, validation commands, durable memory, and review paths without relying on
chat history. The main remaining gap is that some memory records are not yet
linked to outcome evidence.

Element Breakdown:
- Instructions: 92/100 | Stated strong · Routed strong · Proven unmeasured
- Constraints: 82/100 | Stated strong · Enforced partial · Proven unmeasured
- Feedback: 86/100 | Exists strong · Coverage strong · Proven unmeasured
- Memory: 88/100 | Recorded strong · Operationalized strong · Proven unmeasured
- Evaluation: 70/100 | Exists strong · Coverage partial · Proven unmeasured
- Governance: 88/100 | Exists strong · Coverage strong · Proven unmeasured

Coupling Findings:
- warning Unevaluated Memory: docs/failures contains 3 real records, but no
  task outcome record or effectiveness report links those failures to observed
  recurrence reduction.
- info Promotion Gap: review whether the repeated migration failure should also
  be summarized in docs/conventions/coding.md.

Evidence:
- AGENTS.md exists and includes overview, exact commands, forbidden actions,
  safety notes, and links to decisions and failures.
- CI runs tests, linting, typechecking, docs drift, and structure checks.
- docs/decisions contains real ADRs and docs/failures contains production bug
  write-ups with detection checks.
- scripts/check_failure_memory.py validates recurrence-detection linkage.
- docs/evaluation.md and docs/templates/task-outcome.yaml exist.
- commands/harness-review.md and commit/PR guidance document review paths.

Missing Or Weak Baseline Items:
- Evaluation: task outcome records exist only as templates; no comparable
  outcome evidence was found.
- Constraints: one documented architecture boundary has no import or dependency
  check yet.

Non-Scored Manual Review:
- Proven effectiveness: unmeasured; existing reports should not be treated as
  proof of reduced mistakes until comparable outcomes exist.
- Runtime execution/tooling: local commands and CI are visible; runtime
  sandbox/tool protocol behavior is out of scope for this repository scan.

Top Risks:
1. Agents may violate one architecture boundary because it is documented but
   not enforced by linting, tests, CI, or a manual review point.
2. Durable failure memory exists but is not yet connected to comparable outcome
   evidence.
3. Runtime sandbox and tool-protocol assumptions are outside the repository
   score and should be reviewed in the agent runtime separately.

Recommended Next Actions:
1. Add an import or dependency boundary check for the documented architecture
   layer.
2. Record task outcomes for the next comparable agent tasks and aggregate them
   in an effectiveness report.
3. Review whether repeated failure patterns should be promoted into
   conventions, instructions, or checks.
```

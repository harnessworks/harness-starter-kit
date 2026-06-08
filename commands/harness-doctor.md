# /harness doctor

Run Harness Doctor to evaluate how ready the current repository is for reliable
AI coding agent collaboration.

Harness Doctor is diagnostic only. Do not create, edit, delete, move, format, or
stage files while running this command.

Do not remove a nested `./harness-starter-kit` directory from the target
repository while running this command. If you created a temporary clone outside
the target repository, such as under `/tmp`, you may remove only that temporary
copy after the report is complete.

## Goal

Inspect the repository and produce a Harness Score out of 100. The score should
identify weak points where AI coding agents are likely to repeat mistakes across
sessions. It is a harness health diagnostic, not proof of agent effectiveness
or mistake reduction.

## Scope

Harness Doctor scores the six-part repository harness model in
`docs/theory/harness-engineering.md`:

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

The score is a harness health and coupling diagnostic. It checks durable
repository evidence for the six elements and reports broken links between
rules, checks, memory, evaluation, and governance. It does not prove agent
effectiveness or mistake reduction.

Doctor may report task outcome records and effectiveness reports as evidence
that the Evaluation element exists. It must not count those records as proof
that agents improved unless the report explicitly includes comparable outcome
evidence. Runtime-only execution sandboxes and tool protocols are outside the
score unless their assumptions are visible in repository files, commands, CI, or
approval rules.

Use this principle when judging the repository:

> Prompting is temporary. Context is session-scoped. A harness is project-scoped.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect durable repository files, not chat context.
3. If `./harness-starter-kit` exists, treat it as read-only reference material.
   Do not delete it, ignore it, move it, or clean it up as part of the doctor
   run.
4. Read likely harness files:
   - `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`, `.github/copilot-instructions.md`
   - `README.md`, `CONTRIBUTING.md`, project docs, and CI configs
   - `docs/decisions`, `docs/failures`, `docs/conventions`, and `docs/domain`
   - `scripts/`, package manager config, test config, lint config, and pre-commit config
5. If available, run a baseline scan:

   ```bash
   python scripts/harness_doctor.py --target .
   ```

   Treat this script output as objective baseline evidence only. You must still
   review content quality and enforceability yourself.

6. Score the repository across the six elements below.
7. Review coupling findings between elements.
8. Produce the required report format.

## Scoring Rules

Be strict.

- Do not give points for intent alone.
- Do not give points for instructions that exist only in chat.
- Award points for durable files, executable checks, clear documentation, and
  validation that a future agent can find without this conversation.
- Partial credit is allowed only when the durable artifact is present but weak.
- If you cannot find evidence for an item, give 0 for that item.
- If a check exists but is not documented or wired into a normal workflow, count
  the script as constraint evidence but report the missing feedback binding.
- If a workflow runs a check whose rule, local script, or purpose is unclear,
  report it as a possible orphan feedback signal.

Use the detailed rubric in `docs/scoring/harness-score-rubric.md`.

## Elements

Total score: 100 points.

- Instructions
- Constraints
- Feedback
- Memory
- Evaluation
- Governance

Each element is scored on repository-visible health signals. Proven
effectiveness is shown as unmeasured unless durable task outcome or
effectiveness evidence exists; it is not part of the default score.

## Required Report Format

```text
Harness Doctor Report

Score: <score>/100
Grade: <grade>

Verdict:
<one short paragraph explaining what the score means>

Element Breakdown:
- Instructions: <points>/100 | Stated <status> · Routed <status> · Proven <status>
- Constraints: <points>/100 | Stated <status> · Enforced <status> · Proven <status>
- Feedback: <points>/100 | Exists <status> · Coverage <status> · Proven <status>
- Memory: <points>/100 | Recorded <status> · Operationalized <status> · Proven <status>
- Evaluation: <points>/100 | Exists <status> · Coverage <status> · Proven <status>
- Governance: <points>/100 | Exists <status> · Coverage <status> · Proven <status>

Coupling Findings:
- <severity> <finding type>: <evidence and review question>

Evidence:
- <durable evidence found in the repository>
- <durable evidence found in the repository>
- <missing or weak evidence that affected the score>

Non-Scored Manual Review:
- Proven effectiveness: <task outcomes, effectiveness reports, or unmeasured>
- Runtime execution/tooling: <repo-visible assumptions only, or out of scope>

Top Risks:
1. <highest-impact risk>
2. <next risk>
3. <next risk>

Recommended Next Actions:
1. <concrete durable improvement>
2. <concrete durable improvement>
3. <concrete durable improvement>
```

## Grade Scale

```text
90-100: A / Production-ready harness
80-89: B+ / Strong harness
70-79: B / Useful but incomplete
60-69: C / Basic harness
40-59: D / Mostly ad-hoc
0-39: F / No durable agent harness
```

## Final Check

Before answering, confirm that your report names repository evidence for every
major score decision. The report should help the maintainer decide what durable
harness artifact to add next.

Also confirm that you did not modify the target repository. If you used a
temporary clone outside the target repository and removed it, say that
explicitly. Do not describe removal of `./harness-starter-kit` as cleanup unless
the user explicitly asked for that deletion.

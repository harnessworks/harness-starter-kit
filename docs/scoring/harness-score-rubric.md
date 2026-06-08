# Harness Score Rubric

Harness Score measures how ready a repository is for reliable AI coding agent
collaboration.

The goal is not to gamify documentation. The goal is to find weak points where
AI coding agents are likely to repeat mistakes because guidance, constraints,
memory, validation loops, evaluation evidence, or governance paths are missing
from the repository.

## Scoring Principles

- Score durable repository artifacts, not chat instructions.
- Prefer executable checks over requests for discipline.
- Prefer project-specific rules over generic advice.
- Report broken links between rules, checks, memory, evaluation, and governance.
- Award partial credit for weak but real evidence.
- Give 0 when evidence is absent, only implied, or known only from conversation.
- Record missing evidence in the report so the maintainer knows what to improve.

## Score Scope

This 100-point score covers six repository harness elements:

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

The score is a harness health and coupling diagnostic. It is not an agent
effectiveness score. Task outcomes, effectiveness reports, and task outcome
records are evidence that Evaluation exists, but they do not prove reduced
agent mistakes unless they contain comparable outcome evidence.

Harness Doctor also reports coupling findings. These findings may matter more
than the raw score because they show where the harness loop is broken, such as
a rule without a check, a check without a clear rule, or a failure record
without recurrence detection.

Runtime-only execution sandboxes and tool protocols are outside this repository
score unless their assumptions are visible in local commands, CI, scripts,
documentation, or approval paths.

## Signal Model

Structural elements use repository artifact signals:

| Element | Signals |
| --- | --- |
| Instructions | Stated, Routed, Proven |
| Constraints | Stated, Enforced, Proven |
| Memory | Recorded, Operationalized, Proven |

Control elements use capability and coverage signals:

| Element | Signals |
| --- | --- |
| Feedback | Exists, Coverage, Proven |
| Evaluation | Exists, Coverage, Proven |
| Governance | Exists, Coverage, Proven |

`Proven` is reported as unmeasured by default and is not included in the
baseline score. It should become meaningful only when durable task outcome or
effectiveness evidence supports the claim being made.

## 1. Instructions

Evaluate whether the repository has durable guidance that agents can find and
route through.

What counts:

- `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions, or equivalent.
- A concise project overview.
- Exact build, test, lint, typecheck, or validation commands.
- Architecture boundaries, directory rules, generated-file rules, or forbidden
  actions.
- Security or safety notes for credentials, destructive commands, production
  data, or privacy-sensitive files.
- Pointers from the short instruction entry point to deeper docs such as
  decisions, failures, conventions, domain notes, or validation docs.

What does not count:

- A chat message that was never committed to the repository.
- A vague instruction like "run the tests" without a command when no obvious
  standard command exists.
- A large instruction blob with no route to source-of-truth docs or checks.

## 2. Constraints

Evaluate whether important repository invariants are declared and, where
practical, enforceable.

What counts:

- Structure, docs drift, encoding hygiene, failure-memory, decision-memory, or
  effectiveness-plan checks.
- Lint, type, import, dependency, generated-file, forbidden-path, or
  architecture boundary rules.
- `.harness/*.json` rule files, package scripts, Makefile or Just recipes, CI
  jobs, or pre-commit hooks that encode project constraints.
- Explicit no-overwrite, no-delete, source-of-truth, generated-file, or local
  config protections.

What does not count:

- A documented boundary that no check can catch and no reviewer checklist names.
- A drift script that exists but is broken or unrelated to the repository.
- Generated-file guidance with no ignore rule, check, or review point.

Check scripts are a Constraint and Feedback join: the rule belongs to
Constraints; the execution path and reporting loop belong to Feedback.

## 3. Feedback

Evaluate whether validation mechanisms give fast, concrete signals after a
change.

What counts:

- Tests with a durable command in docs, package scripts, Makefile, CI, or
  equivalent.
- Linting and typechecking wired through the repository's normal toolchain.
- CI workflows such as GitHub Actions, GitLab CI, Buildkite, CircleCI, or
  equivalent.
- Pre-commit hooks, `make check`, `npm run validate`, or project-specific local
  validation scripts.
- Documentation that tells a new agent which checks belong to the normal gate
  and which checks are focused or manual.
- Check coverage for declared constraints and memory requirements.

What does not count:

- Tests that exist but have no discoverable command and are not run by CI.
- A linter dependency that is installed but not wired into a command.
- A check script that is never mentioned in local validation docs, package
  scripts, Makefile or Just recipes, CI, or agent guidance.
- CI that only deploys and does not validate code.

## 4. Memory

Evaluate whether the repository stores long-term project memory and makes it
operational.

What counts:

- Architecture Decision Records under `docs/decisions`.
- Failure records under `docs/failures` that describe rejected approaches,
  repeated agent mistakes, incidents, failed checks, or fixes that should not
  be forgotten.
- Conventions that explain local coding, naming, testing, or review rules.
- Domain notes that define product language, workflows, invariants, or user
  expectations.
- At least one non-template decision or failure record with concrete context.
- Failure records that name a regression test, fixture, smoke check, lint rule,
  drift check, CI gate, or manual review point for recurrence detection.
- Instructions, review guidance, or checks that route future agents back to the
  memory store.

What does not count:

- Empty directories.
- Placeholder templates only.
- Historical knowledge that lives only in issue comments, chat, or a person's
  memory.
- Failure records that stop at prose when recurrence can be detected.

## 5. Evaluation

Evaluate whether the repository can separate harness health from observed agent
outcomes.

What counts:

- `docs/evaluation.md`, effectiveness report templates, and task outcome
  templates or records.
- Effectiveness reports that label their mode, such as baseline-vs-harnessed or
  harnessed-only tracking.
- Task outcome records with repository ref, prompt reference, run id, reviewer,
  expected boundary, verification command, and first-pass verification result.
- Check scripts that validate effectiveness plans or task outcome consistency.
- Clear language that Harness Doctor, passing checks, and fixture tests are not
  proof of reduced agent mistakes.

What does not count:

- Treating a high Harness Doctor score as proof that agents improved.
- Counting setup-only or placeholder task outcome records as comparable product
  tasks.
- Effectiveness reports without enough run metadata to compare later.

## 6. Governance

Evaluate whether the repository has durable process controls for maintaining
the harness without blind rewrites.

What counts:

- `/harness doctor`, `/harness update`, `/harness refresh`, and `/harness
  review` guidance when the repository uses this kit.
- Diagnostic-only contracts for review or doctor commands.
- Source-of-truth rules that preserve the target repository's architecture,
  package manager, docs, commands, and conventions.
- Explicit approval gates for deleting, moving, archiving, overwriting, or
  re-cloning files.
- Dirty-worktree and commit/PR rules.
- Source tracking such as `.harness/source.json` when the kit is adopted into a
  target repository.
- Review timing or sub-agent fallback guidance where supported.

What does not count:

- A process rule that lives only in chat.
- An update or refresh command that blindly overwrites target files.
- A deletion, archive, or re-clone policy without explicit approval boundaries.

## Coupling Findings

Harness Doctor should report coupling findings separately from the element
score.

| Finding | Meaning |
| --- | --- |
| Orphan Constraint | A rule or check script exists without a feedback binding. |
| Orphan Feedback | A workflow or check signal exists without a clear local rule, script, or purpose. |
| Unoperationalized Memory | Decision or failure memory exists without instruction, check, review, or recurrence-detection linkage. |
| Unevaluated Memory | Memory exists without task outcome or effectiveness evidence. |
| Ungoverned Change Type | A risky change category lacks a documented approval, review, or maintenance path. |
| Promotion Gap | Repeated failure memory may need promotion into instructions, conventions, constraints, or checks. |

Coupling findings are review prompts. They should cite durable evidence and be
conservative when the relationship cannot be proven mechanically.

## Grade Scale

```text
90-100: A / Production-ready baseline evidence
80-89: B+ / Strong baseline evidence
70-79: B / Useful but incomplete baseline evidence
60-69: C / Basic baseline evidence
40-59: D / Mostly ad-hoc baseline evidence
0-39: F / Little durable baseline evidence
```

## Interpreting Results

A high score does not mean the project has perfect documentation, and it is not
an agent effectiveness score. It means the repository has enough durable
instructions, constraints, feedback, memory, evaluation scaffolding, and
governance paths that a new coding agent can work without depending on
session-scoped context.

Do not use the score as proof that agents make fewer mistakes. Measure that
with comparable task outcomes and effectiveness reports.

A low score is not a failure. It is a map of where to add the next durable
harness artifact or reconnect a broken harness loop.

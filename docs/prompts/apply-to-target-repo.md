# Prompt: Apply harness-starter-kit To A Target Repository

Use this prompt from the target repository root. The agent should clone
`harness-starter-kit` into `./harness-starter-kit`, read it, and then adapt the
workflow to the target repository.

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit, read it, then apply its prompt-first
harness engineering workflow to the current project.

If I ask for /harness doctor instead of adoption, use
./harness-starter-kit/commands/harness-doctor.md to inspect and score the
repository without modifying files.

If I ask for /harness update after adoption, use
./harness-starter-kit/commands/harness-update.md to refresh the kit reference,
selectively update target harness files, record .harness/source.json, and report
what changed without blindly overwriting target files.

If I ask for /harness refresh after adoption, use
./harness-starter-kit/commands/harness-refresh.md to review existing harness
docs, rules, knowledge records, and checks for stale or duplicated guidance.
Do not delete, archive, move, or rename files without my explicit approval for
the specific files.

If I ask for /harness review, use
./harness-starter-kit/commands/harness-review.md to review the current change
set from an opposing harness-engineering perspective. Report findings, missing
checks, overreach, durable memory gaps, and follow-up recommendations without
modifying files unless I explicitly ask you to apply fixes after the review.

Goal:
Make this repository easier and safer for coding agents to work in by adding
durable instructions, architecture constraints, feedback loops, knowledge
storage, and drift checks.

Adoption model:
This is prompt-first adoption. Do not treat the kit as an installer that knows
this repository. Clone it, read it as reference material, inspect the target
repository, and adapt the harness pattern to the target's existing architecture
and tools.

Rules:
- Treat the current working directory as the target repository.
- Treat ./harness-starter-kit as read-only reference material after cloning.
- Inspect this repository before editing.
- Identify the language, framework, package manager, test command, lint command,
  build command, CI provider, docs structure, and monorepo layout if present.
- Identify local servers, database seeds, docker-compose files, JARs, backend
  fixtures, emulator/device requirements, and PDF or localized instruction
  sources if present.
- Read existing AGENTS.md, CLAUDE.md, README, CONTRIBUTING, and CI configs if
  they exist.
- Preserve existing architecture, tools, naming, package managers, and test
  commands.
- Add the smallest useful harness rather than a large generic framework.
- When you find a harness gap, use
  ./harness-starter-kit/docs/theory/harness-engineering.md to decide whether
  the next durable artifact should be instructions, constraints, feedback,
  memory, evaluation, or governance. Do not add every artifact by default.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite existing files without explaining why.
- Do not delete existing files unless I explicitly ask.
- Do not edit files under ./harness-starter-kit during adoption unless I
  explicitly ask.
- Treat any stack profile files as reference snippets for you to adapt, not as
  automatic changes that must be copied into the project.
- Prioritize rules as follows: always preserve existing architecture and tools,
  document exact local checks, and protect generated/local files; when present,
  document servers, seeds, Docker, JARs, emulators, devices, or fixtures; when
  touching auth, external APIs, permissions, hardware, persistence, state, or
  network boundaries, consider whether a decision record is needed; for broad
  feature work, write a small scenario test note.
- During prompt-first adoption, read profile templates from
  ./harness-starter-kit/templates/profiles/<profile>/. If installer-generated
  snippets already exist in this target repository, review them under
  docs/harness/profiles/<profile>/.
- Before finishing, tell me whether ./harness-starter-kit should be removed,
  ignored, or kept intentionally as a submodule/reference before I commit.

Expected work:
- Add or update AGENTS.md with project-specific agent instructions.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if no
  equivalent structure exists.
- Add lightweight drift checks under scripts/ when they reflect actual target
  repo rules. Generic doc-link and temporary-file checks are baseline hygiene;
  target-specific checks should enforce real project constraints.
- Add CI or pre-commit integration only when it fits the existing project and
  explain the tradeoff first.
- Add stack-specific lint/type/test recommendations based on the detected
  language.
- If the repo includes a local server, database seed, docker-compose, JAR, mock
  API, or backend fixture, document how to run and verify it or explain why it
  was not run.
- Before broad feature implementation, write a small scenario test note or explicitly
  say why build-only validation is enough.
- If localized source, XML resources, PDF-derived instructions, or mojibake risk
  exists, run or document an encoding audit before broad edits.
- Fill the Effectiveness Measurement Plan in the adoption report. If baseline
  data does not exist, define the next comparable tasks, primary metric, review
  window, and results location instead of leaving TODOs.
- For individual task outcome records, copy
  ./harness-starter-kit/docs/templates/task-outcome.yaml and store filled
  records under docs/effectiveness/task-outcomes/.
- If adoption fixes a user-visible runtime failure or high-risk bug path that
  should not recur, including a 5xx error, crash, security or permission bug,
  data-loss risk, failed CI run, failed harness check, repeated agent mistake,
  previously identified bug path, or cross-environment mismatch, add a
  `docs/failures/*.md` record unless the issue was purely transient or already
  covered by an existing failure note.
- If you save the adoption report as a file, run
  `scripts/check_effectiveness_plan.py --require-report` when that script is
  present.

Drift check examples:
- If AGENTS.md says routes must not access the database directly, add a check
  that fails on forbidden database imports in route files.
- If a decision record says Zustand is the chosen state library, add a check
  that fails when Redux dependencies are added.
- If generated files must live under one directory, add a structure check that
  rejects generated files elsewhere.
- If Korean, Japanese, Chinese, or other localized text has encoding risk, adapt
  `scripts/check_encoding_hygiene.py` or add a manual audit note that checks for
  invalid UTF-8 and common mojibake markers.

Finish by reporting:
- files added or changed
- checks I can run locally
- effectiveness measurement plan
- server or fixture verification plan
- scenario test note for broad feature work, or the reason build-only validation
  is enough
- failure memory recorded or skipped with reason
- assumptions you made
- remaining manual steps
- what to do with ./harness-starter-kit before committing

Use ./harness-starter-kit/docs/templates/adoption-report.md as the report shape
if present. Use ./harness-starter-kit/docs/evaluation.md for the measurement
protocol, ./harness-starter-kit/docs/templates/task-outcome.yaml for individual
task records, and ./harness-starter-kit/docs/templates/effectiveness-report.md
when recording aggregate before/after results.
```

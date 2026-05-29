# AGENTS.md

## Purpose

This repository is a reusable harness engineering starter kit. Its job is to
teach agents how to add durable project rules, constraints, feedback loops,
knowledge storage, and drift checks to another repository.

When applying this kit to a target repository, treat the target repository as
the source of truth. Preserve its existing architecture and tools.

## Prompt-First Adoption Context

The primary usage pattern is:

1. The user opens the target repository with an agent.
2. The user gives the agent the kit Git URL:
   `https://github.com/baskduf/harness-starter-kit`.
3. The agent clones the kit into `./harness-starter-kit`, reads it, and applies
   the prompt-first harness workflow to the target repository.

After cloning, the expected layout is:

```text
target-repo/
|-- harness-starter-kit/
`-- existing-project-files
```

When an agent is applying the kit from this nested layout:

- Treat the current working directory as the target repository root.
- Treat `./harness-starter-kit` as read-only reference material unless the user
  explicitly asks to edit the kit itself.
- Read this kit's docs, prompts, templates, and scripts to understand the
  harness pattern, then modify only the target repository files needed for
  adoption.
- Prefer adapting the target repository's existing docs, scripts, package
  manager, CI, and conventions over copying starter-kit defaults verbatim.
- Before the target repository commits adoption changes, report whether the
  nested `harness-starter-kit/` clone should be removed, ignored, or kept
  intentionally as a submodule/reference.

## Commands

When the user asks for `/harness doctor`, run the diagnostic workflow in
`commands/harness-doctor.md`. It must inspect and report only; it must not
modify files or remove a target-local `./harness-starter-kit` directory.

When the user asks for `/harness update`, run the update workflow in
`commands/harness-update.md`. It may update target repository harness files, but
it must refresh the kit reference first, avoid blind overwrites, and finish with
a Harness Update Report.

When the user asks for `/harness refresh`, run the maintenance workflow in
`commands/harness-refresh.md`. It reviews existing target harness docs, rules,
knowledge records, and checks for stale or duplicated guidance. It must not
delete, archive, move, or rename files without explicit approval for the
specific files.

Run these checks after changing installer behavior, templates, or drift scripts:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/harness_doctor.py --target .
```

When changing profile README files, also keep
`docs/templates/profile-readme.md`, `docs/checklists/profile-maintenance.md`,
and `tests/test_profile_consistency.py` aligned.

## Project Analysis Rule

When asked to analyze, review, summarize, onboard to, or explain this project,
inspect these first when they exist:

- `README.md`
- `AGENTS.md`
- `.harness/source.json`
- `docs/decisions/`
- `docs/conventions/`
- `docs/domain/`
- `docs/failures/`
- `scripts/check_harness.py`
- `scripts/check_*.py`

Then summarize the project in terms of structure, current behavior, tests,
documentation, known decisions, known failures, drift checks, and recommended
next work.

## How To Apply This Kit To A Target Repository

1. Inspect the target repository before editing.
   - Identify language, framework, package manager, test command, linter, CI,
     directory layout, and existing agent instruction files.
   - Read existing `README`, `AGENTS.md`, `CLAUDE.md`, contribution docs, and CI
     configs if present.

2. Install only the missing harness pieces.
   - Add `AGENTS.md` if there is no durable agent instruction file.
   - Add `docs/decisions`, `docs/failures`, `docs/conventions`, and
     `docs/domain` if the target has no equivalent knowledge store.
   - Add drift checks under `scripts/` when no equivalent checks exist.
   - Add CI or pre-commit wiring only when it fits the existing tooling.
   - Use `--with-ci` only when the target should receive the optional GitHub
     Actions workflow.

3. Prefer local conventions over starter-kit defaults.
   - Use the target repo's naming, formatting, package manager, and test runner.
   - Do not introduce a new framework to enforce a rule that existing tooling
     can already enforce.

4. Make rules enforceable where practical.
   - If `AGENTS.md` says "no direct database access from routes", add a lint,
     import, test, or review check that can catch violations.
   - If an automated check is not practical, document the manual review point.

5. Avoid overwriting existing files.
   - If a file exists, patch it carefully or create a clearly named snippet for
     the maintainer to merge.
   - Never delete target project files unless the user explicitly asks.

6. Finish with an adoption report.
   - List files added or changed.
   - List checks the agent can run.
   - Fill the effectiveness measurement plan.
   - List remaining manual steps.
   - Name any assumptions made about the target stack.

## Harness Components

### Instruction Document

Use `AGENTS.md` for agent-facing rules. Keep it concise, structured, and
specific. Include project overview, directory rules, commands, forbidden
changes, testing expectations, and PR behavior.

### Architecture Constraints

Use tools that block invalid code before it is merged: linters, formatters,
type checks, dependency boundaries, import rules, schema validation, and
pre-commit hooks.

### Feedback Loops

Provide guides and sensors.

- Guides: examples, tests, fixtures, API contracts, golden files
- Sensors: lint failures, type failures, test failures, CI failures, runtime
  checks, observability checks

### Knowledge Store

Store durable context in `docs/`:

- `docs/decisions/` for Architecture Decision Records
- `docs/failures/` for approaches already tried and rejected
- `docs/conventions/` for project-specific coding rules
- `docs/domain/` for business language, workflows, and invariants

If you fix a failed CI run, failed harness check, repeated agent mistake, or
cross-environment mismatch, add a `docs/failures/*.md` record unless the failure
is purely transient. If you skip it, explain why in the final report.

### Garbage Collection

Add checks for drift:

- code drift: unused code, dead imports, duplicate helpers
- document drift: docs reference missing files or broken Markdown links
- structure drift: temporary files or paths outside the agreed architecture

## Starter Kit Editing Rules

- Keep templates generic and conservative.
- Do not bake in a single product architecture.
- Add profile-specific guidance under `templates/profiles/<profile>/`.
- Scripts should be safe by default and avoid overwriting user files.
- Favor clear Markdown and small Python scripts over heavyweight generators.
- Keep `examples/*-adoption-report.md` aligned with real adoption tests.

## Commit And PR Rules

- Keep each commit focused on one logical harness change.
- Do not mix unrelated formatting, generated output, or broad documentation
  rewrites into a feature or fix commit.
- Before committing, inspect `git status` and the staged diff.
- Do not commit local reference clones, virtual environments, dependency
  directories, build outputs, caches, secrets, credentials, or machine-specific
  config.
- Run the relevant documented checks before committing. If a check cannot be
  run, record why in the final report or PR notes.
- Follow the target repository's existing commit convention first.
- If the target repository uses Conventional Commits, follow its prefixes, such
  as `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.
- If no convention exists, use a clear imperative commit subject that names the
  harness area changed, such as `Add commit hygiene rules`.
- PR descriptions should summarize changed files, checks run, assumptions,
  remaining risks, and any manual follow-up.

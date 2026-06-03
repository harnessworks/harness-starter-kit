# Adoption Workflow

Use this workflow when an agent is applying `harness-starter-kit` from a target
repository root. The primary flow is: the user gives the agent the Git URL, the
agent clones the kit into `./harness-starter-kit`, reads it, and adapts the
workflow to the target repository.

The target repository is the current working directory. The
`./harness-starter-kit` directory is reference material during adoption; do not
edit it unless the user asks to change the kit itself.

If the user asks for `/harness doctor`, run the diagnostic command in
`commands/harness-doctor.md` instead of the adoption workflow. Harness Doctor
scores readiness and recommends next actions; it does not modify files. During
that diagnostic flow, do not remove a target-local `./harness-starter-kit`
directory. Only temporary clones created outside the target repository may be
cleaned up without asking.

If the user asks for `/harness refresh`, run the maintenance command in
`commands/harness-refresh.md` instead of the adoption workflow. Harness Refresh
reviews the target repository's existing harness for stale docs, duplicated
guidance, obsolete records, and unused checks. It must not delete, archive,
move, or rename files without explicit approval for the specific files.

## 1. Read The Target Repository

Collect the current shape before changing anything:

- language and framework
- package manager
- test commands
- lint, format, type-check, and build commands
- CI provider
- directory layout
- monorepo layout, if present
- local server, database seed, docker-compose, JAR, backend fixture, emulator,
  device, or other runtime dependency needed by the app
- existing docs and agent instruction files
- existing architecture, domain, decision, and contribution docs

Read `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, package
manifests, and CI configs when they exist. If the target already has an
equivalent docs or knowledge structure, use that structure instead of creating a
parallel one.

## Rule Priority

Use this priority order when applying the workflow. Not every item applies to
every task.

When a harness gap appears, use the decision table in
`docs/theory/harness-engineering.md` to decide whether the next durable artifact
should be instructions, constraints, feedback, memory, evaluation, or
governance. Do not add every artifact by default.

- Always: preserve the target repository's existing architecture and tools,
  document exact local checks, and protect generated files and local config.
- When present: document how to run or verify local servers, database seeds,
  Docker services, JARs, emulators, devices, or backend fixtures.
- When present: use `docs/checklists/external-api-work.md` for external API,
  auth provider, webhook, public-data API, live/mock fallback, or secret
  redaction work.
- When touching that area: consider a decision record for auth, external APIs,
  permissions, hardware, persistence, state management, or networking boundary
  changes. Use `docs/checklists/decision-failure-memory.md` to distinguish
  ADRs, failure notes, domain docs, convention updates, and final-report notes.
- Before finishing implementation work: ask whether the diff changed user
  workflow, input contract, input semantics, state normalization, API request or
  response shape, fallback policy, or displayed decision criteria. If yes,
  either add or update a decision record, cite the existing ADR, or explain why
  no decision memory is needed.
- Broad feature work: write a small scenario test note. For narrow fixes, name
  the relevant check or explain why build-only validation is enough.

## 2. Identify Existing Harness Pieces

Many projects already have part of a harness:

- `README.md` or contribution docs
- tests
- CI
- lint configuration
- architecture docs
- decision records

Reuse these instead of duplicating them.

## 3. Add Or Update `AGENTS.md`

The first useful harness artifact is usually a short `AGENTS.md`.

It should answer:

- What is this project?
- Which commands should agents run?
- Which directories have special rules?
- What should agents avoid?
- What must be true before a change is complete?

## 4. Add A Knowledge Store

Create these directories if the target has no equivalent:

```text
docs/
|-- decisions/
|-- failures/
|-- conventions/
`-- domain/
```

Start small. Empty directories are less useful than one real decision or failure
record.

## 5. Add Constraints

Match constraints to the stack:

- Python: Ruff, mypy, import-linter, vulture, pre-commit
- Django: `manage.py check`, `manage.py test`, virtual environment and
  development database ignores, and migration review rules
- Flask: app factory checks, `python -m unittest discover -s tests`, Flask
  route table checks, and instance-data ignores
- Spring: Maven or Gradle wrapper checks, Spring Boot context tests, generated
  build output ignores, local config ignores, and migration review rules when
  Flyway or Liquibase is present
- Android/Kotlin: Gradle wrapper checks such as `./gradlew test` and
  `./gradlew assembleDebug`, `local.properties` and `ANDROID_HOME` handling,
  generated Android build output ignores, emulator/device/manual test notes,
  Retrofit endpoint boundary checks, and runtime permission, NFC, and Bluetooth
  verification caveats
- TypeScript: ESLint, TypeScript strictness, dependency boundary rules,
  unused-export checks
- Next.js: `next build`, `tsc --noEmit --incremental false`, generated-file
  ignores, and a review of any `tsconfig.json` or `next-env.d.ts` changes made
  by Next itself
- Any stack: CI checks, formatting checks, forbidden-file scans

Profile files are agent reference material, not automatic transformations. When
using a cloned kit during prompt-first adoption, read snippets from
`./harness-starter-kit/templates/profiles/<profile>/`. When using
`scripts/apply_harness.py`, copied profile snippets land in the target
repository under `docs/harness/profiles/<profile>/`. In both cases, adopt only
the snippets that fit the target repository's existing tools and conventions.

Prefer existing tools when possible.

If a repository starts with the generic harness and later gains a real stack,
run `docs/checklists/profile-absorption.md`. Use it to decide which profile
snippets should become real commands, config, ignores, documentation, or checks.

## 6. Add Feedback Loops

Make the common path fast:

- local check command
- local server or fixture verification plan when the app depends on a server
  JAR, SQL seed file, docker-compose service, mock API, emulator, or device
- pre-commit checks when the project already uses them
- CI workflow only when it matches the target repository's CI provider
- clear test names and error messages
- target-specific verification scripts when runtime behavior, external API
  handling, route tables, or environment contracts cannot be proven by lint,
  typecheck, tests, or build alone. See
  `docs/checklists/verification-scripts.md`.

Record the target repository's normal completion gate by its real command or
workflow name, such as `make test`, `just check`, a package script, CI workflow,
`scripts/check_harness.py`, or another documented local command. When adoption
adds deterministic, local, non-network, reasonably fast checks for product
behavior that agents are expected to verify repeatedly, include them in that
normal gate or document why they remain focused or manual.

Before broad feature implementation, write a small scenario test note or
explicitly say why build-only validation is enough. The note can be a compact
matrix of user flows, setup data, server state, automated checks, and manual
checks. For mobile or local-server projects, include endpoint readiness, seed
data, emulator/device coverage, runtime permissions, and hardware-dependent
flows such as NFC, Bluetooth, or beacons when relevant.

For external API work, also name the live/mock mode, redaction behavior,
zero-result behavior, provider error handling, and the smoke command or fixture
used to verify the path. Keep live API checks separate from the default harness
gate when credentials, quota, network access, or provider uptime make them
unsafe as a normal command.

Agents improve fastest when feedback is quick and concrete.

## 7. Add Garbage Collection

Install lightweight baseline drift checks:

- missing files referenced by docs
- broken local Markdown links
- forbidden temporary filenames
- failure records without a concrete detection or prevention check, fixture,
  CI gate, or no-check-practical reason
- watched implementation diffs without a decision-record change, reported as a
  warning that asks the final report to add an ADR, cite an existing ADR, or
  explain why no decision memory is needed
- invalid UTF-8 or common mojibake markers when the target has localized
  comments, XML resources, PDF-derived instructions, or prior encoding drift
- unused code checks for the chosen stack

Then add target-specific drift checks only when they enforce real repository
rules. Generic checks keep the harness tidy; project-specific checks keep the
architecture honest.

When using `scripts/check_decision_memory.py`, tune
`.harness/decision-memory-rules.json` to the target repository's real
implementation paths. Remove ignored patterns such as `scripts/**` when those
paths contain product behavior, workflow code, API smoke behavior, or other
decision-bearing implementation.

In CI, run `scripts/check_decision_memory.py --base <base-ref>` for pull
request comparisons. Non-PR scheduled or manual runs without a changed working
tree are smoke checks for script health, not proof that no decision memory is
needed for a future diff.

Examples:

- If routes/controllers must not access persistence directly, scan route files
  for forbidden database imports.
- If an ADR chooses Zustand instead of Redux, fail when Redux packages are added
  to the manifest.
- If generated files must live under one generated-source directory, reject
  generated files in other directories.

Run them manually at first, then wire them into CI once they are stable. The
installer only adds the GitHub Actions workflow when `--with-ci` is provided.

## 8. Report Adoption

Finish with a short adoption report. Use
`docs/templates/adoption-report.md` as a shape and compare against
`examples/node-adoption-report.md`, `examples/nextjs-adoption-report.md`,
`examples/django-adoption-report.md`, `examples/flask-adoption-report.md`, or
`examples/spring-adoption-report.md` when the target stack is similar.

The report should make clear what the agent observed, which existing structures
were reused, which snippets were adopted or skipped, which checks were run, and
which checks belong to the normal completion gate versus focused or manual
verification. For focused or manual checks, record why they are not part of the
normal gate. Also report whether the nested `harness-starter-kit/` clone should
be removed, ignored, or kept intentionally before committing.

If implementation changed behavior, added a new integration boundary, or chose
a defensive fallback for permissions, hardware, networking, persistence, or
state management, decide whether the change belongs in `docs/domain/` as domain
language or in `docs/decisions/` as an architectural decision. Use
`docs/checklists/decision-failure-memory.md` for boundary examples, then record
the choice or explain why no decision record was needed.

If adoption fixes a user-visible runtime failure or high-risk bug path that
should not recur, including a 5xx error, crash, security or permission bug,
data-loss risk, failed CI run, failed harness check, repeated agent mistake,
previously identified bug path, or cross-environment mismatch, record it under
`docs/failures/*.md` unless the issue was purely transient or already covered by
an existing failure note. The failure record should name the regression test,
fixture, smoke check, lint rule, drift check, CI gate, or manual review point
that prevents or detects recurrence. If no check is practical, explain why in
the record and adoption report.

The report should also include an effectiveness measurement plan. Use
`docs/evaluation.md` to choose the evaluation mode and metrics. If no baseline
data exists, record harnessed-only tracking as the initial mode and name the
next comparable tasks, primary metric, review window, and results location.
Actual results should be recorded later with
`docs/templates/effectiveness-report.md`. Individual task outcomes can be
recorded with `docs/templates/task-outcome.yaml` and stored under the target
repository's docs/effectiveness/task-outcomes directory.

When the adoption report is saved as a file, run
`scripts/check_effectiveness_plan.py --require-report` to catch missing sections
or placeholder measurement fields before finishing.

## 9. Update An Existing Harness

After adoption, use `/harness update` when the maintainer wants to refresh the
local kit reference and consider newly added harness guidance.

Follow `commands/harness-update.md`. Refresh or clone `./harness-starter-kit`,
compare the current kit source with `.harness/source.json`, and classify update
opportunities as safe candidates, careful patches, reference-only guidance, or
manual-review items.

The target repository remains the source of truth. Do not overwrite existing
target files with starter-kit templates. Patch only the pieces that fit the
target repository's current architecture, tools, docs, and verification path.
Finish with a Harness Update Report and update `.harness/source.json` when the
kit source was successfully confirmed.

## 10. Refresh An Existing Harness

After adoption, use `/harness refresh` when the maintainer wants to reduce stale
or duplicated target harness guidance without pulling new kit changes.

Follow `commands/harness-refresh.md`. Review existing agent instructions,
knowledge records, drift checks, CI wiring, and source tracking. Classify
findings as keep, update, merge, archive/delete candidate, or manual review.

Do not delete, archive, move, or rename files during refresh unless the user
explicitly approves the specific files after seeing the candidates. Prefer
marking decision and failure records as superseded or obsolete over deleting
historical context.

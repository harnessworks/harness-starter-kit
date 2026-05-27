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

## 1. Read The Target Repository

Collect the current shape before changing anything:

- language and framework
- package manager
- test commands
- lint, format, type-check, and build commands
- CI provider
- directory layout
- monorepo layout, if present
- existing docs and agent instruction files
- existing architecture, domain, decision, and contribution docs

Read `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, package
manifests, and CI configs when they exist. If the target already has an
equivalent docs or knowledge structure, use that structure instead of creating a
parallel one.

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
- pre-commit checks when the project already uses them
- CI workflow only when it matches the target repository's CI provider
- clear test names and error messages

Agents improve fastest when feedback is quick and concrete.

## 7. Add Garbage Collection

Install lightweight baseline drift checks:

- missing files referenced by docs
- broken local Markdown links
- forbidden temporary filenames
- unused code checks for the chosen stack

Then add target-specific drift checks only when they enforce real repository
rules. Generic checks keep the harness tidy; project-specific checks keep the
architecture honest.

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
whether the nested `harness-starter-kit/` clone should be removed, ignored, or
kept intentionally before committing.

If adoption fixes a failed CI run, failed harness check, repeated agent mistake,
or cross-environment mismatch, record it under `docs/failures/*.md` unless the
failure is purely transient. If no failure note is added, explain why in the
adoption report.

The report should also include an effectiveness measurement plan. Use
`docs/evaluation.md` to choose the evaluation mode and metrics. If no baseline
data exists, record harnessed-only tracking as the initial mode and name the
next comparable tasks, primary metric, review window, and results location.
Actual results should be recorded later with
`docs/templates/effectiveness-report.md`.

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

# AGENTS.md

## Project Overview

- Name: {{PROJECT_NAME}}
- Harness profile: {{PROFILE}}
- Purpose: TODO: describe the product, library, service, or tool.
- Primary language/framework: TODO

## Commands

Document the commands agents should run before finishing work.

```powershell
# TODO: replace with target project commands
# example: pytest
# example: npm test
# example: npm run lint
```

## Directory Rules

Document the important source boundaries.

- TODO: describe where application code lives.
- TODO: describe where tests live.
- TODO: describe generated files, build outputs, or vendored code agents should
  avoid editing.

## Coding Rules

- Follow the existing style in nearby files.
- Keep changes scoped to the requested behavior.
- Prefer existing project helpers and patterns over new abstractions.
- Add or update tests for behavior changes.
- Remove temporary debugging code before finishing.

## Architecture Constraints

TODO: list constraints that should be enforced by lint, type checks, tests, or
CI.

Examples:

- Routes/controllers must not contain business logic.
- UI components must not call persistence APIs directly.
- Domain models must not import presentation-layer code.

## Knowledge Store

Before making architectural or domain-level changes, inspect:

- `docs/decisions/`
- `docs/failures/`
- `docs/conventions/`
- `docs/domain/`

When a decision or rejected approach becomes relevant, add a short record to the
appropriate directory.

If you fix a failed CI run, failed harness check, repeated agent mistake, or
cross-environment mismatch, add a `docs/failures/*.md` record unless the failure
is purely transient. If you skip it, explain why in the final report.

When a new stack, framework, build tool, UI layer, API layer, or test runner is
introduced after generic adoption, review the closest profile. If the kit is
still present as a reference clone, read
`harness-starter-kit/templates/profiles/<profile>/`; if the installer copied
snippets into this repository, read `docs/harness/profiles/<profile>/`. Decide
which profile snippets to adopt, adapt, skip, or defer, then report those
choices before finishing.

When harness rules, checks, CI, architecture boundaries, or agent-facing docs
change, update the effectiveness measurement plan in the adoption report or the
current effectiveness report. If the task is not comparable to prior agent work,
say so explicitly.

## Documentation Rules

When a change affects project structure, UI architecture, state management,
commands, conventions, or recurring workflow, update at least one durable
documentation artifact before finishing.

Prefer:

- The project README for user-facing setup and usage changes.
- `AGENTS.md` for agent workflow, commands, and repository rules.
- `docs/conventions/coding.md` for implementation conventions and recurring
  code patterns.
- `docs/decisions/*.md` for architectural choices, new tools, major structure
  changes, or tradeoffs.
- `docs/failures/*.md` only when an attempted approach failed and should not be
  repeated.

If a feature change adds or changes a local server, database seed, external API,
runtime permission, hardware-dependent behavior, or other integration boundary,
decide whether the durable record belongs in `docs/domain/` or
`docs/decisions/` before finishing.

If no `docs/` file is updated for a non-trivial code change, explicitly explain
why in the final report.

## Commit And PR Rules

- Follow any existing branch, commit message, and PR conventions in this
  repository.
- Keep each commit focused on one logical change.
- Before committing, inspect `git status` and the staged diff.
- Do not commit generated files, dependency directories, local environment
  files, secrets, credentials, or the local `harness-starter-kit/` reference
  clone unless the repository intentionally tracks it.
- Run the relevant documented checks before committing. If a check cannot be
  run, explain why in the final report or PR notes.
- Follow this repository's existing commit convention first.
- If this repository uses Conventional Commits, use prefixes such as `feat:`,
  `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.
- If no convention exists, use a clear commit subject that describes the change
  in imperative form.
- PRs or adoption reports should summarize changed files, checks run,
  assumptions, remaining risks, and manual follow-up.

## Forbidden Actions

- Do not rewrite large parts of the project without an explicit request.
- Do not delete existing files unless the task requires it and the reason is
  clear.
- Do not add new package managers, frameworks, or services when existing tools
  can solve the problem.
- Do not edit or commit a local `harness-starter-kit/` reference clone unless
  the user explicitly asks.
- Do not leave `temp_`, `_new`, `_old`, `_backup`, or `_fix` files behind.

## Completion Criteria

Before reporting completion:

- Run the documented checks that are relevant to the change.
- For local-server, emulator, device, or hardware-dependent work, document the
  scenario test plan or explain why build-only validation is enough.
- Confirm no temporary files were left behind.
- Update docs when behavior, architecture, commands, or known failures changed.
- Update the harness effectiveness measurement plan when the change affects
  agent rules, checks, CI, docs, or architecture boundaries.
- Summarize changed files, verification performed, and remaining risks.

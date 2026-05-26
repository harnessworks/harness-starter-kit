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

If no `docs/` file is updated for a non-trivial code change, explicitly explain
why in the final report.

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
- Confirm no temporary files were left behind.
- Update docs when behavior, architecture, commands, or known failures changed.
- Summarize changed files, verification performed, and remaining risks.

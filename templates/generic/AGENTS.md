# AGENTS.md

## Project Overview

- Name: {{PROJECT_NAME}}
- Harness profile: {{PROFILE}}
- Purpose: TODO: describe the product, library, service, or tool.
- Primary language/framework: TODO

## Core Rules

- Preserve this repository's existing architecture, tools, package manager,
  naming, and conventions.
- Keep changes scoped to the requested behavior.
- Prefer nearby patterns and existing helpers over new abstractions.
- Do not overwrite, delete, or move existing files unless the task requires it
  and the reason is clear.
- Do not add new package managers, frameworks, or services when existing tools
  can solve the problem.
- Do not edit or commit a local `harness-starter-kit/` reference clone unless
  the repository intentionally tracks it.
- Do not leave `temp_`, `_new`, `_old`, `_backup`, or `_fix` files behind.

## Commands

Document the exact commands agents should run before finishing work. Name this
repository's normal completion gate, whether it is `make test`, `just check`, a
package script, CI workflow, `scripts/check_harness.py`, or another local
command.

```powershell
# TODO: replace with target project commands
# example: pytest
# example: npm test
# example: npm run lint
```

Use `python3` instead of `python` when that is the available interpreter.

## Project Analysis Rule

When asked to analyze, review, summarize, onboard to, or explain this project,
inspect these first when they exist:

- README or equivalent project overview
- `AGENTS.md`
- `.harness/source.json`
- `docs/decisions/`
- `docs/conventions/`
- `docs/domain/`
- `docs/failures/`
- `scripts/check_harness.py`
- `scripts/check_*.py`

Then summarize structure, current behavior, tests, documentation, known
decisions, known failures, drift checks, and recommended next work.

## Directory And Architecture Rules

- TODO: describe where application code lives.
- TODO: describe where tests live.
- TODO: describe generated files, build outputs, local config, or vendored code
  agents should avoid editing.
- TODO: list architecture constraints that should be enforced by lint, type
  checks, tests, import rules, CI, or review.

## Knowledge Store

Before architectural, domain, workflow, or integration changes, inspect:

- `docs/decisions/`
- `docs/failures/`
- `docs/conventions/`
- `docs/domain/`

Add or update durable docs when behavior, architecture, commands, conventions,
or known failures change. If no `docs/` file is updated for a non-trivial code
change, explain why in the final report.

Before finishing, ask whether the change alters user workflow, input contract,
input semantics, state normalization, API request or response shape, fallback
policy, or displayed decision criteria. If it does, or if the change otherwise
affects non-trivial product or workflow structure, integration or mock
external-behavior boundaries, major data models, state classifications, or UX
principles that become code structure, handle decision memory explicitly: add
or update `docs/decisions/*.md`, cite the existing ADR that covers the choice,
or explain why the change is too narrow to need decision memory. A
`docs/domain/` update does not replace a decision record.

If you fix a user-visible runtime failure or high-risk bug path that should not
recur, including a 5xx error, crash, security or permission bug, data-loss risk,
failed CI run, failed harness check, repeated agent mistake, previously
identified bug path, or cross-environment mismatch, add a `docs/failures/*.md`
record unless the issue was purely transient or already covered by an existing
failure note. The failure note must name the regression test, fixture, smoke
check, lint rule, drift check, CI gate, or manual review point that prevents or
detects recurrence. If no check is practical, explain why in the note and final
report.

When harness rules, checks, CI, architecture boundaries, or agent-facing docs
change, update the effectiveness measurement plan in the adoption report or the
current effectiveness report. If the task is not comparable to prior agent
work, say so explicitly.

## Profile Guidance

When a new stack, framework, build tool, UI layer, API layer, or test runner is
introduced after generic adoption, review the closest profile. If the kit is
still present as a reference clone, read
`harness-starter-kit/templates/profiles/<profile>/`; if the installer copied
snippets into this repository, read `docs/harness/profiles/<profile>/`.

Adopt, adapt, skip, or defer profile snippets based on this repository's actual
tools and maintenance expectations, then report those choices.

## Commit And PR Rules

- Follow this repository's existing branch, commit message, and PR conventions.
- Keep each commit focused on one logical change.
- Before committing, inspect `git status` and the staged diff.
- Do not commit generated files, dependency directories, local environment
  files, secrets, credentials, or local reference clones.
- Run the relevant documented checks before committing. If a check cannot be
  run, explain why in the final report or PR notes.
- Before pushing substantial harness, external API, integration-boundary, or
  agent-facing workflow changes, run `/harness review` when available, or
  record why review happened after push or was skipped.
- If this repository uses Conventional Commits, use prefixes such as `feat:`,
  `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`. If no convention exists,
  use a clear imperative commit subject.
- PRs or adoption reports should summarize changed files, checks run,
  assumptions, remaining risks, and manual follow-up.

## Completion Criteria

Before reporting completion:

- Run the documented checks relevant to the change.
- Add or update tests for behavior changes.
- When adding deterministic, local, non-network, reasonably fast checks for
  product behavior that agents are expected to verify repeatedly, include them
  in the documented normal completion gate or explain why they remain focused
  or manual.
- Keep live API, credential, quota, provider-uptime, visual, device, slow, or
  otherwise fragile checks outside the normal gate unless they are stable and
  expected in this repository's normal environment.
- For broad local-server, emulator, device, or hardware-dependent work,
  document the scenario test note or explain why build-only validation is
  enough.
- Confirm no temporary files were left behind.
- If `scripts/check_failure_memory.py` exists, run it after adding or updating
  `docs/failures/*.md`.
- If `scripts/check_decision_memory.py` exists, run it for implementation diffs
  before the final report. Treat warnings as a prompt to add or update an ADR,
  cite an existing ADR, or explain why no decision memory is needed.
- Update docs when behavior, architecture, commands, or known failures changed.
- Failure docs: for each new or updated `docs/failures/*.md`, named the
  regression test, fixture, smoke check, lint rule, drift check, CI gate, or
  manual review point that prevents or detects recurrence, or explained why
  none is practical.
- Decision docs: added or updated `docs/decisions/*.md`, cited an existing ADR,
  or explained why no decision record was needed for structural behavior,
  workflow, input contract or semantics, API/mock boundary, data model, state,
  fallback policy, displayed decision criteria, or UX changes.
- Summarize changed files, verification performed, and remaining risks.

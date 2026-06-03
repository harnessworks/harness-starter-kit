# Example Adoption Report: Node JavaScript Target

## Target Repository Observed

- Target: `sample-task-tracker`, a tiny JavaScript ES module project.
- Package manager: npm.
- Existing checks: Node's built-in test runner through `node --test`.
- Existing docs: README only; no durable agent instruction file.
- CI: none detected.
- Layout: single-package repository with source under `src/` and tests under
  `test/`.

## Files Added Or Changed

- Added `AGENTS.md` with project commands, source boundaries, forbidden actions,
  and completion criteria.
- Added `.harness/structure-rules.json`.
- Added `scripts/check_docs_drift.py` and `scripts/check_structure.py`.
- Added `docs/conventions/coding.md`, `docs/domain/glossary.md`,
  `docs/decisions/001-adopt-agent-harness.md`, and failure/decision templates.
- Added TypeScript profile snippets under `docs/harness/profiles/typescript/`.
- Added `check:harness` to `package.json`.
- Added `.gitignore` entries for generated files and the local
  `harness-starter-kit/` clone.

## Existing Structures Reused

- Reused the existing npm package scripts instead of introducing a new task
  runner.
- Reused Node's built-in test runner instead of adding a test framework.
- Kept the single-package layout; no package-level `AGENTS.md` files were added.

## Checks Run

```powershell
npm.cmd run check:harness
```

The command ran syntax checks, `node --test`, baseline document drift checks,
and baseline structure drift checks successfully.

## Verification Gate Placement

- Normal completion gate: `npm.cmd run check:harness`.
- Deterministic behavior checks included in the normal gate: Node's built-in
  `node --test` suite ran through `check:harness`.
- Focused or manual checks outside the normal gate: installer smoke validation
  and intentional failure probes for `temp_debug.js`, `console.log(`, and broken
  Markdown links.
- Reasons for focused/manual placement: installer re-run behavior and
  intentional-failure probes validate adoption tooling, not normal target
  repository completion work.

## Drift Checks Added

- Baseline doc hygiene: broken local Markdown links and stale file references.
- Baseline structure hygiene: temporary and backup filenames.
- Target-specific architecture checks were not added because the sample project
  had no real route/service, persistence, UI/server, or state-management
  boundary to enforce.

## Installer Smoke Validation

The installer was also smoke-tested as a skeleton bootstrap helper, not as the
main adoption path:

```powershell
python harness-starter-kit\scripts\apply_harness.py --target . --profile typescript --dry-run
python harness-starter-kit\scripts\apply_harness.py --target . --profile typescript
python harness-starter-kit\scripts\apply_harness.py --target . --profile typescript
python scripts\check_docs_drift.py
python scripts\check_structure.py
python scripts\check_harness.py
```

The target had an existing `AGENTS.md`, which the installer preserved with
`skip-existing`. Re-running the installer skipped all generated harness files.
The copied TypeScript profile `check_harness.py` successfully ran the target's
`lint`, `typecheck`, `test`, and `build` package scripts before the generic
drift checks.

Intentional failures were also verified:

- `src/temp_debug.js` was rejected by `scripts/check_structure.py`.
- `console.log(` in source code was rejected by the target lint script through
  `scripts/check_harness.py`.
- A broken local Markdown link was rejected by `scripts/check_docs_drift.py`.

On Windows PowerShell, `npm.cmd` worked when direct `npm` invocation was blocked
by script execution policy. The profile `check_harness.py` detected `npm.CMD`
automatically.

## Assumptions

- Windows PowerShell users should run `npm.cmd` if `npm.ps1` is blocked by
  execution policy.
- The local `harness-starter-kit/` clone is adoption reference material, not
  target project source.

## Failure Memory

- Recorded: none; adoption smoke probes intentionally triggered checks but did
  not fix a user-visible runtime failure, high-risk bug path, failed CI run,
  repeated agent mistake, or cross-environment mismatch.
- Detection or prevention check: not applicable because no failure record was
  added.
- Skipped: no recurring failure was fixed during this sample adoption.

## Effectiveness Measurement Plan

- Baseline available: No historical agent PR data was available for this sample
  project.
- Comparable tasks to repeat or track: add a utility function, update a test,
  and make a docs-only change without editing source.
- Primary metric: wrong-file edits, repeated temporary-file mistakes, and
  first-pass `npm.cmd run check:harness` success.
- Review window: next 5 comparable Node.js agent changes.
- Results location: `docs/effectiveness/node-harness.md`.
- Task outcome records location: `docs/effectiveness/task-outcomes/`.

## Remaining Manual Steps

- Remove, ignore, or intentionally keep `harness-starter-kit/` before committing
  adoption changes.
- Add CI only after choosing the target repository's CI provider.

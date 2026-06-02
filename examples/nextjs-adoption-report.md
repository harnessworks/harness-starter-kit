# Example Adoption Report: Next.js Target

## Target

`sample-next-dashboard`, a tiny Next.js App Router project using TypeScript.

## Files Added Or Changed

- Added `AGENTS.md` with App Router boundaries, generated-file rules, and
  completion checks.
- Added `.harness/structure-rules.json`.
- Added `scripts/check_docs_drift.py` and `scripts/check_structure.py`.
- Added `docs/conventions/coding.md`, `docs/domain/glossary.md`, and
  `docs/decisions/001-adopt-next-agent-harness.md`.
- Added Next.js profile snippets under `docs/harness/profiles/nextjs/`.
- Added `typecheck`, `check:docs`, `check:structure`, and `check:harness`
  scripts to `package.json`.
- Added `.gitignore` entries for `.next/`, `node_modules/`,
  `tsconfig.tsbuildinfo`, and `harness-starter-kit/`.

## Checks Run

```powershell
npm.cmd run check:harness
```

The command ran these named axes:

- `npm run typecheck`
- `npm run build`
- `npm run check:docs` (`python scripts/check_docs_drift.py`)
- `npm run check:structure` (`python scripts/check_structure.py`)

All checks passed.

## External API Verification

- Required: No. The sample app does not call an external API.
- Live/mock mode: Not applicable.
- Secret handling and redaction checked: Not applicable; no provider secrets or
  server-only API boundary were introduced.
- Empty or zero-result behavior: Not applicable.
- Provider error handling: Not applicable.
- Focused smoke command or fixture: Not added because typecheck, build, docs
  drift, and structure drift covered the adoption scope.

## Findings

- Use `tsc --noEmit --incremental false` to avoid leaving
  `tsconfig.tsbuildinfo` behind.
- Do not assume `next lint` exists. Current Next.js versions may not expose it
  as a valid command.
- `next build` may update `tsconfig.json` and `next-env.d.ts` during initial
  setup. Review those changes as target-project changes.
- `npm audit --audit-level=high` passed. Moderate advisories may still appear
  through Next.js transitive dependencies; do not apply breaking audit fixes
  blindly.

## Effectiveness Measurement Plan

- Baseline available: No historical agent PR data was available for this sample
  app.
- Comparable tasks to repeat or track: edit app UI without changing generated
  Next.js files, add a typed component, and update build config only when the
  task requires it.
- Primary metric: wrong-file edits and first-pass `npm.cmd run check:harness`
  success.
- Review window: next 5 comparable Next.js agent changes.
- Results location: `docs/effectiveness/nextjs-harness.md`.
- Task outcome records location: `docs/effectiveness/task-outcomes/`.

## Remaining Manual Steps

- Remove, ignore, or intentionally keep `harness-starter-kit/` before committing
  adoption changes.
- Add CI only after confirming the target repository uses GitHub Actions or
  another specific provider.

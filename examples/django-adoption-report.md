# Example Adoption Report: Django Target

## Target

`sample-django-site`, a tiny Django project with a `sample_site` project package
and a `tasks` app.

## Files Added Or Changed

- Added `AGENTS.md` with Django project/app boundaries, virtual environment
  rules, generated-file rules, and completion checks.
- Added `.harness/structure-rules.json`.
- Added `scripts/check_docs_drift.py` and `scripts/check_structure.py`.
- Added `scripts/check_harness.py` as the single local verification entrypoint.
- Added `docs/conventions/coding.md`, `docs/domain/glossary.md`, and
  `docs/decisions/001-adopt-django-agent-harness.md`.
- Added Django/Python profile snippets under `docs/harness/profiles/django/`.
- Added `.gitignore` entries for `.venv/`, `db.sqlite3`, generated Python
  caches, and `harness-starter-kit/`.

## Checks Run

```powershell
.\.venv\Scripts\python.exe scripts\check_harness.py
```

The command ran:

- `python manage.py check`
- `python manage.py test`
- `python scripts/check_docs_drift.py`
- `python scripts/check_structure.py`

All checks passed. The sample project had zero Django tests, so the next useful
improvement would be adding behavior tests for real app logic.

## Verification Gate Placement

- Normal completion gate:
  `.\.venv\Scripts\python.exe scripts\check_harness.py`.
- Deterministic behavior checks included in the normal gate: `manage.py check`
  and `manage.py test`; no real product-behavior tests existed yet in the sample
  scaffold.
- Focused or manual checks outside the normal gate: none.
- Reasons for focused/manual placement: not applicable.

## Findings

- A Python `scripts/check_harness.py` entrypoint fits Django projects well when
  there is no existing package task runner.
- Reuse Django's built-in `manage.py check` and `manage.py test` before adding
  pytest, Ruff, mypy, or pre-commit.
- `.venv/`, `db.sqlite3`, generated Python caches, and the local
  `harness-starter-kit/` clone should not be committed.
- Existing migrations should be treated as source and changed only when model
  changes require it.

## Failure Memory

- Recorded: none; adoption did not fix a user-visible runtime failure,
  high-risk bug path, failed check, CI failure, repeated agent mistake, or
  cross-environment mismatch.
- Detection or prevention check: not applicable because no failure record was
  added.
- Skipped: no recurring failure was fixed during this sample adoption.

## Effectiveness Measurement Plan

- Baseline available: No historical agent PR data was available for this sample
  scaffold.
- Comparable tasks to repeat or track: add a model field with a migration, add a
  view without editing settings directly, and add a test for sample app behavior.
- Primary metric: wrong-file edits and first-pass `scripts/check_harness.py`
  success.
- Review window: next 5 comparable Django agent changes.
- Results location: `docs/effectiveness/django-harness.md`.
- Task outcome records location: `docs/effectiveness/task-outcomes/`.

## Remaining Manual Steps

- Remove, ignore, or intentionally keep `harness-starter-kit/` before committing
  adoption changes.
- Add CI only after confirming the target repository's CI provider.
- Add real Django tests once the app has behavior beyond the generated
  scaffold.

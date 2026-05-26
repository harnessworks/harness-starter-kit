# Example Adoption Report: Flask Target

## Target

`sample-flask-api`, a tiny Flask app using an app factory and Flask's test
client.

## Files Added Or Changed

- Added `AGENTS.md` with Flask app factory rules, test commands, virtual
  environment rules, instance-data rules, and completion checks.
- Added `.harness/structure-rules.json`.
- Added `scripts/check_docs_drift.py` and `scripts/check_structure.py`.
- Added `scripts/check_harness.py` as the single local verification entrypoint.
- Added `docs/conventions/coding.md`, `docs/domain/glossary.md`, and
  `docs/decisions/001-adopt-flask-agent-harness.md`.
- Added Flask profile snippets under `docs/harness/profiles/flask/`.
- Added `.gitignore` entries for `.venv/`, generated Python caches, Flask
  instance directories, and `harness-starter-kit/`.

## Checks Run

```powershell
.\.venv\Scripts\python.exe scripts\check_harness.py
```

The command ran:

- `python -m unittest discover -s tests`
- `python -m flask --app sample_flask routes`
- `python scripts/check_docs_drift.py`
- `python scripts/check_structure.py`

All checks passed.

## Findings

- `python -m unittest discover -s tests` is safer than bare
  `python -m unittest discover` when test discovery needs an explicit directory.
- Flask's route table check is a useful lightweight import and route
  registration sensor.
- A Python `scripts/check_harness.py` entrypoint fits Flask projects well when
  there is no existing task runner.
- Avoid documenting optional local directories as backtick paths unless they
  exist, because document drift checks may treat them as missing references.

## Effectiveness Measurement Plan

- Baseline available: No historical agent PR data was available for this sample
  app.
- Comparable tasks to repeat or track: add a route, add a service helper without
  putting business logic in the route, and update tests without touching
  instance data.
- Primary metric: repeated route-boundary mistakes and first-pass
  `scripts/check_harness.py` success.
- Review window: next 5 comparable Flask agent changes.
- Results location: `docs/effectiveness/flask-harness.md`.

## Remaining Manual Steps

- Remove, ignore, or intentionally keep `harness-starter-kit/` before committing
  adoption changes.
- Add CI only after confirming the target repository's CI provider.
- Add broader route or integration tests as app behavior grows.

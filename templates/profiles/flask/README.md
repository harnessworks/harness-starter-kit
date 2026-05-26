# Flask Harness Profile

Use these snippets when the target project is a Flask app or API.

## Recommended Checks

- `python -m unittest discover -s tests` for standard-library tests.
- `python -m flask --app <app_package> routes` to validate the Flask app can
  import and register routes.
- `scripts/check_docs_drift.py` for stale documentation references.
- `scripts/check_structure.py` for temporary or drift-prone files.

Prefer the target repository's virtual environment path when documenting
commands. On Windows PowerShell, that is often:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe -m flask --app sample_flask routes
.\.venv\Scripts\python.exe scripts\check_harness.py
```

## Suggested Check Script

Copy or adapt `check_harness.py` into the target repository's `scripts/`
directory when the project has no existing task runner.

## Flask Notes

- Prefer an app factory named `create_app`.
- Keep Flask package code under the application package, and keep route tests
  under `tests/`.
- Use Flask's test client for HTTP behavior checks.
- Use `python -m unittest discover -s tests` rather than bare
  `python -m unittest discover` when test discovery needs an explicit test
  directory.
- Do not edit or commit `.venv/`, generated Python caches, Flask instance
  directories, or the local `harness-starter-kit/` clone.
- Avoid documenting optional local directories as backtick paths unless they
  actually exist, because document drift checks may treat them as missing
  references.
- Add pytest, Ruff, mypy, or pre-commit only when they fit the target
  repository's existing tooling.

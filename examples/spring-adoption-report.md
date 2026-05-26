# Example Adoption Report: Spring Boot Target

## Target

`sample-spring-service`, a tiny Spring Boot Maven project with a Spring
application context test.

## Files Added Or Changed

- Added `AGENTS.md` with Spring source boundaries, Maven wrapper commands,
  generated-file rules, local configuration rules, and completion checks.
- Added `.harness/structure-rules.json`.
- Added `scripts/check_docs_drift.py` and `scripts/check_structure.py`.
- Added `scripts/check_harness.py` as the single local verification entrypoint.
- Added `docs/conventions/coding.md`, `docs/domain/glossary.md`, and
  `docs/decisions/001-adopt-spring-agent-harness.md`.
- Added Spring profile snippets under `docs/harness/profiles/spring/`.
- Added `.gitignore` entries for generated build outputs, local config files,
  and `harness-starter-kit/`.

## Checks Run

```powershell
python scripts\check_harness.py
```

The command ran:

- `.\mvnw.cmd test`
- `python scripts/check_docs_drift.py`
- `python scripts/check_structure.py`

All checks passed.

## Findings

- Prefer Maven or Gradle wrappers over global build tool installations so
  agents run the same build as maintainers.
- A Spring Boot context test is a useful lightweight startup and wiring sensor.
- Generated build directories such as `target/`, `build/`, `.gradle/`, and
  `out/` should stay out of source control.
- Local `application-local.*` files should not be committed because they often
  contain machine-specific settings or secrets.
- Flyway or Liquibase migrations should be treated as source and reviewed
  carefully when model or schema behavior changes.

## Remaining Manual Steps

- Remove, ignore, or intentionally keep `harness-starter-kit/` before committing
  adoption changes.
- Add CI only after confirming the target repository's CI provider.
- Add controller, repository, or integration tests as real application behavior
  grows.

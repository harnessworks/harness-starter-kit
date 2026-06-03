# Validation Coverage

This document explains how `harness-starter-kit` is validated. The tests prove
that the kit can install baseline files, keep documentation references healthy,
and run local drift checks. They do not prove that harness adoption reduces
agent mistakes; measure that separately with `docs/evaluation.md`.

## Local Validation

Run these checks before changing starter-kit templates, installer behavior,
drift scripts, command documents, or README structure. On macOS/Linux, use
`python3` instead of `python` when `python` is unavailable:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/check_failure_memory.py scripts/check_decision_memory.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/check_failure_memory.py
python scripts/check_decision_memory.py
python scripts/harness_doctor.py --target .
```

Profile README consistency is covered by
`tests/test_profile_consistency.py`, which runs as part of the full unittest
suite. Run it directly when adding or changing profile guidance:

```powershell
python -m unittest tests.test_profile_consistency
```

## Fixture Smoke Tests

Automated fixture smoke tests cover harness installation for:

- Node.js / TypeScript
- Next.js
- Django
- FastAPI
- Flask
- React
- Spring Boot
- Android / Kotlin Gradle
- Vue

These tests verify that the installer preserves existing files, writes expected
profile snippets, and produces runnable generic drift checks.

## Manual And Opt-In E2E Checks

Additional end-to-end adoption checks have been run manually against:

- a Node.js ES module project using `node --test`, repeated installer runs, the
  TypeScript profile `check_harness.py`, and intentional drift failures
- a FastAPI project using pytest, mypy, generated drift checks, and the FastAPI
  profile `check_harness.py`

FastAPI E2E coverage is available as an opt-in automated test because it
creates a virtual environment and installs dependencies:

```powershell
$env:RUN_FASTAPI_E2E = "1"
python -m unittest tests.test_fastapi_profile_e2e
```

In GitHub Actions, run the `Harness Check` workflow manually and enable
`run_fastapi_e2e` to execute the dependency-installing test.

## Lifecycle Pilots

Pilot lifecycle tests have validated prompt-first adoption from blank
repositories into minimal Django and Next.js projects. These tests verified
generic-first adoption, later stack-specific profile absorption, filled
measurement plans, and runnable local checks. The Next.js pilot also verified
post-adoption cleanup and Git hygiene after removing the local kit clone.

See `docs/examples/lifecycle-pilot-results.md` for the detailed pilot summary.

## Live Adoption Target

[baskduf/harness_starter_kit_django](https://github.com/baskduf/harness_starter_kit_django)
is the active dogfooding repository for this kit. It is used to validate
prompt-first adoption, Django profile absorption, `/harness update`, failure
memory, and effectiveness measurement workflows in a real target repository.

This is operational evidence, not proof that harness adoption reduces agent
mistakes by itself. Record comparable task outcomes in effectiveness reports.

## Example Reports

Use these examples when checking whether a target adoption report is complete:

- `examples/node-adoption-report.md`
- `examples/nextjs-adoption-report.md`
- `examples/django-adoption-report.md`
- `examples/flask-adoption-report.md`
- `examples/spring-adoption-report.md`
- `examples/node-effectiveness-report.md`

## What This Does Not Prove

Fixture tests, smoke tests, and lifecycle pilots validate installation behavior,
runnable checks, and measurement readiness. They do not prove that harness
adoption reduces repeated agent mistakes, CI failure rates, or human rework.

Use `docs/evaluation.md` and
`docs/templates/effectiveness-report.md` to record comparable before/after or
harnessed-only observations.

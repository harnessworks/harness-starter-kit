---
name: harness-doctor
description: Run the diagnostic Harness Doctor workflow. Use when the user asks for /harness doctor, harness score, repository harness readiness, or a no-edit harness health report.
argument-hint: "[target path]"
---

# Harness Doctor

Evaluate repository harness health without modifying files.

## Steps

1. Read `../../references/package-contract.md`.
2. Read `../../references/doctor-workflow.md`.
3. If `./harness-starter-kit/commands/harness-doctor.md` exists in the target,
   prefer that canonical workflow.
4. Inspect durable repository evidence.
5. Run `python scripts/harness_doctor.py --target .` when available.
6. Produce the Harness Doctor Report.

## Boundaries

- Do not create, edit, delete, move, format, or stage files.
- Do not remove a nested `./harness-starter-kit` directory.
- Score repository-visible harness health, not claimed agent effectiveness.

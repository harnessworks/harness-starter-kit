---
name: harness-refresh
description: Review stale, duplicated, obsolete, or unused target harness guidance. Use when the user asks for /harness refresh or wants harness maintenance recommendations without default edits.
argument-hint: "[target details]"
---

# Harness Refresh

Review an existing target harness for maintenance needs.

## Steps

1. Read `../../references/package-contract.md`.
2. Read `../../references/refresh-workflow.md`.
3. If `./harness-starter-kit/commands/harness-refresh.md` exists in the
   target, prefer that canonical workflow.
4. Inspect current harness docs, rules, memory records, checks, and normal
   command wiring.
5. Classify findings as keep, update, merge, archive/delete candidate, or
   manual review.
6. Run lightweight checks when available.
7. Produce the Harness Refresh Report.

## Boundaries

- Do not delete, archive, move, rename, format, or stage files unless the user
  explicitly approves the specific files.
- Report recommendations by default.

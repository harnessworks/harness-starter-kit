---
name: harness-update
description: Refresh an adopted target repository from the latest Harness Starter Kit reference. Use when the user asks for /harness update or wants source tracking and selective harness updates.
argument-hint: "[target details]"
---

# Harness Update

Refresh a target repository's harness from a confirmed kit source.

## Steps

1. Read `../../references/package-contract.md`.
2. Read `../../references/update-workflow.md`.
3. If `./harness-starter-kit/commands/harness-update.md` exists in the target,
   prefer that canonical workflow.
4. Inspect target status before editing.
5. Refresh or inspect the local kit reference without destructive operations.
6. Classify candidates as safe, patch carefully, reference only, manual
   review, or deferred.
7. Apply only target-specific, non-conflicting updates.
8. Update source tracking only when the current kit source is known.
9. Run checks and produce the Harness Update Report.

## Boundaries

- Never blindly overwrite target files.
- Never delete, replace, or re-clone a dirty target-local kit reference.
- Keep source tracking separate from patches to pre-existing dirty files.

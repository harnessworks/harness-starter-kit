# Harness Update Workflow

Use this when refreshing a target repository's harness from a newer Harness
Starter Kit reference. This workflow may modify target files, but never by
blind overwrite.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect target state before changing files:
   - branch and dirty status
   - existing harness files
   - existing `.harness/source.json`
   - existing local kit clone state when present
3. Refresh or inspect the local `./harness-starter-kit` reference:
   - clone it if missing and the user asked for update behavior
   - pull only when clean, on the expected remote, and fast-forwardable
   - do not delete, replace, or re-clone dirty or suspicious local clones
4. Compare previous source tracking with current kit source when possible.
5. Classify candidates:
   - safe candidate
   - patch carefully
   - reference only
   - manual review
   - deferred because the target file was pre-existing dirty
6. Apply only changes that fit the target repository's existing tools and
   conventions.
7. Update `.harness/source.json` only after the current kit source is known and
   the report can explain applied, skipped, and deferred items.
8. Add failure memory only if the update fixes a recurring or high-risk failure
   path that should not recur.
9. Run relevant checks.

## Report Format

```text
Harness Update Report

Kit Source:
- URL: <kit URL>
- Previous commit: <commit or unknown>
- Current commit: <commit>
- Reference clone state: <state>

Target State:
- Branch/status: <summary>
- Existing harness files reviewed: <files>
- Pre-existing target changes: <dirty files or none>
- Dirty target handling: <summary>

Applied:
- <target-specific update>

Skipped:
- <candidate and reason>

Manual Review:
- <maintainer decision needed>

Checks Run:
- <command>: <result>

Failure Memory:
- Recorded: <path or none>
- Detection/prevention check: <check or reason>
- Skipped: <reason if no note added>

Source Tracking:
- `.harness/source.json`: <created, updated, unchanged, or blocked>
- Deferred target patches: <items or none>
```

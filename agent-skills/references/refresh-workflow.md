# Harness Refresh Workflow

Use this diagnostic maintenance workflow to review an existing target harness
for stale, duplicated, obsolete, or unused guidance. Do not delete, archive,
move, rename, format, or stage files unless the user explicitly approves the
specific files.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect current architecture, docs, commands, package manager, CI, and
   existing harness files.
3. Look for:
   - stale docs that reference missing commands, paths, tools, or old stack
     assumptions
   - duplicated guidance split across instruction files, README, and docs
   - obsolete decision or failure records
   - checks that no normal command, CI workflow, or documentation uses
   - profile snippets that were copied but never absorbed into real project
     rules
4. Review gate placement. Deterministic, local, non-network, reasonably fast
   checks that agents should repeat belong in the documented normal completion
   gate. Record the normal completion gate unless there is a focused or manual
   placement reason.
5. Classify each finding as keep, update, merge, archive/delete candidate, or
   manual review.
6. Run lightweight drift checks when available.
7. Report recommendations without modifying files by default.

## Report Format

```text
Harness Refresh Report

Target State:
- Branch/status: <summary>
- Harness files reviewed: <files>
- Project commands/configs reviewed: <files>

Keep:
- <still useful guidance>

Update:
- <stale guidance and proposed patch>

Merge:
- <duplicated guidance and proposed destination>

Archive/Delete Candidates:
- <candidate and reason, pending explicit approval>

Manual Review:
- <maintainer decision needed>

Checks Run:
- <command>: <result>

Risks:
- <risk>

Recommended Next Actions:
1. <action>
2. <action>
3. <action>
```

# /harness update

Update a target repository's harness from the latest
`harness-starter-kit` reference material.

Harness Update is allowed to modify target repository files, but it must never
blindly overwrite existing target files. The target repository remains the
source of truth.

## Goal

Refresh the local `./harness-starter-kit` reference clone, compare the target
repository's recorded harness source against the updated kit, apply only safe
and useful harness improvements, and finish with a clear update report.

## Source Tracking

Record the kit source used by the target repository in `.harness/source.json`:

```json
{
  "kit_url": "https://github.com/baskduf/harness-starter-kit",
  "kit_commit": "<current-kit-commit>",
  "updated_at": "YYYY-MM-DD",
  "update_command": "/harness update"
}
```

This file belongs to the target repository. It is not a file inside the
`./harness-starter-kit` clone.

If `.harness/source.json` is missing, treat the previous kit commit as
`unknown`. If `./harness-starter-kit` already exists, use its current `HEAD` as
fallback evidence before updating.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect target repository state before changing files:
   - `git status --short --branch`
   - existing `AGENTS.md`, `README.md`, `CLAUDE.md`, contribution docs, CI
     configs, package manifests, and harness scripts
   - existing `.harness/source.json`, if present
3. Refresh the kit reference:
   - If `./harness-starter-kit` does not exist, clone
     `https://github.com/baskduf/harness-starter-kit` into that path.
   - If it exists, inspect `git -C harness-starter-kit status --short`,
     `git -C harness-starter-kit remote -v`, and
     `git -C harness-starter-kit rev-parse HEAD`.
   - If the clone is clean and points to the expected remote, run
     `git -C harness-starter-kit pull --ff-only origin main`.
   - If the clone is dirty, has a different remote, is not a Git repository, or
     cannot fast-forward, do not delete or replace it. Report manual resolution
     instead.
4. Compare the previous kit commit from `.harness/source.json` with the updated
   kit `HEAD` when both are available.
5. Classify kit changes and target update opportunities:
   - `safe candidate`: new baseline files that do not conflict with target
     files.
   - `patch carefully`: existing target files such as `AGENTS.md`, drift
     checks, adoption reports, or local docs that may need a small adapted
     patch.
   - `reference only`: templates, profiles, examples, or README guidance that
     should inform the agent but should not be copied directly.
   - `manual review`: CI workflows, package scripts, pre-commit hooks,
     dependency rules, architecture constraints, or anything that changes the
     target's normal development workflow.
6. Apply only changes that fit the target repository's existing architecture,
   package manager, docs, and verification path.
7. Never overwrite an existing target file wholesale. Patch existing files
   carefully after reading them.
8. Update `.harness/source.json` only after the updated kit source is known and
   the report can explain what was applied, skipped, or deferred.
9. If the update fixes a failed CI run, failed harness check, repeated agent
   mistake, or cross-environment mismatch, add a `docs/failures/*.md` record
   unless the failure is purely transient. If no failure note is added, explain
   why in the update report.
10. Run relevant local checks, such as docs drift, structure drift, effectiveness
   plan checks, project tests, linting, type checks, or `/harness doctor`.

## Required Report Format

```text
Harness Update Report

Kit Source:
- URL: <kit URL>
- Previous commit: <commit or unknown>
- Current commit: <commit>
- Reference clone state: <clean, updated, cloned, dirty, wrong remote, or blocked>

Target State:
- Branch/status: <summary>
- Existing harness files reviewed: <files>

Applied:
- <target-specific update applied>

Skipped:
- <candidate skipped and why>

Manual Review:
- <item that needs maintainer decision>

Checks Run:
- <command>: <result>

Failure Memory:
- Recorded: <docs/failures/... or none>
- Skipped: <reason if no failure note was added>

Source Tracking:
- `.harness/source.json`: <created, updated, unchanged, or blocked>
```

## Safety Rules

- Do not delete, replace, or re-clone a dirty target-local
  `./harness-starter-kit` directory.
- Do not use `--force`, destructive Git commands, or wholesale copy operations
  to update target files.
- Do not add CI, pre-commit, package scripts, dependency constraints, or
  architecture checks unless they fit the target repository's existing tools.
- Do not treat profile snippets as mandatory changes.
- If no safe update is available, report that clearly and only update
  `.harness/source.json` when the kit source was successfully confirmed.

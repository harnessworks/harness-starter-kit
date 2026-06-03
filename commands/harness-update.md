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
   - if the target worktree is dirty, record which files were already modified
     before the update and treat them as pre-existing target changes
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
5. If the target worktree was dirty before the update, keep source tracking
   separate from target mutation:
   - still use the latest confirmed kit commit after the reference clone was
     refreshed, when refresh was possible
   - update `.harness/source.json` to the latest confirmed kit commit when the
     source is known, even if some target file patches are deferred
   - do not patch target files that were already dirty unless the user
     explicitly approves the specific file or the patch is clearly
     non-conflicting
   - classify changes to pre-existing dirty target files as `deferred` or
     `manual review` when unsure
   - separate pre-existing target changes from update-applied changes in the
     report
6. Classify kit changes and target update opportunities:
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
7. Apply only changes that fit the target repository's existing architecture,
   package manager, docs, and verification path.
8. Never overwrite an existing target file wholesale. Patch existing files
   carefully after reading them.
9. Update `.harness/source.json` only after the updated kit source is known and
   the report can explain what was applied, skipped, or deferred.
10. If the update fixes a user-visible runtime failure or high-risk bug path that
   should not recur, including a 5xx error, crash, security or permission bug,
   data-loss risk, failed CI run, failed harness check, repeated agent mistake,
   previously identified bug path, or cross-environment mismatch, add a
   `docs/failures/*.md` record unless the issue was purely transient or already
   covered by an existing failure note. Name the regression test, fixture, smoke
   check, lint rule, drift check, CI gate, or manual review point that prevents
   or detects recurrence. If no failure note or check is added, explain why in
   the update report.
11. Run relevant local checks, such as docs drift, structure drift, effectiveness
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
- Pre-existing target changes: <dirty files before update, or none>
- Dirty target handling: <latest kit used; source tracking updated; dirty-file patches applied, deferred, or manual-review>

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
- Detection/prevention check: <test, fixture, smoke check, lint rule, drift
  check, CI gate, manual review point, or reason none is practical>
- Skipped: <reason if no failure note was added>

Source Tracking:
- `.harness/source.json`: <created, updated, unchanged, or blocked>
- Deferred target patches: <dirty-file candidates deferred, or none>
```

## Safety Rules

- Do not delete, replace, or re-clone a dirty target-local
  `./harness-starter-kit` directory.
- A dirty target worktree does not by itself block using the latest clean kit
  reference or updating `.harness/source.json` to the latest confirmed kit
  commit. It does require separating source tracking from target file mutation.
- Do not patch target files that were already dirty before the update unless the
  user explicitly approves the specific file or the patch is clearly
  non-conflicting.
- Do not use `--force`, destructive Git commands, or wholesale copy operations
  to update target files.
- Do not add CI, pre-commit, package scripts, dependency constraints, or
  architecture checks unless they fit the target repository's existing tools.
- Do not treat profile snippets as mandatory changes.
- If no safe update is available, report that clearly and only update
  `.harness/source.json` when the kit source was successfully confirmed.

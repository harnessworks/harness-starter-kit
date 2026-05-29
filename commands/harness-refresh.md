# /harness refresh

Refresh a target repository's existing harness by reviewing whether its
agent-facing rules, knowledge store, and drift checks are still accurate.

Harness Refresh is maintenance for the target harness. It does not refresh the
local `./harness-starter-kit` reference clone and does not replace
`/harness update`.

## Goal

Inspect the target repository's current harness, classify stale or conflicting
artifacts, apply only safe documentation/check updates, and finish with a clear
Harness Refresh Report.

Use this command when the maintainer wants to reduce old guidance, duplicate
records, obsolete failure notes, stale decisions, or unused harness checks.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect target repository state before changing files:
   - `git status --short --branch`
   - `AGENTS.md`, `CLAUDE.md`, README files, contribution docs, and CI configs
   - `.harness/source.json`, if present
   - `docs/decisions/`, `docs/failures/`, `docs/conventions/`, and
     `docs/domain/`
   - `scripts/check_*.py`, `scripts/check_harness.py`, package scripts, test
     configs, lint configs, and pre-commit config
3. Build a short inventory of harness artifacts and classify each relevant item:
   - `keep`: still accurate and useful.
   - `update`: useful but stale, incomplete, or unclear.
   - `merge`: duplicate or overlapping guidance that should be consolidated.
   - `archive/delete candidate`: likely obsolete or unused, but not removed
     without explicit user approval.
   - `manual review`: needs a maintainer decision because it changes workflow,
     CI, dependencies, architecture rules, or historical records.
4. Check for:
   - stale docs that reference missing commands, paths, or tools
   - duplicated guidance split across `AGENTS.md`, README files, and docs
   - obsolete decisions or failure records contradicted by current code
   - harness checks that no normal command, CI workflow, or documentation uses
   - rules that describe architecture constraints no check or review point can
     enforce
5. For large docs directories, list files first and read only records relevant
   to the refresh question, stale/conflict signals, or current harness rules.
6. Patch only safe, target-specific updates that preserve the repository's
   current architecture, tools, commands, and documentation style.
7. Prefer marking decision and failure records as superseded or obsolete over
   deleting them. If a replacement record is clearer, add or update the
   replacement and cross-reference the old record.
8. Do not delete, archive, move, or wholesale replace files unless the user
   explicitly approves the specific files after seeing the candidates.
9. Run relevant local checks, such as docs drift, structure drift,
   effectiveness plan checks, project tests, linting, type checks, or
   `/harness doctor`.

## Required Report Format

```text
Harness Refresh Report

Reviewed Files:
- <files and directories reviewed>

Current Harness State:
- <short summary of current agent instructions, docs, checks, and CI wiring>

Stale Or Conflicting Docs:
- <stale, duplicated, or contradictory guidance found>

Merge/Update Candidates:
- <safe updates or consolidation opportunities>

Archive/Delete Candidates:
- <candidate and why it was not removed automatically>

Checks Run:
- <command>: <result>

Manual Decisions Needed:
- <maintainer decision needed before delete, archive, CI, dependency, or
  architecture-rule changes>

Recommended Next Work:
1. <highest-value follow-up>
2. <next follow-up>
3. <next follow-up>
```

## Safety Rules

- Do not refresh or pull `./harness-starter-kit`; use `/harness update` for kit
  source updates.
- Do not delete, archive, move, or rename files without explicit user approval
  for the specific files.
- Do not erase historical decision or failure context just because it is old.
  Prefer `superseded` or `obsolete` notes with links to the replacement.
- Do not remove a harness check only because it is currently failing. First
  decide whether the check caught real drift, needs an update, or is truly
  unused.
- Do not add CI, pre-commit, package scripts, dependency constraints, or
  architecture checks unless they fit the target repository's existing tools.

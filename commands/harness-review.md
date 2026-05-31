# /harness review

Review the current change set from an opposing harness-engineering perspective.

Harness Review is diagnostic by default. Do not create, edit, delete, move,
format, or stage files while running this command unless the user explicitly
asks you to apply fixes after seeing the review.

## Goal

Challenge whether the current work preserves the target repository as the
source of truth, avoids unnecessary automation, keeps templates conservative,
adds enforceable checks only where practical, updates durable memory when
needed, and runs the right validation before completion.

Use a separate reviewer perspective or subagent when the environment supports
it, but do not depend on any specific agent runtime. The review should report
findings, questions, missing checks, overreach, and follow-up recommendations;
it should not continue implementation.

## Scope

Harness Review reviews the current work or proposed change set. It does not
score harness readiness like `/harness doctor`, refresh the local kit reference
like `/harness update`, or clean up stale target harness guidance like
`/harness refresh`.

It is also different from the maintenance checklist in
`docs/checklists/harness-review.md`. That checklist is for monthly or repeated
mistake review; this command is for the current change set.

It must not implement runtime hooks, policy-driven enforcement, pre-commit
hooks, CI adapters, subagent execution, or broader installer automation.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect repository state and the change set:
   - `git status --short --branch`
   - `git diff --stat`
   - `git diff --check`
   - `git diff --cached --stat` and `git diff --cached --check` when staged
     changes exist
3. Review changed files and nearby harness context:
   - changed `AGENTS.md`, `CLAUDE.md`, README files, contribution docs, and CI
     configs
   - changed `commands/`, `docs/`, `templates/`, `scripts/`, package manifests,
     lint configs, test configs, and pre-commit config
   - `docs/decisions/`, `docs/failures/`, `docs/conventions/`, and
     `docs/domain/` when the change affects architecture, behavior, workflow,
     integration boundaries, or repeated failure paths
4. Challenge source-of-truth preservation:
   - Does the change preserve the target repository's architecture, tools,
     package manager, docs, commands, and conventions?
   - Does it avoid copying starter-kit templates blindly?
   - Does it keep profile snippets as reference material instead of mandatory
     transformations?
5. Challenge overreach and automation:
   - Does the change add package scripts, pre-commit hooks, CI wiring, runtime
     hooks, dependency constraints, or policy enforcement without target
     evidence and maintainer approval?
   - Does it make the installer more automatic or more willing to overwrite
     target files?
   - Are templates still generic and conservative?
6. Challenge checks and validation:
   - Are important rules enforceable through lint, tests, type checks, import
     rules, CI, or drift checks where practical?
   - If automation is not practical, is the manual review point documented?
   - Were the right local checks run for the files changed?
   - Are missing checks or unverified assumptions named clearly?
7. Challenge durable memory:
   - Does the change require a decision record, failure note, convention update,
     domain note, adoption report update, or effectiveness measurement update?
   - If no durable memory was added, is that justified?
   - If the work fixed a user-visible runtime failure, high-risk bug path,
     failed CI run, failed harness check, repeated agent mistake, or
     cross-environment mismatch, was `docs/failures/*.md` updated or explicitly
     skipped with a reason?
8. Check for stale or duplicated guidance:
   - Are new command docs, templates, examples, README links, component maps, and
     tests aligned?
   - Does the change duplicate existing guidance instead of updating the
     authoritative location?
9. Produce the required report format. Do not apply fixes unless the user asks
   for a follow-up implementation after reviewing the report.

## Required Report Format

```text
Harness Review Report

Reviewed Changes:
- Branch/status: <summary>
- Changed files reviewed: <files>
- Review scope: <current diff, staged diff, PR diff, or described change>

Findings:
- <severity>: <finding with file/path evidence, or "none">

Missing Checks:
- <check that should be run, why it matters, or "none">

Durable Memory Assessment:
- Decision records: <needed, updated, skipped with reason>
- Failure records: <needed, updated, skipped with reason>
- Conventions/domain/effectiveness docs: <needed, updated, skipped with reason>

Overreach Risk:
- <source-of-truth, unnecessary automation, installer, template, policy, CI,
  pre-commit, or runtime-hook risk, or "none">

Manual Decisions Needed:
- <maintainer decision needed before applying changes, or "none">

Recommended Follow-Up:
1. <highest-value follow-up>
2. <next follow-up>
3. <next follow-up>
```

## Safety Rules

- Do not modify files during `/harness review` unless the user explicitly asks
  to apply fixes after seeing the review.
- Do not stage, commit, format, delete, archive, move, or rename files while
  reviewing.
- Do not add runtime hooks, subagent execution, policy enforcement, pre-commit
  hooks, CI adapters, package scripts, dependency constraints, or broader
  installer automation as part of the review.
- Do not treat a clean review as proof of agent effectiveness. It is a
  change-set diagnostic, not an outcome measurement.
- If you recommend a stronger check or policy, present it as follow-up or a
  maintainer decision unless the user explicitly asks to implement it.

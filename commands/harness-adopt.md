# /harness adopt

Apply Harness Starter Kit to the current target repository with the prompt-first
adoption workflow.

Harness Adopt may modify target repository files, but it must stay conservative:
inspect first, preserve the target repository as the source of truth, and add
only the smallest useful harness pieces.

## Goal

Turn the target repository's real conventions, checks, repeated mistakes, and
review expectations into durable harness artifacts: agent instructions,
constraints, feedback loops, memory, evaluation, and governance.

This command is for first-time adoption. It is not a blind installer and not a
request to copy every starter-kit template.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect the target repository before editing:
   - `git status --short --branch`
   - existing `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`, or
     `.github/copilot-instructions.md`
   - `README.md`, `CONTRIBUTING.md`, package manifests, CI configs, and local
     verification commands
   - existing docs under `docs/`, especially decisions, failures, conventions,
     domain notes, and evaluation records
3. If `./harness-starter-kit` exists, treat it as read-only reference material.
   If it does not exist and the user asked you to use this kit from GitHub, clone
   `https://github.com/harnessworks/harness-starter-kit` into that path for
   reference.
4. Read the canonical adoption workflow from the local kit reference when
   available:
   - `./harness-starter-kit/docs/adoption-workflow.md`
   - `./harness-starter-kit/docs/prompts/apply-to-target-repo.md`
   - relevant profile snippets under
     `./harness-starter-kit/templates/profiles/<profile>/`
5. Select the smallest useful adoption set for this target. Prefer updating
   existing docs/configs over adding parallel files.
6. Add or update only artifacts that fit the target's existing architecture,
   tools, package manager, docs, commands, and conventions. Common candidates:
   - agent instructions
   - lightweight drift checks
   - decision or failure memory templates
   - convention or domain notes
   - an adoption report with verification and measurement plan
7. Do not add CI, pre-commit hooks, dependencies, package scripts, or broad
   architecture rules unless they match the target's existing workflow and the
   maintainer asked for that level of enforcement.
8. Run relevant local checks using the target repository's existing tools, plus
   any adopted harness checks.
9. Finish with the required report format and state whether the nested
   `./harness-starter-kit` reference should be removed, ignored, or kept before
   commit.

## Required Report Format

```text
Harness Adoption Report

Target State:
- Branch/status: <summary>
- Existing tools and verification commands: <summary>
- Existing agent/harness files reviewed: <files or none>

Applied:
- <target-specific harness artifact added or updated>

Skipped:
- <starter-kit template/profile/check skipped and why>

Checks Run:
- <command>: <result>

Assumptions:
- <assumption made while adapting the kit, or none>

Manual Steps:
- <maintainer action needed, or none>

Failure Memory:
- Recorded: <docs/failures/... or none>
- Detection/prevention check: <test, fixture, smoke check, lint rule, drift check,
  CI gate, manual review point, or reason none is practical>
- Skipped: <reason if no failure note was added>

Effectiveness Measurement Plan:
- Baseline available: <yes/no/unknown>
- Tasks to track: <next comparable tasks>
- Primary metric: <wrong-file edits, first-pass verification, repeated mistakes,
  drift detections, human rework, or other>
- Review window: <for example, next 5 agent PRs>
- Recording location: <where future outcomes should be stored>

Gate Placement:
- Normal completion gate: <commands agents should run before finishing>
- Focused/manual checks: <checks excluded from normal gate and why>

Reference Clone:
- `./harness-starter-kit`: <remove, ignore, keep intentionally, or not present>
```

## Safety Rules

- Do not blindly copy templates.
- Do not overwrite existing target files wholesale.
- Do not delete, move, re-clone, or clean up target files without explicit user
  approval.
- Treat profile snippets as reference material, not mandatory transformations.
- Preserve the target repository's existing architecture, tools, docs, package
  manager, commands, and conventions.
- If no safe useful adoption is available, report that clearly instead of making
  cosmetic harness changes.

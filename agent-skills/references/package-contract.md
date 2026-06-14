# Harness Agent Skills Package Contract

Use this package as an adapter over Harness Starter Kit, not as a replacement
for target-repository judgment.

## Source Priority

1. The target repository is the source of truth for architecture, commands,
   docs, package manager, CI, naming, and conventions.
2. If the target has a local Harness Starter Kit clone, prefer its canonical
   workflow docs:
   - adoption: `harness-starter-kit/docs/adoption-workflow.md`
   - doctor: `harness-starter-kit/commands/harness-doctor.md`
   - update: `harness-starter-kit/commands/harness-update.md`
   - refresh: `harness-starter-kit/commands/harness-refresh.md`
   - review: `harness-starter-kit/commands/harness-review.md`
3. If no local kit clone is available, use the bundled workflow references in
   this package.

## Safety Rules

- Inspect the target repository before editing.
- Preserve existing architecture, docs, scripts, CI, package manager, and
  command conventions.
- Do not blindly copy templates.
- Do not overwrite, delete, move, re-clone, or broadly format target files
  unless the user explicitly asks and the reason is clear.
- Treat a target-local `./harness-starter-kit` clone as read-only reference
  material unless the user asks to edit the kit itself.
- Prefer enforceable checks when practical. If automation is not practical,
  record the manual review point.
- Diagnostic workflows do not modify files.
- Mutating workflows must report changed files, checks run, skipped items,
  assumptions, and remaining manual steps.

## Command Map

| User intent | Skill | Bundled reference |
| --- | --- | --- |
| `/harness adopt` or apply the kit | `harness-adopt` | `adopt-workflow.md` |
| `/harness doctor` | `harness-doctor` | `doctor-workflow.md` |
| `/harness update` | `harness-update` | `update-workflow.md` |
| `/harness refresh` | `harness-refresh` | `refresh-workflow.md` |
| `/harness review` or `/harness review sub-agent` | `harness-review` | `review-workflow.md` |

## Failure And Outcome Memory

Record a failure note when the work fixes a user-visible runtime failure or
high-risk bug path that should not recur, unless the issue is purely transient
or already covered by an existing failure note. Name the regression test,
fixture, smoke check, lint rule, drift check, CI gate, or manual review point
that prevents or detects recurrence.

Record task outcome evidence for substantial harness-maintenance work that
changes profiles, check scripts, command workflows, adoption workflow, dogfood
or effectiveness evidence, first-pass verification results, known failure
paths, failed CI or harness checks, cross-environment mismatches, or high-risk
integration behavior. Skip it for trivial wording, typo, link-label, or
formatting-only changes.

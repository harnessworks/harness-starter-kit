# {{PROFILE_NAME}} Harness Profile

Use these snippets when the target project is {{PROFILE_DESCRIPTION}}.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

Apply this profile by priority: always preserve the target architecture,
generated-file rules, and exact local checks; document local services, fixtures,
or environment setup when present; consider decision records only when changing
architecture, persistence, state, runtime, or integration policy; use a short
final report or check note for a narrow fix.

## Recommended Checks

- TODO: list the target stack's normal test, build, lint, or type-check command.
- `python scripts/check_docs_drift.py` for stale documentation references.
- `python scripts/check_structure.py` for temporary or drift-prone files.

## Suggested Check Script

Copy or adapt `check_harness.py` into the target repository's `scripts/`
directory only when the target has no equivalent local verification command.
When a harness command grows beyond a simple wrapper, make it print or document
which axes it checks, such as lint, typecheck, build, docs drift, structure
drift, server smoke, external API smoke, or route table validation.

## Profile Absorption Notes

When {{PROFILE_NAME}} is introduced after generic adoption:

- Merge useful snippets into existing project files instead of replacing them.
- Keep the target package manager, framework conventions, and local environment
  workflow as source of truth.
- Update `AGENTS.md` with stack commands, source directories, generated paths,
  and completion checks.
- Update `docs/conventions/coding.md` with stack-specific conventions that
  agents should repeat.
- Consider a decision record when changing or selecting architecture,
  persistence, state, runtime, or integration policy. When the task only follows
  the existing architecture or makes a narrow fix, a final report or check note
  is enough.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## {{PROFILE_NAME}} Notes

- TODO: list stack-specific cautions that are conditional and practical.

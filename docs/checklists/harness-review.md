# Harness Maintenance Review Checklist

Run this monthly or after repeated agent mistakes.

This maintenance checklist is different from the `/harness review` command in
`commands/harness-review.md`. Use `/harness review` for a diagnostic review of
the current change set; use this checklist for periodic harness maintenance.

- [ ] Did an agent repeat a mistake that should become a rule?
- [ ] Does every important `AGENTS.md` rule have a test, lint, review, or CI
      sensor where practical?
- [ ] Do docs reference files or commands that no longer exist?
- [ ] Are there temporary, duplicate, backup, or one-off files in source paths?
- [ ] Are rejected approaches documented in `docs/failures/`?
- [ ] Are new architecture decisions documented in `docs/decisions/`?
- [ ] Did any behavior, integration boundary, permission fallback, hardware
      dependency, or server fixture policy change without a decision record?
- [ ] Do local servers, database seeds, JARs, docker-compose services, mock APIs,
      emulators, or device prerequisites have a documented verification plan?
- [ ] For broad feature work, is there a scenario test note, or a written reason
      build-only validation is enough?
- [ ] If localized text is present, are UTF-8 and mojibake risks covered by a
      check or manual audit note?
- [ ] Are test failures and error messages specific enough for an agent to fix?
- [ ] Are stack-specific snippets still aligned with the target toolchain?
- [ ] If a new stack was introduced after generic adoption, was the profile
      absorption checklist completed?
- [ ] Is the effectiveness measurement plan current, with a baseline status,
      comparable tasks, primary metric, review window, and results location?
- [ ] If comparable agent work has happened since adoption, was an
      effectiveness report updated with observable results?

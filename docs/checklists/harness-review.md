# Harness Review Checklist

Run this monthly or after repeated agent mistakes.

- [ ] Did an agent repeat a mistake that should become a rule?
- [ ] Does every important `AGENTS.md` rule have a test, lint, review, or CI
      sensor where practical?
- [ ] Do docs reference files or commands that no longer exist?
- [ ] Are there temporary, duplicate, backup, or one-off files in source paths?
- [ ] Are rejected approaches documented in `docs/failures/`?
- [ ] Are new architecture decisions documented in `docs/decisions/`?
- [ ] Are test failures and error messages specific enough for an agent to fix?
- [ ] Are stack-specific snippets still aligned with the target toolchain?
- [ ] If a new stack was introduced after generic adoption, was the profile
      absorption checklist completed?
- [ ] Is the effectiveness measurement plan current, with a baseline status,
      comparable tasks, primary metric, review window, and results location?
- [ ] If comparable agent work has happened since adoption, was an
      effectiveness report updated with observable results?

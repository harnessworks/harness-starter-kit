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
- [ ] Does each new or updated failure record name a regression test, fixture,
      smoke check, lint rule, drift check, CI gate, or manual review point, or
      explain why no check is practical?
- [ ] Are new architecture decisions documented in `docs/decisions/`?
- [ ] Did any behavior, integration boundary, permission fallback, hardware
      dependency, or server fixture policy change without a decision record?
- [ ] Do local servers, database seeds, JARs, docker-compose services, mock APIs,
      emulators, or device prerequisites have a documented verification plan?
- [ ] Are deterministic, local, non-network, reasonably fast checks for product
      behavior that agents are expected to verify repeatedly included in the
      documented normal completion gate, or is there a recorded reason they
      remain focused or manual?
- [ ] Are live API, credential, quota, provider-uptime, visual, device, slow, or
      otherwise fragile checks kept separate from the normal gate when they are
      unsafe as default verification?
- [ ] For broad feature work, is there a scenario test note, or a written reason
      build-only validation is enough?
- [ ] If localized text is present, are UTF-8 and mojibake risks covered by a
      check or manual audit note?
- [ ] Are test failures and error messages specific enough for an agent to fix?
- [ ] Did `/harness review` run before push for substantial harness or
      integration-boundary changes, or is the post-push/skipped reason recorded?
- [ ] Are stack-specific snippets still aligned with the target toolchain?
- [ ] If a new stack was introduced after generic adoption, was the profile
      absorption checklist completed?
- [ ] Is the effectiveness measurement plan current, with a baseline status,
      comparable tasks, primary metric, review window, and results location?
- [ ] If comparable agent work has happened since adoption, was an
      effectiveness report updated with observable results?

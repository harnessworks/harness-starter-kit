# Verification Script Patterns

Use this checklist when a target repository needs more than lint, typecheck,
test, and build to prove that an agent change works.

The best harness checks are transparent. They say which axis they verify, can
run independently, and fail with a message that tells the next agent where to
look.

## When To Add A Script

Add or adapt a script when:

- a live or mocked backend path must be exercised repeatedly
- an external API can return provider-specific envelopes, zero results, or mixed
  JSON/XML responses
- a route table, generated output location, import boundary, or env contract is
  important enough to enforce
- the same manual smoke check has been run more than once
- `check:harness` has become a black-box command and maintainers need clearer
  step summaries

Skip a script when:

- an existing test, lint rule, type check, or build step already gives a clear
  signal
- the check requires fragile local state that cannot be documented
- the script would only duplicate a one-off debugging command

## Script Shape

A good script should:

- use the target repository's existing runtime and package manager
- print each verification axis before running it
- redact secrets and personal data
- use stable fixtures for provider errors and zero-result cases when live calls
  are not safe
- exit with a nonzero status on real failures
- support a focused mode or separate command when the full harness gate is too
  expensive
- when output is JSON or structured text, include explicit axis fields such as
  `redactionChecked`, `emptyStateChecked`, `providerErrorChecked`, and
  `fallbackChecked`
- avoid writing files unless the script is explicitly a generator

## Transparent Harness Commands

If a target project uses `check:harness`, prefer named subcommands so the final
gate explains itself and focused checks stay cheap:

```json
{
  "scripts": {
    "check:docs": "python scripts/check_docs_drift.py",
    "check:structure": "python scripts/check_structure.py",
    "check:api": "node scripts/check-api-smoke.mjs",
    "check:harness": "npm run lint && npm run typecheck && npm run build && npm run check:docs && npm run check:structure && npm run check:api"
  }
}
```

Do not add a live API smoke command to `check:harness` unless it is stable,
safe, and expected in the target repository's normal environment. Keep it as a
separate command when credentials, network access, quota, or provider uptime
make it unsuitable as a default gate.

## Result Summary

At the end of a custom check, print a compact summary such as:

```text
Harness smoke summary:
- env: required variables present, values redacted
- transport: provider health endpoint reached
- parser: JSON and XML envelopes handled
- empty-state: zero-result fixture returns empty list
- redaction: request URL logs hide service keys
- flags: redactionChecked=true, emptyStateChecked=true, providerErrorChecked=true
```

The summary should describe what was checked, not just that the command passed.

## Documentation

When a verification script becomes part of normal work:

- document it in `AGENTS.md` or the project README
- include it in `check:harness` only if it is safe and stable by default
- add a failure record if the script protects a bug path that should not recur
- explain skipped live checks in the final report rather than pretending build
  validation covered runtime behavior

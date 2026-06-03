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
- a provider bug path was recorded in `docs/failures/*.md` and needs a
  regression test, fixture, smoke check, or documented manual review point
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
- assert provider request contracts such as required parameter names, casing,
  date/time format, coordinate fields, and redaction before making live calls
- exit with a nonzero status on real failures
- support a focused mode or separate command when the full harness gate is too
  expensive
- when output is JSON or structured text, include explicit axis fields such as
  `redactionChecked`, `emptyStateChecked`, `providerErrorChecked`, and
  `fallbackChecked`
- avoid writing files unless the script is explicitly a generator

## Gate Placement

When a new verification script or test proves product behavior, decide where it
belongs before finishing the change.

Deterministic, local, non-network, reasonably fast checks for product behavior
that agents are expected to verify repeatedly should be included in the
documented normal completion gate, or have a documented reason for remaining
focused or manual.

Keep live API, credential, quota, provider-uptime, visual, device, slow, watcher,
or hardware-dependent checks outside the normal gate unless they are stable,
safe, and expected in the target repository's normal environment.

Do not assume the normal gate is named `check:harness`. Use the target
repository's actual workflow, such as `make test`, `just check`, package
scripts, CI workflows, `scripts/check_harness.py`, or another documented local
command.

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
- include it in the documented normal completion gate only if it is safe and
  stable by default
- document focused or manual checks that remain outside the normal gate, with
  the reason
- add a failure record if the script protects a bug path that should not recur
- explain skipped live checks in the final report rather than pretending build
  validation covered runtime behavior

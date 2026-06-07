# 0004. Link Failure Memory To Regression Checks

## Status

Accepted

## Date

2026-06-03

## Context

Dogfood feedback from a public-data API target showed that the kit helped
agents record recurring failures and decisions, but could still let a failure
note become the stopping point. In the TAGO provider case, failure memory
preserved the context, but the provider boundary bug path did not automatically
produce a regression test or fixture for endpoint-specific request shape.

The same feedback showed that `/harness review` is more useful before commit or
push. When review runs after push, it can still find issues, but it is no
longer acting as a local safety gate.

## Decision

Failure memory must be linked to detection or prevention.

When a target repository adds or updates `docs/failures/*.md`, the record and
final report should name the regression test, fixture, smoke check, lint rule,
drift check, CI gate, or manual review point that prevents or detects
recurrence. If no check is practical, the record should explain why and name
the future signal that should revisit the gap.

For external API failures, prefer provider boundary fixtures or contract tests
for endpoint-specific request and response behavior. These fixtures should
cover parameter names and casing, date/time format, coordinate fields, service
key placement, success payloads, zero-result states, provider error envelopes,
provider text errors, schema drift, and redaction when those axes are relevant.

Harness Review should be run before commit or push when practical. Review
reports should record whether the review timing was pre-commit, pre-push,
post-push, or unknown.

## Rationale

- Failure records reduce investigation cost, but they do not prove recurrence
  will be caught.
- A regression check, fixture, smoke check, lint rule, drift check, CI gate, or
  manual review point turns memory into an actionable feedback path.
- External APIs often fail at provider boundary details that build and type
  checks cannot prove, such as parameter casing or mixed text/XML/JSON error
  behavior.
- Pre-push review gives maintainers a chance to catch missing checks and memory
  gaps before the change leaves the local workspace.

## Consequences

- Adoption and update reports must say which check or manual review point
  covers each new failure record.
- Failure templates include a detection or prevention check section.
- `scripts/check_failure_memory.py` validates failure-record structure and
  detection/prevention linkage locally, and the generic template ships the same
  check to target repositories.
- External API checklist guidance becomes more fixture-oriented and less
  documentation-only.
- `/harness review` reports include review timing.
- Some small fixes may need one extra final-report line when automation is not
  practical, but mechanically testable bug paths should not stop at prose.

## Known Limits And Follow-Up

- Path-existence validation confirms that cited local test, fixture, script,
  workflow, or checklist files exist, but it does not prove that the cited check
  asserts the specific failure axis.
- Package-manager script checks such as `npm run test:planner`,
  `pnpm run test:planner`, `yarn run test:planner`, and
  `bun run test:planner` are verified against the checked-in root
  `package.json` `scripts` entries. This closes the first fake-command gap for
  JavaScript package scripts and avoids passing a root command only because a
  nested workspace package has the same script, but it still does not prove that
  the script asserts the specific failure axis.
- Root `make target` and `just recipe` checks are verified against checked-in
  root Makefile variants and justfile variants. This closes the same
  fake-command gap for common task-runner commands, but it still does not parse
  included makefiles, option-heavy invocations such as `make -C app check`, or
  prove that the target asserts the specific failure axis.
- Maven, Gradle, and Go command references are verified against root project
  markers: `pom.xml` for Maven, Gradle settings/build files for Gradle, and
  `go.mod` for Go. Wrapper-shaped references such as `./mvnw verify` and
  `./gradlew check` also require the matching wrapper file at the repository
  root. This closes the fake-command gap for the current Spring, Android, and
  Go profiles, but it does not prove that a Maven goal, Gradle task, or Go
  package pattern asserts the specific failure axis.
- Other command-shaped checks are still recognized mostly by shape. The checker
  does not yet verify that Python module commands, Rust, .NET, or other
  task-runner commands exist in the target configuration.
- Monorepo and workspace-specific commands need explicit target adaptation when
  the intended command is not runnable from the repository root.
- Detection-link validation is regex-based. It blocks known non-committal
  phrases, but future wording may require additional test cases.
- Generic command coverage is still biased toward common JavaScript, Make,
  Just, Python-shaped commands, Maven, Gradle, and Go. Add explicit coverage
  before relying on this gate for Rust, .NET, or other task-runner-heavy
  targets.
- Target repositories with pre-existing non-kit `docs/failures/*.md` schemas
  may need adoption-specific adaptation instead of blindly applying the generic
  checker.

## Agent Guidance

When fixing a recurring failure, do not stop after adding `docs/failures/*.md`.
Name the check that would fail if the issue came back, add the check when
practical, or explain the concrete blocker. Run `scripts/check_failure_memory.py`
when it exists.

For external APIs, create or cite a provider boundary fixture before relying on
live smoke output. Keep live API checks outside the normal gate when
credentials, quota, network access, or provider uptime make them fragile, but
still cover stable provider parsing and request-shape behavior with local
fixtures where possible.

Run `/harness review` before commit or push for substantial harness,
integration-boundary, or external API changes when the runtime permits it.

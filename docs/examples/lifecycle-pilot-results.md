# Lifecycle Pilot Results

These pilot tests exercised prompt-first harness adoption in blank target
repositories that later gained real application stacks. They validate adoption
behavior and measurement readiness, not reduced agent error rates.

## Scope

The pilots asked a fresh agent to:

- start from a blank or near-blank target repository
- clone this kit as read-only reference material
- apply a minimal generic harness first
- introduce a small application stack only after generic adoption
- absorb the closest stack profile selectively
- save an adoption report with a filled effectiveness measurement plan
- run local verification commands
- report cleanup and remaining manual steps

## Pilot Summary

| Pilot | Stack introduced | Result | Main limitation |
| --- | --- | --- | --- |
| Blank to Django | Minimal Django app with one route and one test | Passed adoption lifecycle verification | Target was not initialized as a Git repository, so commit hygiene was only partially tested. |
| Blank to Next.js | Minimal Next.js App Router app with TypeScript | Passed adoption lifecycle, cleanup, and Git hygiene verification | App-specific check script was intentionally narrow and may be brittle if package script strings change. |

## Blank To Django Pilot

The Django pilot verified that the agent did not introduce Django during the
blank repository phase. It first added a generic harness with agent
instructions, baseline docs, drift checks, and an adoption report. Django was
introduced later with a conventional root manage script, project package, app
package, one route, and one test.

Successful behaviors:

- identified the target as blank before adoption
- kept Phase 1 generic instead of inventing a stack
- updated agent instructions after Django was introduced
- reviewed the Django profile as reference material
- recorded adopted, adapted, skipped, and deferred profile snippets
- filled the effectiveness measurement plan without placeholders
- passed docs drift, structure drift, effectiveness-plan, Django system check,
  Django test, and harness check commands

Limitations:

- the target was not a Git repository
- the local kit clone and virtual environment remained present at the end
- Git ignore behavior and commit readiness were not fully verified

## Blank To Next.js Pilot

The Next.js pilot repeated the lifecycle with stricter Git hygiene. The agent
initialized the target as a Git repository, kept Phase 1 generic, introduced a
minimal Next.js App Router app in Phase 2, then removed the local kit clone
before final verification.

Successful behaviors:

- initialized Git before adoption
- kept Phase 1 free of Next.js, React, package-manager, and CI setup
- selected npm only when the Next.js stack was introduced
- used TypeScript no-emit checks and Next.js build instead of assuming a lint
  command
- removed the local kit clone before final verification
- verified generated and dependency output stayed ignored
- filled the effectiveness measurement plan without placeholders
- passed docs drift, structure drift, effectiveness-plan, typecheck, build, app
  structure, and harness check commands

Limitations:

- the app-specific check used exact package script string comparisons, which is
  useful for the tiny pilot but may be too brittle for larger repositories
- the pilot still measured readiness, not actual reduction in repeated agent
  mistakes

## TodayBus External API Dogfood

After adding the practical verification checklists, a `today-bus` Next.js
target was used as an external API dogfood case. The target exercised TAGO and
Gumi BIS public-data paths, server-only secret handling, deterministic planner
fallbacks, and live smoke scripts. Later review separated deterministic planner
tests, which are normal-gate placement candidates, from live smoke scripts that
can remain focused because they depend on credentials, network state, quota, and
provider uptime.

Successful behaviors:

- redacted raw, encoded, and error-message samples of `TAGO_SERVICE_KEY`
- treated current TAGO arrival zero-result responses as a deliberate empty live
  state instead of a crash or mock success
- verified deterministic `tago`, `gumi_bis_timetable`, and `mock` fallback
  planner paths, then identified those checks as normal-gate placement
  candidates rather than ordinary live-smoke checks
- kept live smoke commands separate from `check:harness` because provider
  credentials, network state, and public-data availability vary
- used focused live checks such as `node scripts/check-tago-backend.mjs` and
  `node scripts/check-gumi-bis-offset.mjs`

Finding:

- Invalid TAGO credentials returned `401 text/plain Unauthorized`, not an XML
  or JSON provider error envelope. The external API checklist should call out
  provider text errors explicitly, and target smoke scripts should summarize
  redaction, empty-state, provider-error, and fallback axes directly.
- `npm run test:planner` was deterministic, local, non-network, and reasonably
  fast, but was initially grouped with focused smoke commands instead of being
  reviewed as a normal completion gate candidate. This led to
  `docs/failures/0004-deterministic-behavior-check-remained-focused-without-gate-placement-review.md`.

Limitations:

- This dogfood validated checklist usefulness for one external API target. It
  did not prove broader agent effectiveness or reduced human rework.

## Harness ERP Spring/Maven Dogfood

A `harness-erp` Spring Boot target was used as a backend dogfood case after the
Spring profile and effectiveness tracking workflow were in place. The target
exercised source tracking, local Maven verification, service-layer business
rules, decision memory, failure memory, and task outcome aggregation across
five initial comparable product tasks and four follow-up comparable product
tasks.

Successful behaviors:

- recorded `.harness/source.json` with the kit path, remote, commit, profile,
  and setup prompt reference
- used `python scripts/check_harness.py` as the normal completion gate, with
  Maven tests plus docs and structure drift checks
- preserved ERP-001 through ERP-005 task outcome records with prompt hashes,
  repository refs, first-pass verification, final verification, and changed
  file boundaries
- counted ERP-004 fixture-only edits outside the strict expected boundary as a
  wrong-file edit instead of hiding the boundary miss
- tracked ERP-006 through ERP-009 as a separate follow-up benchmark group
  instead of merging it into the initial aggregate
- recorded all four follow-up product tasks as first-pass verification
  successes with no wrong-file edits or repeated known mistakes observed
- added a non-comparable MAINT-001 CI verification record and kept it out of
  comparable product-task counts
- verified the target GitHub Actions workflow runs the local harness gate with
  Java 21 and Python
- recorded the Spring Boot `4.0.6.RELEASE` coordinate failure in the target
  failure memory and linked it to `python scripts/check_harness.py` /
  `./mvnw test`

Finding:

- The first adoption evidence pass treated a non-comparable setup fix as
  excluded from metrics but did not immediately add failure memory. Follow-up
  review corrected that evidence gap and reinforced the rule that failed setup
  checks may still need durable failure records even when excluded from
  comparable product-task counts.

Limitations:

- This dogfood is harnessed-only backend evidence split into initial and
  follow-up groups. It does not prove broader agent effectiveness or reduced
  human rework.
- Prompt hashes are preserved in task outcome records, but prompt text was local
  to the dogfood environment rather than stored in this kit.

## Starter Kit Findings

The pilots found one documentation ambiguity:

- Prompt-first adoption uses profile templates from
  `./harness-starter-kit/templates/profiles/<profile>/`.
- Installer-generated profile snippets, when used, are copied into the target
  repository under `docs/harness/profiles/<profile>/`.

The adoption workflow and profile absorption checklist should distinguish these
two paths so agents know whether they are reading the cloned kit or copied
target-repository snippets.

## Interpretation

These pilots support the following claims:

- A blank target repository can adopt the generic harness without inventing a
  stack too early.
- A later stack introduction can trigger selective profile absorption.
- Agents can fill an effectiveness measurement plan when the adoption flow and
  checker require it.
- Local checks can verify adoption reports, docs drift, structure drift, and
  stack-specific commands.

These pilots do not support claims that the harness reduces agent mistakes, CI
failure rates, or human rework. Those claims require repeated comparable tasks
recorded with the effectiveness evaluation protocol.

## Recommended Next Step

Run comparable follow-up tasks against one pilot target, such as:

- update only the home page copy
- add a second route or page
- change setup documentation without editing application source

Record wrong-file edits, first-pass harness check success, generated-file
touches, and reviewer rework in an effectiveness report.

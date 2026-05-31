# Roadmap

This roadmap describes where `harness-starter-kit` should grow after the
`v0.1.0` early release.

The project should stay prompt-first. The goal is to help maintainers turn
repository-specific agent instructions into durable rules, checks, examples,
and memory. More automation is useful only when it preserves the target
repository as the source of truth.

## Guiding Priorities

- Improve adoption quality before adding broad automatic mutation behavior.
- Prefer real examples, fixtures, and checks over untested profile snippets.
- Keep the optional installer conservative and non-destructive by default.
- Make repeated agent failures easier to record, detect, and avoid.
- Measure outcomes carefully instead of claiming that harness adoption reduces
  mistakes without evidence.

## Recommended Order

This is the preferred order for near-term work. It is a sequencing guide, not a
promise that every item belongs in the next release.

1. Strengthen adoption evidence before adding larger features.
2. Improve governance commands, especially review and maintenance workflows.
3. Use review findings to shape policy-driven enforcement.
4. Add optional runtime or CI adapters only after the portable checks and
   policy workflow are clear.
5. Grow stack profiles only when they have fixtures, smoke coverage, and a
   clear local verification path.

## Adoption Evidence

The project needs more examples that show how prompt-first harness adoption
behaves in real repositories.

Useful examples include:

- a TypeScript or Node.js service adoption
- a Next.js app adoption
- a FastAPI adoption with completed effectiveness tracking
- a monorepo adoption note
- a GitLab CI adoption note
- a second dogfood repository beyond the Django reference target
- a real `docs/failures/` record from dogfood adoption, update, or refresh work

Each example should document what was adopted, adapted, skipped, and verified.
Add practical effectiveness measurement examples using the existing report
template.

## Governance Commands

Future command work should make the harness easier to maintain without turning
the starter kit into an automatic rewrite system.

- Improve Harness Doctor evidence messages and scoring calibration.
- Refine `/harness update` and `/harness refresh` workflows from real target
  repository use.
- Refine the `/harness review` command for critical review of the current turn's
  changes from an opposing harness-engineering perspective.

The review command should use a separate reviewer perspective or subagent when
the environment supports it. Its job is not to continue implementation, but to
challenge whether the current changes preserve the target repository as the
source of truth, avoid unnecessary automation, keep templates conservative,
add enforceable checks only where practical, update durable memory when needed,
and run the right validation before completion.

The review should be diagnostic by default. It should report findings,
questions, missing checks, overreach, and follow-up recommendations without
modifying files unless the user explicitly asks to apply fixes after seeing the
review.

Also keep localized README consistency and language-switcher presentation tidy
as documentation maintenance work.

## Policy-Driven Enforcement

Future work: add an optional policy proposal workflow for target repositories
that want stronger enforcement without making starter-kit defaults more
opinionated.

Users should not be expected to hand-write a policy file. Instead, the agent
should inspect the target repository, identify existing checks, CI wiring,
generated paths, protected local files, package manager behavior, and team
conventions, then produce a Markdown policy proposal for maintainer review.

The default behavior should remain observe-only. Stronger enforcement, such as
pre-commit hooks, CI failures, or agent runtime hooks, should be opt-in,
target-specific, and generated only after the maintainer approves the proposed
policy.

Policy work should follow adoption evidence and review-command experience. The
review workflow should help identify which rules are worth proposing for
stronger enforcement.

## Optional Runtime And CI Adapters

Runtime and CI adapters should remain optional, reference-only integrations.
They are useful only after a target repository has chosen its own enforcement
policy.

Possible adapters include pre-commit hooks, GitHub Actions wiring, GitLab CI
notes, and agent runtime hook examples. Adapters should call portable harness
checks instead of owning separate policy logic, and they must not become part of
default adoption.

## Profile Growth

New stack profiles are welcome when they are backed by evidence.

A new profile should include:

- profile guidance under `templates/profiles/<profile>/`
- a minimal fixture under `tests/fixtures/<profile>-basic/`
- smoke coverage in `tests/test_smoke_fixtures.py`
- installer coverage in `tests/test_apply_harness.py` when new file types are
  introduced
- documentation updates for the profile list and validation coverage
- conservative guidance that can be adapted instead of copied blindly

Candidate profiles include Rails, Laravel, Go, and Rust. Add them only when the
profile has a real fixture and a clear local verification path.

## Not Currently Prioritized

- Turning the kit into a one-command framework migration tool.
- Making the installer overwrite or deeply rewrite target repositories.
- Adding profiles without fixtures and smoke tests.
- Claiming effectiveness from fixture tests alone.
- Replacing target repository conventions with starter-kit defaults.

## Related Decisions

- `docs/decisions/0001-prompt-first-adoption.md`

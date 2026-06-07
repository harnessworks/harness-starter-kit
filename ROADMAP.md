# Roadmap

This roadmap describes where `harness-starter-kit` should grow after the
current early releases.

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
2. Exercise the new task-outcome evidence decision gate on real substantial
   harness work before adding a separate evidence command.
3. Improve governance commands, especially review and maintenance workflows.
4. Use review findings to shape policy-driven enforcement.
5. Add optional runtime or CI adapters only after the portable checks and
   policy workflow are clear.
6. Grow stack profiles only when they have fixtures, smoke coverage, and a
   clear local verification path.

## Adoption Evidence

The project needs more examples that show how prompt-first harness adoption
behaves in real repositories. Recent work has added Django and Next.js dogfood
targets, lifecycle pilot notes, concrete failure-memory records, and practical
external API verification guidance. Future examples should broaden that
evidence instead of repeating the same target shapes.

Useful examples include:

- a TypeScript or Node.js service adoption
- a FastAPI adoption with completed effectiveness tracking
- a monorepo adoption note
- a GitLab CI adoption note
- a comparative effectiveness report using repeated task outcomes across more
  than one target repository

Each example should document what was adopted, adapted, skipped, and verified.
Add practical effectiveness measurement examples using the existing report
template.

The next evidence pass should use the task-outcome decision gate from
`docs/decisions/0006-trigger-task-outcome-evidence-for-substantial-harness-work.md`.
Record or explicitly skip task outcome evidence for substantial harness work,
then review whether the trigger list produces useful records without becoming
paperwork. Useful pilot tasks include a profile update, a checker update, a
governance-command refinement, and a dogfood adoption or update. Keep
harness-maintenance records out of comparable product-task counts unless they
are true product-task runs.

## Operational Evidence Loop

The first step of the operational evidence loop is now in place: substantial
harness work must decide whether task outcome evidence should be recorded, and
included task outcome records are checked for comparable evidence fields.

The pilot now has three harness-maintenance task outcome records:
`004-evidence-decision-gate.yaml` and
`005-make-just-command-validation.yaml`, and
`006-maven-gradle-go-command-validation.yaml`. These are useful evidence that
the loop can capture substantial checker and policy work, but they are still
harness-maintenance observations, not product-task effectiveness proof.

The remaining work is to prove that the loop is useful in practice before
turning it into another command or a heavier reporting system.

Near-term milestones:

1. Continue applying the evidence decision gate until at least 3-5 substantial
   harness changes have records or explicit skip reasons. The next useful
   pilots should be a profile update, governance-command refinement, and
   dogfood adoption or update rather than another checker-only change.
2. For each substantial change, record a task outcome or state a skip reason in
   the final report. Keep trivial docs-only, typo, link-label, and formatting
   work out of task outcome records.
3. When a recorded task outcome shows a miss, convert it into the smallest
   durable harness improvement: an instruction update, check, gate-placement
   change, decision record, failure record, or refresh candidate.
4. After several records exist, write a maintenance evidence report that
   summarizes recorded outcomes, skipped outcomes, first-pass verification,
   wrong-file edits, drift detections, human rework, and which observations
   changed the harness.
5. Only after that report exists, decide whether `/harness evidence` or a
   dedicated evidence checklist is worth adding.

Report templates should be adjusted only after the pilot shows the field shape
is stable. The likely minimal addition is a `Task Outcome Evidence` field that
records `recorded in <path>` or `skipped because <reason>` without requiring
YAML for every task.

## Practical Verification Patterns

Recent adoption feedback says the kit is useful as a completion safety belt but
less useful during hard implementation work. Near-term improvements should add
more reusable, execution-oriented patterns without turning the kit into a
framework-specific fixer.

Recent additions cover external API checklists, provider-boundary fixture
guidance, Next.js App Router notes, failure-memory verification, decision-memory
warnings, deterministic behavior gate placement, trigger-based task outcome
evidence, root `make`/`just` command-reference validation, and root
Maven/Gradle/Go project-marker validation. Useful next additions include:

- command existence validation beyond package scripts, root `make` targets,
  root `just` recipes, and root Maven/Gradle/Go project markers for Rust, .NET,
  Python module commands, or other profile-relevant task runners referenced by
  failure-memory or effectiveness records
- more fixture-backed examples for provider-specific request shape, response
  envelopes, redaction, zero-result behavior, and provider errors
- clearer ADR and failure-record boundary examples for small changes so
  maintainers do not create unnecessary documentation pressure
- verification-script examples that summarize checked axes and explain focused
  or manual gate placement
- examples where a target-specific smoke script catches a real backend, API, or
  cross-environment bug that lint, typecheck, and build could not prove

## Governance Commands

Future command work should make the harness easier to maintain without turning
the starter kit into an automatic rewrite system.

- Improve Harness Doctor evidence messages and scoring calibration.
- Refine `/harness update`, `/harness refresh`, and `/harness review` workflows
  from real target repository use.
- Improve diagnostics for durable-memory gaps, gate placement, and review timing
  without making the commands mutate files by default.
- Document and refine the fix-and-re-review loop for `/harness review` and
  `/harness review sub-agent` after more target diffs show that the loop reaches
  no actionable findings.

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

Do not add a new `/harness evidence` command yet. First collect several
substantial-work task outcomes and at least one aggregate maintenance evidence
report so the command can be shaped by observed records rather than assumed
workflow needs.

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

iOS is also a useful candidate profile to pair with the existing Android
profile. Because Xcode and simulator checks require macOS, its fixture smoke
coverage should validate profile installation and portable drift checks, while
`xcodebuild`, simulator, signing, CocoaPods, Swift Package Manager, and device
verification guidance should be documented as macOS/manual unless the target
repository already has macOS CI.

## Not Currently Prioritized

- Turning the kit into a one-command framework migration tool.
- Making the installer overwrite or deeply rewrite target repositories.
- Adding profiles without fixtures and smoke tests.
- Claiming effectiveness from fixture tests alone.
- Replacing target repository conventions with starter-kit defaults.

## Related Decisions

- `docs/decisions/0001-prompt-first-adoption.md`
- `docs/decisions/0002-configurable-decision-memory-warning.md`
- `docs/decisions/0003-review-gate-placement-for-deterministic-behavior-checks.md`
- `docs/decisions/0004-link-failure-memory-to-regression-checks.md`
- `docs/decisions/0005-validate-dogfood-evidence-consistency.md`
- `docs/decisions/0006-trigger-task-outcome-evidence-for-substantial-harness-work.md`

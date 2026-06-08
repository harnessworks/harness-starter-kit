# Changelog

Notable project changes should be recorded here before release tags are cut.

## Unreleased

### Added

- Rust profile guidance, fixture coverage, smoke-test wiring, installer
  coverage, and README/profile documentation so Rust crate and Cargo workspace
  targets have a conservative local verification path.

## v0.1.10 - 2026-06-08

Patch release for Harness Doctor v2. This release turns Doctor from a flat
baseline scan into a six-element repository health and coupling diagnostic
while preserving the boundary between harness readiness and agent
effectiveness.

### Added

- Harness Doctor v2 scoring across Instructions, Constraints, Feedback, Memory,
  Evaluation, and Governance.
- First-class coupling findings for orphan constraints, orphan feedback,
  unoperationalized memory, unevaluated memory, ungoverned change types, and
  promotion gaps.
- Optional Doctor gates for minimum score and critical coupling findings,
  disabled by default.
- Decision memory for the Doctor v2 model and task outcome evidence for the
  implementation and review loop.

### Changed

- Update `/harness doctor`, the scoring rubric, example reports, component map,
  theory docs, and roadmap guidance to describe the six-element diagnostic.
- Keep Proven/effectiveness signals unmeasured in Doctor output unless durable
  outcome evidence supports a claim.
- Tighten feedback-binding heuristics so generic documentation mentions do not
  count as execution wiring, and unbound check scripts do not inflate Feedback
  health.
- Expand Doctor regression tests for coupling findings, optional gates,
  non-comparable outcome evidence, illustrative effectiveness reports, and
  feedback-binding edge cases.

## v0.1.9 - 2026-06-06

Patch release for operational evidence tracking, Go profile coverage, and
command-reference validation. This release strengthens the kit's ability to
collect trustworthy agent-work evidence without turning the starter kit into a
heavier automation framework.

### Added

- Go profile guidance, fixture coverage, smoke-test wiring, and README/profile
  documentation so Go targets have a conservative local verification path.
- Task outcome evidence decision guidance for substantial harness work,
  including required evidence fields for included task outcome records.
- Dogfood and effectiveness evidence reports for Today Bus, Harness ERP, and
  small evidence-pass scenarios, plus task outcome examples for harness
  adoption and maintenance work.
- Failure records and decision memory for dogfood evidence consistency and
  first-pass task outcome evidence gaps.
- Google site verification, sitemap, robots, and static-site metadata updates.

### Changed

- Extend `scripts/check_effectiveness_plan.py`, plus the generic template copy,
  to validate task outcome evidence fields and reject contradictory or stale
  effectiveness-report completion language.
- Extend `scripts/check_failure_memory.py` and
  `scripts/check_effectiveness_plan.py`, plus generic template copies, to
  validate root `make` targets and root `just` recipes referenced by
  failure-memory records, adoption reports, and task outcome verification
  commands.
- Strengthen dogfood evidence validation, effectiveness templates, adoption
  evidence checklists, roadmap guidance, and evaluation docs around operational
  evidence loops.
- Refresh README, localized README files, contributor visuals, profile lists,
  validation docs, and lifecycle pilot notes to match the current evidence and
  profile coverage.
- Revert the Crowdin localization sync path while preserving localized README
  consistency.

## v0.1.8 - 2026-06-03

Patch release for failure-memory verification hardening and expanded dogfood
context. This release turns failure notes and adoption-report failure memory
from prose guidance into concrete, path-aware checks while preserving
prompt-first adoption.

### Added

- `scripts/check_failure_memory.py`, plus generic template and CI wiring, to
  validate `docs/failures/*.md` sections and require concrete detection or
  prevention checks, or a practical no-check rationale.
- Failure-memory fields in adoption reports, report templates, PR templates,
  and review guidance that tie recorded failures to regression tests, fixtures,
  smoke checks, lint rules, drift checks, CI gates, or manual review points.
- Regression coverage for failure-memory section validation, concrete check
  detection, package-script validation, missing path detection, and generic
  template wiring.
- Today Bus as a Next.js dogfood target in the README badge list and dogfood
  target notes.

### Changed

- Extend `scripts/check_effectiveness_plan.py` to validate failure-memory
  linkage in adoption reports, including referenced failure records, local
  paths, and package scripts.
- Update failure-note templates and existing failure records to name concrete
  detection or prevention checks.
- Expand adoption, review, update, validation, and checklist docs around
  failure-memory verification and package-script checks.
- Include `scripts/check_failure_memory.py` in documented validation commands
  and generic harness CI.

## v0.1.7 - 2026-06-02

Patch release for deterministic behavior gate placement. This release adds
durable guidance and checks so adoption reports explain which deterministic
checks belong in normal completion gates and which remain focused or manual.

### Added

- Decision memory for placing deterministic behavior checks in normal,
  focused, or manual verification gates.
- Failure memory for deterministic behavior checks that stayed focused without
  explicit gate-placement review.
- Verification gate-placement fields in adoption reports, harness review report
  templates, example reports, and profile adoption reports.
- Regression coverage for gate-placement reporting, prompt drift, and repository
  hygiene.

### Changed

- Extend `scripts/check_effectiveness_plan.py`, plus the generic template copy,
  to require `## Verification Gate Placement` fields in adoption reports.
- Expand adoption workflow, `/harness review`, `/harness refresh`,
  verification-script checklist, and adoption prompt guidance for gate
  placement.
- Update localized README files and the static site Quick Start wording to
  mention gate placement alongside failure memory and effectiveness tracking.

## v0.1.6 - 2026-06-02

Patch release for practical verification guidance and decision-memory
automation. This release keeps the kit prompt-first while adding a configurable
warning gate for implementation diffs that may need ADR review.

### Added

- `scripts/check_decision_memory.py`, plus generic template wiring, to warn when
  watched implementation paths change without a matching `docs/decisions/`
  update.
- `.harness/decision-memory-rules.json` in the kit and generic template so
  repositories can tune watched implementation paths, decision paths, and
  ignored paths.
- GitHub Actions wiring for decision-memory review checks, using the pull
  request base SHA in PRs and a local smoke check for non-PR runs.
- Practical checklists for external API work, decision/failure memory
  boundaries, and verification script patterns.
- Regression coverage for the decision-memory warning script, installer output,
  generic template wiring, CI wiring, and profile guidance.

### Changed

- Expand adoption workflow and adoption report guidance for external API
  verification, redaction, live/mock mode, empty-result behavior, provider
  errors, and focused smoke checks.
- Clarify `/harness update` handling for dirty target worktrees by separating
  source tracking from target file mutation.
- Strengthen `/harness review`, generic `AGENTS.md`, and UI profile guidance
  around input semantics, state normalization, fallback policy, and displayed
  decision criteria.
- Make the Next.js profile's `check:harness` example more transparent with
  named docs and structure subcommands, and add App Router verification notes.

## v0.1.5 - 2026-06-02

Patch release for the decision-memory follow-up to `v0.1.4`. This release moves
the decision-docs gate from review-only guidance into the generic target
template that future adoptions copy.

### Added

- Decision-memory guidance in the generic `AGENTS.md` template for non-trivial
  product or workflow structure, integration or mock external-behavior
  boundaries, major data models, state classifications, or UX principles that
  become code structure.
- A completion criterion requiring agents to report whether decision docs were
  added, an existing ADR covers the choice, or no decision record was needed.
- A `Decision-docs gate` field in the harness review report template so the
  specific `/harness review` diagnostic does not get lost when reviewers use
  the template.
- Regression coverage that keeps the generic completion gate and review report
  gate wired in.

## v0.1.4 - 2026-06-02

Patch release for governance documentation and review diagnostics. This release
keeps `/harness review` diagnostic-only while tightening the durable-memory
review path and clarifying command usage.

### Added

- Failure memory for missed ADR review when structural product decisions are
  implemented without decision-record consideration.
- A `/harness review` diagnostic warning for product or workflow structure,
  mock external-behavior boundaries, major data models, state classifications,
  or product UX principles that become code structure without a
  `docs/decisions/` update or explicit justification.
- iOS as a roadmap candidate profile paired with the existing Android profile,
  with Xcode, simulator, signing, and device checks documented as macOS/manual
  unless a target repository already has macOS CI.

### Changed

- Clarify that `/harness ...` names are prompt conventions by default, not
  built-in editor commands.
- Refine `/harness review sub-agent` ownership guidance so reviewer mode and
  fallback reason stay parent/orchestrator-owned.
- Update localized README command guidance to match the English prompt
  convention wording.

## v0.1.3 - 2026-05-31

Patch release for `/harness review` reviewer-mode routing. This release keeps
the command diagnostic-only while making subagent availability and fallback
reporting harder to skip silently.

### Added

- Explicit `/harness review sub-agent` invocation mode that treats the request
  as permission to call a read-only reviewer subagent when the active runtime
  and tool instructions allow it.
- Review report `Invocation`, `Reviewer mode`, and `Fallback reason` fields in
  the template and example report.
- Regression coverage for subagent fallback guidance, prompt drift, localized
  README wiring, and route precedence between `/harness review sub-agent` and
  `/harness review`.

### Changed

- Clarify `/harness review` fallback behavior when a subagent tool is present
  but not permitted by active tool instructions.
- Route the more specific `/harness review sub-agent` command before the
  generic `/harness review` command in agent-facing prompts and command
  routing.

## v0.1.2 - 2026-05-31

Governance release for change-set review. This release adds a diagnostic
`/harness review` workflow so maintainers can challenge current changes before
completion without adding runtime hooks, policy enforcement, CI adapters, or
more automatic installer behavior.

### Added

- `/harness review` command workflow for opposing harness-engineering review of
  the current change set.
- Harness review report template and example report.
- Quick Start, full adoption prompt, localized README, static site, and
  component-map wiring for `/harness review`.
- Regression tests that keep `/harness review` command routing, localized docs,
  report-template sections, and prompt drift covered.

### Changed

- Clarify that the existing harness review checklist is a periodic maintenance
  checklist, distinct from the `/harness review` change-set command.
- Update the roadmap from adding `/harness review` to refining it through real
  target-repository use.

## v0.1.1 - 2026-05-30

Stabilization release for the initial harness workflow. This release strengthens
the theory, evaluation, failure-memory, and contributor guidance added around
the `v0.1.0` early release.

### Added

- Harness engineering theory document that separates repository harness health
  from observed agent effectiveness.
- Task outcome record template for comparable agent-work observations.
- Roadmap and expanded contributor guidance for profiles, drift checks,
  adoption examples, and release validation.
- Regression coverage that keeps the static site copy prompt aligned with the
  README adoption prompt.

### Changed

- Compact root and generic `AGENTS.md` guidance while preserving command
  routing, analysis, validation, and commit rules.
- Clarify `python3` validation commands for macOS/Linux environments where
  `python` is unavailable.
- Clarify Harness Doctor score scope and non-scored evaluation/governance
  signals.
- Strengthen adoption and update guidance around failure-memory records for
  user-visible runtime failures, high-risk bug paths, failed checks, repeated
  agent mistakes, and cross-environment mismatches.

## v0.1.0 - 2026-05-29

Initial early release of `harness-starter-kit`.

This release is for maintainers who want to make repositories safer for AI
coding agents through durable instructions, project memory, feedback loops, and
drift checks. The kit is prompt-first by design; the installer is a conservative
bootstrap helper, not a full automatic migration tool.

### Added

- Prompt-first adoption workflow for applying the kit from a target repository.
- Generic harness templates for `AGENTS.md`, knowledge storage, and drift
  checks.
- Stack profile snippets for Python, TypeScript, Node.js, Next.js, React, Vue,
  Django, Flask, FastAPI, Spring Boot, and Android.
- `/harness doctor`, `/harness update`, and `/harness refresh` command
  workflows.
- Drift checks for documentation references, structure hygiene, encoding
  hygiene, and effectiveness measurement plans.
- Harness Doctor baseline scoring across agent instructions, feedback loops,
  durable memory, structural safety, and adoption clarity.
- Fixture smoke tests and an opt-in FastAPI profile E2E test.
- Adoption report and effectiveness report templates.
- Lifecycle pilot notes, launch essay link, and Django dogfood repository link.

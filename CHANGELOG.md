# Changelog

Notable project changes should be recorded here before release tags are cut.

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

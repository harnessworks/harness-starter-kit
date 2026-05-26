# Profile Absorption Checklist

Use this checklist when a repository that started with the generic harness later
introduces a real stack, framework, build tool, UI layer, API layer, or test
runner.

Profiles are reference material. Absorption means deciding which profile
snippets should become real project rules, scripts, ignores, docs, or checks.

## When To Run This

Run this checklist when:

- a previously empty or generic repository gets its first app implementation
- a new framework is introduced, such as Vue, React, FastAPI, Django, Flask,
  Spring, or Next.js
- a new package manager, build command, lint tool, type checker, or test runner
  appears
- recurring implementation patterns become clear enough to document

## 1. Pick The Closest Profile

- [ ] Identify the closest profile under `docs/harness/profiles/<profile>/` or
      `harness-starter-kit/templates/profiles/<profile>/`.
- [ ] If no profile fits, use `generic` and document the missing profile need in
      the adoption report or `docs/decisions/`.
- [ ] Treat the target repository's existing tools as source of truth.

## 2. Review Profile Snippets

For each available snippet, decide whether to adopt, adapt, skip, or defer it.

- [ ] `README.md`: read the profile notes and stack-specific cautions.
- [ ] `package-scripts.harness.json`: merge only compatible scripts into
      `package.json`.
- [ ] `pyproject.harness.toml`, `eslint.config.harness.mjs`, or similar config:
      merge relevant rules into existing config instead of replacing it.
- [ ] `gitignore.harness.txt`: merge generated directories, local caches, and
      reference clone ignores into the target `.gitignore`.
- [ ] `check_harness.py`: copy or adapt into `scripts/` only when the target has
      no equivalent local verification command.

## 3. Update Durable Docs

- [ ] Update `AGENTS.md` with the new stack, commands, directory rules, and
      completion criteria.
- [ ] Update `docs/conventions/coding.md` with stack-specific conventions that
      agents should repeat.
- [ ] Add or update `docs/decisions/*.md` when the new stack, tool, state
      approach, routing model, or project structure is an architectural choice.
- [ ] Add `docs/failures/*.md` only when an attempted approach failed and should
      not be repeated.
- [ ] Update the project README when setup, usage, or user-facing commands
      changed.

## 4. Add Feedback Loops

- [ ] Run the target stack's tests, type checks, lint checks, and build checks.
- [ ] Run `scripts/check_docs_drift.py`.
- [ ] Run `scripts/check_structure.py`.
- [ ] Run `scripts/check_effectiveness_plan.py` if adoption or effectiveness
      reports are stored in the repository.
- [ ] If a profile check script was copied or adapted, run it directly.
- [ ] Wire stable checks into CI or the existing local task runner when it fits
      the target repository.

## 5. Report The Absorption

In the final report, list:

- [ ] profile reviewed
- [ ] snippets adopted
- [ ] snippets adapted
- [ ] snippets skipped and why
- [ ] docs updated
- [ ] checks run
- [ ] remaining manual steps

## Vue/Vite Example

When a generic repository later becomes a Vue/Vite app:

- Review the Vue profile.
- Merge useful package scripts into `package.json`.
- Merge `.vite/`, `dist/`, `node_modules/`, local env files, and
  `harness-starter-kit/` into `.gitignore` if they are not already ignored.
- Decide whether Vue ESLint rules should be merged into the existing ESLint
  config.
- Copy or adapt the profile `check_harness.py` only if no equivalent local check
  command exists.
- Update `AGENTS.md` with Vue/Vite commands.
- Update `docs/conventions/coding.md` with component, state, routing, styling,
  and testing conventions.
- Add an ADR if choosing Vue/Vite or a state management approach is a meaningful
  architectural decision.

<p align="center">
  <img alt="harness-starter-kit agent session demo" src="site/assets/banner.gif" />
</p>

<p align="center">
  <img alt="Generic profile" src="https://img.shields.io/badge/profile-generic-6b7280?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white" />
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-087EA4?style=flat-square&logo=react&logoColor=white" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" />
  <img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="Spring Boot" src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" />
  <img alt="Android" src="https://img.shields.io/badge/Android-3DDC84?style=flat-square&logo=android&logoColor=white" />
</p>

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

<p align="center">
  <a href="https://baskduf.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
</p>

## Quick Start

Open the target repository with your coding agent and give it this prompt:

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit if it is not already present, read it,
then apply its prompt-first harness engineering workflow to this repository.

Requirements:
- Treat the current working directory as the target repository.
- Treat ./harness-starter-kit as read-only reference material after cloning.
- Inspect this repository before editing.
- Preserve existing architecture, tools, package manager, commands, docs, and
  conventions.
- Do not blindly copy templates.
- Add only the minimum useful harness pieces.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite or delete existing files without explaining why.
- If I ask for /harness doctor, use
  ./harness-starter-kit/commands/harness-doctor.md.
- If I ask for /harness update after adoption, use
  ./harness-starter-kit/commands/harness-update.md to refresh the kit reference,
  record .harness/source.json, and selectively update target harness files
  without blindly overwriting existing files.
- If I ask for /harness refresh after adoption, use
  ./harness-starter-kit/commands/harness-refresh.md to review existing harness
  docs, rules, knowledge records, and checks for stale or duplicated guidance.
  Do not delete, archive, move, or rename files without my explicit approval for
  the specific files.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit
```

For the full prompt and workflow details, see
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
and [`docs/adoption-workflow.md`](docs/adoption-workflow.md).

## Commands

### `/harness doctor`

Run Harness Doctor to evaluate how ready a repository is for reliable AI coding
agent collaboration. It reports a Harness Score across Agent Instructions,
Feedback Loops, Durable Memory, Structural Safety, and Adoption Clarity.

- Command workflow: [`commands/harness-doctor.md`](commands/harness-doctor.md)
- Rubric: [`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)
- Example report: [`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)

For an objective baseline scan:

```powershell
python scripts/harness_doctor.py --target .
```

### `/harness update`

After a repository has adopted the harness, use `/harness update` to refresh the
local `./harness-starter-kit` reference clone and selectively apply new harness
guidance.

Harness Update records the confirmed kit source in `.harness/source.json`,
classifies update opportunities, and finishes with a Harness Update Report. It
must not blindly overwrite target repository files.

- Command workflow: [`commands/harness-update.md`](commands/harness-update.md)

### `/harness refresh`

After a repository has adopted the harness, use `/harness refresh` to review the
existing target harness for stale docs, duplicated guidance, obsolete records,
or unused checks.

Harness Refresh classifies findings as keep, update, merge,
archive/delete candidate, or manual review. It does not refresh the local kit
reference and must not delete files without explicit approval.

- Command workflow: [`commands/harness-refresh.md`](commands/harness-refresh.md)

## How Adoption Works

This is not primarily an automatic installer. The agent should inspect the
target repository first, then adapt the smallest useful set of harness
artifacts:

- `AGENTS.md` for durable agent instructions
- architecture constraints through linting, type checks, import boundaries, or
  project-specific rules
- feedback loops through tests, CI, pre-commit hooks, and clear failure messages
- a knowledge store under `docs/` for decisions, failures, conventions, and
  domain context
- garbage-collection checks that detect code, document, and structure drift

Use the optional installer only when you want a skeleton before agent-driven
adaptation:

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

The optional installer never overwrites existing files unless `--force` is
provided. It copies stack profile snippets into `docs/harness/profiles/<profile>`
for review. During prompt-first adoption, agents read profile templates from the
cloned kit under `harness-starter-kit/templates/profiles/<profile>`.

## Profiles

Available profiles are `generic`, `python`, `typescript`, `nextjs`, `django`,
`flask`, `fastapi`, `spring`, `android`, `react`, and `vue`.

Profiles are conservative reference material, not automatic transformations.
Adopt only the snippets that fit the target repository's current tools and
maintenance expectations. For profile absorption after a stack is introduced,
use [`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md).

## Documentation Map

- Overview: [`docs/overview.md`](docs/overview.md)
- Adoption workflow: [`docs/adoption-workflow.md`](docs/adoption-workflow.md)
- Harness refresh workflow: [`commands/harness-refresh.md`](commands/harness-refresh.md)
- Full adoption prompt: [`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
- Component map: [`docs/component-map.md`](docs/component-map.md)
- Validation coverage: [`docs/validation.md`](docs/validation.md)
- Effectiveness evaluation: [`docs/evaluation.md`](docs/evaluation.md)
- Lifecycle pilot details: [`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)

## Validation And Measurement

Automated fixture tests cover installation and runnable drift checks across
Node.js, Next.js, Django, FastAPI, Flask, React, Spring Boot, Android, Vue,
Python, and TypeScript-oriented profiles. See
[`docs/validation.md`](docs/validation.md) for coverage details and opt-in E2E
checks.

A live dogfooding target is
[baskduf/harness_starter_kit_django](https://github.com/baskduf/harness_starter_kit_django),
a small Django project used to test prompt-first adoption, `/harness update`,
failure memory, and effectiveness tracking in a real repository.

They do not prove that harness adoption reduces repeated agent mistakes. Use
[`docs/evaluation.md`](docs/evaluation.md) and
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)
to measure comparable tasks, wrong-file edits, first-pass verification, and
human rework.

## Local Checks

Run these checks before changing starter-kit templates, command workflows,
installer behavior, or drift scripts:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/harness_doctor.py --target .
```

## License

This project is licensed under the [MIT License](LICENSE).

## Core Principle

Every recurring agent failure should be converted into at least one durable
artifact: a clearer instruction, an automated constraint, a test or CI check, a
decision or failure record, or a drift check.

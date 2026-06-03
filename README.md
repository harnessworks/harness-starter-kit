<p align="center">
  <img width="2172" height="724" alt="06d3c515-5fd8-4942-95e0-50ae2a2c5456" src="https://github.com/user-attachments/assets/4ba0bcf8-7500-49bd-a0fd-b8666807df39" />
<img width="1672" height="941" alt="ChatGPT Image 2026년 5월 31일 오후 03_58_36" src="https://github.com/user-attachments/assets/e9edcba6-4cf1-43e5-8fbb-6d4d6426d0c3" />

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
  <a href="https://dev.to/baskduf/i-stopped-prompt-engineering-my-ai-coding-agent-i-started-engineering-the-repo-instead-1i3e">
    <img alt="Read the launch essay" src="https://img.shields.io/badge/Read-Launch_Essay-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" />
  </a>
  <a href="https://github.com/baskduf/harness_starter_kit_django/tree/main">
    <img alt="View Django dogfood repo" src="https://img.shields.io/badge/View-Django_Dogfood-092E20?style=for-the-badge&logo=django&logoColor=white" />
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
- If I ask for /harness review sub-agent, use
  ./harness-starter-kit/commands/harness-review.md and treat the request as
  explicit permission to use a read-only reviewer subagent when available and
  permitted by the active runtime and tool instructions. If unavailable,
  blocked, not permitted, or failed, report the fallback reason.
- If I ask for /harness review, use
  ./harness-starter-kit/commands/harness-review.md to review the current change
  set from an opposing harness-engineering perspective. Report findings,
  missing checks, overreach, durable memory gaps, and follow-up recommendations
  without modifying files unless I explicitly ask you to apply fixes after the
  review.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, normal/focused/manual gate placement, and whether
  ./harness-starter-kit should be removed, ignored, or kept before commit
```

For the full prompt and workflow details, see
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
and [`docs/adoption-workflow.md`](docs/adoption-workflow.md).

<p align="center">
<img width="939" height="783" alt="제목 없는 디자인" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />

> 💫 If this kit helps you, a GitHub star would be appreciated. 💫
</p>


## Harness Theory

Harness engineering treats the repository as the durable operating environment
for coding agents:

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

Harness health is different from agent effectiveness. Harness Doctor can scan
for durable repository evidence, but it cannot prove that agents make fewer
mistakes. Measure that separately with task outcomes and effectiveness reports.
See [`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)
for the model.

## Commands

The `/harness ...` names below are prompt conventions by default, not built-in
editor commands. Type or paste them into your coding agent chat. In editors such
as Cursor, they will not appear in the command palette unless you separately add
matching custom slash commands.

### `/harness doctor`

Run Harness Doctor to evaluate baseline repository evidence for reliable AI
coding agent collaboration. It reports a five-category Harness Score across
Agent Instructions, Feedback Loops, Durable Memory, Structural Safety, and
Adoption Clarity; agent effectiveness and governance maturity remain non-scored
manual review items.

- Command workflow: [`commands/harness-doctor.md`](commands/harness-doctor.md)
- Rubric: [`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)
- Example report: [`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)

For an objective baseline scan, use `python3` instead of `python` on
macOS/Linux when `python` is unavailable:

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

### `/harness review`

Use `/harness review` to challenge the current change set from an opposing
harness-engineering perspective before finishing.

Harness Review is diagnostic by default. It checks for target source-of-truth
violations, unnecessary automation, weak validation, missing durable memory,
overreach, and stale or duplicated guidance. It must not modify files unless the
user explicitly asks to apply fixes after seeing the review.

Use `/harness review sub-agent` when you want to explicitly request a read-only
reviewer subagent. It still falls back to single-agent review and reports why if
the active runtime cannot call one.

- Command workflow: [`commands/harness-review.md`](commands/harness-review.md)
- Report template: [`docs/templates/harness-review-report.md`](docs/templates/harness-review-report.md)
- Example report: [`docs/examples/harness-review-report.md`](docs/examples/harness-review-report.md)

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
- Theory: [`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)
- Roadmap: [`ROADMAP.md`](ROADMAP.md)
- Adoption workflow: [`docs/adoption-workflow.md`](docs/adoption-workflow.md)
- External API work checklist: [`docs/checklists/external-api-work.md`](docs/checklists/external-api-work.md)
- Decision and failure memory checklist: [`docs/checklists/decision-failure-memory.md`](docs/checklists/decision-failure-memory.md)
- Verification script patterns: [`docs/checklists/verification-scripts.md`](docs/checklists/verification-scripts.md)
- Harness refresh workflow: [`commands/harness-refresh.md`](commands/harness-refresh.md)
- Harness review workflow: [`commands/harness-review.md`](commands/harness-review.md)
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
or [`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml) to
measure comparable tasks, wrong-file edits, first-pass verification, and human
rework.

## Local Checks

Run these checks before changing starter-kit templates, command workflows,
installer behavior, or drift scripts. Use `python3` instead of `python` on
macOS/Linux when `python` is unavailable:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/check_failure_memory.py scripts/check_decision_memory.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/check_failure_memory.py
python scripts/check_decision_memory.py
python scripts/harness_doctor.py --target .
```

## License

This project is licensed under the [MIT License](LICENSE).

## Core Principle

Every recurring agent failure should be converted into at least one durable
artifact: a clearer instruction, an automated constraint, a test or CI check, a
decision or failure record, or a drift check.

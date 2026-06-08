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
  <img alt="Go" src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" />
  <img alt="Rust" src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white" />
  <img alt="Contributors" src="https://img.shields.io/github/contributors/baskduf/harness-starter-kit?style=flat-square" />
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
  <a href="https://github.com/baskduf/today-bus">
    <img alt="View Next.js dogfood repo" src="https://img.shields.io/badge/View-Next.js_Dogfood-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
  </a>
  <a href="https://github.com/baskduf/harness-erp">
    <img alt="View Spring Boot dogfood repo" src="https://img.shields.io/badge/View-Spring_Boot_Dogfood-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" />
  </a>
</p>

A prompt-first starter kit for turning repeated coding-agent mistakes into
durable repository instructions, checks, memory, and evaluation.

## Quick Start

Open the target repository with your coding agent and give it this prompt.

<details>
<summary>Show full adoption prompt</summary>

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
  manual steps, failure memory, effectiveness measurement plan,
  normal/focused/manual gate placement, and whether
  ./harness-starter-kit should be removed, ignored, or kept before commit
```

</details>

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

Every recurring agent failure should be converted into at least one durable
artifact: a clearer instruction, an automated constraint, a test or CI check, a
decision or failure record, or a drift check.

## Commands

The `/harness ...` names below are prompt conventions by default, not built-in
editor commands. Type or paste them into your coding agent chat. In editors such
as Cursor, they will not appear in the command palette unless you separately add
matching custom slash commands.

| Command | Use when |
| --- | --- |
| `/harness doctor` | Score baseline harness evidence without modifying files. |
| `/harness update` | Refresh the local `./harness-starter-kit` reference after adoption. |
| `/harness refresh` | Review stale, duplicated, obsolete, or unused target harness guidance. |
| `/harness review` | Challenge the current change set before finishing. |
| `/harness review sub-agent` | Explicitly request a read-only reviewer subagent when the runtime permits it. |

See [`commands/`](commands/) for full workflows:
[`doctor`](commands/harness-doctor.md),
[`update`](commands/harness-update.md),
[`refresh`](commands/harness-refresh.md),
and [`review`](commands/harness-review.md).

## How Adoption Works

<details>
<summary>Show adoption details</summary>

This is not primarily an automatic installer. The agent should inspect the
target repository first, then adapt the smallest useful set of harness
artifacts: instructions, enforceable constraints, feedback loops, durable
memory, drift checks, and an adoption report. Follow
[`docs/adoption-workflow.md`](docs/adoption-workflow.md) and the prompt in
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md).

Use the optional installer only when you want a skeleton before agent-driven
adaptation. It copies profile snippets into
`docs/harness/profiles/<profile>` for review; prompt-first adoption reads
profiles from the cloned kit at
`harness-starter-kit/templates/profiles/<profile>`.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

Profiles shown in the badges above are conservative reference snippets, not
automatic migrations. See [`docs/profiles.md`](docs/profiles.md) and
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md).

For the detailed documentation index, see
[`docs/component-map.md`](docs/component-map.md). Common adoption references:
[`docs/checklists/external-api-work.md`](docs/checklists/external-api-work.md),
[`docs/checklists/decision-failure-memory.md`](docs/checklists/decision-failure-memory.md),
and [`docs/checklists/verification-scripts.md`](docs/checklists/verification-scripts.md).

Validation coverage and local checks live in
[`docs/validation.md`](docs/validation.md). Lifecycle pilot details live in
[`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md).
They do not prove that harness adoption reduces repeated agent mistakes. Use
[`docs/evaluation.md`](docs/evaluation.md),
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md),
and [`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml) to
measure comparable tasks, wrong-file edits, first-pass verification, and human
rework.

Dogfood reports include
[`TodayBus`](docs/examples/effectiveness-report-todaybus-dogfood.md) for a
Next.js public-data target and
[`Harness ERP`](docs/examples/effectiveness-report-harness-erp-dogfood.md) for
a Spring/Maven backend and vanilla frontend target. Both are harnessed-only
benchmarks, not proof of effectiveness improvement.

</details>

## Contributors

Thanks to everyone who has helped shape this kit through code, docs, reviews,
examples, translations, and dogfooding.

<a href="https://github.com/baskduf/harness-starter-kit/graphs/contributors">
  <img src="https://readme-contribs.as93.net/contributors/baskduf/harness-starter-kit?v=20260604" alt="Contributors" />
</a>

## License

This project is licensed under the [MIT License](LICENSE).

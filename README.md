<img width="2172" height="724" alt="Harness Starter Kit logo banner" src="https://github.com/user-attachments/assets/c303dffe-402d-44f4-8d11-3c28936f3a3e" />

<img width="1536" height="1024" alt="Harness engineering workflow diagram" src="https://github.com/user-attachments/assets/13dbc277-ec47-4c0b-87ca-d31a88e83f4f" />


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
  <img alt="Contributors" src="https://img.shields.io/github/contributors/harnessworks/harness-starter-kit?style=flat-square" />
</p>

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

<p align="center">
  <a href="https://harnessworks.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
  <a href="https://dev.to/baskduf/i-stopped-prompt-engineering-my-ai-coding-agent-i-started-engineering-the-repo-instead-1i3e">
    <img alt="Read the launch essay" src="https://img.shields.io/badge/Read-Launch_Essay-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/harness-agent-benchmark-runner">
    <img alt="View benchmark runner" src="https://img.shields.io/badge/Benchmark-Harness_Runner-2F855A?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>


# Harness Starter Kit

A prompt-first starter kit for turning repeated coding-agent mistakes into
durable repository instructions, checks, memory, and evaluation.

## Product Effects

Harness Starter Kit does not position repository harnessing as raw coding
performance tuning. Its product effect is operational: make agent work safer to
run, easier to diagnose, and easier to improve from repository evidence.

- **Isolate agent work safely.** Run agent tasks inside clear repository
  boundaries so hidden or sensitive files, generated outputs, credentials, and
  forbidden paths stay out of normal task flow.
- **Turn failures into diagnosis.** Separate functional, schema, workflow,
  boundary, timeout, and hidden-access failures instead of reducing an agent
  result to one pass/fail label.
- **Transfer repository conventions.** Preserve local API style, documentation
  placement, validation commands, and review expectations in durable repo
  guidance that agents can follow repeatedly.
- **Create an improvement loop.** Convert observed mistakes into instructions,
  checks, failure records, decision memory, benchmark tasks, or review points
  so the next agent run has better operating context.

## Quick Start

Open the target repository with your coding agent and give it this prompt.

<details>
<summary>Show full adoption prompt</summary>

```text
Use this kit to apply harness engineering to this repository:

https://github.com/harnessworks/harness-starter-kit

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
  <img width="360" alt="GitHub star support illustration for Harness Starter Kit" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />
</p>

<p align="center">
  <em>💫 If this kit helps you, a GitHub star would be appreciated. 💫</em>
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

## Command Flow

The `/harness ...` names below are prompt conventions by default, not built-in
editor commands. Type or paste them into your coding agent chat. In editors such
as Cursor, they will not appear in the command palette unless you separately add
matching custom slash commands.

Think about the commands by user stage:

| Stage | Command | Use when |
| --- | --- | --- |
| First time | `/harness doctor` | Inspect current harness readiness without modifying files. |
| First time | `/harness adopt` | Apply the smallest useful harness pieces to this repository. |
| Daily work | `/harness review` | Challenge the current diff before commit or PR. |
| Daily work | `/harness review sub-agent` | Explicitly request a read-only reviewer subagent when the runtime permits it. |
| Maintenance | `/harness update` | Bring in a newer `harness-starter-kit` reference and selectively update this repo. |
| Maintenance | `/harness refresh` | Clean up stale, duplicated, obsolete, or unused harness guidance already in this repo. |

Quick rule:

- Use `doctor` to inspect.
- Use `adopt` to start.
- Use `review` before finishing work.
- Use `update` when the kit version changes.
- Use `refresh` when this repo's existing harness guidance gets stale.

See [`commands/`](commands/) for full workflows:
[`adopt`](commands/harness-adopt.md),
[`doctor`](commands/harness-doctor.md),
[`update`](commands/harness-update.md),
[`refresh`](commands/harness-refresh.md),
and [`review`](commands/harness-review.md).

## Install Agent Skills

Harness workflows are prompt-first by default, but the same workflows are also
published as runtime-native skills for Codex and Claude Code.

### Codex

```bash
codex plugin marketplace add harnessworks/harness-agent-skills-marketplace --ref v0.1.15
```

Restart Codex, open the Plugins screen, select `Harnessworks`, and install
`harness-agent-skills`.

Use the same command model in every runtime:

```text
Start:      $harness doctor → $harness adopt
Daily:      $harness review
Maintain:   $harness update or $harness refresh
```

Common commands:

```text
$harness doctor
$harness adopt
$harness review
```

Maintenance commands:

```text
$harness update
$harness refresh
```

### Claude Code

```bash
claude plugin marketplace add harnessworks/harness-agent-skills-marketplace@v0.1.15
claude plugin install harness-agent-skills@harnessworks
```

Use the router command:

```text
Start:      /harness-agent-skills:harness doctor → /harness-agent-skills:harness adopt
Daily:      /harness-agent-skills:harness review
Maintain:   /harness-agent-skills:harness update or /harness-agent-skills:harness refresh
```

Common commands:

```text
/harness-agent-skills:harness doctor
/harness-agent-skills:harness adopt
/harness-agent-skills:harness review
```

Maintenance commands:

```text
/harness-agent-skills:harness update
/harness-agent-skills:harness refresh
```

The source package lives in [`agent-skills/`](agent-skills/). For direct
repo-local installs, packaging details, and update behavior, see
[`docs/agent-skills-package.md`](docs/agent-skills-package.md).

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

<a href="https://github.com/harnessworks/harness-starter-kit/graphs/contributors">
  <img src="https://readme-contribs.as93.net/contributors/harnessworks/harness-starter-kit?v=20260608-yunhwane" alt="Contributors" />
</a>

## Recognition

Listed in:

- [Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents) as an AI agent tooling project.
- [github/awesome-copilot](https://github.com/github/awesome-copilot) as a Copilot customization resource.

## License

This project is licensed under the [MIT License](LICENSE).

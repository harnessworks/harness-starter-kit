<img width="2172" height="724" alt="Harness Starter Kit 标志横幅" src="https://github.com/user-attachments/assets/c303dffe-402d-44f4-8d11-3c28936f3a3e" />

<img width="1536" height="1024" alt="Harness engineering 工作流图" src="https://github.com/user-attachments/assets/13dbc277-ec47-4c0b-87ca-d31a88e83f4f" />


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

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

<p align="center">
  <a href="https://harnessworks.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
  <a href="https://dev.to/baskduf/i-stopped-prompt-engineering-my-ai-coding-agent-i-started-engineering-the-repo-instead-1i3e">
    <img alt="Read the launch essay" src="https://img.shields.io/badge/Read-Launch_Essay-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/harness_starter_kit_django/tree/main">
    <img alt="View Django dogfood repo" src="https://img.shields.io/badge/View-Django_Dogfood-092E20?style=for-the-badge&logo=django&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/today-bus">
    <img alt="View Next.js dogfood repo" src="https://img.shields.io/badge/View-Next.js_Dogfood-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/harness-erp">
    <img alt="View Spring Boot dogfood repo" src="https://img.shields.io/badge/View-Spring_Boot_Dogfood-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" />
  </a>
</p>

# Harness Starter Kit

一个 prompt-first starter kit，用于把反复出现的 coding-agent mistakes 转化为
durable repository instructions、checks、memory 和 evaluation。

## 快速开始

用代码代理打开目标仓库，然后发送下面的 prompt。

<details>
<summary>显示完整采用提示</summary>

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

完整 prompt 和 workflow 见
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
以及 [`docs/adoption-workflow.md`](docs/adoption-workflow.md)。

<p align="center">
  <img width="360" alt="Harness Starter Kit GitHub star 支持插图" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />
</p>

<p align="center">
  <em>💫 If this kit helps you, a GitHub star would be appreciated. 💫</em>
</p>


## Harness 理论

Harness engineering 把仓库视为 coding agent 的 durable operating environment。

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

Harness health 不同于 agent effectiveness。Harness Doctor 可以扫描 durable
repository evidence，但不能证明 agent 会减少 mistakes。请用 task outcomes 和
effectiveness reports 单独测量。模型见
[`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)。

每一个 repeated agent failure 都应转化为至少一个 durable artifact：更清晰的
instruction、automated constraint、test 或 CI check、decision/failure record，
或 drift check。

## 命令

下面的 `/harness ...` 名称默认是 prompt convention，不是内置 editor command。
请把它们输入或粘贴到 coding agent chat 中。在 Cursor 等 editor 里，除非另外添加
对应的 custom slash command，否则它们不会出现在 command palette 中。

| Command | Use when |
| --- | --- |
| `/harness doctor` | 在不修改文件的情况下评分 baseline harness evidence。 |
| `/harness update` | adoption 后刷新本地 `./harness-starter-kit` reference。 |
| `/harness refresh` | 检查 stale、duplicated、obsolete 或 unused target harness guidance。 |
| `/harness review` | 完成前批判性检查当前 change set。 |
| `/harness review sub-agent` | runtime 允许时明确请求 read-only reviewer subagent。 |

完整 workflow 见 [`commands/`](commands/):
[`doctor`](commands/harness-doctor.md),
[`update`](commands/harness-update.md),
[`refresh`](commands/harness-refresh.md),
[`review`](commands/harness-review.md).

## 采用方式

<details>
<summary>显示采用细节</summary>

这个 kit 主要不是自动 installer。代理应先检查目标仓库，然后只应用最小但有用的
harness artifacts: instructions, enforceable constraints, feedback loops,
durable memory, drift checks, and an adoption report。请遵循
[`docs/adoption-workflow.md`](docs/adoption-workflow.md) 和
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)。

optional installer 只适合在 agent-driven adaptation 前需要 skeleton 时使用。它会
把 profile snippets 复制到 `docs/harness/profiles/<profile>` 供审阅；
prompt-first adoption 会读取 cloned kit 中的
`harness-starter-kit/templates/profiles/<profile>`。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

上方 badges 中的 profiles 是保守的 reference snippets，不是 automatic
migrations。请参阅 [`docs/profiles.md`](docs/profiles.md) 和
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md)。

详细 documentation index 见 [`docs/component-map.md`](docs/component-map.md)。常用
adoption references:
[`docs/checklists/external-api-work.md`](docs/checklists/external-api-work.md),
[`docs/checklists/decision-failure-memory.md`](docs/checklists/decision-failure-memory.md),
[`docs/checklists/verification-scripts.md`](docs/checklists/verification-scripts.md).

Validation coverage 和 local checks 位于
[`docs/validation.md`](docs/validation.md)。Lifecycle pilot details 见
[`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)。
这些内容不能证明 harness adoption 会减少 repeated agent mistakes。要测量
comparable tasks、wrong-file edits、first-pass verification 和 human rework，请使用
[`docs/evaluation.md`](docs/evaluation.md),
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md),
[`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml)。

Dogfood reports 包括 Next.js public-data target
[`TodayBus`](docs/examples/effectiveness-report-todaybus-dogfood.md)，以及
Spring/Maven backend 和 vanilla frontend target
[`Harness ERP`](docs/examples/effectiveness-report-harness-erp-dogfood.md)。两者都只是
harnessed-only benchmarks，并不能证明 effectiveness improvement。

</details>

## 贡献者

感谢所有通过 code、docs、reviews、examples、translations 和 dogfooding 帮助完善
这个 kit 的人。

<a href="https://github.com/harnessworks/harness-starter-kit/graphs/contributors">
  <img src="https://readme-contribs.as93.net/contributors/harnessworks/harness-starter-kit?v=20260608-yunhwane" alt="Contributors" />
</a>

## 许可证

本项目使用 [MIT License](LICENSE)。

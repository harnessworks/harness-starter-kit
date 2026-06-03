# harness-starter-kit

**[English](README.md)** | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

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
</p>

详细操作文档以英文维护。本 README 作为快速入口。

## 快速开始

用代码代理打开目标仓库，然后发送下面的 prompt。

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

完整 prompt 和 workflow 见
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
以及 [`docs/adoption-workflow.md`](docs/adoption-workflow.md)。

<p align="center">
<img width="939" height="783" alt="제목 없는 디자인" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />

> 💫 If this kit helps you, a GitHub star would be appreciated. 💫
</p>


## 命令

下面的 `/harness ...` 名称默认是 prompt convention，不是内置 editor
command。请把它们输入或粘贴到 coding agent chat 中。在 Cursor 等 editor 里，
除非另外添加对应的 custom slash command，否则它们不会出现在 command palette
中。

### `/harness doctor`

Harness Doctor 用于评估仓库与 AI coding agent 稳定协作所需的 baseline
evidence。它会从 Agent Instructions、Feedback Loops、Durable Memory、
Structural Safety、Adoption Clarity 生成 5-category Harness Score；agent
effectiveness 和 governance maturity 属于 non-scored manual review。

- Command workflow: [`commands/harness-doctor.md`](commands/harness-doctor.md)
- Rubric: [`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)
- Example report: [`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)

客观 baseline scan。macOS/Linux 上如果没有 `python`，请使用 `python3`。

```powershell
python scripts/harness_doctor.py --target .
```

### `/harness update`

仓库完成 harness adoption 后，可以使用 `/harness update` 更新本地
`./harness-starter-kit` reference clone，并只选择性应用适合当前仓库的新
harness guidance。

Harness Update 会把确认过的 kit source 记录到 `.harness/source.json`，分类更新
候选项，并以 Harness Update Report 结束。它不能无条件覆盖 target repository
文件。

- Command workflow: [`commands/harness-update.md`](commands/harness-update.md)

### `/harness refresh`

仓库完成 harness adoption 后，可以使用 `/harness refresh` 检查现有 target
harness 中的 stale docs、duplicated guidance、obsolete records 或 unused
checks。

Harness Refresh 会把 findings 分类为 keep、update、merge、archive/delete
candidate 或 manual review。它不会更新本地 kit reference，也不能在没有明确批准
时删除文件。

- Command workflow: [`commands/harness-refresh.md`](commands/harness-refresh.md)

### `/harness review`

`/harness review` 用于在完成前，从 opposing harness-engineering perspective
检查当前 change set。

Harness Review 默认是 diagnostic。它检查 target source-of-truth violations、
unnecessary automation、weak validation、missing durable memory、overreach，以及
stale or duplicated guidance。除非用户在 review 后明确要求应用修复，否则不能修改
文件。

`/harness review sub-agent` 用于明确请求 read-only reviewer subagent。若
active runtime 无法调用，则 fallback 到 single-agent review，并报告原因。

- Command workflow: [`commands/harness-review.md`](commands/harness-review.md)
- Report template: [`docs/templates/harness-review-report.md`](docs/templates/harness-review-report.md)
- Example report: [`docs/examples/harness-review-report.md`](docs/examples/harness-review-report.md)

## 采用方式

这个 kit 主要不是自动 installer。代理应先检查目标仓库，然后只应用最小但有用的
harness artifacts。

- `AGENTS.md`: durable agent instructions
- 通过 lint、type checks、import boundaries 或 project rules 建立 architecture constraints
- 通过 tests、CI、pre-commit hooks 和清晰失败信息建立 feedback loops
- 在 `docs/` 下存储 decisions、failures、conventions、domain context
- 用 garbage-collection checks 检测 code、document、structure drift

optional installer 只适合在 agent-driven adaptation 前需要 skeleton 时使用。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

optional installer 在没有 `--force` 时不会覆盖已有文件。Profile snippets 会复制到
`docs/harness/profiles/<profile>` 供审阅。Prompt-first adoption 时，代理读取
cloned kit 中的 `harness-starter-kit/templates/profiles/<profile>`。

## Profiles

可用 profile 包括 `generic`, `python`, `typescript`, `nextjs`, `django`,
`flask`, `fastapi`, `spring`, `android`, `react`, `vue`。

Profile 是保守参考资料，不是自动转换规则。只采用符合目标仓库当前工具和维护预期
的 snippet。若之后引入 stack，请使用
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md)。

## 文档地图

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

## 验证与测量

自动 fixture tests 覆盖 Node.js、Next.js、Django、FastAPI、Flask、React、
Spring Boot、Android、Vue、Python、TypeScript 相关 profile 的安装行为和
runnable drift checks。Coverage details 和 opt-in E2E checks 见
[`docs/validation.md`](docs/validation.md)。

实际 dogfooding targets 包括
[baskduf/harness_starter_kit_django](https://github.com/baskduf/harness_starter_kit_django)
和 [baskduf/today-bus](https://github.com/baskduf/today-bus)。Django target
用于验证 prompt-first adoption、`/harness update`、failure memory 和
effectiveness tracking；Next.js target 用于在真实仓库中验证 external API work、
deterministic behavior checks 和 dogfood review gates。

这些 tests 并不能证明 harness adoption 会减少 repeated agent mistakes。要测量
comparable tasks、wrong-file edits、first-pass verification 和 human rework，请使用
[`docs/evaluation.md`](docs/evaluation.md) 与
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)。
个别手动 task outcome record 请使用
[`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml)。

## 本地检查

修改 starter-kit templates、command workflows、installer behavior 或 drift scripts
之前，运行以下 checks。macOS/Linux 上如果没有 `python`，请使用 `python3`。

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

## 许可证

本项目使用 [MIT License](LICENSE)。

## 核心原则

每一个 repeated agent failure 都应转化为至少一个 durable artifact：更清晰的
instruction、automated constraint、test 或 CI check、decision/failure record，
或 drift check。

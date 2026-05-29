# harness-starter-kit

**[English](README.md)** | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

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

<p align="center">
  <a href="https://baskduf.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
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

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit
```

完整 prompt 和 workflow 见
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
以及 [`docs/adoption-workflow.md`](docs/adoption-workflow.md)。

## 命令

### `/harness doctor`

Harness Doctor 用于评估仓库是否已准备好与 AI coding agent 稳定协作。它会从
Agent Instructions、Feedback Loops、Durable Memory、Structural Safety、
Adoption Clarity 生成 Harness Score。

- Command workflow: [`commands/harness-doctor.md`](commands/harness-doctor.md)
- Rubric: [`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)
- Example report: [`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)

客观 baseline scan:

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
- Adoption workflow: [`docs/adoption-workflow.md`](docs/adoption-workflow.md)
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

实际 dogfooding target 是
[baskduf/harness_starter_kit_django](https://github.com/baskduf/harness_starter_kit_django)。
这个小型 Django project 用于在真实仓库中验证 prompt-first adoption、
`/harness update`、failure memory 和 effectiveness tracking。

这些 tests 并不能证明 harness adoption 会减少 repeated agent mistakes。要测量
comparable tasks、wrong-file edits、first-pass verification 和 human rework，请使用
[`docs/evaluation.md`](docs/evaluation.md) 与
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)。

## 本地检查

修改 starter-kit templates、command workflows、installer behavior 或 drift scripts
之前，运行以下 checks。

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/harness_doctor.py --target .
```

## 许可证

本项目使用 [MIT License](LICENSE)。

## 核心原则

每一个 repeated agent failure 都应转化为至少一个 durable artifact：更清晰的
instruction、automated constraint、test 或 CI check、decision/failure record，
或 drift check。

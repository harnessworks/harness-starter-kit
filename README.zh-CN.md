<pre align="center">
 _   _    _    ____  _   _ _____ ____ ____
| | | |  / \  |  _ \| \ | | ____/ ___/ ___|
| |_| | / _ \ | |_) |  \| |  _| \___ \___ \
|  _  |/ ___ \|  _ <| |\  | |___ ___) |__) |
|_| |_/_/   \_\_| \_\_| \_|_____|____/____/

 ____ _____  _    ____ _____ _____ ____    _  _____ _____
/ ___|_   _|/ \  |  _ \_   _| ____|  _ \  | |/ /_ _|_   _|
\___ \ | | / _ \ | |_) || | |  _| | |_) | | ' / | |  | |
 ___) || |/ ___ \|  _ < | | | |___|  _ <  | . \ | |  | |
|____/ |_/_/   \_\_| \_\|_| |_____|_| \_\ |_|\_\___| |_|
</pre>

# harness-starter-kit

<p align="center">
  <img alt="Generic profile" src="https://img.shields.io/badge/profile-generic-6b7280?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img alt="Spring Boot" src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" />
</p>

<p align="center">
  <img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=111111" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" />
</p>

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

`harness-starter-kit` 是一个 prompt-first 入门套件，用于把 harness
engineering 应用到任意软件项目。它的预期用法是把 Git URL 交给代理，让代理在
目标仓库中 clone、读取，并根据目标仓库真实的工具和约束进行适配。

预期工作流很简单：用代码代理打开目标仓库，把套件 URL 和提示词交给代理，让
代理 clone、read、adapt。

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit, read it, then apply its prompt-first
harness engineering workflow to the current project.

Rules:
- Treat the current working directory as the target repository.
- Treat ./harness-starter-kit as read-only reference material after cloning.
- Inspect this repository before editing.
- Preserve existing architecture, tools, package manager, commands, docs, and
  conventions.
- Do not blindly copy templates.
- Add only the minimum useful harness pieces.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite or delete existing files without explaining why.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit
```

目标项目最终应该拥有一套实用的代理 harness：

- 用于持久化代理指令的 `AGENTS.md`
- 通过 lint、type check、import boundary 或项目专属规则建立的架构约束
- 通过 test、CI、pre-commit hook 和清晰失败信息形成的反馈回路
- 位于 `docs/` 下的知识库，用于保存 decision、failure、convention 和 domain context
- 用于检测 code、document 和 structure drift 的 garbage-collection check

## 为什么需要它

提示词是临时的。上下文只存在于会话中。harness 属于项目。

好的 harness engineering 会把重复性的指令从聊天中移到仓库里，让代理在稳定的
规则内工作。当代理犯错时，长期修复方式不只是修正当次输出。更好的做法是添加
规则、测试、文档或自动化检查，让同样的错误下次更不容易发生。

## 快速开始

在目标仓库中打开你的代码代理。把 Git URL 交给代理，并要求它 clone 到
`./harness-starter-kit`、读取套件，然后应用 workflow：

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit, read it, then apply its prompt-first
harness engineering workflow to the current project.
```

如果代理无法访问 GitHub，请先在目标仓库中手动 clone 本套件，然后要求代理读取
`./harness-starter-kit` 并应用同一个 workflow。

### 可选: Skeleton Bootstrap

`apply_harness.py` 是 skeleton bootstrapper，不是 full harness adoption
engine。如果你想手动运行它，请先预览将要生成的文件：

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

除非提供 `--force`，否则脚本不会覆盖已有文件。
默认安装只会添加本地 harness 文件。只有在确认目标仓库也需要可选的 GitHub
Actions harness workflow 时，才使用 `--with-ci`。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## Harness Doctor

运行 Harness Doctor 可以评估一个仓库是否已经准备好与 AI 代码代理可靠协作。

```text
/harness doctor
```

Harness Doctor 会从五个方面为仓库评分：

- Agent Instructions
- Feedback Loops
- Durable Memory
- Structural Safety
- Adoption Clarity

目标不是把文档游戏化。目标是找出代码代理容易重复犯错的薄弱点。

一句话概括：`harness-starter-kit` 帮助你诊断并改进仓库对 AI 代码代理的准备程度。

代理命令位于
[`commands/harness-doctor.md`](commands/harness-doctor.md)。评分规则位于
[`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)，
示例报告位于
[`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)。

如需客观的 baseline scan，可以运行：

```powershell
python scripts/harness_doctor.py --target .
```

示例输出：

```text
Harness Doctor Report

Score: 72/100
Grade: B

Verdict:
Useful but incomplete. This repository has durable agent instructions and some
validation loops, but it still lacks durable failure memory and CI-level
structural enforcement.

Breakdown:
- Agent Instructions: 18/20
- Feedback Loops: 14/20
- Durable Memory: 10/20
- Structural Safety: 16/20
- Adoption Clarity: 14/20
```

## 由代理驱动的采用流程

在新项目或已有项目中，把下面的提示交给你的代码代理：

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit if it is not already present, read it,
then apply its prompt-first harness engineering workflow to this repository.

Requirements:
- Inspect the target repository before editing.
- Identify the language, framework, package manager, test command, lint command,
  build command, CI provider, docs structure, and monorepo layout if present.
- Read existing AGENTS.md, CLAUDE.md, README, CONTRIBUTING, and CI configs if
  they exist.
- Preserve existing architecture, tools, and conventions.
- Add or update AGENTS.md with project-specific rules.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if they
  are missing and no equivalent knowledge store exists.
- Add lightweight drift checks under scripts/ only when they reflect real target
  repo rules, then wire stable checks into the closest existing verification
  path.
- Prefer existing linters, tests, CI, and package managers over introducing new
  ones.
- Do not overwrite existing files without explaining why.
- Finish with a short report listing files changed, checks added, assumptions,
  remaining manual integration steps, and what to do with ./harness-starter-kit
  before committing.
```

更长版本位于
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)。

## 仓库结构

```text
harness-starter-kit/
|-- AGENTS.md
|-- commands/
|-- docs/
|   |-- adoption-workflow.md
|   |-- component-map.md
|   |-- overview.md
|   |-- checklists/
|   |-- examples/
|   |-- scoring/
|   `-- prompts/
|-- scripts/
|   `-- apply_harness.py
|-- tests/
`-- templates/
    |-- generic/
    `-- profiles/
```

## 采用模式

`generic` 适用于任何项目。它会提供持久化 harness skeleton，不假设具体语言或
框架。

当目标项目使用 Python 时，选择 `python`。它会添加面向 Ruff、mypy、vulture 和
pre-commit 的 Python 参考片段。

当目标项目使用 JavaScript 或 TypeScript 时，选择 `typescript`。它会添加面向
ESLint、dependency boundary、unused export check 和 package script 的参考片段。

当目标项目是 Next.js 应用时，选择 `nextjs`。它会添加面向 `next build`、不产生
输出的 TypeScript check、generated file ignore 和当前 Next.js lint 注意事项的
参考片段。

当目标项目是 Django 应用时，选择 `django`。它会添加面向 `manage.py check`、
`manage.py test`、virtual environment ignore、SQLite 开发数据库 ignore 和
Python `check_harness.py` entrypoint 的参考片段。

当目标项目是 Flask 应用时，选择 `flask`。它会添加面向 `unittest` discovery、
Flask route check、instance-data ignore 和 Python `check_harness.py`
entrypoint 的参考片段。

当目标项目是 Spring Boot 应用时，选择 `spring`。它会添加面向 Maven 或 Gradle
wrapper check、Spring test command、generated build output ignore、local config
ignore 和 Python `check_harness.py` entrypoint 的参考片段。

当目标项目是 FastAPI 应用时，选择 `fastapi`。它会添加面向 pytest、mypy、
app import/startup check、generated file ignore 和 Python `check_harness.py`
entrypoint 的参考片段。

当目标项目是 React 应用时，选择 `react`。它会添加面向 ESLint、TypeScript check、
test/build script 和 React-specific lint rule 的参考片段。

当目标项目是 Vue 应用时，选择 `vue`。它会添加面向 ESLint、`vue-tsc`、
test/build script 和 Vue-specific lint rule 的参考片段。

这些 profile 有意保持保守，是参考材料，而不是自动项目转换。installer 会把
profile 文件复制到 `docs/harness/profiles/<profile>/` 下，方便代理或 maintainer
在保留目标项目现有构建系统的同时，只 merge、adapt 或 ignore 合适的片段。

## 安装和 Drift Check 覆盖范围

自动 fixture smoke test 覆盖以下 stack 的 harness installation：

- Node.js / TypeScript
- Next.js
- Django
- FastAPI
- Flask
- React
- Spring Boot
- Vue

这些 fixture test 会验证 installer 能保留现有文件、写入预期的 profile snippet，
并生成可运行的 generic drift check。

额外的 end-to-end adoption check 已手动运行在：

- 使用 `node --test`、重复 installer 运行、TypeScript profile `check_harness.py`
  和故意制造的 drift failure 的 Node.js ES module 项目
- 使用 pytest、mypy、generated drift check 和 FastAPI profile `check_harness.py`
  的 FastAPI 项目

FastAPI E2E coverage 会创建 virtual environment 并安装 dependency，因此作为
opt-in 自动测试提供。

```powershell
$env:RUN_FASTAPI_E2E = "1"
python -m unittest tests.test_fastapi_profile_e2e
```

在 GitHub Actions 中，手动运行 `Harness Check` workflow 并启用
`run_fastapi_e2e`，即可执行同一个 dependency-installing test。

## 效果测量

上面的自动测试验证安装行为和可运行的 drift check。它们不能证明 harness
adoption 减少了重复出现的 agent mistake。效果应使用
[`docs/evaluation.md`](docs/evaluation.md) 中的协议单独测量。

adoption 时，请填写
[`docs/templates/adoption-report.md`](docs/templates/adoption-report.md) 中的
Effectiveness Measurement Plan。如果没有 baseline，请记录 harnessed-only
tracking，并定义后续可比较任务、primary metric、review window 和 results
location。实际的 before/after 或后续观测结果应记录在
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)。

## 本地检查

修改 starter kit 模板、安装脚本或 drift script 后，请运行这些检查：

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_effectiveness_plan.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_effectiveness_plan.py
python scripts/harness_doctor.py --target .
```

## 许可证

本项目基于 [MIT License](LICENSE) 发布。

## 核心原则

每一次重复出现的代理失败，都应该被转化为至少一个 durable artifact：

- `AGENTS.md` 中更清晰的指令
- 自动化约束
- test 或 CI check
- decision 或 failure record
- drift check

这就是 harness engineering 的核心。

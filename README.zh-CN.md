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

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

`harness-starter-kit` 是一个用于把 harness engineering 应用到任意软件项目的
入门套件。

预期工作流很简单：

```text
Clone harness-starter-kit into a target project.
Ask an agent: "Read ./harness-starter-kit and apply its harness engineering guidelines
to this repo. Preserve the existing architecture and add only the minimum
missing harness files."
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

把本仓库克隆或下载到目标项目内部：

```text
workspace/
`-- target-repo/
    |-- harness-starter-kit/
    `-- existing-project-files
```

然后在目标仓库中打开你的代码代理，并给它这个提示词：

```text
Read ./harness-starter-kit first, then apply the harness engineering starter kit
to this repository.

Treat the current working directory as the target repository. Treat
./harness-starter-kit as read-only reference material unless I explicitly ask
you to edit the kit itself.

Preserve this repository's existing architecture, tools, package manager,
commands, and conventions. Add only the minimum missing harness files. Prefer
updating existing docs/configs over duplicating them. Do not overwrite or delete
existing files without explaining why.

Finish with a short adoption report listing files changed, checks I can run,
assumptions made, and remaining manual steps.
```

如果你想手动运行安装脚本，请先预览将要生成的文件：

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

除非提供 `--force`，否则脚本不会覆盖已有文件。
默认安装只会添加本地 harness 文件。只有在确认目标仓库也需要可选的 GitHub
Actions harness workflow 时，才使用 `--with-ci`。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## 由代理驱动的采用流程

在新项目或已有项目中，把下面的提示交给你的代码代理：

```text
Read ./harness-starter-kit first. Apply the harness engineering starter kit to this
repository.

Requirements:
- Preserve existing architecture, tools, and conventions.
- Add or update AGENTS.md with project-specific rules.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if they
  are missing.
- Add drift checks under scripts/ and wire them into the closest existing
  verification path.
- Prefer existing linters, tests, CI, and package managers over introducing new
  ones.
- Do not overwrite existing files without explaining why.
- Finish with a short report listing files changed, checks added, and remaining
  manual integration steps.
```

更长版本位于
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)。

## 仓库结构

```text
harness-starter-kit/
|-- AGENTS.md
|-- docs/
|   |-- adoption-workflow.md
|   |-- component-map.md
|   |-- overview.md
|   |-- checklists/
|   `-- prompts/
|-- scripts/
|   `-- apply_harness.py
|-- tests/
`-- templates/
    |-- generic/
    `-- profiles/
```

## 采用模式

`generic` 适用于任何项目。它会安装持久化 harness skeleton，不假设具体语言或
框架。

当目标项目使用 Python 时，选择 `python`。它会添加面向 Ruff、mypy、vulture 和
pre-commit 的 Python 参考片段。

当目标项目使用 JavaScript 或 TypeScript 时，选择 `typescript`。它会添加面向
ESLint、dependency boundary、unused export check 和 package script 的参考片段。

这些 profile 有意保持保守。它们提供片段和指南，而不是重写现有构建系统。

## 本地检查

修改 starter kit 模板、安装脚本或 drift script 后，请运行这些检查：

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
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

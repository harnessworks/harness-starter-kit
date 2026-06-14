<img width="2172" height="724" alt="Harness Starter Kit 標誌橫幅" src="https://github.com/user-attachments/assets/c303dffe-402d-44f4-8d11-3c28936f3a3e" />

<img width="1536" height="1024" alt="Harness engineering 工作流程圖" src="https://github.com/user-attachments/assets/13dbc277-ec47-4c0b-87ca-d31a88e83f4f" />


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

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | **繁體中文**

<p align="center">
  <a href="https://harnessworks.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
  <a href="https://dev.to/baskduf/i-stopped-prompt-engineering-my-ai-coding-agent-i-started-engineering-the-repo-instead-1i3e">
    <img alt="Read the launch essay" src="https://img.shields.io/badge/Read-Launch_Essay-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/harness-agent-benchmark-runner">
    <img alt="查看 benchmark runner" src="https://img.shields.io/badge/Benchmark-Harness_Runner-2F855A?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

# Harness Starter Kit

一套 prompt-first starter kit，協助你把 coding agent 反覆出現的錯誤，整理成能
長期留在儲存庫中的 instructions、checks、memory 與 evaluation。

## 快速開始

用你的 coding agent 開啟目標儲存庫，並給它下面這段 prompt。

<details>
<summary>顯示完整導入 prompt</summary>

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

完整 prompt 與工作流程請見
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
與 [`docs/adoption-workflow.md`](docs/adoption-workflow.md)。

<p align="center">
  <img width="360" alt="Harness Starter Kit GitHub star 支持插圖" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />
</p>

<p align="center">
  <em>💫 如果這套 kit 對你有幫助，歡迎給一顆 GitHub star。 💫</em>
</p>


## Harness 理論

Harness engineering 會把儲存庫視為 coding agent 可長期依賴的 operating
environment：

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

Harness health 和 agent effectiveness 是不同的概念。Harness Doctor 可以掃描
durable repository evidence，但不能證明 agent 會少犯錯。這件事需要另外用
task outcomes 和 effectiveness reports 來衡量。模型說明請見
[`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)。

每一個 repeated agent failure 都應該轉成至少一個 durable artifact：更清楚的
instruction、automated constraint、test 或 CI check、decision/failure record，
或 drift check。

## 指令

下面的 `/harness ...` 名稱預設是 prompt convention，不是 editor 內建的
command。請直接輸入或貼到 coding agent chat。像 Cursor 這類 editor，除非你另外
新增對應的 custom slash command，否則這些名稱不會出現在 command palette。

| Command | Use when |
| --- | --- |
| `/harness doctor` | 在不修改檔案的前提下，評估 baseline harness evidence。 |
| `/harness update` | 導入之後，更新本機的 `./harness-starter-kit` reference。 |
| `/harness refresh` | 檢查 stale、duplicated、obsolete 或 unused target harness guidance。 |
| `/harness review` | 收尾前，從批判角度檢查目前的 change set。 |
| `/harness review sub-agent` | runtime 允許時，明確要求 read-only reviewer subagent。 |

完整 workflow 請見 [`commands/`](commands/)：
[`doctor`](commands/harness-doctor.md),
[`update`](commands/harness-update.md),
[`refresh`](commands/harness-refresh.md),
[`review`](commands/harness-review.md)。

## Universal Agent Skills 套件

可選的 [`agent-skills/`](agent-skills/) 套件會把同一組 harness workflows 包裝成
Codex 和 Claude Code 可用的 portable Agent Skills。它是建立在本儲存庫
prompt-first workflows 之上的 adapter layer，不能取代 target-repository
inspection。

- 使用 [`agent-skills/skills/harness/SKILL.md`](agent-skills/skills/harness/SKILL.md)
  作為 `/harness adopt`、`/harness doctor`、`/harness update`、
  `/harness refresh`、`/harness review` 的 router。
- 當 runtime 比較適合每個 workflow 一個 command 時，使用
  [`agent-skills/skills/`](agent-skills/skills/) 下的 shortcut skills。
- 作為 Codex plugin 打包時，使用
  [`agent-skills/.codex-plugin/plugin.json`](agent-skills/.codex-plugin/plugin.json)；
  作為 Claude Code plugin 打包時，使用
  [`agent-skills/.claude-plugin/plugin.json`](agent-skills/.claude-plugin/plugin.json)。
- Codex、Claude Code 和 repo-local 安裝說明請見
  [`docs/agent-skills-package.md`](docs/agent-skills-package.md)。

## 導入方式

<details>
<summary>顯示導入細節</summary>

這套 kit 的重點不是自動安裝。Agent 應該先檢查目標儲存庫，再導入最小但有用的
harness artifacts：instructions、enforceable constraints、feedback loops、
durable memory、drift checks，以及 adoption report。請依照
[`docs/adoption-workflow.md`](docs/adoption-workflow.md) 和
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)。

只有在 agent-driven adaptation 前需要初始骨架時，才使用 optional installer。它
會把 profile snippets 複製到 `docs/harness/profiles/<profile>` 供你檢視；
prompt-first adoption 則會讀取 cloned kit 裡的
`harness-starter-kit/templates/profiles/<profile>`。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

上方 badges 裡列出的 profiles 是保守的 reference snippets，不是 automatic
migrations。請見 [`docs/profiles.md`](docs/profiles.md) 和
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md)。

詳細的 documentation index 請見
[`docs/component-map.md`](docs/component-map.md)。常用 adoption references：
[`docs/checklists/external-api-work.md`](docs/checklists/external-api-work.md),
[`docs/checklists/decision-failure-memory.md`](docs/checklists/decision-failure-memory.md),
[`docs/checklists/verification-scripts.md`](docs/checklists/verification-scripts.md)。

Validation coverage 和 local checks 在
[`docs/validation.md`](docs/validation.md)。Lifecycle pilot details 在
[`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)。
這些內容不能證明 harness adoption 會減少 repeated agent mistakes。若要衡量
comparable tasks、wrong-file edits、first-pass verification 與 human rework，請使用
[`docs/evaluation.md`](docs/evaluation.md),
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md),
[`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml)。

Dogfood reports 包含 Next.js public-data target
[`TodayBus`](docs/examples/effectiveness-report-todaybus-dogfood.md)，以及
Spring/Maven backend 和 vanilla frontend target
[`Harness ERP`](docs/examples/effectiveness-report-harness-erp-dogfood.md)。兩者都是
harnessed-only benchmarks，不能當成 effectiveness improvement 的證明。

</details>

## 貢獻者

感謝所有透過 code、docs、reviews、examples、translations 和 dogfooding 一起打磨
這套 kit 的人。

<a href="https://github.com/harnessworks/harness-starter-kit/graphs/contributors">
  <img src="https://readme-contribs.as93.net/contributors/harnessworks/harness-starter-kit?v=20260608-yunhwane" alt="Contributors" />
</a>

## 授權

本專案採用 [MIT License](LICENSE)。

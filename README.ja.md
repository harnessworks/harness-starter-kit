<img width="2172" height="724" alt="Harness Starter Kit ロゴバナー" src="https://github.com/user-attachments/assets/c303dffe-402d-44f4-8d11-3c28936f3a3e" />

<img width="1536" height="1024" alt="Harness engineering のワークフロー図" src="https://github.com/user-attachments/assets/13dbc277-ec47-4c0b-87ca-d31a88e83f4f" />


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

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

<p align="center">
  <a href="https://harnessworks.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
  <a href="https://dev.to/baskduf/i-stopped-prompt-engineering-my-ai-coding-agent-i-started-engineering-the-repo-instead-1i3e">
    <img alt="Read the launch essay" src="https://img.shields.io/badge/Read-Launch_Essay-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/harness-agent-benchmark-runner">
    <img alt="benchmark runner を見る" src="https://img.shields.io/badge/Benchmark-Harness_Runner-2F855A?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

# Harness Starter Kit

繰り返される coding-agent mistakes を durable repository instructions, checks,
memory, evaluation に変えるための prompt-first starter kit です。

## クイックスタート

対象リポジトリをコーディングエージェントで開き、次の prompt を渡します。

<details>
<summary>完全な導入プロンプトを表示</summary>

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

完全な prompt と workflow は
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md) と
[`docs/adoption-workflow.md`](docs/adoption-workflow.md) を参照してください。

<p align="center">
  <img width="360" alt="Harness Starter Kit の GitHub star 案内画像" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />
</p>

<p align="center">
  <em>💫 If this kit helps you, a GitHub star would be appreciated. 💫</em>
</p>


## ハーネス理論

Harness engineering は、リポジトリを coding agent の durable operating
environment として扱います。

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

Harness health は agent effectiveness とは別です。Harness Doctor は durable
repository evidence をスキャンできますが、agent が mistakes を減らすことは
証明できません。task outcomes と effectiveness reports で別に測定してください。
モデルは [`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)
を参照してください。

繰り返される agent failure は、より明確な instruction、automated constraint、
test または CI check、decision/failure record、drift check の少なくとも一つの
durable artifact に変換します。

## コマンド

以下の `/harness ...` 名は、デフォルトでは組み込み editor command ではなく
prompt convention です。coding agent chat に直接入力または貼り付けてください。
Cursor などの editor では、対応する custom slash command を別途追加しない限り
command palette には表示されません。

| Command | Use when |
| --- | --- |
| `/harness doctor` | ファイルを変更せずに baseline harness evidence を採点するとき。 |
| `/harness update` | 導入後にローカル `./harness-starter-kit` reference を更新するとき。 |
| `/harness refresh` | stale、duplicated、obsolete、unused target harness guidance をレビューするとき。 |
| `/harness review` | 完了前に現在の change set を批判的に確認するとき。 |
| `/harness review sub-agent` | runtime が許可する場合に read-only reviewer subagent を明示的に依頼するとき。 |

完全な workflow は [`commands/`](commands/) を参照してください:
[`doctor`](commands/harness-doctor.md),
[`update`](commands/harness-update.md),
[`refresh`](commands/harness-refresh.md),
[`review`](commands/harness-review.md).

## Agent Skills のインストール

Harness workflows はデフォルトでは prompt-first ですが、同じ workflows を
Codex と Claude Code の runtime-native skills として install できます。

### Codex

```bash
codex plugin marketplace add harnessworks/harness-agent-skills-marketplace --ref v0.1.15
```

Codex を再起動し、Plugins 画面を開いて `Harnessworks` marketplace から
`harness-agent-skills` を install してください。

使用例:

```text
$harness doctor
$harness-review
```

### Claude Code

```bash
claude plugin marketplace add harnessworks/harness-agent-skills-marketplace@v0.1.15
claude plugin install harness-agent-skills@harnessworks
```

使用例:

```text
/harness-agent-skills:harness doctor
/harness-agent-skills:harness review
```

ソース package は [`agent-skills/`](agent-skills/) にあります。repo-local
direct install、packaging details、update behavior については
[`docs/agent-skills-package.md`](docs/agent-skills-package.md) を参照してください。

## 導入の仕組み

<details>
<summary>導入の詳細を表示</summary>

この kit は主に自動 installer ではありません。エージェントは対象リポジトリを
先に読み、instructions、enforceable constraints、feedback loops、durable
memory、drift checks、adoption report のうち最小限で有用なものだけを適用します。
[`docs/adoption-workflow.md`](docs/adoption-workflow.md) と
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md) に
従ってください。

optional installer は、agent-driven adaptation の前に skeleton が必要な場合だけ
使います。レビュー用の profile snippets を
`docs/harness/profiles/<profile>` にコピーします。Prompt-first adoption では
cloned kit の `harness-starter-kit/templates/profiles/<profile>` を参照します。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

上の badges に表示される profiles は保守的な reference snippets であり、
automatic migrations ではありません。
[`docs/profiles.md`](docs/profiles.md) と
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md) を
参照してください。

詳細な documentation index は [`docs/component-map.md`](docs/component-map.md) に
あります。主な adoption references:
[`docs/checklists/external-api-work.md`](docs/checklists/external-api-work.md),
[`docs/checklists/decision-failure-memory.md`](docs/checklists/decision-failure-memory.md),
[`docs/checklists/verification-scripts.md`](docs/checklists/verification-scripts.md).

Validation coverage と local checks は
[`docs/validation.md`](docs/validation.md) にあります。Lifecycle pilot details は
[`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)
を参照してください。これらは harness adoption が repeated agent mistakes を
減らすことを証明しません。comparable tasks、wrong-file edits、first-pass
verification、human rework の測定には
[`docs/evaluation.md`](docs/evaluation.md),
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md),
[`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml) を使います。

Dogfood reports には、Next.js public-data target の
[`TodayBus`](docs/examples/effectiveness-report-todaybus-dogfood.md) と、
Spring/Maven backend および vanilla frontend target の
[`Harness ERP`](docs/examples/effectiveness-report-harness-erp-dogfood.md) が
含まれます。どちらも harnessed-only benchmarks であり、effectiveness
improvement の証明ではありません。

</details>

## コントリビューター

code、docs、reviews、examples、translations、dogfooding を通じてこの kit を
形づくってくれたすべての方に感謝します。

<a href="https://github.com/harnessworks/harness-starter-kit/graphs/contributors">
  <img src="https://readme-contribs.as93.net/contributors/harnessworks/harness-starter-kit?v=20260608-yunhwane" alt="Contributors" />
</a>

## 掲載

- [Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents): AI agent tooling project.
- [github/awesome-copilot](https://github.com/github/awesome-copilot): Copilot customization resource.

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

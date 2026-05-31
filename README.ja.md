# harness-starter-kit

**[English](README.md)** | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

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

詳細な運用ドキュメントは英語を基準に維持します。この README は入口です。

## クイックスタート

対象リポジトリをコーディングエージェントで開き、次の prompt を渡します。

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
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit
```

完全な prompt と workflow は
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md) と
[`docs/adoption-workflow.md`](docs/adoption-workflow.md) を参照してください。

## コマンド

### `/harness doctor`

Harness Doctor は、リポジトリが AI coding agent と安定して協働するための
baseline evidence を評価します。Agent Instructions、Feedback Loops、Durable
Memory、Structural Safety、Adoption Clarity の 5 category Harness Score を
報告し、agent effectiveness と governance maturity は non-scored manual
review 項目です。

- Command workflow: [`commands/harness-doctor.md`](commands/harness-doctor.md)
- Rubric: [`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)
- Example report: [`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)

客観的な baseline scan です。macOS/Linux で `python` が使えない場合は
`python3` を使ってください。

```powershell
python scripts/harness_doctor.py --target .
```

### `/harness update`

リポジトリが harness を採用した後は、`/harness update` でローカルの
`./harness-starter-kit` 参照 clone を更新し、新しい harness guidance のうち
合うものだけを選択的に反映できます。

Harness Update は確認済みの kit source を `.harness/source.json` に記録し、
update 候補を分類して Harness Update Report で完了します。target repository
のファイルを無条件に上書きしてはいけません。

- Command workflow: [`commands/harness-update.md`](commands/harness-update.md)

### `/harness refresh`

リポジトリが harness を採用した後は、`/harness refresh` で既存の target
harness にある stale docs、duplicated guidance、obsolete records、unused
checks をレビューできます。

Harness Refresh は findings を keep、update、merge、archive/delete
candidate、manual review に分類します。ローカル kit reference は更新せず、
明示的な承認なしにファイルを削除してはいけません。

- Command workflow: [`commands/harness-refresh.md`](commands/harness-refresh.md)

### `/harness review`

`/harness review` は、完了前に現在の change set を opposing
harness-engineering perspective で点検します。

Harness Review は diagnostic by default です。target source-of-truth
violations、unnecessary automation、weak validation、missing durable memory、
overreach、stale or duplicated guidance を確認します。ユーザーが review 後に
fix 適用を明示的に依頼するまでは、ファイルを変更してはいけません。

- Command workflow: [`commands/harness-review.md`](commands/harness-review.md)
- Report template: [`docs/templates/harness-review-report.md`](docs/templates/harness-review-report.md)
- Example report: [`docs/examples/harness-review-report.md`](docs/examples/harness-review-report.md)

## 導入の考え方

この kit は主に自動 installer ではありません。エージェントは対象リポジトリを
先に読み、最小限の有用な harness artifact だけを適用します。

- `AGENTS.md`: durable agent instructions
- lint、type check、import boundary、project rule による architecture constraints
- tests、CI、pre-commit hooks、明確な失敗メッセージによる feedback loops
- `docs/` 配下の decisions、failures、conventions、domain knowledge store
- code、docs、structure drift を検出する garbage-collection checks

optional installer は、agent-driven adaptation の前に skeleton が必要な場合だけ
使います。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

optional installer は `--force` なしで既存ファイルを上書きしません。Profile
snippet はレビュー用に `docs/harness/profiles/<profile>` にコピーされます。
Prompt-first adoption では cloned kit の
`harness-starter-kit/templates/profiles/<profile>` を参照します。

## Profiles

利用できる profile は `generic`, `python`, `typescript`, `nextjs`, `django`,
`flask`, `fastapi`, `spring`, `android`, `react`, `vue` です。

Profile は保守的な参考資料であり、自動変換ルールではありません。対象
リポジトリの現在の tools と maintenance expectations に合う snippet だけを
採用してください。Stack が後から導入された場合は
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md)
を使います。

## ドキュメントマップ

- Overview: [`docs/overview.md`](docs/overview.md)
- Theory: [`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)
- Adoption workflow: [`docs/adoption-workflow.md`](docs/adoption-workflow.md)
- Harness refresh workflow: [`commands/harness-refresh.md`](commands/harness-refresh.md)
- Harness review workflow: [`commands/harness-review.md`](commands/harness-review.md)
- Full adoption prompt: [`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
- Component map: [`docs/component-map.md`](docs/component-map.md)
- Validation coverage: [`docs/validation.md`](docs/validation.md)
- Effectiveness evaluation: [`docs/evaluation.md`](docs/evaluation.md)
- Lifecycle pilot details: [`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)

## 検証と測定

自動 fixture tests は、Node.js、Next.js、Django、FastAPI、Flask、React、
Spring Boot、Android、Vue、Python、TypeScript 系 profile の installation と
runnable drift checks を検証します。Coverage details と opt-in E2E checks は
[`docs/validation.md`](docs/validation.md) を参照してください。

実際の dogfooding target は
[baskduf/harness_starter_kit_django](https://github.com/baskduf/harness_starter_kit_django)
です。この小さな Django project で prompt-first adoption、`/harness update`、
failure memory、effectiveness tracking を実リポジトリで検証します。

これらの tests は、harness adoption が repeated agent mistakes を減らすことを
証明するものではありません。Comparable tasks、wrong-file edits、first-pass
verification、human rework の測定には
[`docs/evaluation.md`](docs/evaluation.md) と
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)
を使います。個別の手動 task outcome record には
[`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml) を使います。

## ローカルチェック

starter-kit templates、command workflows、installer behavior、drift scripts を
変更する前に、次の checks を実行してください。macOS/Linux で `python` が
使えない場合は `python3` を使ってください。

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/harness_doctor.py --target .
```

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 基本原則

繰り返される agent failure は、より明確な instruction、automated constraint、
test または CI、decision/failure record、drift check の少なくとも一つの
durable artifact に変換します。

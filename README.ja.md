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

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

`harness-starter-kit` は、あらゆるソフトウェアプロジェクトに harness
engineering を適用するための prompt-first スターターキットです。Git URL を
エージェントに渡し、エージェントが対象リポジトリ内に clone して読み、その
リポジトリの実際のツールと制約に合わせて適用することを想定しています。

想定しているワークフローはシンプルです。対象リポジトリをコーディング
エージェントで開き、キットの URL とプロンプトを渡し、エージェントに clone、
read、adapt させます。

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

対象プロジェクトには、実用的なエージェント harness が残るべきです。

- 永続的なエージェント指示のための `AGENTS.md`
- lint、type check、import boundary、プロジェクト固有ルールによる
  アーキテクチャ制約
- test、CI、pre-commit hook、明確な失敗メッセージによるフィードバックループ
- decision、failure、convention、domain context を保存する `docs/` ナレッジストア
- code、document、structure drift を検出する garbage-collection check

## なぜ必要か

プロンプトは一時的です。コンテキストはセッションに閉じています。harness は
プロジェクトに残ります。

よい harness engineering は、繰り返し使う指示をチャットからリポジトリへ
移します。そうすることで、エージェントは安定したルールの中で作業できます。
エージェントがミスをしたとき、長期的な解決策は出力だけを直すことでは
ありません。同じミスが次に起きにくくなるように、ルール、テスト、文書、
自動チェックを追加することです。

## クイックスタート

対象リポジトリをコーディングエージェントで開きます。エージェントに Git URL
を渡し、`./harness-starter-kit` に clone して読み、workflow を適用するよう
依頼します。

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit, read it, then apply its prompt-first
harness engineering workflow to the current project.
```

エージェントが GitHub にアクセスできない場合は、対象リポジトリ内に手動で
clone してから、エージェントに `./harness-starter-kit` を読んで同じ
workflow を適用するよう依頼してください。

### 任意: Skeleton Bootstrap

`apply_harness.py` は skeleton bootstrapper であり、full harness adoption
engine ではありません。手動で実行したい場合は、まず生成されるファイルを
確認します。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

このスクリプトは、`--force` を指定しない限り既存ファイルを上書きしません。
デフォルトではローカル harness ファイルだけを導入します。対象リポジトリに
任意の GitHub Actions harness workflow も追加する場合だけ `--with-ci` を指定します。

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## エージェント主導の導入

新規または既存のプロジェクトで、コーディングエージェントに次のプロンプトを
渡してください。

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

長い版は
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md) に
あります。

## リポジトリ構成

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

## 導入モード

`generic` はどのプロジェクトにも使えます。特定の言語やフレームワークを
仮定せず、durable harness skeleton を提供します。

`python` は対象プロジェクトが Python を使っている場合に選びます。Ruff、
mypy、vulture、pre-commit 向けの Python 用リファレンススニペットを追加します。

`typescript` は対象プロジェクトが JavaScript または TypeScript を使っている
場合に選びます。ESLint、dependency boundary、unused export check、package
script 向けのリファレンススニペットを追加します。

`nextjs` は対象プロジェクトが Next.js アプリの場合に選びます。`next build`、
emit しない TypeScript check、generated file ignore、現在の Next.js lint の
注意点に関するリファレンススニペットを追加します。

`django` は対象プロジェクトが Django アプリの場合に選びます。`manage.py
check`、`manage.py test`、virtual environment ignore、SQLite 開発 DB ignore、
Python `check_harness.py` entrypoint に関するリファレンススニペットを追加します。

`flask` は対象プロジェクトが Flask アプリの場合に選びます。`unittest`
discovery、Flask route check、instance-data ignore、Python `check_harness.py`
entrypoint に関するリファレンススニペットを追加します。

`spring` は対象プロジェクトが Spring Boot アプリの場合に選びます。Maven または
Gradle wrapper check、Spring test command、generated build output ignore、
local config ignore、Python `check_harness.py` entrypoint に関するリファレンス
スニペットを追加します。

`fastapi` は対象プロジェクトが FastAPI アプリの場合に選びます。pytest、mypy、
app import/startup check、generated file ignore、Python `check_harness.py`
entrypoint に関するリファレンススニペットを追加します。

`react` は対象プロジェクトが React アプリの場合に選びます。ESLint、TypeScript
check、test/build script、React-specific lint rule に関するリファレンス
スニペットを追加します。

`vue` は対象プロジェクトが Vue アプリの場合に選びます。ESLint、`vue-tsc`、
test/build script、Vue-specific lint rule に関するリファレンススニペットを
追加します。

プロファイルは意図的に保守的なリファレンス資料です。自動的なプロジェクト変換
ではありません。installer は profile ファイルを
`docs/harness/profiles/<profile>/` にコピーするので、エージェントや maintainer
は対象プロジェクトの既存ビルドシステムを保ちながら、必要なスニペットだけを
merge、adapt、ignore できます。

## インストールと Drift Check Coverage

自動 fixture smoke test は、次の stack で harness installation を検証します。

- Node.js / TypeScript
- Next.js
- Django
- FastAPI
- Flask
- React
- Spring Boot
- Vue

これらの fixture test は、installer が既存ファイルを保持し、期待される profile
snippet を書き込み、generic drift check が実行可能であることを確認します。

追加の end-to-end adoption check は、次の対象に対して手動で実行されています。

- `node --test`、installer の再実行、TypeScript profile `check_harness.py`、
  意図的な drift failure を使った Node.js ES module プロジェクト
- pytest、mypy、generated drift check、FastAPI profile `check_harness.py` を
  使った FastAPI プロジェクト

FastAPI E2E coverage は virtual environment を作成し dependency をインストール
するため、opt-in の自動テストとして提供しています。

```powershell
$env:RUN_FASTAPI_E2E = "1"
python -m unittest tests.test_fastapi_profile_e2e
```

GitHub Actions では、`Harness Check` workflow を手動実行し、
`run_fastapi_e2e` を有効にすると同じ dependency-installing test が実行されます。

## 効果測定

上記の自動テストは、インストール動作と実行可能な drift check を検証します。
harness adoption が繰り返される agent mistake を減らしたことの証明では
ありません。その効果は
[`docs/evaluation.md`](docs/evaluation.md) のプロトコルで別途測定します。

adoption 時には
[`docs/templates/adoption-report.md`](docs/templates/adoption-report.md) の
Effectiveness Measurement Plan を埋めてください。baseline がない場合は
harnessed-only tracking として記録し、次の comparable task、primary metric、
review window、results location を定義します。実際の before/after または
後続の観測結果は
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)
に記録します。

## ローカルチェック

starter kit のテンプレート、インストーラー、drift script を変更した後は、
次のチェックを実行してください。

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_effectiveness_plan.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_effectiveness_plan.py
```

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下で配布されます。

## 基本原則

繰り返し起きるエージェントの失敗は、少なくとも一つの durable artifact に
変換するべきです。

- `AGENTS.md` のより明確な指示
- 自動化された制約
- test または CI check
- decision または failure record
- drift check

これが harness engineering の中心です。

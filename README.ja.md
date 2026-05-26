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

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

`harness-starter-kit` は、あらゆるソフトウェアプロジェクトに harness
engineering を適用するためのスターターキットです。

想定しているワークフローはシンプルです。

```text
Clone harness-starter-kit into a target project.
Ask an agent: "Read ./harness-starter-kit and apply its harness engineering guidelines
to this repo. Preserve the existing architecture and add only the minimum
missing harness files."
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

このリポジトリを対象プロジェクトの中にクローンまたはダウンロードします。

```text
workspace/
`-- target-repo/
    |-- harness-starter-kit/
    `-- existing-project-files
```

次に、対象リポジトリをコーディングエージェントで開き、このプロンプトを渡します。

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

インストーラーを手動で実行したい場合は、まず生成されるファイルを確認します。

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
仮定せず、durable harness skeleton を導入します。

`python` は対象プロジェクトが Python を使っている場合に選びます。Ruff、
mypy、vulture、pre-commit 向けの Python 用リファレンススニペットを追加します。

`typescript` は対象プロジェクトが JavaScript または TypeScript を使っている
場合に選びます。ESLint、dependency boundary、unused export check、package
script 向けのリファレンススニペットを追加します。

プロファイルは意図的に保守的です。既存のビルドシステムを書き換えるのではなく、
スニペットとガイドを提供します。

## ローカルチェック

starter kit のテンプレート、インストーラー、drift script を変更した後は、
次のチェックを実行してください。

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
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

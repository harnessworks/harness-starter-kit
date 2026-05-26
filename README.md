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

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

`harness-starter-kit` is a starter kit for applying harness engineering to any
software project.

The intended workflow is simple:

```text
Clone harness-starter-kit into a target project.
Ask an agent: "Read ./harness-starter-kit and apply its harness engineering guidelines
to this repo. Preserve the existing architecture and add only the minimum
missing harness files."
```

The target project should end up with a practical agent harness:

- `AGENTS.md` for durable agent instructions
- architecture constraints through linting, type checks, import boundaries, or
  project-specific rules
- feedback loops through tests, CI, pre-commit hooks, and clear failure messages
- a knowledge store under `docs/` for decisions, failures, conventions, and
  domain context
- garbage-collection checks that detect code, document, and structure drift

## Why This Exists

Prompting is temporary. Context is session-scoped. A harness is project-scoped.

Good harness engineering moves repeated instructions out of chat and into the
repository so agents can work inside stable rules. When an agent makes a
mistake, the long-term fix is not only to correct that output. The better fix is
to add a rule, test, document, or automated check that makes the same mistake
less likely next time.

## Quick Start

Clone or download this repository inside the target project:

```text
workspace/
`-- target-repo/
    |-- harness-starter-kit/
    `-- existing-project-files
```

Then open `target-repo`, not `target-repo/harness-starter-kit`, with your
coding agent and give it this prompt:

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

The prompt-first workflow is the main way to use this kit because the agent can
inspect the target repository and adapt to its existing tools.

If you want a mechanical bootstrap instead, preview the generated files first:

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

The script never overwrites existing files unless `--force` is provided.
By default it installs local harness files only; add `--with-ci` when the target
repository should also receive the optional GitHub Actions harness workflow.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## Agent-Driven Adoption

In a new or existing project, give your coding agent this prompt:

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

The longer version lives in
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md).

## Repository Layout

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

## Adoption Modes

Use `generic` for any project. It installs the durable harness skeleton without
assuming a language or framework.

Use `python` when the target project uses Python. It adds Python-focused
reference snippets for Ruff, mypy, vulture, and pre-commit.

Use `typescript` when the target project uses JavaScript or TypeScript. It adds
reference snippets for ESLint, dependency boundaries, unused export checks, and
package scripts.

Profiles are intentionally conservative. They provide snippets and guidance
instead of rewriting existing build systems.

## Local Checks

Run these checks before changing the starter kit templates or installer:

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
```

## License

This project is licensed under the [MIT License](LICENSE).

## Core Principle

Every recurring agent failure should be converted into at least one durable
artifact:

- a clearer instruction in `AGENTS.md`
- an automated constraint
- a test or CI check
- a decision or failure record
- a drift check

That is the heart of harness engineering.

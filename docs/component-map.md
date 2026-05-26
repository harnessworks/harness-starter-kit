# Component Map

This map connects harness engineering concepts to files in a target repository.

| Harness Concept | Target Repo Artifact | Starter Template |
| --- | --- | --- |
| Agent instructions | `AGENTS.md` | `templates/generic/AGENTS.md` |
| Architecture decisions | `docs/decisions/*.md` | `templates/generic/docs/decisions/000-template.md` |
| Failure memory | `docs/failures/*.md` | `templates/generic/docs/failures/000-template.md` |
| Coding conventions | `docs/conventions/*.md` | `templates/generic/docs/conventions/coding.md` |
| Domain knowledge | `docs/domain/*.md` | `templates/generic/docs/domain/glossary.md` |
| Document drift check | `scripts/check_docs_drift.py` | `templates/generic/scripts/check_docs_drift.py` |
| Structure drift check | `scripts/check_structure.py` | `templates/generic/scripts/check_structure.py` |
| Optional scheduled harness check | `.github/workflows/harness-check.yml` | `templates/generic/.github/workflows/harness-check.yml` |
| Stack-specific rules | lint/type/pre-commit snippets | `templates/profiles/*` |

## Minimum Useful Install

For a very small project, install only:

- `AGENTS.md`
- `docs/decisions/000-template.md`
- `docs/failures/000-template.md`
- `scripts/check_docs_drift.py`
- `scripts/check_structure.py`

Then grow the harness as the project and agent usage mature.
Install the optional GitHub Actions workflow with `--with-ci` only after
confirming the target repository uses GitHub Actions.

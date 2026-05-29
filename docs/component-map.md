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
| Encoding hygiene check | `scripts/check_encoding_hygiene.py` | `templates/generic/scripts/check_encoding_hygiene.py` |
| Effectiveness plan check | `scripts/check_effectiveness_plan.py` | `templates/generic/scripts/check_effectiveness_plan.py` |
| Harness readiness diagnostic | `/harness doctor` report | `commands/harness-doctor.md`, `docs/scoring/harness-score-rubric.md` |
| Harness source tracking | `.harness/source.json` | documented in `commands/harness-update.md` |
| Harness update workflow | `/harness update` report | `commands/harness-update.md` |
| Harness refresh workflow | `/harness refresh` report | `commands/harness-refresh.md` |
| Baseline harness score scan | preliminary file and directory scan | `scripts/harness_doctor.py` |
| Optional scheduled harness check | `.github/workflows/harness-check.yml` | `templates/generic/.github/workflows/harness-check.yml` |
| Stack-specific rules | lint/type/pre-commit/framework snippets | `templates/profiles/*` |
| Profile absorption | checklist for turning profile snippets into project rules | `docs/checklists/profile-absorption.md` |
| Adoption report example | final adoption summary | `docs/templates/adoption-report.md`, `examples/*-adoption-report.md` |
| Effectiveness evaluation | agent mistake reduction measurement | `docs/evaluation.md`, `docs/templates/effectiveness-report.md` |
| Validation coverage | tests, smoke checks, and E2E coverage notes | `docs/validation.md` |
| Lifecycle pilot results | prompt-first adoption behavior evidence | `docs/examples/lifecycle-pilot-results.md` |

## Minimum Useful Adoption

For a very small project, the agent should add or adapt only:

- `AGENTS.md`
- `docs/decisions/000-template.md`
- `docs/failures/000-template.md`
- `scripts/check_docs_drift.py`
- `scripts/check_structure.py`
- `scripts/check_encoding_hygiene.py`
- `scripts/check_effectiveness_plan.py`

Then grow the harness as the project and agent usage mature.
Use the optional GitHub Actions workflow skeleton with `--with-ci` only after
confirming the target repository uses GitHub Actions.

Use `/harness doctor` when the maintainer wants a diagnostic score before or
after adoption. The command reports readiness; it does not install harness
files.

Use `/harness update` after adoption when the maintainer wants to refresh the
local kit reference and selectively apply new harness guidance. The command
records the current kit source in `.harness/source.json` and reports applied,
skipped, and manual-review items.

Use `/harness refresh` after adoption when the maintainer wants to clean up the
target harness itself. The command reviews stale docs, duplicated guidance,
obsolete records, and unused checks, then reports keep, update, merge,
archive/delete candidate, and manual-review items without deleting files unless
the user explicitly approves the specific files.

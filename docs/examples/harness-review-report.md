# Harness Review Example Report

This example shows the expected report shape for `/harness review` and
`/harness review sub-agent`. It is diagnostic and does not apply fixes.
When a subagent is used, the parent or orchestrator determines `Reviewer mode`
and `Fallback reason` from the actual spawn/wait result, not from subagent
output.

```text
Harness Review Report

Reviewed Changes:
- Invocation: /harness review sub-agent
- Branch/status: feature/add-harness-docs with unstaged documentation changes
- Changed files reviewed: AGENTS.md, docs/adoption-workflow.md,
  scripts/check_structure.py, templates/generic/AGENTS.md
- Review scope: current diff
- Reviewer mode: subagent used
- Fallback reason: none

Findings:
- P1: AGENTS.md now says agents must run a new architecture check, but the check
  is not documented in README.md or wired into the local validation list. Future
  agents may miss it.
- P2: templates/generic/AGENTS.md describes a framework-specific state rule.
  That belongs in a target repository or a stack profile, not the generic
  template.

Missing Checks:
- Run `python scripts/check_docs_drift.py` after adding the new README link.
- Run the changed structure check against a fixture that intentionally violates
  the new rule.

Durable Memory Assessment:
- Decision records: skipped; this documentation change does not choose a new
  architecture, framework, or integration boundary.
- Failure records: skipped; no user-visible runtime failure, failed CI run,
  failed harness check, repeated agent mistake, or cross-environment mismatch
  was fixed.
- Conventions/domain/effectiveness docs: update docs/conventions/coding.md if
  the new architecture check becomes a standing review rule.

Overreach Risk:
- The generic template change risks replacing target repository conventions with
  starter-kit defaults.
- No policy enforcement, CI adapter, pre-commit hook, runtime hook, or installer
  automation was added.

Manual Decisions Needed:
- Decide whether the new architecture check is target-specific guidance,
  profile guidance, or generic starter-kit guidance before merging.

Recommended Follow-Up:
1. Move the framework-specific state rule out of the generic template.
2. Add fixture coverage for the new structure check before documenting it as a
   required validation command.
3. Update README.md or AGENTS.md so future agents know when to run the check.
```

## Single-Agent Fallback Example

```text
Harness Review Report

Reviewed Changes:
- Invocation: /harness review
- Branch/status: docs/harness-review-fallback with unstaged command-doc changes
- Changed files reviewed: commands/harness-review.md,
  docs/templates/harness-review-report.md
- Review scope: current diff
- Reviewer mode: single-agent fallback
- Fallback reason: tool present but not permitted by active runtime/tool
  instructions

Findings:
- none

Missing Checks:
- Run `python -m unittest tests.test_repository_hygiene` after changing the
  command contract.

Durable Memory Assessment:
- Decision records: skipped; this refines command behavior without choosing a
  new architecture or integration boundary.
- Failure records: skipped; no user-visible runtime failure, failed CI run,
  failed harness check, repeated agent mistake, or cross-environment mismatch
  was fixed.
- Conventions/domain/effectiveness docs: skipped; no durable convention or
  effectiveness measurement changed.

Overreach Risk:
- none

Manual Decisions Needed:
- none

Recommended Follow-Up:
1. Re-run the full documented validation suite before release.
2. Keep the fallback reason visible in any saved review report.
3. Revisit the command after real target-repository review usage.
```

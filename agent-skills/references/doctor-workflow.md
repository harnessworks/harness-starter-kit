# Harness Doctor Workflow

Use this diagnostic to evaluate repository readiness for reliable AI coding
agent collaboration. Do not modify files.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect durable repository evidence:
   - `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`,
     `.github/copilot-instructions.md`
   - README, contributing docs, project docs, package manifests, CI configs
   - `docs/decisions`, `docs/failures`, `docs/conventions`, `docs/domain`
   - scripts, tests, lint/type/build config, pre-commit config
3. If a local kit clone exists, treat it as read-only reference material.
4. If available, run `python scripts/harness_doctor.py --target .` and use it
   as baseline evidence, not as the whole judgment.
5. Score the six harness elements:
   - Instructions
   - Constraints
   - Feedback
   - Memory
   - Evaluation
   - Governance
6. Report coupling findings between rules, checks, memory, evaluation, and
   governance.

## Scoring Rules

- Score durable repository evidence only.
- Do not give points for chat-only intent.
- Do not count runtime-only sandbox/tool behavior unless assumptions are
  visible in repository files, commands, CI, or approval rules.
- Harness health is not proof of agent effectiveness.

## Report Format

```text
Harness Doctor Report

Score: <score>/100
Grade: <grade>

Verdict:
<one short paragraph>

Element Breakdown:
- Instructions: <points>/100 | Stated <status> · Routed <status> · Proven <status>
- Constraints: <points>/100 | Stated <status> · Enforced <status> · Proven <status>
- Feedback: <points>/100 | Exists <status> · Coverage <status> · Proven <status>
- Memory: <points>/100 | Recorded <status> · Operationalized <status> · Proven <status>
- Evaluation: <points>/100 | Exists <status> · Coverage <status> · Proven <status>
- Governance: <points>/100 | Exists <status> · Coverage <status> · Proven <status>

Coupling Findings:
- <severity> <finding type>: <evidence and review question>

Evidence:
- <durable evidence found>
- <missing or weak evidence>

Non-Scored Manual Review:
- Proven effectiveness: <evidence or unmeasured>
- Runtime execution/tooling: <repo-visible assumptions or out of scope>

Top Risks:
1. <risk>
2. <risk>
3. <risk>

Recommended Next Actions:
1. <durable improvement>
2. <durable improvement>
3. <durable improvement>
```

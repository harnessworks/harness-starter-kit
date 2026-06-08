# Harness Engineering Theory

Harness engineering is the practice of shaping a repository so coding agents
work inside durable project context instead of relying on one-off chat prompts.

This document is an operational model, not a literature review. Use it to decide
which harness artifact to add, update, measure, or remove during adoption,
update, and refresh work.

## Working Model

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

| Part | Purpose | Common repository artifacts |
| --- | --- | --- |
| Instructions | Tell agents what the project is, how to work, and what to avoid. | `AGENTS.md`, `CLAUDE.md`, contribution docs |
| Constraints | Make important rules enforceable where practical. | lint rules, type checks, import rules, drift checks, CI gates |
| Feedback | Give fast, concrete signals after a change. | tests, `scripts/check_harness.py`, `scripts/check_*.py`, CI |
| Memory | Preserve decisions, failures, conventions, and domain context across sessions. | `docs/decisions`, `docs/failures`, `docs/conventions`, `docs/domain` |
| Evaluation | Measure harness readiness and observed agent outcomes. | Harness Doctor, effectiveness reports, task outcome records |
| Governance | Keep the harness maintained without making it an automatic rewrite system. | `/harness update`, `/harness refresh`, `.harness/source.json`, commit and PR rules |

The model deliberately keeps the target repository as the source of truth.
Harness artifacts are useful only when they reflect the target's real
architecture, commands, generated files, risks, and review habits.

## How To Use This Model

Use the model as a decision table when a harness gap appears.

| Situation | Add or update | Review question |
| --- | --- | --- |
| The agent does not know the project shape, commands, or forbidden actions. | Instructions | Is the guidance short, durable, and specific to this repository? |
| The agent can violate a rule that tooling can detect. | Constraints | Can lint, types, import rules, drift checks, or CI enforce it? |
| The agent needs a fast pass/fail signal after a change. | Feedback | Is there a local command or CI check with clear failure output? |
| The same decision, convention, domain term, or failure mode keeps reappearing. | Memory | Should this become a decision, failure, convention, or domain record? |
| The maintainer wants evidence that agent work improved. | Evaluation | Is there a comparable task outcome record, not just a health score? |
| Harness guidance is stale, duplicated, untrusted, or source-tracking changed. | Governance | Is this `/harness refresh`, `/harness update`, or manual review work? |

When multiple rows apply, prefer enforceable constraints and feedback over more
prose. Keep instructions minimal; unnecessary requirements can make agent tasks
harder and more expensive.

Use this table before adding adoption, update, or refresh work. It should help
choose the next durable artifact, not justify adding every artifact.

## Health Versus Effectiveness

Harness health is the condition of the repository harness itself. It asks
whether durable instructions, enforceable constraints, feedback loops, memory,
and maintenance paths exist and are discoverable. Harness Doctor is a harness
health diagnostic. Its six-element score is a repository evidence scan, and its
coupling findings highlight broken links such as rules without checks, checks
without clear rules, memory without recurrence detection, or risky change types
without governance.

Agent effectiveness is the observed result of agent work. It asks whether
agents edit fewer wrong files, repeat fewer known mistakes, pass verification
earlier, trigger useful drift checks, or require less human rework. These
outcomes require task records or effectiveness reports.

A high Harness Doctor score does not prove that agents became smarter, safer,
or more productive. It means the repository has stronger baseline evidence for
agent collaboration. Treat it as a readiness signal, not an outcome claim.

`Proven` signals should be interpreted carefully. A repository can prove that a
check exists, that a rule is wired into CI, or that a failure record names a
recurrence-detection path. It cannot prove reduced agent mistakes without task
outcome records or effectiveness reports that compare observable outcomes.

## Improvement Loop

Use this loop when a repository has repeated agent work:

1. Map the work: identify the task type, expected file boundary, local commands,
   and likely failure modes.
2. Add or refine harness artifacts: instructions, constraints, feedback, memory,
   evaluation, or governance.
3. Measure harness health: run local checks and, when useful, Harness Doctor.
4. Record task outcomes: capture wrong-file edits, repeated mistakes,
   verification results, drift detections, rework, and reverted files.
5. Manage the next change: update rules, checks, decision records, failure
   records, or refresh guidance only where the evidence justifies it.

This loop is intentionally lightweight. The goal is not to build a research
platform. The goal is to make recurring agent failure modes visible and cheaper
to prevent.

## Related Ideas

Harness engineering combines familiar software practices around a new user of
the repository: the coding agent.

- Test harnesses isolate behavior and make expected outcomes repeatable. A
  repository harness does the same for agent work by defining setup, commands,
  fixtures, and acceptance signals.
- CI and self-testing code turn quality expectations into repeatable checks.
  Harness constraints should follow that pattern when a rule is important and
  mechanically detectable.
- Architecture Decision Records make architectural memory durable. Harness
  memory uses ADRs for decisions and failure records for mistakes that future
  agents should not repeat.
- SRE postmortems convert incidents into prevention and detection work. Harness
  failure memory follows the same loop for failed checks, CI failures, repeated
  agent mistakes, and cross-environment mismatches.
- LLM and agent evaluation separates claims from measurements. Harness
  adoption should be evaluated with comparable task outcomes, not assumed from
  the presence of templates.
- AI risk management loops such as govern, map, measure, and manage are useful
  because they separate policy, context, evidence, and response. Harness
  governance should do the same at repository scale.

## Non-Goals

- Do not treat the starter kit as an installer that knows a target repository
  better than the target repository knows itself.
- Do not copy every template or profile snippet just to improve a score.
- Do not claim fixture tests, lifecycle pilots, or Harness Doctor scores prove
  agent mistake reduction.
- Do not add a dashboard, database, or metrics pipeline until a real repository
  has enough task outcome records to justify that maintenance cost.

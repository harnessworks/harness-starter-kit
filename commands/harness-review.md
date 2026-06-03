# /harness review

Review the current change set from an opposing harness-engineering perspective.

Harness Review is diagnostic by default. Do not create, edit, delete, move,
format, or stage files while running this command unless the user explicitly
asks you to apply fixes after seeing the review.

Run this review before commit or push when practical. If it runs after commit or
push, record that timing so maintainers know whether it acted as a safety gate
or as a post-hoc diagnostic.

## Goal

Challenge whether the current work preserves the target repository as the
source of truth, avoids unnecessary automation, keeps templates conservative,
adds enforceable checks only where practical, updates durable memory when
needed, and runs the right validation before completion.

Every review must check whether the current environment exposes a multi-agent
or subagent review tool, record the reviewer mode, and report any fallback
reason. The parent or orchestrator agent that runs this command owns the
reviewer-mode and fallback decision. Do not depend on any specific agent
runtime.

## Invocation Modes

### `/harness review`

Run the normal diagnostic review. At the start, check whether multi-agent or
subagent tools are available in the current environment. If a subagent tool is
available and permitted by the active runtime and tool instructions for this
invocation, invoke a read-only reviewer subagent before writing the final
review.

If the active tool instructions require an explicit user request to spawn a
subagent and the user only asked for `/harness review`, treat the tool as
present but not permitted, continue with a single-agent reviewer perspective,
and report the fallback reason.

### `/harness review sub-agent`

Run the same diagnostic review, but treat this invocation as the user's
explicit request to use a read-only reviewer subagent. If a multi-agent or
subagent tool is available and permitted by the active runtime and tool
instructions, invoke it before writing the final review.

This mode is still diagnostic only. It is not permission to modify files, add
runtime-specific subagent integration, or ignore higher-priority tool
instructions. If no such tool is available, the tool is blocked, the active
runtime still does not permit the call, or the subagent call fails, continue
with a single-agent reviewer perspective and state the fallback reason in the
report.

## Scope

Harness Review reviews the current work or proposed change set. It does not
score harness readiness like `/harness doctor`, refresh the local kit reference
like `/harness update`, or clean up stale target harness guidance like
`/harness refresh`.

It is also different from the maintenance checklist in
`docs/checklists/harness-review.md`. That checklist is for monthly or repeated
mistake review; this command is for the current change set.

It must not implement runtime hooks, policy-driven enforcement, pre-commit
hooks, CI adapters, runtime-specific subagent integration, or broader installer
automation.

## Procedure

1. Treat the current working directory as the target repository root.
2. Determine whether the user invoked `/harness review` or
   `/harness review sub-agent`, then check whether multi-agent or subagent
   tools are available in the current environment.
   - For `/harness review`, use a subagent only when the tool is available and
     permitted by the active runtime and tool instructions for this invocation.
   - For `/harness review sub-agent`, treat the invocation as explicit user
     permission to use a read-only reviewer subagent, while still obeying the
     active runtime and tool instructions.
   - If a subagent tool is available and permitted by the active runtime and
     tool instructions, call a read-only reviewer subagent before producing the
     final report.
   - Limit the subagent prompt to: "Read the current diff, staged diff,
     AGENTS.md, docs/decisions, docs/failures, docs/conventions, and
     docs/domain. You are the read-only reviewer subagent. Do not assess
     reviewer mode, fallback reason, or subagent availability. Return only
     review findings, missing checks, and risks. Do not produce a full Harness
     Review Report. Do not modify files."
   - The parent or orchestrator agent must determine `Reviewer mode` and
     `Fallback reason` from the actual availability check and subagent
     spawn/wait result. Do not trust or copy reviewer-mode, fallback-reason, or
     subagent-availability claims from subagent output.
   - If no subagent tool is available, the tool is present but not permitted,
     the tool is blocked, or the subagent call fails, use a single-agent
     reviewer perspective and record the fallback reason in the report.
   - Use a concrete fallback reason such as `tool unavailable`,
     `tool present but not permitted`, `tool blocked`, or `subagent call
     failed`.
   - Do not skip this availability check silently.
3. Inspect repository state and the change set:
   - `git status --short --branch`
   - `git diff --stat`
   - `git diff --check`
   - `git diff --cached --stat` and `git diff --cached --check` when staged
     changes exist
   - whether the review is pre-commit, pre-push, post-push, or unknown based on
     the current branch and user-provided context
4. Review changed files and nearby harness context:
   - changed `AGENTS.md`, `CLAUDE.md`, README files, contribution docs, and CI
     configs
   - changed `commands/`, `docs/`, `templates/`, `scripts/`, package manifests,
     lint configs, test configs, and pre-commit config
   - `docs/decisions/`, `docs/failures/`, `docs/conventions/`, and
     `docs/domain/` when the change affects architecture, behavior, workflow,
     integration boundaries, or repeated failure paths
5. Challenge source-of-truth preservation:
   - Does the change preserve the target repository's architecture, tools,
     package manager, docs, commands, and conventions?
   - Does it avoid copying starter-kit templates blindly?
   - Does it keep profile snippets as reference material instead of mandatory
     transformations?
6. Challenge overreach and automation:
   - Does the change add package scripts, pre-commit hooks, CI wiring, runtime
     hooks, dependency constraints, or policy enforcement without target
     evidence and maintainer approval?
   - Does it make the installer more automatic or more willing to overwrite
     target files?
   - Are templates still generic and conservative?
7. Challenge checks and validation:
   - Are important rules enforceable through lint, tests, type checks, import
     rules, CI, or drift checks where practical?
   - If automation is not practical, is the manual review point documented?
   - Are deterministic, local, non-network, reasonably fast checks for product
     behavior that agents are expected to verify repeatedly
     included in the documented normal completion gate, or is there a recorded
     reason they remain focused or manual?
   - Are live API, credential, quota, provider-uptime, visual, device, slow, or
     otherwise fragile checks kept separate from the normal gate when they are
     unsafe as default verification?
   - Were the right local checks run for the files changed?
   - Are missing checks or unverified assumptions named clearly?
   - Does each new or updated failure record name the regression test, fixture,
     smoke check, lint rule, drift check, CI gate, or manual review point that
     prevents or detects recurrence, or explain why no check is practical?
8. Challenge durable memory:
   - Does the change require a decision record, failure note, convention update,
     domain note, adoption report update, or effectiveness measurement update?
   - Ask whether the change alters user workflow, input contract, input
     semantics, state normalization, API request or response shape, fallback
     policy, or displayed decision criteria.
   - If the change fixes product or workflow structure in code, changes an
     integration or mock external-behavior boundary, introduces major data
     models or state classifications, codifies a product UX principle in
     implementation, or changes one of the decision-memory trigger axes above,
     and `docs/decisions/` was not changed, flag whether an existing ADR covers
     it or why the change is too narrow to need decision memory. Treat this as
     a diagnostic warning, not an automatic failure.
   - If no durable memory was added, is that justified?
   - If the work fixed a user-visible runtime failure, high-risk bug path,
     failed CI run, failed harness check, repeated agent mistake, or
     cross-environment mismatch, was `docs/failures/*.md` updated or explicitly
     skipped with a reason, and was the detection or prevention check named?
9. Check for stale or duplicated guidance:
   - Are new command docs, templates, examples, README links, component maps, and
     tests aligned?
   - Does the change duplicate existing guidance instead of updating the
     authoritative location?
10. Produce the required report format. Do not apply fixes unless the user asks
   for a follow-up implementation after reviewing the report.

## Required Report Format

```text
Harness Review Report

Reviewed Changes:
- Invocation: <command used: /harness review or /harness review sub-agent>
- Branch/status: <summary>
- Changed files reviewed: <files>
- Review scope: <current diff, staged diff, PR diff, or described change>
- Review timing: <pre-commit, pre-push, post-push, or unknown>
- Reviewer mode: <subagent used | single-agent fallback>
- Fallback reason: <reason or none>

Findings:
- <severity>: <finding with file/path evidence, or "none">

Missing Checks:
- <check that should be run, why it matters, or "none">

Gate Placement:
- <normal completion gate reviewed, deterministic behavior checks included or
  excluded with reason, and focused/manual checks with reasons>

Durable Memory Assessment:
- Decision records: <needed, updated, skipped with reason>
- Failure records: <needed, updated, skipped with reason; include
  detection/prevention check or reason none is practical>
- Conventions/domain/effectiveness docs: <needed, updated, skipped with reason>

Overreach Risk:
- <source-of-truth, unnecessary automation, installer, template, policy, CI,
  pre-commit, or runtime-hook risk, or "none">

Manual Decisions Needed:
- <maintainer decision needed before applying changes, or "none">

Recommended Follow-Up:
1. <highest-value follow-up>
2. <next follow-up>
3. <next follow-up>
```

## Safety Rules

- Do not modify files during `/harness review` unless the user explicitly asks
  to apply fixes after seeing the review.
- Do not stage, commit, format, delete, archive, move, or rename files while
  reviewing.
- Do not add runtime hooks, runtime-specific subagent integration, policy
  enforcement, pre-commit hooks, CI adapters, package scripts, dependency
  constraints, or broader installer automation as part of the review.
- Do not silently skip the multi-agent or subagent availability check. If the
  review falls back to a single-agent perspective, report why.
- Do not ask the spawned reviewer subagent to assess reviewer mode, fallback
  reason, or subagent availability. The spawned subagent should only report
  findings, missing checks, and risks.
- Do not copy reviewer-mode or fallback fields from subagent output. The parent
  or orchestrator agent records those fields from the actual spawn/wait outcome.
- Treat `/harness review sub-agent` only as explicit permission to request a
  read-only reviewer subagent. It is not approval to modify files or add
  runtime-specific subagent integration.
- Do not treat a clean review as proof of agent effectiveness. It is a
  change-set diagnostic, not an outcome measurement.
- If you recommend a stronger check or policy, present it as follow-up or a
  maintainer decision unless the user explicitly asks to implement it.

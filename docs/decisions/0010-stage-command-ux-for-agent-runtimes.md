# 0010. Stage Command UX For Agent Runtimes

## Status

Accepted

## Context

Harness Starter Kit exposes prompt-first workflows through README prompts,
`/harness ...` prompt conventions, Codex skills, and Claude Code plugin skills.
The workflow set had the right primitives, but the user-facing presentation made
new users compare individual commands before understanding when to use them.

The most confusing areas were:

- first-time adoption was documented as a large Quick Start prompt, while the
  runtime skills already supported `/harness adopt`
- `doctor`, `review`, `update`, and `refresh` were listed as peers even though
  they belong to different stages of use
- Codex and Claude Code examples showed different small command subsets, making
  the runtime-native UX look inconsistent
- `update` and `refresh` are both maintenance actions, but they operate on
  different sources: the kit reference versus the target repository's existing
  harness guidance

## Decision

Present command UX by user stage across README and Agent Skills docs:

- First time: `doctor` to inspect, then `adopt` to apply the smallest useful
  harness pieces
- Daily work: `review` before commit or PR
- Maintenance: `update` for newer kit-source adoption, `refresh` for stale local
  target harness guidance

Add `commands/harness-adopt.md` as the canonical command workflow for first-time
adoption while keeping `docs/adoption-workflow.md` as the deeper background
workflow. Keep Codex and Claude Code examples aligned to the same stage model,
even though Claude plugin invocation is namespaced.

## Rationale

- Stage-based commands are easier for new users than a flat command list.
- Keeping `adopt` explicit closes the gap between the first-prompt README flow
  and the runtime-native `harness-adopt` skill.
- Grouping `update` and `refresh` under Maintenance reduces naming confusion
  without breaking existing command names.
- The target repository remains the source of truth because `adopt` is still a
  prompt-first workflow, not a blind installer.

## Alternatives Considered

- Add a new `/harness maintain` command. Rejected for now because it would add a
  new command surface before the simpler documentation and routing cleanup is
  proven useful.
- Rename `update` and `refresh`. Rejected because existing docs, skills, and
  user habits already use those names; stage grouping is lower risk.
- Keep adoption only as a Quick Start prompt. Rejected because Codex and Claude
  users need the same mental model as prompt-only users.

## Agent Guidance

When explaining commands, use the stage model first: First time, Daily work,
Maintenance. Do not present `update` and `refresh` as generic synonyms. Say that
`update` brings in a newer kit reference and `refresh` cleans up existing target
harness guidance. Treat `/harness adopt` as first-time prompt-first adoption, not
an automatic template installer.

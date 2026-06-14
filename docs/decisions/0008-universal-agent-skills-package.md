# 0008. Package Harness Workflows As Universal Agent Skills

## Status

Accepted

## Date

2026-06-14

## Context

Harness Starter Kit has treated `/harness ...` names as prompt conventions
rather than runtime-native commands. That keeps adoption portable, but it also
requires maintainers to paste or remember the workflow routing in every coding
agent surface.

Codex and Claude Code both support filesystem-based Agent Skills with
progressive disclosure. A skill can expose the same workflow in a runtime-native
way while loading detailed instructions only when needed.

The risk is over-packaging. If the skills become a separate source of truth,
they can drift from `commands/`, `docs/adoption-workflow.md`, and the kit's
prompt-first philosophy.

## Decision

Add `agent-skills/` as a universal Agent Skills package.

The package includes:

- a `harness` router skill for `/harness adopt`, `/harness doctor`,
  `/harness update`, `/harness refresh`, `/harness review`, and
  `/harness review sub-agent`
- shortcut skills for each workflow
- bundled workflow references for standalone installs
- a Codex plugin manifest at `agent-skills/.codex-plugin/plugin.json`
- a Claude Code plugin manifest at `agent-skills/.claude-plugin/plugin.json`
- validation through `scripts/check_agent_skills_package.py`

The repository workflow docs remain canonical. Skills must first prefer target
repository evidence, then a target-local `./harness-starter-kit` clone, then the
package's bundled fallback references.

## Rationale

- A shared Agent Skills package lets Codex and Claude Code users invoke the
  same workflows without changing the kit's underlying model.
- Keeping the skills short preserves progressive disclosure and avoids loading
  the whole starter kit into context.
- Bundled fallback references make standalone installs usable, while source
  priority rules prevent the package from overriding a target repository or a
  local kit clone.
- A dedicated drift check makes the new distribution surface visible in normal
  validation.

## Consequences

- Changes to `agent-skills/` are now decision-bearing harness product behavior.
- Validation must include `scripts/check_agent_skills_package.py`.
- Documentation must explain that the package is optional and adapter-oriented.
- Future command workflow changes should update the matching skill references
  or intentionally document why the skill package is not affected.

## Known Limits And Follow-Up

- The bundled references are compact workflow fallbacks, not full replacements
  for the canonical command docs.
- The package does not install itself into a user's Codex or Claude Code
  configuration; it documents copy and plugin-packaging paths.
- Public marketplace publication remains a separate release operation from the
  prompt-first package source.

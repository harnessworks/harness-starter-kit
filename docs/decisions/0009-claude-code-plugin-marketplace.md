# 0009. Publish Harness Agent Skills Through Claude Code Plugins

## Status

Accepted

## Date

2026-06-14

## Context

The Universal Agent Skills package is intentionally prompt-first: canonical
workflow behavior lives in `commands/`, `docs/adoption-workflow.md`, and the
bundled workflow references. Claude Code now supports plugin marketplaces for
versioned distribution of skills, with plugin manifests at
`agent-skills/.claude-plugin/plugin.json` and marketplace catalogs named
.claude-plugin/marketplace.json inside marketplace repositories.

Shipping only direct-copy Claude skill instructions would keep the package
portable, but it would make team installation, version pinning, and updates
manual. Shipping a Claude plugin should not change the source-of-truth model or
turn the kit into an automated rewrite tool.

## Decision

Add Claude Code plugin metadata to the existing `agent-skills/` package and
publish it through the same public Harnessworks marketplace repository used for
the Codex package.

The Claude release path is:

1. update `agent-skills/.claude-plugin/plugin.json`
2. validate the package with `scripts/check_agent_skills_package.py`
3. validate the plugin with `claude plugin validate agent-skills` when Claude
   Code is available
4. copy the released package into the marketplace repository
5. publish the Claude marketplace catalog with a relative plugin source
6. tag and release the marketplace repository

Claude plugin installs use namespaced skill invocation such as
`/harness-agent-skills:harness doctor`. Direct skill installs can still use
`/harness doctor`.

## Rationale

- A Claude plugin marketplace gives Claude Code users the same install and
  update ergonomics that Codex users get from the Codex marketplace.
- Keeping both runtime manifests in `agent-skills/` avoids forking the skill
  body and bundled references.
- Namespaced Claude plugin commands prevent conflicts with project-local
  skills while preserving the direct-copy `/harness ...` path.
- Requiring both repository validation and Claude's own validator catches drift
  between prompt-first package content and runtime packaging metadata.

## Consequences

- Changes to `agent-skills/.claude-plugin/plugin.json` are release-affecting.
- Release notes must distinguish direct Claude skill invocation from Claude
  plugin invocation.
- Marketplace release automation or docs should keep Codex root
  marketplace JSON and the Claude marketplace catalog in the same repository
  intentionally aligned.
- The community marketplace submission path remains optional and review-gated;
  the first public release is the Harnessworks GitHub marketplace source.

# Universal Agent Skills Package

The Universal Agent Skills package exposes Harness Starter Kit workflows as
portable Agent Skills for Codex and Claude Code.

The package lives in [`agent-skills/`](../agent-skills/) and contains:

- [`agent-skills/skills/harness/SKILL.md`](../agent-skills/skills/harness/SKILL.md)
  as the `/harness ...` router
- shortcut skills for adopt, doctor, update, refresh, and review workflows
- [`agent-skills/references/`](../agent-skills/references/) with bundled
  fallback workflow references
- [`agent-skills/.codex-plugin/plugin.json`](../agent-skills/.codex-plugin/plugin.json)
  for Codex plugin packaging

## Design Contract

The skills are adapters over the repository workflow docs:

- target repositories remain the source of truth
- prompt-first adoption remains the default model
- canonical command docs remain under [`commands/`](../commands/)
- standalone skill installs use bundled references only when the target does
  not contain a local `./harness-starter-kit` clone

This keeps the package useful in Codex and Claude Code without turning the kit
into a one-command rewrite tool.

## Codex Usage

Codex can use the package either as direct skills or as a plugin-compatible
bundle. For repo-local direct skills, copy the skills and references into the
repository's agent configuration directory:

```bash
mkdir -p .agents/skills .agents/references
cp -R agent-skills/skills/* .agents/skills/
cp -R agent-skills/references/* .agents/references/
```

For user-level direct skills, copy the same two directories under the user's
agent configuration directory:

```bash
mkdir -p ~/.agents/skills ~/.agents/references
cp -R agent-skills/skills/* ~/.agents/skills/
cp -R agent-skills/references/* ~/.agents/references/
```

For Codex plugin packaging, use [`agent-skills/`](../agent-skills/) as the
plugin root. The manifest at
[`agent-skills/.codex-plugin/plugin.json`](../agent-skills/.codex-plugin/plugin.json)
points Codex at the packaged skills directory.

To test the package through a local Codex marketplace without committing
workspace-specific config, copy the plugin into a temporary marketplace root and
register that root with Codex:

```bash
MARKETPLACE_ROOT=/tmp/harness-agent-skills-marketplace
rm -rf "$MARKETPLACE_ROOT"
mkdir -p "$MARKETPLACE_ROOT/plugins"
cp -R agent-skills "$MARKETPLACE_ROOT/plugins/harness-agent-skills"
cat > "$MARKETPLACE_ROOT/marketplace.json" <<'JSON'
{
  "name": "harness-starter-kit-local",
  "interface": {
    "displayName": "Harness Starter Kit Local"
  },
  "plugins": [
    {
      "name": "harness-agent-skills",
      "source": {
        "source": "local",
        "path": "./plugins/harness-agent-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
JSON
codex plugin marketplace add "$MARKETPLACE_ROOT"
```

After registering the marketplace, restart Codex and install
`harness-agent-skills` from the plugin directory. When iterating locally, copy
the updated `agent-skills/` directory into the marketplace plugin path again and
restart Codex so the updated package is discovered.

## Claude Code Usage

Claude Code uses the same `SKILL.md` files. For a repo-local install, copy the
skills and references into the repository's Claude configuration directory:

```bash
mkdir -p .claude/skills .claude/references
cp -R agent-skills/skills/* .claude/skills/
cp -R agent-skills/references/* .claude/references/
```

For user-level use, copy the same two directories under the user's Claude
configuration directory:

```bash
mkdir -p ~/.claude/skills ~/.claude/references
cp -R agent-skills/skills/* ~/.claude/skills/
cp -R agent-skills/references/* ~/.claude/references/
```

The `harness` skill is the router, so users can invoke it with a subcommand
such as `/harness doctor` in Claude Code. The shortcut skills are available for
runtimes or teams that prefer one command per workflow.

## Validation

Run the package drift check after changing skills, skill references, plugin
metadata, or installation guidance:

```bash
python3 scripts/check_agent_skills_package.py
```

The check validates skill frontmatter, Codex metadata, plugin manifest fields,
reference coverage, router coverage, and documentation wiring.

---
name: harness-adopt
description: Apply Harness Starter Kit prompt-first adoption to a target repository. Use when the user asks to apply, install, adopt, or bootstrap repository harness guidance, checks, memory, and adoption reporting.
argument-hint: "[target details]"
---

# Harness Adopt

Apply harness engineering to the current target repository.

## Steps

1. Read `../../references/package-contract.md`.
2. Read `../../references/adopt-workflow.md`.
3. If `./harness-starter-kit/docs/adoption-workflow.md` exists in the target,
   prefer that canonical workflow.
4. Inspect the target repository before editing.
5. Add or update only the smallest useful harness artifacts that fit the
   target's existing architecture, tools, docs, commands, and conventions.
6. Run relevant local checks.
7. Finish with an adoption report, including task outcome evidence status for
   substantial harness work.

## Boundaries

- Do not blindly copy templates.
- Do not replace existing target docs or config wholesale.
- Do not add CI, pre-commit hooks, dependencies, or package scripts unless
  they match the target's existing workflow.
- Treat a nested `./harness-starter-kit` clone as read-only reference material.

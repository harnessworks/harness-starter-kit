# Stack Profiles

Profiles are conservative stack-specific reference snippets for target
repositories. They are not automatic migrations and should not replace the
target repository's architecture, package manager, docs, commands, or
conventions.

Available profiles:

- `generic`
- `python`
- `typescript`
- `nextjs`
- `django`
- `flask`
- `fastapi`
- `spring`
- `android`
- `react`
- `vue`
- `go`
- `rust`

## How Agents Use Profiles

During prompt-first adoption, agents read profile templates from a local kit
clone:

```text
harness-starter-kit/templates/profiles/<profile>/
```

When the optional installer copies profile snippets, it places them under the
target repository for review:

```text
docs/harness/profiles/<profile>/
```

In both cases, profile snippets are reference material. Agents should adopt,
adapt, skip, or defer each snippet based on the target repository's existing
tools and maintenance expectations.

## What Profiles May Contain

A profile may include:

- `README.md` guidance for the stack
- `check_harness.py` or another suggested local verification entrypoint
- merge-only config snippets such as `pyproject.harness.toml`,
  `package-scripts.harness.json`, `eslint.config.harness.mjs`, or
  `pre-commit-config.harness.yaml`
- `gitignore.harness.txt` entries for generated files, dependency directories,
  caches, and local reference clones

Merge-only snippets should be copied into existing target configs only after
review. Do not replace target configs wholesale.

## Profile Absorption

If a repository starts with the generic harness and later gains a real stack,
use [`docs/checklists/profile-absorption.md`](checklists/profile-absorption.md).
That checklist helps decide which snippets should become real commands, config,
ignores, documentation, or checks.

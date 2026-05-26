# Coding Conventions

These conventions apply to the starter kit itself. Templates may still contain
TODO markers because target repositories must fill in their own project-specific
rules.

## Naming

- Use clear file names that describe the installed artifact, such as
  `check_docs_drift.py` or `pyproject.harness.toml`.
- Keep profile-specific files under `templates/profiles/<profile>/`.
- Use `*.harness.*` for snippets that should be merged into an existing target
  config rather than copied over it.

## Error Handling

- Installer failures should stop with a direct message that names the target
  path or invalid option.
- Default behavior must be non-destructive. Existing target files are skipped
  unless `--force` is provided.
- Optional integrations, such as CI workflows, should require an explicit flag
  when they may not fit every target repository.

## Testing

- Prefer standard-library `unittest` tests so the kit can be validated without
  installing dependencies.
- Use temporary directories for installer tests and assert both filesystem
  results and user-facing output.
- Add a regression test whenever installer copy rules, overwrite behavior, or
  drift checks change.

## Logging

- Installer output should list one action per destination: `create`,
  `overwrite`, or `skip-existing`.
- Keep summaries short and script-friendly.
- Avoid noisy debug output in generated target repositories.

## Agent Notes

When a convention is repeatedly missed, make it more specific here and add an
automated check where practical.


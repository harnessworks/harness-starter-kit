# 0005. Use Crowdin GitHub Action For README Localization

## Status

Accepted

## Context

The repository already maintains localized README files:

- `README.ko.md`
- `README.ja.md`
- `README.zh-CN.md`

Manual translation updates are easy to miss when `README.md` changes. A custom
translation bot would add more code, credentials, and review surface than this
kit needs. Crowdin is the chosen localization system, and the workflow should
stay small enough to preserve the kit's prompt-first approach.

## Decision

Use the official Crowdin GitHub Action v2 with a checked-in `crowdin.yml`
configuration.

The workflow uploads `README.md` to Crowdin, downloads translated README files,
and opens a pull request from a dedicated localization branch. It runs on
`main` pushes that affect README localization setup and on manual
`workflow_dispatch`. It does not run on pull request events.

Crowdin credentials are provided through repository secrets:

- `CROWDIN_PROJECT_ID`
- `CROWDIN_PERSONAL_TOKEN`

If those secrets are absent, the workflow exits successfully after emitting a
notice instead of breaking unrelated repository checks.

## Rationale

- The official action avoids maintaining a custom translation bot.
- A checked-in `crowdin.yml` makes source and translation paths reviewable.
- Avoiding pull request triggers keeps Crowdin secrets away from fork PRs.
- Secret-gating lets the workflow land before the Crowdin project is fully
  configured.
- Translation changes still arrive as pull requests, so maintainers can review
  generated Markdown before merge.

## Alternatives Considered

- Custom GitHub Action plus translation API: rejected because it would require
  bespoke bot logic, provider-specific API handling, and more failure modes.
- Crowdin native GitHub integration: rejected for now because this repository
  can express the synchronization behavior directly in versioned workflow code.
- Manual-only translation updates: rejected because README changes can drift
  from localized versions without a durable feedback loop.

## Agent Guidance

When changing README localization behavior, keep `crowdin.yml`,
`.github/workflows/crowdin-sync.yml`, `.github/PULL_REQUEST_TEMPLATE.md`,
`docs/validation.md`, and `tests/test_repository_hygiene.py` aligned.

Do not add pull request triggers to the Crowdin workflow unless the workflow
continues to avoid checking out or executing untrusted PR code and the secret
exposure model is explicitly reviewed.

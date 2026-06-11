# 0009. README Language Switcher Drift Missed Traditional Chinese

## Date Observed

2026-06-11

## Failure Type

Failed harness check and documentation localization drift.

## Goal

README language-switcher tests should cover every localized README in the
repository. Adding a new localized README should not require duplicating the
same hardcoded language list across UTF-8, prompt-drift, and switcher tests.

## What Happened Or Was Tried

`README.zh-TW.md` existed and every README language switcher linked to it, but
`tests/test_readme_prompt_drift.py` still listed only Korean, Japanese, and
Simplified Chinese README files. The same test also hardcoded four expected
language-switcher strings that omitted the Traditional Chinese link.

Running `python3 -m unittest discover -s tests` failed four
`test_language_switcher_highlights_only_current_language` assertions. The
`Harness Check` GitHub Actions workflow runs the same full unittest command, so
the drift would block pull-request validation.

## Why It Failed

- Failed check or CI failure: the committed test expectations no longer matched
  the localized README files in the repository.
- The language list was duplicated in the test instead of being derived from
  the current README files.
- The UTF-8 and prompt-drift checks did not include `README.zh-TW.md`, so they
  would miss future Traditional Chinese prompt or encoding drift.

## Current Replacement

`tests/test_readme_prompt_drift.py` now discovers `README*.md` files, derives
the localized README set from the filesystem, parses each language switcher,
and checks that all switchers share the same label order, link every other
README, and highlight exactly one current language. The prompt-drift and UTF-8
checks use the same discovered localized README set.

## Detection Or Prevention Check

`python3 -m unittest tests.test_readme_prompt_drift` catches recurrence for
localized README prompt drift and language-switcher drift. The broader
`python3 -m unittest discover -s tests` gate also catches it, and the
`.github/workflows/harness-check.yml` `Run unit tests` step runs that command
for pull requests.

## Agent Guidance

When adding, removing, or renaming a localized README, run
`python3 -m unittest tests.test_readme_prompt_drift` before finishing. Do not
reintroduce per-language expected switcher strings in the test; keep the
language set derived from repository files so new README localizations are
covered automatically.

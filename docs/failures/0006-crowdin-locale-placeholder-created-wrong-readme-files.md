# 0006. Crowdin Locale Placeholder Created Wrong README Files

## Date Observed

2026-06-03

## Failure Type

Cross-environment mismatch and automation bug path.

## Goal

Crowdin synchronization should update the repository's existing localized README
files:

- `README.ko.md`
- `README.ja.md`
- `README.zh-CN.md`

It should not create alternate locale-named files that bypass the README
language switcher and existing drift tests.

## What Happened Or Was Tried

The initial Crowdin configuration used `README.%locale%.md` as the translation
target. The first successful Crowdin GitHub Action run downloaded translations
to `README.ja-JP.md`, `README.ko-KR.md`, and `README.zh-CN.md`, then opened a
translation pull request from `l10n_crowdin_readme`.

The generated PR was closed because it introduced new Japanese and Korean file
names instead of updating `README.ja.md` and `README.ko.md`.

## Why It Failed

- Crowdin's `%locale%` placeholder expanded Japanese and Korean to regional
  locale codes.
- The repository's public README switcher and tests use shorter Japanese and
  Korean filenames.
- The mismatch was only visible after the live Crowdin sync ran against the
  configured project languages.

## Current Replacement

`crowdin.yml` now uses the `two_letters_code` placeholder and maps Chinese
Simplified back to `zh-CN`. This keeps Korean and Japanese as `ko` and `ja`
while preserving the existing Chinese Simplified filename.

Regression coverage lives in `tests/test_repository_hygiene.py`.

## Detection Or Prevention Check

`tests/test_repository_hygiene.py` checks that `crowdin.yml` uses
`README.%two_letters_code%.md`, includes `languages_mapping`, maps `zh-CN` to
`zh-CN`, and documents the expected localized README filenames in
`docs/validation.md`. The `Harness Check` CI gate runs this test suite before
merge.

## Agent Guidance

Do not switch README localization back to `%locale%` unless the repository also
renames the localized README files, updates every language switcher, and adjusts
the README drift tests. After changing Crowdin language mapping, run the
Crowdin workflow once and inspect the generated PR file list before merging any
translation output.

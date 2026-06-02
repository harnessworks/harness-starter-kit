# Profile Maintenance Checklist

Use this checklist when adding or changing files under `templates/profiles/`.

## 1. Start From The Contract

- [ ] For a new profile, start from `docs/templates/profile-readme.md`.
- [ ] Keep profile files as reference material, not automatic transformations.
- [ ] Preserve the target repository as the source of truth in the wording.

## 2. Keep Guidance Conditional

- [ ] Include `Apply this profile by priority`.
- [ ] Cover the priority model: always protect architecture, generated files,
      local config, and exact checks; when present, document services,
      fixtures, seeds, or local environment setup; when touching an area,
      consider decision records only for meaningful architecture or integration
      changes; for narrow fixes, use a final report or check note.
- [ ] Avoid making broad feature planning, ADRs, server verification, or
      encoding audits sound mandatory for every small change.

## 3. Maintain Shared Phrases

- [ ] Include `Consider a decision record`.
- [ ] Include `narrow fix`.
- [ ] Include `final report or check note`.
- [ ] Include a final-report sentence that asks agents to list snippets adopted,
      adapted, skipped, or deferred.
- [ ] When a profile suggests a `check_harness.py` or `check:harness` command,
      keep the checked axes discoverable so it is clear whether the command is
      validating lint, typecheck, build, docs drift, structure drift, server
      smoke, or API smoke behavior.

## 4. Avoid Regressions

- [ ] Do not reintroduce `Add a decision record when choosing`.
- [ ] Do not reintroduce `Before feature implementation`.
- [ ] Do not reintroduce `scenario test plan` when `scenario test note` is
      sufficient.
- [ ] Update `tests/test_profile_consistency.py` when the profile contract
      intentionally changes.

## 5. Validate

On macOS/Linux, use `python3` instead of `python` when `python` is unavailable.

```powershell
python -m unittest tests.test_profile_consistency
python -m unittest discover -s tests
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
```

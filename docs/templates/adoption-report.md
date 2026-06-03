# Adoption Report

## Target Repository Observed

- Stack and framework: TODO
- Package manager and commands: TODO
- Local server, fixture, seed data, emulator, or device dependencies: TODO
- Existing docs or agent instructions: TODO
- CI or verification path: TODO
- Monorepo or special layout: TODO

## Files Added Or Changed

- `AGENTS.md`: TODO
- `docs/`: TODO
- `scripts/`: TODO

## Existing Structures Reused

- TODO: list README, CONTRIBUTING, CI, docs, package scripts, or lint/test tools
  that were reused instead of duplicated.

## Checks Run

```powershell
TODO: command
```

Result: TODO

## Verification Gate Placement

- Normal completion gate: TODO: command, package script, CI workflow,
  `scripts/check_harness.py`, or other documented default verification path.
- Deterministic behavior checks included in the normal gate: TODO: list local,
  non-network, reasonably fast checks for product behavior, or explain why none
  were added.
- Focused or manual checks outside the normal gate: TODO: list live API,
  credential, quota, provider-uptime, visual, device, slow, watcher, or other
  checks kept separate.
- Reasons for focused/manual placement: TODO: explain why each separated check
  is not safe, stable, fast, or expected in normal verification.

## Server Or Fixture Verification

- Required: TODO: yes/no and why.
- How to run: TODO: command, working directory, ports, seed data, or fixture
  setup.
- Verification performed: TODO: endpoint, log line, smoke test, emulator/device
  check, or reason it was not run.
- Not applicable: TODO: explain when the target has no local server, fixture,
  seed, emulator, or device dependency.

## External API Verification

- Required: TODO: yes/no and why.
- Boundary: TODO: server-only caller, route handler, service module, fixture, or
  mock boundary reviewed.
- Provider boundary fixture: TODO: fixture/test path, provider contract axes
  covered, or reason no fixture was practical.
- Endpoint parameter contract: TODO: required query parameters, casing,
  date/time format, coordinate fields, service-key placement, or not
  applicable.
- Live/mock mode: TODO: live, mock, fixture, disabled, or not applicable.
- Secret handling and redaction checked: TODO: env vars, request URL, headers,
  logs, screenshots, and reports reviewed without exposing values.
- Empty or zero-result behavior: TODO: verified, covered by fixture/test, not
  applicable, or not run with reason.
- Provider error handling: TODO: HTTP error, provider error envelope, mixed
  JSON/XML/text response, or not applicable.
- Focused smoke command or fixture: TODO: command, endpoint, fixture path, or
  reason build/typecheck was enough.

## Feature Scenario Test Note

- Broad feature work: TODO: yes/no and why.
- Build-only validation is enough: TODO: yes/no and why.
- Scenarios covered for broad feature work: TODO: list user flows, API/server
  state, automated checks, and manual checks. For narrow fixes, name the
  relevant check instead.
- Manual or hardware-dependent checks: TODO: emulator/device, permissions, NFC,
  Bluetooth, beacon, camera, location, or other caveats.

## Failure Memory

- Recorded: TODO: list `docs/failures/...` records added while fixing
  user-visible runtime failures, high-risk bug paths, failed checks, CI
  failures, repeated agent mistakes, or cross-environment mismatches.
- Detection or prevention check: TODO: regression test, fixture, smoke check,
  lint rule, drift check, CI gate, manual review point, or reason no check is
  practical.
- Skipped: TODO: explain why no failure note was needed, such as purely
  transient behavior or coverage by an existing failure note.

## Documentation Updated

- `README.md`: TODO
- `AGENTS.md`: TODO
- `docs/conventions/coding.md`: TODO
- `docs/decisions/`: TODO
- Behavior or integration decisions considered: TODO: explain whether user
  workflow, input contract, input semantics, state normalization, API
  request/response shape, fallback policy, displayed decision criteria, or
  integration behavior changed.
- Decision memory result: TODO: ADR added/updated, existing ADR cited, or no ADR
  needed with reason.
- Not updated: TODO: explain why if this adoption or change did not require a
  durable docs update.

## Profile Absorption

- Profile reviewed: TODO
- Snippets adopted: TODO
- Snippets adapted: TODO
- Snippets skipped or deferred: TODO

## Drift Checks Added

- Baseline doc or structure hygiene checks: TODO
- Encoding or localization hygiene checks: TODO
- Target-specific architecture checks: TODO
- Not added: TODO: explain why if no target-specific drift check was practical.

## Effectiveness Measurement Plan

Do not leave this section as TODO. If measurement is not possible yet, explain
why and define the next observable event.

- Baseline available: TODO
- Comparable tasks to repeat or track: TODO
- Primary metric: TODO
- Review window: TODO
- Results location: TODO
- Task outcome records location: TODO: usually docs/effectiveness/task-outcomes/

## Assumptions

- TODO

## Remaining Manual Steps

- Decide whether the local `harness-starter-kit/` clone should be removed,
  ignored, or kept intentionally as a submodule/reference before committing.
- TODO

## Notes For Future Agents

- TODO

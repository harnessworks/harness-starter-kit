# 0004. Deterministic Behavior Check Remained Focused Without Gate-Placement Review

## Date Observed

2026-06-02

## Failure Type

Repeated agent mistake and harness maintenance gap.

## Goal

When a target repository adds a deterministic, local, non-network, reasonably
fast check for product behavior that agents are expected to verify repeatedly,
the harness should review whether that check belongs in the
documented normal completion gate. If the check remains focused or manual, the
reason should be recorded.

## What Happened Or Was Tried

During TodayBus dogfood work, `npm run test:planner` verified deterministic
planner fallback behavior. The same adoption record also kept live API smoke
commands outside the default `check:harness` gate because they depended on
credentials, network state, quota, and public-data provider availability.

The deterministic planner test was initially grouped with focused smoke
commands instead of being reviewed separately as a normal-gate candidate.

## Why It Failed

- The existing verification guidance clearly warned against putting unstable
  live API smoke checks into the normal gate.
- It did not state the complementary rule: deterministic, local, non-network,
  reasonably fast checks for product behavior should be reviewed for inclusion
  in the normal completion gate.
- Adoption and report templates asked which checks ran, but did not ask which
  checks were normal gate checks versus focused or manual checks.
- Harness refresh and review guidance could find unused checks, but did not
  challenge important deterministic behavior checks left outside the normal
  gate without a reason.

## Current Replacement

Adoption, review, refresh, generic `AGENTS.md`, verification checklist, adoption
report, maintenance checklist, and lifecycle dogfood documentation now require a
gate-placement review:

- deterministic, local, non-network, reasonably fast checks for product
  behavior that agents are expected to verify repeatedly should be included in
  the documented normal completion gate, or have a documented reason for
  remaining focused or manual
- live API, credential, quota, provider-uptime, visual, device, slow, watcher,
  or otherwise fragile checks should stay outside the normal gate when they are
  unsafe as default verification
- the normal gate must be named by the target repository's actual workflow, not
  assumed to be `check:harness`

Regression coverage lives in `tests/test_repository_hygiene.py`.

## Detection Or Prevention Check

`tests/test_repository_hygiene.py` verifies that adoption, review, refresh,
generic agent instructions, verification checklist, adoption reports, examples,
and lifecycle documentation all require gate-placement review for deterministic,
local, non-network, reasonably fast product-behavior checks.

## Agent Guidance

Do not treat all focused checks alike. When a new check is deterministic, local,
non-network, reasonably fast, and protects product behavior that agents should
verify repeatedly, review whether it belongs in the normal completion gate. If
it stays focused or manual, record the reason. Keep genuinely live, slow,
credentialed, device-dependent, visual, watcher, or provider-uptime-sensitive
checks separate unless the target repository intentionally expects them in
normal verification.

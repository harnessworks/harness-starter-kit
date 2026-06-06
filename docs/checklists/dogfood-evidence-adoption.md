# Dogfood Evidence Adoption Checklist

Use this checklist before adding a target repository as a dogfood report,
README badge, lifecycle result, validation note, or effectiveness example in
this kit.

Dogfood evidence should make the kit easier to evaluate. It should not turn a
single target run into an unsupported effectiveness claim.

## Required Before Adoption

- Source tracking exists and names the kit source, commit, applied profile, and
  adoption or setup context, usually in `.harness/source.json`.
- The target repository commit or PR being cited is stable and linkable.
- The report separates non-comparable setup work from comparable product-task
  outcomes.
- Each counted product task has a task outcome record with repository ref,
  prompt ref or prompt hash, expected boundary, known failure mode, files
  changed, first-pass verification, final verification, and inclusion flags.
- The target normal completion gate is named from the target's real workflow.
- Deterministic, local, non-network, reasonably fast behavior checks are either
  included in that normal gate or have a recorded reason for focused/manual
  placement.
- Live API, credential, provider-uptime, visual, device, slow, watcher, or
  otherwise fragile checks are kept outside the normal gate unless the target
  intentionally expects them in normal verification.
- Failure records exist for non-transient failed setup checks, failed harness
  checks, recurring agent mistakes, cross-environment mismatches, or high-risk
  bug paths that should not recur.
- Each failure record names a regression test, fixture, smoke check, lint rule,
  drift check, CI gate, or manual review point that detects or prevents
  recurrence, or explains why no check is practical.
- Aggregate reports state clearly whether the evidence is baseline-vs-harnessed
  or harnessed-only tracking.
- Harnessed-only reports explicitly say they do not prove effectiveness
  improvement without a later comparison point.

## Required Checks

Run the target's normal gate and this kit's report validators before adopting
the evidence:

```bash
python scripts/check_harness.py
python /path/to/harness-starter-kit/scripts/check_effectiveness_plan.py
python /path/to/harness-starter-kit/scripts/check_failure_memory.py
```

Use the target's real normal gate if it is not `python scripts/check_harness.py`.
For JavaScript targets, this might be `npm run check:harness`; for framework
targets, it might be `make test`, `just check`, Maven, Gradle, Django, or
another local command.

## Reject Or Defer Adoption When

- The evidence relies on local-only paths without stable repository refs or
  prompt hashes.
- Setup failures are excluded from metrics but not evaluated for failure
  memory.
- A template or placeholder task outcome is included in the effectiveness report
  or comparable product-task count.
- The aggregate report says product tasks are complete while also saying no
  product-task records are complete.
- The report uses Harness Doctor, passing checks, or fixture tests as proof of
  agent effectiveness.
- The target adopted starter-kit defaults blindly instead of preserving its own
  architecture, package manager, docs, commands, and conventions.
- The example would require copying target-specific architecture into generic
  templates.

## Report Placement

Use the smallest durable placement that fits the evidence:

- `docs/examples/effectiveness-report-<target>-dogfood.md` for an aggregate
  dogfood report.
- `docs/examples/lifecycle-pilot-results.md` for a short lifecycle or dogfood
  summary.
- `docs/evaluation.md` for the example index.
- `docs/validation.md` when the target is used as validation or dogfood
  evidence.
- README badges only when the target repository is public and intentionally
  maintained as dogfood evidence.

## Review Questions

- Does the report preserve the target repository as the source of truth?
- Does it count only comparable product-task outcomes?
- Does it name the target's real normal gate and gate-placement decisions?
- Does it record misses honestly, including wrong-file edits and failed first
  verification?
- Does it link failure memory to detection or prevention?
- Does it avoid claiming improvement unless there is a comparable baseline or
  later comparison window?

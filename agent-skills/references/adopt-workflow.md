# Harness Adoption Workflow

Use this when applying Harness Starter Kit patterns to a target repository.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect the target before editing:
   - README, AGENTS, CLAUDE, contributing docs, package manifests, CI configs
   - source layout, test commands, lint/type/build commands, generated outputs
   - existing architecture, domain, decision, failure, and convention docs
3. Reuse existing harness pieces instead of creating parallel structures.
4. Add or update the smallest useful set of durable artifacts:
   - agent instructions
   - knowledge store
   - drift checks or local verification scripts
   - CI or pre-commit wiring only when it matches existing project practice
   - adoption report
5. Add stack profile snippets only as reference material. Do not replace target
   configs wholesale.
6. If the target depends on local servers, database seeds, Docker services,
   emulators, external APIs, auth providers, webhooks, devices, or hardware,
   document the verification setup and live/mock fallback.
7. For changes that alter workflow, input semantics, state normalization, API
   shape, fallback policy, permissions, networking, persistence, or displayed
   decision criteria, add or cite decision memory, or explain why none is
   needed.
8. If the adoption fixes a recurring or high-risk bug path, add failure memory
   with a concrete detection or prevention check.
9. Run relevant checks.
10. Finish with an adoption report.

## Minimum Useful Adoption

For a small repository, prefer:

- `AGENTS.md` or an update to existing agent instructions
- `docs/decisions/000-template.md`
- `docs/failures/000-template.md`
- lightweight drift checks under `scripts/`
- an adoption report that names changed files, checks run, assumptions,
  manual steps, failure memory, effectiveness measurement, gate placement, and
  whether a nested kit clone should be removed, ignored, or kept intentionally

## Report Shape

Include:

- repository shape observed
- existing docs/configs reused
- files changed
- snippets adopted, skipped, or deferred
- checks run and results
- normal completion gate versus focused/manual checks
- assumptions and remaining manual steps
- failure memory recorded or skipped with reason
- effectiveness measurement plan
- nested `harness-starter-kit/` handling before commit

# Initial Adoption Checklist

Use this checklist after copying the starter kit into a target repository.

- [ ] `AGENTS.md` names the project, stack, commands, and completion criteria.
- [ ] `AGENTS.md` includes important forbidden actions.
- [ ] Existing test and lint commands are documented.
- [ ] `docs/decisions/` has at least one real decision or the template.
- [ ] `docs/failures/` has at least one rejected approach or the template.
- [ ] `docs/conventions/` captures project-specific style beyond formatter
      defaults.
- [ ] `docs/domain/` captures business terms or invariants when relevant.
- [ ] Drift scripts run locally.
- [ ] CI or pre-commit runs the stable checks.
- [ ] If the first real stack or app has been introduced, run
      `docs/checklists/profile-absorption.md`.
- [ ] The final adoption report lists remaining manual integration steps.
- [ ] The final adoption report includes an effectiveness measurement plan with
      baseline status, comparable tasks, primary metric, review window, and
      results location.
- [ ] If the adoption report is saved as a file,
      `scripts/check_effectiveness_plan.py --require-report` passes.

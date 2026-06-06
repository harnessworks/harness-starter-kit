# Harness ERP Spring/Maven Dogfood Benchmark

## Target

- Repository: [baskduf/harness-erp](https://github.com/baskduf/harness-erp)
- Evidence commit:
  [`0192d962961427a49c20210b5692aa76ac96d6bd`](https://github.com/baskduf/harness-erp/commit/0192d962961427a49c20210b5692aa76ac96d6bd)
- Backend follow-up evidence commit:
  [`eeb6c74f8e13320207db0827781987aee22bce77`](https://github.com/baskduf/harness-erp/commit/eeb6c74f8e13320207db0827781987aee22bce77)
- Initial benchmark evidence commit:
  [`ef34c12517158da62032a33bb93e318c0418b6f7`](https://github.com/baskduf/harness-erp/commit/ef34c12517158da62032a33bb93e318c0418b6f7)
- Stack and framework: Java 21, Spring Boot 4.0.6, Maven wrapper, H2, vanilla
  HTML/CSS/JavaScript static resources
- Evaluation window: 2026-06-06 dogfood benchmark, backend follow-up benchmark,
  and frontend follow-up benchmark
- Agent or model: Codex in Codex desktop
- Evaluation mode: harnessed-only initial benchmark plus separate backend and
  frontend follow-up benchmarks
- Harness source at final evidence commit:
  [`387dbfabda3d63975494bdabfc812ddf64100919`](https://github.com/baskduf/harness-starter-kit/commit/387dbfabda3d63975494bdabfc812ddf64100919)

This report records Spring/Maven backend and vanilla frontend dogfood evidence
for harness adoption, source tracking, task outcome records, failure memory,
gate placement, boundary tracking, frontend API coverage, browser smoke
verification, and CI-backed local harness verification. It does not prove that
harness adoption improved agent effectiveness because no pre-harness baseline
exists.

## Scope

This report keeps three comparable product-task groups separate:

- `harness-erp-initial-benchmark`: ERP-001 through ERP-005
- `harness-erp-follow-up-benchmark`: ERP-006 through ERP-009
- `harness-erp-frontend-follow-up`: FE-001 through FE-005

The backend follow-up and frontend follow-up groups are useful additional
dogfood evidence, but they are not merged into the ERP-001 through ERP-005
initial benchmark aggregate.

Excluded non-comparable runs:

- `setup-2026-06-06`
- `harness-update-2026-06-06`
- `MAINT-001-ci-verification`
- `MAINT-002-frontend-design-baseline`

Reason for exclusion: setup and harness-update work established or refreshed
the target harness, MAINT-001 added CI verification for the local harness gate,
and MAINT-002 added the legacy ERP frontend design baseline before measurable
frontend implementation. These runs are useful operational evidence, but they
are not comparable product-task outcomes.

## Task Set

### Initial Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `ERP-001` | Add employee search by name. | Employee controller, service, repository, DTOs, tests, task outcome, effectiveness report. | Query logic added without a service test. |
| `ERP-002` | Add purchase request amount validation. | Purchase request DTO/service/controller paths, tests, task outcome, effectiveness report. | Validation exists only at the controller boundary. |
| `ERP-003` | Add approval comment. | Approval DTOs, approval service behavior, approval entity, approval response DTO, approval tests, task outcome, effectiveness report. | Comment is returned but not persisted. |
| `ERP-004` | Add department field to employees. | Employee entity, DTOs, service, controller, employee tests, optional glossary, task outcome, effectiveness report. | Field missing from list/search response. |
| `ERP-005` | Add role-based access policy as documented behavior. | Decision record, role type, access-policy class, policy tests, optional glossary/AGENTS, task outcome, effectiveness report. | Security behavior claimed without tests or explicit deferral. |

### Backend Follow-Up Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `ERP-006` | Enforce service-layer role policy. | Existing role/policy code, employee/purchase/approval services and controllers, focused tests, optional glossary/decision update, task outcome, effectiveness report. | Policy service exists but is not called by business services. |
| `ERP-007` | Add purchase request filtering. | Purchase request repository, service, controller, DTOs if needed, focused tests, optional glossary, task outcome, effectiveness report. | Combined filters ignore one of the filter fields. |
| `ERP-008` | Add approval history read behavior. | Approval repository, service, controller, DTOs, approval-related tests, optional glossary, task outcome, effectiveness report. | Approval history order is nondeterministic. |
| `ERP-009` | Add employee update behavior. | Employee entity, DTOs, policy code if needed, service, controller, employee tests, optional glossary/decision update, task outcome, effectiveness report. | Employee update can bypass ADMIN policy validation. |

### Frontend Follow-Up Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `FE-001` | Add vanilla frontend shell and shared frontend infrastructure. | Static frontend resources, optional static-resource test, README if needed, task outcome, effectiveness report. | Modern dashboard or landing page replaces the legacy ERP workspace; static files are not served from `/`. |
| `FE-002` | Connect employee management frontend to employee APIs. | Static frontend resources, optional employee static-resource test, README if needed, task outcome, effectiveness report. | Employee forms exist but do not call real APIs; create/update omits `X-ERP-Role`. |
| `FE-003` | Connect purchase request frontend to purchase request APIs. | Static frontend resources, optional purchase request static-resource test, README if needed, task outcome, effectiveness report. | Purchase request controls exist but do not call real APIs; combined filters ignore one field. |
| `FE-004` | Connect approval queue and history frontend to approval APIs. | Static frontend resources, optional approval static-resource test, README if needed, task outcome, effectiveness report. | Approval buttons update UI only; comments are not persisted in history; queue does not refresh after decisions. |
| `FE-005` | Verify full frontend API coverage. | Static frontend resources if gaps are found, optional full coverage static-resource test, README if needed, task outcome, effectiveness report. | One or more README APIs are not reachable from the UI or smoke evidence misses persistence. |

## Results

### Initial Results

| Metric | Baseline | Initial harnessed | Delta |
| --- | --- | --- | --- |
| Product-task outcomes counted | Not available | 5 | Initial benchmark only |
| Wrong-file edits | Not available | 1 in 5 tasks | Inconclusive; no baseline |
| Repeated known mistakes | Not available | 0 observed | Inconclusive; no baseline |
| First-pass verification success | Not available | 5 / 5 | Initial benchmark only |
| Drift violations detected | Not available | 0 observed | Inconclusive; no baseline |
| Human rework minutes | Not available | Unknown | Not measured |
| Reverted files | Not available | 0 observed | Inconclusive; no baseline |

### Backend Follow-Up Results

| Metric | Baseline | Backend follow-up harnessed | Delta |
| --- | --- | --- | --- |
| Product-task outcomes counted | Not available | 4 | Follow-up benchmark only |
| Wrong-file edits | Not available | 0 in 4 tasks | Inconclusive; no baseline |
| Repeated known mistakes | Not available | 0 observed | Inconclusive; no baseline |
| First-pass verification success | Not available | 4 / 4 | Follow-up benchmark only |
| Drift violations detected | Not available | 0 observed | Inconclusive; no baseline |
| Human rework minutes | Not available | Unknown | Not measured |
| Reverted files | Not available | 0 observed | Inconclusive; no baseline |

### Frontend Follow-Up Results

| Metric | Baseline | Frontend follow-up harnessed | Delta |
| --- | --- | --- | --- |
| Product-task outcomes counted | Not available | 5 | Frontend follow-up benchmark only |
| Wrong-file edits | Not available | 0 in 5 tasks | Inconclusive; no baseline |
| Repeated known mistakes | Not available | 0 observed | Inconclusive; no baseline |
| First-pass verification success | Not available | 3 / 5 | Inconclusive; no baseline |
| Drift violations detected | Not available | 0 observed | Inconclusive; no baseline |
| Human rework minutes | Not available | Unknown | Not measured |
| Reverted files | Not available | 0 observed | Inconclusive; no baseline |

## Non-Comparable Runs

| Run | Reason excluded | Use in metrics |
| --- | --- | --- |
| `setup-2026-06-06` | Initial ERP MVP, harness adoption, source tracking, and Spring Boot coordinate correction. | Excluded from comparable product-task count |
| `harness-update-2026-06-06` | Refreshed harness source tracking and added the target-local effectiveness evidence consistency check. | Excluded from comparable product-task count |
| `MAINT-001-ci-verification` | Added GitHub Actions CI that runs `python scripts/check_harness.py` with Java 21. | Excluded from comparable product-task count |
| `MAINT-002-frontend-design-baseline` | Added the legacy ERP frontend design convention before measurable frontend product work. | Excluded from comparable product-task count |

## Run Log

| Condition | Task ID | Run | Verification result | Notes |
| --- | --- | ---: | --- | --- |
| harnessed-only | `setup` | 1 | pass after non-comparable setup fix | Spring Boot parent coordinate was corrected from generated `4.0.6.RELEASE` to resolvable `4.0.6`; failure memory records the check. |
| harnessed-only | `harness-update` | 1 | pass | Refreshed source tracking to starter-kit commit `387dbfabda3d63975494bdabfc812ddf64100919` and added the evidence consistency checker to the local harness gate. |
| harnessed-only | `ERP-001` | 1 | first pass and final pass | Added case-insensitive employee search through the service/repository boundary. |
| harnessed-only | `ERP-002` | 1 | first pass and final pass | Added service-layer positive amount validation. |
| harnessed-only | `ERP-003` | 1 | first pass and final pass | Added persisted approval/rejection comments with blank-to-null normalization. |
| harnessed-only | `ERP-004` | 1 | first pass and final pass | Added required employee department field; fixture-only edits in approval and purchase request tests were counted as a boundary miss. |
| harnessed-only | `ERP-005` | 1 | first pass and final pass | Added documented and tested role access policy while intentionally deferring runtime HTTP security. |
| harnessed-only | `ERP-006` | 1 | first pass and final pass | Enforced the role access policy at service mutating entrypoints; controllers pass a trusted role header, and runtime HTTP security remains deferred. |
| harnessed-only | `ERP-007` | 1 | first pass and final pass | Added repository-backed purchase request filters by employee id, status, and both filters together. |
| harnessed-only | `ERP-008` | 1 | first pass and final pass | Added persisted approval history ordered by creation time and approval id. |
| harnessed-only | `ERP-009` | 1 | first pass and final pass | Added ADMIN-only employee update for name and department. |
| non-comparable-maintenance | `MAINT-001` | 1 | first pass and final pass | Added a GitHub Actions workflow for the local harness gate; this is operational evidence only. |
| non-comparable-maintenance | `MAINT-002` | 1 | first pass and final pass | Added the legacy ERP frontend design baseline before measurable frontend implementation; this is operational evidence only. |
| harnessed-only | `FE-001` | 1 | first pass failed, final pass | Added the vanilla static legacy ERP shell and shared frontend helpers. First verification failed because the initial static-resource test used unavailable `TestRestTemplate`; final verification passed after switching to JDK `HttpClient`. |
| harnessed-only | `FE-002` | 1 | first pass and final pass | Connected Employee Management to real employee APIs with ADMIN mutating role headers and visible status-bar errors. |
| harnessed-only | `FE-003` | 1 | first pass failed, final pass | Connected Purchase Requests to real list, filter, detail, create, and employee lookup APIs. First verification failed on a brittle static test assertion for a wrapped endpoint call; final verification passed after making the assertion behavioral. |
| harnessed-only | `FE-004` | 1 | first pass and final pass | Connected Approval Queue and Approval History to real approval APIs with MANAGER decisions, persisted comments, queue refresh, and visible service errors. |
| harnessed-only | `FE-005` | 1 | first pass and final pass | Added full frontend API coverage evidence and browser-smoke verified every README API from the vanilla frontend. |

## Changed-Files Consistency

| Task ID | Expected boundary | Actual changed files | Wrong-file edit result |
| --- | --- | --- | --- |
| `ERP-001` | Employee controller, service, repository, tests, task outcome, effectiveness report | Employee controller, repository, service, service test, effectiveness report, task outcome | false |
| `ERP-002` | Purchase request DTO/service/controller/entity paths as needed, tests, task outcome, effectiveness report | Create purchase request DTO, purchase request service, service test, effectiveness report, task outcome | false |
| `ERP-003` | Approval controller/domain/DTO/service/test paths, task outcome, effectiveness report | Approval controller, approval entity, approval request/response DTOs, approval service, service test, effectiveness report, task outcome | false |
| `ERP-004` | Employee entity/DTO/service/controller/repository as needed, employee tests, optional glossary, task outcome, effectiveness report | Employee files, employee service test, glossary, effectiveness report, task outcome, plus fixture-only edits in approval and purchase request service tests | true |
| `ERP-005` | Decision record, policy code/tests, optional glossary/AGENTS, task outcome, effectiveness report | AGENTS.md, role policy decision, glossary, `AccessPolicy`, `Role`, `AccessPolicyTest`, effectiveness report, task outcome | false |
| `ERP-006` | Existing role/policy code, employee/purchase/approval services and controllers, focused tests, optional glossary/decision update, task outcome, effectiveness report | Employee, purchase request, and approval services/controllers; focused service policy tests; role policy decision; glossary; effectiveness report; task outcome | false |
| `ERP-007` | Purchase request repository, service, controller, DTOs if needed, focused tests, optional glossary, task outcome, effectiveness report | `PurchaseRequestRepository`, `PurchaseRequestService`, `PurchaseRequestController`, `PurchaseRequestServiceTest`, effectiveness report, task outcome | false |
| `ERP-008` | Approval repository, service, controller, DTOs, approval-related tests, optional glossary, task outcome, effectiveness report | `ApprovalRepository`, `ApprovalService`, `ApprovalController`, `ApprovalServiceTest`, effectiveness report, task outcome | false |
| `ERP-009` | Employee entity, DTOs, policy code if needed, service, controller, employee tests, optional glossary/decision update, task outcome, effectiveness report | `Employee`, `UpdateEmployeeRequest`, `AccessPolicy`, `EmployeeService`, `EmployeeController`, employee and policy tests, role policy decision, glossary, effectiveness report, task outcome | false |
| `MAINT-002` | README, legacy ERP design convention, effectiveness report, MAINT-002 task outcome | target README, target legacy ERP design convention, effectiveness report, task outcome | false |
| `FE-001` | Static frontend resources, optional static-resource test, README if needed, effectiveness report, FE-001 task outcome | README, static `index.html`, `styles.css`, `app.js`, `FrontendShellStaticResourceTest`, effectiveness report, task outcome | false |
| `FE-002` | Static frontend resources, optional employee static-resource test, README if needed, effectiveness report, FE-002 task outcome | README, static resources, `EmployeeFrontendStaticResourceTest`, effectiveness report, task outcome | false |
| `FE-003` | Static frontend resources, optional purchase request static-resource test, README if needed, effectiveness report, FE-003 task outcome | README, static resources, `PurchaseRequestFrontendStaticResourceTest`, effectiveness report, task outcome | false |
| `FE-004` | Static frontend resources, optional approval static-resource test, README if needed, effectiveness report, FE-004 task outcome | README, static resources, `ApprovalFrontendStaticResourceTest`, effectiveness report, task outcome | false |
| `FE-005` | Static frontend resources if gaps are found, optional full coverage static-resource test, README if needed, effectiveness report, FE-005 task outcome | `FullFrontendApiCoverageStaticResourceTest`, effectiveness report, task outcome | false |

## Source Records

- Final evidence commit:
  [`0192d962961427a49c20210b5692aa76ac96d6bd`](https://github.com/baskduf/harness-erp/commit/0192d962961427a49c20210b5692aa76ac96d6bd)
- CI evidence:
  [Harness Verification push run](https://github.com/baskduf/harness-erp/actions/runs/27059370935)
- Adoption and setup evidence:
  - [adoption report](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/harness/adoption-report.md)
  - [Harness Doctor setup baseline](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/harness/harness-doctor-setup.md)
  - [source tracking](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/.harness/source.json)
  - [legacy frontend design convention](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/conventions/legacy-erp-design.md)
- Task outcome records reviewed:
  - [ERP-001 employee search](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-001-employee-search.yaml)
  - [ERP-002 purchase request amount validation](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-002-purchase-request-amount-validation.yaml)
  - [ERP-003 approval comment](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-003-approval-comment.yaml)
  - [ERP-004 employee department field](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-004-employee-department-field.yaml)
  - [ERP-005 role-based access policy](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-005-role-based-access-policy.yaml)
  - [ERP-006 service-layer role policy enforcement](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-006-service-layer-role-policy-enforcement.yaml)
  - [ERP-007 purchase request filtering](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-007-purchase-request-filtering.yaml)
  - [ERP-008 approval history](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-008-approval-history.yaml)
  - [ERP-009 employee update](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/ERP-009-employee-update.yaml)
  - [MAINT-001 CI verification](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/MAINT-001-ci-verification.yaml)
  - [MAINT-002 frontend design baseline](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/MAINT-002-frontend-design-baseline.yaml)
  - [FE-001 vanilla frontend shell](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/FE-001-vanilla-frontend-shell.yaml)
  - [FE-002 employee management frontend](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/FE-002-employee-management-frontend.yaml)
  - [FE-003 purchase request frontend](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/FE-003-purchase-request-frontend.yaml)
  - [FE-004 approval workflow frontend](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/FE-004-approval-workflow-frontend.yaml)
  - [FE-005 full frontend API verification](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/effectiveness/task-outcomes/FE-005-full-frontend-api-verification.yaml)
- Failure memory reviewed:
  - [Spring Boot coordinate resolution](https://github.com/baskduf/harness-erp/blob/0192d962961427a49c20210b5692aa76ac96d6bd/docs/failures/0001-spring-boot-coordinate-resolution.md)
  - `FE-001` and `FE-003` did not create separate target failure notes at this
    evidence commit. The failures are preserved in task outcome records because
    they were deterministic verification-test design failures caught before
    product acceptance, not product runtime regressions. Recurrence is detected
    by the target normal gate `python scripts/check_harness.py` through
    `FrontendShellStaticResourceTest` and
    `PurchaseRequestFrontendStaticResourceTest`. Repeated instances should be
    promoted to target `docs/failures/*.md` records.
- Repository refs compared:
  - setup commit `a1521406f443d3a5a9d2c86bb987658068afafd8`
  - initial evidence commit `ef34c12517158da62032a33bb93e318c0418b6f7`
  - backend follow-up evidence commit `eeb6c74f8e13320207db0827781987aee22bce77`
  - final evidence commit `0192d962961427a49c20210b5692aa76ac96d6bd`
  - FE-001 start ref `0b135f836e8e72c67bf755fb3e5fbb8c865c8ef2`
  - FE-002 start ref `7aefb7ca4b7e96c990edd4f9131c815be46779fa`
  - FE-003 start ref `38a0c44c96bff0d146de1ce03249fa580b1c35f3`
  - FE-004 start ref `4b906d7125e7c3163b455546ced2c7d46b988a8c`
  - FE-005 start ref `2907544e9aab0ddecb545dee5b9336b0a27af953`
- Prompt refs compared: local prompt files from 2026-06-06 with recorded
  SHA-256 hashes in each task outcome record.
- Verification commands compared:
  - `python scripts/check_harness.py`
  - `python /Users/wb/Desktop/harness-starter-kit/scripts/check_effectiveness_plan.py`
  - `python /Users/wb/Desktop/harness-starter-kit/scripts/check_failure_memory.py`
  - `./mvnw spring-boot:run`
  - Browser smoke against the static frontend
  - `curl http://localhost:8080/`
  - `curl http://localhost:8080/app.js`

## Interpretation

### Observed benchmark

The Harness ERP dogfood run now contains fourteen harnessed-only product-task
observations across three task groups. The initial group produced five
completed product tasks; one task, ERP-004, recorded fixture-only edits outside
the strict expected boundary and counted them as a wrong-file edit. The backend
follow-up group produced four completed product tasks, all with first-pass
verification success and no recorded wrong-file edits.

The frontend follow-up group produced five completed product tasks. Three
passed first verification. FE-001 and FE-003 failed first verification because
their initial static-resource tests were too brittle or used an unavailable
test helper, then passed final verification after the tests were corrected.
The frontend records include browser smoke evidence for the legacy ERP shell,
tab navigation, API-backed employee, purchase request, approval, and history
flows, status-bar service errors, and console-error checks.

MAINT-001 added CI verification for the target's local harness gate. MAINT-002
added the frontend design baseline. Both are operational evidence only and are
excluded from comparable product-task counts.

### What improved

No improvement claim is made. This report has no comparable pre-harness
baseline or later baseline-vs-harnessed comparison window.

### What did not improve

Human rework minutes were not measured. The run therefore cannot assess whether
review effort decreased. The benchmark also uses one small Spring Boot target,
so the result does not generalize to larger backend or frontend systems by
itself.

### Confounders or limitations

- This is harnessed-only evidence, not a controlled experiment.
- The setup, harness-update, design-baseline, and CI maintenance runs are
  excluded from product-task metrics.
- The initial backend, backend follow-up, and frontend follow-up groups are
  tracked separately.
- Prompt files were local artifacts; task outcome records preserve prompt
  hashes, but the prompt text is not stored in this kit.
- Runtime HTTP authentication remains intentionally deferred in the target.
  `X-ERP-Role` is only a trusted service-layer role input.
- Browser smoke evidence is recorded in task outcomes, but the kit report does
  not embed screenshots or full prompt text.
- Harness Doctor, passing local checks, and passing CI are target readiness
  signals, not effectiveness evidence.

### Narrow claim

This report establishes Spring/Maven and vanilla frontend dogfood evidence for
source tracking, task outcome completeness, failure-memory linkage, gate
placement, boundary adherence, frontend API coverage, browser-smoke
verification, and CI-backed local harness verification.

It does not prove that harness adoption improved agent effectiveness.

### Human rework interpretation

Human rework is unknown, not 0. Future runs should record reviewer time or
review findings if the project wants to evaluate rework cost.

## Follow-Up

- Next review window: a repeated ERP or frontend task set under a later harness
  revision, or a baseline-vs-harnessed comparison on a similar Spring/Maven
  target.
- Owner or reviewer: maintainer or dogfood reviewer.
- Related decision or failure records: Harness ERP architecture decision,
  role-based access policy decision, Spring Boot coordinate failure record, and
  ERP-001 through ERP-009 plus FE-001 through FE-005 task outcome records.
- Harness changes to make next: collect human review time, qualitative review
  findings, screenshots, or prompt text if the project wants stronger
  reproducibility and rework-cost evidence.

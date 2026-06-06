# Harness ERP Spring/Maven Dogfood Benchmark

## Target

- Repository: [baskduf/harness-erp](https://github.com/baskduf/harness-erp)
- Evidence commit:
  [`eeb6c74f8e13320207db0827781987aee22bce77`](https://github.com/baskduf/harness-erp/commit/eeb6c74f8e13320207db0827781987aee22bce77)
- Initial benchmark evidence commit:
  [`ef34c12517158da62032a33bb93e318c0418b6f7`](https://github.com/baskduf/harness-erp/commit/ef34c12517158da62032a33bb93e318c0418b6f7)
- Stack and framework: Java 21, Spring Boot 4.0.6, Maven wrapper, H2
- Evaluation window: 2026-06-06 dogfood benchmark and follow-up benchmark
- Agent or model: Codex in Codex desktop
- Evaluation mode: harnessed-only initial benchmark plus separate follow-up
  benchmark
- Harness source at final evidence commit:
  [`387dbfabda3d63975494bdabfc812ddf64100919`](https://github.com/baskduf/harness-starter-kit/commit/387dbfabda3d63975494bdabfc812ddf64100919)

This report records Spring/Maven backend dogfood evidence for harness adoption,
source tracking, task outcome records, failure memory, gate placement,
boundary tracking, and follow-up CI verification. It does not prove that
harness adoption improved agent effectiveness because no pre-harness baseline
exists.

## Scope

This report keeps two comparable product-task groups separate:

- `harness-erp-initial-benchmark`: ERP-001 through ERP-005
- `harness-erp-follow-up-benchmark`: ERP-006 through ERP-009

The follow-up group is useful additional dogfood evidence, but it is not merged
into the ERP-001 through ERP-005 initial benchmark aggregate.

Excluded non-comparable runs:

- `setup-2026-06-06`
- `harness-update-2026-06-06`
- `MAINT-001-ci-verification`

Reason for exclusion: setup and harness-update work established or refreshed
the target harness, and MAINT-001 added CI verification for the local harness
gate. These runs are useful operational evidence, but they are not comparable
product-task outcomes.

## Task Set

### Initial Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `ERP-001` | Add employee search by name. | Employee controller, service, repository, DTOs, tests, task outcome, effectiveness report. | Query logic added without a service test. |
| `ERP-002` | Add purchase request amount validation. | Purchase request DTO/service/controller paths, tests, task outcome, effectiveness report. | Validation exists only at the controller boundary. |
| `ERP-003` | Add approval comment. | Approval DTOs, approval service behavior, approval entity, approval response DTO, approval tests, task outcome, effectiveness report. | Comment is returned but not persisted. |
| `ERP-004` | Add department field to employees. | Employee entity, DTOs, service, controller, employee tests, optional glossary, task outcome, effectiveness report. | Field missing from list/search response. |
| `ERP-005` | Add role-based access policy as documented behavior. | Decision record, role type, access-policy class, policy tests, optional glossary/AGENTS, task outcome, effectiveness report. | Security behavior claimed without tests or explicit deferral. |

### Follow-Up Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `ERP-006` | Enforce service-layer role policy. | Existing role/policy code, employee/purchase/approval services and controllers, focused tests, optional glossary/decision update, task outcome, effectiveness report. | Policy service exists but is not called by business services. |
| `ERP-007` | Add purchase request filtering. | Purchase request repository, service, controller, DTOs if needed, focused tests, optional glossary, task outcome, effectiveness report. | Combined filters ignore one of the filter fields. |
| `ERP-008` | Add approval history read behavior. | Approval repository, service, controller, DTOs, approval-related tests, optional glossary, task outcome, effectiveness report. | Approval history order is nondeterministic. |
| `ERP-009` | Add employee update behavior. | Employee entity, DTOs, policy code if needed, service, controller, employee tests, optional glossary/decision update, task outcome, effectiveness report. | Employee update can bypass ADMIN policy validation. |

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

### Follow-Up Results

| Metric | Baseline | Follow-up harnessed | Delta |
| --- | --- | --- | --- |
| Product-task outcomes counted | Not available | 4 | Follow-up benchmark only |
| Wrong-file edits | Not available | 0 in 4 tasks | Inconclusive; no baseline |
| Repeated known mistakes | Not available | 0 observed | Inconclusive; no baseline |
| First-pass verification success | Not available | 4 / 4 | Follow-up benchmark only |
| Drift violations detected | Not available | 0 observed | Inconclusive; no baseline |
| Human rework minutes | Not available | Unknown | Not measured |
| Reverted files | Not available | 0 observed | Inconclusive; no baseline |

## Non-Comparable Runs

| Run | Reason excluded | Use in metrics |
| --- | --- | --- |
| `setup-2026-06-06` | Initial ERP MVP, harness adoption, source tracking, and Spring Boot coordinate correction. | Excluded from comparable product-task count |
| `harness-update-2026-06-06` | Refreshed harness source tracking and added the target-local effectiveness evidence consistency check. | Excluded from comparable product-task count |
| `MAINT-001-ci-verification` | Added GitHub Actions CI that runs `python scripts/check_harness.py` with Java 21. | Excluded from comparable product-task count |

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

## Source Records

- Final evidence commit:
  [`eeb6c74f8e13320207db0827781987aee22bce77`](https://github.com/baskduf/harness-erp/commit/eeb6c74f8e13320207db0827781987aee22bce77)
- CI evidence:
  [Harness Verification push run](https://github.com/baskduf/harness-erp/actions/runs/27056895393)
- Adoption and setup evidence:
  - [adoption report](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/harness/adoption-report.md)
  - [Harness Doctor setup baseline](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/harness/harness-doctor-setup.md)
  - [source tracking](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/.harness/source.json)
- Task outcome records reviewed:
  - [ERP-001 employee search](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-001-employee-search.yaml)
  - [ERP-002 purchase request amount validation](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-002-purchase-request-amount-validation.yaml)
  - [ERP-003 approval comment](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-003-approval-comment.yaml)
  - [ERP-004 employee department field](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-004-employee-department-field.yaml)
  - [ERP-005 role-based access policy](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-005-role-based-access-policy.yaml)
  - [ERP-006 service-layer role policy enforcement](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-006-service-layer-role-policy-enforcement.yaml)
  - [ERP-007 purchase request filtering](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-007-purchase-request-filtering.yaml)
  - [ERP-008 approval history](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-008-approval-history.yaml)
  - [ERP-009 employee update](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/ERP-009-employee-update.yaml)
  - [MAINT-001 CI verification](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/effectiveness/task-outcomes/MAINT-001-ci-verification.yaml)
- Failure memory reviewed:
  - [Spring Boot coordinate resolution](https://github.com/baskduf/harness-erp/blob/eeb6c74f8e13320207db0827781987aee22bce77/docs/failures/0001-spring-boot-coordinate-resolution.md)
- Repository refs compared:
  - setup commit `a1521406f443d3a5a9d2c86bb987658068afafd8`
  - initial evidence commit `ef34c12517158da62032a33bb93e318c0418b6f7`
  - final evidence commit `eeb6c74f8e13320207db0827781987aee22bce77`
  - ERP-006 start ref `88ed8cf90afe14f357b0edb0bb8fd966ce524ecc`
  - ERP-007 start ref `3db120556aca37050ceb5793c5a8153e22a2067f`
  - ERP-008 start ref `27a2c60cc241af9ee1d730e4000348ea8cc45d23`
  - ERP-009 start ref `25971ff51f9d825571902a8dd5a5c762d3018390`
- Prompt refs compared: local prompt files from 2026-06-06 with recorded
  SHA-256 hashes in each task outcome record.
- Verification commands compared:
  - `python scripts/check_harness.py`
  - `python /Users/wb/Desktop/harness-starter-kit/scripts/check_effectiveness_plan.py`
  - `python /Users/wb/Desktop/harness-starter-kit/scripts/check_failure_memory.py`

## Interpretation

### Observed benchmark

The Harness ERP dogfood run now contains nine harnessed-only product-task
observations across two task groups. The initial group produced five completed
product tasks; one task, ERP-004, recorded fixture-only edits outside the
strict expected boundary and counted them as a wrong-file edit. The follow-up
group produced four completed product tasks, all with first-pass verification
success and no recorded wrong-file edits.

MAINT-001 added CI verification for the target's local harness gate. It is
operational evidence only and is excluded from comparable product-task counts.

### What improved

No improvement claim is made. This report has no comparable pre-harness
baseline or later baseline-vs-harnessed comparison window.

### What did not improve

Human rework minutes were not measured. The run therefore cannot assess whether
review effort decreased. The benchmark also uses one small Spring Boot target,
so the result does not generalize to larger backend systems by itself.

### Confounders or limitations

- This is harnessed-only evidence, not a controlled experiment.
- The setup, harness-update, and CI maintenance runs are excluded from
  product-task metrics.
- The initial and follow-up groups are tracked separately.
- Prompt files were local artifacts; task outcome records preserve prompt
  hashes, but the prompt text is not stored in this kit.
- Runtime HTTP authentication remains intentionally deferred in the target.
- Harness Doctor and passing CI are target readiness signals, not
  effectiveness evidence.

### Narrow claim

This report establishes Spring/Maven backend dogfood evidence for source
tracking, task outcome completeness, failure-memory linkage, gate placement,
boundary adherence, follow-up comparable tasks, and CI-backed local harness
verification.

It does not prove that harness adoption improved agent effectiveness.

### Human rework interpretation

Human rework is unknown, not 0. Future runs should record reviewer time or
review findings if the project wants to evaluate rework cost.

## Follow-Up

- Next review window: a repeated ERP task set under a later harness revision or
  a baseline-vs-harnessed comparison on a similar Spring/Maven target.
- Owner or reviewer: maintainer or dogfood reviewer.
- Related decision or failure records: Harness ERP architecture decision,
  role-based access policy decision, Spring Boot coordinate failure record, and
  ERP-001 through ERP-009 task outcome records.
- Harness changes to make next: collect human review time or qualitative
  review findings if the project wants to evaluate rework cost.

# harness-starter-kit

**[English](README.md)** | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

<p align="center">
  <img alt="harness-starter-kit agent session demo" src="site/assets/banner.gif" />
</p>

<p align="center">
  <img alt="Generic profile" src="https://img.shields.io/badge/profile-generic-6b7280?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white" />
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-087EA4?style=flat-square&logo=react&logoColor=white" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" />
  <img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="Spring Boot" src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" />
  <img alt="Android" src="https://img.shields.io/badge/Android-3DDC84?style=flat-square&logo=android&logoColor=white" />
</p>

<p align="center">
  <a href="https://baskduf.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
</p>

상세 운영 문서는 영어 기준으로 유지합니다. 이 README는 빠른 진입점입니다.

## 빠른 시작

대상 저장소를 코딩 에이전트로 열고 아래 prompt를 전달하세요.

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit if it is not already present, read it,
then apply its prompt-first harness engineering workflow to this repository.

Requirements:
- Treat the current working directory as the target repository.
- Treat ./harness-starter-kit as read-only reference material after cloning.
- Inspect this repository before editing.
- Preserve existing architecture, tools, package manager, commands, docs, and
  conventions.
- Do not blindly copy templates.
- Add only the minimum useful harness pieces.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite or delete existing files without explaining why.
- If I ask for /harness doctor, use
  ./harness-starter-kit/commands/harness-doctor.md.
- If I ask for /harness update after adoption, use
  ./harness-starter-kit/commands/harness-update.md to refresh the kit reference,
  record .harness/source.json, and selectively update target harness files
  without blindly overwriting existing files.
- If I ask for /harness refresh after adoption, use
  ./harness-starter-kit/commands/harness-refresh.md to review existing harness
  docs, rules, knowledge records, and checks for stale or duplicated guidance.
  Do not delete, archive, move, or rename files without my explicit approval for
  the specific files.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit
```

전체 prompt와 workflow는
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)와
[`docs/adoption-workflow.md`](docs/adoption-workflow.md)를 보세요.

## 명령

### `/harness doctor`

Harness Doctor는 저장소가 AI 코딩 에이전트와 안정적으로 협업할 준비가 되었는지
평가합니다. Agent Instructions, Feedback Loops, Durable Memory, Structural
Safety, Adoption Clarity를 기준으로 Harness Score를 보고합니다.

- 명령 workflow: [`commands/harness-doctor.md`](commands/harness-doctor.md)
- 채점 rubric: [`docs/scoring/harness-score-rubric.md`](docs/scoring/harness-score-rubric.md)
- 예시 report: [`docs/examples/harness-doctor-report.md`](docs/examples/harness-doctor-report.md)

객관적인 baseline scan:

```powershell
python scripts/harness_doctor.py --target .
```

### `/harness update`

저장소가 harness를 채택한 뒤에는 `/harness update`로 로컬
`./harness-starter-kit` 참조 clone을 최신화하고, 새 harness guidance 중 맞는
것만 선택적으로 반영할 수 있습니다.

Harness Update는 확인된 kit source를 `.harness/source.json`에 기록하고,
업데이트 후보를 분류한 뒤 Harness Update Report로 마무리합니다. target 저장소
파일을 무조건 덮어쓰면 안 됩니다.

- 명령 workflow: [`commands/harness-update.md`](commands/harness-update.md)

## 적용 방식

이 kit은 주로 자동 installer가 아닙니다. 에이전트가 대상 저장소를 먼저 읽고,
가장 작은 유용한 harness artifact만 적용해야 합니다.

- `AGENTS.md`: 지속되는 agent instructions
- lint, type check, import boundary, project rule을 통한 architecture constraints
- test, CI, pre-commit hook, 명확한 실패 메시지를 통한 feedback loops
- `docs/` 아래 decisions, failures, conventions, domain 지식 저장소
- code, docs, structure drift를 잡는 garbage-collection checks

optional installer는 agent-driven adaptation 전에 skeleton이 필요할 때만 쓰세요.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

optional installer는 `--force` 없이는 기존 파일을 덮어쓰지 않습니다. Profile
snippet은 검토용으로 `docs/harness/profiles/<profile>`에 복사됩니다. Prompt-first
adoption 중에는 cloned kit의 `harness-starter-kit/templates/profiles/<profile>`을
참조합니다.

## Profiles

사용 가능한 profile은 `generic`, `python`, `typescript`, `nextjs`, `django`,
`flask`, `fastapi`, `spring`, `android`, `react`, `vue`입니다.

Profile은 보수적인 참고 자료이며 자동 변환 규칙이 아닙니다. 대상 저장소의 현재
도구와 유지보수 기대에 맞는 snippet만 채택하세요. Stack이 나중에 도입되면
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md)를
사용하세요.

## 문서 지도

- Overview: [`docs/overview.md`](docs/overview.md)
- Adoption workflow: [`docs/adoption-workflow.md`](docs/adoption-workflow.md)
- Full adoption prompt: [`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)
- Component map: [`docs/component-map.md`](docs/component-map.md)
- Validation coverage: [`docs/validation.md`](docs/validation.md)
- Effectiveness evaluation: [`docs/evaluation.md`](docs/evaluation.md)
- Lifecycle pilot details: [`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)

## 검증과 측정

자동 fixture test는 Node.js, Next.js, Django, FastAPI, Flask, React, Spring
Boot, Android, Vue, Python, TypeScript 중심 profile의 설치와 drift check 실행
가능성을 검증합니다. 자세한 coverage와 opt-in E2E checks는
[`docs/validation.md`](docs/validation.md)를 보세요.

실제 dogfooding 대상은
[baskduf/harness_starter_kit_django](https://github.com/baskduf/harness_starter_kit_django)입니다.
이 작은 Django 프로젝트로 prompt-first adoption, `/harness update`, failure
memory, effectiveness tracking을 실제 저장소에서 검증합니다.

이 테스트들은 harness adoption이 반복되는 agent 실수를 줄인다는 것을 증명하지는
않습니다. 비교 가능한 작업, wrong-file edits, first-pass verification, human
rework 측정은 [`docs/evaluation.md`](docs/evaluation.md)와
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)를
사용하세요.

## 로컬 검사

starter-kit template, command workflow, installer behavior, drift script를 바꾸기
전에는 아래 검사를 실행하세요.

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_encoding_hygiene.py scripts/check_effectiveness_plan.py scripts/harness_doctor.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_encoding_hygiene.py
python scripts/check_effectiveness_plan.py
python scripts/harness_doctor.py --target .
```

## 라이선스

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.

## 핵심 원칙

반복되는 agent 실패는 더 명확한 instruction, 자동 constraint, test 또는 CI,
decision/failure record, drift check 중 하나 이상의 지속되는 artifact로 바뀌어야
합니다.

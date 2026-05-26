<pre align="center">
 _   _    _    ____  _   _ _____ ____ ____
| | | |  / \  |  _ \| \ | | ____/ ___/ ___|
| |_| | / _ \ | |_) |  \| |  _| \___ \___ \
|  _  |/ ___ \|  _ <| |\  | |___ ___) |__) |
|_| |_/_/   \_\_| \_\_| \_|_____|____/____/

 ____ _____  _    ____ _____ _____ ____    _  _____ _____
/ ___|_   _|/ \  |  _ \_   _| ____|  _ \  | |/ /_ _|_   _|
\___ \ | | / _ \ | |_) || | |  _| | |_) | | ' / | |  | |
 ___) || |/ ___ \|  _ < | | | |___|  _ <  | . \ | |  | |
|____/ |_/_/   \_\_| \_\|_| |_____|_| \_\ |_|\_\___| |_|
</pre>

# harness-starter-kit

<p align="center">
  <img alt="Generic profile" src="https://img.shields.io/badge/profile-generic-6b7280?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img alt="Spring Boot" src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" />
</p>

<p align="center">
  <img alt="Django" src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=111111" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" />
</p>

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

`harness-starter-kit`은 모든 소프트웨어 프로젝트에 harness engineering을
적용하기 위한 prompt-first 스타터 키트입니다. Git URL을 에이전트에게 주면,
에이전트가 대상 저장소 안에 clone하고 읽은 뒤 그 저장소의 실제 도구와 제약에
맞게 적용하도록 설계되어 있습니다.

기본 사용 흐름은 단순합니다. 대상 저장소를 코딩 에이전트로 열고, 키트 URL과
프롬프트를 준 뒤, 에이전트가 clone, read, adapt하게 합니다.

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit, read it, then apply its prompt-first
harness engineering workflow to the current project.

Rules:
- Treat the current working directory as the target repository.
- Treat ./harness-starter-kit as read-only reference material after cloning.
- Inspect this repository before editing.
- Preserve existing architecture, tools, package manager, commands, docs, and
  conventions.
- Do not blindly copy templates.
- Add only the minimum useful harness pieces.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite or delete existing files without explaining why.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, and whether ./harness-starter-kit should be removed, ignored, or
  kept before commit
```

이 프로젝트는 자동 설치기가 주된 형태가 아닙니다. 에이전트가 대상 저장소를
검사하고 가장 작은 유용한 durable artifact 집합을 추가했을 때, 대상
프로젝트에는 실용적인 에이전트 harness가 생겨야 합니다.

- 지속 가능한 에이전트 지침을 위한 `AGENTS.md`
- lint, type check, import boundary, 프로젝트별 규칙을 통한 아키텍처 제약
- test, CI, pre-commit hook, 명확한 실패 메시지를 통한 피드백 루프
- 결정, 실패 기록, 컨벤션, 도메인 맥락을 저장하는 `docs/` 지식 저장소
- 코드, 문서, 구조 drift를 감지하는 garbage-collection check

## 왜 필요한가

프롬프트는 일시적입니다. 컨텍스트는 세션에 묶입니다. harness는 프로젝트에
남습니다.

좋은 harness engineering은 반복되는 지시를 채팅 밖으로 꺼내 저장소 안에
둡니다. 그러면 에이전트가 안정적인 규칙 안에서 작업할 수 있습니다.
에이전트가 실수했을 때 장기적인 해결책은 결과물만 고치는 것이 아닙니다.
같은 실수가 다음에 덜 일어나도록 규칙, 테스트, 문서, 자동 검사를 추가하는
것이 더 나은 해결책입니다.

## 빠른 시작

대상 저장소를 코딩 에이전트로 여세요. 에이전트에게 Git URL을 주고
`./harness-starter-kit`에 clone한 뒤 읽고 workflow를 적용하라고 요청하세요.

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit, read it, then apply its prompt-first
harness engineering workflow to the current project.
```

prompt-first workflow가 이 키트의 기본 사용법입니다. 에이전트가 대상 저장소의
stack, package manager, test/lint command, 기존 문서, agent instruction file,
CI, 저장소 구조를 먼저 검사하고 그 결과에 맞게 적용할 수 있기 때문입니다.

커밋하기 전에는 로컬 `harness-starter-kit/` clone을 제거할지, 대상
`.gitignore`에 추가할지, 의도적으로 submodule/reference로 유지할지 결정하세요.
중첩 clone을 일반 프로젝트 파일처럼 실수로 커밋하지 마세요.

에이전트가 GitHub에 접근할 수 없다면 대상 저장소 안에 키트를 직접 clone한 뒤,
에이전트에게 `./harness-starter-kit`을 읽고 같은 workflow를 적용하라고
요청하세요.

### 선택 사항: Skeleton Bootstrap

`apply_harness.py`는 skeleton bootstrapper입니다. full harness adoption
engine이 아닙니다. generic starter file과 profile reference snippet을 만들 뿐,
대상 저장소의 아키텍처를 검사하거나 병합하거나 검증하지 않습니다.

에이전트 주도 적용 전에 빠른 초기 파일 구조가 필요할 때만 사용하세요. 먼저
생성될 파일을 확인합니다.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

이 스크립트는 `--force`를 제공하지 않는 한 기존 파일을 덮어쓰지 않습니다.
기본 설치는 로컬 harness skeleton file만 추가합니다. 대상 저장소에 선택
사항인 GitHub Actions harness workflow도 추가해야 할 때만 `--with-ci`를
사용하세요.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## 에이전트 주도 적용

새 프로젝트나 기존 프로젝트에서 실제 적용 경로는 에이전트 주도 방식입니다.
에이전트는 먼저 검사하고, 그 다음 적용하고, 마지막에 결과를 보고해야 합니다.
코딩 에이전트에게 다음 프롬프트를 주세요.

```text
Use this kit to apply harness engineering to this repository:

https://github.com/baskduf/harness-starter-kit

Clone the kit into ./harness-starter-kit if it is not already present, read it,
then apply its prompt-first harness engineering workflow to this repository.

Requirements:
- Inspect the target repository before editing.
- Identify the language, framework, package manager, test command, lint command,
  build command, CI provider, docs structure, and monorepo layout if present.
- Read existing AGENTS.md, CLAUDE.md, README, CONTRIBUTING, and CI configs if
  they exist.
- Preserve existing architecture, tools, and conventions.
- Add or update AGENTS.md with project-specific rules.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if they
  are missing and no equivalent knowledge store exists.
- Add lightweight drift checks under scripts/ only when they reflect real target
  repo rules, then wire stable checks into the closest existing verification
  path.
- Prefer existing linters, tests, CI, and package managers over introducing new
  ones.
- Do not overwrite existing files without explaining why.
- Finish with a short report listing files changed, checks added, assumptions,
  remaining manual integration steps, and what to do with ./harness-starter-kit
  before committing.
```

더 긴 버전은
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)에
있습니다.

## 저장소 구조

```text
harness-starter-kit/
|-- AGENTS.md
|-- docs/
|   |-- adoption-workflow.md
|   |-- component-map.md
|   |-- overview.md
|   |-- checklists/
|   `-- prompts/
|-- scripts/
|   `-- apply_harness.py
|-- tests/
`-- templates/
    |-- generic/
    `-- profiles/
```

## 적용 모드

`generic`은 모든 프로젝트에 사용할 수 있습니다. 특정 언어나 프레임워크를
가정하지 않고 durable harness skeleton을 제공합니다.

`python`은 대상 프로젝트가 Python을 사용할 때 선택합니다. Ruff, mypy,
vulture, pre-commit을 위한 Python 중심 참고 스니펫을 추가합니다.

`typescript`는 대상 프로젝트가 JavaScript 또는 TypeScript를 사용할 때
선택합니다. ESLint, dependency boundary, unused export check, package script를
위한 참고 스니펫을 추가합니다.

`nextjs`는 대상 프로젝트가 Next.js 앱일 때 선택합니다. `next build`, emit 없는
TypeScript check, generated file ignore, 최신 Next.js lint 주의사항을 위한 참고
스니펫을 추가합니다.

`django`는 대상 프로젝트가 Django 앱일 때 선택합니다. `manage.py check`,
`manage.py test`, virtual environment ignore, SQLite 개발 DB ignore, Python
`check_harness.py` entrypoint를 위한 참고 스니펫을 추가합니다.

`flask`는 대상 프로젝트가 Flask 앱일 때 선택합니다. `unittest` discovery, Flask
route check, instance-data ignore, Python `check_harness.py` entrypoint를 위한
참고 스니펫을 추가합니다.

`spring`은 대상 프로젝트가 Spring Boot 앱일 때 선택합니다. Maven 또는 Gradle
wrapper check, Spring test command, generated build output ignore, local config
ignore, Python `check_harness.py` entrypoint를 위한 참고 스니펫을 추가합니다.

`fastapi`는 대상 프로젝트가 FastAPI 앱일 때 선택합니다. pytest, mypy,
app import/startup check, generated file ignore, Python `check_harness.py`
entrypoint를 위한 참고 스니펫을 추가합니다.

`react`는 대상 프로젝트가 React 앱일 때 선택합니다. ESLint, TypeScript check,
test/build script, React-specific lint rule을 위한 참고 스니펫을 추가합니다.

`vue`는 대상 프로젝트가 Vue 앱일 때 선택합니다. ESLint, `vue-tsc`, test/build
script, Vue-specific lint rule을 위한 참고 스니펫을 추가합니다.

프로필은 의도적으로 보수적인 참고 자료입니다. 자동 프로젝트 변환이 아닙니다.
installer는 profile 파일을 `docs/harness/profiles/<profile>/` 아래에 복사하므로,
에이전트나 maintainer가 대상 프로젝트의 기존 빌드 시스템을 보존하면서 필요한
스니펫만 merge, adapt, ignore할 수 있습니다.

generic drift check는 baseline hygiene check입니다.

- `scripts/check_docs_drift.py`는 문서의 깨진 로컬 Markdown link와 오래된 파일
  참조를 잡습니다.
- `scripts/check_structure.py`는 임시 파일과 drift-prone filename을 잡습니다.
- `scripts/check_effectiveness_plan.py`는 adoption report와 effectiveness
  report의 누락되거나 placeholder로 남은 효과 측정 field를 잡습니다.

유용한 architecture drift check는 대상 저장소의 실제 규칙에서 나와야 합니다.
예를 들어 `AGENTS.md`가 route에서 DB 직접 접근을 금지한다면 route file의 DB
import를 금지하는 check를 추가하세요. ADR이 Redux 대신 Zustand를 선택했다면
Redux dependency가 들어올 때 실패하는 check를 추가하세요. generated file이 한
디렉터리에만 있어야 한다면 다른 위치의 generated file을 거부하는 structure
rule을 추가하세요.

## 설치 및 Drift Check Coverage

자동 fixture smoke test는 다음 stack의 harness 설치를 확인합니다.

- Node.js / TypeScript
- Next.js
- Django
- FastAPI
- Flask
- React
- Spring Boot
- Vue

이 fixture test는 installer가 기존 파일을 보존하고, 예상 profile snippet을 쓰며,
generic drift check가 실행 가능한지 확인합니다.

추가 end-to-end adoption check는 다음 대상으로 수동 실행되었습니다.

- `node --test`, 반복 installer 실행, TypeScript profile `check_harness.py`,
  의도적인 drift failure를 사용한 Node.js ES module 프로젝트
- pytest, mypy, generated drift check, FastAPI profile `check_harness.py`를
  사용한 FastAPI 프로젝트

FastAPI E2E coverage는 virtual environment를 만들고 dependency를 설치하므로
opt-in 자동 테스트로 제공합니다.

```powershell
$env:RUN_FASTAPI_E2E = "1"
python -m unittest tests.test_fastapi_profile_e2e
```

GitHub Actions에서는 `Harness Check` workflow를 수동 실행하고
`run_fastapi_e2e`를 켜면 같은 dependency-installing test가 실행됩니다.

## 효과 측정

위 자동 테스트는 설치 동작과 실행 가능한 drift check를 검증합니다. harness
적용이 반복되는 agent 실수를 줄였다는 증거는 아닙니다. 그 효과는
[`docs/evaluation.md`](docs/evaluation.md)의 프로토콜로 별도 측정해야 합니다.

adoption 시점에는
[`docs/templates/adoption-report.md`](docs/templates/adoption-report.md)의
Effectiveness Measurement Plan을 채우세요. baseline이 없다면 harnessed-only
tracking으로 기록하고 다음 비교 가능 task, primary metric, review window,
results location을 정의하세요. 실제 before/after 또는 후속 관측값은
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md)에
기록하세요.

## 로컬 검사

starter kit 템플릿, 설치 스크립트, drift script를 바꾼 뒤에는 다음 검사를
실행하세요.

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py scripts/check_effectiveness_plan.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
python scripts/check_effectiveness_plan.py
```

## 라이선스

이 프로젝트는 [MIT License](LICENSE)로 배포됩니다.

## 핵심 원칙

반복되는 모든 에이전트 실패는 적어도 하나의 durable artifact로 전환되어야
합니다.

- `AGENTS.md`의 더 명확한 지침
- 자동화된 제약
- test 또는 CI check
- decision 또는 failure record
- drift check

이것이 harness engineering의 핵심입니다.

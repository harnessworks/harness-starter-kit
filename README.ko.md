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

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

`harness-starter-kit`은 모든 소프트웨어 프로젝트에 harness engineering을
적용하기 위한 스타터 키트입니다.

기본 사용 흐름은 단순합니다.

```text
Clone harness-starter-kit into a target project.
Ask an agent: "Read ./harness-starter-kit and apply its harness engineering guidelines
to this repo. Preserve the existing architecture and add only the minimum
missing harness files."
```

대상 프로젝트에는 실용적인 에이전트 harness가 생겨야 합니다.

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

이 저장소를 대상 프로젝트 안에 클론하거나 다운로드합니다.

```text
workspace/
`-- target-repo/
    |-- harness-starter-kit/
    `-- existing-project-files
```

그 다음 대상 저장소를 코딩 에이전트로 열고 이 프롬프트를 주세요.

```text
Read ./harness-starter-kit first, then apply the harness engineering starter kit
to this repository.

Treat the current working directory as the target repository. Treat
./harness-starter-kit as read-only reference material unless I explicitly ask
you to edit the kit itself.

Preserve this repository's existing architecture, tools, package manager,
commands, and conventions. Add only the minimum missing harness files. Prefer
updating existing docs/configs over duplicating them. Do not overwrite or delete
existing files without explaining why.

Finish with a short adoption report listing files changed, checks I can run,
assumptions made, and remaining manual steps.
```

설치 스크립트를 직접 실행하고 싶다면 먼저 생성될 파일을 확인하세요.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

이 스크립트는 `--force`를 제공하지 않는 한 기존 파일을 덮어쓰지 않습니다.
기본 설치는 로컬 harness 파일만 추가합니다. 대상 저장소에 선택 사항인 GitHub
Actions harness workflow도 추가해야 할 때만 `--with-ci`를 사용하세요.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --with-ci
```

## 에이전트 주도 적용

새 프로젝트나 기존 프로젝트에서 코딩 에이전트에게 다음 프롬프트를 주세요.

```text
Read ./harness-starter-kit first. Apply the harness engineering starter kit to this
repository.

Requirements:
- Preserve existing architecture, tools, and conventions.
- Add or update AGENTS.md with project-specific rules.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if they
  are missing.
- Add drift checks under scripts/ and wire them into the closest existing
  verification path.
- Prefer existing linters, tests, CI, and package managers over introducing new
  ones.
- Do not overwrite existing files without explaining why.
- Finish with a short report listing files changed, checks added, and remaining
  manual integration steps.
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
가정하지 않고 durable harness skeleton을 설치합니다.

`python`은 대상 프로젝트가 Python을 사용할 때 선택합니다. Ruff, mypy,
vulture, pre-commit을 위한 Python 중심 참고 스니펫을 추가합니다.

`typescript`는 대상 프로젝트가 JavaScript 또는 TypeScript를 사용할 때
선택합니다. ESLint, dependency boundary, unused export check, package script를
위한 참고 스니펫을 추가합니다.

프로필은 의도적으로 보수적입니다. 기존 빌드 시스템을 다시 쓰는 대신 스니펫과
가이드를 제공합니다.

## 로컬 검사

starter kit 템플릿, 설치 스크립트, drift script를 바꾼 뒤에는 다음 검사를
실행하세요.

```powershell
python -m unittest discover -s tests
python -m py_compile scripts/apply_harness.py scripts/check_docs_drift.py scripts/check_structure.py
python scripts/check_docs_drift.py
python scripts/check_structure.py
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

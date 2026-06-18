<img width="2172" height="724" alt="Harness Starter Kit 로고 배너" src="https://github.com/user-attachments/assets/c303dffe-402d-44f4-8d11-3c28936f3a3e" />

<img width="1536" height="1024" alt="Harness engineering 워크플로 다이어그램" src="https://github.com/user-attachments/assets/13dbc277-ec47-4c0b-87ca-d31a88e83f4f" />


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
  <img alt="Go" src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" />
  <img alt="Rust" src="https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white" />
  <img alt="Contributors" src="https://img.shields.io/github/contributors/harnessworks/harness-starter-kit?style=flat-square" />
</p>

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

<p align="center">
  <a href="https://harnessworks.github.io/harness-starter-kit/">
    <img alt="Launch site" src="https://img.shields.io/badge/Launch-Agent_Session_Demo-0077ff?style=for-the-badge" />
  </a>
  <a href="https://dev.to/baskduf/i-stopped-prompt-engineering-my-ai-coding-agent-i-started-engineering-the-repo-instead-1i3e">
    <img alt="Read the launch essay" src="https://img.shields.io/badge/Read-Launch_Essay-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" />
  </a>
  <a href="https://github.com/harnessworks/harness-agent-benchmark-runner">
    <img alt="benchmark runner 보기" src="https://img.shields.io/badge/Benchmark-Harness_Runner-2F855A?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

# Harness Starter Kit

반복되는 coding-agent 실수를 durable repository instructions, checks, memory,
evaluation으로 바꾸기 위한 prompt-first starter kit입니다.

## 빠른 시작

대상 저장소를 코딩 에이전트로 열고 아래 prompt를 전달하세요.

<details>
<summary>전체 도입 프롬프트 보기</summary>

```text
Use this kit to apply harness engineering to this repository:

https://github.com/harnessworks/harness-starter-kit

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
- If I ask for /harness review sub-agent, use
  ./harness-starter-kit/commands/harness-review.md and treat the request as
  explicit permission to use a read-only reviewer subagent when available and
  permitted by the active runtime and tool instructions. If unavailable,
  blocked, not permitted, or failed, report the fallback reason.
- If I ask for /harness review, use
  ./harness-starter-kit/commands/harness-review.md to review the current change
  set from an opposing harness-engineering perspective. Report findings,
  missing checks, overreach, durable memory gaps, and follow-up recommendations
  without modifying files unless I explicitly ask you to apply fixes after the
  review.

Expected result:
- project-specific AGENTS.md or updated existing agent instructions
- knowledge store if no equivalent exists
- lightweight drift checks based on this repo's real rules
- local verification commands using existing tools
- adoption report with files changed, checks to run, assumptions, remaining
  manual steps, failure memory, effectiveness measurement plan,
  normal/focused/manual gate placement, and whether
  ./harness-starter-kit should be removed, ignored, or kept before commit
```

</details>

전체 prompt와 workflow는
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)와
[`docs/adoption-workflow.md`](docs/adoption-workflow.md)를 보세요.

<p align="center">
  <img width="360" alt="Harness Starter Kit GitHub star 안내 이미지" src="https://github.com/user-attachments/assets/a09c060c-3ac1-4ca4-bbce-8220478da130" />
</p>

<p align="center">
  <em>💫 If this kit helps you, a GitHub star would be appreciated. 💫</em>
</p>


## 하네스 이론

Harness engineering은 저장소를 coding agent의 지속 가능한 운영 환경으로 다룹니다.

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

Harness health는 agent effectiveness와 다릅니다. Harness Doctor는 지속되는
저장소 evidence를 스캔할 수 있지만, 에이전트가 실수를 덜 한다는 것을 증명하지는
못합니다. task outcomes와 effectiveness reports로 별도 측정하세요. 모델은
[`docs/theory/harness-engineering.md`](docs/theory/harness-engineering.md)를 보세요.

반복되는 agent failure는 더 명확한 instruction, automated constraint, test 또는
CI check, decision/failure record, drift check 중 하나 이상의 durable artifact로
전환해야 합니다.

## 명령 흐름

아래 `/harness ...` 이름은 기본적으로 내장 editor command가 아니라 prompt
convention입니다. 코딩 에이전트 chat에 직접 입력하거나 붙여넣으세요. Cursor 같은
editor에서는 matching custom slash command를 별도로 추가하지 않는 한 command
palette에 표시되지 않습니다.

명령은 사용 단계별로 생각하면 됩니다:

| 단계 | Command | Use when |
| --- | --- | --- |
| 처음 사용 | `/harness doctor` | 파일을 수정하지 않고 현재 harness readiness를 점검할 때. |
| 처음 사용 | `/harness adopt` | 이 저장소에 가장 작은 유용한 harness 조각을 적용할 때. |
| 일상 작업 | `/harness review` | commit 또는 PR 전에 현재 diff를 비판적으로 점검할 때. |
| 일상 작업 | `/harness review sub-agent` | runtime이 허용할 때 read-only reviewer subagent를 명시적으로 요청할 때. |
| 유지보수 | `/harness update` | 더 새 `harness-starter-kit` reference를 가져와 이 repo에 선택적으로 반영할 때. |
| 유지보수 | `/harness refresh` | 이 repo 안의 stale, duplicated, obsolete, unused harness guidance를 정리할 때. |

빠른 규칙:

- `doctor`는 점검할 때 사용합니다.
- `adopt`는 시작할 때 사용합니다.
- `review`는 작업을 끝내기 전에 사용합니다.
- `update`는 kit version이 바뀌었을 때 사용합니다.
- `refresh`는 이 repo의 기존 harness guidance가 낡았을 때 사용합니다.

전체 workflow는 [`commands/`](commands/)를 보세요:
[`adopt`](commands/harness-adopt.md),
[`doctor`](commands/harness-doctor.md),
[`update`](commands/harness-update.md),
[`refresh`](commands/harness-refresh.md),
[`review`](commands/harness-review.md).

## Agent Skills 설치

Harness workflows는 기본적으로 prompt-first 방식이지만, 같은 workflows를 Codex와
Claude Code에서 runtime-native skills로 설치할 수도 있습니다.

### Codex

```bash
codex plugin marketplace add harnessworks/harness-agent-skills-marketplace --ref v0.1.15
```

Codex를 재시작한 뒤 Plugins 화면을 열고 `Harnessworks` marketplace에서
`harness-agent-skills`를 설치하세요.

모든 runtime에서 같은 command model을 사용합니다:

```text
Start:      $harness doctor → $harness adopt
Daily:      $harness review
Maintain:   $harness update or $harness refresh
```

자주 쓰는 명령:

```text
$harness doctor
$harness adopt
$harness review
```

유지보수 명령:

```text
$harness update
$harness refresh
```

### Claude Code

```bash
claude plugin marketplace add harnessworks/harness-agent-skills-marketplace@v0.1.15
claude plugin install harness-agent-skills@harnessworks
```

Router command를 사용합니다:

```text
Start:      /harness-agent-skills:harness doctor → /harness-agent-skills:harness adopt
Daily:      /harness-agent-skills:harness review
Maintain:   /harness-agent-skills:harness update or /harness-agent-skills:harness refresh
```

자주 쓰는 명령:

```text
/harness-agent-skills:harness doctor
/harness-agent-skills:harness adopt
/harness-agent-skills:harness review
```

유지보수 명령:

```text
/harness-agent-skills:harness update
/harness-agent-skills:harness refresh
```

소스 패키지는 [`agent-skills/`](agent-skills/)에 있습니다. repo-local 직접 설치,
packaging 세부사항, update 동작은
[`docs/agent-skills-package.md`](docs/agent-skills-package.md)를 보세요.

## 적용 방식

<details>
<summary>적용 세부사항 보기</summary>

이 kit은 주로 자동 installer가 아닙니다. 에이전트가 대상 저장소를 먼저 읽고,
instructions, enforceable constraints, feedback loops, durable memory, drift
checks, adoption report 중 가장 작은 유용한 세트만 적용해야 합니다.
[`docs/adoption-workflow.md`](docs/adoption-workflow.md)와
[`docs/prompts/apply-to-target-repo.md`](docs/prompts/apply-to-target-repo.md)를
따르세요.

optional installer는 agent-driven adaptation 전에 skeleton이 필요할 때만 쓰세요.
검토용 profile snippets를 `docs/harness/profiles/<profile>`에 복사합니다.
Prompt-first adoption은 cloned kit의
`harness-starter-kit/templates/profiles/<profile>`을 참조합니다.

```powershell
python harness-starter-kit/scripts/apply_harness.py --target . --profile generic --dry-run
```

위 badge에 표시된 profiles는 보수적인 reference snippets이며 automatic
migrations가 아닙니다. [`docs/profiles.md`](docs/profiles.md)와
[`docs/checklists/profile-absorption.md`](docs/checklists/profile-absorption.md)를
보세요.

자세한 문서 index는 [`docs/component-map.md`](docs/component-map.md)에 있습니다.
주요 adoption references:
[`docs/checklists/external-api-work.md`](docs/checklists/external-api-work.md),
[`docs/checklists/decision-failure-memory.md`](docs/checklists/decision-failure-memory.md),
[`docs/checklists/verification-scripts.md`](docs/checklists/verification-scripts.md).

Validation coverage와 local checks는
[`docs/validation.md`](docs/validation.md)에 있습니다. Lifecycle pilot details는
[`docs/examples/lifecycle-pilot-results.md`](docs/examples/lifecycle-pilot-results.md)를
보세요. 이 자료들은 harness adoption이 repeated agent mistakes를 줄인다는 것을
증명하지 않습니다. comparable tasks, wrong-file edits, first-pass verification,
human rework 측정에는 [`docs/evaluation.md`](docs/evaluation.md),
[`docs/templates/effectiveness-report.md`](docs/templates/effectiveness-report.md),
[`docs/templates/task-outcome.yaml`](docs/templates/task-outcome.yaml)을 사용하세요.

Dogfood reports에는 Next.js public-data target인
[`TodayBus`](docs/examples/effectiveness-report-todaybus-dogfood.md)와
Spring/Maven backend 및 vanilla frontend target인
[`Harness ERP`](docs/examples/effectiveness-report-harness-erp-dogfood.md)가
포함됩니다. 둘 다 harnessed-only benchmarks이며 effectiveness improvement의
증거는 아닙니다.

</details>

## 기여자

코드, 문서, 리뷰, 예시, 번역, dogfooding으로 이 kit을 다듬어준 모든 분께
감사합니다.

<a href="https://github.com/harnessworks/harness-starter-kit/graphs/contributors">
  <img src="https://readme-contribs.as93.net/contributors/harnessworks/harness-starter-kit?v=20260608-yunhwane" alt="Contributors" />
</a>

## 소개된 곳

- [Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents): AI agent tooling project.
- [github/awesome-copilot](https://github.com/github/awesome-copilot): Copilot customization resource.

## 라이선스

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.

# Luna Agent Teams for Codex

Luna의 **기본 Codex 사용 방식은 Repository-local `AGENTS.md` + `.agents/skills/` + `docs/CORE_ENGINEERING_PROTOCOL_V2.md`** 입니다. 별도 Luna 프로세스나 서버를 실행할 필요가 없습니다.

Codex에서 Luna가 포함된 프로젝트 Repository를 열고 자연어로 작업을 요청하면, 프로젝트의 `AGENTS.md`가 Luna Chat Coder, Luna Router, Core Engineering Protocol v2 정책을 안내합니다.

전체 한국어 사용 매뉴얼: [`docs/USAGE.ko.md`](../../docs/USAGE.ko.md)

## Core Engineering Protocol v2

Codex에서의 기본 개발 흐름은 다음과 같습니다.

```text
Requirements
-> bounded requirement grilling
-> architecture decision
-> codebase impact/design review
-> repository/template
-> task-owned feature branch
-> implementation
-> risk-calibrated tests/TDD
-> evidence-first debugging when failures occur
-> self-review
-> dual-axis independent review
-> repository-required verification
-> GitHub publication
-> PR
```

핵심 동작은 다음과 같습니다.

- 사용자의 자연어 요청과 기존 Repository 문맥에서 일상적인 세부사항을 추론하고, 결과를 실제로 바꿀 수 있는 질문만 합니다.
- 단순한 계획이나 구현 일부에서 멈추지 않고, 이미 승인된 reversible/read-only/reviewable 작업은 요청한 결과까지 이어서 수행합니다.
- 기존 코드베이스의 모듈 경계와 SSOT를 확인한 뒤 새 추상화·의존성·API·설정 계층을 추가합니다.
- TDD는 회귀 버그, 명확한 비즈니스 규칙, 보안/데이터/마이그레이션/파서/프로토콜 경계 등 효과가 큰 변경에 우선 적용합니다.
- 실패는 로그·재현·테스트·설정·버전·최근 변경 증거를 먼저 수집한 뒤 수정합니다.
- Code Review는 `behavioral correctness`와 `codebase fit` 두 축을 독립적으로 검토합니다.
- Host가 안정적인 subagent delegation을 지원하고 작업이 독립적이면 병렬화할 수 있지만, 불필요한 agent 생성은 하지 않습니다.

Canonical policy: [`docs/CORE_ENGINEERING_PROTOCOL_V2.md`](../../docs/CORE_ENGINEERING_PROTOCOL_V2.md)

## Recommended default usage

1. `luna-chat-coder` 템플릿으로 프로젝트를 만들거나 기존 프로젝트에 Luna 정책 파일을 추가합니다.
2. Codex에서 해당 프로젝트 Repository를 작업 디렉터리로 엽니다.
3. 자연어로 작업을 요청합니다.

예:

```text
RHEL agent can connect to the manager, but the manager cannot connect back. Diagnose it.
```

```text
Add OAuth login and RBAC to this service and open a PR.
```

```text
Analyze this SAST High finding and implement a verified remediation.
```

사용자가 Coding, Security, Incident Analysis 중 하나를 직접 고를 필요는 없습니다. Repository-local Luna Router policy가 lead team과 필요한 specialist를 선택합니다.

## Luna Doctor

저장소의 지침과 스킬 구성을 점검하려면 Codex에서 `$doctor`를 요청합니다. `$doctor --deep`은 중복 문단과 경로 참조까지 확인하고, `$doctor --fix`는 근거가 있는 작은 변경의 diff를 준비해 검증합니다. 실제 파일 삭제나 플러그인/MCP 제거를 자동 실행하지 않습니다.

직접 읽기 전용 진단을 실행하려면 `python3 .agents/skills/doctor/scripts/health.py --root . --deep`을 사용합니다. 최초 진단의 기준값과 조치 분류는 [`docs/LUNA_HEALTH_CHECK_2026-09-23.md`](../../docs/LUNA_HEALTH_CHECK_2026-09-23.md)에 있습니다. 저장소에 설정 파일이 없으면 사용자 환경의 플러그인 설치 상태나 MCP 연결 상태는 **미확인**으로 표시합니다.

## Optional custom-agent integration

`integrations/codex/agents/*.toml`은 named custom agent/subagent 기능을 사용할 수 있는 Codex 환경을 위한 **선택적 통합**입니다. Luna의 핵심 동작은 이 기능에 의존하지 않습니다.

Codex 버전 또는 product surface에 따라 custom agent/subagent 노출 방식이 다를 수 있으므로, 지원 여부가 불확실한 환경에서는 Repository-local `AGENTS.md` + Skills 방식을 사용하십시오.

### Optional install

macOS/Linux:

```bash
bash scripts/install-codex-agents.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-codex-agents.ps1
```

스크립트는 TOML 파일을 `$CODEX_HOME/agents/` 또는 기본 `~/.codex/agents/`에 새로 설치합니다. 같은 이름의 파일이나 링크가 이미 있으면 내용이 같거나 달라도 보존하고, 설치·보존 개수를 출력합니다. 기존 정의의 갱신이 필요하면 diff를 검토한 뒤 별도로 병합하십시오. 강제 덮어쓰기 옵션은 제공하지 않습니다.

이 변경은 향후 템플릿 사용과 명시적인 신규 설치에 적용합니다. 기존 프로젝트의 지침·정책·스킬을 일괄 갱신하거나 Codex 전역 정책을 자동 변경하지 않습니다. 기존 프로젝트에서는 현재 구성을 유지하고, 신규 프로젝트는 최신 템플릿에서 시작하십시오. 전역 named agent 변경은 다른 프로젝트에도 사용될 수 있으므로 기존 프로젝트와 분리된 설치가 필요하면 별도 `CODEX_HOME`을 지정하십시오.

설치 후 해당 Codex build가 named custom agents를 지원한다면 다음 정의를 사용할 수 있습니다.

- `Luna Router`
- `Luna Coding Team`
- `Luna Code Reviewer`
- `Luna Security Team`
- `Luna Incident Analysis Team`
- `Luna Reverse Engineer` (역공학 작업에서만 선택)

## Router execution model

Luna Router는 특정 subagent orchestration 기능에 종속되지 않습니다.

- Host가 named-agent/subagent delegation을 안정적으로 지원하면 독립적이고 bounded한 workstream을 병렬 위임할 수 있습니다.
- 병렬 작업은 conflicting writes 또는 ownership ambiguity를 만들지 않는 경우에만 사용합니다.
- Delegation이 없거나 불확실하면 현재 agent가 Repository-local Luna Agent Teams skill과 routing policy에 따라 선택된 workflow를 직접 수행합니다.

따라서 custom-agent TOML을 설치하지 않아도 Luna Router의 핵심 라우팅 정책을 사용할 수 있습니다.

## Routing behavior

Router precedence는 다음과 같습니다.

1. 기존 failure/degradation의 diagnosis/recovery가 목적 -> Incident Analysis.
2. security assurance/risk reduction이 주목적 -> Security.
3. planned creation 또는 repository behavior change -> Coding.

Mixed request는 하나의 lead team과 필요한 support만 사용합니다. Live incident가 code fix를 필요로 할 가능성이 있어도 defect가 격리되기 전에는 Incident-led이며, 신규 authentication feature는 Coding-led + Security support입니다.

Canonical routing policy와 regression cases는 `.agents/skills/luna-agent-teams/references/` 아래에 있습니다.

## GPT-6 Astra / API harness adaptation

Luna의 Repository-local 정책은 특정 모델에 종속되지 않습니다. 다만 GPT-6 Astra를 Responses API 기반 agent harness에서 사용할 경우 `CORE_ENGINEERING_PROTOCOL_V2.md`의 Astra adaptation 원칙을 적용할 수 있습니다.

- tool calling은 Responses API 기준으로 설계합니다.
- 독립 workstream은 harness가 지원할 때 async tool calling을 활용할 수 있습니다.
- mid-turn steering이 지원되면 이미 완료된 유효 작업을 버리지 않고 새 요구사항을 반영합니다.
- reasoning configuration update가 지원되면 작업 복잡도 변화에 맞춰 effort를 조정합니다.
- accessible `AGENTS.md`/Skill 지시가 많을수록 충돌 감사를 중요하게 봅니다.
- 모델별 API 파라미터·cache·data residency 제한은 적용 시점의 OpenAI 1차 문서를 확인합니다.

Codex 제품 표면이 이러한 모델/API 제어를 직접 노출한다고 가정하지 않습니다. 지원 여부는 해당 Host의 실제 기능을 기준으로 판단합니다.

## Source and attribution

The role taxonomy was informed by the MIT-licensed `Edward-Jeong/agency-agents` repository. Luna's definitions are condensed and adapted around Luna Chat Coder's exact-state, evidence, GitHub, and delivery policies rather than copied wholesale.

## REA를 Codex에서 사용하는 방법

Repository-local 진입점은 `.agents/skills/luna-reverse-engineering/SKILL.md`입니다. 최신 파일이 포함된 프로젝트를 Codex에서 열고 다음과 같이 요청하십시오.

```text
Luna 역공학 스킬을 사용해 제공한 ASAR의 모듈 구조와 API 호출 흐름을 정적으로 분석해줘.
설치된 REA 버전과 샘플 해시를 확인하고 범위 파일을 만든 뒤 계획을 검토해 실행해.
샘플 자체는 실행하지 말고, 관측 사실과 추론 및 미확인 사항을 구분해줘.
```

REA가 없을 때 설치는 별도 사용자 지시가 필요합니다. 다음 명령은 **사용자가 선택해 실행하는 1회 설치·검증 예시**이며, 매 작업의 자동 설정이 아닙니다. Node.js 24.19.0과 Python 3.11로 검증하는 구성이며, 정확한 REA 버전은 6.7.0입니다. 지원 Node 버전은 선택한 REA 배포의 요구사항도 확인하십시오. 사용자 PC 설치를 원격에서 완료했다고 간주하지 않습니다.

Windows PowerShell (프로젝트 루트):

```powershell
npm install --prefix .\work\rea-runtime --ignore-scripts --no-audit --no-fund rea-agents@6.7.0
$reaNode = (Get-Command node).Source
$reaEntry = (Resolve-Path .\work\rea-runtime\node_modules\rea-agents\scripts\rea.mjs).Path
python tests/run_security_ops_sample.py --node $reaNode --rea $reaEntry --version 6.7.0
```

macOS/Linux (프로젝트 루트):

```bash
npm install --prefix ./work/rea-runtime --ignore-scripts --no-audit --no-fund rea-agents@6.7.0
REA_NODE="$(command -v node)"
REA_ENTRY="$PWD/work/rea-runtime/node_modules/rea-agents/scripts/rea.mjs"
python3 tests/run_security_ops_sample.py --node "$REA_NODE" --rea "$REA_ENTRY" --version 6.7.0
```

macOS의 위 명령은 사용 절차이며 실제 macOS 공급자 검증 결과를 의미하지 않습니다. 샘플 러너는 가상 ASAR만 검사하며 고객 파일은 사용하지 않습니다. 성공하려면 프로세스 종료코드뿐 아니라 `portal.js`의 파싱 완료가 확인되어야 합니다.

실제 승인된 샘플에는 [범위 JSON과 분석 사용법](../../docs/SECURITY_OPS.ko.md)을 적용합니다. Windows에서는 `--node`에 절대 `node.exe` 경로, `--executable`에 절대 `scripts/rea.mjs` 경로를 지정하십시오. `rea.cmd`/`cmd.exe`/shell 실행을 사용하지 않습니다. 기본 호출은 계획만 출력하고 `--execute`가 있어야 실제 REA를 호출합니다.

Named agent가 지원되는 Codex에서는 기존 설치 명령으로 `Luna Reverse Engineer`도 추가할 수 있습니다. 같은 이름의 기존 파일은 보존하므로 기존 사용자 정의를 갱신하려면 별도 diff 검토가 필요합니다. 전용 agent만 다른 프로젝트에 설치해도 해당 프로젝트의 스킬·실행 도구가 자동 복사되지는 않습니다. 기존 프로젝트에는 해당 스킬과 Security Ops helper를 먼저 검토해 포함하거나, 그 프로젝트의 승인된 도구를 사용하십시오.

이 통합은 선택형 CLI 방식입니다. Codex MCP 등록·전역 설정을 변경하지 않으며, 에이전트 선택만으로 139개 이상의 REA 도구를 모든 작업에 상시 노출하지 않습니다. Ghidra/네이티브와 JAR/WAR 및 런타임 후킹 지원은 이번 ASAR 정적 분석 검증과 구분합니다.

# Luna Agent Teams for Codex

Luna의 **기본 Codex 사용 방식은 Repository-local `AGENTS.md` + `.agents/skills/`** 입니다. 별도 Luna 프로세스나 서버를 실행할 필요가 없습니다.

Codex에서 Luna가 포함된 프로젝트 Repository를 열고 자연어로 작업을 요청하면, 프로젝트의 `AGENTS.md`가 Luna Chat Coder와 Luna Router 정책을 안내합니다.

전체 한국어 사용 매뉴얼: [`docs/USAGE.ko.md`](../../docs/USAGE.ko.md)

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

스크립트는 TOML 파일을 `$CODEX_HOME/agents/` 또는 기본 `~/.codex/agents/`에 복사합니다.

설치 후 해당 Codex build가 named custom agents를 지원한다면 다음 정의를 사용할 수 있습니다.

- `Luna Router`
- `Luna Coding Team`
- `Luna Code Reviewer`
- `Luna Security Team`
- `Luna Incident Analysis Team`

## Router execution model

Luna Router는 특정 subagent orchestration 기능에 종속되지 않습니다.

- Host가 named-agent/subagent delegation을 안정적으로 지원하면 선택된 team/specialist에 bounded work를 위임할 수 있습니다.
- Delegation이 없거나 불확실하면 현재 agent가 Repository-local Luna Agent Teams skill과 routing policy에 따라 선택된 workflow를 직접 수행합니다.

따라서 custom-agent TOML을 설치하지 않아도 Luna Router의 핵심 라우팅 정책을 사용할 수 있습니다.

## Routing behavior

Router precedence는 다음과 같습니다.

1. 기존 failure/degradation의 diagnosis/recovery가 목적 -> Incident Analysis.
2. security assurance/risk reduction이 주목적 -> Security.
3. planned creation 또는 repository behavior change -> Coding.

Mixed request는 하나의 lead team과 필요한 support만 사용합니다. Live incident가 code fix를 필요로 할 가능성이 있어도 defect가 격리되기 전에는 Incident-led이며, 신규 authentication feature는 Coding-led + Security support입니다.

Canonical routing policy와 regression cases는 `.agents/skills/luna-agent-teams/references/` 아래에 있습니다.

## Source and attribution

The role taxonomy was informed by the MIT-licensed `Edward-Jeong/agency-agents` repository. Luna's definitions are condensed and adapted around Luna Chat Coder's exact-state, evidence, GitHub, and delivery policies rather than copied wholesale.

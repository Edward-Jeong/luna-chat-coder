# Luna Chat Coder 사용 매뉴얼

이 문서는 Luna Chat Coder를 실제로 어디에서, 어떻게 사용하는지 설명합니다.

## 1. 가장 중요한 결론

**Luna Chat Coder는 PC에서 별도의 서버나 프로그램으로 계속 실행하는 소프트웨어가 아닙니다.**

기본 사용 방식은 다음과 같습니다.

```text
luna-chat-coder 템플릿으로 프로젝트 생성
        ↓
Codex에서 그 프로젝트/Repository를 연다
        ↓
Codex가 프로젝트의 AGENTS.md를 읽는다
        ↓
AGENTS.md가 Luna Chat Coder + Luna Router 정책을 안내한다
        ↓
사용자는 자연어로 개발/보안/장애 요청만 한다
        ↓
Luna Router가 Coding / Security / Incident Analysis를 자동 선택
```

즉, **평소에는 Luna를 별도로 실행하지 않습니다.**

---

## 2. 어디에서 사용할 수 있나

### A. Codex에서 사용 — 권장

가장 권장하는 방식입니다.

Codex에서 Luna가 포함된 Repository를 작업 대상으로 열고 평소처럼 자연어로 요청합니다.

예:

```text
이 프로젝트에 OAuth 로그인과 RBAC을 추가하고 테스트 후 PR까지 만들어줘.
```

Router 예상 동작:

```text
Lead: Coding Team
Support: Security Architect / AppSec
Final gate: Test + Code Reviewer
```

장애 요청 예:

```text
RHEL 에이전트에서 매니저 통신은 되는데 매니저에서 에이전트로 역방향 통신이 안 돼. 원인을 찾아줘.
```

Router 예상 동작:

```text
Lead: Incident Analysis Team
Specialist: Infrastructure Diagnostician
```

보안 요청 예:

```text
이 PR에서 SQL Injection과 인증 우회 가능성을 보안 관점으로 검토해줘.
```

Router 예상 동작:

```text
Lead: Security Team
Specialists: AppSec Engineer + Security Reviewer
```

사용자가 `Coding Team을 사용해`, `Incident Team을 사용해`처럼 팀을 직접 지정할 필요는 없습니다.

### B. ChatGPT + GitHub 연결 환경에서 사용

Repository의 `AGENTS.md`와 `.agents/skills/`를 읽을 수 있고 GitHub 작업 권한이 있는 ChatGPT 개발 환경에서도 같은 정책을 사용할 수 있습니다.

이 경우에도 사용자는 자연어 요구사항을 주고, Luna 정책은 Repository 내부에 존재합니다.

### C. 일반 터미널에서 독립 실행

Luna 자체를 실행하는 별도의 `luna` 명령이나 백그라운드 서버는 없습니다.

프로젝트를 직접 편집하거나 테스트할 때는 평소 사용하는 Git, IDE, 터미널을 그대로 사용합니다. Luna는 **AI agent의 작업 방식과 역할 분담을 정의하는 Repository-local 정책 계층**입니다.

---

## 3. 신규 프로젝트에서 사용하는 방법

### Step 1. luna-chat-coder를 Template으로 새 Repository 생성

GitHub의 `Edward-Jeong/luna-chat-coder` Repository에서 Template 기능으로 새 프로젝트 Repository를 만듭니다.

예:

```text
my-new-security-app
```

새 Repository에는 최소한 다음 Luna 파일을 유지합니다.

```text
AGENTS.md
.agents/
  skills/
    luna-chat-coder/
    luna-agent-teams/
```

이 파일들이 Luna의 실행 정책입니다.

### Step 2. Codex에서 새 프로젝트를 연다

Codex가 실제 프로젝트 Repository를 작업 디렉터리로 사용하도록 엽니다.

Codex는 프로젝트의 `AGENTS.md`를 작업 지침으로 사용하며, Luna의 `AGENTS.md`는 추가 정책 파일을 읽도록 안내합니다.

### Step 3. 자연어로 작업 요청

예:

```text
사용자가 서버 목록을 조회하고 취약점 결과를 볼 수 있는 웹 서비스를 만들어줘.
React 프론트엔드와 REST API가 필요하고 인증도 포함해줘.
```

Luna Router는 내부적으로 다음처럼 판단합니다.

```text
Lead Team: Coding
Support: Security
Specialists:
- Software Architect
- Implementation Engineer
- Security Architect / AppSec
- Test Engineer
- Code Reviewer
```

그리고 Luna 개발 프로토콜을 따릅니다.

```text
요구사항
→ 아키텍처 결정
→ Repository / Template
→ Feature Branch
→ 구현
→ 테스트·검증
→ Code Review
→ GitHub 반영
→ PR
```

---

## 4. 기존 프로젝트에 Luna를 적용하는 방법

기존 Repository 전체를 luna-chat-coder 템플릿으로 다시 만들 필요는 없습니다.

다음 구조를 기존 프로젝트에 추가할 수 있습니다.

```text
AGENTS.md
.agents/skills/luna-chat-coder/
.agents/skills/luna-agent-teams/
```

단, 기존 프로젝트에 `AGENTS.md`가 이미 있다면 덮어쓰지 말고 기존 프로젝트 지침과 Luna entry-point를 합쳐야 합니다.

프로젝트의 기술 스택, 빌드 방법, 테스트 프레임워크가 항상 우선이며 Luna가 임의로 바꾸지 않습니다.

---

## 5. Luna Router는 무엇을 하는가

Router는 키워드만 보고 팀을 정하지 않습니다.

기본 판단 순서는 다음과 같습니다.

```text
1. 이미 장애/실패가 발생 중인가?
   YES → Incident Analysis

2. 보안 검증/위험 감소 자체가 주목적인가?
   YES → Security

3. 신규 기능/수정/리팩터링/개발이 목적인가?
   YES → Coding
```

복합 요청도 모든 팀을 무조건 실행하지 않습니다.

예:

```text
OAuth 로그인 신규 개발
→ Coding Lead + Security Support

운영 장애 후 코드 버그 의심
→ Incident Lead
→ 결함 확인 후 Coding handoff

SAST High 수정
→ Security 분석
→ Coding 수정
→ Security 재검증
```

---

## 6. Codex Custom Agent TOML은 꼭 설치해야 하나

**아니요. 기본 사용에는 필요하지 않습니다.**

Repository 안의 `AGENTS.md` + Luna Skills 방식이 기본입니다.

`integrations/codex/agents/*.toml`은 Codex 환경에서 named custom agent/subagent 기능을 별도로 활용하고 싶은 경우를 위한 **선택적 통합**입니다.

Codex 버전과 제품 surface에 따라 custom agent/subagent 노출 방식이 달라질 수 있으므로, Luna의 핵심 동작이 이 기능에 의존하지 않도록 설계되어 있습니다.

### 선택적으로 설치하려는 경우

macOS/Linux:

```bash
bash scripts/install-codex-agents.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-codex-agents.ps1
```

스크립트는 TOML 파일을 다음 위치로 복사합니다.

```text
$CODEX_HOME/agents/
```

`CODEX_HOME`이 없다면 기본적으로:

```text
~/.codex/agents/
```

을 사용합니다.

이 설치는 **선택 사항**이며, Codex build에서 custom agent 기능이 지원되지 않더라도 Repository-local Luna Router는 계속 사용할 수 있어야 합니다.

---

## 7. 평소 내가 해야 하는 일

신규 개발에서는 사실상 다음 두 가지만 하면 됩니다.

```text
1. Luna가 포함된 프로젝트를 Codex에서 연다.
2. 원하는 작업을 자연어로 설명한다.
```

예:

```text
이 서비스를 Docker로 배포할 수 있게 구성해줘.
```

```text
로그인 실패 원인을 로그와 코드 기준으로 찾아서 수정해줘.
```

```text
이 PR을 보안과 코드 품질 관점에서 최종 리뷰해줘.
```

팀 선택, 리뷰어 선택, 장애 분석 담당 선택은 Router의 역할입니다.

---

## 8. PC에서 매번 실행해야 하는 것이 있나

없습니다.

### 매번 필요하지 않은 것

- Luna 서버 실행
- Docker로 Luna 실행
- Python 서비스 실행
- 별도 Router daemon 실행
- `install-codex-agents` 반복 실행

### 필요한 것

- Codex가 해당 Repository를 읽고 수정할 수 있어야 함
- 프로젝트 자체 개발에 필요한 Node.js, Java, Python, Docker, DB 등은 프로젝트 요구사항에 따라 필요
- GitHub 반영/PR이 필요한 경우 GitHub 접근 권한 필요

Luna는 개발환경 자체가 아니라 **개발 프로토콜 + Agent 역할 + 라우팅 정책**입니다.

---

## 9. 추천 운영 방식

권장 구조는 다음과 같습니다.

```text
luna-chat-coder
    = Master Template / AI Engineering Policy

새 프로젝트 A
새 프로젝트 B
새 프로젝트 C
    = luna-chat-coder Template 기반 Repository
```

각 프로젝트는 자기 기술 스택과 코드를 갖고, Luna 정책은 공통 개발 방식으로 사용합니다.

따라서 `luna-chat-coder` Repository 자체에서 모든 실제 제품 코드를 개발하는 방식은 권장하지 않습니다.

---

## 10. 가장 간단한 사용 예

### 신규 프로젝트

```text
Codex에서 Luna 기반 Repository 열기

"서버 취약점 결과를 관리하는 웹 서비스를 새로 만들어줘.
사용자는 로그인해야 하고 관리자와 일반 사용자를 구분해줘."
```

Luna 내부 처리:

```text
Router
→ Coding Lead
→ Security support
→ Architecture
→ Feature Branch
→ Implementation
→ Tests
→ Code Review
→ PR
```

### 장애 분석

```text
"Tomcat은 시작되는데 Spring Bean 생성 오류로 웹 서비스가 안 올라와.
로그를 보고 원인을 찾아줘."
```

Luna 내부 처리:

```text
Router
→ Incident Analysis Lead
→ Application Diagnostician
→ 필요 시 Database Diagnostician
→ 원인 격리
→ 코드 결함이면 Coding handoff
```

### 보안 리뷰

```text
"이 API 변경사항에 인증 우회나 권한 상승 위험이 있는지 검토해줘."
```

Luna 내부 처리:

```text
Router
→ Security Lead
→ AppSec
→ Security Reviewer
```

---

## 11. 현재 권장 원칙

**기본:** Repository-local `AGENTS.md` + `.agents/skills/` 사용

**선택:** Codex custom agent TOML 설치

**불필요:** Luna 전용 PC 서버/daemon 실행

**사용자 인터페이스:** 자연어 요청

**Luna 역할:** 요청을 자동 라우팅하고 정해진 개발·보안·장애 프로토콜을 적용

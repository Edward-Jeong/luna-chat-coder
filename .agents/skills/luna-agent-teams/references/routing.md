# Luna Router v1

Luna Router selects one lead team and the minimum supporting specialists from a natural-language request. Routing is semantic: classify the user's objective, current system state, dominant risk, and required action. Do not route by keyword counting alone.

## Routing contract

For every task, determine internally:

```text
Lead team: Coding | Security | Incident Analysis
Supporting team(s): optional
Specialists: minimum useful set
Mode: delivery | review | diagnostic | recovery
Confidence: high | medium | low
Reason: one sentence
Escalation trigger: evidence that would change the route
```

The routing decision is normally silent. Surface it only when it helps explain a handoff, a safety boundary, or a materially mixed task.

## Decision order

Evaluate in this order.

### 1. Is something currently failing or degraded?

If the primary goal is to explain, restore, isolate, or recover a failure that already exists, route to **Incident Analysis**.

Typical signals:
- service will not start, process crashes, timeout, connection failure, installation/runtime error
- unexpected resource growth, DB error, stack trace, container failure, OS/network/firewall issue
- "why is this failing", "root cause", "logs show", "worked before", "after patch/migration it broke"

Do not route a production failure directly to Coding just because source code may eventually need a fix. Incident Analysis owns evidence and fault isolation first; hand off to Coding after a reproducible source/config defect is established.

### 2. Is the primary objective security assurance or security risk reduction?

If the main requested outcome is to identify, model, validate, prioritize, or remediate security risk, route to **Security**.

Typical signals:
- threat model, security architecture, vulnerability assessment, secure code review
- SAST/DAST/SCA findings, OWASP/CWE/CVE analysis, secrets exposure
- authorized penetration testing, exploitability validation, security hardening
- authn/authz, trust boundaries, sensitive data, privilege, cryptography as the main subject

Security is a supporting team rather than lead when these concerns are only one part of building a larger feature.

### 3. Is the primary objective to create or deliberately change repository behavior?

If the goal is a new project, feature, refactor, defect fix after diagnosis, tests, architecture, or PR preparation, route to **Coding**.

Typical signals:
- build/create/implement/add/refactor/migrate a feature or service
- design an API/data model/module architecture
- write tests, fix a confirmed bug, prepare/review a general PR

For material UI/frontend work, Coding remains the lead team and conditionally adds the Luna Design Specialist and an independent Design Reviewer. Read `.agents/skills/luna-design-system/SKILL.md`; use repository-root `DESIGN.md` as persistent design context, creating it from `templates/DESIGN.md` for new/material UI surfaces when missing.

### 4. Resolve mixed tasks by dominant outcome

Use exactly one lead team unless the task has clearly separable phases.

- Existing outage + likely code defect -> **Incident lead**, then Coding handoff after isolation.
- New auth/security feature -> **Coding lead + Security support** from architecture through review.
- New/material UI feature -> **Coding lead + Design Specialist**, then Design Reviewer before Code Reviewer readiness; add Security only when a security boundary materially changes.
- Security finding requiring code remediation -> **Security lead** for finding/acceptance criteria, then Coding implementation, then Security verification.
- Suspected breach causing outage -> **Incident lead + Security support**; prioritize evidence preservation and containment.
- General PR review -> **Coding / Code Reviewer**; add Security only when the diff materially changes a security boundary and Design only when UI/design-system behavior materially changes.

## Specialist selection

### Coding
- **Software Architect**: material architecture, APIs, data models, migrations, module boundaries, non-trivial tradeoffs.
- **Implementation Engineer**: source/config changes.
- **Test Engineer**: any behavior change requiring executable verification.
- **Code Reviewer**: any merge/readiness decision; independent from implementation.
- **Design Specialist**: conditional role for material UI/frontend/design-system work; creates/reads/refines `DESIGN.md` and turns design intent into implementation constraints.
- **Design Reviewer**: independent post-implementation UI consistency/accessibility gate; blockers prevent merge readiness.

### Security
- **Security Architect**: trust boundaries, security controls, auth models, sensitive-data flows.
- **AppSec Engineer**: code-level security, SAST/DAST/SCA, secure remediation.
- **Penetration Tester**: bounded authorized exploitability validation only.
- **Security Reviewer**: independent severity/remediation/release verification.

### Incident Analysis
- **Incident Lead**: always for multi-step or production-impacting incidents.
- **Infrastructure Diagnostician**: OS, process, network, DNS, ports, firewall, filesystem, container/service manager.
- **Application Diagnostician**: runtime, stack traces, app configuration, dependency/request flow.
- **Database Diagnostician**: DB connectivity, credentials, migrations, locks, storage/capacity, SQL behavior.
- **Root Cause Analyst**: multi-layer causal synthesis and corrective/preventive actions.

## UI design-system routing

Treat work as material UI when it creates or substantially changes web/mobile screens, dashboards, forms, navigation, tables, data visualization, frontend information architecture, component libraries, design tokens/themes, responsive behavior, accessibility behavior, or reusable visual rules.

For that route:

1. Read `.agents/skills/luna-design-system/SKILL.md`.
2. Read repository-root `DESIGN.md` before UI architecture/implementation decisions.
3. If `DESIGN.md` is missing for a new/material UI surface, instantiate it from `templates/DESIGN.md` when available, replace placeholders, and refine generic defaults from known project evidence.
4. Use the Design Specialist before implementation and the independent Design Reviewer after implementation.
5. Keep UI implementation in the repository's existing framework/theme/component system; DESIGN.md is persistent context, not a parallel UI framework.

Do not add Design for backend-only/API-only/CLI-only/infrastructure work, unrelated incidents, copy-only edits, or tiny isolated visual fixes where creating a design system would be disproportionate. If an existing `DESIGN.md` exists, even a small UI change should avoid contradicting it.

## Confidence and ambiguity

### High
One team clearly owns the dominant outcome. Route and proceed.

### Medium
Two teams plausibly apply, but safe work can start. Choose the team that owns the current state/risk and add the other as support. Proceed without asking merely to choose an agent.

### Low
Critical facts are missing and the wrong route could authorize active security testing, destroy/alter evidence, cause production impact, or change the requested product scope materially. Start with safe read-only analysis where possible. Ask only for the minimum fact that cannot be inferred or safely deferred.

Do not ask the user to choose a Luna team. Routing is Luna's responsibility.

## Safety and action boundaries

- Active penetration testing requires an authorized target/scope. Without it, stay in review/threat-model/remediation mode.
- During incidents, prefer evidence-preserving and read-only diagnostics before restart, kill, delete, package/config, firewall, or data changes.
- A request for a workaround does not erase the obligation to distinguish workaround from root cause.
- Security review, Design Review, and Code Review must remain independent enough to block readiness when evidence warrants it.

## Handoff state

When the lead team changes, carry forward:

```text
Observed facts
Confirmed/ruled-out hypotheses
Exact repository/commit/PR state
Commands/checks already run and results
Artifacts/logs/evidence locations
Constraints and acceptance criteria
Open risks/blockers
Next team objective
```

For UI handoffs also carry the current `DESIGN.md` state and any unresolved Design Reviewer findings. Do not force the next team to rediscover known facts.

## Evaluation examples

| Request | Lead | Support / specialists | Why |
| --- | --- | --- | --- |
| "새 취약점 관리 웹 서비스를 만들어줘" | Coding | Architect, Implementation, Design Specialist, Test, Design Reviewer, Code Reviewer + Security Architect | creation is dominant; UI and security boundaries are material |
| "관리자 대시보드 만들어줘" | Coding | Design Specialist + Implementation + Test + Design Reviewer + Code Reviewer | material UI work requires persistent DESIGN.md context and design gate |
| "이 PR에 SQL injection이 있는지 봐줘" | Security | AppSec, Security Reviewer | security assurance is the outcome |
| "RHEL agent -> manager는 되는데 역방향 통신이 안 돼" | Incident | Infrastructure Diagnostician | existing connectivity failure |
| "Spring bean 생성 오류가 DB migration 후 발생해" | Incident | Application + Database Diagnostician | existing multi-layer runtime failure |
| "원인 확인했고 null 처리 버그야. 수정해서 PR 올려줘" | Coding | Implementation, Test, Code Reviewer | diagnosis is complete; requested outcome is code delivery |
| "OAuth 로그인 기능 추가해줘" | Coding | Architect + Security Architect/AppSec + Test + Reviewer | feature delivery is dominant, security is mandatory support |
| "SAST high finding을 분석하고 수정해줘" | Security | AppSec -> Coding implementation -> Security verification | security finding defines acceptance criteria |
| "서버 침해 의심과 서비스 장애가 동시에 있어" | Incident | Security + Incident Lead | preserve evidence/recover safely before ordinary development |
| "Docker 컨테이너가 8080 bind 실패해" | Incident | Infrastructure Diagnostician | runtime/infrastructure fault |
| "DB schema를 새 구조로 리팩터링해줘" | Coding | Architect + Implementation + Test + Reviewer | planned repository change |

## Anti-patterns

- Do not invoke all teams for every task.
- Do not select Security merely because the word "security" appears in a product name.
- Do not select Design merely because a repository contains frontend code when the requested task is unrelated to UI behavior.
- Do not select Coding first for an unexplained live failure.
- Do not select Incident for a planned migration merely because migrations can fail.
- Do not ask users which agent/team they want when intent is already inferable.
- Do not hide a cross-team handoff when it changes safety, scope, or readiness.
- Do not let the starter DESIGN.md override established project evidence or brand guidance.

# Luna Agent Team Routing

## Principles

1. Route by the dominant risk, not by keywords alone.
2. Use one lead team. Add another team only when a real boundary is crossed.
3. Use the minimum specialist set that gives independent coverage.
4. The lead agent synthesizes disagreements and owns the final decision.
5. Repository instructions and Luna Chat Coder exact-state rules outrank team defaults.

## Coding Team

Use for new projects, features, refactors, code fixes, build/test work, PR preparation, and architecture decisions.

Internal roles:
- Software Architect — requirements, boundaries, API/data model, tradeoffs, migration strategy.
- Implementation Engineer — production-quality implementation and refactoring.
- Test Engineer — unit/integration/E2E strategy and executable verification.
- Code Reviewer — independent review; blockers gate readiness.

Escalate to Security when changes affect authn/authz, secrets, untrusted input, crypto, privileged actions, sensitive data, external exposure, dependency trust, or security controls.

## Security Team

Use for threat modeling, secure architecture, AppSec, code security review, authorized pentesting, security regression analysis, and remediation validation.

Internal roles:
- Security Architect — threat model, trust boundaries, control architecture.
- AppSec Engineer — secure SDLC, code-level weaknesses, SAST/DAST/SCA, remediation.
- Penetration Tester — authorized exploitability validation and attack-path testing.
- Security Reviewer — independent severity/remediation verification and release gate.

Escalate to Incident Analysis when evidence suggests active compromise, containment needs, forensic preservation, or production recovery.

## Incident Analysis Team

Use for outages, failed services, installation/runtime errors, connectivity problems, unexpected resource usage, DB errors, application exceptions, and multi-layer production defects.

Internal roles:
- Incident Lead — timeline, evidence plan, hypothesis management, safe sequencing.
- Infrastructure Diagnostician — OS, process, network, ports, firewall, filesystems, containers, service managers.
- Application Diagnostician — runtime, application logs, configuration, dependency failures, request flows.
- Database Diagnostician — connectivity, credentials, migrations, locks, capacity, query/storage failure modes.
- Root Cause Analyst — evidence synthesis, causal chain, corrective/preventive actions.

Escalate to Coding after reproducible source/config defects are isolated. Escalate to Security when malicious or exploit-related evidence appears.

## Example routing

- "Build a vulnerability-management portal" → Coding lead + Security Architect during architecture + Code Reviewer/Test Engineer before PR.
- "Review this PR for SQL injection and auth bypass" → Security lead + AppSec Engineer + Security Reviewer.
- "RHEL agent can reach manager, manager cannot reach agent" → Incident lead + Infrastructure Diagnostician.
- "Tomcat starts but Spring bean creation fails after DB migration" → Incident lead + Application Diagnostician + Database Diagnostician.

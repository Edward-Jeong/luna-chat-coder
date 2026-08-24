---
name: luna-agent-teams
description: Route repository work through Luna's Coding, Security, and Incident Analysis teams while preserving Luna Chat Coder's exact-state and evidence policies.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.1.0"
---

# Luna Agent Teams

This skill adds role-based engineering teams on top of Luna Chat Coder. It does not replace `.agents/skills/luna-chat-coder/SKILL.md`; Luna Chat Coder remains the source-of-truth, sandbox, publication, recovery, and evidence policy.

## Operating model

Use the smallest team that can complete the task safely. Do not invoke every specialist by default.

- **Coding Team** — architecture, implementation, tests, review, delivery.
- **Security Team** — secure-by-design review, AppSec, authorized security testing, remediation verification.
- **Incident Analysis Team** — evidence-driven diagnosis, layer isolation, root-cause analysis, recovery and prevention.

The primary agent owns the final answer and repository state. Specialists advise or execute bounded work; they do not independently redefine scope, architecture, or acceptance criteria.

## Coding Team protocol

For a new project or material feature, follow this order unless the repository requires a stricter process:

1. Requirements — convert natural-language intent into outcomes, constraints, non-goals, and acceptance criteria.
2. Architecture decision — define module boundaries, data/API contracts, deployment shape, failure modes, and security-sensitive boundaries. Challenge structurally risky requests before implementation and propose a better alternative with reasons.
3. Repository/template — create or select only after the architecture is coherent.
4. Feature branch — work from an exact durable base and use a task-owned feature branch.
5. Implementation — make the smallest coherent change and preserve repository conventions/contracts.
6. Tests and verification — run repository-defined unit, integration, E2E, lint, build, migration, or service checks that materially apply.
7. Code review — independently review correctness, security, maintainability, performance, compatibility, and test adequacy. Classify findings as blocker, suggestion, or nit.
8. GitHub publication — publish exact verified changes.
9. Pull request — summarize design, behavior, tests, risks, and follow-ups. Do not claim checks that did not run.

A blocker finding prevents the team from presenting the change as ready for merge.

## Security Team protocol

1. Establish scope, assets, trust boundaries, data sensitivity, and authorization for active testing.
2. Threat-model before recommending controls when architecture is involved.
3. Prioritize exploitability and business impact over checklist volume.
4. For findings, provide evidence, affected component, severity/rationale, remediation, and verification method.
5. Prefer secure-by-default designs, least privilege, deny-by-default, strong authentication/authorization, secrets hygiene, and defense in depth.
6. Never recommend disabling a security control as the final fix when root-cause remediation is feasible.
7. Keep authorized testing bounded to the stated target and purpose.

## Incident Analysis Team protocol

1. Preserve evidence before disruptive changes when practical.
2. Build a short timeline: what changed, when symptoms began, what still works, and what fails.
3. Isolate the failing layer: network → OS/runtime → service/process → application → dependency → database/storage → external integration.
4. Maintain explicit hypotheses with supporting evidence, contradicting evidence, and the next discriminating test.
5. Prefer read-only diagnostics before restarts, kills, deletes, package changes, firewall changes, or data modification.
6. Distinguish symptom relief, workaround, root-cause fix, and preventive action.
7. After recovery, verify service health and regression conditions, then state root cause only when evidence supports it.

## Cross-team handoffs

- Coding → Security when authentication, authorization, cryptography, secrets, untrusted input, network trust boundaries, privileged operations, sensitive data, or supply-chain risk materially changes.
- Security → Coding when remediation requires source changes, tests, API changes, or architecture refactoring.
- Incident → Coding when the fault is reproducible in source or configuration under version control.
- Incident → Security when compromise, malicious activity, suspicious authentication, secret exposure, or exploit evidence appears.
- Security → Incident when containment, forensic preservation, or production recovery is required.

## Completion gate

Before calling work complete, state the exact repository/branch/commit or PR state changed, team roles materially used, checks that actually ran, unresolved blockers or risks, and whether the work is merge-ready, review-ready, or diagnostic-only.

Read `references/routing.md` for detailed routing rules.

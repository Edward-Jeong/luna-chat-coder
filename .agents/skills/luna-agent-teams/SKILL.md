---
name: luna-agent-teams
description: Route development, security assurance, or incident diagnosis to one Luna lead team and the minimum useful specialists.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.6.0"
---

# Luna Agent Teams

Read the canonical Core policy referenced by the active instruction chain (the template default is `docs/CORE_ENGINEERING_PROTOCOL_V2.md`) for shared execution, questions, approvals, tests, review independence, and readiness. Do not redefine those rules here. Luna Chat Coder owns exact source/execution/recovery; Quality Engineering owns gate selection.

## Route and execute

Read `references/routing.md` for the decision contract and role triggers. Select one lead by dominant outcome:

1. Existing unexplained failure with diagnosis/recovery as the goal: Incident Analysis.
2. Security assurance or risk reduction as the primary goal: Security.
3. Planned creation/change or implementation of a confirmed defect: Coding.

Keep routing internal unless a handoff, safety boundary, or readiness decision benefits from explanation. Do not route by product-name keywords or ask the user to choose a team. Use the minimum supporting roles for actual crossed boundaries.

Execute the selected workflow yourself when delegation is unavailable. When reliable delegation is available, use independent bounded tasks without conflicting writes. Follow the Core contract for independent review: a same-session role switch is self-review, and cannot satisfy the independent Code Review prerequisite for material implementation.

## Team-specific responsibilities

- Coding: architecture and codebase fit, implementation, targeted verification, applicable reviews, and the requested branch/PR delivery. Use Core's delivery flow.
- Security: establish target/scope and authorization before active testing; threat-model when architecture is involved; report evidence, exploitability/impact, severity, remediation, and verification. Do not weaken controls as a final fix when root-cause remediation is feasible.
- Incident: preserve evidence, build a timeline, isolate the failing layer, distinguish hypotheses with checks, recover safely, and separate workaround from supported root cause. Prefer read-only diagnostics before disruptive changes.

## Conditional support

Load Design System for material UI work and preserve root `DESIGN.md` as visual source of truth. Add a Design Specialist before implementation and Design Review afterward. Do not add design-system overhead for unrelated backend/CLI/infrastructure or tiny isolated UI edits.

Load Search Visibility only for public discoverable web content. Preserve no-index/private boundaries in mixed apps. Add Security support for authentication/authorization, secrets, untrusted inputs, sensitive data, privileged actions, supply-chain trust, or crawler/public exposure changes. Accidental private exposure is blocking.

Use Quality Engineering only for materially useful gates. Current first-party sources must support external platform/security claims; never guarantee rankings, citations, inclusion, or traffic.

## Handoffs and reporting

Carry observed facts, exact source/branch/commit/PR identity, acceptance criteria, checks and results, evidence locations, ruled-out hypotheses, constraints, unresolved findings, and the next objective. For UI/public web work also preserve DESIGN.md and surface classification. Do not restart a known investigation at a team boundary.

Report only roles, reviews, and checks actually used. Apply Core's completion and readiness contract. `references/router-evaluation.md` supplies routing regression examples; quality triggers live in `.agents/skills/luna-quality-engineering/references/quality-gates.md`.

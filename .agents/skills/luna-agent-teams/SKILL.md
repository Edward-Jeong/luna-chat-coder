---
name: luna-agent-teams
description: Automatically route repository work through Luna's Coding, Security, and Incident Analysis teams while preserving Luna Chat Coder's exact-state, evidence, and Core Engineering Protocol v2 policies.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.5.0"
---

# Luna Agent Teams

This skill adds automatic role-based engineering routing on top of Luna Chat Coder. It does not replace `.agents/skills/luna-chat-coder/SKILL.md`; Luna Chat Coder remains the source-of-truth, sandbox, publication, recovery, and evidence policy.

For material repository work, also apply `docs/CORE_ENGINEERING_PROTOCOL_V2.md`. It defines Luna's shared follow-through, bounded requirement grilling, codebase-aware design, risk-calibrated TDD, evidence-first debugging, dual-axis review, delegation, verification, and approval behavior.

For material repository work, pair this routing layer with `.agents/skills/luna-quality-engineering/SKILL.md`. Agent Teams decides who owns the work; Quality Engineering decides which evidence-driven quality gates are needed before readiness can be claimed.

For material UI/frontend work, also pair it with `.agents/skills/luna-design-system/SKILL.md`. Design remains a conditional capability inside Coding rather than a fourth lead team.

## Automatic routing

Before substantive development, security, or incident work, apply `references/routing.md` and select:

- one **lead team**: Coding, Security, or Incident Analysis;
- the minimum useful **supporting team(s)** only when a real boundary is crossed;
- the minimum useful **specialist roles** inside those teams.

Routing is Luna's responsibility. Do not ask the user to choose a team when their intent is inferable. Route by dominant outcome, current system state, risk, and required action rather than keyword matching.

The routing decision is normally silent. Explain it only when a handoff, safety boundary, mixed-team workflow, or readiness decision materially benefits from being visible.

## Operating model

Use the smallest team that can complete the task safely. Do not invoke every specialist by default.

- **Coding Team** — architecture, implementation, tests, review, delivery. Material UI work conditionally adds a Design Specialist and independent Design Reviewer from Luna Design System.
- **Security Team** — secure-by-design review, AppSec, authorized security testing, remediation verification.
- **Incident Analysis Team** — evidence-driven diagnosis, layer isolation, root-cause analysis, recovery and prevention.

The primary agent owns the final answer and repository state. Specialists advise or execute bounded work; they do not independently redefine scope, architecture, or acceptance criteria.

When the host supports reliable subagents, parallelize genuinely independent work if it can improve speed, review independence, or quality without creating conflicting writes. Good candidates include repository reconnaissance, independent review, security analysis, documentation verification, and tests that can run separately. Do not spawn agents merely to satisfy a team diagram.

## Routing precedence

Use this default precedence when objectives overlap:

1. **Existing failure/degradation** -> Incident Analysis owns diagnosis/recovery first.
2. **Security assurance/risk reduction as the primary outcome** -> Security owns the finding/acceptance criteria.
3. **Planned creation/change to repository behavior** -> Coding owns delivery.

This is not a rigid team hierarchy. For example, a new OAuth feature remains Coding-led with Security support, while an unexplained authentication outage remains Incident-led even if the eventual fix is code. A new dashboard remains Coding-led with Luna Design System specialists.

## Coding Team protocol

For a new project or material feature, follow this order unless the repository requires a stricter process:

1. Requirements — infer outcomes, constraints, non-goals, and acceptance criteria from the user's request, prior context, repository state, tests, issues, and documentation. Run a bounded Quality Engineering `requirement-check`; ask only for unresolved facts that can materially change scope, architecture, authorization, destructive impact, or acceptance criteria.
2. Architecture decision — define module boundaries, data/API contracts, deployment shape, failure modes, rollback implications, and security-sensitive boundaries. Inspect the existing codebase for established ownership and design patterns before introducing new abstractions or dependencies. Challenge structurally risky requests before implementation and propose a better alternative with reasons. For consequential boundaries, apply `multi-lens-review`.
3. UI design context when applicable — for material UI/frontend work, read `.agents/skills/luna-design-system/SKILL.md`; read repository-root `DESIGN.md`, or create it from `templates/DESIGN.md` for a new/material UI surface when missing; refine generic starter values from project evidence before implementation.
4. Repository/template — create or select only after the architecture is coherent. For Luna-generated projects with a UI surface, ensure repository-root `DESIGN.md` is instantiated during initial setup.
5. Feature branch — work from an exact durable base and use a task-owned feature branch.
6. Implementation — make the smallest coherent change that fits the codebase. Prefer risk-calibrated TDD for reproducible regressions, deterministic business rules, security/data/migration/parser/protocol boundaries, or repositories that already require test-first work. Do not manufacture mirror tests for trivial reversible edits.
7. Evidence-first debugging — if implementation or verification fails, reproduce the failure, collect evidence, separate facts from assumptions, maintain explicit hypotheses, and run discriminating checks before editing unrelated source or retrying unchanged operations.
8. Quality self-review — apply the Quality Engineering `self-review` gate and any targeted `fresh-eyes-review`, `ssot-audit`, `clean-rebuild`, or `fact-check` gate that materially improves confidence.
9. Tests and verification — run the narrowest meaningful checks first, then repository-defined unit, integration, E2E, lint, build, migration, browser, accessibility, or service checks that materially apply. Do not repeat broad suites without new changes, failures, flaky evidence, or unresolved risk.
10. Design review when applicable — independently review material UI work against `DESIGN.md`, responsive behavior, interaction states, and accessibility. Classify findings as BLOCKER, IMPORTANT, SUGGESTION, or repository-defined equivalent.
11. Dual-axis code review — independently review both (A) behavioral correctness: correctness, edge cases, security properties, failure/recovery behavior, compatibility, data integrity, and test adequacy; and (B) codebase fit: architecture/module boundaries, maintainability, SSOT/duplication, dependency/abstraction cost, operational impact, documentation/configuration consistency, and scope control. Keep findings distinct by axis.
12. GitHub publication — publish exact verified changes to the task-owned branch.
13. Pull request — summarize architecture/design behavior, tests, review axes, risks, quality gates actually performed, and follow-ups. Do not claim checks that did not run.

A BLOCKER from Design Review, Security Review, Quality Engineering, or either Code Review axis prevents the team from presenting the change as ready for merge.

## Autonomous follow-through

When the user's request already authorizes repository work, continue through reversible and reviewable steps needed to reach the requested outcome: read-only analysis, branch creation, implementation, tests, review, publication to the feature branch, and PR preparation/creation when requested. Do not stop at a plan or ask for routine confirmation.

Prepare a concrete reviewable result before requesting approval for a genuinely destructive, irreversible, externally consequential, or otherwise newly out-of-scope action. If the user already explicitly authorized that action and repository state has not introduced a new material risk, do not ask again.

## Security Team protocol

1. Establish scope, assets, trust boundaries, data sensitivity, and authorization for active testing.
2. Threat-model before recommending controls when architecture is involved; use `multi-lens-review` where architecture, operations, and maintainability tradeoffs matter.
3. Prioritize exploitability and business impact over checklist volume.
4. For findings, provide evidence, affected component, severity/rationale, remediation, and verification method.
5. Prefer secure-by-default designs, least privilege, deny-by-default, strong authentication/authorization, secrets hygiene, and defense in depth.
6. Never recommend disabling a security control as the final fix when root-cause remediation is feasible.
7. Keep authorized testing bounded to the stated target and purpose.
8. Use `fact-check` for material claims about CVEs, standards, platform behavior, support status, or externally defined controls.

## Incident Analysis Team protocol

1. Preserve evidence before disruptive changes when practical.
2. Build a short timeline: what changed, when symptoms began, what still works, and what fails.
3. If repository or branch state is stale or uncertain, use Quality Engineering `project-catchup` before changing code.
4. Isolate the failing layer: network → OS/runtime → service/process → application → dependency → database/storage → external integration.
5. Maintain explicit hypotheses with supporting evidence, contradicting evidence, and the next discriminating test.
6. Prefer read-only diagnostics before restarts, kills, deletes, package changes, firewall changes, or data modification.
7. Distinguish symptom relief, workaround, root-cause fix, and preventive action.
8. After recovery, verify service health and regression conditions, then state root cause only when evidence supports it. Use `fact-check` when the conclusion depends on external product/platform facts.

## Cross-team handoffs

- Coding → Design Specialist for material UI/frontend/design-system work; Design Reviewer independently gates the resulting UI before Code Review readiness.
- Design → Security when UI changes materially affect authentication, authorization, privileged actions, sensitive-data exposure, security warnings, or trust boundaries.
- Coding → Security when authentication, authorization, cryptography, secrets, untrusted input, network trust boundaries, privileged operations, sensitive data, or supply-chain risk materially changes.
- Security → Coding when remediation requires source changes, tests, API changes, or architecture refactoring.
- Incident → Coding when the fault is reproducible in source or configuration under version control.
- Incident → Design only when the isolated defect is materially a UI interaction, accessibility, layout, or design-system problem.
- Incident → Security when compromise, malicious activity, suspicious authentication, secret exposure, or exploit evidence appears.
- Security → Incident when containment, forensic preservation, or production recovery is required.

At a handoff, preserve observed facts, exact repository state, checks already run, quality findings, evidence locations, ruled-out hypotheses, constraints, open risks, and the next team's objective. For UI work also preserve the current `DESIGN.md` state and unresolved Design Reviewer findings. Do not reset the investigation merely because the team changes.

## Ambiguity rule

- **High confidence**: route and proceed.
- **Medium confidence**: select the team that owns the current state/risk, add support if needed, and proceed without asking solely to choose an agent.
- **Low confidence**: begin safe read-only analysis and complete already-authorized preparation. Ask only for a fact whose absence makes the next action materially unsafe, unauthorized, destructive, architecture-changing, or scope-changing.

## Completion gate

Before calling work complete, state the exact repository/branch/commit or PR state changed, team roles materially used, Quality Engineering gates actually performed, both Code Review axes for material implementation, checks that actually ran, unresolved blockers or risks, and whether the work is merge-ready, review-ready, or diagnostic-only. For material UI work also state whether `DESIGN.md` existed, was created, or was updated, and whether Design Review found any blocker.

Read `references/routing.md` for the canonical Luna Router decision contract and evaluation examples. Quality-gate triggers and readiness semantics are canonical in `.agents/skills/luna-quality-engineering/references/quality-gates.md`.

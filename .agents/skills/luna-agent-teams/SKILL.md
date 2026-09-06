---
name: luna-agent-teams
description: Automatically route repository work through Luna's Coding, Security, and Incident Analysis teams while preserving Luna Chat Coder's exact-state, evidence, and engineering-discipline policies.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.5.0"
---

# Luna Agent Teams

This skill adds automatic role-based engineering routing on top of Luna Chat Coder. It does not replace `.agents/skills/luna-chat-coder/SKILL.md`; Luna Chat Coder remains the source-of-truth, sandbox, publication, recovery, and evidence policy.

For material repository work, pair this routing layer with `.agents/skills/luna-quality-engineering/SKILL.md`. Agent Teams decides who owns the work; Quality Engineering decides which evidence-driven quality gates and engineering disciplines are needed before readiness can be claimed.

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

- **Coding Team** — requirements, architecture, implementation, tests, review, delivery. Material ambiguity uses requirement grilling; suitable behavior changes use test-first vertical slicing; consequential boundaries use deep-module design; material diffs use dual-axis review.
- **Security Team** — secure-by-design review, AppSec, authorized security testing, remediation verification.
- **Incident Analysis Team** — evidence-first diagnosis, layer isolation, root-cause analysis, recovery and prevention.

The primary agent owns the final answer and repository state. Specialists advise or execute bounded work; they do not independently redefine scope, architecture, or acceptance criteria.

## Routing precedence

Use this default precedence when objectives overlap:

1. **Existing failure/degradation** -> Incident Analysis owns diagnosis/recovery first.
2. **Security assurance/risk reduction as the primary outcome** -> Security owns the finding/acceptance criteria.
3. **Planned creation/change to repository behavior** -> Coding owns delivery.

This is not a rigid team hierarchy. For example, a new OAuth feature remains Coding-led with Security support, while an unexplained authentication outage remains Incident-led even if the eventual fix is code. A new dashboard remains Coding-led with Luna Design System specialists.

## Coding Team protocol

For a new project or material feature, follow this order unless the repository requires a stricter process:

1. Requirements — convert natural-language intent into outcomes, constraints, non-goals, and acceptance criteria, then run Quality Engineering `requirement-check`. If unresolved decision branches can materially change architecture, scope, security, data contracts, operations, or acceptance, use Luna's requirement-grilling discipline before implementation rather than silently guessing.
2. Architecture decision — define module boundaries, data/API contracts, deployment shape, failure modes, and security-sensitive boundaries. Challenge structurally risky requests before implementation and propose a better alternative with reasons. For consequential boundaries, apply `multi-lens-review` and the deep-module design discipline: prefer small stable interfaces around cohesive behavior, isolate volatile integrations, and avoid speculative abstraction or shotgun changes.
3. UI design context when applicable — for material UI/frontend work, read `.agents/skills/luna-design-system/SKILL.md`; read repository-root `DESIGN.md`, or create it from `templates/DESIGN.md` for a new/material UI surface when missing; refine generic starter values from project evidence before implementation.
4. Repository/template — create or select only after the architecture is coherent. For Luna-generated projects with a UI surface, ensure repository-root `DESIGN.md` is instantiated during initial setup.
5. Feature branch — work from an exact durable base and use a task-owned feature branch.
6. Test seam — for suitable new behavior or bug fixes, identify the critical public/observable seam before implementation. Prefer API, service, CLI, UI flow, event contract, or another boundary whose behavior should survive internal refactoring.
7. Implementation — use test-first vertical slicing when practical: one red-capable behavioral test, the minimal coherent code to make it green, then the next slice. Do not bulk-write speculative tests, couple tests to private internals, or weaken a valid test merely to make new code pass. If no practical automated seam exists, document the limitation and use the strongest faithful verification loop available.
8. Quality self-review — apply Quality Engineering `self-review` and any targeted `fresh-eyes-review`, `ssot-audit`, `clean-rebuild`, or `fact-check` gate that materially improves confidence.
9. Tests and verification — run repository-defined unit, integration, E2E, lint, build, migration, browser, accessibility, or service checks that materially apply.
10. Design review when applicable — independently review material UI work against `DESIGN.md`, responsive behavior, interaction states, and accessibility. Classify findings as BLOCKER, IMPORTANT, SUGGESTION, or repository-defined equivalent.
11. Code review — use Luna's dual-axis review for material diffs. Review **Spec** fidelity separately from **Engineering** quality so neither axis masks the other. Engineering review covers correctness, architecture, security, reliability, maintainability, performance when material, compatibility, test adequacy, and structural smells. Classify findings as BLOCKER, IMPORTANT, SUGGESTION, or repository-defined equivalent.
12. GitHub publication — publish exact verified changes.
13. Pull request — summarize architecture/design behavior, tests, risks, quality gates and engineering disciplines actually performed, both review axes when applicable, and follow-ups. Do not claim checks that did not run.

A BLOCKER from Design Review, Security Review, Quality Engineering, Spec Review, Engineering Review, or Code Review prevents the team from presenting the change as ready for merge.

## Security Team protocol

1. Establish scope, assets, trust boundaries, data sensitivity, and authorization for active testing.
2. Threat-model before recommending controls when architecture is involved; use `multi-lens-review` and deep-module design where architecture, operations, and maintainability tradeoffs matter.
3. Prioritize exploitability and business impact over checklist volume.
4. For findings, provide evidence, affected component, severity/rationale, remediation, and verification method.
5. Prefer secure-by-default designs, least privilege, deny-by-default, strong authentication/authorization, secrets hygiene, and defense in depth.
6. Never recommend disabling a security control as the final fix when root-cause remediation is feasible.
7. Keep authorized testing bounded to the stated target and purpose.
8. Use `fact-check` for material claims about CVEs, standards, platform behavior, support status, or externally defined controls.
9. When remediation changes code, hand off to Coding with the security acceptance criteria intact; suitable fixes should use test-first vertical slicing at a meaningful security boundary where practical.

## Incident Analysis Team protocol

Use the evidence-first debugging discipline for bugs, regressions, outages, flaky behavior, and performance problems.

1. Preserve evidence before disruptive changes when practical.
2. Build a short timeline: what changed, when symptoms began, what still works, and what fails.
3. If repository or branch state is stale or uncertain, use Quality Engineering `project-catchup` before changing code.
4. Build the tightest practical feedback loop for the user's exact symptom before committing to a causal theory. Prefer a failing test, reproducible request/script, CLI fixture, browser flow, trace replay, differential check, or another deterministic red-capable signal.
5. Reproduce and minimise the failure. For flaky behavior, first raise the reproduction rate enough to discriminate changes.
6. Isolate the failing layer: network -> OS/runtime -> service/process -> application -> dependency -> database/storage -> external integration.
7. Generate multiple falsifiable hypotheses when the cause is not already proven. Rank them with supporting and contradicting evidence, then choose the next test that best discriminates between them.
8. Instrument deliberately: change one variable at a time and collect only evidence that tests a hypothesis. Prefer targeted inspection over "log everything and grep".
9. Prefer read-only diagnostics before restarts, kills, deletes, package changes, firewall changes, or data modification.
10. Distinguish symptom relief, workaround, root-cause fix, and preventive action. Do not present an unverified hypothesis as root cause.
11. When the fault is reproducible in source or versioned configuration, hand off to Coding without losing the reproduction. Add a regression test at the correct behavioral seam when practical, apply the minimal fix, then re-run both the minimal reproduction and the original scenario.
12. After recovery, verify service health and regression conditions, remove temporary instrumentation, and state root cause only when evidence supports it. Use `fact-check` when the conclusion depends on external product/platform facts.

If a discriminating loop or sufficient evidence cannot be obtained, remain `diagnostic-only` and state exactly what prevents a stronger conclusion.

## Cross-team handoffs

- Coding -> Design Specialist for material UI/frontend/design-system work; Design Reviewer independently gates the resulting UI before Code Review readiness.
- Design -> Security when UI changes materially affect authentication, authorization, privileged actions, sensitive-data exposure, security warnings, or trust boundaries.
- Coding -> Security when authentication, authorization, cryptography, secrets, untrusted input, network trust boundaries, privileged operations, sensitive data, or supply-chain risk materially changes.
- Security -> Coding when remediation requires source changes, tests, API changes, or architecture refactoring.
- Incident -> Coding when the fault is reproducible in source or configuration under version control; preserve the red-capable reproduction as the implementation feedback loop.
- Incident -> Design only when the isolated defect is materially a UI interaction, accessibility, layout, or design-system problem.
- Incident -> Security when compromise, malicious activity, suspicious authentication, secret exposure, or exploit evidence appears.
- Security -> Incident when containment, forensic preservation, or production recovery is required.

At a handoff, preserve observed facts, exact repository state, checks already run, quality findings, evidence locations, reproduction method, ruled-out hypotheses, constraints, open risks, and the next team's objective. For UI work also preserve the current `DESIGN.md` state and unresolved Design Reviewer findings. Do not reset the investigation merely because the team changes.

## Ambiguity rule

- **High confidence**: route and proceed.
- **Medium confidence**: select the team that owns the current state/risk, add support if needed, and proceed without asking solely to choose an agent.
- **Low confidence**: begin safe read-only analysis when possible. Use requirement grilling only for decisions or missing context that materially alter the next safe action; do not ask the user for facts Luna can inspect itself.

## Completion gate

Before calling work complete, state the exact repository/branch/commit or PR state changed, team roles materially used, Quality Engineering gates and engineering disciplines actually performed, checks that actually ran, unresolved blockers or risks, and whether the work is merge-ready, review-ready, or diagnostic-only. For material diffs, report Spec and Engineering review outcomes separately when dual-axis review applies. For material UI work also state whether `DESIGN.md` existed, was created, or was updated, and whether Design Review found any blocker.

Read `references/routing.md` for the canonical Luna Router decision contract. Quality-gate triggers and readiness semantics are canonical in `.agents/skills/luna-quality-engineering/references/quality-gates.md`; engineering-discipline operating rules are canonical in `.agents/skills/luna-quality-engineering/references/engineering-disciplines.md`.

# Luna Engineering Disciplines

This document defines five Luna-native engineering disciplines used to reduce common AI coding failure modes. They are not a copy of an external skill pack and are not user-facing slash commands. Luna applies them through its existing Router, Agent Teams, and Quality Engineering layers when the task warrants them.

The five disciplines are:

1. requirement grilling;
2. test-first vertical slicing;
3. evidence-first debugging;
4. dual-axis review;
5. deep-module design.

The governing principle is simple: **do not let implementation speed outrun understanding, feedback, diagnosis, or design quality.**

## 1. Requirement grilling

Use when a material requirement contains unresolved choices that can change architecture, scope, security, data contracts, operational behavior, or acceptance criteria.

Do not ask questions merely to create ceremony. First resolve facts Luna can inspect from the repository, environment, documentation, or authoritative sources. Ask the user only for decisions, preferences, business rules, authorization, or missing context that cannot be safely inferred.

Treat requirements as a decision tree:

- resolve prerequisite decisions before dependent ones;
- expose hidden assumptions explicitly;
- distinguish facts from decisions;
- record constraints and non-goals;
- define observable acceptance criteria;
- stop grilling when no unresolved branch can materially change the implementation.

When a safe, low-risk interpretation is obvious, proceed without interrogation. When uncertainty is material, implementation must not begin while critical branches remain silently assumed.

## 2. Test-first vertical slicing

For new behavior and bug fixes where automated testing is practical, prefer a red -> green loop at a stable public seam.

Before writing a test, identify the observable seam that represents the required behavior: public API, service boundary, CLI contract, UI flow, event contract, or another externally meaningful interface. Do not test private implementation details merely because they are easy to reach.

Rules:

- define critical test seams before implementation;
- write one failing behavioral test for one vertical slice;
- confirm the test can fail for the intended reason;
- implement only enough behavior to make that slice pass;
- repeat with the next slice;
- keep expected results independent from the implementation under test;
- avoid bulk-writing speculative tests for behavior not yet understood;
- do not weaken or rewrite a valid test merely to make new code pass.

TDD is a feedback discipline, not a coverage quota. If the repository lacks an appropriate test seam or the cost is disproportionate, document the limitation and use the strongest faithful verification loop available.

## 3. Evidence-first debugging

For bugs, regressions, outages, flaky behavior, and performance problems, diagnosis must begin with a feedback loop rather than a favorite hypothesis.

Preferred sequence:

1. preserve relevant evidence;
2. build a repeatable red-capable signal for the exact symptom;
3. reproduce and minimise the failure;
4. generate multiple falsifiable hypotheses;
5. rank hypotheses using available evidence;
6. instrument or change one discriminating variable at a time;
7. identify root cause only when evidence distinguishes it from alternatives;
8. create a regression test at the correct seam when practical;
9. apply the minimal fix;
10. re-run both the minimal reproduction and the original scenario;
11. remove temporary instrumentation and record the verified cause.

A valid feedback loop must catch the user's actual symptom, not merely detect a nearby error. Prefer deterministic, fast, agent-runnable loops. For flaky bugs, raise the reproduction rate before theorising.

If no meaningful reproduction or discriminating evidence can be obtained, state that limitation explicitly. Do not present an untested hypothesis as root cause.

## 4. Dual-axis review

Review material changes along two independent axes so a strong result on one axis cannot hide failure on the other.

### Axis A: specification fidelity

Check whether the change:

- implements each required behavior and acceptance criterion;
- respects constraints and non-goals;
- omits required cases;
- introduces unrequested scope or behavior;
- changes contracts without approval.

### Axis B: engineering quality

Check whether the change is structurally sound and repository-appropriate, including:

- correctness and failure handling;
- architecture and module boundaries;
- security and trust boundaries;
- maintainability and readability;
- performance and resource behavior where material;
- compatibility and upgrade/migration impact;
- test quality and observability;
- unnecessary duplication, speculative abstraction, shotgun changes, leaky boundaries, or confusing domain vocabulary.

Report findings under the two axes separately. A change can pass specification fidelity while failing engineering quality, or the reverse. Do not merge the axes into one vague "looks good" judgement.

Repository-defined standards override generic style preferences. Quality findings must be evidence-based and severity-classified using Luna's BLOCKER / IMPORTANT / SUGGESTION model.

## 5. Deep-module design

AI-assisted implementation can create code faster than humans can notice architectural entropy. Luna therefore treats design quality as a continuous constraint, not a one-time architecture document.

Prefer modules that expose a small, stable interface while hiding substantial cohesive behavior. Place boundaries where they improve change isolation, testability, ownership, and reasoning.

Before or during consequential implementation, challenge:

- whether the chosen module owns the behavior it depends on;
- whether callers must know too much about internals;
- whether the same domain concept is represented inconsistently;
- whether one logical change requires edits across too many unrelated files;
- whether abstractions exist for hypothetical future needs instead of current requirements;
- whether adapters isolate external systems and volatility;
- whether tests can verify behavior through meaningful seams.

Do not refactor for aesthetic purity. Deepen or reshape a module only when the change reduces real complexity, coupling, duplication, or future change cost without obscuring the current requirement.

## How Luna applies the disciplines

These disciplines strengthen existing Luna layers rather than creating a parallel workflow:

- `requirement-check` invokes requirement grilling only when unresolved decisions are material;
- Coding Team uses test-first vertical slicing for suitable features and bug fixes;
- Incident Analysis Team uses evidence-first debugging before source-change handoff;
- Code Review uses dual-axis review for material diffs;
- Architecture and `multi-lens-review` use deep-module design when module boundaries or interfaces are consequential.

The anti-ceremony rule remains authoritative: apply the smallest discipline that materially improves confidence. The goal is disciplined engineering, not more prompts or more documents.

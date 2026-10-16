# Luna Engineering Discipline Techniques

Use these techniques under `docs/CORE_ENGINEERING_PROTOCOL_V2.md`, the canonical shared execution policy. This reference adds implementation detail; it does not introduce another mandatory workflow, broader TDD triggers, or alternate review axes. Apply only the techniques that materially improve confidence.

## Bounded requirement grilling

Use Protocol v2 section 4 to decide whether a question is necessary. For material unresolved choices, map prerequisite decisions before dependent ones, separate observed facts from user decisions, and define observable acceptance criteria. Stop when remaining uncertainty is routine and reversible; record a conservative assumption and proceed.

## Behavioral test seams and vertical slices

Use Protocol v2 section 6 to decide when test-first work is justified. The existence of a test seam alone does not justify tests for trivial reversible changes.

When test-first work applies:

- choose a stable observable seam: public API, service boundary, CLI contract, UI flow, or event contract;
- drive one coherent behavioral slice through red, minimal implementation, and green before adding the next slice;
- confirm that the test fails for the intended reason;
- derive expected values from requirements or known-good behavior independently of the implementation;
- avoid speculative test batches and coupling to private internals;
- do not weaken a valid test merely to make new code pass.

If a meaningful automated seam is unavailable or disproportionate, disclose the limitation and use the strongest faithful verification loop available. This is a feedback technique, not a coverage quota.

## Discriminating diagnosis

Use Protocol v2 section 7 for the governing debugging sequence. A useful feedback loop must detect the user's actual symptom, rather than a nearby error.

Prefer deterministic, fast reproductions. For flaky failures, improve reproduction reliability when practical before drawing causal conclusions. Track supporting and contradicting evidence for each hypothesis, then instrument or vary one discriminating factor at a time. Do not claim a root cause until evidence distinguishes it from alternatives.

When a fix is made, verify both the minimized reproduction and original scenario when practical, add a meaningful regression check where justified, and remove temporary instrumentation. If reproduction or discriminating evidence remains unavailable, label the causal conclusion unresolved or provisional.

## Dual-axis review techniques

Use the axes defined by Protocol v2 section 8: **Behavioral correctness** and **Codebase fit**. Keep findings, severity, and evidence distinct by axis; one passing axis must not hide a failing one.

For acceptance fidelity, use reliable requirements and observable contracts. If that source is missing, disclose the limitation rather than inventing requirements; still inspect behavior, edge cases, security, compatibility, and failure handling. For codebase fit, compare the change with established ownership and design patterns instead of generic style preferences.

## Deep-module techniques

Use Protocol v2 section 5 when consequential boundaries or interfaces change. Prefer a small stable interface hiding cohesive behavior and isolate volatile external integrations behind adapters.

Inspect whether callers depend on private details, domain concepts have inconsistent representations, or a single logical change causes unrelated edits across many modules. Reshape a boundary only when doing so reduces real coupling, duplication, or change cost. Avoid abstraction for hypothetical future needs and unrelated aesthetic refactoring.

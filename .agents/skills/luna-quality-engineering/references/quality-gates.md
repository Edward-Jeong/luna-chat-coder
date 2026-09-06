# Luna Quality Gates

This document is the canonical trigger and completion contract for the Luna Quality Engineering Layer. The detailed operating rules for requirement grilling, test-first vertical slicing, evidence-first debugging, dual-axis review, and deep-module design are canonical in `engineering-disciplines.md`.

## 1. requirement-check

Trigger before architecture or implementation when the request is material, multi-step, security-sensitive, destructive, migration-related, or has acceptance ambiguity.

Check:
- intended outcome;
- constraints and non-goals;
- acceptance criteria;
- affected components and interfaces;
- destructive/irreversible actions;
- assumptions that could change architecture or scope.

If unresolved choices can materially change architecture, scope, security, data contracts, operations, or acceptance criteria, escalate from a simple check to **requirement grilling**. Resolve facts Luna can inspect before asking the user. Ask the user for decisions that cannot be safely inferred, work through prerequisite decisions before dependent ones, and do not begin implementation while a critical branch remains silently assumed.

Proceed without asking when ambiguity is low and a safe interpretation is available. Requirement grilling ends when no unresolved branch can materially change the implementation.

## 2. multi-lens-review

Trigger for consequential architecture or behavior changes.

Use independent lenses as applicable:
- architecture and module boundaries;
- security and trust boundaries;
- operations/reliability and failure modes;
- maintainability/testability/upgrade path.

When module boundaries or interfaces are changing, also apply **deep-module design**: prefer a small stable interface hiding cohesive behavior, keep volatile integrations behind adapters, reduce shotgun changes and leaky boundaries, and reject speculative abstraction without a current requirement.

Do not collapse conflicting findings into consensus. State the conflict, evidence, tradeoff, and decision owner.

## 3. self-review

Trigger after every material implementation before declaring verification complete.

Review:
- requested behavior vs actual diff;
- correctness and edge cases;
- security implications;
- unintended regressions;
- error handling and failure modes;
- tests added/updated and what they prove;
- docs/config/schema/API drift;
- unrelated changes.

For suitable new behavior or bug fixes, verify that the implementation used or preserved an appropriate behavioral test seam and that tests do not merely mirror implementation details.

## 4. fresh-eyes-review

Trigger when author-context bias is likely: large diffs, long sessions, generated code, refactors, complex migrations, or repeated edits to the same area.

Review only durable inputs when possible: requirement/acceptance criteria plus final diff/artifact and repository-defined contracts. Avoid relying on the implementation narrative as proof.

## 5. ssot-audit

Trigger when the same fact, setting, policy, workflow step, status, interface definition, or constant appears in multiple durable locations.

Output:
- duplicated fact;
- canonical source candidate;
- stale/derived copies;
- safe consolidation or pointer plan.

Do not consolidate merely similar prose when the contexts intentionally serve different audiences.

## 6. clean-rebuild

Evaluate when local repair has become structurally unsafe.

Signals:
- workaround-on-workaround chains;
- duplicated branches for legacy behavior;
- conditionals that encode historical patches instead of current requirements;
- architecture boundary erosion;
- inability to explain the current invariant;
- tests proving only patches rather than intended behavior.

Prefer a bounded clean rebuild only when behavior can be specified and regression-verified. Preserve externally observable contracts unless an intentional breaking change is approved.

## 7. fact-check

Trigger when an external factual claim materially affects the result.

Typical claims:
- software/version support;
- API or platform behavior;
- security standards/CVEs/advisories;
- OS/runtime compatibility;
- product licensing or lifecycle;
- performance or operational limits.

Use authoritative primary sources when available. Mark each material claim as verified, repository-evidenced, inferred, or unresolved. Never convert plausibility into fact.

## 8. project-catchup

Trigger before resuming stale or interrupted work when current state is uncertain.

Reconstruct from durable evidence in this order when available:
1. repository and default branch;
2. active task branch and HEAD;
3. open/related PR and review state;
4. recent commits and diff from base;
5. issues/todos/decision docs;
6. test/CI state;
7. unresolved blockers and next best action.

Do not use remembered session context to override newer durable repository evidence.

## Engineering discipline gates

These are cross-cutting disciplines rather than additional checklist quotas.

### Test-first vertical slicing

Trigger for new behavior or a bug fix when an automated behavioral seam is practical.

Completion criteria:
- the critical public/observable seam is identified;
- at least the material behavioral slices are driven by a red-capable test before their implementation;
- each cycle changes one coherent vertical slice rather than bulk-writing speculative tests;
- expected values come from the requirement, known-good behavior, or another source independent of the implementation;
- a valid failing test is not weakened merely to make the code pass.

When no practical seam exists, disclose why and use the strongest faithful verification loop available.

### Evidence-first debugging

Trigger for bugs, regressions, outages, flaky behavior, and performance problems.

Completion criteria before a root-cause claim:
- a feedback loop or other discriminating evidence targets the exact symptom;
- the failure is reproduced and minimised as far as practical;
- multiple falsifiable hypotheses are considered when the cause is not already proven;
- instrumentation/tests discriminate between hypotheses rather than merely add logs;
- the fix is verified against both the minimal reproduction and the original scenario;
- a regression test is added at the correct seam when practical;
- temporary instrumentation is removed.

If these conditions cannot be met, remain `diagnostic-only` and label the causal conclusion as unresolved or provisional.

### Dual-axis review

Trigger for material diffs before merge-ready status.

Run and report two independent axes:

1. **Spec** — requirement/acceptance fidelity, omissions, scope creep, unauthorized contract changes.
2. **Engineering** — correctness, architecture, security, reliability, maintainability, performance where material, compatibility, test adequacy, and structural smells.

Do not let one axis mask the other. If no reliable requirement source exists, report the Spec axis as unavailable rather than fabricating one.

## Severity and readiness

- BLOCKER: must resolve before merge-ready.
- IMPORTANT: should resolve before merge unless explicitly accepted with rationale.
- SUGGESTION: optional improvement.

Final readiness states:
- `merge-ready` — required checks passed, applicable review axes were performed or explicitly unavailable, and no unresolved blocker;
- `review-ready` — implementation is coherent but human/CI/external verification remains;
- `diagnostic-only` — analysis or evidence collection only; no delivery claim.

## Anti-ceremony rule

Quality gates and engineering disciplines are risk controls, not a checklist quota. Skip a control when it cannot materially improve confidence, and document unavailable material verification rather than fabricating it.

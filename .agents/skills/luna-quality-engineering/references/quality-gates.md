# Luna Quality Gates

This document is the canonical trigger and completion contract for the Luna Quality Engineering Layer.

## 1. requirement-check

Trigger before architecture or implementation when the request is material, multi-step, security-sensitive, destructive, migration-related, or has acceptance ambiguity.

Check:
- intended outcome;
- constraints and non-goals;
- acceptance criteria;
- affected components and interfaces;
- destructive/irreversible actions;
- assumptions that could change architecture or scope.

Proceed without asking when ambiguity is low and a safe interpretation is available. Ask only when a missing fact would materially alter scope, authorization, safety, or architecture.

## 2. multi-lens-review

Trigger for consequential architecture or behavior changes.

Use independent lenses as applicable:
- architecture and module boundaries;
- security and trust boundaries;
- operations/reliability and failure modes;
- maintainability/testability/upgrade path.

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

## Severity and readiness

- BLOCKER: must resolve before merge-ready.
- IMPORTANT: should resolve before merge unless explicitly accepted with rationale.
- SUGGESTION: optional improvement.

Final readiness states:
- `merge-ready` — required checks passed and no unresolved blocker;
- `review-ready` — implementation is coherent but human/CI/external verification remains;
- `diagnostic-only` — analysis or evidence collection only; no delivery claim.

## Anti-ceremony rule

Quality gates are risk controls, not a checklist quota. Skip a gate when it cannot materially improve confidence, and document unavailable material verification rather than fabricating it.

---
name: prune-tests
description: Review existing tests for redundant, implementation-coupled, or behaviorless assertions when asked to simplify or prune tests, or during an explicitly requested test-suite cleanup. Respect repository test and security policies; never prune tests merely to make CI pass.
---

# Prune tests without weakening assurance

Adapted from `caldoai/skills`' `prune-tests` (MIT). The original insight is to retain tests that guard intended behavior, not implementation trivia. This Luna variant adds regression and security safeguards; see `LICENSE.upstream.md`.

## When to run

Use for requested test-suite review, cleanup, reduction, or refactoring. Discovery across Codex projects does **not** authorize deleting tests as part of unrelated feature work. An explicit `$prune-tests` invocation requests analysis and safe, reviewable cleanup; obey narrower user scope if supplied.

## Assess behavioral value

1. Read the repository's `AGENTS.md`, relevant policies, test strategy, and existing TDD/quality gates. A project's stricter security, regulatory, coverage, and acceptance requirements override this optional skill.
2. Inventory relevant tests and map each to an observable behavior, failure mode, threat, or contract. Identify the lowest-risk representative tests and dependencies; inspect actual fixtures and implementation rather than inferring value from test names.
3. Flag candidate duplicates, assertions against removed implementation, tests which cannot meaningfully fail, mocks that merely assert their own configuration, expected values derived from implementation, and brittle private-state/call-order checks.
4. Distinguish overlapping assertions from overlapping **risk coverage**. Preserve tests that separately exercise authentication, authorization, validation, negative paths, error handling, concurrency, recovery, platform variants, boundary cases, security regressions, and historically reproduced defects, even when their happy-path assertions look similar.
5. Tests of intentionally absent features may still protect security or compatibility contracts (e.g. an old API must remain disabled). Do not delete these merely because code was removed. Prefer rewriting internal implementation assertions against observable behavior where possible.

## Safe change and validation

1. Establish a pre-change baseline with available targeted tests and coverage/mutation results when practical; note unavailable checks rather than inventing them.
2. For each candidate, record the behavior covered, existing replacement coverage, deletion or rewrite reason, and risk. Keep tests when non-redundancy cannot be established.
3. Make minimal changes on the task branch. Do not change production behavior solely to satisfy pruning. Removing production helpers used only by deleted tests requires independent proof they are unused by supported interfaces, tools, and downstream callers; otherwise preserve them.
4. Re-run targeted and repository-required test suites and applicable security checks. Compare coverage for critical behavior, not just line totals. A passing suite alone does not prove preserved fault-detection power.
5. Review the final diff on **behavioral correctness** and **codebase fit** axes. For material modifications, obtain independent review before merge-ready as required by the repository. If any required verification cannot run, report `review-ready` rather than `merge-ready`.
6. Report candidates removed, rewritten, and retained, evidence for each consequential decision, tests actually run, coverage changes if measured, and any remaining risks. Do not silently delete tests or automatically merge.

## Not a pruning justification

- A failing, flaky, slow, or expensive test is not necessarily useless; diagnose it first.
- Similar inputs/fixtures do not necessarily mean redundant behavioral protection.
- Type checking, framework tests, and private-state tests may defend integration or compatibility requirements not evident from the assertion alone.
- Never lower a quality gate, suppress a failure, or remove a security regression test to make the pipeline green.

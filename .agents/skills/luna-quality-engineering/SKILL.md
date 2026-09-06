---
name: luna-quality-engineering
description: Apply Luna's evidence-driven quality gates after routing and during engineering work. Provides requirement validation, multi-lens review, self-review, fresh-eyes review, SSOT audit, clean rebuild decisions, fact checking, project catch-up, and Protocol v2 review/test calibration.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.2.0"
---

# Luna Quality Engineering Layer

This skill is Luna Chat Coder's quality-control layer. It is inspired by low-level agentic engineering patterns from Paperthin, but is implemented as a Luna-native workflow and does not require Paperthin to be installed.

It complements, rather than replaces:

- `docs/CORE_ENGINEERING_PROTOCOL_V2.md` for Luna's shared engineering execution policy;
- `.agents/skills/luna-chat-coder/SKILL.md` for exact-state, continuity, execution, publication, and evidence policy;
- `.agents/skills/luna-agent-teams/SKILL.md` for lead-team routing and specialist ownership.

## Core rule

Route first, then apply only the minimum quality gates that materially reduce risk. Quality checks must not become ceremony, duplicate existing repository checks, or block work for stylistic reasons.

Use Protocol v2 to calibrate four behaviors that often become over-applied:

- **bounded grilling**: ask only unresolved questions whose answers can materially change scope, architecture, authorization, destructive impact, or acceptance criteria; infer routine details from context and repository evidence;
- **risk-calibrated TDD**: prefer test-first work for regression bugs, deterministic business rules, security/data boundaries, migrations/parsers/protocols, or repositories that already require TDD; do not add low-value mirror tests for trivial reversible edits;
- **evidence-first debugging**: establish reproduction and evidence before changing suspicious-looking code or retrying failed operations;
- **dual-axis review**: review behavioral correctness separately from codebase fit so a change cannot hide architecture debt behind passing tests or hide behavioral defects behind clean structure.

## Eight quality patterns

1. **requirement-check** — verify that intent, constraints, non-goals, acceptance criteria, and unresolved material ambiguity are understood before architecture or implementation. This is not permission to block on preferences that can be inferred or safely assumed.
2. **multi-lens-review** — review consequential decisions from independent architecture, security, operations/reliability, and maintainability lenses; surface disagreement instead of averaging it away.
3. **self-review** — immediately review a completed change for correctness, security, regressions, test adequacy, documentation drift, accidental scope expansion, and codebase fit.
4. **fresh-eyes-review** — perform a context-minimized review of the artifact or diff so hidden assumptions and author-context bias are exposed.
5. **ssot-audit** — detect duplicated facts, policies, constants, decisions, status claims, or configuration guidance and identify one canonical source.
6. **clean-rebuild** — when patches and compatibility workarounds have accumulated beyond safe local repair, prefer a bounded clean reconstruction from current requirements while preserving verified behavior.
7. **fact-check** — externally verify reality-grounded claims that can materially affect design, security, compatibility, operations, or user decisions; distinguish verified facts from assumptions.
8. **project-catchup** — reconstruct current project state from durable evidence such as branch, commit, PR, issues, docs, tests, and recent changes before resuming stale or interrupted work.

Read `references/quality-gates.md` for trigger rules, severity, and completion criteria.

## Default placement in Luna workflow

For material development:

`Requirements -> bounded requirement-check -> Architecture -> codebase impact review -> multi-lens-review when consequential -> Repository/Branch -> Implementation -> risk-calibrated tests/TDD -> self-review -> targeted fresh-eyes/ssot/fact-check/clean-rebuild checks -> dual-axis independent review -> repository-required verification -> GitHub -> PR`

For incident work, do not run architecture-oriented gates before evidence preservation and diagnosis. Apply evidence-first debugging, then quality gates to hypotheses, fixes, remediation, and final root-cause claims only where relevant.

For security work, Security Team ownership remains authoritative for risk acceptance and finding severity; this layer improves review quality but does not override authorization or scope boundaries.

## Gate selection

Use the minimum applicable set:

- Always for material implementation: `requirement-check`, `self-review`, and dual-axis Code Review before merge-ready status.
- Architecture, auth, privileged, data, deployment, or reliability boundary changes: add `multi-lens-review`.
- Large/refactored/generated output or long-session work: add `fresh-eyes-review`.
- Repeated facts/config/docs across files: add `ssot-audit`.
- Repeated workaround/patch stacking or architecture drift: evaluate `clean-rebuild`.
- Claims about versions, APIs, CVEs, standards, compatibility, product behavior, or external reality: add `fact-check` when material.
- Resuming an old branch/project or unclear repository state: start with `project-catchup`.
- Reproducible bugs: prefer a failing regression test before the fix when the repository can express one meaningfully.
- Narrow low-impact reversible edits: use targeted verification and do not manufacture tests solely to satisfy process.

## Testing calibration

Start with the narrowest meaningful check that can falsify the change. Broaden only when repository requirements, changed boundaries, risk, previous failures, or unresolved concerns justify it.

Once the required and risk-appropriate checks pass, do not repeat broad suites without new changes, failure evidence, flaky behavior, or an unresolved material concern.

Tests must verify behavior, contracts, boundaries, or regressions. A test that simply restates implementation structure without protecting a meaningful contract is not automatically valuable.

## Dual-axis review contract

For material code changes, independent Code Review must record conclusions on both axes:

- **Behavioral correctness** — requested behavior, edge cases, security properties, failure/recovery behavior, compatibility, test adequacy, data integrity.
- **Codebase fit** — architecture/module boundaries, maintainability, SSOT/duplication, dependency/abstraction cost, operational impact, documentation/configuration consistency, scope control.

A BLOCKER or IMPORTANT issue on either axis remains visible on that axis. Do not collapse both into a single generic pass/fail judgment that hides the nature of the risk.

## Findings

Classify findings as:

- **BLOCKER** — correctness, security, data integrity, authorization, unrecoverable migration, or materially false evidence issue. Prevents merge-ready status.
- **IMPORTANT** — meaningful maintainability, reliability, test, compatibility, documentation, or architecture risk that should normally be resolved before merge.
- **SUGGESTION** — beneficial improvement that does not invalidate readiness.

Do not create blocker findings for taste, naming preference, or speculative future concerns without evidence.

## Completion contract

A quality pass must report only checks actually performed. For each blocking or important finding, include evidence, affected scope, consequence, and the next corrective action. If no material issue is found, say so without inventing findings.

A change is merge-ready only when repository-required verification has passed or any unavailable checks are explicitly disclosed, both review axes have no unresolved BLOCKER, and no specialist gate that materially applies has an unresolved BLOCKER.

## Attribution

The conceptual inspiration for several patterns comes from the MIT-licensed `LilMGenius/paperthin` project. Luna names, trigger rules, severity model, routing integration, and workflow implementation are project-specific. See `references/provenance.md`.

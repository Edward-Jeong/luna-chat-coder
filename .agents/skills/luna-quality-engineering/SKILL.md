---
name: luna-quality-engineering
description: Apply Luna's evidence-driven quality gates and engineering disciplines after routing and during engineering work. Provides requirement validation, disciplined test-first implementation, evidence-first debugging, dual-axis review, deep-module design, self-review, fresh-eyes review, SSOT audit, clean rebuild decisions, fact checking, and project catch-up.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.2.0"
---

# Luna Quality Engineering Layer

This skill is Luna Chat Coder's quality-control layer. It is inspired by low-level agentic engineering patterns from Paperthin and selected engineering principles reviewed from Matt Pocock's MIT-licensed `mattpocock/skills`, but it is implemented as a Luna-native workflow and does not require either upstream project to be installed.

It complements, rather than replaces:

- `.agents/skills/luna-chat-coder/SKILL.md` for exact-state, continuity, execution, publication, and evidence policy;
- `.agents/skills/luna-agent-teams/SKILL.md` for lead-team routing and specialist ownership.

## Core rule

Route first, then apply only the minimum quality gates and engineering disciplines that materially reduce risk. Quality controls must not become ceremony, duplicate existing repository checks, or block work for stylistic reasons.

## Five engineering disciplines

Luna strengthens its existing workflow with five embedded disciplines:

1. **requirement grilling** — resolve material decision branches before architecture or implementation instead of silently guessing;
2. **test-first vertical slicing** — prefer behavioral red -> green feedback at stable public seams, one coherent slice at a time;
3. **evidence-first debugging** — reproduce and discriminate before hypothesising or changing source;
4. **dual-axis review** — review specification fidelity and engineering quality independently;
5. **deep-module design** — continuously challenge module/interface depth, coupling, locality, vocabulary, and test seams when architecture is consequential.

These are Luna-native rules, not imported slash commands. Read `references/engineering-disciplines.md` for the canonical operating contract.

## Eight quality patterns

1. **requirement-check** — verify that intent, constraints, non-goals, acceptance criteria, and unresolved ambiguity are understood before architecture or implementation; invoke requirement grilling when material decision branches remain.
2. **multi-lens-review** — review consequential decisions from independent architecture, security, operations/reliability, and maintainability lenses; apply deep-module design where module boundaries or interfaces are involved; surface disagreement instead of averaging it away.
3. **self-review** — immediately review a completed change for correctness, security, regressions, test adequacy, documentation drift, and accidental scope expansion.
4. **fresh-eyes-review** — perform a context-minimized review of the artifact or diff so hidden assumptions and author-context bias are exposed.
5. **ssot-audit** — detect duplicated facts, policies, constants, decisions, status claims, or configuration guidance and identify one canonical source.
6. **clean-rebuild** — when patches and compatibility workarounds have accumulated beyond safe local repair, prefer a bounded clean reconstruction from current requirements while preserving verified behavior.
7. **fact-check** — externally verify reality-grounded claims that can materially affect design, security, compatibility, operations, or user decisions; distinguish verified facts from assumptions.
8. **project-catchup** — reconstruct current project state from durable evidence such as branch, commit, PR, issues, docs, tests, and recent changes before resuming stale or interrupted work.

Read `references/quality-gates.md` for trigger rules, severity, and completion criteria.

## Default placement in Luna workflow

For material development:

`Requirements -> requirement-check/grilling when needed -> Architecture/deep-module check -> Repository/Branch -> test seam -> test-first vertical implementation -> self-review -> Tests/Verification -> dual-axis review -> GitHub -> PR`

Add `multi-lens-review`, `fresh-eyes-review`, `ssot-audit`, `clean-rebuild`, and `fact-check` only when their risk triggers apply.

For incident work, do not run architecture-oriented gates before evidence preservation and diagnosis. Use the evidence-first debugging discipline: build a feedback loop, reproduce, minimise, rank falsifiable hypotheses, instrument, fix, regression-test, and only then state root cause. Apply other quality gates to remediation and final claims where relevant.

For security work, Security Team ownership remains authoritative for risk acceptance and finding severity; this layer improves review quality but does not override authorization or scope boundaries.

## Gate selection

Use the minimum applicable set:

- Always for material implementation: `requirement-check`, `self-review`.
- Material requirement ambiguity that can change architecture/scope/security/acceptance: add requirement grilling.
- New behavior or bug fix with a practical automated seam: use test-first vertical slicing.
- Existing failure, regression, flaky behavior, or performance problem: use evidence-first debugging before causal claims or speculative source changes.
- Material diff before readiness: use dual-axis review; keep specification fidelity separate from engineering quality.
- Architecture, auth, privileged, data, deployment, or reliability boundary changes: add `multi-lens-review` and deep-module design where boundaries/interfaces are changing.
- Large/refactored/generated output or long-session work: add `fresh-eyes-review`.
- Repeated facts/config/docs across files: add `ssot-audit`.
- Repeated workaround/patch stacking or architecture drift: evaluate `clean-rebuild`.
- Claims about versions, APIs, CVEs, standards, compatibility, product behavior, or external reality: add `fact-check` when material.
- Resuming an old branch/project or unclear repository state: start with `project-catchup`.

## Findings

Classify findings as:

- **BLOCKER** — correctness, security, data integrity, authorization, unrecoverable migration, materially false evidence, or unmet critical requirement issue. Prevents merge-ready status.
- **IMPORTANT** — meaningful maintainability, reliability, test, compatibility, documentation, or architecture risk that should normally be resolved before merge.
- **SUGGESTION** — beneficial improvement that does not invalidate readiness.

Do not create blocker findings for taste, naming preference, or speculative future concerns without evidence.

## Completion contract

A quality pass must report only checks actually performed. For each blocking or important finding, include evidence, affected scope, consequence, and the next corrective action. If no material issue is found, say so without inventing findings.

For material code changes, readiness reporting should identify both review axes when dual-axis review applies:

- **Spec** — pass / findings / unavailable because no reliable requirement source exists;
- **Engineering** — pass / findings / unavailable because required evidence could not be inspected.

A change is merge-ready only when repository-required verification has passed or any unavailable checks are explicitly disclosed, and no unresolved BLOCKER remains on either axis.

## Attribution

The conceptual inspiration for several quality patterns comes from the MIT-licensed `LilMGenius/paperthin` project. The five engineering disciplines are Luna-native adaptations informed by selected ideas reviewed from the MIT-licensed `mattpocock/skills` project. Luna names, trigger rules, severity model, routing integration, and workflow implementation are project-specific. See `references/provenance.md`.

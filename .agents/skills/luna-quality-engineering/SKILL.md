---
name: luna-quality-engineering
description: Apply Luna's evidence-driven quality gates after routing and during engineering work. Provides requirement validation, multi-lens review, self-review, fresh-eyes review, SSOT audit, clean rebuild decisions, fact checking, and project catch-up.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.1.0"
---

# Luna Quality Engineering Layer

This skill is Luna Chat Coder's quality-control layer. It is inspired by low-level agentic engineering patterns from Paperthin, but is implemented as a Luna-native workflow and does not require Paperthin to be installed.

It complements, rather than replaces:

- `.agents/skills/luna-chat-coder/SKILL.md` for exact-state, continuity, execution, publication, and evidence policy;
- `.agents/skills/luna-agent-teams/SKILL.md` for lead-team routing and specialist ownership.

## Core rule

Route first, then apply only the minimum quality gates that materially reduce risk. Quality checks must not become ceremony, duplicate existing repository checks, or block work for stylistic reasons.

## Eight quality patterns

1. **requirement-check** — verify that intent, constraints, non-goals, acceptance criteria, and unresolved ambiguity are understood before architecture or implementation.
2. **multi-lens-review** — review consequential decisions from independent architecture, security, operations/reliability, and maintainability lenses; surface disagreement instead of averaging it away.
3. **self-review** — immediately review a completed change for correctness, security, regressions, test adequacy, documentation drift, and accidental scope expansion.
4. **fresh-eyes-review** — perform a context-minimized review of the artifact or diff so hidden assumptions and author-context bias are exposed.
5. **ssot-audit** — detect duplicated facts, policies, constants, decisions, status claims, or configuration guidance and identify one canonical source.
6. **clean-rebuild** — when patches and compatibility workarounds have accumulated beyond safe local repair, prefer a bounded clean reconstruction from current requirements while preserving verified behavior.
7. **fact-check** — externally verify reality-grounded claims that can materially affect design, security, compatibility, operations, or user decisions; distinguish verified facts from assumptions.
8. **project-catchup** — reconstruct current project state from durable evidence such as branch, commit, PR, issues, docs, tests, and recent changes before resuming stale or interrupted work.

Read `references/quality-gates.md` for trigger rules, severity, and completion criteria.

## Default placement in Luna workflow

For material development:

`Requirements -> requirement-check -> Architecture -> multi-lens-review when consequential -> Repository/Branch -> Implementation -> self-review -> targeted fresh-eyes/ssot/fact-check/clean-rebuild checks -> Tests/Verification -> GitHub -> PR`

For incident work, do not run architecture-oriented gates before evidence preservation and diagnosis. Apply quality gates to hypotheses, fixes, remediation, and final root-cause claims only where relevant.

For security work, Security Team ownership remains authoritative for risk acceptance and finding severity; this layer improves review quality but does not override authorization or scope boundaries.

## Gate selection

Use the minimum applicable set:

- Always for material implementation: `requirement-check`, `self-review`.
- Architecture, auth, privileged, data, deployment, or reliability boundary changes: add `multi-lens-review`.
- Large/refactored/generated output or long-session work: add `fresh-eyes-review`.
- Repeated facts/config/docs across files: add `ssot-audit`.
- Repeated workaround/patch stacking or architecture drift: evaluate `clean-rebuild`.
- Claims about versions, APIs, CVEs, standards, compatibility, product behavior, or external reality: add `fact-check` when material.
- Resuming an old branch/project or unclear repository state: start with `project-catchup`.

## Findings

Classify findings as:

- **BLOCKER** — correctness, security, data integrity, authorization, unrecoverable migration, or materially false evidence issue. Prevents merge-ready status.
- **IMPORTANT** — meaningful maintainability, reliability, test, compatibility, documentation, or architecture risk that should normally be resolved before merge.
- **SUGGESTION** — beneficial improvement that does not invalidate readiness.

Do not create blocker findings for taste, naming preference, or speculative future concerns without evidence.

## Completion contract

A quality pass must report only checks actually performed. For each blocking or important finding, include evidence, affected scope, consequence, and the next corrective action. If no material issue is found, say so without inventing findings.

A change is merge-ready only when repository-required verification has passed or any unavailable checks are explicitly disclosed, and no unresolved BLOCKER remains.

## Attribution

The conceptual inspiration for several patterns comes from the MIT-licensed `LilMGenius/paperthin` project. Luna names, trigger rules, severity model, routing integration, and workflow implementation are project-specific. See `references/provenance.md`.

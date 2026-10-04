---
name: luna-quality-engineering
description: Select evidence-driven quality gates for material implementation, consequential decisions, complex reviews, or uncertain project state.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.3.0"
---

# Luna Quality Engineering Layer

Apply the canonical Core policy referenced by the active instruction chain (the template default is `docs/CORE_ENGINEERING_PROTOCOL_V2.md`) for shared engineering execution, testing, review independence, and readiness. Read `references/quality-gates.md` for the canonical gate triggers. Keep those responsibilities separate; summaries here must not override either source.

Route first, then select the minimum useful gates:

| Situation | Gate |
| --- | --- |
| Material implementation | requirement-check, self-review, dual-axis Code Review |
| Consequential architecture/security/data/operations decision | multi-lens-review |
| Large/generated/refactored diff or long-session author bias | fresh-eyes-review |
| Repeated policy, fact, setting, interface, or status | ssot-audit |
| Patch stacking or unsafe architectural drift | evaluate clean-rebuild |
| Material external product/API/security claim | fact-check |
| Resuming uncertain or interrupted project state | project-catchup |

For narrow low-impact edits, use targeted verification. Do not run every gate, manufacture mirror tests, introduce a new test stack, or block on stylistic preferences. Core defines bounded grilling, risk-calibrated TDD, evidence-first debugging, and the two review axes; do not duplicate their procedures here.

## Review evidence

Keep behavioral correctness and codebase fit conclusions separate. Include evidence, affected scope, consequence, and practical remediation for BLOCKER or IMPORTANT findings. Do not invent findings when no material issue is found.

Label a same-agent pass as self-review or fresh-eyes-review. A separate agent/session or human must supply independent Code Review for material implementation before merge readiness. If unavailable, finish authorized implementation and hand off as review-ready.

Never claim a check that did not run. Required verification that fails, cannot run, or is pending prevents merge-ready even when disclosed. Follow Core's readiness states and IMPORTANT-acceptance rule; the gate reference owns severity definitions.

## Attribution

Quality patterns were informed by MIT-licensed Paperthin and adapted for Luna. See `references/provenance.md`.

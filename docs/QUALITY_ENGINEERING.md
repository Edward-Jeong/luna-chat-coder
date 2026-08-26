# Luna Quality Engineering Layer

Luna Quality Engineering Layer is the quality-control stage between Agent Team execution and readiness claims.

## Why it exists

Luna Chat Coder already provides repository state continuity and reliable delivery, while Luna Agent Teams provides role-based routing. Quality Engineering adds a separate concern: preventing plausible but weak agent output from being treated as finished engineering work.

The layer focuses on eight recurring failure modes:

1. misunderstood requirements;
2. single-perspective architecture decisions;
3. missing post-implementation review;
4. author-context bias;
5. duplicated sources of truth;
6. patch/workaround accumulation;
7. unverified external claims;
8. stale project/session context.

## Architecture

```text
User request
    |
    v
Luna Chat Coder
(exact state / execution / delivery)
    |
    v
Luna Agent Teams
(route lead + support teams)
    |
    v
Luna Quality Engineering
(select minimum useful gates)
    |
    v
Repository verification
    |
    v
GitHub / Pull Request
```

Quality Engineering is intentionally one Agent Skill with internal gates. This avoids globally installing many small skills and reduces routing ambiguity in Codex.

## Gate map

| Gate | Primary purpose | Typical trigger |
| --- | --- | --- |
| requirement-check | Validate intent and acceptance criteria | Material feature/change |
| multi-lens-review | Expose architecture/security/ops tradeoffs | Consequential boundary change |
| self-review | Inspect final implementation against request | Every material implementation |
| fresh-eyes-review | Reduce author-context bias | Large/complex/generated/refactored output |
| ssot-audit | Prevent truth/document/config drift | Same fact in multiple durable locations |
| clean-rebuild | Stop workaround accumulation | Patch-on-patch or boundary erosion |
| fact-check | Verify external reality claims | Versions, APIs, CVEs, standards, support |
| project-catchup | Reconstruct current durable state | Resuming stale/interrupted work |

## Normal development flow

```text
Requirements
  -> requirement-check
Architecture
  -> multi-lens-review (when consequential)
Repository / Feature branch
Implementation
  -> self-review
  -> targeted fresh-eyes / ssot / clean-rebuild / fact-check
Tests / verification
GitHub publication
Pull request
```

Not every gate runs on every task. The anti-ceremony rule is part of the design: a quality gate is used only when it can materially improve confidence.

## Team integration

### Coding Team

Coding owns delivery. Quality Engineering validates requirements, architecture tradeoffs, implementation quality, and readiness.

### Security Team

Security still owns security finding severity, authorization boundaries, and risk acceptance. Quality Engineering adds factual verification and independent lenses but cannot expand testing scope.

### Incident Analysis Team

Incident Analysis still prioritizes evidence preservation and diagnosis. `project-catchup` is useful before repository changes, while `fact-check` is useful when final root-cause claims depend on external platform behavior.

## Readiness

- `merge-ready`: applicable repository checks passed and no unresolved BLOCKER remains.
- `review-ready`: implementation is coherent but human, CI, environment, or external validation remains.
- `diagnostic-only`: analysis/evidence only; no delivery claim.

## Paperthin relationship

The layer was inspired by selected concepts in the MIT-licensed Paperthin project (`LilMGenius/paperthin`) but is not a runtime dependency and is not a direct global installation. Luna uses its own naming, gate selection, severity model, team integration, evidence rules, and readiness contract.

See `.agents/skills/luna-quality-engineering/references/provenance.md` for provenance details.

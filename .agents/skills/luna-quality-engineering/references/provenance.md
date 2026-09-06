# Quality Layer Provenance

Luna Quality Engineering Layer is a Luna-native implementation informed by ideas from the MIT-licensed Paperthin project by LilMGenius and selected engineering principles reviewed from the MIT-licensed `mattpocock/skills` project by Matt Pocock.

Upstream references:

- Project: `LilMGenius/paperthin`
  - License: MIT
  - Concepts reviewed: read/requirement checking, multiple perspectives, post-work self-checks, context-free review, SSOT consolidation, clean reconstruction, factual verification, and project/session catch-up.
- Project: `mattpocock/skills`
  - License: MIT
  - Concepts reviewed: requirement grilling/design-tree questioning, test-first red/green feedback at meaningful seams, disciplined bug diagnosis before causal claims, separate specification-vs-standards review, and codebase/module design discipline.

Luna does not require either upstream project at runtime and does not globally install or vendor their skill packs. The Luna implementation intentionally changes naming, orchestration, trigger conditions, severity, evidence requirements, team ownership, completion semantics, and interaction model to fit Luna Chat Coder's architecture.

The `engineering-disciplines.md` reference is a Luna-authored policy synthesis. It does not expose the upstream slash-command surface and is designed to be invoked implicitly through Luna Router, Agent Teams, and Quality Engineering rather than as a second parallel workflow.

When copying upstream code or substantial text in future changes, preserve the applicable upstream MIT license and attribution as required. Conceptual reimplementation should still retain this provenance note for engineering traceability.

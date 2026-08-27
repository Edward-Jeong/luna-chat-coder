---
name: luna-search-visibility
description: Apply Luna's search visibility quality gate to public web projects. Covers technical search discoverability, AI-search crawler access, Naver visibility, exposure safety, and measurement without applying SEO ceremony to private/admin systems.
license: MIT
compatibility: Designed for Agent Skills hosts and Codex custom agents.
metadata:
  version: "0.1.0"
---

# Luna Search Visibility Quality Gate

This skill is a conditional quality gate for web projects. It is not a mandatory SEO phase for every repository.

## Activation rule

Activate by default when a project exposes public web pages whose intended users may discover them through search or AI-assisted search, including public product sites, SaaS landing pages, documentation, blogs, knowledge pages, public catalogs, and public service pages.

Do not activate search optimization for private/admin/internal-only surfaces, authenticated management consoles, closed-network systems, backend-only services, CLI tools, or infrastructure repositories unless the user explicitly requests public discoverability work.

For mixed repositories, apply the gate only to the public surface. Private routes must remain intentionally non-indexable.

## Core principles

1. **Discoverability follows product intent.** Never make a page indexable merely because it is technically possible.
2. **Security outranks visibility.** Never expose private, privileged, staging, debug, API-doc, log, backup, internal-document, or test surfaces to improve search visibility.
3. **Crawler-eye verification.** Validate the deployed/static HTTP result, not only source-code intent. Important content and directives must be inspectable in the response a crawler receives.
4. **No ranking guarantees.** Search inclusion, citation, ranking, AI answer placement, and traffic are outcomes that cannot be guaranteed.
5. **Official-source facts only for engine-specific policy.** Search/AI crawler names, directives, structured-data support, and engine behavior are time-sensitive. Verify material claims against the relevant vendor's current first-party documentation.
6. **Measurement is part of completion.** Record a baseline when practical and define how the effect will be checked after deployment.

## Gate sequence

### Gate 0 — classify the surface

Classify each relevant surface as one of:
- `PUBLIC_DISCOVERABLE`: should be searchable/discoverable.
- `PUBLIC_NO_INDEX`: public by URL but intentionally excluded from search.
- `PRIVATE`: authentication/network/policy restricted and must not be indexed.

If classification is uncertain and accidental exposure would be material, treat it as `PRIVATE` until product intent is established.

### Gate 1 — exposure safety

Before increasing crawler access, check for sensitive or non-product surfaces such as `/admin`, `/internal`, `/debug`, `/staging`, `/api-docs`, `/swagger`, `/logs`, `/backup`, test fixtures, source maps containing secrets, directory listings, and unintended public object storage.

Robots rules are not access control. Sensitive content requires authentication, authorization, network controls, or equivalent enforcement.

### Gate 2 — technical discoverability

For `PUBLIC_DISCOVERABLE` pages, verify the applicable items:
- successful HTTP response and stable canonical URL;
- accidental `noindex` absent from both HTML directives and relevant response headers;
- important content available in crawler-retrievable output rather than requiring unsupported client-only execution;
- meaningful title and description where relevant;
- sitemap coverage for indexable canonical pages when the site benefits from a sitemap;
- robots policy consistent with product intent;
- correct 404/redirect behavior;
- structured data only when it matches visible content and a currently supported use case.

Do not treat fixed title/description character counts as hard correctness rules.

### Gate 3 — AI search access

For public pages intended to be discoverable in ChatGPT Search, verify current OpenAI guidance before changing policy. At minimum, check whether `OAI-SearchBot` is unintentionally blocked and whether hosting/CDN/WAF policy prevents legitimate crawler traffic when ChatGPT visibility is an explicit goal.

Keep search access and model-training policy conceptually separate. Do not infer that allowing a search crawler requires allowing model-training crawlers.

`llms.txt` is optional/experimental unless a target platform's current first-party documentation makes it a requirement. Its presence must never substitute for crawlability, indexability, useful content, canonical URLs, or engine-supported controls.

### Gate 4 — Google and Naver public-search compatibility

For Google-facing pages, follow current Google Search Central guidance. Do not invent special AEO/GEO markup requirements for AI features; use supported SEO fundamentals and engine-documented features.

For Korean public-facing sites, also verify current Naver Search Advisor guidance, including Yeti/robots policy and sitemap/search registration considerations where applicable.

### Gate 5 — content usefulness and source quality

Prefer pages that answer a real user intent clearly and contain useful, attributable, maintainable information. First-party facts, original measurements, product documentation, and clearly sourced technical material are stronger assets than generated filler or duplicated summaries.

Do not create doorway pages, hidden text, cloaking, fabricated schema, link schemes, or mass low-value pages.

### Gate 6 — verification and measurement

Report:
1. surface classification;
2. checks performed and evidence;
3. changes made;
4. unresolved BLOCKER/IMPORTANT findings;
5. measurement plan.

Where analytics/search-console access exists, capture a baseline appropriate to the project (for example indexed pages, impressions, clicks, referral traffic, crawler hits, or selected query visibility). Re-check after sufficient indexing time rather than claiming success immediately after deployment.

## Severity

- **BLOCKER** — accidental indexing/exposure of private content, production `noindex` on a discoverable surface, crawler-blocking configuration that directly contradicts an explicit discoverability requirement, fabricated/misleading structured data, or materially false verification evidence.
- **IMPORTANT** — missing canonical/sitemap coverage on material public content, client-rendering behavior that prevents reliable discovery, broken status/redirect behavior, or missing measurement plan for a material visibility change.
- **SUGGESTION** — nonessential content/metadata enhancements or optional discovery features.

No unresolved BLOCKER may remain when claiming the public web surface is search-visibility ready.

## Integration

This gate complements:
- `luna-chat-coder` for repository workflow and exact-state evidence;
- `luna-agent-teams` for lead-team routing;
- `luna-quality-engineering` for review severity and merge readiness;
- `luna-design-system` for UI quality;
- Luna Security Team when crawler/access changes cross a security boundary.

Read `references/engine-policy.md` for time-sensitive vendor-policy anchors and verification notes.

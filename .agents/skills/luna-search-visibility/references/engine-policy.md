# Search Visibility engine-policy anchors

Engine-specific behavior changes over time. Treat this file as verification guidance, not as a frozen copy of vendor policy.

## OpenAI / ChatGPT Search

First-party source: OpenAI Help Center, "Publishers and Developers - FAQ" and "ChatGPT Search".

Current verified principles as of 2026-08:
- Public websites can be eligible to appear in ChatGPT Search.
- To support inclusion of site content in ChatGPT Search summaries/snippets, do not unintentionally block `OAI-SearchBot`.
- Hosting/CDN/WAF policy can also block legitimate crawler traffic; check OpenAI-published crawler/IP guidance when visibility is required.
- Search-result inclusion or ranking is not guaranteed.
- Search crawling and model-training crawling are separate policy concerns; do not collapse them into one allow/deny decision.

Before implementing an OpenAI-specific robots/WAF rule, verify the current OpenAI first-party crawler documentation.

## Google Search and generative AI features

First-party source: Google Search Central documentation, including the generative-AI optimization guide and Search documentation updates.

Current verified principles as of 2026-08:
- Google's established SEO fundamentals remain relevant to AI Mode/AI Overviews and other generative Search features.
- Do not assume special AEO/GEO markup is required unless Google explicitly documents it.
- Google deprecated FAQ rich results in May 2026; do not use FAQ structured data as a promise of FAQ rich-result visibility.
- Search spam policies apply to generative Search features as well.

Before implementing Google-specific structured data or AI-feature behavior, verify the current Search Central documentation because supported features can be added or deprecated.

## Naver Search

First-party source: Naver Search Advisor technical guidance.

Verify before Korean-market launch:
- intended public content is crawlable by Naver's current crawler policy;
- robots.txt does not accidentally block the intended surface;
- sitemap/search registration guidance is followed when applicable;
- mobile/public-page behavior matches Naver's current guidance.

Do not encode undocumented claims about Naver ranking or AI Briefing citation as guaranteed rules. Keep observations separate from official policy.

## Bing / Microsoft search ecosystem

Use Bing Webmaster Tools and IndexNow only according to current Microsoft/Bing first-party documentation. Do not assume that another AI product's search pipeline is equivalent to Bing indexing unless that product's owner documents the dependency.

## `llms.txt`

Treat `llms.txt` as optional/experimental in Luna. It is not a replacement for robots directives, canonical/indexability controls, sitemap hygiene, useful public content, or vendor-documented crawler access. Do not make it a merge blocker unless a target platform's current first-party documentation makes it an explicit requirement.

## Fact-check rule

When an engine-specific claim can materially affect implementation, security, indexing, traffic, or user expectations:
1. use the vendor's first-party documentation;
2. record the verification date in the work report when useful;
3. distinguish documented behavior from empirical observation;
4. never guarantee ranking, citation, or traffic outcomes.

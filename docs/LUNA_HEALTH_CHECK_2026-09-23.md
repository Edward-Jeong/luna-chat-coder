# Luna Health Check — 2026-09-23

Baseline: `Edward-Jeong/luna-chat-coder` `main` at `aff5b088662a22050b92fa54f04ae66036b370f2`. This snapshot covers repository files only; it does not inspect a user's installed plugins, active MCP connections, or actual skill usage history.

| Surface | Files | UTF-8 bytes | Assessment |
| --- | ---: | ---: | --- |
| `AGENTS.md` | 1 | 4,892 | Short entry point, but directs material work to several policies |
| Core protocol | 1 | 11,751 | Canonical engineering rules; review repeated summaries elsewhere |
| Skill bodies | 5 | 49,865 | Main size review candidates are `luna-chat-coder` (14,373) and `luna-agent-teams` (12,929) |
| Skill references | 9 | 64,467 | On-demand material; 24,050-byte design rationale is largest |
| Optional Codex agents | 6 | 18,115 | Router TOML (8,041) repeats core and conditional gate instructions |
| Repository plugin/MCP declarations | 0 | 0 | No repository-local configuration to assess; runtime status unknown |

These are file sizes, **not measured prompt tokens**. The skill bodies and references are not necessarily all loaded for one task; `AGENTS.md` currently directs the agent to read three policy layers for material work. No evidence from this snapshot establishes that a skill is unused, a plugin is installed, an MCP is reachable, or an instruction conflict exists.

## Decisions

| Action | Evidence and scope | Next verification |
| --- | --- | --- |
| KEEP | Core protocol is the declared source for follow-through, testing, debugging and review. Design and Search Visibility skills have conditional triggers in `AGENTS.md`. | Preserve conditional routing on CLI, private, and UI tasks. |
| SIMPLIFY | `AGENTS.md` repeats routing and gate summaries from the skills; `integrations/codex/agents/luna-router.toml` repeats Core protocol and the Design/Search Visibility gates. This is semantic overlap, not a proven contradiction. | In a separate change, shorten only duplicated summaries and compare behavior against `references/router-evaluation.md`. |
| MERGE | No pair of skills has demonstrated identical ownership. Assess shared instructions in Core protocol, `luna-agent-teams`, and the Router TOML paragraph by paragraph before moving text. | Check that task routing and review requirements still resolve to a single canonical source. |
| REMOVE | No removal is justified by repository evidence. | Gather actual usage and dependency evidence first. |

## Doctor implementation boundary

The repository skill `$doctor` inventories local instruction surfaces and reports deterministic review signals. `$doctor --deep` additionally checks exact repeated paragraphs and broken explicit repository path references. `$doctor --fix` guides the agent through a narrow, reviewed patch with a visible diff and verification; the inventory script itself is read-only. Plugin/MCP connection checks require separate runtime access and must be labeled `not observed` when unavailable.

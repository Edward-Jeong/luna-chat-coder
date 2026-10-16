---
name: doctor
description: Audit a Luna repository's AGENTS.md, skills, agents, router, and declared plugin/MCP configuration. Use for $doctor, $doctor --deep, $doctor --fix, or a Luna health check.
---

# Luna Doctor

Run `python3 .agents/skills/doctor/scripts/health.py --root .` from the target repository. Add `--deep` when requested to inspect exact repeated paragraphs. The script reads repository files only and never edits them.

Interpret results before recommending changes:

1. Check the current branch, `AGENTS.md`, the canonical protocol, skill entry points and references, optional agent definitions, and repository-declared plugin/MCP files. Report bytes as bytes; do not present them as measured context tokens. References and optional agents are loaded only when used, so their sizes are not an always-loaded budget.
2. Trace every finding to file paths and content. An exact repeated paragraph is evidence of overlap, not proof that either copy is redundant. A large file is a review candidate, not a defect. Do not call a skill unused without usage history; do not infer installed plugins, enabled MCP servers, or connection health from a repository without runtime access.
3. Classify concrete actions as KEEP, MERGE, SIMPLIFY, or REMOVE. For each change, state evidence, expected effect, compatibility risk, and verification. Prefer one canonical instruction with short pointers over deleting functionality. Preserve explicit user instructions and higher-priority host rules.
4. `$doctor` is read-only. `$doctor --deep` adds dependency and overlap inspection, including references from router and agent definitions. `$doctor --fix` means prepare a narrowly scoped patch for evidence-backed, low-risk changes, show the diff, run relevant checks, and report what changed. Never auto-remove a skill, plugin, MCP server, or user setting. If the user requests a PR, use a feature branch and create one after verification.

For runtime plugin/MCP checks, use the host's available read-only status commands or APIs with the user's authorization. Label unavailable checks `not observed`; never equate missing repository configuration with disabled or healthy runtime integrations. Avoid printing credentials or raw configuration values.

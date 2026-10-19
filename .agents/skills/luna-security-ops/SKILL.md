---
name: luna-security-ops
description: Handle scoped security analysis with advisory domain routing, local tool discovery, and inspectable evidence contracts.
license: MIT
compatibility: Agent Skills hosts; executable helpers require Python 3.10 or newer.
metadata:
  version: "0.2.0"
---

# Luna Security Ops

Use the active canonical Core policy (template default: `docs/CORE_ENGINEERING_PROTOCOL_V2.md`) for execution, approval, review independence, tests, and readiness. The top-level team decision remains in `.agents/skills/luna-agent-teams/references/routing.md`. This optional layer supplies domain routing and evidence helpers; it does not introduce a fourth lead team.

## Conditional activation

Load for a concrete security assessment, finding validation, evidence handoff, or security tool task. Repository/link review alone does not authorize installation, target execution, or scanning. Existing unexplained failures stay Incident-led; source fixes and new products stay Coding-led. Reverse analysis can support any lead team: load `.agents/skills/luna-reverse-engineering/SKILL.md` only when inspecting implementation artifacts is part of the requested outcome.

## Executable helpers

Run from the project root:

- `python scripts/security-ops.py route "<request>"`: advisory domain/handoff suggestion from `config/routing.json`. Lexical scoring is not semantic understanding. Resolve ties, negation, and mixed intent using the canonical team router; never use this result as permission to act.
- `python scripts/security-ops.py doctor`: find tool paths without executing or installing tools. Found does not mean verified, and does not establish live MCP connectivity.
- `python scripts/security-ops.py check-scope --scope CASE/scope.json --action ACTION --asset ASSET`: exact action/asset admission. Follow `references/scope-contract.md`.
- `python scripts/security-ops.py verify-case CASE/case.json`: check evidence links and case-local artifact hashes using `references/evidence-contract.md`.

The helper uses the standard library, makes no global configuration writes, installs nothing, and does not run targets. REA execution is a separate explicit subcommand described by the reverse-engineering skill. Scope declarations are not network isolation or a sandbox.

## Evidence and handoff

Use the minimum useful records, not a mandatory report/diagram ritual. Preserve facts, uncertainty, exact sample/source identity, commands and actual results. A scanner result alone is not a validated finding. Link remediation to supporting evidence and hand the established state to Coding or Incident Analysis when needed. Keep customer samples, raw output, and local tool paths outside git by default.

See `docs/SECURITY_OPS.ko.md` for working examples and limitations. Routing examples in `tests/routing-cases.json` are exercised by `tests/test_security_ops.py`.

## Provenance

This completes the Luna-native draft from `feature/luna-security-ops` (2026-08-26). Routing, tool inventory, and Evidence/Finding/Path concepts were reviewed against `Edward-Jeong/reverse-skill`. Luna does not vendor its skill pack, bootstrap tools automatically, require every report/diagram, or import its global behavior rules. Runtime analysis is delegated separately to an explicitly selected REA installation.

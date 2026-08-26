---
name: luna-security-ops
description: Route authorized security engineering work into focused Luna security capabilities with explicit scope, evidence, and tool-state contracts.
license: MIT
compatibility: Designed to operate under luna-agent-teams and Codex-compatible Agent Skills hosts.
metadata:
  version: "0.1.0"
---

# Luna Security Ops

Luna Security Ops is the security execution layer beneath `luna-agent-teams`. It does not replace the top-level Luna team router. The Security Team remains the lead team selector; this skill classifies the security domain, enforces execution gates, and dispatches to the smallest applicable capability.

## Architecture boundary

```text
User request
  -> Luna Master / Agent Team Router
  -> Security Team
  -> Luna Security Ops Router
  -> Scope Gate
  -> Security Capability
  -> Evidence -> Finding -> Path
  -> Verification / Report
```

## Core contracts

1. **Routing SSoT** — `config/routing.json` is the single source of truth for Security Ops domain routing.
2. **Scope Gate** — active testing requires explicit authorization and bounded target scope. Read-only analysis may proceed when it does not touch a live target.
3. **Evidence Contract** — findings must be traceable to evidence. Confidence and unresolved uncertainty must be explicit.
4. **Tool State** — do not guess whether a tool exists or where it is installed. Tool discovery and installation policy is defined separately from routing.
5. **Minimum Capability Set** — select one primary capability. Add another only when the task crosses a real technical boundary.
6. **No automatic privileged mutation** — package installation, service mutation, firewall changes, destructive testing, exploitation, persistence, or other privileged/destructive actions require the applicable Luna safety and authorization gates.

## Initial capability set

Phase 1 intentionally starts small:

- `code-audit` — source review, SAST, auth/input/crypto flaws, fix verification.
- `api-security` — API authorization, input validation, BOLA/BFLA, authentication/session risks.
- `supply-chain` — SBOM, SCA, dependency/provenance, CI/CD and build integrity.
- `llm-security` — LLM/agent threat analysis, prompt/tool/memory and agent supply-chain risks.
- `digital-forensics` — evidence-preserving forensic and incident artifacts analysis.
- `threat-intelligence` — IOC enrichment, public threat intelligence, campaign/context analysis.
- `malware-analysis` — authorized offline sample triage and malware analysis.
- `cloud-security` — container, Kubernetes, cloud trust-boundary and configuration security.
- `windows-security` — Windows/AD security assessment and configuration review.
- `protocol-analysis` — PCAP/protocol behavior and custom protocol analysis.

Offensive capabilities such as exploit development, EDR bypass, attack-chain orchestration, and production-target exploitation are intentionally excluded from the default capability set. If added later, they must live behind an explicit `offensive-lab` boundary.

## Routing process

1. Confirm the top-level task is security-led. If it is primarily a build, refactor, or outage, route back to Coding or Incident Analysis.
2. Read `config/routing.json` and identify the primary capability by semantic intent and dominant risk. Keywords are hints, not the sole decision mechanism.
3. If no route fits, do not force-fit. Record an `unmatched` result and propose a new capability or routing rule.
4. Apply `references/scope-contract.md` before any active action against a target.
5. Use `references/evidence-contract.md` for findings and handoffs.
6. Use `references/tool-registry.md` when a real external tool is required.
7. Before changing routing rules, update and run the routing regression cases under `tests/`.

## Cross-team handoff

- Security Ops -> Coding: remediation requires source/config changes in version control.
- Security Ops -> Incident Analysis: live compromise, containment, production recovery, or evidence-preservation workflow is required.
- Incident Analysis -> Security Ops: evidence indicates exploitability, malicious activity, auth bypass, secret exposure, or a security control failure.
- Coding -> Security Ops: a change materially affects trust boundaries, authn/authz, secrets, untrusted input, dependency trust, or privileged actions.

## Completion state

A Security Ops task is not complete until the output states:

- primary capability used;
- authorization/scope status when active testing was involved;
- evidence supporting each material finding;
- confidence and unresolved uncertainty;
- verification performed;
- any required Coding or Incident handoff.

# Luna Agent Teams for Codex

This directory contains ready-to-install Codex custom agents for Luna Router and the Coding, Security, and Incident Analysis teams.

## Install

macOS/Linux:

```bash
bash scripts/install-codex-agents.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-codex-agents.ps1
```

The scripts validate the required TOML fields and copy the agents to `~/.codex/agents/` or `$CODEX_HOME/agents`.

## Recommended entry point

Use **`Luna Router`** for normal work. Give it the natural-language request; it chooses the lead team and minimum supporting specialists automatically.

Examples:

```text
Use Luna Router: RHEL agent can connect to the manager, but the manager cannot connect back. Diagnose it.
```

```text
Use Luna Router: Add OAuth login and RBAC to this service and open a PR.
```

```text
Use Luna Router: Analyze this SAST High finding and implement a verified remediation.
```

The user does not need to choose Coding, Security, or Incident Analysis manually.

## Execution model

Luna Router does not depend on one specific Codex orchestration primitive. It operates in two modes:

- When the host supports reliable named-agent/subagent delegation, Router delegates bounded phases to the selected Luna team or specialist and synthesizes the result.
- When delegation is unavailable or uncertain, Router performs the selected workflow itself using the repository-local Luna Agent Teams skill and routing policy.

This keeps the Router usable as the single entry point across Codex surfaces without requiring the user to re-invoke a different agent manually.

## Agents

- `Luna Router` — semantic natural-language routing and cross-team handoff.
- `Luna Coding Team` — end-to-end development orchestration.
- `Luna Code Reviewer` — independent merge-readiness review.
- `Luna Security Team` — threat modeling, AppSec, authorized validation, remediation verification.
- `Luna Incident Analysis Team` — evidence-driven troubleshooting and root-cause analysis.

Direct team invocation remains available when the caller deliberately wants one role, for example an independent code-review pass. Otherwise prefer Luna Router.

## Routing behavior

Router precedence is outcome-based:

1. Existing failure/degradation whose goal is diagnosis/recovery -> Incident Analysis.
2. Security assurance or risk reduction as the main outcome -> Security.
3. Planned creation or repository behavior change -> Coding.

Mixed requests use one lead team plus only the support needed. A live incident that probably needs a code fix remains Incident-led until the defect is isolated; a new authentication feature remains Coding-led with Security support.

Canonical routing policy and regression cases live under `.agents/skills/luna-agent-teams/references/`.

## Source and attribution

The role taxonomy was informed by the MIT-licensed `Edward-Jeong/agency-agents` repository. Luna's definitions are condensed and adapted around Luna Chat Coder's exact-state, evidence, GitHub, and delivery policies rather than copied wholesale.

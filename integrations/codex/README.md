# Luna Agent Teams for Codex

This directory contains ready-to-install Codex custom agents for Luna's Coding, Security, and Incident Analysis teams.

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

## Agents

- `Luna Coding Team` — end-to-end development orchestration.
- `Luna Code Reviewer` — independent merge-readiness review.
- `Luna Security Team` — threat modeling, AppSec, authorized validation, remediation verification.
- `Luna Incident Analysis Team` — evidence-driven troubleshooting and root-cause analysis.

Each team agent contains internal specialist roles so normal use does not require manually selecting many agents.

Example:

```text
Use the Luna Coding Team to implement this feature using the repository's existing architecture and tests. Stop readiness if the code reviewer finds a blocker.
```

```text
Use the Luna Incident Analysis Team to diagnose this service failure from the logs. Preserve evidence and separate hypothesis from confirmed root cause.
```

## Source and attribution

The role taxonomy was informed by the MIT-licensed `Edward-Jeong/agency-agents` repository. Luna's definitions are condensed and adapted around Luna Chat Coder's exact-state, evidence, GitHub, and delivery policies rather than copied wholesale.

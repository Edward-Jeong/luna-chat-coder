# Luna Agent Teams

Luna Chat Coder includes three operational teams inspired by the role-separation patterns in `Edward-Jeong/agency-agents`, adapted to Luna's exact-state and evidence-first workflow.

## Architecture

```text
Natural-language task
        |
        v
Luna Agent Team routing
        |
        +-- Coding Team
        |     Software Architect
        |     Implementation Engineer
        |     Test Engineer
        |     Code Reviewer
        |
        +-- Security Team
        |     Security Architect
        |     AppSec Engineer
        |     Penetration Tester
        |     Security Reviewer
        |
        +-- Incident Analysis Team
              Incident Lead
              Infrastructure Diagnostician
              Application Diagnostician
              Database Diagnostician
              Root Cause Analyst
```

Luna Chat Coder remains the continuity/exact-state layer. Agent Teams decide who should reason about the work; the repository still decides how the software is built and verified.

## Coding Team

Default lifecycle for new projects and material features:

```text
Requirements
-> Architecture decision
-> Repository/template
-> Feature branch
-> Implementation
-> Tests/verification
-> Code review
-> GitHub publication
-> Pull request
```

Security-sensitive changes add the Security Team before implementation/release as appropriate. A Code Reviewer blocker means the change is not merge-ready.

## Security Team

Use for threat modeling, security architecture, secure code review, SAST/DAST/SCA interpretation, authorized penetration testing, secrets/dependency risk, and remediation verification.

The team is evidence- and remediation-oriented. Active testing must remain within the authorized scope.

## Incident Analysis Team

Use for service startup failures, connectivity problems, agent/manager communication issues, application stack traces, database failures, containers, OS/runtime problems, and multi-layer production defects.

Default diagnostic flow:

```text
Preserve evidence
-> Build timeline
-> Isolate failing layer
-> Rank hypotheses
-> Run discriminating tests
-> Recover service safely
-> Confirm root cause
-> Corrective/preventive action
```

## Codex

Ready-to-install custom agents are under `integrations/codex/agents/`.

### macOS / Linux

```bash
./scripts/install-codex-agents.sh
```

### Windows PowerShell

```powershell
./scripts/install-codex-agents.ps1
```

The installer copies the agents to `~/.codex/agents/` or `$CODEX_HOME/agents`.

Recommended entry agents:

- `Luna Coding Team`
- `Luna Code Reviewer`
- `Luna Security Team`
- `Luna Incident Analysis Team`

## Routing examples

| Request | Routing |
| --- | --- |
| Build a new vulnerability dashboard | Coding Team + Security role during architecture |
| Review this PR for auth bypass | Security Team + Code Reviewer if source quality also matters |
| RHEL agent can reach manager but reverse connection fails | Incident Analysis Team / infrastructure role |
| Spring bean fails after DB migration | Incident Analysis Team / application + database roles |
| Implement a confirmed defect fix | Incident Analysis -> Coding Team -> Test -> Code Reviewer |

## Source attribution

The role taxonomy and specialist separation were informed by the MIT-licensed `Edward-Jeong/agency-agents` project (AgentLand Contributors, 2025). The Luna definitions are condensed and rewritten for this repository's workflow and do not import the full Agency Agents roster.

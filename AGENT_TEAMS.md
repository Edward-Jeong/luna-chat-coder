# Luna Agent Teams

Luna Chat Coder includes three operational teams plus **Luna Router**, an automatic natural-language dispatcher inspired by the role-separation patterns in `Edward-Jeong/agency-agents` and adapted to Luna's exact-state and evidence-first workflow.

## Architecture

```text
Natural-language task
        |
        v
   Luna Router
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

Luna Chat Coder remains the continuity/exact-state layer. Luna Router decides who should reason about the work; the repository still decides how the software is built and verified.

## Luna Router v1

Users normally describe the task in natural language and do not choose a team. Router selects exactly one lead team plus the minimum supporting specialists.

Default decision order:

```text
Existing failure / degradation?
    -> Incident Analysis

Security assurance / risk reduction is the main outcome?
    -> Security

Planned creation or repository behavior change?
    -> Coding
```

Routing is semantic rather than keyword-based. A security product UI feature remains Coding-led; an unexplained live failure remains Incident-led even when a code fix may eventually be required.

Mixed tasks use handoffs rather than loading every team. Examples:

- New OAuth feature -> Coding lead + Security support.
- SAST finding requiring remediation -> Security finding -> Coding fix -> Security verification.
- Production outage likely caused by code -> Incident diagnosis -> Coding after defect isolation.
- Suspected compromise plus outage -> Incident lead + Security support with evidence preservation.

Canonical policy: `.agents/skills/luna-agent-teams/references/routing.md`  
Regression matrix: `.agents/skills/luna-agent-teams/references/router-evaluation.md`

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
bash scripts/install-codex-agents.sh
```

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-codex-agents.ps1
```

The installer copies the agents to `~/.codex/agents/` or `$CODEX_HOME/agents`.

Recommended normal entry point:

- `Luna Router`

Direct specialist/team entry points remain available:

- `Luna Coding Team`
- `Luna Code Reviewer`
- `Luna Security Team`
- `Luna Incident Analysis Team`

## Routing examples

| Request | Routing |
| --- | --- |
| Build a new vulnerability dashboard | Coding lead + Security Architect during architecture |
| Review this PR for auth bypass | Security lead + AppSec + Security Reviewer |
| RHEL agent can reach manager but reverse connection fails | Incident lead + Infrastructure Diagnostician |
| Spring bean fails after DB migration | Incident lead + Application + Database Diagnostician |
| Implement a confirmed defect fix | Coding lead + Test + Code Reviewer |

## Source attribution

The role taxonomy and specialist separation were informed by the MIT-licensed `Edward-Jeong/agency-agents` project (AgentLand Contributors, 2025). The Luna definitions are condensed and rewritten for this repository's workflow and do not import the full Agency Agents roster.

# Luna Router v1 Evaluation Matrix

These cases are regression examples for reviewing changes to Luna Router. A router change should preserve the expected lead team unless the policy change is deliberate and documented.

| # | Natural-language request | Expected lead | Expected support / phase | Confidence |
| ---: | --- | --- | --- | --- |
| 1 | Build a new vulnerability management dashboard. | Coding | Security Architect, Test, Code Reviewer | High |
| 2 | Add OAuth/OIDC login and RBAC. | Coding | Security Architect + AppSec | High |
| 3 | Refactor the DB schema and migration code. | Coding | Architect + Test + Reviewer | High |
| 4 | The bug is confirmed as null handling; fix it and open a PR. | Coding | Implementation + Test + Reviewer | High |
| 5 | Review this general PR before merge. | Coding | Code Reviewer | High |
| 6 | Review this PR specifically for SQL injection and auth bypass. | Security | AppSec + Security Reviewer | High |
| 7 | Analyze a SAST High finding and remediate it. | Security | AppSec -> Coding -> Security verification | High |
| 8 | Threat-model a new externally exposed API. | Security | Security Architect | High |
| 9 | Validate exploitability of this finding on our authorized staging target. | Security | Penetration Tester + Security Reviewer | High |
| 10 | Test whether this public IP is exploitable; no scope or ownership information is provided. | Security | Review-only until authorization is established | Low |
| 11 | RHEL agent can connect to manager, but manager cannot connect back. | Incident Analysis | Infrastructure Diagnostician | High |
| 12 | Tomcat starts but Spring bean creation fails after DB migration. | Incident Analysis | Application + Database Diagnostician | High |
| 13 | Docker cannot bind port 8080. | Incident Analysis | Infrastructure Diagnostician | High |
| 14 | PostgreSQL service returns 1067 after an IP change. | Incident Analysis | Infrastructure + Database Diagnostician | High |
| 15 | Disk usage suddenly grew by 30 GB and logs cannot be deleted. | Incident Analysis | Infrastructure/Application as evidence dictates | High |
| 16 | Users cannot log in after today's release; likely auth code regression. | Incident Analysis | Application + Security support; Coding after isolation | High |
| 17 | We suspect compromise and the service is also down. | Incident Analysis | Security support; preserve evidence/containment | High |
| 18 | Plan a database migration next month. | Coding | Architect + Database expertise | High |
| 19 | The planned migration failed in production and now the app is unavailable. | Incident Analysis | Application + Database; Coding after diagnosis | High |
| 20 | Make the system more secure. | Security | Start architecture/risk discovery; avoid active testing assumptions | Medium |
| 21 | The security product's UI needs a new export button. | Coding | Test + Reviewer; Security only if boundary changes | High |
| 22 | Fix firewall rules so the agent can receive manager connections. | Incident Analysis | Infrastructure; diagnose active zone/path before change | High |
| 23 | Add encrypted secrets storage to the new service. | Coding | Security Architect/AppSec mandatory support | High |
| 24 | A secret was committed and may have been used by an attacker. | Security | Incident support for exposure/containment; Coding for repository remediation | High |

## Invariants tested by the matrix

1. Existing unexplained failures route to Incident before Coding.
2. Planned changes route to Coding even when the product itself is security-related.
3. Security leads when security assurance/risk is the actual requested outcome.
4. Security-sensitive features do not become Security-led merely because they contain auth, secrets, or crypto; Coding remains lead for feature delivery with mandatory Security support.
5. Active security validation without authorization stays bounded and non-invasive.
6. The router does not ask the user to select an agent/team.
7. Mixed requests use a lead + handoff/support model instead of invoking every team.

# Luna Security Ops Evidence Contract

Security conclusions must be traceable and reproducible.

## Evidence model

```text
Evidence
  -> Finding
  -> Path
  -> Remediation
  -> Verification
```

### Evidence
Raw or minimally interpreted facts such as logs, code locations, packet captures, configuration values, scan output, hashes, timestamps, screenshots, or reproducible commands.

### Finding
A security-relevant conclusion supported by one or more evidence items. A finding must state affected component, impact, exploitability or relevance, and confidence.

### Path
The causal or attack path connecting evidence to impact. Do not imply a complete path when only one weak link is confirmed.

### Remediation
The smallest root-cause correction that materially reduces the identified risk. Workarounds must be labelled separately.

### Verification
The evidence that shows remediation is effective and did not introduce a material regression.

## Finding template

```yaml
finding_id:
title:
component:
severity:
confidence: high | medium | low
evidence: []
path:
impact:
preconditions: []
remediation:
verification:
uncertainties: []
```

## Rules

1. Scanner output alone is evidence, not automatically a validated finding.
2. Separate observed fact from inference.
3. Mark unsupported or partially tested paths with explicit uncertainty.
4. Prefer precise file/line, endpoint, host, process, hash, timestamp, packet, or command references when available.
5. Never fabricate proof-of-concept success, tool output, execution results, or test coverage.
6. For incident handoff, preserve original evidence and distinguish security hypothesis from confirmed compromise.
7. For Coding handoff, include the affected trust boundary and the expected security regression test.

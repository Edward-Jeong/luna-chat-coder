# Luna Security Ops Scope Contract

This contract separates **analysis permission** from **active target interaction**.

## Modes

- `read_only` — inspect user-provided files, code, logs, configs, reports, or public documentation without touching a live target.
- `offline_sample` — analyze an explicitly supplied local sample in an isolated/offline workflow.
- `authorized_target_only` — active testing is restricted to explicitly listed assets and activities.
- `lab_only` — active testing is restricted to a user-owned or explicitly authorized lab/CTF environment.

## Required state for active testing

```yaml
case_id:
authorization:
  status: granted | pending | denied
  basis: written_contract | customer_ticket | own_system | lab | ctf | bug_bounty_scope
  evidence:
scope:
  assets: []
  surfaces: []
  allowed_actions: []
  prohibited_actions: []
network_profile:
  mode: read_only | offline_sample | authorized_target_only | lab_only
constraints:
  data_handling: anonymize | no_sensitive_retention
  destructive_actions: false

```

## Gate rules

1. `read_only` analysis does not require target authorization because no live target action occurs.
2. `offline_sample` requires an explicitly supplied sample and an isolated workflow.
3. `authorized_target_only` or `lab_only` active testing requires `authorization.status=granted`.
4. Active scope must contain at least one explicit asset and at least one allowed action.
5. Denied or pending authorization blocks active testing but does not block read-only planning, architecture review, or remediation guidance.
6. Scope expansion is never inferred. New targets or new active techniques require explicit inclusion.
7. Package installation, privileged configuration changes, destructive actions, persistence, denial-of-service, or real-data extraction are separate execution decisions and are not implicitly authorized by a general pentest scope.

## Default operating order

```text
Understand request
  -> determine read-only vs active
  -> establish authorization and bounded scope if active
  -> route to capability
  -> collect evidence
  -> validate finding
  -> recommend or implement bounded remediation
```

## Executable JSON admission

`scripts/security-ops.py check-scope` reads JSON (not the illustrative YAML above). Use `authorization.status`, nonempty `authorization.evidence`, `network_profile.mode`, and `scope.allowed_actions`/`prohibited_actions`. Active network cases list exact strings in `scope.assets`. Offline cases list objects in `scope.samples` with an existing absolute `path` and `sha256`; only `static_analysis` is admitted. Read-only planning needs no executable gate or manufactured authorization record. Scope checks declare admission, not authorization proof, network enforcement, a sandbox, or permission for other mutations. See `docs/SECURITY_OPS.ko.md` for examples.

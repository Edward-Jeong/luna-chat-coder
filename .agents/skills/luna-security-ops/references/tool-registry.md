# Luna Security Ops Tool Registry Contract

The tool registry is a runtime inventory, not a routing table. Routing decides **what capability is needed**; the registry answers **which verified tool is available**.

## Principles

1. Never guess tool installation state or path.
2. Prefer already installed and repository-approved tooling.
3. Installation is not implicit. Package installation or system mutation follows the host/repository execution policy.
4. Record version and verification command when a tool is used materially.
5. A missing tool should first trigger an equivalent-tool or built-in-capability check before installation is proposed.

## Suggested machine-local schema

```json
{
  "schemaVersion": "0.1",
  "generatedAt": "ISO-8601",
  "tools": {
    "semgrep": {
      "status": "installed|missing|unknown",
      "path": "absolute-path-or-null",
      "version": "string-or-null",
      "verification": "command-or-null"
    }
  }
}
```

## Initial registry categories

- Source/SAST: Semgrep, CodeQL, Bandit, gosec, SpotBugs/FindSecBugs
- Supply chain: Syft, Trivy, OSV-Scanner, CycloneDX tooling, Cosign, Gitleaks
- Network/protocol: Wireshark/tshark, tcpdump, Nmap
- Forensics: Volatility, Plaso, Autopsy-compatible workflows
- Malware/offline: YARA, capa, static PE/ELF tooling
- Cloud/container: Docker, kubectl, Trivy, kube-bench where applicable

The concrete generated registry file should remain machine-local or gitignored unless it contains no environment-specific or sensitive paths.

#!/usr/bin/env python3
"""Read-only inventory of repository-local Luna instruction surfaces."""

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


CONFIG_NAMES = {"config.toml", "mcp.json", ".mcp.json", "plugin.json", "plugins.json"}
LONG_SKILL_BYTES = 8_000


def tracked_files(root):
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=False
    )
    if result.returncode == 0:
        paths = [Path(p.decode("utf-8", "surrogateescape")) for p in result.stdout.split(b"\0") if p]
    else:
        paths = [p.relative_to(root) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    # Include a newly added skill in a local working tree before it is staged.
    skill_root = root / ".agents" / "skills"
    if skill_root.is_dir():
        paths.extend(p.relative_to(root) for p in skill_root.glob("*/SKILL.md"))
    return sorted({p for p in paths if (root / p).is_file() and not (root / p).is_symlink()})


def paragraphs(content):
    return [" ".join(block.split()) for block in re.split(r"\n\s*\n", content)
            if len(" ".join(block.split())) >= 160 and not block.lstrip().startswith("```")]


def audit(root, deep=False):
    files = tracked_files(root)
    names = [p.as_posix() for p in files]
    instruction = [p for p in files if p.name == "AGENTS.md"]
    protocols = [p for p in files if p.as_posix() == "docs/CORE_ENGINEERING_PROTOCOL_V2.md"]
    skills = [p for p in files if re.fullmatch(r"\.agents/skills/[^/]+/SKILL\.md", p.as_posix())]
    references = [p for p in files if p.as_posix().startswith(".agents/skills/") and "/references/" in p.as_posix()]
    agents = [p for p in files if p.as_posix().startswith("integrations/codex/agents/") and p.suffix == ".toml"]
    configs = [p for p in files if p.name in CONFIG_NAMES or p.as_posix().startswith(".codex/")]

    def group(paths):
        return {"count": len(paths), "bytes": sum((root / p).stat().st_size for p in paths),
                "files": [p.as_posix() for p in paths]}

    findings = []
    for p in skills:
        body = (root / p).read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", body, re.S)
        if not frontmatter or not all(re.search(rf"^{key}:\s*\S+", frontmatter.group(1), re.M)
                                       for key in ("name", "description")):
            findings.append({"kind": "missing-metadata", "path": p.as_posix()})
        if (root / p).stat().st_size > LONG_SKILL_BYTES:
            findings.append({"kind": "large-skill-review", "path": p.as_posix(),
                             "bytes": (root / p).stat().st_size})

    if deep:
        occurrences = defaultdict(set)
        for p in instruction + protocols + skills + agents:
            for paragraph in paragraphs((root / p).read_text(encoding="utf-8")):
                occurrences[paragraph].add(p.as_posix())
        for paragraph, paths in occurrences.items():
            if len(paths) > 1:
                findings.append({"kind": "exact-overlap", "paths": sorted(paths),
                                 "excerpt": paragraph[:120]})
        # References to explicit repository paths are checked without following arbitrary links.
        for p in instruction + protocols + skills + agents:
            content = (root / p).read_text(encoding="utf-8")
            for candidate in set(re.findall(r"`((?:\.agents/skills|docs|templates|integrations/codex)/[^`\s]+)`", content)):
                path = candidate.rstrip(".,;:")
                if path not in names and not (root / path).exists():
                    findings.append({"kind": "missing-reference", "path": p.as_posix(), "target": path})

    return {"root": str(root), "groups": {
        "instructions": group(instruction), "protocol": group(protocols),
        "skill_bodies": group(skills), "skill_references": group(references),
        "optional_agents": group(agents), "repository_configs": group(configs)},
        "findings": sorted(findings, key=lambda x: (x["kind"], x.get("path", ""))),
        "runtime_plugins_mcp": "not observed (repository files cannot establish installation or connectivity)"}


def markdown(report):
    lines = ["# Luna Health Check", "", "| Surface | Files | Bytes |", "| --- | ---: | ---: |"]
    for name, group in report["groups"].items():
        lines.append(f"| {name.replace('_', ' ')} | {group['count']} | {group['bytes']:,} |")
    lines += ["", f"Runtime plugins/MCP: {report['runtime_plugins_mcp']}", "",
              "References and optional agents are not an always-loaded context budget.", "", "## Review signals", ""]
    if not report["findings"]:
        lines.append("No deterministic review signals found.")
    for finding in report["findings"]:
        lines.append(f"- {finding['kind']}: {finding.get('path', ', '.join(finding.get('paths', [])))}" +
                     (f" ({finding['bytes']:,} bytes)" if "bytes" in finding else "") +
                     (f" -> {finding['target']}" if "target" in finding else ""))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit(args.root.resolve(), args.deep)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else markdown(report))


if __name__ == "__main__":
    main()

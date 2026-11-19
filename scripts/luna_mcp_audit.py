#!/usr/bin/env python3
"""Read-only MCP package-selector audit. Never runs MCP servers or packages."""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None  # Python 3.10: TOML must be reviewed manually

CONFIGS = (".mcp.json", "mcp.json", ".codex/config.toml", ".cursor/mcp.json", ".vscode/mcp.json")
EXACT_VERSION = re.compile(r"^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?(?:\+[A-Za-z0-9.-]+)?$")
PACKAGE_NAME = re.compile(r"^(?:@[A-Za-z0-9_.-]+/)?[A-Za-z0-9_.-]+$")


def classify_selector(value):
    """Classify the direct npm selector, not transitive dependencies or vulnerabilities."""
    if not isinstance(value, str) or not value:
        return "review", "invalid-selector"
    if value.startswith(("file:", "git+", "http:", "https:", ".", "/")):
        return "review", "non-registry-selector"
    position = value.rfind("@")
    name, version = (value[:position], value[position + 1:]) if position > 0 else (value, "")
    if not PACKAGE_NAME.fullmatch(name):
        return "review", "unsupported-selector"
    if not version:
        return "mutable", "version-not-pinned"
    if EXACT_VERSION.fullmatch(version):
        return "pinned", "exact-direct-npm-version"
    return "mutable", "range-or-tag"


def selectors(command, args):
    """Only understand simple npm execution patterns; never guess unknown flags."""
    if not isinstance(command, str) or not isinstance(args, list) or not all(isinstance(x, str) for x in args):
        return None
    executable = command.replace("\\", "/").rsplit("/", 1)[-1].lower()
    if executable in ("npx", "npx.cmd", "npx.exe", "bunx", "bunx.cmd"):
        tokens = args
    elif executable in ("pnpm", "pnpm.cmd", "yarn", "yarn.cmd") and args[:1] == ["dlx"]:
        tokens = args[1:]
    else:
        return None
    found = []
    i = 0
    while i < len(tokens):
        arg = tokens[i]
        if arg in ("-p", "--package"):
            if i + 1 >= len(tokens):
                return None
            found.append(tokens[i + 1])
            i += 2
            continue
        if arg.startswith("--package="):
            found.append(arg.split("=", 1)[1])
            i += 1
            continue
        if arg in ("-y", "--yes", "--no-install", "--offline", "--quiet", "--"):
            i += 1
            continue
        if arg.startswith("-"):
            return None
        if not found:
            found.append(arg)
        return found
    return found or None


def audit(root, configs=None):
    root = Path(root).resolve()
    selected = list(configs) if configs is not None else [
        path for path in CONFIGS if (root / path).exists() or (root / path).is_symlink()
    ]
    result = {"configs": [], "findings": [], "summary": {"pinned": 0, "mutable": 0, "review": 0}}

    def add(config, server, classification, reason):
        result["findings"].append({"config": config, "server": server,
                                   "classification": classification, "reason": reason})
        result["summary"][classification] += 1

    for raw_path in selected:
        path = Path(raw_path)
        shown = path.as_posix()
        if path.is_absolute() or ".." in path.parts:
            add("<rejected-path>", "<config>", "review", "path-outside-root")
            continue
        file = root / path
        if (any(root.joinpath(*path.parts[:i]).is_symlink() for i in range(1, len(path.parts) + 1))
                or not file.resolve().is_relative_to(root)):
            add(shown, "<config>", "review", "symlink-or-escape")
            continue
        if not file.is_file():
            add(shown, "<config>", "review", "missing-config")
            continue
        result["configs"].append(shown)
        try:
            with file.open("rb") as stream:
                if file.suffix == ".toml":
                    if tomllib is None:
                        add(shown, "<config>", "review", "requires-python-3.11-for-toml")
                        continue
                    data = tomllib.load(stream)
                    servers = data.get("mcp_servers")
                elif file.suffix == ".json":
                    data = json.load(stream)
                    servers = data.get("mcpServers", data.get("servers")) if isinstance(data, dict) else None
                else:
                    add(shown, "<config>", "review", "unsupported-format")
                    continue
        except (OSError, ValueError, UnicodeError):
            add(shown, "<config>", "review", "unreadable-config")
            continue
        if not isinstance(servers, dict):
            add(shown, "<config>", "review", "missing-server-map")
            continue
        for name, definition in sorted(servers.items()):
            safe_name = name if isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", name) else "<server>"
            if not isinstance(definition, dict):
                add(shown, safe_name, "review", "invalid-definition")
                continue
            packages = selectors(definition.get("command"), definition.get("args"))
            if packages is None:
                add(shown, safe_name, "review", "unsupported-or-ambiguous-command")
                continue
            for package in packages:
                classification, reason = classify_selector(package)
                add(shown, safe_name, classification, reason)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--config", action="append", help="Repo-relative config; repeatable")
    parser.add_argument("--fail-on-mutable", action="store_true")
    parser.add_argument("--fail-on-review", action="store_true")
    args = parser.parse_args(argv)
    report = audit(args.root, args.config)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return int(bool((args.fail_on_mutable and report["summary"]["mutable"]) or
                    (args.fail_on_review and report["summary"]["review"])))


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Safely install Luna's opt-in prune-tests skill for the current Codex user.

The only install targets are ~/.agents/skills/prune-tests and a Luna-owned
manifest under ~/.agents/luna. No repository or Codex configuration is edited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

SKILL = "prune-tests"
OWNED_FILES = ("SKILL.md", "LICENSE.upstream.md")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".luna-skill-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def assert_not_link(*paths: Path) -> None:
    for path in paths:
        if path.is_symlink():
            raise ValueError(f"refusing symlinked installation path: {path}")


def install(source_root: Path, agents_home: Path, *, dry_run: bool = False,
            uninstall: bool = False) -> dict:
    source = source_root / "integrations" / "codex" / "skills" / SKILL
    destination = agents_home / "skills" / SKILL
    manifest = agents_home / "luna" / f"{SKILL}-install.json"
    assert_not_link(agents_home, agents_home / "skills", destination,
                    agents_home / "luna", manifest)

    expected = {}
    if not uninstall:
        for name in OWNED_FILES:
            item = source / name
            assert_not_link(item)
            if not item.is_file():
                raise ValueError(f"missing skill source: {item}")
            expected[name] = item.read_bytes()

    managed = None
    if manifest.exists():
        if not manifest.is_file():
            raise ValueError("invalid Luna skill installation manifest")
        record = json.loads(manifest.read_text(encoding="utf-8"))
        if (not isinstance(record, dict) or record.get("version") != 1
                or record.get("skill") != SKILL or not isinstance(record.get("files"), dict)
                or set(record["files"]) != set(OWNED_FILES)
                or any(not isinstance(value, str) or len(value) != 64
                       for value in record["files"].values())):
            raise ValueError("invalid Luna skill installation manifest")
        managed = record["files"]

    if managed is None:
        if uninstall:
            raise ValueError("managed prune-tests installation not found")
        if destination.exists():
            raise ValueError(f"existing unmanaged skill directory; refusing overwrite: {destination}")
    else:
        for name in OWNED_FILES:
            target = destination / name
            assert_not_link(target)
            if not target.is_file() or digest(target.read_bytes()) != managed[name]:
                raise ValueError(f"modified or missing managed skill file; refusing overwrite: {target}")

    if uninstall:
        if not dry_run:
            for name in OWNED_FILES:
                (destination / name).unlink()
            if not any(destination.iterdir()):
                destination.rmdir()
            manifest.unlink()
        return {"action": "uninstall", "dry_run": dry_run,
                "managed_files": len(OWNED_FILES), "project_files_modified": False}

    changed = sum(managed is None or digest(content) != managed[name]
                  for name, content in expected.items())
    if not dry_run:
        # All conflicts are checked before the first write; disk errors are not
        # an atomic multi-file transaction and must be inspected before retry.
        for name, content in expected.items():
            target = destination / name
            if managed is None or digest(content) != managed[name]:
                atomic_write(target, content)
        record = {"version": 1, "skill": SKILL,
                  "files": {name: digest(data) for name, data in expected.items()}}
        atomic_write(manifest, (json.dumps(record, indent=2) + "\n").encode("utf-8"))
    return {"action": "install", "dry_run": dry_run, "changed_files": changed,
            "skill_path": str(destination), "project_files_modified": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--agents-home", type=Path, default=Path.home() / ".agents")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = install(args.source_root.expanduser(), args.agents_home.expanduser(),
                         dry_run=args.dry_run, uninstall=args.uninstall)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Luna shared skill installer: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

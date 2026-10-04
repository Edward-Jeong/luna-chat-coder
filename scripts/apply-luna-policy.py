#!/usr/bin/env python3
"""Preview or apply versioned Luna defaults without replacing project guidance."""
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

REVISION = "2.1"
BEGIN = b"<!-- BEGIN LUNA MANAGED POLICY -->"
END = b"<!-- END LUNA MANAGED POLICY -->"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, relative):
    path = root / relative
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"Refusing symlink: {part}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Expected a file: {path}")
    return path


def active_guidance(root):
    override = safe_path(root, "AGENTS.override.md")
    if override.exists() and override.read_bytes().strip():
        return override
    return safe_path(root, "AGENTS.md")


def block(pointer):
    return BEGIN + b"\n" + (
        "## Luna shared engineering policy (revision 2.1)\n\n"
        f"For material engineering work, read `{pointer}`. "
        "It is canonical for Luna's shared workflow, verification, review independence, "
        "and readiness; older inherited Luna summaries must not redefine that contract. "
        "Preserve this project's technology choices, security boundaries, required checks, "
        "and stricter review/approval rules. This update does not authorize new scope. "
        "Required verification must pass and material implementation needs independent "
        "Code Review before merge-ready. Missing/failing/pending required checks or "
        "independent review mean review-ready; disclosure is not a pass. "
        "A same-session role switch is self-review. Continue other authorized work.\n"
    ).encode() + END + b"\n"


def merge_guidance(original, managed):
    begins, ends = original.count(BEGIN), original.count(END)
    if begins != ends or begins > 1:
        raise ValueError("Malformed or duplicate Luna managed markers")
    if begins:
        start, finish = original.index(BEGIN), original.index(END)
        if finish < start:
            raise ValueError("Luna managed markers are out of order")
        finish += len(END)
        if original[finish:finish + 1] == b"\n":
            finish += 1
        return original[:start] + managed + original[finish:]
    separator = b"\n\n" if original and not original.endswith(b"\n") else b"\n" if original else b""
    return original + separator + managed


def plan_update(root, policy, global_scope=False):
    # Resolve only after rejecting the root itself as a symlink.
    if root.is_symlink():
        raise ValueError(f"Refusing symlink root: {root}")
    root = root.absolute()
    if root.exists() and not root.is_dir():
        raise ValueError(f"Expected a directory: {root}")
    directory = "luna" if global_scope else "docs/luna"
    policy_path = safe_path(root, directory + "/CORE_ENGINEERING_PROTOCOL_V2.md")
    lock_path = safe_path(root, directory + "/policy-lock.json")
    guidance = active_guidance(root)
    original = guidance.read_bytes() if guidance.exists() else b""
    if policy_path.exists():
        current = policy_path.read_bytes()
        if lock_path.exists():
            lock = json.loads(lock_path.read_bytes())
            if lock.get("sha256") != digest(current):
                raise ValueError(f"Local policy edits conflict: {policy_path}")
        elif current != policy:
            raise ValueError(f"Unmanaged policy conflicts: {policy_path}")
    elif lock_path.exists():
        raise ValueError(f"Managed policy is missing: {policy_path}")
    pointer = policy_path.as_posix() if global_scope else policy_path.relative_to(root).as_posix()
    lock = {"revision": REVISION, "sha256": digest(policy), "source": "Edward-Jeong/luna-chat-coder"}
    return {
        policy_path: policy,
        lock_path: (json.dumps(lock, indent=2) + "\n").encode(),
        guidance: merge_guidance(original, block(pointer)),
    }


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".luna-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        else:
            os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def apply_plan(plan):
    changes = {path: data for path, data in plan.items()
               if not path.exists() or path.read_bytes() != data}
    # Check every backup before the first write; never overwrite another backup.
    for path in changes:
        backup = path.with_name(path.name + ".luna-backup")
        safe_path(path.parent, backup.name)
        if path.exists() and backup.exists() and backup.read_bytes() != path.read_bytes():
            raise ValueError(f"Backup already exists with different contents: {backup}")
    for path, data in changes.items():
        if path.exists():
            backup = path.with_name(path.name + ".luna-backup")
            if not backup.exists():
                write_atomic(backup, path.read_bytes())
        write_atomic(path, data)
    return list(changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, action="append", default=[])
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write changes; default is preview only")
    args = parser.parse_args()
    if not args.project and args.codex_home is None:
        parser.error("Select --project PATH and/or --codex-home PATH")
    policy = (Path(__file__).resolve().parents[1] / "docs/CORE_ENGINEERING_PROTOCOL_V2.md").read_bytes()
    try:
        targets = [(p, False) for p in args.project]
        if args.codex_home is not None:
            targets.append((args.codex_home, True))
        combined = {}
        for root, global_scope in targets:
            for path, data in plan_update(root, policy, global_scope).items():
                if path in combined and combined[path] != data:
                    raise ValueError(f"Overlapping update targets: {path}")
                combined[path] = data
        changes = [p for p, data in combined.items() if not p.exists() or p.read_bytes() != data]
        for path in changes:
            print(("UPDATE " if args.apply else "PREVIEW ") + str(path))
        if args.apply:
            apply_plan(combined)
        print(f"{'Applied' if args.apply else 'Previewed'} {len(changes)} file changes")
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"No automatic conflict resolution: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

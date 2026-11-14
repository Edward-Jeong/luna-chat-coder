#!/usr/bin/env python3
"""Install the opt-in Luna CLI launcher for every local Codex project.

The installer only owns ~/.codex/luna/runtime and ~/.codex/luna/bin.
It never changes AGENTS.md, project files, or Codex config/hook files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile


RUNTIME = ("luna_workspace.py", "luna_model_router.py")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_launcher(python: str, windows: bool) -> tuple[str, bytes]:
    if windows:
        safe_python = python.replace("%", "%%")
        return "luna.cmd", (f'@echo off\r\n"{safe_python}" "%~dp0..\\runtime\\luna_workspace.py" %*\r\n').encode("utf-8")
    return "luna", (f'#!/bin/sh\nexec {shlex.quote(python)} "$(dirname "$0")/../runtime/luna_workspace.py" "$@"\n').encode("utf-8")


def read_manifest(path: Path) -> dict:
    if not path.exists():
        return {}
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict) or not isinstance(result.get("files"), dict):
        raise ValueError("invalid Luna installer manifest; refusing to modify installation")
    return result["files"]


def atomic_write(path: Path, data: bytes, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp = tempfile.mkstemp(prefix=".luna-install-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.chmod(tmp, 0o700 if executable else 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def add_windows_path(bin_dir: Path) -> bool:
    if sys.platform != "win32":
        raise ValueError("--add-to-user-path is available on Windows only")
    import winreg
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
        try:
            old, old_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            old, old_type = "", winreg.REG_EXPAND_SZ
        entries = [x for x in old.split(";") if x]
        if any(os.path.normcase(os.path.normpath(os.path.expandvars(x))) ==
               os.path.normcase(os.path.normpath(str(bin_dir))) for x in entries):
            return False
        updated = ";".join([*entries, str(bin_dir)])
        winreg.SetValueEx(key, "Path", 0, old_type if old_type in (winreg.REG_SZ, winreg.REG_EXPAND_SZ) else winreg.REG_EXPAND_SZ, updated)
    return True


def install(source: Path, home: Path, python: str, *, windows: bool, remove: bool = False,
            dry_run: bool = False) -> dict:
    target_base = home / "luna"
    manifest = target_base / "installation.json"
    originals = read_manifest(manifest)
    runtime = target_base / "runtime"
    bin_dir = target_base / "bin"
    launcher_name, launcher_content = build_launcher(python, windows)
    for parent in (target_base, runtime, bin_dir):
        if parent.is_symlink():
            raise ValueError(f"refusing symlinked Luna directory: {parent}")
    files = {runtime / name: (source / "scripts" / name).read_bytes() for name in RUNTIME}
    files[bin_dir / launcher_name] = launcher_content
    # All-or-nothing conflict preflight. Unrelated user changes are never overwritten.
    for path in files:
        key = str(path.relative_to(target_base)).replace("\\", "/")
        if path.is_symlink():
            raise ValueError(f"refusing symlink at managed destination: {path}")
        if path.exists() and (not path.is_file() or sha(path.read_bytes()) != originals.get(key, "")):
            if not remove and path.is_file() and path.read_bytes() == files[path]:
                continue  # An identical initial install may be adopted.
            raise ValueError(f"existing unmanaged or modified installation: {path}")
    if remove:
        if not originals:
            raise ValueError("Luna installation manifest not found")
        if not dry_run:
            for path in files:
                path.unlink(missing_ok=True)
            manifest.unlink(missing_ok=True)
        return {"action": "uninstall", "managed_files": len(files), "metrics_retained": True}
    changed = sum(not path.exists() or path.read_bytes() != data for path, data in files.items())
    if not dry_run:
        for path, data in files.items():
            if not path.exists() or path.read_bytes() != data:
                atomic_write(path, data, executable=(path.name == "luna"))
        items = {str(path.relative_to(target_base)).replace("\\", "/"): sha(data) for path, data in files.items()}
        atomic_write(manifest, (json.dumps({"version": 1, "files": items}, indent=2) + "\n").encode("utf-8"))
    return {"action": "install", "changed_files": changed, "launcher": str(bin_dir / launcher_name),
            "project_files_modified": False, "dry_run": dry_run}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path,
                        default=Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex")))
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--python", default=sys.executable, help="Python used by the launcher")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--add-to-user-path", action="store_true", help="Windows HKCU PATH (no admin required)")
    args = parser.parse_args(argv)
    try:
        home = args.codex_home.expanduser().resolve()
        result = install(args.source_root.resolve(strict=True), home, args.python,
                         windows=(sys.platform == "win32"), remove=args.uninstall, dry_run=args.dry_run)
        if args.add_to_user_path and not args.uninstall and not args.dry_run:
            result["windows_path_updated"] = add_windows_path(home / "luna" / "bin")
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Luna install: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

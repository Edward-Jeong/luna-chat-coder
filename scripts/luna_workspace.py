#!/usr/bin/env python3
"""Shared per-user Luna/Codex runner; project instructions remain owned by Codex."""
from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

import luna_model_router as routing


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex")).expanduser().resolve()


def project_root(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError(f"not a project directory: {path}")
    # Select the repository root without modifying local project configuration.
    check = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, errors="replace", check=False)
    if check.returncode == 0 and check.stdout.strip():
        return Path(check.stdout.strip()).resolve(strict=True)
    return path


def project_key(path: Path) -> str:
    normalized = os.path.normcase(str(path.resolve()))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:24]


def session_path(home: Path, project: Path) -> Path:
    return home / "luna" / "sessions" / (project_key(project) + ".json")


def read_session(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("invalid Luna session file; restore or reset it manually")
    tid = data.get("thread_id")
    if tid is not None and (not isinstance(tid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{5,128}", tid)):
        raise ValueError("invalid thread identifier in Luna session file")
    return data


def write_session(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp = tempfile.mkstemp(prefix=".luna-session-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=True, sort_keys=True)
            stream.write("\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def session_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = path.with_suffix(".lock")
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise RuntimeError("another Luna run is active for this project; retry after it finishes") from exc
    try:
        with os.fdopen(fd, "w", encoding="ascii") as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        lock.unlink(missing_ok=True)


def choose(task: str, session: dict, options: argparse.Namespace, history: list[dict], invalid: int) -> dict:
    risk = options.risk
    # Do not inadvertently lower security posture within a continuing session.
    if risk == "auto" and session.get("risk") in ("high", "critical"):
        risk = session["risk"]
    return routing.select_model(task, kind=options.kind, risk=risk, files=options.files,
                                failed_runs=options.failed_runs,
                                failure_reason=options.failure_reason,
                                history=history, adaptive=not invalid and not options.no_adaptive)


def command_for(task: str, decision: dict, thread_id: str | None, codex_binary: str) -> list[str]:
    command = [codex_binary, "exec", "--json", "-m", decision["model"],
               "-c", f'model_reasoning_effort="{decision["reasoning_effort"]}"']
    if thread_id:
        command.extend(["resume", thread_id])
    # Codex supports PROMPT=-, which reads standard input. Never put an
    # untrusted natural-language prompt on a Windows .cmd command line.
    command.append("-")
    return command


def run_turn(task: str, project: Path, home: Path, metrics: Path,
             options: argparse.Namespace) -> int:
    if not task.strip():
        raise ValueError("an empty request cannot be executed")
    path = session_path(home, project)
    with session_lock(path):
        previous = read_session(path)
        history, invalid = routing.parse_metrics(metrics)
        if invalid:
            print(f"[Luna] {invalid} damaged metric line(s); adaptive selection disabled", file=sys.stderr)
        decision = choose(task, previous, options, history, invalid)
        command = command_for(task, decision, previous.get("thread_id"), options.codex_bin)
        label = decision["model"] + " / " + decision["reasoning_effort"]
        if options.plan or options.dry_run:
            print(json.dumps({"model": decision, "resume": bool(previous.get("thread_id")),
                              "project_id": project_key(project), "dry_run": bool(options.dry_run)}, indent=2))
            return 0
        if not shutil.which(options.codex_bin) and not Path(options.codex_bin).is_file():
            raise FileNotFoundError("Codex CLI is not available; install/login to Codex first")
        print(f"[Luna] {label} | {decision['kind']} | project {project_key(project)[:8]}", file=sys.stderr)
        started_thread = None
        usage = defaultdict(int)
        turns = 0
        # Standard Codex invocation: project-scoped AGENTS.md / skills / sandbox / approvals
        # are discovered and enforced by Codex, not reimplemented or bypassed here.
        with subprocess.Popen(command, cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=None, encoding="utf-8", errors="replace", text=True) as process:
            assert process.stdout is not None and process.stdin is not None
            try:
                process.stdin.write(task)
                process.stdin.close()
            except BrokenPipeError:
                # Codex may reject its model/config before reading stdin.
                pass
            for line in process.stdout:
                try:
                    event = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if not isinstance(event, dict):
                    continue
                if event.get("type") == "thread.started":
                    tid = event.get("thread_id")
                    if isinstance(tid, str) and re.fullmatch(r"[A-Za-z0-9_-]{5,128}", tid):
                        started_thread = tid
                token = routing.extract_usage(event)
                if token is not None:
                    turns += 1
                    for key, value in token.items():
                        usage[key] += value
                item = event.get("item")
                if event.get("type") == "item.completed" and isinstance(item, dict):
                    if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                        try:
                            print(item["text"], flush=True)
                        except UnicodeEncodeError:
                            # Legacy Windows CI/terminals may use cp1252 instead of UTF-8.
                            encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
                            escaped = item["text"].encode(encoding, errors="backslashreplace").decode(encoding)
                            print(escaped, flush=True)
            exit_code = process.wait()
        if previous.get("thread_id") and started_thread and previous["thread_id"] != started_thread:
            print("[Luna] Codex resumed an unexpected thread; preserving previous session pointer", file=sys.stderr)
        elif started_thread:
            write_session(path, {"thread_id": started_thread, "kind": decision["kind"],
                                 "risk": decision["risk"], "updated_at": datetime.now(timezone.utc).isoformat()})
        elif previous.get("thread_id"):
            # A CLI may omit thread.started on resume; do not discard known context.
            pass
        else:
            print("[Luna] No thread ID reported: next request starts a new session", file=sys.stderr)
        usage_dict = dict(usage) if turns else None
        entry = {"event": "run", "run_id": str(uuid.uuid4()),
                 "timestamp": datetime.now(timezone.utc).isoformat(),
                 "project_id": project_key(project), "source": "luna-workspace",
                 "model": decision["model"], "reasoning_effort": decision["reasoning_effort"],
                 "kind": decision["kind"], "risk": decision["risk"],
                 "route_reasons": decision["reasons"], "exit_code": exit_code,
                 "verification": "unverified", "failure_reason": "unknown",
                 "usage": usage_dict,
                 "api_equivalent_usd": routing.api_equivalent_usd(decision["model"], usage_dict or {}),
                 "pricing_date": routing.PRICE_DATE}
        routing.append_metric(metrics, entry)
        print(f"[Luna] run={entry['run_id']} | tokens={usage_dict or 'unknown'} | verification=unverified", file=sys.stderr)
        return exit_code


def reset_session(path: Path) -> None:
    with session_lock(path):
        # Drop only Luna's pointer, never Codex's native conversation history.
        path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Luna global natural-language model router for Codex CLI")
    parser.add_argument("--project", default=".", help="project directory; defaults to current repository")
    parser.add_argument("--codex-home", type=Path, default=codex_home())
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--metrics-file", type=Path)
    parser.add_argument("--kind", choices=routing.KINDS)
    parser.add_argument("--risk", default="auto", choices=("auto", "low", "medium", "high", "critical"))
    parser.add_argument("--files", type=int, default=0)
    parser.add_argument("--failed-runs", type=int, default=0)
    parser.add_argument("--failure-reason", default="unknown", choices=routing.FAILURES)
    parser.add_argument("--no-adaptive", action="store_true")
    parser.add_argument("--plan", action="store_true", help="show the model choice without executing")
    parser.add_argument("--dry-run", action="store_true", help="same as --plan")
    parser.add_argument("prompt", nargs="*", help="natural-language task; omit to enter chat mode")
    args = parser.parse_args(argv)
    try:
        project = project_root(args.project)
        home = args.codex_home.expanduser().resolve()
        metrics = (args.metrics_file.expanduser().resolve() if args.metrics_file
                   else home / "luna" / "usage.jsonl")
        text = " ".join(args.prompt)
        if text == "stats":
            return routing.cli(["--metrics-file", str(metrics), "report"])
        if text == "doctor":
            print(json.dumps({"project": str(project), "project_id": project_key(project),
                              "codex_cli": shutil.which(args.codex_bin), "session_present": session_path(home, project).exists(),
                              "metrics_path": str(metrics)}, indent=2))
            return 0
        if text.startswith("verify "):
            fields = text.split()
            if len(fields) not in (3, 4) or fields[2] not in ("passed", "failed"):
                parser.error("usage: luna verify RUN_ID passed|failed [reason]")
            reason = fields[3] if len(fields) == 4 else ("none" if fields[2] == "passed" else "unknown")
            return routing.cli(["--metrics-file", str(metrics), "record", fields[1],
                                "--verification", fields[2], "--failure-reason", reason])
        if text == "new":
            reset_session(session_path(home, project))
            print("[Luna] New thread selected; previous Codex thread remains recoverable", file=sys.stderr)
            return 0
        if text:
            return run_turn(text, project, home, metrics, args)
        if args.plan or args.dry_run:
            parser.error("--plan requires a task")
        print(f"Luna ready in {project}. Type a request; :new / :stats / :exit", file=sys.stderr)
        while True:
            try:
                task = input("Luna> ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                return 0
            if not task:
                continue
            if task.lower() in (":exit", ":quit", ":q"):
                return 0
            if task.lower() == ":new":
                reset_session(session_path(home, project))
                print("[Luna] New thread", file=sys.stderr)
                continue
            if task.lower() == ":stats":
                routing.cli(["--metrics-file", str(metrics), "report"])
                continue
            result = run_turn(task, project, home, metrics, args)
            if result:
                print(f"[Luna] Codex exit code {result}; no implicit model fallback", file=sys.stderr)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"luna workspace: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

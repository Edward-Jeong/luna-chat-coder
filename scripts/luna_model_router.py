#!/usr/bin/env python3
"""Deterministic, opt-in Codex model selection and privacy-minimal usage metrics.

No API credentials, third-party libraries, network calls, or prompt retention.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

# Standard short-context API-equivalent USD rates per million tokens.
# These are NOT ChatGPT subscription debits, Codex credits, or a billing API.
PRICE_DATE = "2026-11-14"
MODELS = (
    ("gpt-6-luna", "low", 0.10, 0.01, 0.50),
    ("gpt-6.1-terra", "low", 1.00, 0.05, 5.00),
    ("gpt-6.1-sol", "medium", 2.00, 0.10, 10.00),
    ("gpt-6-astra", "high", 10.00, 1.00, 50.00),
)
MODEL_BY_NAME = {row[0]: row for row in MODELS}
REASONING = {"low", "medium", "high"}
KINDS = ("routine", "coding", "incident", "security", "architecture", "reverse")
FAILURES = ("none", "reasoning", "environment", "external", "unknown")
DEFAULT_METRICS = Path.home() / ".codex" / "luna" / "usage.jsonl"

PATTERNS = {
    "reverse": r"역공학|디컴파일|바이너리 분석|리버스 엔지니어링|reverse.engineer|decompil",
    "architecture": r"아키텍처|재설계|전체 구조|설계|architecture|refactor|migration|마이그레이션",
    "incident": r"장애|실패 원인|오류 분석|원인 분석|로그 분석|디버깅|incident|root cause|debug|outage|원인 추적",
    "security": r"취약점|보안 진단|권한 상승|인증 우회|인증|인가|접근제어|침투|공격|exploit|vulnerability|security review|cve-|sast|authentication|authorization|\brbac\b|\boauth\b",
    "coding": r"구현|개발|코드|수정|테스트|스크립트|기능 추가|만들어|구축|제작|생성|fix|implement|create|build|develop|code|test|patch|pull request|\bpr\b",
}
ROUTINE = re.compile(r"요약|정리|초안|번역|format|summari|draft|translate|리스트|목록", re.I)
HEAVY = re.compile(r"복합|다중|전체|대규모|critical|high.risk|high severity|근본 원인|복잡|massive|cross.system", re.I)


def task_kind(task: str, explicit: str | None = None) -> str:
    if explicit:
        if explicit not in KINDS:
            raise ValueError("invalid task kind")
        return explicit
    for kind in ("reverse", "architecture", "incident", "security", "coding"):
        if re.search(PATTERNS[kind], task, re.I):
            return kind
    return "routine"


def parse_metrics(path: Path) -> tuple[list[dict], int]:
    if not path.exists():
        return [], 0
    runs: dict[str, dict] = {}
    invalid = 0
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                entry = json.loads(line)
                if not isinstance(entry, dict) or not isinstance(entry.get("run_id"), str):
                    raise ValueError("missing run_id")
                rid = entry["run_id"]
                if entry.get("event") == "run":
                    runs[rid] = entry
                elif entry.get("event") == "verification" and rid in runs:
                    if entry.get("verification") not in ("passed", "failed") or entry.get("failure_reason") not in FAILURES:
                        raise ValueError("invalid verification")
                    runs[rid].update(verification=entry["verification"], failure_reason=entry["failure_reason"])
                else:
                    invalid += 1
            except (json.JSONDecodeError, ValueError, TypeError):
                invalid += 1
    return list(runs.values()), invalid


def select_model(task: str, *, kind: str | None = None, risk: str = "auto", files: int = 0,
                 failed_runs: int = 0, failure_reason: str = "unknown",
                 history: list[dict] | None = None, adaptive: bool = True) -> dict:
    if not task.strip():
        raise ValueError("task cannot be empty")
    if risk not in ("auto", "low", "medium", "high", "critical") or files < 0 or failed_runs < 0:
        raise ValueError("invalid risk, file count or retry count")
    if failure_reason not in FAILURES:
        raise ValueError("invalid failure reason")
    category = task_kind(task, kind)
    reasons = [f"kind={category}"]
    explicit_high = risk in ("high", "critical")
    complex_task = bool(HEAVY.search(task)) or files >= 12
    # An explicit critical/high-risk call raises the floor. Not every CVE mention needs Astra.
    if category == "routine":
        tier, effort = (0, "low") if ROUTINE.search(task) and len(task) < 400 and files <= 1 else (2, "medium")
    elif category == "coding":
        tier, effort = (1, "medium") if files <= 1 and not complex_task and risk == "low" else (2, "medium")
    elif category in ("incident", "security"):
        tier, effort = 2, "high"
    else:
        tier, effort = 2, "high"
    if complex_task:
        tier = max(tier, 2)
        effort = "high"
        reasons.append("complexity_or_files")
    if category in ("reverse", "architecture") and (complex_task or explicit_high):
        tier = 3
        reasons.append("high_stakes_specialist")
    if risk == "critical" and category != "routine":
        tier = 3
        reasons.append("critical_risk")
    elif explicit_high:
        tier = max(tier, 2)
        effort = "high"
        reasons.append("explicit_high_risk")
    # Failed runs can be environmental; never upgrade on count alone.
    if failed_runs >= 2 and failure_reason == "reasoning":
        tier = min(3, max(2, tier + 1))
        effort = "high"
        reasons.append("verified_reasoning_failure")
    # Conservative, bounded adaptation: only verified outcomes; no automatic downgrades
    # for security/high-risk tasks and no use of unverified CLI exit codes as quality.
    samples = [r for r in (history or []) if r.get("kind") == category and r.get("model") == MODELS[tier][0]
               and r.get("verification") in ("passed", "failed")]
    if adaptive and risk not in ("high", "critical") and len(samples) >= 8 and tier < 3:
        failed = [r for r in samples if r.get("verification") == "failed"]
        reasoning_failures = sum(r.get("failure_reason") == "reasoning" for r in failed)
        if len(failed) / len(samples) >= 0.25 and reasoning_failures >= 3:
            tier += 1
            effort = "high" if tier >= 2 else "medium"
            reasons.append(f"historical_verified_reasoning_failures={reasoning_failures}/{len(samples)}")
    name = MODELS[tier][0]
    if tier == 3:
        effort = "high"
    elif tier == 2 and effort not in ("medium", "high"):
        effort = "medium"
    return {"model": name, "reasoning_effort": effort, "kind": category, "risk": risk,
            "reasons": reasons, "pricing_date": PRICE_DATE}


def api_equivalent_usd(model: str, usage: dict) -> float | None:
    if model not in MODEL_BY_NAME or usage.get("input_tokens") is None or usage.get("output_tokens") is None:
        return None
    _, _, input_rate, cached_rate, output_rate = MODEL_BY_NAME[model]
    total_input = usage["input_tokens"]
    cached = usage.get("cached_input_tokens") or 0
    output = usage["output_tokens"]
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (total_input, cached, output)):
        return None
    if min(total_input, cached, output) < 0 or cached > total_input:
        return None
    return round(((total_input - cached) * input_rate + cached * cached_rate + output * output_rate) / 1_000_000, 8)


def extract_usage(event: dict) -> dict | None:
    if event.get("type") != "turn.completed":
        return None
    usage = event.get("usage")
    if not isinstance(usage, dict):
        return None
    inp, out = usage.get("input_tokens"), usage.get("output_tokens")
    cache = usage.get("cached_input_tokens", 0)
    if any(not isinstance(x, int) or isinstance(x, bool) or x < 0 for x in (inp, out, cache)):
        return None
    if cache > inp:
        return None
    return {"input_tokens": inp, "output_tokens": out, "cached_input_tokens": cache}


def append_metric(path: Path, entry: dict) -> None:
    # Single OS append, no prompts, source code, logs, credentials, or raw trace.
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    data = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        if os.write(fd, data) != len(data):
            raise OSError("incomplete metrics write")
    finally:
        os.close(fd)


def aggregate(rows: list[dict]) -> dict:
    result = {}
    for model in (r[0] for r in MODELS):
        subset = [r for r in rows if r.get("model") == model]
        if not subset:
            continue
        valid = [r for r in subset if r.get("verification") in ("passed", "failed")]
        usage = [r.get("usage") for r in subset if isinstance(r.get("usage"), dict)]
        total_usd = sum(r.get("api_equivalent_usd") or 0 for r in subset)
        result[model] = {"runs": len(subset), "verified_runs": len(valid),
                         "verified_success_rate": round(sum(r["verification"] == "passed" for r in valid) / len(valid), 4) if valid else None,
                         "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
                         "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
                         "cached_input_tokens": sum(u.get("cached_input_tokens", 0) for u in usage),
                         "api_equivalent_usd_estimate": round(total_usd, 6)}
    return result


def cli(argv: list[str] | None = None) -> int:
    # Older Windows terminals use legacy code pages; never crash while printing
    # Korean task descriptions or multilingual agent output.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics-file", type=Path, default=DEFAULT_METRICS)
    sub = parser.add_subparsers(dest="command", required=True)
    for action in ("plan", "run"):
        p = sub.add_parser(action)
        p.add_argument("task", help="task description; never stored in usage metrics")
        p.add_argument("--kind", choices=KINDS)
        p.add_argument("--risk", default="auto", choices=("auto", "low", "medium", "high", "critical"))
        p.add_argument("--files", type=int, default=0)
        p.add_argument("--failed-runs", type=int, default=0)
        p.add_argument("--failure-reason", choices=FAILURES, default="unknown")
        p.add_argument("--no-adaptive", action="store_true")
        if action == "run":
            p.add_argument("--codex-bin", default="codex")
            p.add_argument("--dry-run", action="store_true")
            p.add_argument("--cwd", type=Path)
    p = sub.add_parser("record")
    p.add_argument("run_id")
    p.add_argument("--verification", required=True, choices=("passed", "failed"))
    p.add_argument("--failure-reason", choices=FAILURES, default="none")
    sub.add_parser("report")
    args = parser.parse_args(argv)
    try:
        rows, invalid = parse_metrics(args.metrics_file)
        if args.command == "report":
            print(json.dumps({"models": aggregate(rows), "invalid_metric_lines": invalid,
                              "pricing_date": PRICE_DATE, "billing_note": "API-equivalent estimate only; not Codex credits or subscription billing"}, indent=2))
            return 0
        if args.command == "record":
            if args.verification == "passed" and args.failure_reason != "none":
                parser.error("passed verification must have failure-reason=none")
            if args.verification == "failed" and args.failure_reason == "none":
                parser.error("failed verification requires a failure reason")
            if not any(r.get("run_id") == args.run_id for r in rows):
                parser.error("unknown run_id")
            append_metric(args.metrics_file, {"event": "verification", "run_id": args.run_id,
                                                 "verification": args.verification, "failure_reason": args.failure_reason,
                                                 "timestamp": datetime.now(timezone.utc).isoformat()})
            return 0
        if invalid:
            print(f"warning: {invalid} invalid metrics line(s); adaptive routing disabled", file=sys.stderr)
        decision = select_model(args.task, kind=args.kind, risk=args.risk, files=args.files,
                                failed_runs=args.failed_runs, failure_reason=args.failure_reason,
                                history=rows, adaptive=not args.no_adaptive and not invalid)
        if args.command == "plan":
            print(json.dumps(decision, ensure_ascii=True, indent=2))
            return 0
        command = [args.codex_bin, "exec", "--json", "-m", decision["model"],
                   "-c", f'model_reasoning_effort="{decision["reasoning_effort"]}"', args.task]
        if args.dry_run:
            print(json.dumps({"decision": decision, "command": command, "dry_run": True}, ensure_ascii=True, indent=2))
            return 0
        print(json.dumps({"decision": decision}, ensure_ascii=True), file=sys.stderr)
        run_id = str(uuid.uuid4())
        count = 0
        totals = defaultdict(int)
        proc = subprocess.Popen(command, cwd=args.cwd, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        assert proc.stdout is not None
        for line in proc.stdout:
            try:
                event = json.loads(line)
            except (json.JSONDecodeError, TypeError):
                continue
            if not isinstance(event, dict):
                continue
            u = extract_usage(event)
            if u is not None:
                count += 1
                for key, value in u.items():
                    totals[key] += value
            item = event.get("item")
            if event.get("type") == "item.completed" and isinstance(item, dict) and item.get("type") == "agent_message":
                if isinstance(item.get("text"), str):
                    print(item["text"], flush=True)
        exit_code = proc.wait()
        usage = dict(totals) if count else None
        entry = {"event": "run", "run_id": run_id, "timestamp": datetime.now(timezone.utc).isoformat(),
                 "model": decision["model"], "reasoning_effort": decision["reasoning_effort"],
                 "kind": decision["kind"], "risk": decision["risk"], "route_reasons": decision["reasons"],
                 "exit_code": exit_code, "verification": "unverified", "failure_reason": "unknown",
                 "usage": usage, "api_equivalent_usd": api_equivalent_usd(decision["model"], usage or {}),
                 "pricing_date": PRICE_DATE}
        append_metric(args.metrics_file, entry)
        print(json.dumps({"run_id": run_id, "exit_code": exit_code, "usage": usage,
                          "api_equivalent_usd_estimate": entry["api_equivalent_usd"],
                          "verification": "unverified"}, ensure_ascii=True), file=sys.stderr)
        return exit_code
    except (OSError, ValueError) as exc:
        print(f"luna router: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(cli())

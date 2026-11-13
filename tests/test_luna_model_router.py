"""Offline risk routing, accounting and Codex JSONL integration contract tests."""
import importlib.util
import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "scripts" / "luna_model_router.py"
spec = importlib.util.spec_from_file_location("luna_model_router", MOD)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


class DecisionTests(unittest.TestCase):
    def test_routine_summary_uses_luna(self):
        self.assertEqual(router.select_model("보고서 요약")["model"], "gpt-6-luna")

    def test_bounded_code_uses_terra_when_explicitly_low_risk(self):
        route = router.select_model("스크립트 코드 수정", risk="low", files=1)
        self.assertEqual((route["model"], route["reasoning_effort"]), ("gpt-6.1-terra", "medium"))

    def test_standard_code_uses_sol(self):
        self.assertEqual(router.select_model("신규 기능 개발 및 테스트")["model"], "gpt-6.1-sol")

    def test_security_default_sol_high(self):
        self.assertEqual(router.select_model("SecuMS CVE-2026-123 취약점 분석")["reasoning_effort"], "high")
        self.assertEqual(router.select_model("SecuMS CVE 취약점 분석")["model"], "gpt-6.1-sol")

    def test_high_risk_reverse_uses_astra(self):
        self.assertEqual(router.select_model("바이너리 역공학", risk="high")["model"], "gpt-6-astra")

    def test_critical_coding_uses_astra(self):
        self.assertEqual(router.select_model("인증 로직 구현", risk="critical")["model"], "gpt-6-astra")

    def test_unverified_failures_never_escalate(self):
        self.assertEqual(router.select_model("신규 기능 개발", failed_runs=4, failure_reason="environment")["model"], "gpt-6.1-sol")
        self.assertEqual(router.select_model("신규 기능 개발", failed_runs=4)["model"], "gpt-6.1-sol")

    def test_reasoning_failure_escalates(self):
        self.assertEqual(router.select_model("신규 기능 개발", failed_runs=2, failure_reason="reasoning")["model"], "gpt-6-astra")

    def test_big_change_escalates_to_sol_high(self):
        r = router.select_model("코드 패치", risk="low", files=20)
        self.assertEqual((r["model"], r["reasoning_effort"]), ("gpt-6.1-sol", "high"))

    def test_histories_need_verified_reasoning_failures(self):
        evidence = [{"kind": "coding", "model": "gpt-6.1-sol", "verification": "failed", "failure_reason": "reasoning"} for _ in range(3)]
        evidence += [{"kind": "coding", "model": "gpt-6.1-sol", "verification": "passed", "failure_reason": "none"} for _ in range(5)]
        self.assertEqual(router.select_model("기능 개발", history=evidence)["model"], "gpt-6-astra")
        evidence[0]["verification"] = "unverified"
        self.assertEqual(router.select_model("기능 개발", history=evidence)["model"], "gpt-6.1-sol")
        self.assertEqual(router.select_model("기능 개발", history=[*evidence, evidence[1]], risk="high")["model"], "gpt-6.1-sol")

    def test_no_user_prompt_retained_and_input_validation(self):
        with self.assertRaises(ValueError):
            router.select_model(" ")
        with self.assertRaises(ValueError):
            router.select_model("code", files=-1)
        with self.assertRaises(ValueError):
            router.select_model("code", risk="zero")


class AccountingTests(unittest.TestCase):
    def test_usage_and_cached_api_equivalent(self):
        usage = router.extract_usage({"type": "turn.completed", "usage": {"input_tokens": 1000, "cached_input_tokens": 700, "output_tokens": 200}})
        self.assertEqual(usage, {"input_tokens": 1000, "cached_input_tokens": 700, "output_tokens": 200})
        self.assertAlmostEqual(router.api_equivalent_usd("gpt-6.1-sol", usage), (300 * 2 + 700 * .1 + 200 * 10) / 1e6)

    def test_invalid_usage_and_non_turn_are_ignored(self):
        self.assertIsNone(router.extract_usage({"type": "turn.completed", "usage": {"input_tokens": 5, "output_tokens": 2, "cached_input_tokens": 6}}))
        self.assertIsNone(router.extract_usage({"type": "turn.completed", "usage": {"input_tokens": True, "output_tokens": 2}}))
        self.assertIsNone(router.extract_usage({"type": "item.completed", "usage": {"input_tokens": 3, "output_tokens": 2}}))
        self.assertIsNone(router.api_equivalent_usd("gpt-6-astra", {}))

    def test_aggregates_only_verified_success(self):
        rows = [{"model": "gpt-6.1-sol", "verification": "unverified", "usage": None},
                {"model": "gpt-6.1-sol", "verification": "passed", "usage": {"input_tokens": 10, "output_tokens": 8}, "api_equivalent_usd": 0.001},
                {"model": "gpt-6.1-sol", "verification": "failed", "usage": {"input_tokens": 10, "output_tokens": 7}, "api_equivalent_usd": 0.001}]
        stats = router.aggregate(rows)["gpt-6.1-sol"]
        self.assertEqual(stats["verified_success_rate"], .5)
        self.assertEqual(stats["verified_runs"], 2)
        self.assertEqual(stats["runs"], 3)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.metrics = self.base / "usage.jsonl"

    def cli(self, *args):
        return subprocess.run([sys.executable, str(MOD), "--metrics-file", str(self.metrics), *args],
                              capture_output=True, text=True)

    def test_plan_and_dry_run_no_metrics(self):
        result = self.cli("plan", "비정상 패키지 업데이트 실패 원인 분석")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["model"], "gpt-6.1-sol")
        result = self.cli("run", "정책 요약", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gpt-6-luna", result.stdout)
        self.assertFalse(self.metrics.exists())

    @unittest.skipIf(os.name == "nt", "POSIX test stub requires a shebang; Windows covered by pure routing tests")
    def test_fake_codex_captures_aggregate_usage_no_prompt(self):
        fake = self.base / "fake_codex.py"
        fake.write_text(f'''#!{sys.executable}\nimport json, sys\nassert sys.argv[1:5] == ["exec", "--json", "-m", "gpt-6.1-sol"]\nprint(json.dumps({{"type":"turn.completed", "usage": {{"input_tokens": 100, "output_tokens": 20, "cached_input_tokens": 50}}}}))\nprint(json.dumps({{"type":"item.completed", "item":{{"type":"agent_message", "text":"완료"}}}}))\nprint(json.dumps({{"type":"turn.completed", "usage": {{"input_tokens": 60, "output_tokens": 10, "cached_input_tokens": 10}}}}))\n''')
        fake.chmod(0o700)
        secret = "신규 기능 개발 - SECRET-PROMPT-DO-NOT-LOG"
        result = self.cli("run", secret, "--codex-bin", str(fake))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("완료", result.stdout)
        data = self.metrics.read_text()
        self.assertNotIn(secret, data)
        self.assertNotIn("SECRET", data)
        rows, bad = router.parse_metrics(self.metrics)
        self.assertEqual(bad, 0)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["usage"], {"input_tokens": 160, "output_tokens": 30, "cached_input_tokens": 60})
        self.assertEqual(rows[0]["verification"], "unverified")
        rid = rows[0]["run_id"]
        self.assertNotEqual(self.cli("record", rid, "--verification", "failed", "--failure-reason", "none").returncode, 0)
        self.assertEqual(self.cli("record", rid, "--verification", "passed").returncode, 0)
        rows, bad = router.parse_metrics(self.metrics)
        self.assertEqual(rows[0]["verification"], "passed")
        report = self.cli("report")
        self.assertEqual(json.loads(report.stdout)["models"]["gpt-6.1-sol"]["verified_success_rate"], 1)

    @unittest.skipIf(os.name == "nt", "POSIX test stub requires a shebang; Windows covered by pure routing tests")
    def test_failed_process_is_not_verified_failure(self):
        fake = self.base / "failure.py"
        fake.write_text(f'#!{sys.executable}\nimport sys\nprint("not-json")\nsys.exit(7)\n')
        fake.chmod(0o700)
        result = self.cli("run", "장애 분석", "--codex-bin", str(fake))
        self.assertEqual(result.returncode, 7)
        rows, _ = router.parse_metrics(self.metrics)
        self.assertEqual(rows[0]["verification"], "unverified")
        self.assertIsNone(rows[0]["usage"])

    def test_unknown_run_rejected_and_invalid_log_does_not_affect_decision(self):
        self.assertNotEqual(self.cli("record", "missing", "--verification", "passed").returncode, 0)
        self.metrics.write_text('oops\n')
        self.assertIn("adaptive routing disabled", self.cli("plan", "신규 기능 개발").stderr)


if __name__ == "__main__":
    unittest.main()

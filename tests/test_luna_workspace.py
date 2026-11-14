"""Global Luna must not mutate project instructions or leak prompt text to usage logs."""
import argparse
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import luna_workspace as workspace


class CaptureInput(io.StringIO):
    def close(self):
        self.captured = self.getvalue()
        super().close()


class FakeProcess:
    def __init__(self, events, code=0):
        self.stdin = CaptureInput()
        self.stdout = io.StringIO("\n".join(json.dumps(x, ensure_ascii=False) for x in events) + "\n")
        self.code = code

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def wait(self):
        return self.code


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.home = base / "codexhome"
        self.metrics = self.home / "luna" / "usage.jsonl"
        self.project1 = base / "project1"
        self.project2 = base / "project2"
        for project in (self.project1, self.project2):
            project.mkdir()
            (project / "AGENTS.md").write_text("PROJECT-SPECIFIC-RULES\n", encoding="utf-8")
            (project / ".codex").mkdir()
            (project / ".codex" / "config.toml").write_text('sandbox_mode = "read-only"\n')
        self.opts = argparse.Namespace(kind=None, risk="auto", files=0, failed_runs=0,
                                       failure_reason="unknown", no_adaptive=False,
                                       codex_bin="codex", plan=False, dry_run=False)
        self.calls = []
        self.processes = []
        self.events = []
        self.return_code = 0

    def fake_popen(self, command, cwd=None, **kwargs):
        self.calls.append((command, cwd, kwargs))
        process = FakeProcess(self.events, self.return_code)
        self.processes.append(process)
        return process

    def call(self, prompt, project=None):
        with patch.object(workspace.subprocess, "Popen", side_effect=self.fake_popen), \
             patch.object(workspace.shutil, "which", return_value="/fake/codex"):
            return workspace.run_turn(prompt, project or self.project1, self.home, self.metrics, self.opts)

    def events_for(self, tid, n=10):
        return [{"type": "thread.started", "thread_id": tid},
                {"type": "item.completed", "item": {"type": "agent_message", "text": "완료"}},
                {"type": "turn.completed", "usage": {"input_tokens": n, "cached_input_tokens": 2, "output_tokens": 4}}]

    def test_project_isolation_resume_and_model_switch_without_editing_rules(self):
        self.events = self.events_for("0199aaaa-bbbb-cccc-1111-222222222222")
        self.assertEqual(self.call("신규 기능 개발 PRIVATE-TEXT"), 0)
        self.assertEqual(self.calls[0][0][1:5], ["exec", "--json", "-m", "gpt-6.1-sol"])
        self.assertEqual(self.calls[0][1], self.project1)
        self.opts.risk = "high"
        self.events = self.events_for("0199aaaa-bbbb-cccc-1111-222222222222", 20)
        self.assertEqual(self.call("아키텍처 재설계 해줘"), 0)
        self.assertEqual(self.calls[1][0][1:5], ["exec", "--json", "-m", "gpt-6-astra"])
        self.assertIn("resume", self.calls[1][0])
        self.assertIn("0199aaaa-bbbb-cccc-1111-222222222222", self.calls[1][0])
        self.opts.risk = "auto"
        self.events = self.events_for("0199dddd-eeee-ffff-3333-444444444444", 30)
        self.assertEqual(self.call("이 문서 요약", self.project2), 0)
        self.assertNotIn("resume", self.calls[2][0])
        self.assertEqual(self.calls[2][0][3:5], ["-m", "gpt-6-luna"])
        self.assertEqual(len(workspace.routing.parse_metrics(self.metrics)[0]), 3)
        self.assertNotIn("PRIVATE-TEXT", self.metrics.read_text(encoding="utf-8"))
        for project in (self.project1, self.project2):
            self.assertEqual((project / "AGENTS.md").read_text(), "PROJECT-SPECIFIC-RULES\n")
            self.assertEqual((project / ".codex" / "config.toml").read_text(), 'sandbox_mode = "read-only"\n')

    def test_plan_no_codex_or_persistent_metrics(self):
        self.opts.plan = True
        result = self.call("로그 분석")
        self.assertEqual(result, 0)
        self.assertFalse(self.metrics.exists())
        self.assertEqual(self.calls, [])

    def test_error_unverified_and_unexpected_thread_does_not_lose_pointer(self):
        self.events = self.events_for("thread-old-001")
        self.assertEqual(self.call("신규 기능 개발"), 0)
        self.events = self.events_for("thread-unexpected-999")
        self.return_code = 7
        self.assertEqual(self.call("계속 개발해 줘"), 7)
        session = workspace.read_session(workspace.session_path(self.home, self.project1))
        self.assertEqual(session["thread_id"], "thread-old-001")
        rows, bad = workspace.routing.parse_metrics(self.metrics)
        self.assertEqual(bad, 0)
        self.assertEqual(rows[-1]["verification"], "unverified")
        self.assertEqual(rows[-1]["exit_code"], 7)

    def test_concurrent_project_session_lock_prevents_conflicting_turns(self):
        path = workspace.session_path(self.home, self.project1)
        with workspace.session_lock(path):
            with self.assertRaisesRegex(RuntimeError, "another Luna run"):
                self.call("신규 기능 개발")
        self.assertFalse(path.with_suffix(".lock").exists())

    def test_no_session_id_cannot_borrow_unrelated_codex_thread(self):
        self.events = [{"type": "turn.completed", "usage": {"input_tokens": 10,
                                                           "output_tokens": 2, "cached_input_tokens": 0}}]
        self.assertEqual(self.call("신규 기능 개발"), 0)
        self.assertFalse(workspace.session_path(self.home, self.project1).exists())
        self.assertNotIn("resume", self.calls[0][0])

    def test_project_root_from_nested_git_path(self):
        if not __import__("shutil").which("git"):
            self.skipTest("Git not present")
        subprocess.run(["git", "init", "-q", str(self.project1)], check=True)
        child = self.project1 / "src"
        child.mkdir()
        self.assertTrue(os.path.samefile(workspace.project_root(child), self.project1))

    def test_global_history_is_shared_between_projects(self):
        self.events = self.events_for("thread-share-1")
        self.call("신규 기능 개발", self.project1)
        self.events = self.events_for("thread-share-2")
        self.call("신규 기능 개발", self.project2)
        rows, _ = workspace.routing.parse_metrics(self.metrics)
        self.assertEqual(len(rows), 2)
        self.assertNotEqual(rows[0]["project_id"], rows[1]["project_id"])
        self.assertEqual({row["model"] for row in rows}, {"gpt-6.1-sol"})

    def test_reset_only_luna_pointer(self):
        self.events = self.events_for("thread-reset-001")
        self.assertEqual(self.call("신규 기능 개발"), 0)
        path = workspace.session_path(self.home, self.project1)
        self.assertTrue(path.exists())
        workspace.reset_session(path)
        self.assertFalse(path.exists())
        self.assertTrue(self.metrics.exists())
        self.assertTrue((self.project1 / "AGENTS.md").exists())

    def test_shell_arguments_not_evaluated(self):
        task = '신규 기능 개발; echo BAD && $(rm -rf /)'
        self.events = self.events_for("thread-safe-123")
        self.assertEqual(self.call(task), 0)
        self.assertEqual(self.calls[0][0][-1], "-")
        self.assertNotIn(task, self.calls[0][0])
        self.assertEqual(self.processes[0].stdin.captured, task)
        self.assertEqual(self.calls[0][2]["stdin"], subprocess.PIPE)
        self.assertNotIn("shell", self.calls[0][2])


if __name__ == "__main__":
    unittest.main()

"""Behavioral checks for doctor inventory and evidence labels."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/doctor/scripts/health.py"
spec = importlib.util.spec_from_file_location("health", SCRIPT)
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class DoctorTests(unittest.TestCase):
    def test_valid_skill_and_missing_reference_are_distinguished(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / ".agents/skills/sample/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: sample\ndescription: A valid skill.\n---\n\nUse it.\n")
            (root / "AGENTS.md").write_text("Read `docs/MISSING.md`.\n")
            report = health.audit(root, deep=True)
            self.assertFalse(any(f["kind"] == "missing-metadata" for f in report["findings"]))
            self.assertIn({"kind": "missing-reference", "path": "AGENTS.md",
                           "target": "docs/MISSING.md"}, report["findings"])
            self.assertTrue(report["runtime_plugins_mcp"].startswith("not observed"))

    def test_exact_overlap_requires_two_distinct_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paragraph = "The same detailed operating rule is repeated across two instruction surfaces. " * 3
            (root / "AGENTS.md").write_text(paragraph)
            protocol = root / "docs/CORE_ENGINEERING_PROTOCOL_V2.md"
            protocol.parent.mkdir()
            protocol.write_text(paragraph)
            report = health.audit(root, deep=True)
            overlaps = [f for f in report["findings"] if f["kind"] == "exact-overlap"]
            self.assertEqual(len(overlaps), 1)
            self.assertEqual(overlaps[0]["paths"], ["AGENTS.md", protocol.relative_to(root).as_posix()])


if __name__ == "__main__":
    unittest.main()

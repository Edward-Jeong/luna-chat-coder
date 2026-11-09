"""Static integration-contract checks for the optional Socratic Tutor skill.

These tests intentionally do NOT claim to validate model behavior. See the
manual agent prompt cases in the skill's references directory.
"""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/luna-socratic-tutor/SKILL.md"
LICENSE = ROOT / ".agents/skills/luna-socratic-tutor/LICENSE.upstream.md"
CASES = ROOT / ".agents/skills/luna-socratic-tutor/references/evaluation-cases.md"


class SocraticTutorIntegrationTests(unittest.TestCase):
    def test_skill_is_discoverable_and_metadata_is_valid(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        header = content.split("---\n", 2)[1]
        self.assertIn("name: luna-socratic-tutor", header)
        self.assertIn("description:", header)
        self.assertIn("license: MIT", header)
        entry = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(".agents/skills/luna-socratic-tutor/SKILL.md", entry)

    def test_optional_activation_and_existing_router_are_explicit(self):
        content = SKILL.read_text(encoding="utf-8")
        for contract in [
            "explicit opt-in only",
            "Do not activate",
            "Coding / Security / Incident",
            "not a new Router lead team",
            "ONE question at a time",
            "3–5 diagnostic questions",
            "two or more independent checks",
            "unprompted recall",
            "save state",
            "not a validated exam score",
        ]:
            with self.subTest(contract=contract):
                self.assertIn(contract, content)

    def test_license_and_manual_behavior_cases_are_present(self):
        self.assertIn("Jane Street Group", LICENSE.read_text(encoding="utf-8"))
        text = CASES.read_text(encoding="utf-8")
        for phrase in [
            "SQL injection이 뭔지 설명해줘",
            "Teach me PostgreSQL",
            "Debug this production",
            "Review this PR",
            "grill my requirements",
            "save state",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_user_guide_has_explicit_usage_and_boundaries(self):
        guide = (ROOT / "docs/USAGE.ko.md").read_text(encoding="utf-8")
        self.assertIn("Socratic Tutor", guide)
        self.assertIn("학습시켜 줘", guide)
        self.assertIn("일반 개발·장애·보안", guide)
        self.assertIn("자동 저장", guide)


if __name__ == "__main__":
    unittest.main()

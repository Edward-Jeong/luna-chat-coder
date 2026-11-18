"""Verify a reversible user-scoped Codex skill install without host writes."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import install_codex_shared_skills as installer


class SharedSkillInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.agents_home = self.work / ".agents"
        self.source = self.work / "source"
        self.source_skill = self.source / "integrations/codex/skills/prune-tests"
        self.source_skill.mkdir(parents=True)
        for name in installer.OWNED_FILES:
            (self.source_skill / name).write_bytes((ROOT / "integrations/codex/skills/prune-tests" / name).read_bytes())

    @property
    def dest(self):
        return self.agents_home / "skills/prune-tests"

    def run_install(self, **kwargs):
        return installer.install(self.source, self.agents_home, **kwargs)

    def test_install_is_user_scoped_idempotent_and_reversible(self):
        project = self.work / "product"
        project.mkdir()
        (project / "AGENTS.md").write_text("SECURITY RULES", encoding="utf-8")
        self.assertEqual(self.run_install()["changed_files"], 2)
        self.assertEqual(self.run_install()["changed_files"], 0)
        for name in installer.OWNED_FILES:
            self.assertEqual((self.dest / name).read_bytes(), (self.source_skill / name).read_bytes())
        self.assertEqual((project / "AGENTS.md").read_text(), "SECURITY RULES")
        self.assertEqual(self.run_install(uninstall=True)["action"], "uninstall")
        self.assertFalse(self.dest.exists())
        self.assertEqual((project / "AGENTS.md").read_text(), "SECURITY RULES")

    def test_dry_run_never_writes(self):
        result = self.run_install(dry_run=True)
        self.assertEqual(result["changed_files"], 2)
        self.assertFalse(self.agents_home.exists())

    def test_unmanaged_skill_refused_without_partial_write(self):
        self.dest.mkdir(parents=True)
        original = self.dest / "SKILL.md"
        original.write_text("CUSTOM")
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            self.run_install()
        self.assertEqual(original.read_text(), "CUSTOM")
        self.assertFalse((self.agents_home / "luna").exists())

    def test_changed_managed_file_prevents_upgrade_and_uninstall(self):
        self.run_install()
        (self.dest / "SKILL.md").write_text("CUSTOM")
        (self.source_skill / "LICENSE.upstream.md").write_text("NEW LICENSE")
        with self.assertRaisesRegex(ValueError, "modified"):
            self.run_install()
        with self.assertRaisesRegex(ValueError, "modified"):
            self.run_install(uninstall=True)
        self.assertEqual((self.dest / "SKILL.md").read_text(), "CUSTOM")
        self.assertNotEqual((self.dest / "LICENSE.upstream.md").read_text(), "NEW LICENSE")

    def test_safe_update_and_unrelated_file_preserved(self):
        self.run_install()
        extra = self.dest / "user-notes.txt"
        extra.write_text("LEAVE ALONE")
        (self.source_skill / "SKILL.md").write_text("UPDATED")
        self.assertEqual(self.run_install()["changed_files"], 1)
        self.assertEqual((self.dest / "SKILL.md").read_text(), "UPDATED")
        self.run_install(uninstall=True)
        self.assertEqual(extra.read_text(), "LEAVE ALONE")

    def test_corrupted_manifest_refused(self):
        self.run_install()
        manifest = self.agents_home / "luna/prune-tests-install.json"
        record = json.loads(manifest.read_text())
        record["files"]["../../AGENTS.md"] = "0" * 64
        manifest.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "invalid"):
            self.run_install()
        self.assertTrue((self.dest / "SKILL.md").exists())

    def test_symlinked_skill_directory_refused(self):
        outside = self.work / "outside"
        outside.mkdir()
        self.dest.parent.mkdir(parents=True)
        try:
            self.dest.symlink_to(outside, target_is_directory=True)
        except (NotImplementedError, OSError):
            self.skipTest("symlink creation restricted")
        with self.assertRaisesRegex(ValueError, "symlinked"):
            self.run_install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_manifest_uninstall_dry_run_preserves_files(self):
        self.run_install()
        result = self.run_install(uninstall=True, dry_run=True)
        self.assertEqual(result["action"], "uninstall")
        self.assertTrue((self.dest / "SKILL.md").exists())

    def test_skill_requires_frontmatter_and_guardrails(self):
        text = (ROOT / "integrations/codex/skills/prune-tests/SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: prune-tests\ndescription:"))
        for phrase in ("AGENTS.md", "authentication", "security regression", "independent review"):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()

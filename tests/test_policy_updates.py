import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/apply-luna-policy.py"
spec = importlib.util.spec_from_file_location("policy_updates", SCRIPT)
policy_updates = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy_updates)


class PolicyUpdateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.policy = b"# Policy\nrevision 2.1\n"

    def plan(self, global_scope=False):
        return policy_updates.plan_update(self.root, self.policy, global_scope)

    def test_preserves_project_bytes_and_is_idempotent(self):
        original = "# Existing\r\n보안 제한을 유지합니다.\r\n".encode()
        path = self.root / "AGENTS.md"
        path.write_bytes(original)
        plan = self.plan()
        self.assertEqual(path.read_bytes(), original)  # Preview does not write.
        policy_updates.apply_plan(plan)
        self.assertTrue(path.read_bytes().startswith(original))
        self.assertEqual((self.root / "AGENTS.md.luna-backup").read_bytes(), original)
        self.assertEqual(policy_updates.apply_plan(self.plan()), [])

    def test_global_active_override_keeps_default_untouched(self):
        regular, override = self.root / "AGENTS.md", self.root / "AGENTS.override.md"
        regular.write_bytes(b"base")
        override.write_bytes(b"temporary constraints")
        policy_updates.apply_plan(self.plan(True))
        self.assertEqual(regular.read_bytes(), b"base")
        self.assertTrue(override.read_bytes().startswith(b"temporary constraints"))
        self.assertIn(str(self.root).encode(), override.read_bytes())

    def test_rejects_edited_policy(self):
        policy_updates.apply_plan(self.plan())
        (self.root / "docs/luna/CORE_ENGINEERING_PROTOCOL_V2.md").write_bytes(b"custom")
        with self.assertRaisesRegex(ValueError, "Local policy edits"):
            self.plan()

    def test_rejects_unmanaged_policy(self):
        path = self.root / "docs/luna/CORE_ENGINEERING_PROTOCOL_V2.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"custom")
        with self.assertRaisesRegex(ValueError, "Unmanaged"):
            self.plan()

    def test_rejects_duplicate_or_incomplete_markers(self):
        for original in [policy_updates.BEGIN, policy_updates.block("x") * 2]:
            with self.assertRaises(ValueError):
                policy_updates.merge_guidance(original, policy_updates.block("y"))

    def test_replaces_only_managed_block(self):
        original = b"before\n" + policy_updates.block("old") + b"after\n"
        merged = policy_updates.merge_guidance(original, policy_updates.block("new"))
        self.assertEqual(merged, b"before\n" + policy_updates.block("new") + b"after\n")

    def test_rejects_symlink_parent_and_guidance(self):
        external = self.root / "external"
        external.mkdir()
        target = self.root / "target"
        target.mkdir()
        (target / "docs").symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            policy_updates.plan_update(target, self.policy)
        (target / "docs").unlink()
        (external / "guidance").write_bytes(b"outside")
        (target / "AGENTS.md").symlink_to(external / "guidance")
        with self.assertRaisesRegex(ValueError, "symlink"):
            policy_updates.plan_update(target, self.policy)

    def test_next_revision_preserves_initial_backup(self):
        # Existing backups must be archived explicitly before a differing overwrite.
        policy_updates.apply_plan(self.plan())
        self.policy = b"# next revision\n"
        policy_updates.apply_plan(self.plan())
        with self.assertRaisesRegex(ValueError, "Backup already exists"):
            self.policy = b"# third revision\n"
            policy_updates.apply_plan(self.plan())


if __name__ == "__main__":
    unittest.main()

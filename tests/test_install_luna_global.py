"""Cross-platform, reversible user-wide Luna installation contract."""
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import install_luna_global as installer


class GlobalInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "codex"
        self.source = self.root / "source"
        scripts = self.source / "scripts"
        scripts.mkdir(parents=True)
        for name in installer.RUNTIME:
            (scripts / name).write_text("# managed binary " + name, encoding="utf-8")

    def test_windows_install_does_not_touch_projects_and_uninstall_keeps_metrics(self):
        project = self.root / "existing-project"
        project.mkdir()
        (project / "AGENTS.md").write_text("keep me")
        result = installer.install(self.source, self.home, r"C:\Python\python.exe", windows=True)
        self.assertTrue((self.home / "luna" / "bin" / "luna.cmd").exists())
        self.assertEqual(result["project_files_modified"], False)
        result = installer.install(self.source, self.home, r"C:\Python\python.exe", windows=True)
        self.assertEqual(result["changed_files"], 0)
        data = self.home / "luna" / "usage.jsonl"
        data.write_text("one local record")
        result = installer.install(self.source, self.home, r"C:\Python\python.exe", windows=True, remove=True)
        self.assertTrue(result["metrics_retained"])
        self.assertEqual(data.read_text(), "one local record")
        self.assertEqual((project / "AGENTS.md").read_text(), "keep me")

    def test_posix_script_and_dry_run(self):
        result = installer.install(self.source, self.home, "/usr/bin/python3", windows=False, dry_run=True)
        self.assertFalse((self.home / "luna").exists())
        self.assertEqual(result["changed_files"], 3)
        installer.install(self.source, self.home, "/usr/bin/python3", windows=False)
        script = self.home / "luna" / "bin" / "luna"
        self.assertTrue(script.read_text().startswith("#!/bin/sh\nexec"))
        self.assertTrue(script.stat().st_mode & 0o100)

    def test_symlinked_runtime_directory_is_rejected(self):
        if not hasattr(Path, "symlink_to"):
            self.skipTest("symlinks are unsupported")
        target = self.root / "external"
        target.mkdir()
        base = self.home / "luna"
        base.mkdir(parents=True)
        try:
            (base / "runtime").symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is restricted")
        with self.assertRaisesRegex(ValueError, "symlinked"):
            installer.install(self.source, self.home, "/usr/bin/python3", windows=False)
        self.assertEqual(list(target.iterdir()), [])

    def test_unmanaged_content_is_never_overwritten(self):
        path = self.home / "luna" / "runtime" / "luna_workspace.py"
        path.parent.mkdir(parents=True)
        path.write_text("USER CUSTOMIZATIONS")
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            installer.install(self.source, self.home, "/usr/bin/python3", windows=False)
        self.assertEqual(path.read_text(), "USER CUSTOMIZATIONS")
        self.assertFalse((self.home / "luna" / "installation.json").exists())

    def test_modified_managed_file_blocks_update_without_partial_overwrite(self):
        installer.install(self.source, self.home, "/usr/bin/python3", windows=False)
        path = self.home / "luna" / "runtime" / "luna_workspace.py"
        path.write_text("USER PATCH")
        (self.source / "scripts" / "luna_model_router.py").write_text("SOURCE UPDATED")
        with self.assertRaisesRegex(ValueError, "modified"):
            installer.install(self.source, self.home, "/usr/bin/python3", windows=False)
        self.assertEqual(path.read_text(), "USER PATCH")
        self.assertNotEqual((self.home / "luna" / "runtime" / "luna_model_router.py").read_text(), "SOURCE UPDATED")


if __name__ == "__main__":
    unittest.main()

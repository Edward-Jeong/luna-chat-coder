"""Exercise installers only against disposable Codex homes."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "integrations/codex/agents"


class InstallerContract:
    command = None

    def setUp(self):
        if not self.command:
            self.skipTest("Installer runtime is unavailable")
        self.temp = tempfile.TemporaryDirectory(prefix="luna install ")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "Codex profile"
        self.env = dict(os.environ, CODEX_HOME=str(self.home))

    def install(self):
        return subprocess.run(self.command, cwd=ROOT, env=self.env,
                              capture_output=True, text=True, check=True)

    def test_installs_missing_files_and_preserves_custom_files(self):
        agents = self.home / "agents"
        agents.mkdir(parents=True)
        custom = agents / "luna-router.toml"
        original = b"# Customer modifications\r\nname = 'Custom router'\r\n"
        custom.write_bytes(original)
        self.install()
        self.assertEqual(custom.read_bytes(), original)
        for source in SOURCES.glob("*.toml"):
            if source.name != custom.name:
                self.assertEqual((agents / source.name).read_bytes(), source.read_bytes())

    def test_repeated_install_preserves_bytes_and_modification_time(self):
        self.install()
        agents = self.home / "agents"
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in agents.glob("*.toml")}
        # Distinct fixed timestamps reveal rewriting even on coarse filesystems.
        for p in agents.glob("*.toml"):
            os.utime(p, (1_000_000_000, 1_000_000_000))
        self.install()
        for p in agents.glob("*.toml"):
            self.assertEqual(p.read_bytes(), before[p.name][0])
            self.assertEqual(p.stat().st_mtime, 1_000_000_000)

    def test_preserves_unrelated_files(self):
        agents = self.home / "agents"
        agents.mkdir(parents=True)
        unrelated = agents / "customer-agent.toml"
        unrelated.write_bytes(b"custom unrelated agent")
        self.install()
        self.assertEqual(unrelated.read_bytes(), b"custom unrelated agent")


class BashInstallerTests(InstallerContract, unittest.TestCase):
    command = ([shutil.which("bash"), "scripts/install-codex-agents.sh"]
               if shutil.which("bash") else None)

    def test_preserves_dangling_symlink(self):
        agents = self.home / "agents"
        agents.mkdir(parents=True)
        outside = self.home / "absent-target"
        link = agents / "luna-router.toml"
        link.symlink_to(outside)
        self.install()
        self.assertTrue(link.is_symlink())
        self.assertFalse(outside.exists())


class PowerShellInstallerTests(InstallerContract, unittest.TestCase):
    runtime = shutil.which("pwsh") or shutil.which("powershell")
    command = ([runtime, "-NoProfile", "-File", "scripts/install-codex-agents.ps1"]
               if runtime else None)


if __name__ == "__main__":
    unittest.main()

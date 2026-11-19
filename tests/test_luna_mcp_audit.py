"""Read-only MCP package selector audit regression tests."""

import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/luna_mcp_audit.py"
spec = importlib.util.spec_from_file_location("luna_mcp_audit", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuditTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def config(self, servers):
        (self.root / ".mcp.json").write_text(json.dumps({"mcpServers": servers}), encoding="utf-8")

    def test_scoped_exact_version(self):
        self.config({"context7": {"command": "npx", "args": ["-y", "@upstash/context7-mcp@1.2.3"]}})
        self.assertEqual(module.audit(self.root)["summary"], {"pinned": 1, "mutable": 0, "review": 0})

    def test_mutable_tag_does_not_expose_input(self):
        self.config({"example": {"command": "npx", "args": ["--yes", "example@latest"]}})
        report = module.audit(self.root)
        self.assertEqual(report["summary"]["mutable"], 1)
        self.assertNotIn("example@latest", json.dumps(report))

    def test_bare_and_range_selectors(self):
        self.config({"a": {"command": "npx", "args": ["pkg"]},
                     "b": {"command": "pnpm", "args": ["dlx", "pkg@^1.0.0"]}})
        self.assertEqual(module.audit(self.root)["summary"]["mutable"], 2)

    def test_npx_package_option(self):
        self.config({"a": {"command": "npx", "args": ["-p", "pkg@1.2.3", "start"]}})
        self.assertEqual(module.audit(self.root)["summary"]["pinned"], 1)

    def test_unknown_commands_are_not_approved(self):
        self.config({"a": {"command": "node", "args": ["script.js"]},
                     "b": {"command": "npx", "args": ["--registry", "https://example.test", "pkg@1.2.3"]}})
        self.assertEqual(module.audit(self.root)["summary"]["review"], 2)

    def test_invalid_json_redacted(self):
        (self.root / ".mcp.json").write_text("SECRET_TOKEN=never-show", encoding="utf-8")
        report = module.audit(self.root)
        self.assertEqual(report["summary"]["review"], 1)
        self.assertNotIn("SECRET_TOKEN", json.dumps(report))

    def test_parent_path_is_rejected(self):
        report = module.audit(self.root, ["../secrets.json"])
        self.assertEqual(report["findings"][0]["reason"], "path-outside-root")

    def test_symlink_not_followed(self):
        target = self.root / "target.json"
        target.write_text("{}")
        link = self.root / ".mcp.json"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink unavailable")
        self.assertEqual(module.audit(self.root)["findings"][0]["reason"], "symlink-or-escape")

    def test_strict_mode_is_explicit(self):
        self.config({"a": {"command": "npx", "args": ["pkg@latest"]}})
        with redirect_stdout(StringIO()):
            self.assertEqual(module.main(["--root", str(self.root)]), 0)
            self.assertEqual(module.main(["--root", str(self.root), "--fail-on-mutable"]), 1)

    @unittest.skipUnless(module.tomllib is not None, "Python 3.11+ TOML parser")
    def test_codex_toml(self):
        config = self.root / ".codex/config.toml"
        config.parent.mkdir()
        config.write_text('[mcp_servers.sample]\ncommand = "npx"\nargs = ["-y", "pkg@1.2.3"]\n')
        self.assertEqual(module.audit(self.root)["summary"]["pinned"], 1)


if __name__ == "__main__":
    unittest.main()

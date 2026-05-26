from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "apply_harness.py"


class ApplyHarnessTests(unittest.TestCase):
    def run_installer(self, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), "--target", str(target), *args],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_dry_run_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            result = self.run_installer(target, "--dry-run")

            self.assertIn("Dry run only. No files were written.", result.stdout)
            self.assertNotIn("harness-check.yml", result.stdout)
            self.assertEqual([], list(target.rglob("*")))

    def test_default_install_excludes_optional_ci(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target)

            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "scripts" / "check_docs_drift.py").exists())
            self.assertFalse(
                (target / ".github" / "workflows" / "harness-check.yml").exists()
            )

    def test_with_ci_installs_optional_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--with-ci")

            self.assertTrue(
                (target / ".github" / "workflows" / "harness-check.yml").exists()
            )

    def test_existing_files_are_skipped_unless_force_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            agents = target / "AGENTS.md"
            agents.write_text("existing instructions\n", encoding="utf-8")

            result = self.run_installer(target)
            self.assertIn("skip-existing", result.stdout)
            self.assertEqual("existing instructions\n", agents.read_text(encoding="utf-8"))

            self.run_installer(target, "--force")
            self.assertIn("Harness profile: generic", agents.read_text(encoding="utf-8"))

    def test_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "python")

            profile_root = target / "docs" / "harness" / "profiles" / "python"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "pyproject.harness.toml").exists())
            self.assertTrue((profile_root / "pre-commit-config.harness.yaml").exists())

    def test_generated_harness_checks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.run_installer(target)

            for script in (
                target / "scripts" / "check_docs_drift.py",
                target / "scripts" / "check_structure.py",
            ):
                subprocess.run(
                    [sys.executable, str(script)],
                    cwd=target,
                    check=True,
                    capture_output=True,
                    text=True,
                )


if __name__ == "__main__":
    unittest.main()

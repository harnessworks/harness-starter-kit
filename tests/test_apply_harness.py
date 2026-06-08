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
            self.assertTrue(
                (target / "scripts" / "check_effectiveness_plan.py").exists()
            )
            self.assertTrue((target / "scripts" / "check_failure_memory.py").exists())
            self.assertTrue((target / "scripts" / "check_decision_memory.py").exists())
            self.assertTrue(
                (target / ".harness" / "decision-memory-rules.json").exists()
            )
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

    def test_nextjs_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "nextjs")

            profile_root = target / "docs" / "harness" / "profiles" / "nextjs"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "package-scripts.harness.json").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_django_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "django")

            profile_root = target / "docs" / "harness" / "profiles" / "django"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_flask_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "flask")

            profile_root = target / "docs" / "harness" / "profiles" / "flask"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_spring_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "spring")

            profile_root = target / "docs" / "harness" / "profiles" / "spring"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_android_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "android")

            profile_root = target / "docs" / "harness" / "profiles" / "android"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_rust_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "rust")

            profile_root = target / "docs" / "harness" / "profiles" / "rust"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_generated_harness_checks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target)

            result = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_structure.py")],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode)
            result2 = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_docs_drift.py")],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result2.returncode)
            result3 = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_effectiveness_plan.py")],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result3.returncode)
            result4 = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_encoding_hygiene.py")],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result4.returncode)
            result5 = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_failure_memory.py")],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result5.returncode)
            result6 = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_decision_memory.py")],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result6.returncode)

    def test_fastapi_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "fastapi")

            profile_root = target / "docs" / "harness" / "profiles" / "fastapi"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "gitignore.harness.txt").exists())

    def test_react_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "react")

            profile_root = target / "docs" / "harness" / "profiles" / "react"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "eslint.config.harness.mjs").exists())
            self.assertTrue((profile_root / "package-scripts.harness.json").exists())

    def test_vue_profile_snippets_are_written_under_docs_harness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)

            self.run_installer(target, "--profile", "vue")

            profile_root = target / "docs" / "harness" / "profiles" / "vue"
            self.assertTrue((profile_root / "README.md").exists())
            self.assertTrue((profile_root / "check_harness.py").exists())
            self.assertTrue((profile_root / "eslint.config.harness.mjs").exists())
            self.assertTrue((profile_root / "package-scripts.harness.json").exists())


if __name__ == "__main__":
    unittest.main()

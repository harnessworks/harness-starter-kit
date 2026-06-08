from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures"
INSTALLER = REPO_ROOT / "scripts" / "apply_harness.py"


class FixtureSmokeTests(unittest.TestCase):
    scenarios = {
        "node-basic": (
            "typescript",
            (
                "check_harness.py",
                "eslint.config.harness.mjs",
                "package-scripts.harness.json",
            ),
        ),
        "nextjs-basic": (
            "nextjs",
            ("gitignore.harness.txt", "package-scripts.harness.json"),
        ),
        "django-basic": ("django", ("check_harness.py", "gitignore.harness.txt")),
        "fastapi-basic": ("fastapi", ("check_harness.py", "gitignore.harness.txt")),
        "flask-basic": ("flask", ("check_harness.py", "gitignore.harness.txt")),
        "react-basic": (
            "react",
            (
                "check_harness.py",
                "eslint.config.harness.mjs",
                "package-scripts.harness.json",
            ),
        ),
        "go-basic": ("go", ("check_harness.py", "gitignore.harness.txt")),
        "rust-basic": ("rust", ("check_harness.py", "gitignore.harness.txt")),
        "spring-basic": ("spring", ("check_harness.py", "gitignore.harness.txt")),
        "android-basic": ("android", ("check_harness.py", "gitignore.harness.txt")),
        "vue-basic": (
            "vue",
            (
                "check_harness.py",
                "eslint.config.harness.mjs",
                "package-scripts.harness.json",
            ),
        ),
    }

    def run_installer(self, target: Path, profile: str) -> None:
        subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                "--target",
                str(target),
                "--profile",
                profile,
            ],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def run_generated_check(self, target: Path, script_name: str) -> None:
        subprocess.run(
            [sys.executable, str(target / "scripts" / script_name)],
            cwd=target,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_fixture_adoption_installs_runnable_harness_checks(self) -> None:
        for fixture_name, (profile, expected_profile_files) in self.scenarios.items():
            with self.subTest(fixture=fixture_name, profile=profile):
                with tempfile.TemporaryDirectory() as tmp:
                    target = Path(tmp)
                    shutil.copytree(FIXTURE_ROOT / fixture_name, target, dirs_exist_ok=True)

                    self.run_installer(target, profile)

                    self.assertTrue((target / "AGENTS.md").exists())
                    self.assertTrue((target / "docs" / "decisions").is_dir())
                    self.assertTrue((target / "docs" / "failures").is_dir())
                    self.assertTrue(
                        (target / "scripts" / "check_decision_memory.py").exists()
                    )
                    self.assertTrue(
                        (target / "scripts" / "check_failure_memory.py").exists()
                    )
                    self.assertTrue(
                        (target / ".harness" / "decision-memory-rules.json").exists()
                    )
                    self.assertFalse(
                        (target / ".github" / "workflows" / "harness-check.yml").exists()
                    )

                    profile_root = target / "docs" / "harness" / "profiles" / profile
                    for filename in expected_profile_files:
                        self.assertTrue((profile_root / filename).exists())

                    self.run_generated_check(target, "check_docs_drift.py")
                    self.run_generated_check(target, "check_structure.py")
                    self.run_generated_check(target, "check_effectiveness_plan.py")
                    self.run_generated_check(target, "check_failure_memory.py")
                    self.run_generated_check(target, "check_decision_memory.py")

    @unittest.skipUnless(
        shutil.which("cargo"), "cargo not installed; skipping Rust Cargo path check"
    )
    def test_rust_profile_check_harness_runs_cargo_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            shutil.copytree(
                FIXTURE_ROOT / "rust-basic", target, dirs_exist_ok=True
            )

            self.run_installer(target, "rust")

            check_harness = (
                target / "docs" / "harness" / "profiles" / "rust" / "check_harness.py"
            )
            self.assertTrue(check_harness.exists())

            result = subprocess.run(
                [sys.executable, str(check_harness)],
                cwd=target,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                0,
                result.returncode,
                msg=f"rust check_harness.py failed:\n{result.stdout}\n{result.stderr}",
            )


if __name__ == "__main__":
    unittest.main()

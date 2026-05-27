from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTOR = REPO_ROOT / "scripts" / "harness_doctor.py"


class HarnessDoctorTests(unittest.TestCase):
    def run_doctor(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(DOCTOR), "--target", str(target)],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_reports_score_without_modifying_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text(
                "# Example\n\n## Quick Start\n\nRun `python -m unittest`.\n",
                encoding="utf-8",
            )
            before = sorted(path.relative_to(target) for path in target.rglob("*"))

            result = self.run_doctor(target)

            after = sorted(path.relative_to(target) for path in target.rglob("*"))
            self.assertEqual(before, after)
            self.assertIn("Harness Doctor Report", result.stdout)
            self.assertIn("Score:", result.stdout)
            self.assertIn("Missing Or Weak Baseline Items:", result.stdout)

    def test_scores_repository_harness_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "docs" / "decisions").mkdir(parents=True)
            (target / "docs" / "failures").mkdir(parents=True)
            (target / "docs" / "conventions").mkdir(parents=True)
            (target / "docs" / "domain").mkdir(parents=True)
            (target / "scripts").mkdir()
            (target / ".github" / "workflows").mkdir(parents=True)
            (target / "README.md").write_text(
                "# Example Harness\n\n## Quick Start\n\nThis harness helps AI coding agents.\n",
                encoding="utf-8",
            )
            (target / "AGENTS.md").write_text(
                "\n".join(
                    [
                        "# Agent Instructions",
                        "Project overview: example service.",
                        "Run `python -m unittest discover -s tests`.",
                        "Architecture boundary: do not import routes from data.",
                        "Forbidden: never commit secrets.",
                        "Security: keep credentials out of git.",
                    ]
                ),
                encoding="utf-8",
            )
            (target / "docs" / "decisions" / "001-real.md").write_text(
                "# Use the existing service layer\n",
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "001-real.md").write_text(
                "# Repeated migration mistake\n",
                encoding="utf-8",
            )
            (target / "docs" / "conventions" / "coding.md").write_text(
                "# Coding conventions\n",
                encoding="utf-8",
            )
            (target / "docs" / "domain" / "glossary.md").write_text(
                "# Glossary\n",
                encoding="utf-8",
            )
            (target / "scripts" / "check_structure.py").write_text(
                "forbidden_patterns = []\n",
                encoding="utf-8",
            )
            (target / "scripts" / "check_docs_drift.py").write_text(
                "# docs drift\n",
                encoding="utf-8",
            )
            (target / ".github" / "workflows" / "ci.yml").write_text(
                "name: CI\njobs:\n  check:\n    steps:\n      - run: python scripts/check_structure.py\n",
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("Agent Instructions: 20/20", result.stdout)
            self.assertIn("Durable Memory: 20/20", result.stdout)
            self.assertIn("Structural Safety:", result.stdout)

    def test_failure_readme_does_not_count_as_real_failure_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "docs" / "decisions").mkdir(parents=True)
            (target / "docs" / "failures").mkdir(parents=True)
            (target / "docs" / "conventions").mkdir(parents=True)
            (target / "docs" / "domain").mkdir(parents=True)
            (target / "README.md").write_text(
                "# Example\n\n## Quick Start\n\nRun `python -m unittest`.\n",
                encoding="utf-8",
            )
            (target / "docs" / "decisions" / "000-template.md").write_text(
                "# 000. Decision Title\n\nTODO\n",
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "README.md").write_text(
                "# Failure Memory\n\nEntry point for future failure notes.\n",
                encoding="utf-8",
            )
            (target / "docs" / "conventions" / "coding.md").write_text(
                "# Coding conventions\n",
                encoding="utf-8",
            )
            (target / "docs" / "domain" / "glossary.md").write_text(
                "# Glossary\n",
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("Durable Memory: 17/20", result.stdout)
            self.assertIn(
                "Durable Memory: At least one real decision or failure record exists",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()

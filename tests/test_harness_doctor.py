from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTOR = REPO_ROOT / "scripts" / "harness_doctor.py"


class HarnessDoctorTests(unittest.TestCase):
    def run_doctor(
        self,
        target: Path,
        *extra_args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(DOCTOR), "--target", str(target), *extra_args],
            cwd=REPO_ROOT,
            check=check,
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
            self.assertIn("Element Breakdown:", result.stdout)
            self.assertIn("Coupling Findings:", result.stdout)
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
                "\n".join(
                    [
                        "# Use the existing service layer",
                        "",
                        "## Context",
                        "",
                        "Routes need a stable boundary.",
                        "",
                        "## Decision",
                        "",
                        "Keep business behavior in the service layer.",
                    ]
                ),
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "001-real.md").write_text(
                "\n".join(
                    [
                        "# Repeated migration mistake",
                        "",
                        "## Why It Failed",
                        "",
                        "Agents edited generated migrations directly.",
                        "",
                        "## Current Replacement",
                        "",
                        "Regenerate migrations from model changes.",
                        "",
                        "## Agent Guidance",
                        "",
                        "Do not rewrite committed migrations without approval.",
                        "",
                        "## Detection Or Prevention Check",
                        "",
                        "`python scripts/check_structure.py` and manual review catch direct generated migration edits.",
                    ]
                ),
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

            self.assertIn("Element Breakdown:", result.stdout)
            self.assertIn("Instructions:", result.stdout)
            self.assertIn("Constraints:", result.stdout)
            self.assertIn("Feedback:", result.stdout)
            self.assertIn("Memory:", result.stdout)
            self.assertIn("Evaluation:", result.stdout)
            self.assertIn("Governance:", result.stdout)
            self.assertIn("Coupling Findings:", result.stdout)

    def test_title_only_records_do_not_count_as_real_memory(self) -> None:
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
            (target / "docs" / "decisions" / "001-thin.md").write_text(
                "# Use services\n",
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "001-thin.md").write_text(
                "# Migration mistake\n",
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

            self.assertIn("Memory:", result.stdout)
            self.assertNotIn("non-template decision or failure records found", result.stdout)

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

            self.assertIn("Memory:", result.stdout)
            self.assertNotIn("non-template decision or failure records found", result.stdout)

    def test_reports_critical_coupling_for_failure_without_detection_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "docs" / "failures").mkdir(parents=True)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            (target / "AGENTS.md").write_text(
                "Read docs/failures before fixing repeated mistakes.\n",
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "001-real.md").write_text(
                "\n".join(
                    [
                        "# Repeated issue",
                        "",
                        "## Why It Failed",
                        "",
                        "The same issue recurred.",
                        "",
                        "## Current Replacement",
                        "",
                        "Use the stable path.",
                        "",
                        "## Agent Guidance",
                        "",
                        "Do not repeat the old path.",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("critical Unoperationalized Memory", result.stdout)
            self.assertIn("Detection Or Prevention Check", result.stdout)

    def test_critical_coupling_gate_is_default_off_and_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / ".github" / "workflows").mkdir(parents=True)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            (target / ".github" / "workflows" / "ci.yml").write_text(
                "name: CI\njobs:\n  check:\n    steps:\n      - run: python scripts/check_missing.py\n",
                encoding="utf-8",
            )

            default_result = self.run_doctor(target)
            gated_result = self.run_doctor(
                target,
                "--fail-on",
                "critical-coupling",
                check=False,
            )

            self.assertEqual(0, default_result.returncode)
            self.assertNotEqual(0, gated_result.returncode)
            self.assertIn("critical Orphan Feedback", gated_result.stdout)
            self.assertIn("Gate failed: critical coupling findings are present.", gated_result.stdout)

    def test_min_score_gate_is_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")

            result = self.run_doctor(target, "--min-score", "100", check=False)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("Gate failed: score", result.stdout)

    def test_non_comparable_task_outcome_does_not_prove_or_suppress_memory_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "docs" / "failures").mkdir(parents=True)
            (target / "docs" / "examples" / "task-outcomes").mkdir(parents=True)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            (target / "AGENTS.md").write_text(
                "Read docs/failures before fixing repeated mistakes.\n",
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "001-real.md").write_text(
                "\n".join(
                    [
                        "# Repeated issue",
                        "",
                        "## Why It Failed",
                        "",
                        "The same issue recurred.",
                        "",
                        "## Current Replacement",
                        "",
                        "Use the stable path.",
                        "",
                        "## Agent Guidance",
                        "",
                        "Do not repeat the old path.",
                        "",
                        "## Detection Or Prevention Check",
                        "",
                        "Manual review checks for recurrence.",
                    ]
                ),
                encoding="utf-8",
            )
            (target / "docs" / "examples" / "task-outcomes" / "001-maint.yaml").write_text(
                "\n".join(
                    [
                        "schema_version: 1",
                        "follow_up:",
                        "  include_in_effectiveness_report: false",
                        "  include_in_comparable_product_task_count: false",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("warning Unevaluated Memory", result.stdout)
            self.assertIn("Proven unmeasured", result.stdout)
            self.assertNotIn("Proven evidence present", result.stdout)

    def test_generic_docs_mention_does_not_bind_check_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "scripts").mkdir()
            (target / "docs" / "scoring").mkdir(parents=True)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            (target / "scripts" / "check_structure.py").write_text(
                "forbidden_patterns = []\n",
                encoding="utf-8",
            )
            (target / "docs" / "scoring" / "rubric.md").write_text(
                "Mention scripts/check_structure.py only as a generic example.\n",
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("warning Orphan Constraint", result.stdout)
            self.assertIn("scripts/check_structure.py exists", result.stdout)
            self.assertNotIn(
                "Feedback/Exists: local validation script, package check, pre-commit, or task-runner command found",
                result.stdout,
            )

    def test_unknown_check_run_without_purpose_is_orphan_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "scripts").mkdir()
            (target / ".github" / "workflows").mkdir(parents=True)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            (target / "scripts" / "check_custom.py").write_text(
                "print('ok')\n",
                encoding="utf-8",
            )
            (target / ".github" / "workflows" / "ci.yml").write_text(
                "name: CI\njobs:\n  check:\n    steps:\n      - run: python scripts/check_custom.py\n",
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("warning Orphan Feedback", result.stdout)
            self.assertIn("scripts/check_custom.py is run by a workflow or local command", result.stdout)

    def test_example_effectiveness_report_does_not_suppress_unevaluated_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "docs" / "failures").mkdir(parents=True)
            (target / "docs" / "examples").mkdir(parents=True)
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            (target / "AGENTS.md").write_text(
                "Read docs/failures before fixing repeated mistakes.\n",
                encoding="utf-8",
            )
            (target / "docs" / "failures" / "001-real.md").write_text(
                "\n".join(
                    [
                        "# Repeated issue",
                        "",
                        "## Why It Failed",
                        "",
                        "The same issue recurred.",
                        "",
                        "## Current Replacement",
                        "",
                        "Use the stable path.",
                        "",
                        "## Agent Guidance",
                        "",
                        "Do not repeat the old path.",
                        "",
                        "## Detection Or Prevention Check",
                        "",
                        "Manual review checks for recurrence.",
                    ]
                ),
                encoding="utf-8",
            )
            (target / "docs" / "examples" / "effectiveness-report-sample.md").write_text(
                "# Example effectiveness report\n\nIllustrative only.\n",
                encoding="utf-8",
            )

            result = self.run_doctor(target)

            self.assertIn("warning Unevaluated Memory", result.stdout)


if __name__ == "__main__":
    unittest.main()

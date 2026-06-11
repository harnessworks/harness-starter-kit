from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "benchmarks" / "tasks"
REPO_SOURCE = "https://github.com/harnessworks/harness-starter-kit"

EXPECTED_FILES_BY_TASK = {
    "small-bugfix-docs-drift-uv-command": {
        "scripts/check_docs_drift.py",
        "tests/test_check_docs_drift.py",
    },
    "docs-only-evaluation-benchmark-ownership": {
        "docs/evaluation.md",
    },
    "forbidden-file-structure-ignore-runner-output": {
        ".harness/structure-rules.json",
    },
    "failure-memory-benchmark-noop-oracle-gap": {
        "docs/failures/0012-benchmark-noop-oracle-gap.md",
    },
    "decision-memory-benchmark-ownership-adr": {
        "docs/decisions/0008-benchmark-task-ownership.md",
    },
    "profile-boundary-go-race-check": {
        "templates/profiles/go/README.md",
    },
    "installer-non-destructive-list-profiles": {
        "scripts/apply_harness.py",
        "tests/test_apply_harness.py",
    },
    "command-workflow-refresh-benchmark-guidance": {
        "commands/harness-refresh.md",
        "tests/test_repository_hygiene.py",
    },
}


class BenchmarkTaskTests(unittest.TestCase):
    def load_tasks(self) -> dict[str, dict[str, Any]]:
        self.assertTrue(TASK_DIR.is_dir(), "benchmarks/tasks must exist")
        tasks: dict[str, dict[str, Any]] = {}
        for path in sorted(TASK_DIR.glob("*.json")):
            with self.subTest(path=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                task_id = data["id"]
                self.assertNotIn(task_id, tasks)
                tasks[task_id] = data
        return tasks

    def test_required_benchmark_task_files_exist(self) -> None:
        present = {path.name for path in TASK_DIR.glob("*.json")}
        self.assertLessEqual(
            {
                "small-bugfix-docs-drift-uv-command.json",
                "docs-only-evaluation-benchmark-ownership.json",
                "forbidden-file-structure-ignore-runner-output.json",
                "failure-memory-benchmark-noop-oracle-gap.json",
                "decision-memory-benchmark-ownership-adr.json",
                "profile-boundary-go-race-check.json",
                "installer-non-destructive-list-profiles.json",
                "command-workflow-refresh-benchmark-guidance.json",
            },
            present,
        )

    def test_tasks_follow_runner_schema_subset(self) -> None:
        tasks = self.load_tasks()
        self.assertLessEqual(set(EXPECTED_FILES_BY_TASK), set(tasks))

        for task_id, data in tasks.items():
            with self.subTest(task_id=task_id):
                self.assertEqual(1, data["schema_version"])
                self.assertEqual(REPO_SOURCE, data["repo"]["source"])
                self.assertEqual("main", data["repo"]["ref"])
                self.assertEqual(1, data["max_attempts"])
                self.assertGreaterEqual(data["timeout_seconds"], 120)
                self.assertEqual(
                    f"benchmarks/tasks/{task_id}.json",
                    data["prompt_ref"],
                )
                if task_id in EXPECTED_FILES_BY_TASK:
                    self.assertEqual(
                        EXPECTED_FILES_BY_TASK[task_id],
                        set(data["expected_files"]),
                    )
                self.assertTrue(data["forbidden_files"])
                commands = data["verification"]["commands"]
                self.assertTrue(commands)
                for command in commands:
                    self.assertIsInstance(command.get("name"), str)
                    self.assertIn("command", command)
                    self.assertGreater(command.get("timeout_seconds", 0), 0)
                    self.assert_command_shape(command["command"])

    def test_docs_only_task_has_docs_boundary(self) -> None:
        task = self.load_tasks()["docs-only-evaluation-benchmark-ownership"]
        self.assertEqual(["docs/evaluation.md"], task["expected_files"])
        self.assertIn("scripts/**", task["forbidden_files"])
        self.assertIn("tests/**", task["forbidden_files"])
        self.assertIn("benchmarks/**", task["forbidden_files"])

    def test_docs_only_task_oracle_accepts_concept_equivalent_wording(self) -> None:
        result = self.run_docs_only_text_oracle(
            """
            Keep benchmark task definitions in `benchmarks/tasks/`.
            Project-specific benchmark oracle logic is owned by this repository
            instead of the runner repository.
            `expected_files` and `forbidden_files` are boundary controls that
            are assessed independently from verification success.
            """
        )
        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)

    def test_docs_only_task_oracle_rejects_runner_owned_oracles(self) -> None:
        result = self.run_docs_only_text_oracle(
            """
            Keep benchmark task definitions in `benchmarks/tasks/`.
            Project-specific benchmark oracles belong to the runner repository,
            not this repository.
            `expected_files` and `forbidden_files` are boundary controls that
            are assessed independently from verification success.
            """
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("runner repository", result.stderr)

    def test_forbidden_file_guard_names_sensitive_and_generated_paths(self) -> None:
        task = self.load_tasks()["forbidden-file-structure-ignore-runner-output"]
        forbidden = set(task["forbidden_files"])
        for pattern in (
            ".env",
            ".env.*",
            ".github/workflows/**",
            "pyproject.toml",
            "package.json",
            "runs/**",
            "results/**",
            "logs/**",
            "templates/**",
        ):
            self.assertIn(pattern, forbidden)

    def test_expanded_tasks_cover_core_harness_failure_modes(self) -> None:
        tasks = self.load_tasks()
        for task_id in (
            "failure-memory-benchmark-noop-oracle-gap",
            "decision-memory-benchmark-ownership-adr",
            "profile-boundary-go-race-check",
            "installer-non-destructive-list-profiles",
            "command-workflow-refresh-benchmark-guidance",
        ):
            self.assertIn(task_id, tasks)

    def test_expected_files_are_required_by_task_oracles(self) -> None:
        tasks = self.load_tasks()
        for task_id, expected_files in EXPECTED_FILES_BY_TASK.items():
            with self.subTest(task_id=task_id):
                command_text = "\n".join(
                    "\n".join(command["command"])
                    if isinstance(command["command"], list)
                    else command["command"]
                    for command in tasks[task_id]["verification"]["commands"]
                )
                for expected_file in expected_files:
                    self.assertIn(expected_file, command_text)

    def test_installer_task_preserves_template_boundary(self) -> None:
        task = self.load_tasks()["installer-non-destructive-list-profiles"]
        self.assertEqual(
            {"scripts/apply_harness.py", "tests/test_apply_harness.py"},
            set(task["expected_files"]),
        )
        self.assertIn("templates/**", task["forbidden_files"])
        self.assertIn("tests/fixtures/**", task["forbidden_files"])

    def test_command_workflow_task_blocks_benchmark_json_edits(self) -> None:
        task = self.load_tasks()["command-workflow-refresh-benchmark-guidance"]
        self.assertEqual(
            {"commands/harness-refresh.md", "tests/test_repository_hygiene.py"},
            set(task["expected_files"]),
        )
        self.assertIn("benchmarks/**", task["forbidden_files"])

    def test_command_workflow_oracle_accepts_line_wrapped_concepts(self) -> None:
        result = self.run_refresh_workflow_oracle(
            command_body="""
            Refresh reviews should inspect `benchmarks/tasks/*.json` and
            benchmark documentation for stale prompts, stale verification
            commands, obsolete expected/forbidden boundaries, or runner-output
            assumptions.
            """,
            test_body="""
            def test_refresh_mentions_benchmark_guidance():
                guidance = '''
                benchmarks/tasks/*.json
                expected/forbidden boundaries
                runner-output
                assumptions
                '''
                assert guidance
            """,
        )
        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)

    def test_command_workflow_oracle_rejects_missing_runner_output_concept(self) -> None:
        result = self.run_refresh_workflow_oracle(
            command_body="""
            Refresh reviews should inspect `benchmarks/tasks/*.json` and
            benchmark documentation for stale prompts, stale verification
            commands, and obsolete expected/forbidden boundaries.
            """,
            test_body="""
            def test_refresh_mentions_benchmark_guidance():
                guidance = '''
                benchmarks/tasks/*.json
                expected/forbidden boundaries
                '''
                assert guidance
            """,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("runner-output assumptions", result.stderr)

    def test_benchmark_readme_documents_main_ref_reproducibility(self) -> None:
        text = (ROOT / "benchmarks" / "README.md").read_text(encoding="utf-8")
        self.assertIn("`repo.ref` set to `main`", text)
        self.assertIn("resolved", text)
        self.assertIn("`repository_ref`", text)
        self.assertIn("`--repo-ref <commit-sha>`", text)
        self.assertIn("runner repository", text)
        for task_id in EXPECTED_FILES_BY_TASK:
            self.assertIn(task_id, text)

    def assert_command_shape(self, command: Any) -> None:
        if isinstance(command, str):
            self.assertTrue(command.strip())
            return
        if isinstance(command, list):
            self.assertTrue(command)
            self.assertTrue(all(isinstance(item, str) and item for item in command))
            return
        self.fail(f"unsupported command shape: {command!r}")

    def run_refresh_workflow_oracle(
        self,
        *,
        command_body: str,
        test_body: str,
    ) -> subprocess.CompletedProcess[str]:
        task = self.load_tasks()["command-workflow-refresh-benchmark-guidance"]
        command = task["verification"]["commands"][1]["command"]
        script = command[2]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            commands_dir = tmp / "commands"
            tests_dir = tmp / "tests"
            commands_dir.mkdir()
            tests_dir.mkdir()
            refresh = commands_dir / "harness-refresh.md"
            hygiene = tests_dir / "test_repository_hygiene.py"
            refresh.write_text("# /harness refresh\n\nInitial guidance.\n", encoding="utf-8")
            hygiene.write_text("def test_seed():\n    assert True\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Benchmark Test"],
                cwd=tmp,
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "add",
                    "commands/harness-refresh.md",
                    "tests/test_repository_hygiene.py",
                ],
                cwd=tmp,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-q", "-m", "seed refresh workflow"],
                cwd=tmp,
                check=True,
            )
            refresh.write_text(
                "# /harness refresh\n\n"
                f"{textwrap.dedent(command_body).strip()}\n",
                encoding="utf-8",
            )
            hygiene.write_text(
                f"{textwrap.dedent(test_body).strip()}\n",
                encoding="utf-8",
            )
            return subprocess.run(
                ["python3", "-c", script],
                cwd=tmp,
                text=True,
                capture_output=True,
                check=False,
            )

    def run_docs_only_text_oracle(
        self, section_body: str
    ) -> subprocess.CompletedProcess[str]:
        task = self.load_tasks()["docs-only-evaluation-benchmark-ownership"]
        command = task["verification"]["commands"][0]["command"]
        script = command[2]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            docs = tmp / "docs"
            docs.mkdir()
            evaluation = docs / "evaluation.md"
            evaluation.write_text(
                "# Harness Effectiveness Evaluation\n\n"
                "Initial tracked content.\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Benchmark Test"],
                cwd=tmp,
                check=True,
            )
            subprocess.run(["git", "add", "docs/evaluation.md"], cwd=tmp, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "seed docs"],
                cwd=tmp,
                check=True,
            )
            evaluation.write_text(
                "# Harness Effectiveness Evaluation\n\n"
                "## Deterministic Benchmark Tasks\n\n"
                f"{textwrap.dedent(section_body).strip()}\n\n"
                "## Interpretation\n\n"
                "The rest of the evaluation guide continues here.\n",
                encoding="utf-8",
            )
            return subprocess.run(
                ["python3", "-c", script],
                cwd=tmp,
                text=True,
                capture_output=True,
                check=False,
            )


if __name__ == "__main__":
    unittest.main()

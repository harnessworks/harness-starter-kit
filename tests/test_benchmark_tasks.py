from __future__ import annotations

import json
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

    def test_benchmark_readme_documents_main_ref_reproducibility(self) -> None:
        text = (ROOT / "benchmarks" / "README.md").read_text(encoding="utf-8")
        self.assertIn("`repo.ref` set to `main`", text)
        self.assertIn("resolved", text)
        self.assertIn("`repository_ref`", text)
        self.assertIn("`--repo-ref <commit-sha>`", text)
        self.assertIn("runner repository", text)

    def assert_command_shape(self, command: Any) -> None:
        if isinstance(command, str):
            self.assertTrue(command.strip())
            return
        if isinstance(command, list):
            self.assertTrue(command)
            self.assertTrue(all(isinstance(item, str) and item for item in command))
            return
        self.fail(f"unsupported command shape: {command!r}")


if __name__ == "__main__":
    unittest.main()

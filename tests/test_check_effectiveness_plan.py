from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_effectiveness_plan.py"


COMPLETE_ADOPTION_REPORT = """# Adoption Report

## Verification Gate Placement

- Normal completion gate: `npm run check:harness`.
- Deterministic behavior checks included in the normal gate: `npm test`.
- Focused or manual checks outside the normal gate: live API smoke check.
- Reasons for focused/manual placement: live API smoke requires credentials and
  provider uptime.

## Failure Memory

- Recorded: none; no recurring failure was fixed.
- Detection or prevention check: not applicable because no failure record was
  added.
- Skipped: no user-visible runtime failure, high-risk bug path, failed check,
  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.

## Effectiveness Measurement Plan

- Baseline available: No historical agent PR data available.
- Comparable tasks to repeat or track: next 5 route, docs, and test changes.
- Primary metric: wrong-file edits and first-pass verification success.
- Review window: next 5 comparable agent changes.
- Results location: `docs/effectiveness/harness.md`.
- Task outcome records location: `docs/effectiveness/task-outcomes/`.
"""


COMPLETE_EFFECTIVENESS_REPORT = """# Harness Effectiveness Report

## Target

- Repository: sample

## Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| T1 | Add route | routes and tests | direct database import |

## Results

| Metric | Baseline | Harnessed | Delta |
| --- | ---: | ---: | ---: |
| Wrong-file edits | 3 | 1 | -2 |

## Interpretation

- What improved: fewer wrong-file edits.
"""


class CheckEffectivenessPlanTests(unittest.TestCase):
    def run_checker(
        self, root: Path, *args: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            cwd=root,
            capture_output=True,
            text=True,
        )

    def write_failure_record(
        self,
        root: Path,
        relative: str = "docs/failures/0001-provider-casing.md",
    ) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Failure\n", encoding="utf-8")

    def touch_local_path(self, root: Path, relative: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")

    def write_task_outcome(
        self,
        root: Path,
        relative: str,
        include_in_report: str = "true",
        include_in_count: str = "true",
        task_id: str = "T1",
        run_id: str = "T1-001",
        prompt_summary: str = "Add route",
        prompt_ref: str = "local test prompt",
        prompt_hash: str = "not recorded",
        start_ref: str = "abc123",
        reviewer: str = "human reviewer",
        expected_boundary: tuple[str, ...] = ("src/app.py", "tests/test_app.py"),
        verification_command: str = "python -m unittest",
        first_pass_result: str = "passed",
    ) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        boundary_lines = tuple(f"    - {item}" for item in expected_boundary)
        path.write_text(
            "\n".join(
                (
                    "schema_version: 1",
                    "",
                    "target:",
                    "  repository: example/repo",
                    f"  repository_ref: {start_ref}",
                    "  stack_or_framework: Python",
                    "  date: 2026-06-06",
                    "  agent_or_model: test-agent",
                    f"  reviewer: {reviewer}",
                    "",
                    "task:",
                    f"  id: {task_id}",
                    f"  run_id: {run_id}",
                    f"  prompt_summary: {prompt_summary}",
                    f"  prompt_ref: {prompt_ref}",
                    f"  prompt_hash: {prompt_hash}",
                    "  comparable_task_group: test-group",
                    "  condition: harnessed-only",
                    "  expected_boundary:",
                    *boundary_lines,
                    "  known_failure_mode: wrong-file edit",
                    "",
                    "outcome:",
                    "  files_changed:",
                    "    - src/app.py",
                    "  wrong_file_edits: 0",
                    "  repeated_known_mistake: false",
                    f"  verification_command: {verification_command}",
                    "  first_pass_verification:",
                    f"    result: {first_pass_result}",
                    "  drift_violations_detected: []",
                    "  human_rework_minutes: 0",
                    "  reverted_files: []",
                    "  notes: test fixture outcome",
                    "",
                    "follow_up:",
                    "  harness_change_needed: false",
                    "  decision_or_failure_record: none",
                    f"  include_in_effectiveness_report: {include_in_report}",
                    f"  include_in_comparable_product_task_count: {include_in_count}",
                    "",
                )
            ),
            encoding="utf-8",
        )

    def write_package_json(self, root: Path, scripts: dict[str, str]) -> None:
        (root / "package.json").write_text(
            json.dumps({"scripts": scripts}),
            encoding="utf-8",
        )

    def write_makefile(self, root: Path, text: str) -> None:
        (root / "Makefile").write_text(text, encoding="utf-8")

    def write_justfile(self, root: Path, text: str) -> None:
        (root / "justfile").write_text(text, encoding="utf-8")

    def write_maven_project(
        self,
        root: Path,
        with_wrapper: bool = False,
        wrapper_name: str = "mvnw",
    ) -> None:
        (root / "pom.xml").write_text(
            "<project><modelVersion>4.0.0</modelVersion></project>\n",
            encoding="utf-8",
        )
        if with_wrapper:
            (root / wrapper_name).write_text("#!/bin/sh\n", encoding="utf-8")

    def write_gradle_project(
        self,
        root: Path,
        with_wrapper: bool = False,
        wrapper_name: str = "gradlew",
    ) -> None:
        (root / "build.gradle").write_text("tasks.register('check')\n", encoding="utf-8")
        if with_wrapper:
            (root / wrapper_name).write_text("#!/bin/sh\n", encoding="utf-8")

    def write_go_project(self, root: Path) -> None:
        (root / "go.mod").write_text("module example.com/app\n", encoding="utf-8")

    def test_no_report_passes_unless_report_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = self.run_checker(root)
            required = self.run_checker(root, "--require-report")

            self.assertEqual(0, result.returncode)
            self.assertEqual(1, required.returncode)
            self.assertIn("No adoption or effectiveness report found", required.stdout)

    def test_complete_adoption_report_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT,
                encoding="utf-8",
            )

            result = self.run_checker(root, "--require-report")

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_missing_measurement_plan_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                "# Adoption Report\n\n## Verification Gate Placement\n\n"
                "- Normal completion gate: `npm test`.\n"
                "- Deterministic behavior checks included in the normal gate: `npm test`.\n"
                "- Focused or manual checks outside the normal gate: none.\n"
                "- Reasons for focused/manual placement: not applicable.\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("missing ## Effectiveness Measurement Plan", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_missing_gate_placement_plan_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "## Verification Gate Placement",
                    "## Removed Gate Placement",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("missing ## Verification Gate Placement", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_missing_failure_memory_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            failure_section = (
                "## Failure Memory\n\n"
                "- Recorded: none; no recurring failure was fixed.\n"
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.\n"
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.\n\n"
            )
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(failure_section, ""),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("missing ## Failure Memory", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_todo_failure_memory_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "not applicable because no failure record was\n  added.",
                    "TODO",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn(
                "incomplete failure-memory field: Detection or prevention check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_no_record_detection_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "- Recorded: none; no recurring failure was fixed.",
                    "- Recorded: `docs/failures/0001-provider-casing.md`.",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn(
                "contradictory failure-memory field: Detection or prevention check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_vague_detection_fails(self) -> None:
        examples = (
            "smoke check.",
            "Smoke check `provider boundary`.",
            "Drift check `generated docs`.",
            "CI gate `main`.",
            "Manual review point `provider contract`.",
        )
        for example in examples:
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: {example}",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(
                        "incomplete failure-memory detection link",
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_vague_no_check_reason_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                (
                    "- Detection or prevention check: No check is practical because "
                    "this is external behavior; revisit when some process is "
                    "available."
                ),
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn("incomplete failure-memory detection link", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_field_must_name_failure_record_path(self) -> None:
        examples = (
            "yes",
            "0001-provider-casing.md",
        )
        for example in examples:
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        f"- Recorded: {example}.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        "- Detection or prevention check: `npm run test:planner`.",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(
                        "Recorded must list docs/failures/... or none",
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_path_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/missing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `npm run test:planner`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "Recorded references missing record: docs/failures/missing.md",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_non_committal_detection_fails(self) -> None:
        examples = (
            (
                "No regression test exists yet, but "
                "tests/provider-contract.test.ts should be added."
            ),
            "tests/provider-contract.test.ts should be added later.",
            "tests/provider-contract.test.ts is planned.",
            "tests/provider-contract.test.ts will be added.",
        )
        for example in examples:
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    self.touch_local_path(root, "tests/provider-contract.test.ts")
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: {example}",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(
                        "non-committal failure-memory detection prose",
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_recorded_none_with_failure_reference_fails(self) -> None:
        examples = (
            "none; docs/failures/missing.md was not added.",
            "none; covered by docs/failures/0001-provider-casing.md.",
        )
        for example in examples:
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        f"- Recorded: {example}",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(
                        "contradictory failure-memory Recorded",
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_missing_detection_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `tests/provider-contract.test.ts`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "detection references missing local path: tests/provider-contract.test.ts",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_existing_detection_path_may_include_planned_word(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.touch_local_path(root, "tests/planned-route.test.ts")
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `tests/planned-route.test.ts`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_recorded_failure_with_concrete_command_detection_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.write_package_json(
                root,
                {"test:planner": "node --test planner.test.mjs"},
            )
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `npm run test:planner`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_recorded_failure_command_allows_terminal_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.write_package_json(
                root,
                {"test:planner": "node --test planner.test.mjs"},
            )
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: npm run test:planner.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_recorded_failure_command_managers_use_root_scripts(self) -> None:
        examples = (
            "npm run test:planner",
            "pnpm run test:planner",
            "yarn run test:planner",
            "bun run test:planner",
        )
        for example in examples:
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    self.write_package_json(
                        root,
                        {"test:planner": "node --test planner.test.mjs"},
                    )
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{example}`.",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_recorded_failure_with_missing_package_script_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.write_package_json(root, {"test:other": "node --test other.test.mjs"})
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `npm run test:planner`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "failure-memory detection references missing package.json script: "
                "npm run test:planner",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_make_or_just_command_detection_passes(self) -> None:
        examples = (
            ("make check.", "Makefile", "check:\n\tpython3 -m unittest\n"),
            ("just verify.", "justfile", "@verify:\n    python3 -m unittest\n"),
            (
                "just ci.",
                "justfile",
                "alias ci := verify\nverify:\n    python3 -m unittest\n",
            ),
            (
                "just deploy.",
                "justfile",
                "deploy env='prod':\n    python3 -m unittest\n",
            ),
        )
        for command, command_file, command_file_text in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    (root / command_file).write_text(
                        command_file_text,
                        encoding="utf-8",
                    )
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{command}`",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_recorded_failure_with_maven_gradle_go_detection_passes(self) -> None:
        examples = (
            ("mvn test.", "maven", False),
            ("./mvnw verify.", "maven", True),
            (".\\mvnw.cmd verify.", "maven-cmd", True),
            ("gradle test.", "gradle", False),
            ("./gradlew check.", "gradle", True),
            (".\\gradlew.bat check.", "gradle-bat", True),
            ("go test ./...", "go", False),
        )
        for command, project_type, with_wrapper in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    if project_type == "maven":
                        self.write_maven_project(root, with_wrapper=with_wrapper)
                    elif project_type == "maven-cmd":
                        self.write_maven_project(
                            root,
                            with_wrapper=with_wrapper,
                            wrapper_name="mvnw.cmd",
                        )
                    elif project_type == "gradle":
                        self.write_gradle_project(root, with_wrapper=with_wrapper)
                    elif project_type == "gradle-bat":
                        self.write_gradle_project(
                            root,
                            with_wrapper=with_wrapper,
                            wrapper_name="gradlew.bat",
                        )
                    else:
                        self.write_go_project(root)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{command}`",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_recorded_failure_with_missing_make_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.write_makefile(root, "other:\n\tpython3 -m unittest\n")
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `make check`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "failure-memory detection references missing Makefile target: make check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_missing_maven_gradle_go_project_fails(self) -> None:
        examples = (
            (
                "`mvn test`.",
                "failure-memory detection maven command references missing pom.xml: mvn test",
            ),
            (
                "`gradle test`.",
                "failure-memory detection gradle command references missing build file: gradle test",
            ),
            (
                "`go test ./...`.",
                (
                    "failure-memory detection go command references missing go.mod: "
                    "go test ./..."
                ),
            ),
        )
        for command, expected_message in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: {command}",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(expected_message, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_capitalized_go_command_requires_go_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `Go test ./...`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "failure-memory detection go command references missing go.mod: Go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_windows_subpath_wrappers_are_not_root_commands(
        self,
    ) -> None:
        examples = (
            "tools\\mvnw.cmd verify",
            "tools\\gradlew.bat check",
        )
        for command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{command}`.",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(
                        "incomplete failure-memory detection link",
                        result.stdout,
                    )
                    self.assertNotIn("wrapper command references", result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_missing_maven_or_gradle_wrapper_fails(self) -> None:
        examples = (
            (
                "./mvnw verify",
                "maven",
                "failure-memory detection maven wrapper command references missing wrapper: ./mvnw verify",
            ),
            (
                "./gradlew check",
                "gradle",
                "failure-memory detection gradle wrapper command references missing wrapper: ./gradlew check",
            ),
        )
        for command, project_type, expected_message in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    if project_type == "maven":
                        self.write_maven_project(root)
                    else:
                        self.write_gradle_project(root)
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{command}`.",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(expected_message, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_wrapper_flavor_mismatch_fails(self) -> None:
        examples = (
            (
                "./mvnw verify",
                "maven",
                "mvnw.cmd",
                "failure-memory detection maven wrapper command references missing wrapper: ./mvnw verify",
            ),
            (
                ".\\mvnw.cmd verify",
                "maven",
                "mvnw",
                "failure-memory detection maven wrapper command references missing wrapper: .\\mvnw.cmd verify",
            ),
            (
                "./gradlew check",
                "gradle",
                "gradlew.bat",
                "failure-memory detection gradle wrapper command references missing wrapper: ./gradlew check",
            ),
            (
                ".\\gradlew.bat check",
                "gradle",
                "gradlew",
                "failure-memory detection gradle wrapper command references missing wrapper: .\\gradlew.bat check",
            ),
        )
        for command, project_type, existing_wrapper, expected_message in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    if project_type == "maven":
                        self.write_maven_project(
                            root,
                            with_wrapper=True,
                            wrapper_name=existing_wrapper,
                        )
                    else:
                        self.write_gradle_project(
                            root,
                            with_wrapper=True,
                            wrapper_name=existing_wrapper,
                        )
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{command}`.",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertIn(expected_message, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_recorded_failure_make_command_allows_leading_variable_assignments(
        self,
    ) -> None:
        examples = (
            "make ENV=ci check",
            "make PYTHON=python3.11 check",
        )
        for command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_failure_record(root)
                    self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
                    report = COMPLETE_ADOPTION_REPORT.replace(
                        "- Recorded: none; no recurring failure was fixed.",
                        "- Recorded: `docs/failures/0001-provider-casing.md`.",
                    ).replace(
                        "- Detection or prevention check: not applicable because no failure record was\n"
                        "  added.",
                        f"- Detection or prevention check: `{command}`.",
                    ).replace(
                        "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                        "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                        "- Skipped: none; failure memory was recorded.",
                    )
                    (root / "adoption-report.md").write_text(report, encoding="utf-8")

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_recorded_failure_make_variable_assignment_without_target_is_not_concrete(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `make ENV=ci`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "incomplete failure-memory detection link",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_make_command_uses_gnu_makefile_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            (root / "GNUmakefile").write_text(
                "other:\n\tpython3 -m unittest\n",
                encoding="utf-8",
            )
            self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `make check`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "failure-memory detection references missing Makefile target: make check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_missing_just_recipe_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            self.write_justfile(root, "other:\n    python3 -m unittest\n")
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `just verify`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "failure-memory detection references missing justfile recipe: just verify",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_requires_root_package_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_failure_record(root)
            nested_package = root / "packages" / "app"
            nested_package.mkdir(parents=True)
            self.write_package_json(
                nested_package,
                {"test:planner": "node --test planner.test.mjs"},
            )
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `npm run test:planner`.",
            ).replace(
                "- Skipped: no user-visible runtime failure, high-risk bug path, failed check,\n"
                "  CI failure, repeated agent mistake, or cross-environment mismatch was fixed.",
                "- Skipped: none; failure memory was recorded.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "failure-memory detection references missing package.json script: "
                "npm run test:planner",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_recorded_failure_with_skipped_no_failure_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = COMPLETE_ADOPTION_REPORT.replace(
                "- Recorded: none; no recurring failure was fixed.",
                "- Recorded: `docs/failures/0001-provider-casing.md`.",
            ).replace(
                "- Detection or prevention check: not applicable because no failure record was\n"
                "  added.",
                "- Detection or prevention check: `tests/provider-contract.test.ts`.",
            )
            (root / "adoption-report.md").write_text(report, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "contradictory failure-memory field: Skipped",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_similar_gate_placement_heading_does_not_satisfy_section(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "## Verification Gate Placement",
                    "## Verification Gate Placement Notes",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("missing ## Verification Gate Placement", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_todo_gate_placement_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "`npm run check:harness`",
                    "TODO",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn(
                "incomplete gate-placement field: Normal completion gate",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_blank_gate_placement_field_before_next_bullet_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "- Normal completion gate: `npm run check:harness`.",
                    "- Normal completion gate:",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn(
                "incomplete gate-placement field: Normal completion gate",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_wrapped_gate_placement_field_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "- Normal completion gate: `npm run check:harness`.",
                    "- Normal completion gate:\n  `npm run check:harness`.",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_nested_bullet_gate_placement_field_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "- Normal completion gate: `npm run check:harness`.",
                    "- Normal completion gate:\n  - `npm run check:harness`",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_gate_placement_fields_outside_section_do_not_satisfy_section(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "## Verification Gate Placement\n\n"
                    "- Normal completion gate: `npm run check:harness`.\n"
                    "- Deterministic behavior checks included in the normal gate: `npm test`.\n"
                    "- Focused or manual checks outside the normal gate: live API smoke check.\n"
                    "- Reasons for focused/manual placement: live API smoke requires credentials and\n"
                    "  provider uptime.",
                    "## Verification Gate Placement\n\n"
                    "## Other Section\n\n"
                    "- Normal completion gate: `npm run check:harness`.\n"
                    "- Deterministic behavior checks included in the normal gate: `npm test`.\n"
                    "- Focused or manual checks outside the normal gate: live API smoke check.\n"
                    "- Reasons for focused/manual placement: live API smoke requires credentials and\n"
                    "  provider uptime.",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn(
                "incomplete gate-placement field: Normal completion gate",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_todo_measurement_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "wrong-file edits and first-pass verification success.",
                    "TODO",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("incomplete measurement field: Primary metric", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_templates_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template_dir = root / "docs" / "templates"
            template_dir.mkdir(parents=True)
            (template_dir / "adoption-report.md").write_text(
                "# Adoption Report\n\n## Effectiveness Measurement Plan\n\n"
                "- Baseline available: TODO\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_complete_effectiveness_report_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node-effectiveness-report.md").write_text(
                COMPLETE_EFFECTIVENESS_REPORT,
                encoding="utf-8",
            )

            result = self.run_checker(root, "--require-report")

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_effectiveness_report_completion_contradiction_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node-effectiveness-report.md").write_text(
                COMPLETE_EFFECTIVENESS_REPORT
                + "\nFive comparable product-task runs have been completed.\n"
                + "\n- Confounders or limitations: no baseline and no completed "
                "product-task records yet.\n"
                + "- Harness changes to make next: record T1 through T5 task "
                "outcomes as they run.\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn(
                "contradictory effectiveness-report completion language",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_no_completed_language_without_completion_claim_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node-effectiveness-report.md").write_text(
                COMPLETE_EFFECTIVENESS_REPORT
                + "\n- Confounders or limitations: no completed product-task "
                "records yet.\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_effectiveness_report_with_todo_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node-effectiveness-report.md").write_text(
                COMPLETE_EFFECTIVENESS_REPORT + "\n- Follow-up: TODO\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("effectiveness report still contains TODO", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_task_outcome_template_with_true_inclusion_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/task-outcome-template.yaml",
                task_id="unknown",
                run_id="unknown",
                prompt_summary="unknown",
                start_ref="unknown",
            )

            result = self.run_checker(root)

            self.assertIn("task outcome template must not be included", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_included_task_outcome_requires_comparable_count_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                include_in_count="",
            )

            result = self.run_checker(root)

            self.assertIn(
                "must declare include_in_comparable_product_task_count",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_comparable_task_outcome_requires_report_inclusion_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                include_in_report="",
            )

            result = self.run_checker(root)

            self.assertIn(
                "must set include_in_effectiveness_report to true",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_comparable_task_outcome_rejects_false_report_inclusion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                include_in_report="false",
                include_in_count="true",
            )

            result = self.run_checker(root)

            self.assertIn(
                "must set include_in_effectiveness_report to true",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_report_included_non_product_task_outcome_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-adoption-cleanup.yaml",
                include_in_report="true",
                include_in_count="false",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_included_task_outcome_requires_core_evidence_fields(self) -> None:
        cases = (
            ("missing-ref", {"start_ref": ""}, "repository_ref"),
            ("missing-run", {"run_id": ""}, "run_id"),
            ("missing-reviewer", {"reviewer": ""}, "reviewer"),
            ("missing-boundary", {"expected_boundary": ()}, "expected_boundary"),
            (
                "empty-inline-boundary",
                {"expected_boundary": ("[]",)},
                "expected_boundary",
            ),
            (
                "missing-verification",
                {"verification_command": ""},
                "verification_command",
            ),
        )
        for name, kwargs, missing_field in cases:
            with self.subTest(case=name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        **kwargs,
                    )

                    result = self.run_checker(root)

                    self.assertIn(
                        "included task outcome is missing required evidence field(s)",
                        result.stdout,
                    )
                    self.assertIn(missing_field, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_included_task_outcome_rejects_empty_inline_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "docs/effectiveness/task-outcomes/001-route.yaml"
            self.write_task_outcome(root, str(path.relative_to(root)))
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                "  expected_boundary:\n    - src/app.py\n    - tests/test_app.py",
                "  expected_boundary: []",
            )
            path.write_text(text, encoding="utf-8")

            result = self.run_checker(root)

            self.assertIn(
                "included task outcome is missing required evidence field(s)",
                result.stdout,
            )
            self.assertIn("expected_boundary", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_included_task_outcome_requires_prompt_ref_or_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                prompt_ref="",
                prompt_hash="not recorded",
            )

            result = self.run_checker(root)

            self.assertIn(
                "must include prompt_ref or prompt_hash",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_included_task_outcome_requires_first_pass_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                first_pass_result="",
            )

            result = self.run_checker(root)

            self.assertIn(
                "missing first_pass_verification.result",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_included_task_outcome_make_or_just_verification_passes_when_defined(
        self,
    ) -> None:
        examples = (
            ("make check.", "Makefile", "check:\n\tpython3 -m unittest\n"),
            ("just verify.", "justfile", "@verify:\n    python3 -m unittest\n"),
            (
                "just ci.",
                "justfile",
                "alias ci := verify\nverify:\n    python3 -m unittest\n",
            ),
            (
                "just deploy.",
                "justfile",
                "deploy env='prod':\n    python3 -m unittest\n",
            ),
        )
        for command, command_file, command_file_text in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / command_file).write_text(
                        command_file_text,
                        encoding="utf-8",
                    )
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        verification_command=command,
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_included_task_outcome_maven_gradle_go_verification_passes_when_defined(
        self,
    ) -> None:
        examples = (
            ("mvn test.", "maven", False),
            ("./mvnw verify.", "maven", True),
            (".\\mvnw.cmd verify.", "maven-cmd", True),
            ("gradle test.", "gradle", False),
            ("./gradlew check.", "gradle", True),
            (".\\gradlew.bat check.", "gradle-bat", True),
            ("go test ./...", "go", False),
        )
        for command, project_type, with_wrapper in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    if project_type == "maven":
                        self.write_maven_project(root, with_wrapper=with_wrapper)
                    elif project_type == "maven-cmd":
                        self.write_maven_project(
                            root,
                            with_wrapper=with_wrapper,
                            wrapper_name="mvnw.cmd",
                        )
                    elif project_type == "gradle":
                        self.write_gradle_project(root, with_wrapper=with_wrapper)
                    elif project_type == "gradle-bat":
                        self.write_gradle_project(
                            root,
                            with_wrapper=with_wrapper,
                            wrapper_name="gradlew.bat",
                        )
                    else:
                        self.write_go_project(root)
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        verification_command=command,
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_included_task_outcome_make_or_just_verification_must_exist(self) -> None:
        examples = (
            (
                "make check",
                "task outcome verification references missing Makefile target: make check",
            ),
            (
                "make PYTHON=python3.11 missing",
                "task outcome verification references missing Makefile target: make missing",
            ),
            (
                "just verify",
                "task outcome verification references missing justfile recipe: just verify",
            ),
        )
        for command, expected_message in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        verification_command=command,
                    )

                    result = self.run_checker(root)

                    self.assertIn(expected_message, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_included_task_outcome_maven_gradle_go_verification_must_exist(
        self,
    ) -> None:
        examples = (
            (
                "mvn test",
                "task outcome verification maven command references missing pom.xml: mvn test",
            ),
            (
                "./mvnw verify",
                "task outcome verification maven wrapper command references missing wrapper: ./mvnw verify",
            ),
            (
                "gradle test",
                "task outcome verification gradle command references missing build file: gradle test",
            ),
            (
                "./gradlew check",
                "task outcome verification gradle wrapper command references missing wrapper: ./gradlew check",
            ),
            (
                "go test ./...",
                (
                    "task outcome verification go command references missing go.mod: "
                    "go test ./..."
                ),
            ),
        )
        for command, expected_message in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        verification_command=command,
                    )

                    result = self.run_checker(root)

                    self.assertIn(expected_message, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_task_outcome_capitalized_go_verification_requires_go_project(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                verification_command="Go test ./...",
            )

            result = self.run_checker(root)

            self.assertIn(
                "task outcome verification go command references missing go.mod: Go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_task_outcome_windows_subpath_wrappers_are_not_root_commands(
        self,
    ) -> None:
        examples = (
            "tools\\mvnw.cmd verify",
            "tools\\gradlew.bat check",
        )
        for command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        verification_command=command,
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_task_outcome_wrapper_flavor_mismatch_fails(self) -> None:
        examples = (
            (
                "./mvnw verify",
                "maven",
                "mvnw.cmd",
                "task outcome verification maven wrapper command references missing wrapper: ./mvnw verify",
            ),
            (
                ".\\mvnw.cmd verify",
                "maven",
                "mvnw",
                "task outcome verification maven wrapper command references missing wrapper: .\\mvnw.cmd verify",
            ),
            (
                "./gradlew check",
                "gradle",
                "gradlew.bat",
                "task outcome verification gradle wrapper command references missing wrapper: ./gradlew check",
            ),
            (
                ".\\gradlew.bat check",
                "gradle",
                "gradlew",
                "task outcome verification gradle wrapper command references missing wrapper: .\\gradlew.bat check",
            ),
        )
        for command, project_type, existing_wrapper, expected_message in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    if project_type == "maven":
                        self.write_maven_project(
                            root,
                            with_wrapper=True,
                            wrapper_name=existing_wrapper,
                        )
                    else:
                        self.write_gradle_project(
                            root,
                            with_wrapper=True,
                            wrapper_name=existing_wrapper,
                        )
                    self.write_task_outcome(
                        root,
                        "docs/effectiveness/task-outcomes/001-route.yaml",
                        verification_command=command,
                    )

                    result = self.run_checker(root)

                    self.assertIn(expected_message, result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_task_outcome_go_verification_does_not_count_vendor_only_source(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.touch_local_path(root, "vendor/example.com/lib/lib.go")
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                verification_command="go test ./...",
            )

            result = self.run_checker(root)

            self.assertIn(
                "task outcome verification go command references missing go.mod: go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_task_outcome_go_verification_does_not_count_source_only_project(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.touch_local_path(root, "cmd/app/main.go")
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                verification_command="go test ./...",
            )

            result = self.run_checker(root)

            self.assertIn(
                "task outcome verification go command references missing go.mod: go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_false_inclusion_task_outcome_still_validates_make_verification(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-route.yaml",
                include_in_report="false",
                include_in_count="false",
                verification_command="make check",
            )

            result = self.run_checker(root)

            self.assertIn(
                "task outcome verification references missing Makefile target: make check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_task_outcome_template_with_false_inclusion_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/task-outcome-template.yaml",
                include_in_report="false",
                include_in_count="false",
                task_id="unknown",
                run_id="unknown",
                prompt_summary="unknown",
                start_ref="unknown",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_placeholder_task_outcome_with_true_inclusion_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-placeholder.yaml",
                task_id="unknown",
            )

            result = self.run_checker(root)

            self.assertIn(
                "placeholder task outcome must not be included",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_todo_task_outcome_with_true_inclusion_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_task_outcome(
                root,
                "docs/effectiveness/task-outcomes/001-todo.yaml",
                task_id="TODO",
                run_id="TODO",
                prompt_summary="TODO",
                start_ref="TODO",
            )

            result = self.run_checker(root)

            self.assertIn(
                "placeholder task outcome must not be included",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()

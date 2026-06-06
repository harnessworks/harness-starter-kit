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
        start_ref: str = "abc123",
    ) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(
                (
                    "schema_version: 1",
                    "",
                    "task:",
                    f"  id: {task_id}",
                    f"  run_id: {run_id}",
                    f"  prompt_summary: {prompt_summary}",
                    f"  start_ref: {start_ref}",
                    "",
                    "follow_up:",
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

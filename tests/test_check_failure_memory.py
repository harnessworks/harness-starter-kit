from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_failure_memory.py"


VALID_RECORD = """# 0001. Example Failure

## Date Observed

2026-06-03

## Failure Type

Failed harness check.

## Goal

Prevent recurrence.

## What Happened Or Was Tried

Something failed.

## Why It Failed

The check was missing.

## Current Replacement

The check now exists.

## Detection Or Prevention Check

`tests/test_example.py` fails if the bug path returns.

## Agent Guidance

Run the check before finishing similar work.
"""


class CheckFailureMemoryTests(unittest.TestCase):
    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=root,
            capture_output=True,
            text=True,
        )

    def write_record(self, root: Path, text: str, name: str = "0001-example.md") -> None:
        failures = root / "docs" / "failures"
        failures.mkdir(parents=True)
        (failures / name).write_text(text, encoding="utf-8")

    def touch_local_path(self, root: Path, relative: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")

    def create_valid_reference_paths(self, root: Path) -> None:
        for relative in (
            "tests/test_example.py",
            "scripts/check_docs_drift.py",
            ".github/workflows/harness-check.yml",
            "docs/checklists/external-api-work.md",
            "fixtures/tago-nodeid.json",
        ):
            self.touch_local_path(root, relative)

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

    def test_no_failure_records_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_checker(Path(tmp))

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_valid_failure_record_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.touch_local_path(root, "tests/test_example.py")
            self.write_record(root, VALID_RECORD)

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_missing_detection_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "## Detection Or Prevention Check\n\n"
                    "`tests/test_example.py` fails if the bug path returns.\n\n",
                    "",
                ),
            )

            result = self.run_checker(root)

            self.assertIn("missing required section", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_non_committal_test_language_fails(self) -> None:
        examples = (
            "No test has been added yet for tests/test_example.py.",
            "tests/test_example.py should be added later.",
            "tests/test_example.py is planned.",
            "tests/test_example.py will be added.",
        )
        for index, example in enumerate(examples, start=1):
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.touch_local_path(root, "tests/test_example.py")
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            example,
                        ),
                        f"000{index}-example.md",
                    )

                    result = self.run_checker(root)

                    self.assertIn(
                        "non-committal detection/prevention prose",
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_bare_check_categories_fail(self) -> None:
        examples = (
            "A lint rule fails when the forbidden import returns.",
            "A smoke check covers the provider boundary before live calls.",
            "A smoke check `provider boundary` covers provider behavior.",
            "A drift check rejects the stale generated path.",
            "A drift check `generated docs` rejects stale docs.",
            "A CI gate catches this before merge.",
            "A CI gate `main` catches this before merge.",
            "A manual review point checks the provider contract.",
            "A manual review point `provider contract` checks the contract.",
        )
        for index, example in enumerate(examples, start=1):
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.create_valid_reference_paths(root)
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            example,
                        ),
                        f"000{index}-example.md",
                    )

                    result = self.run_checker(root)

                    self.assertIn("detection/prevention section must name", result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_concrete_check_categories_pass(self) -> None:
        examples = (
            "Lint rule `no-restricted-imports` fails on direct route imports.",
            "Smoke check `npm run smoke:tago` covers the provider boundary.",
            "Drift check `python scripts/check_docs_drift.py` rejects stale paths.",
            "CI gate `.github/workflows/harness-check.yml` runs before merge.",
            (
                "Manual review point `docs/checklists/external-api-work.md "
                "Provider Boundary Fixtures` checks the provider contract."
            ),
            "Provider boundary fixture `fixtures/tago-nodeid.json` covers casing.",
        )
        for index, example in enumerate(examples, start=1):
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.create_valid_reference_paths(root)
                    if "npm run smoke:tago" in example:
                        self.write_package_json(
                            root,
                            {"smoke:tago": "node scripts/smoke-tago.mjs"},
                        )
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            example,
                        ),
                        f"000{index}-example.md",
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_referenced_local_paths_must_exist(self) -> None:
        examples = (
            "tests/missing_provider_contract.py",
            "fixtures/missing-provider.json",
            "scripts/missing_smoke.py",
            ".github/workflows/missing-check.yml",
            "docs/checklists/missing-review.md",
        )
        for index, reference in enumerate(examples, start=1):
            with self.subTest(reference=reference):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            f"`{reference}` fails if the bug path returns.",
                        ),
                        f"000{index}-example.md",
                    )

                    result = self.run_checker(root)

                    self.assertIn(
                        "references missing local path",
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_concrete_commands_pass(self) -> None:
        examples = (
            "`npm run test:planner` fails when the provider casing regresses.",
            "`make check` runs the regression suite.",
            "`just verify` runs the harness gate.",
            "`python -m unittest tests.test_provider_contract` covers the boundary.",
            "`mvn test` runs the Maven regression suite.",
            "`./mvnw verify` runs the Maven wrapper regression suite.",
            "`.\\mvnw.cmd verify` runs the Windows Maven wrapper regression suite.",
            "`gradle test` runs the Gradle regression suite.",
            "`./gradlew check` runs the Gradle wrapper regression suite.",
            "`.\\gradlew.bat check` runs the Windows Gradle wrapper regression suite.",
            "`go test ./...` runs the Go regression suite.",
        )
        for index, example in enumerate(examples, start=1):
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    if "npm run test:planner" in example:
                        self.write_package_json(
                            root,
                            {"test:planner": "node --test planner.test.mjs"},
                        )
                    if "make check" in example:
                        self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
                    if "just verify" in example:
                        self.write_justfile(root, "verify:\n    python3 -m unittest\n")
                    if "`mvn test`" in example:
                        self.write_maven_project(root)
                    if "`./mvnw verify`" in example:
                        self.write_maven_project(root, with_wrapper=True)
                    if "`.\\mvnw.cmd verify`" in example:
                        self.write_maven_project(
                            root,
                            with_wrapper=True,
                            wrapper_name="mvnw.cmd",
                        )
                    if "`gradle test`" in example:
                        self.write_gradle_project(root)
                    if "`./gradlew check`" in example:
                        self.write_gradle_project(root, with_wrapper=True)
                    if "`.\\gradlew.bat check`" in example:
                        self.write_gradle_project(
                            root,
                            with_wrapper=True,
                            wrapper_name="gradlew.bat",
                        )
                    if "`go test ./...`" in example:
                        self.write_go_project(root)
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            example,
                        ),
                        f"000{index}-example.md",
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_make_and_just_commands_allow_terminal_punctuation(self) -> None:
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
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            command,
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_package_manager_run_script_allows_terminal_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_package_json(
                root,
                {"test:planner": "node --test planner.test.mjs"},
            )
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "npm run test:planner.",
                ),
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_maven_gradle_go_commands_allow_terminal_punctuation(self) -> None:
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
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            command,
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_package_manager_run_script_managers_use_root_scripts(self) -> None:
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
                    self.write_package_json(
                        root,
                        {"test:planner": "node --test planner.test.mjs"},
                    )
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            example,
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_package_manager_run_script_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_package_json(root, {"test:other": "node --test other.test.mjs"})
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`npm run test:planner` fails when the provider casing regresses.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "package-manager command references missing package.json script: "
                "npm run test:planner",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_package_manager_run_script_requires_root_package_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested_package = root / "packages" / "app"
            nested_package.mkdir(parents=True)
            self.write_package_json(
                nested_package,
                {"test:planner": "node --test planner.test.mjs"},
            )
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`npm run test:planner` fails when the provider casing regresses.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "package-manager command references missing package.json script: "
                "npm run test:planner",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_make_command_target_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_makefile(root, "other:\n\tpython3 -m unittest\n")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`make check` runs the regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "make command references missing Makefile target: make check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_make_command_allows_leading_variable_assignments(self) -> None:
        examples = (
            "make ENV=ci check",
            "make PYTHON=python3.11 check",
        )
        for command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            f"`{command}` runs the regression suite.",
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertEqual("", result.stdout)
                    self.assertEqual(0, result.returncode)

    def test_make_variable_assignment_without_target_is_not_concrete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`make ENV=ci` does not name a check target.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn("detection/prevention section must name", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_make_command_uses_gnu_makefile_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "GNUmakefile").write_text(
                "other:\n\tpython3 -m unittest\n",
                encoding="utf-8",
            )
            self.write_makefile(root, "check:\n\tpython3 -m unittest\n")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`make check` runs the regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "make command references missing Makefile target: make check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_just_command_recipe_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_justfile(root, "other:\n    python3 -m unittest\n")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`just verify` runs the harness gate.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "just command references missing justfile recipe: just verify",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_maven_command_requires_pom(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`mvn test` runs the Maven regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "maven command references missing pom.xml: mvn test",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_maven_wrapper_command_requires_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_maven_project(root)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`./mvnw verify` runs the Maven wrapper regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "maven wrapper command references missing wrapper: ./mvnw verify",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_maven_wrapper_command_requires_matching_wrapper_flavor(self) -> None:
        examples = (
            ("./mvnw verify", "mvnw.cmd", "./mvnw verify"),
            (".\\mvnw.cmd verify", "mvnw", ".\\mvnw.cmd verify"),
        )
        for command, existing_wrapper, expected_command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_maven_project(
                        root,
                        with_wrapper=True,
                        wrapper_name=existing_wrapper,
                    )
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            f"`{command}` runs the Maven wrapper regression suite.",
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertIn(
                        (
                            "maven wrapper command references missing wrapper: "
                            f"{expected_command}"
                        ),
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_gradle_command_requires_build_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`gradle test` runs the Gradle regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "gradle command references missing build file: gradle test",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_gradle_wrapper_command_requires_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_gradle_project(root)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`./gradlew check` runs the Gradle wrapper regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "gradle wrapper command references missing wrapper: ./gradlew check",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_gradle_wrapper_command_requires_matching_wrapper_flavor(self) -> None:
        examples = (
            ("./gradlew check", "gradlew.bat", "./gradlew check"),
            (".\\gradlew.bat check", "gradlew", ".\\gradlew.bat check"),
        )
        for command, existing_wrapper, expected_command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_gradle_project(
                        root,
                        with_wrapper=True,
                        wrapper_name=existing_wrapper,
                    )
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            f"`{command}` runs the Gradle wrapper regression suite.",
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertIn(
                        (
                            "gradle wrapper command references missing wrapper: "
                            f"{expected_command}"
                        ),
                        result.stdout,
                    )
                    self.assertEqual(1, result.returncode)

    def test_go_command_requires_go_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`go test ./...` runs the Go regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "go command references missing go.mod: go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_capitalized_go_command_requires_go_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`Go test ./...` runs the Go regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "go command references missing go.mod: Go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_windows_subpath_wrappers_are_not_root_wrapper_commands(self) -> None:
        examples = (
            "tools\\mvnw.cmd verify",
            "tools\\gradlew.bat check",
        )
        for command in examples:
            with self.subTest(command=command):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            f"`{command}` is not a root wrapper command.",
                        ),
                    )

                    result = self.run_checker(root)

                    self.assertIn(
                        "detection/prevention section must name",
                        result.stdout,
                    )
                    self.assertNotIn("wrapper command references", result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_go_command_does_not_count_vendor_only_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.touch_local_path(root, "vendor/example.com/lib/lib.go")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`go test ./...` runs the Go regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "go command references missing go.mod: go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_go_command_does_not_count_source_only_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.touch_local_path(root, "cmd/app/main.go")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`go test ./...` runs the Go regression suite.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn(
                "go command references missing go.mod: go test ./...",
                result.stdout,
            )
            self.assertEqual(1, result.returncode)

    def test_valid_existing_path_may_include_planned_word(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.touch_local_path(root, "tests/planned-route.test.ts")
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "`tests/planned-route.test.ts` fails if the bug path returns.",
                ),
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_no_check_practical_requires_blocker_and_future_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    "No check is practical.",
                ),
            )

            result = self.run_checker(root)

            self.assertIn("detection/prevention section must name", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_no_check_practical_requires_concrete_blocker_and_future_signal(
        self,
    ) -> None:
        examples = (
            "No check is practical because future review may happen.",
            (
                "No check is practical because this is external behavior; "
                "revisit when some process is available."
            )
        )
        for index, example in enumerate(examples, start=1):
            with self.subTest(example=example):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self.write_record(
                        root,
                        VALID_RECORD.replace(
                            "`tests/test_example.py` fails if the bug path returns.",
                            example,
                        ),
                        f"000{index}-example.md",
                    )

                    result = self.run_checker(root)

                    self.assertIn("detection/prevention section must name", result.stdout)
                    self.assertEqual(1, result.returncode)

    def test_no_check_practical_with_blocker_and_future_signal_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "`tests/test_example.py` fails if the bug path returns.",
                    (
                        "No check is practical because the provider has no stable "
                        "fixture format yet; revisit when a stable sandbox is available."
                    ),
                ),
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_only_canonical_template_record_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(root, "# Template\n\nTODO\n", name="000-template.md")

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_real_failure_record_with_template_in_name_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_record(
                root,
                VALID_RECORD.replace(
                    "## Detection Or Prevention Check\n\n"
                    "`tests/test_example.py` fails if the bug path returns.\n\n",
                    "",
                ),
                name="0006-template-rendering-failed.md",
            )

            result = self.run_checker(root)

            self.assertIn("missing required section", result.stdout)
            self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()

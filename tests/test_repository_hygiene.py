from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    def test_python_cache_files_are_not_tracked(self) -> None:
        if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
            self.skipTest("git repository is not available")

        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        tracked_cache_files = [
            path
            for path in result.stdout.splitlines()
            if "__pycache__/" in path.replace("\\", "/") or path.endswith(".pyc")
        ]

        self.assertEqual([], tracked_cache_files)

    def test_fastapi_check_harness_excludes_generated_profile_snippets(self) -> None:
        check_harness = (
            REPO_ROOT / "templates" / "profiles" / "fastapi" / "check_harness.py"
        )
        text = check_harness.read_text(encoding="utf-8")

        self.assertIn("--exclude", text)
        self.assertIn("docs", text)
        self.assertIn("harness", text)

    def test_effectiveness_measurement_is_wired_into_adoption_flow(self) -> None:
        adoption_report = (
            REPO_ROOT / "docs" / "templates" / "adoption-report.md"
        ).read_text(encoding="utf-8")
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        adoption_prompt = (
            REPO_ROOT / "docs" / "prompts" / "apply-to-target-repo.md"
        ).read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Effectiveness Measurement Plan", adoption_report)
        self.assertIn("Do not leave this section as TODO", adoption_report)
        self.assertIn("Baseline available", adoption_report)
        self.assertIn("Primary metric", adoption_report)
        self.assertIn("Results location", adoption_report)
        self.assertIn("effectiveness measurement plan", agent_template)
        self.assertIn("Effectiveness Measurement Plan", adoption_prompt)
        self.assertIn("They do not prove", readme)
        self.assertIn("docs/evaluation.md", readme)

    def test_failure_memory_is_required_for_fixed_harness_failures(self) -> None:
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        update_command = (REPO_ROOT / "commands" / "harness-update.md").read_text(
            encoding="utf-8"
        )
        adoption_report = (
            REPO_ROOT / "docs" / "templates" / "adoption-report.md"
        ).read_text(encoding="utf-8")

        for text in (root_agents, agent_template, update_command):
            self.assertIn("failed harness check", text)
            self.assertIn("cross-environment mismatch", text)
            self.assertIn("docs/failures/*.md", text)

        self.assertIn("## Failure Memory", adoption_report)
        self.assertIn("Recorded:", update_command)
        self.assertIn("Skipped:", update_command)

    def test_commit_and_pr_rules_are_wired_into_agent_instructions(self) -> None:
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )

        for text in (root_agents, agent_template):
            self.assertIn("## Commit And PR Rules", text)
            self.assertIn("staged diff", text)
            self.assertIn("checks before committing", text)
            self.assertIn("Conventional Commits", text)
            self.assertIn("feat:", text)
            self.assertIn("chore:", text)
            self.assertIn("If no convention exists", text)
            self.assertIn("changed files", text)
            self.assertIn("remaining risks", text)

    def test_harness_update_command_is_documented_and_linked(self) -> None:
        update_command = (REPO_ROOT / "commands" / "harness-update.md").read_text(
            encoding="utf-8"
        )
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        component_map = (REPO_ROOT / "docs" / "component-map.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(".harness/source.json", update_command)
        self.assertIn("git -C harness-starter-kit pull --ff-only origin main", update_command)
        self.assertIn("dirty", update_command)
        self.assertIn("blindly overwrite", update_command)
        self.assertIn("Harness Update Report", update_command)

        for text in (root_agents, readme, component_map):
            self.assertIn("/harness update", text)
            self.assertIn("commands/harness-update.md", text)

    def test_harness_refresh_command_is_documented_and_linked(self) -> None:
        refresh_command = (
            REPO_ROOT / "commands" / "harness-refresh.md"
        ).read_text(encoding="utf-8")
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        adoption_workflow = (
            REPO_ROOT / "docs" / "adoption-workflow.md"
        ).read_text(encoding="utf-8")
        component_map = (REPO_ROOT / "docs" / "component-map.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Harness Refresh Report", refresh_command)
        self.assertIn("keep", refresh_command)
        self.assertIn("update", refresh_command)
        self.assertIn("merge", refresh_command)
        self.assertIn("archive/delete candidate", refresh_command)
        self.assertIn("manual review", refresh_command)
        self.assertIn("explicit user approval", refresh_command)

        for text in (root_agents, readme, adoption_workflow, component_map):
            self.assertIn("/harness refresh", text)
            self.assertIn("commands/harness-refresh.md", text)

    def test_profile_reference_paths_distinguish_clone_from_installer_output(
        self,
    ) -> None:
        adoption_workflow = (REPO_ROOT / "docs" / "adoption-workflow.md").read_text(
            encoding="utf-8"
        )
        profile_checklist = (
            REPO_ROOT / "docs" / "checklists" / "profile-absorption.md"
        ).read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        for text in (adoption_workflow, profile_checklist, readme):
            self.assertIn("harness-starter-kit/templates/profiles/<profile>", text)
            self.assertIn("docs/harness/profiles/<profile>", text)

        self.assertIn("cloned kit", adoption_workflow)
        self.assertIn("optional installer", readme)

    def test_lifecycle_pilot_results_are_documented_without_effectiveness_claims(
        self,
    ) -> None:
        pilot_results = (
            REPO_ROOT / "docs" / "examples" / "lifecycle-pilot-results.md"
        ).read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Blank to Django", pilot_results)
        self.assertIn("Blank to Next.js", pilot_results)
        self.assertIn("not reduced agent error rates", pilot_results)
        self.assertIn("docs/examples/lifecycle-pilot-results.md", readme)

    def test_readmes_link_to_split_detail_docs(self) -> None:
        validation = REPO_ROOT / "docs" / "validation.md"
        self.assertTrue(validation.exists())
        validation_text = validation.read_text(encoding="utf-8")
        self.assertIn("Fixture Smoke Tests", validation_text)
        self.assertIn("Lifecycle Pilots", validation_text)
        self.assertIn("They do not prove", validation_text)

        for filename in (
            "README.md",
            "README.ko.md",
            "README.ja.md",
            "README.zh-CN.md",
        ):
            with self.subTest(readme=filename):
                text = (REPO_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("docs/adoption-workflow.md", text)
                self.assertIn("docs/prompts/apply-to-target-repo.md", text)
                self.assertIn("docs/validation.md", text)
                self.assertIn("docs/evaluation.md", text)
                self.assertIn("/harness update", text)
                self.assertIn("/harness refresh", text)


if __name__ == "__main__":
    unittest.main()

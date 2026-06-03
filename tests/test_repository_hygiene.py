from __future__ import annotations

import json
import re
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

    def test_effectiveness_plan_check_matches_generic_template(self) -> None:
        root_script = (
            REPO_ROOT / "scripts" / "check_effectiveness_plan.py"
        ).read_text(encoding="utf-8")
        generic_script = (
            REPO_ROOT
            / "templates"
            / "generic"
            / "scripts"
            / "check_effectiveness_plan.py"
        ).read_text(encoding="utf-8")

        self.assertEqual(root_script, generic_script)

    def test_failure_memory_check_matches_generic_template(self) -> None:
        root_script = (
            REPO_ROOT / "scripts" / "check_failure_memory.py"
        ).read_text(encoding="utf-8")
        generic_script = (
            REPO_ROOT
            / "templates"
            / "generic"
            / "scripts"
            / "check_failure_memory.py"
        ).read_text(encoding="utf-8")

        self.assertEqual(root_script, generic_script)

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
        adoption_workflow = (
            REPO_ROOT / "docs" / "adoption-workflow.md"
        ).read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Effectiveness Measurement Plan", adoption_report)
        self.assertIn("Do not leave this section as TODO", adoption_report)
        self.assertIn("Baseline available", adoption_report)
        self.assertIn("Primary metric", adoption_report)
        self.assertIn("Results location", adoption_report)
        self.assertIn("Task outcome records location", adoption_report)
        self.assertIn("effectiveness measurement plan", agent_template)
        self.assertIn("Effectiveness Measurement Plan", adoption_prompt)
        self.assertIn("task-outcome.yaml", adoption_prompt)
        self.assertIn("task-outcome.yaml", adoption_workflow)
        self.assertIn("docs/effectiveness/task-outcomes", adoption_report)
        self.assertIn("They do not prove", readme)
        self.assertIn("docs/evaluation.md", readme)

    def test_theory_model_separates_health_from_effectiveness(self) -> None:
        theory = (REPO_ROOT / "docs" / "theory" / "harness-engineering.md").read_text(
            encoding="utf-8"
        )
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        overview = (REPO_ROOT / "docs" / "overview.md").read_text(encoding="utf-8")
        evaluation = (REPO_ROOT / "docs" / "evaluation.md").read_text(
            encoding="utf-8"
        )
        rubric = (
            REPO_ROOT / "docs" / "scoring" / "harness-score-rubric.md"
        ).read_text(encoding="utf-8")
        doctor_command = (REPO_ROOT / "commands" / "harness-doctor.md").read_text(
            encoding="utf-8"
        )
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        task_outcome = (
            REPO_ROOT / "docs" / "templates" / "task-outcome.yaml"
        ).read_text(encoding="utf-8")

        for text in (theory, readme, overview):
            self.assertIn(
                "Instructions + Constraints + Feedback + Memory + Evaluation + Governance",
                text,
            )

        self.assertIn("Harness health", theory)
        self.assertIn("Agent effectiveness", theory)
        self.assertIn("operational model", theory)
        self.assertIn("## How To Use This Model", theory)
        self.assertIn("Add or update", theory)
        self.assertIn("prefer enforceable constraints and feedback", theory)
        self.assertIn("not justify adding every artifact", theory)
        self.assertIn("does not prove", theory)
        self.assertIn("Harness Doctor", evaluation)
        self.assertIn("repository ref", evaluation)
        self.assertIn("verification command", evaluation)
        self.assertIn("task-outcome.yaml", evaluation)
        self.assertIn("agent effectiveness score", rubric)
        self.assertIn("Score Scope", rubric)
        self.assertIn("not proof of agent effectiveness", doctor_command)
        self.assertIn("Non-Scored Manual Review", doctor_command)
        self.assertIn("governance maturity", doctor_command)
        self.assertIn("docs/theory/", root_agents)
        self.assertIn("docs/effectiveness/task-outcomes", evaluation)
        self.assertIn("repository_ref", task_outcome)
        self.assertIn("prompt_ref", task_outcome)
        self.assertIn("run_id", task_outcome)
        self.assertIn("reviewer", task_outcome)
        self.assertIn("verification_command", task_outcome)
        self.assertIn("harness_doctor_score", task_outcome)
        self.assertIn("not effectiveness proof", task_outcome)
        self.assertIn("docs/effectiveness/task-outcomes", task_outcome)

    def test_failure_memory_is_required_for_fixed_harness_failures(self) -> None:
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        adoption_workflow = (
            REPO_ROOT / "docs" / "adoption-workflow.md"
        ).read_text(encoding="utf-8")
        adoption_prompt = (
            REPO_ROOT / "docs" / "prompts" / "apply-to-target-repo.md"
        ).read_text(encoding="utf-8")
        update_command = (REPO_ROOT / "commands" / "harness-update.md").read_text(
            encoding="utf-8"
        )
        adoption_report = (
            REPO_ROOT / "docs" / "templates" / "adoption-report.md"
        ).read_text(encoding="utf-8")
        failure_template = (
            REPO_ROOT / "docs" / "failures" / "000-template.md"
        ).read_text(encoding="utf-8")
        generic_failure_template = (
            REPO_ROOT / "templates" / "generic" / "docs" / "failures" / "000-template.md"
        ).read_text(encoding="utf-8")

        failure_rule_texts = (
            root_agents,
            agent_template,
            adoption_workflow,
            adoption_prompt,
            update_command,
        )
        for text in failure_rule_texts:
            normalized = " ".join(text.split())
            self.assertIn("user-visible runtime failure", normalized)
            self.assertIn("high-risk bug path", normalized)
            self.assertIn("5xx", normalized)
            self.assertIn("security or permission bug", normalized)
            self.assertIn("data-loss risk", normalized)
            self.assertIn("failed harness check", normalized)
            self.assertIn("previously identified bug path", normalized)
            self.assertIn("cross-environment mismatch", normalized)
            self.assertIn("already covered by an existing failure note", normalized)
            self.assertIn("docs/failures/*.md", normalized)

        self.assertIn("## Failure Memory", adoption_report)
        normalized_adoption_report = " ".join(adoption_report.split())
        self.assertIn("user-visible runtime failures", normalized_adoption_report)
        self.assertIn("high-risk bug paths", normalized_adoption_report)
        self.assertIn("purely transient", normalized_adoption_report)
        self.assertIn("existing failure note", normalized_adoption_report)
        self.assertIn("Recorded:", update_command)
        self.assertIn("Skipped:", update_command)

        for text in (failure_template, generic_failure_template):
            self.assertIn("Failure Or Failed Approach Title", text)
            self.assertIn("## Date Observed", text)
            self.assertIn("## Failure Type", text)
            self.assertIn("## What Happened Or Was Tried", text)
            self.assertIn("## Detection Or Prevention Check", text)
            self.assertIn("Runtime failure", text)
            self.assertIn("5xx response", text)
            self.assertIn("Security, permission, or data-loss risk", text)
            self.assertIn("regression test", text)
            self.assertIn("fixture", text)
            self.assertIn("smoke check", text)
            self.assertIn("drift check", text)

        for text in (root_agents, agent_template, adoption_workflow, adoption_prompt):
            normalized = " ".join(text.split())
            self.assertIn("regression test", normalized)
            self.assertIn("fixture", normalized)
            self.assertIn("smoke check", normalized)
            self.assertIn("manual review point", normalized)

        self.assertIn("Detection or prevention check", adoption_report)
        self.assertIn("Detection/prevention check", update_command)
        self.assertIn("check_failure_memory.py", agent_template)
        self.assertIn("check_failure_memory.py", adoption_prompt)

    def test_failure_records_name_detection_or_prevention_check(self) -> None:
        failure_records = sorted((REPO_ROOT / "docs" / "failures").glob("*.md"))
        checked_records: list[str] = []
        required_sections = (
            "## Date Observed",
            "## Failure Type",
            "## Goal",
            "## What Happened Or Was Tried",
            "## Why It Failed",
            "## Current Replacement",
            "## Detection Or Prevention Check",
            "## Agent Guidance",
        )
        concrete_check_patterns = (
            r"\b(?:tests?|specs?|fixtures?|scripts?)/[^\s,.;)]+",
            r"`?\.github/workflows/[^\s,.;)`]+`?",
            r"\b(?:npm|pnpm|yarn|bun)\s+run\s+[\w:./-]+",
            r"\b(?:make|just)\s+[\w:./-]+",
            r"\bpython3?\s+(?:-m\s+[\w.:-]+|scripts?/[^\s,.;)]+)",
            r"\bpytest\s+(?:-[\w-]+|tests?/[^\s,.;)]+|[\w/.-]+)",
            r"\b(?:vitest|jest|ruff|mypy|eslint)\s+[\w/.:@-]+",
            r"\blint rule\s+`?[\w@./]+[-:/][\w@./:-]+`?",
            r"\bci gate\s+`?\.github/workflows/[^\s,.;)`]+`?",
            r"\bmanual review point\s+`?docs/checklists/[^\s,.;)`]+",
            r"\bfixture\s+`?(?:tests?|fixtures?)/[^\s,.;)`]+`?",
        )
        no_check_blocker_patterns = (
            (
                r"\bbecause\b.{8,}\b(?:blocked|cannot|requires|depends on|"
                r"no stable|not available|impractical|credential|quota|"
                r"network|hardware|permission|sandbox|fixture|manual-only|"
                r"nondeterministic)\b"
            ),
        )
        no_check_future_signal_patterns = (
            (
                r"\brevisit\s+when\s+.{0,80}\b(?:stable sandbox|sandbox|"
                r"fixture|provider contract|api contract|schema|endpoint|"
                r"mock|emulator|credential|quota|permission|hardware|ci|"
                r"workflow|tooling)\b"
            ),
            (
                r"\breview\s+when\s+.{0,80}\b(?:stable sandbox|sandbox|"
                r"fixture|provider contract|api contract|schema|endpoint|"
                r"mock|emulator|credential|quota|permission|hardware|ci|"
                r"workflow|tooling)\b"
            ),
            (
                r"\btrigger\s+review\s+when\s+.{0,80}\b(?:stable sandbox|"
                r"sandbox|fixture|provider contract|api contract|schema|"
                r"endpoint|mock|emulator|credential|quota|permission|"
                r"hardware|ci|workflow|tooling)\b"
            ),
            (
                r"\badd\s+(?:a\s+)?check\s+when\s+.{0,80}\b(?:stable "
                r"sandbox|sandbox|fixture|provider contract|api contract|"
                r"schema|endpoint|mock|emulator|credential|quota|permission|"
                r"hardware|ci|workflow|tooling)\b"
            ),
            (
                r"\bwhen\s+.{0,80}\b(?:stable sandbox|sandbox|fixture|"
                r"provider contract|api contract|schema|endpoint|mock|"
                r"emulator|credential|quota|permission|hardware|ci|workflow|"
                r"tooling)\b.{0,40}\s+(?:is|are|becomes|become)\s+"
                r"(?:available|stable|supported)"
            ),
        )
        rejected_phrases = (
            "no test has been added",
            "no regression test",
            "no fixture",
            "not added yet",
            "todo",
        )

        for path in failure_records:
            if path.name in ("000-template.md", "README.md"):
                continue

            text = path.read_text(encoding="utf-8")
            for section_name in required_sections:
                self.assertIn(section_name, text, path.name)

            section = text.split("## Detection Or Prevention Check", 1)[1].split(
                "\n## ",
                1,
            )[0]
            normalized = " ".join(section.lower().split())
            self.assertFalse(
                any(phrase in normalized for phrase in rejected_phrases),
                f"{path.name} uses non-committal detection/prevention prose",
            )
            self.assertTrue(
                any(
                    re.search(pattern, normalized)
                    for pattern in concrete_check_patterns
                )
                or (
                    "no check is practical" in normalized
                    and any(
                        re.search(pattern, normalized)
                        for pattern in no_check_blocker_patterns
                    )
                    and any(
                        re.search(pattern, normalized)
                        for pattern in no_check_future_signal_patterns
                    )
                ),
                f"{path.name} does not name a detection/prevention check",
            )
            checked_records.append(path.name)

        malformed_section = "No test has been added yet for tests/provider-contract.test.ts."
        self.assertFalse(
            any(
                re.search(pattern, malformed_section.lower())
                for pattern in concrete_check_patterns
            )
            and not any(phrase in malformed_section.lower() for phrase in rejected_phrases)
        )
        for bare_section in (
            "A lint rule fails when the bug returns.",
            "A smoke check covers the provider boundary.",
            "A smoke check `provider boundary` covers the provider boundary.",
            "A drift check rejects stale docs.",
            "A drift check `generated docs` rejects stale docs.",
            "A CI gate catches the failure.",
            "A CI gate `main` catches the failure.",
            "A manual review point checks the contract.",
            "A manual review point `provider contract` checks the contract.",
        ):
            self.assertFalse(
                any(
                    re.search(pattern, bare_section.lower())
                    for pattern in concrete_check_patterns
                ),
                bare_section,
            )

        self.assertIn(
            "0005-failure-memory-was-not-linked-to-regression-checks.md",
            checked_records,
        )

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

    def test_decision_memory_gate_is_visible_in_generic_completion(self) -> None:
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(agent_template.split())

        self.assertIn("handle decision memory explicitly", normalized)
        self.assertIn("docs/decisions/*.md", normalized)
        self.assertIn("existing ADR", normalized)
        self.assertIn("docs/domain", normalized)
        self.assertIn("does not replace a decision record", normalized)
        self.assertIn("Decision docs:", normalized)
        self.assertIn("API/mock boundary", normalized)
        self.assertIn("input contract", normalized)
        self.assertIn("input semantics", normalized)
        self.assertIn("state normalization", normalized)
        self.assertIn("fallback policy", normalized)
        self.assertIn("displayed decision criteria", normalized)

    def test_decision_memory_warning_script_is_wired_into_harness(self) -> None:
        script = REPO_ROOT / "scripts" / "check_decision_memory.py"
        generic_script = (
            REPO_ROOT / "templates" / "generic" / "scripts" / "check_decision_memory.py"
        )
        rules = REPO_ROOT / ".harness" / "decision-memory-rules.json"
        generic_rules = (
            REPO_ROOT
            / "templates"
            / "generic"
            / ".harness"
            / "decision-memory-rules.json"
        )
        component_map = (REPO_ROOT / "docs" / "component-map.md").read_text(
            encoding="utf-8"
        )
        validation = (REPO_ROOT / "docs" / "validation.md").read_text(
            encoding="utf-8"
        )
        contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        root_workflow = (
            REPO_ROOT / ".github" / "workflows" / "harness-check.yml"
        ).read_text(encoding="utf-8")
        generic_workflow = (
            REPO_ROOT
            / "templates"
            / "generic"
            / ".github"
            / "workflows"
            / "harness-check.yml"
        ).read_text(encoding="utf-8")
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        adoption_prompt = (
            REPO_ROOT / "docs" / "prompts" / "apply-to-target-repo.md"
        ).read_text(encoding="utf-8")

        for path in (script, generic_script, rules, generic_rules):
            self.assertTrue(path.exists(), path)

        script_text = script.read_text(encoding="utf-8")
        generic_text = generic_script.read_text(encoding="utf-8")
        self.assertEqual(script_text, generic_text)
        root_rules = json.loads(rules.read_text(encoding="utf-8"))
        template_rules = json.loads(generic_rules.read_text(encoding="utf-8"))
        self.assertIn(".github/workflows/**", root_rules["watched_paths"])
        self.assertIn("AGENTS.md", root_rules["watched_paths"])
        self.assertIn("scripts/**", root_rules["watched_paths"])
        self.assertIn("templates/**", root_rules["watched_paths"])
        self.assertIn("commands/**", root_rules["watched_paths"])
        self.assertIn("src/**", template_rules["watched_paths"])
        self.assertIn("scripts/**", template_rules["ignored_paths"])
        self.assertNotEqual(root_rules, template_rules)
        self.assertIn("--fail-on-warning", script_text)
        self.assertIn("Decision memory review warning", script_text)
        self.assertIn("input semantics", script_text)
        self.assertIn("displayed", script_text)
        self.assertIn("decision criteria", script_text)

        for text in (component_map, validation, agent_template, adoption_prompt):
            self.assertIn("check_decision_memory.py", text)

        failure_script = REPO_ROOT / "scripts" / "check_failure_memory.py"
        generic_failure_script = (
            REPO_ROOT
            / "templates"
            / "generic"
            / "scripts"
            / "check_failure_memory.py"
        )
        self.assertTrue(failure_script.exists())
        self.assertTrue(generic_failure_script.exists())
        self.assertEqual(
            failure_script.read_text(encoding="utf-8"),
            generic_failure_script.read_text(encoding="utf-8"),
        )
        for text in (component_map, validation, agent_template, adoption_prompt):
            self.assertIn("check_failure_memory.py", text)
        self.assertIn("check_failure_memory.py", contributing)
        self.assertIn("python scripts/check_failure_memory.py", contributing)

        for text in (root_workflow, generic_workflow):
            self.assertIn("fetch-depth: 0", text)
            self.assertIn("github.event.pull_request.base.sha", text)
            self.assertIn("--base", text)
            self.assertIn("local smoke", text)
            self.assertIn("check_failure_memory.py", text)

    def test_ui_profiles_call_out_decision_memory_triggers(self) -> None:
        for relative in (
            "templates/profiles/typescript/README.md",
            "templates/profiles/nextjs/README.md",
            "templates/profiles/react/README.md",
            "templates/profiles/vue/README.md",
        ):
            with self.subTest(profile=relative):
                text = (REPO_ROOT / relative).read_text(encoding="utf-8")
                normalized = " ".join(text.split())
                self.assertIn("input semantics", normalized)
                self.assertIn("fallback behavior", normalized)
                self.assertIn("displayed decision criteria", normalized)

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
        normalized_update = " ".join(update_command.lower().split())
        self.assertIn("pre-existing target changes", normalized_update)
        self.assertIn("latest confirmed kit commit", normalized_update)
        self.assertIn("source tracking", normalized_update)
        self.assertIn("separating source tracking from target file mutation", normalized_update)
        self.assertIn("do not patch target files that were already dirty", normalized_update)
        self.assertIn("Deferred target patches", update_command)
        self.assertIn("blindly overwrite", update_command)
        self.assertIn("Harness Update Report", update_command)

        for text in (root_agents, readme, component_map):
            self.assertIn("/harness update", text)
            self.assertIn("commands/harness-update.md", text)

    def test_readme_clarifies_harness_commands_are_prompt_conventions(self) -> None:
        for filename in (
            "README.md",
            "README.ko.md",
            "README.ja.md",
            "README.zh-CN.md",
        ):
            with self.subTest(readme=filename):
                readme = (REPO_ROOT / filename).read_text(encoding="utf-8")
                normalized = " ".join(readme.split())

                self.assertIn("/harness ...", normalized)
                self.assertIn("prompt convention", normalized)
                self.assertIn("editor command", normalized)
                self.assertIn("command palette", normalized)

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

    def test_harness_review_command_is_documented_and_linked(self) -> None:
        review_command = (
            REPO_ROOT / "commands" / "harness-review.md"
        ).read_text(encoding="utf-8")
        review_template = (
            REPO_ROOT / "docs" / "templates" / "harness-review-report.md"
        )
        review_example = REPO_ROOT / "docs" / "examples" / "harness-review-report.md"
        root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        component_map = (REPO_ROOT / "docs" / "component-map.md").read_text(
            encoding="utf-8"
        )
        adoption_prompt = (
            REPO_ROOT / "docs" / "prompts" / "apply-to-target-repo.md"
        ).read_text(encoding="utf-8")
        maintenance_checklist = (
            REPO_ROOT / "docs" / "checklists" / "harness-review.md"
        ).read_text(encoding="utf-8")

        self.assertTrue(review_template.exists())
        self.assertTrue(review_example.exists())

        normalized_command = " ".join(review_command.split())
        for phrase in (
            "diagnostic by default",
            "explicitly asks",
            "opposing harness-engineering perspective",
            "source of truth",
            "unnecessary automation",
            "templates conservative",
            "durable memory",
            "validation",
            "checks",
            "Invocation Modes",
            "/harness review sub-agent",
            "explicit user permission",
            "explicit request",
            "multi-agent or subagent tools are available",
            "available and permitted by the active runtime and tool instructions",
            "read-only reviewer subagent",
            "parent or orchestrator agent",
            "Do not assess reviewer mode, fallback reason, or subagent availability.",
            "Return only review findings, missing checks, and risks.",
            "Do not produce a full Harness Review Report.",
            "Do not modify files.",
            "actual availability check and subagent spawn/wait result",
            "Do not trust or copy reviewer-mode, fallback-reason, or subagent-availability claims",
            "tool unavailable",
            "tool present but not permitted",
            "subagent call failed",
            "single-agent reviewer perspective",
            "fallback reason",
        ):
            self.assertIn(phrase, normalized_command)
        self.assertIn("Do not modify files", review_command)
        self.assertIn("runtime hooks", review_command)
        self.assertIn("pre-commit", review_command)
        self.assertIn("CI adapters", review_command)
        self.assertIn("installer automation", review_command)
        self.assertIn("runtime-specific subagent integration", review_command)
        self.assertIn("docs/checklists/harness-review.md", review_command)
        self.assertIn("current change set", review_command)
        self.assertIn("monthly or repeated mistake review", normalized_command)

        self.assertIn("Harness Maintenance Review Checklist", maintenance_checklist)
        self.assertIn("/harness review", maintenance_checklist)
        self.assertIn("current change set", maintenance_checklist)
        self.assertIn("periodic harness maintenance", maintenance_checklist)

        for text in (root_agents, readme, component_map, adoption_prompt):
            self.assertIn("/harness review", text)
            self.assertIn("/harness review sub-agent", text)
            self.assertIn("commands/harness-review.md", text)

        for name, text, specific_route, generic_route in (
            (
                "AGENTS.md",
                root_agents,
                "`/harness review sub-agent`",
                "`/harness review`:",
            ),
            (
                "README.md",
                readme,
                "If I ask for /harness review sub-agent",
                "If I ask for /harness review, use",
            ),
            (
                "docs/prompts/apply-to-target-repo.md",
                adoption_prompt,
                "If I ask for /harness review sub-agent",
                "If I ask for /harness review, use",
            ),
        ):
            with self.subTest(route_order=name):
                self.assertLess(
                    text.index(specific_route),
                    text.index(generic_route),
                )

        for filename in ("README.ko.md", "README.ja.md", "README.zh-CN.md"):
            with self.subTest(readme=filename):
                localized = (REPO_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("| `/harness review` |", localized)
                self.assertIn("/harness review sub-agent", localized)
                self.assertIn("commands/harness-review.md", localized)
                self.assertLess(
                    localized.index("If I ask for /harness review sub-agent"),
                    localized.index("If I ask for /harness review, use"),
                )

        template_text = review_template.read_text(encoding="utf-8")
        for section in (
            "## Reviewed Changes",
            "## Findings",
            "## Missing Checks",
            "## Durable Memory Assessment",
            "## Overreach Risk",
            "## Manual Decisions Needed",
            "## Recommended Follow-Up",
        ):
            self.assertIn(section, template_text)
        self.assertIn("Reviewer mode: TODO: subagent used | single-agent fallback", template_text)
        self.assertIn("Fallback reason: TODO: reason or none", template_text)
        self.assertIn("Invocation: TODO: /harness review | /harness review sub-agent", template_text)
        normalized_template = " ".join(template_text.split())
        self.assertIn("parent/orchestrator-owned", normalized_template)
        self.assertIn(
            "actual availability check and subagent spawn/wait result",
            normalized_template,
        )
        self.assertIn("not from subagent output", normalized_template)
        self.assertIn("Review timing", template_text)
        self.assertIn("pre-push", template_text)
        self.assertIn("does not apply fixes", template_text)
        self.assertIn("Decision-docs gate", template_text)
        self.assertIn("mock external-behavior boundary", normalized_template)
        self.assertIn("state classification", normalized_template)
        self.assertIn("product UX principle", normalized_template)
        self.assertIn("detection/prevention check", normalized_template)

        example_text = review_example.read_text(encoding="utf-8")
        normalized_example = " ".join(example_text.split())
        self.assertIn("actual spawn/wait result", normalized_example)
        self.assertIn("not from subagent output", normalized_example)
        self.assertIn("Review timing: pre-push", example_text)
        self.assertIn("Review timing: pre-commit", example_text)
        self.assertIn("Invocation: /harness review sub-agent", example_text)
        self.assertIn("Invocation: /harness review", example_text)
        self.assertIn("Reviewer mode: subagent used", example_text)
        self.assertIn("Fallback reason: none", example_text)
        self.assertIn("Reviewer mode: single-agent fallback", example_text)
        self.assertIn("tool present but not permitted", example_text)

        failure_memory = (
            REPO_ROOT
            / "docs"
            / "failures"
            / "0002-subagent-reviewer-mode-ownership.md"
        ).read_text(encoding="utf-8")
        normalized_failure_memory = " ".join(failure_memory.split())
        self.assertIn(
            "Reviewer mode: single-agent fallback",
            normalized_failure_memory,
        )
        self.assertIn("parent orchestrator", normalized_failure_memory)
        self.assertIn(
            "Do not copy those fields from subagent output",
            normalized_failure_memory,
        )

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
                self.assertIn("docs/theory/harness-engineering.md", text)
                self.assertIn("docs/validation.md", text)
                self.assertIn("docs/evaluation.md", text)
                self.assertIn("docs/templates/task-outcome.yaml", text)
                self.assertIn("/harness update", text)
                self.assertIn("/harness refresh", text)
                self.assertIn("/harness review", text)
                self.assertIn("commands/harness-review.md", text)

    def test_feedback_driven_practical_checklists_are_linked(self) -> None:
        checklist_paths = (
            "docs/checklists/external-api-work.md",
            "docs/checklists/decision-failure-memory.md",
            "docs/checklists/verification-scripts.md",
        )
        for relative in checklist_paths:
            with self.subTest(path=relative):
                self.assertTrue((REPO_ROOT / relative).exists())

        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        component_map = (REPO_ROOT / "docs" / "component-map.md").read_text(
            encoding="utf-8"
        )
        adoption_workflow = (
            REPO_ROOT / "docs" / "adoption-workflow.md"
        ).read_text(encoding="utf-8")
        adoption_prompt = (
            REPO_ROOT / "docs" / "prompts" / "apply-to-target-repo.md"
        ).read_text(encoding="utf-8")
        adoption_report = (
            REPO_ROOT / "docs" / "templates" / "adoption-report.md"
        ).read_text(encoding="utf-8")
        nextjs_example = (
            REPO_ROOT / "examples" / "nextjs-adoption-report.md"
        ).read_text(encoding="utf-8")
        external_api_checklist = (
            REPO_ROOT / "docs" / "checklists" / "external-api-work.md"
        ).read_text(encoding="utf-8")
        verification_scripts = (
            REPO_ROOT / "docs" / "checklists" / "verification-scripts.md"
        ).read_text(encoding="utf-8")
        lifecycle_pilots = (
            REPO_ROOT / "docs" / "examples" / "lifecycle-pilot-results.md"
        ).read_text(encoding="utf-8")
        nextjs_profile = (
            REPO_ROOT / "templates" / "profiles" / "nextjs" / "README.md"
        ).read_text(encoding="utf-8")
        nextjs_scripts = json.loads(
            (
                REPO_ROOT
                / "templates"
                / "profiles"
                / "nextjs"
                / "package-scripts.harness.json"
            ).read_text(encoding="utf-8")
        )["scripts"]

        for text in (readme, component_map, adoption_workflow, adoption_prompt):
            for relative in checklist_paths:
                self.assertIn(relative, text)

        external_api_report_fields = (
            "## External API Verification",
            "Required",
            "Boundary",
            "Live/mock mode",
            "Secret handling and redaction checked",
            "Empty or zero-result behavior",
            "Provider error handling",
            "Focused smoke command or fixture",
        )
        for phrase in external_api_report_fields:
            self.assertIn(phrase, adoption_report)
        for phrase in external_api_report_fields:
            self.assertIn(phrase, nextjs_example)

        normalized_nextjs = " ".join(nextjs_profile.split())
        self.assertIn("App Router Checklist", nextjs_profile)
        self.assertIn("route handlers", normalized_nextjs)
        self.assertIn("server components", normalized_nextjs)
        self.assertIn("env vars", normalized_nextjs)
        self.assertIn("zero-result", normalized_nextjs)
        self.assertIn("focused smoke script", normalized_nextjs)

        for script_name, script_command in nextjs_scripts.items():
            with self.subTest(script=script_name):
                self.assertIn(f'"{script_name}"', nextjs_profile)
                self.assertIn(script_command, nextjs_profile)

        self.assertIn("check:docs", nextjs_example)
        self.assertIn("check:structure", nextjs_example)
        self.assertIn("named axes", nextjs_example)
        self.assertIn("401 text/plain Unauthorized", external_api_checklist)
        self.assertIn("provider text-error", external_api_checklist)
        self.assertIn("Provider Boundary Fixtures", external_api_checklist)
        self.assertIn("Endpoint parameter contract", external_api_checklist)
        self.assertIn("nodeId", external_api_checklist)
        self.assertIn("nodeid", external_api_checklist)
        self.assertIn("service-key placement", external_api_checklist)
        self.assertIn("Endpoint parameter contract", adoption_report)
        self.assertIn("Provider boundary fixture", adoption_report)
        self.assertIn("Endpoint parameter contract", nextjs_example)
        self.assertIn("Provider boundary fixture", nextjs_example)
        self.assertIn("redactionChecked", verification_scripts)
        self.assertIn("emptyStateChecked", verification_scripts)
        self.assertIn("providerErrorChecked", verification_scripts)
        self.assertIn("parameter names", verification_scripts)
        self.assertIn("TodayBus External API Dogfood", lifecycle_pilots)

    def test_p1_feedback_requires_regression_links_and_pre_push_review(self) -> None:
        feedback_failure = (
            REPO_ROOT
            / "docs"
            / "failures"
            / "0005-failure-memory-was-not-linked-to-regression-checks.md"
        ).read_text(encoding="utf-8")
        feedback_decision = (
            REPO_ROOT
            / "docs"
            / "decisions"
            / "0004-link-failure-memory-to-regression-checks.md"
        ).read_text(encoding="utf-8")
        review_command = (
            REPO_ROOT / "commands" / "harness-review.md"
        ).read_text(encoding="utf-8")
        pr_template = (
            REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
        ).read_text(encoding="utf-8")
        maintenance_checklist = (
            REPO_ROOT / "docs" / "checklists" / "harness-review.md"
        ).read_text(encoding="utf-8")
        decision_failure_checklist = (
            REPO_ROOT / "docs" / "checklists" / "decision-failure-memory.md"
        ).read_text(encoding="utf-8")
        verification_scripts = (
            REPO_ROOT / "docs" / "checklists" / "verification-scripts.md"
        ).read_text(encoding="utf-8")

        normalized_failure = " ".join(feedback_failure.split())
        self.assertIn(
            "Failure Memory Was Not Linked To Regression Checks",
            feedback_failure,
        )
        self.assertIn("provider boundary fixtures", normalized_failure)
        self.assertIn("pre-push review", normalized_failure)
        self.assertIn("Regression coverage lives in `tests/test_repository_hygiene.py`", feedback_failure)

        normalized_decision = " ".join(feedback_decision.split())
        self.assertIn("Link Failure Memory To Regression Checks", feedback_decision)
        self.assertIn("Accepted", feedback_decision)
        self.assertIn("Failure memory must be linked to detection or prevention", normalized_decision)
        self.assertIn("provider boundary fixtures", normalized_decision)
        self.assertIn("review timing was pre-commit, pre-push, post-push, or unknown", normalized_decision)

        for text in (
            review_command,
            pr_template,
            maintenance_checklist,
            decision_failure_checklist,
            verification_scripts,
        ):
            with self.subTest(text=text[:40]):
                normalized = " ".join(text.split())
                self.assertIn("regression test", normalized)
                self.assertIn("fixture", normalized)
                self.assertIn("smoke check", normalized)
                self.assertIn("lint rule", normalized)

        self.assertIn("Run this review before commit or push", review_command)
        self.assertIn("Review timing", review_command)
        self.assertIn("post-push", review_command)
        self.assertIn("Pre-Push Review", pr_template)
        self.assertIn("/harness review", pr_template)

    def test_gate_placement_guidance_is_wired_into_harness_workflows(self) -> None:
        workflow_paths = (
            "commands/harness-refresh.md",
            "commands/harness-review.md",
            "templates/generic/AGENTS.md",
            "docs/checklists/verification-scripts.md",
            "docs/adoption-workflow.md",
            "docs/prompts/apply-to-target-repo.md",
            "docs/checklists/harness-review.md",
        )
        for relative in workflow_paths:
            with self.subTest(path=relative):
                text = (REPO_ROOT / relative).read_text(encoding="utf-8")
                normalized = " ".join(text.lower().split())
                self.assertIn(
                    "deterministic, local, non-network, reasonably fast",
                    normalized,
                )
                self.assertIn("checks for product behavior", normalized)
                self.assertIn("normal completion gate", normalized)
                self.assertIn("focused or manual", normalized)

        verification_scripts = (
            REPO_ROOT / "docs" / "checklists" / "verification-scripts.md"
        ).read_text(encoding="utf-8")
        normalized_verification = " ".join(verification_scripts.split())
        self.assertIn("Gate Placement", verification_scripts)
        self.assertIn(
            "Do not assume the normal gate is named `check:harness`",
            normalized_verification,
        )
        self.assertIn("make test", normalized_verification)
        self.assertIn("just check", normalized_verification)
        self.assertIn("scripts/check_harness.py", normalized_verification)
        self.assertIn(
            "live API, credential, quota, provider-uptime",
            normalized_verification,
        )

        adoption_report = (
            REPO_ROOT / "docs" / "templates" / "adoption-report.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "## Verification Gate Placement",
            "Normal completion gate",
            "Deterministic behavior checks included in the normal gate",
            "Focused or manual checks outside the normal gate",
            "Reasons for focused/manual placement",
        ):
            self.assertIn(phrase, adoption_report)

        for report in sorted((REPO_ROOT / "examples").glob("*-adoption-report.md")):
            with self.subTest(adoption_report=report.name):
                text = report.read_text(encoding="utf-8")
                self.assertIn("## Verification Gate Placement", text)
                self.assertIn("Normal completion gate", text)
                self.assertIn(
                    "Deterministic behavior checks included in the normal gate",
                    text,
                )
                self.assertIn("Focused or manual checks outside the normal gate", text)
                self.assertIn("Reasons for focused/manual placement", text)

        review_command = (
            REPO_ROOT / "commands" / "harness-review.md"
        ).read_text(encoding="utf-8")
        refresh_command = (
            REPO_ROOT / "commands" / "harness-refresh.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Gate Placement:", review_command)
        self.assertIn("Gate Placement Review:", refresh_command)

        review_template = (
            REPO_ROOT / "docs" / "templates" / "harness-review-report.md"
        ).read_text(encoding="utf-8")
        review_example = (
            REPO_ROOT / "docs" / "examples" / "harness-review-report.md"
        ).read_text(encoding="utf-8")
        for text in (review_template, review_example):
            self.assertIn("Gate Placement", text)
            self.assertIn("Normal completion gate", text)
            self.assertIn("Deterministic behavior checks", text)
            self.assertIn("Focused/manual checks", text)

        lifecycle_pilots = (
            REPO_ROOT / "docs" / "examples" / "lifecycle-pilot-results.md"
        ).read_text(encoding="utf-8")
        normalized_lifecycle = " ".join(lifecycle_pilots.split())
        self.assertIn("normal-gate placement candidates", normalized_lifecycle)
        self.assertIn("npm run test:planner", normalized_lifecycle)
        self.assertIn("focused live checks", normalized_lifecycle)

        failure_memory = (
            REPO_ROOT
            / "docs"
            / "failures"
            / "0004-deterministic-behavior-check-remained-focused-without-gate-placement-review.md"
        ).read_text(encoding="utf-8")
        decision_memory = (
            REPO_ROOT
            / "docs"
            / "decisions"
            / "0003-review-gate-placement-for-deterministic-behavior-checks.md"
        ).read_text(encoding="utf-8")
        normalized_failure = " ".join(failure_memory.split())
        normalized_decision = " ".join(decision_memory.split())
        self.assertIn("Deterministic Behavior Check Remained Focused", failure_memory)
        self.assertIn("normal completion gate", normalized_failure)
        self.assertIn("check:harness", normalized_failure)
        self.assertIn(
            "Regression coverage lives in `tests/test_repository_hygiene.py`",
            failure_memory,
        )
        self.assertIn("Review Gate Placement For Deterministic Behavior Checks", decision_memory)
        self.assertIn("Accepted", decision_memory)
        self.assertIn("prompt-first governance and reporting rule", normalized_decision)
        self.assertIn("Do not assume it is called `check:harness`", decision_memory)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class AgentSkillsPackageTests(unittest.TestCase):
    def test_agent_skills_package_check_passes(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/check_agent_skills_package.py"],
            cwd=REPO_ROOT,
            check=True,
        )

    def test_codex_plugin_manifest_points_to_packaged_skills(self) -> None:
        manifest = json.loads(
            (
                REPO_ROOT / "agent-skills" / ".codex-plugin" / "plugin.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual("harness-agent-skills", manifest["name"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertEqual("MIT", manifest["license"])
        self.assertIn("$harness", " ".join(manifest["interface"]["defaultPrompt"]))

    def test_router_and_shortcut_skills_cover_all_harness_commands(self) -> None:
        skills_root = REPO_ROOT / "agent-skills" / "skills"
        expected = {
            "harness",
            "harness-adopt",
            "harness-doctor",
            "harness-update",
            "harness-refresh",
            "harness-review",
        }
        actual = {path.name for path in skills_root.iterdir() if path.is_dir()}

        self.assertEqual(expected, actual)

        router = (skills_root / "harness" / "SKILL.md").read_text(encoding="utf-8")
        for command in ("adopt", "doctor", "update", "refresh", "review"):
            self.assertIn(command, router)

    def test_direct_install_layout_resolves_skill_references(self) -> None:
        package_root = REPO_ROOT / "agent-skills"

        with tempfile.TemporaryDirectory() as raw_temp_dir:
            temp_root = Path(raw_temp_dir)
            for config_name in (".agents", ".claude"):
                config_dir = temp_root / config_name
                shutil.copytree(package_root / "skills", config_dir / "skills")
                shutil.copytree(package_root / "references", config_dir / "references")

                for skill_file in (config_dir / "skills").glob("*/SKILL.md"):
                    text = skill_file.read_text(encoding="utf-8")
                    self.assertIn("../../references/", text)
                    references = {
                        match.split("`", 1)[0]
                        for match in text.split("`../../references/")[1:]
                    }
                    for reference in references:
                        resolved = skill_file.parent / "../../references" / reference
                        self.assertTrue(
                            resolved.exists(),
                            f"{skill_file} reference did not resolve: {reference}",
                        )


if __name__ == "__main__":
    unittest.main()

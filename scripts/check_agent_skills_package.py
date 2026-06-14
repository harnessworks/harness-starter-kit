#!/usr/bin/env python3
"""Validate the universal Agent Skills package."""

from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "agent-skills"
SKILLS_ROOT = PACKAGE_ROOT / "skills"
REFERENCES_ROOT = PACKAGE_ROOT / "references"
CODEX_PLUGIN_MANIFEST = PACKAGE_ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_PLUGIN_MANIFEST = PACKAGE_ROOT / ".claude-plugin" / "plugin.json"
PACKAGE_VERSION = "0.1.13"

WORKFLOW_SKILLS = {
    "harness": None,
    "harness-adopt": "adopt-workflow.md",
    "harness-doctor": "doctor-workflow.md",
    "harness-update": "update-workflow.md",
    "harness-refresh": "refresh-workflow.md",
    "harness-review": "review-workflow.md",
}

REQUIRED_REFERENCES = {
    "package-contract.md",
    "adopt-workflow.md",
    "doctor-workflow.md",
    "update-workflow.md",
    "refresh-workflow.md",
    "review-workflow.md",
}

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
RESERVED_NAME_PARTS = {"anthropic", "claude"}
XML_TAG_RE = re.compile(r"<[^>]+>")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path} frontmatter is not closed")

    raw_frontmatter = text[4:end]
    body = text[end + len("\n---\n") :]
    metadata: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"{path} frontmatter line is not key/value: {line}")
        metadata[key.strip()] = value.strip().strip('"')

    return metadata, body


def read_json(path: Path, label: str, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid {label} JSON: {exc}")
        return None


def validate_codex_plugin_manifest(errors: list[str]) -> None:
    if not CODEX_PLUGIN_MANIFEST.exists():
        errors.append(
            f"Missing Codex plugin manifest: {CODEX_PLUGIN_MANIFEST.relative_to(ROOT)}"
        )
        return

    manifest = read_json(CODEX_PLUGIN_MANIFEST, "Codex plugin manifest", errors)
    if manifest is None:
        return

    expected = {
        "name": "harness-agent-skills",
        "version": PACKAGE_VERSION,
        "skills": "./skills/",
        "license": "MIT",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            errors.append(f"Codex plugin.json {key!r} should be {value!r}")

    if "[TODO:" in CODEX_PLUGIN_MANIFEST.read_text(encoding="utf-8"):
        errors.append("Codex plugin.json contains TODO placeholders")

    interface = manifest.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName"):
        if not interface.get(key):
            errors.append(f"Codex plugin.json interface.{key} is required")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts:
        errors.append(
            "Codex plugin.json interface.defaultPrompt must include starter prompts"
        )
    elif not any("$harness" in prompt for prompt in prompts):
        errors.append("Codex plugin.json default prompts should mention $harness")


def validate_claude_plugin_manifest(errors: list[str]) -> None:
    if not CLAUDE_PLUGIN_MANIFEST.exists():
        errors.append(
            f"Missing Claude plugin manifest: {CLAUDE_PLUGIN_MANIFEST.relative_to(ROOT)}"
        )
        return

    manifest = read_json(CLAUDE_PLUGIN_MANIFEST, "Claude plugin manifest", errors)
    if manifest is None:
        return

    expected = {
        "name": "harness-agent-skills",
        "displayName": "Harness Agent Skills",
        "version": PACKAGE_VERSION,
        "license": "MIT",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            errors.append(f"Claude plugin.json {key!r} should be {value!r}")

    if "[TODO:" in CLAUDE_PLUGIN_MANIFEST.read_text(encoding="utf-8"):
        errors.append("Claude plugin.json contains TODO placeholders")

    if not manifest.get("description"):
        errors.append("Claude plugin.json description is required")
    if manifest.get("repository") != "https://github.com/harnessworks/harness-starter-kit":
        errors.append("Claude plugin.json repository should point to starter kit")

    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or "claude-code" not in keywords:
        errors.append("Claude plugin.json keywords should include claude-code")


def validate_skill(skill_name: str, workflow_reference: str | None, errors: list[str]) -> None:
    skill_dir = SKILLS_ROOT / skill_name
    skill_file = skill_dir / "SKILL.md"
    openai_file = skill_dir / "agents" / "openai.yaml"

    if not skill_file.exists():
        errors.append(f"Missing skill file: {skill_file.relative_to(ROOT)}")
        return
    if not openai_file.exists():
        errors.append(f"Missing Codex metadata: {openai_file.relative_to(ROOT)}")

    try:
        metadata, body = parse_frontmatter(skill_file)
    except ValueError as exc:
        errors.append(str(exc))
        return

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != skill_name:
        errors.append(f"{skill_file.relative_to(ROOT)} name should match directory")
    if not NAME_RE.fullmatch(name):
        errors.append(f"{skill_file.relative_to(ROOT)} name is not hyphen-case")
    if any(part in name for part in RESERVED_NAME_PARTS):
        errors.append(f"{skill_file.relative_to(ROOT)} uses a reserved name part")
    if not description:
        errors.append(f"{skill_file.relative_to(ROOT)} description is required")
    if len(description) > 1024:
        errors.append(f"{skill_file.relative_to(ROOT)} description exceeds 1024 chars")
    if XML_TAG_RE.search(name) or XML_TAG_RE.search(description):
        errors.append(f"{skill_file.relative_to(ROOT)} frontmatter contains XML-like tags")

    if "../../references/package-contract.md" not in body:
        errors.append(f"{skill_file.relative_to(ROOT)} must read package-contract.md")
    if workflow_reference and f"../../references/{workflow_reference}" not in body:
        errors.append(
            f"{skill_file.relative_to(ROOT)} must read {workflow_reference}"
        )

    if skill_name == "harness":
        for command in ("adopt", "doctor", "update", "refresh", "review"):
            if command not in body:
                errors.append("harness router is missing subcommand " + command)

    if openai_file.exists():
        openai_text = openai_file.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "default_prompt:"):
            if required not in openai_text:
                errors.append(f"{openai_file.relative_to(ROOT)} missing {required}")
        if f"${skill_name}" not in openai_text:
            errors.append(
                f"{openai_file.relative_to(ROOT)} default_prompt must mention ${skill_name}"
            )


def validate_references(errors: list[str]) -> None:
    for filename in sorted(REQUIRED_REFERENCES):
        path = REFERENCES_ROOT / filename
        if not path.exists():
            errors.append(f"Missing package reference: {path.relative_to(ROOT)}")

    contract = REFERENCES_ROOT / "package-contract.md"
    if contract.exists():
        text = contract.read_text(encoding="utf-8")
        for canonical in (
            "commands/harness-doctor.md",
            "commands/harness-update.md",
            "commands/harness-refresh.md",
            "commands/harness-review.md",
            "docs/adoption-workflow.md",
        ):
            if canonical not in text:
                errors.append(f"package-contract.md missing canonical path {canonical}")
        for skill_name in WORKFLOW_SKILLS:
            if skill_name not in text:
                errors.append(f"package-contract.md missing skill {skill_name}")


def validate_installed_layout(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory() as raw_temp_dir:
        temp_root = Path(raw_temp_dir)
        for config_dir in (temp_root / ".agents", temp_root / ".claude"):
            installed_skills = config_dir / "skills"
            installed_refs = config_dir / "references"
            shutil.copytree(SKILLS_ROOT, installed_skills)
            shutil.copytree(REFERENCES_ROOT, installed_refs)

            for skill_name in WORKFLOW_SKILLS:
                skill_file = installed_skills / skill_name / "SKILL.md"
                try:
                    _metadata, body = parse_frontmatter(skill_file)
                except ValueError as exc:
                    errors.append(str(exc))
                    continue

                references = sorted(
                    set(re.findall(r"`(\.\./\.\./references/[^`]+)`", body))
                )
                if not references:
                    errors.append(
                        f"{skill_file.relative_to(config_dir)} does not reference "
                        "../../references"
                    )
                for reference in references:
                    resolved = (skill_file.parent / reference).resolve()
                    if not resolved.exists():
                        errors.append(
                            f"{skill_file.relative_to(config_dir)} has broken "
                            f"installed reference {reference}"
                        )


def validate_workflow_safeguards(errors: list[str]) -> None:
    review = REFERENCES_ROOT / "review-workflow.md"
    refresh = REFERENCES_ROOT / "refresh-workflow.md"

    if review.exists():
        text = review.read_text(encoding="utf-8")
        for phrase in (
            "parent agent owns reviewer mode",
            "Do not copy those fields from subagent output",
            "gate placement",
            "normal completion gate",
        ):
            if phrase not in text:
                errors.append(f"review-workflow.md missing safeguard: {phrase}")

    if refresh.exists():
        text = refresh.read_text(encoding="utf-8")
        for phrase in ("gate placement", "normal completion gate"):
            if phrase not in text:
                errors.append(
                    f"refresh-workflow.md missing gate-placement phrase: {phrase}"
                )


def validate_documentation_wiring(errors: list[str]) -> None:
    expected_mentions = {
        ROOT / "README.md": "agent-skills/",
        ROOT / "docs" / "component-map.md": "agent-skills/",
        ROOT / "docs" / "validation.md": "check_agent_skills_package.py",
        ROOT / "docs" / "agent-skills-package.md": ".claude-plugin/plugin.json",
    }
    for path, needle in expected_mentions.items():
        if not path.exists() or needle not in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)} should mention {needle}")


def validate_package() -> list[str]:
    errors: list[str] = []

    if not PACKAGE_ROOT.exists():
        errors.append("Missing agent-skills package root")
        return errors

    validate_codex_plugin_manifest(errors)
    validate_claude_plugin_manifest(errors)
    validate_references(errors)
    validate_installed_layout(errors)
    validate_workflow_safeguards(errors)
    for skill_name, workflow_reference in WORKFLOW_SKILLS.items():
        validate_skill(skill_name, workflow_reference, errors)
    validate_documentation_wiring(errors)
    return errors


def main() -> int:
    errors = validate_package()
    for error in errors:
        print(f"Agent skills package error: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

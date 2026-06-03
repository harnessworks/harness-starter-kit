#!/usr/bin/env python3
"""Validate failure records include concrete detection or prevention checks."""

from __future__ import annotations

import json
from dataclasses import dataclass
import re
from pathlib import Path


REQUIRED_SECTIONS = (
    "## Date Observed",
    "## Failure Type",
    "## Goal",
    "## What Happened Or Was Tried",
    "## Why It Failed",
    "## Current Replacement",
    "## Detection Or Prevention Check",
    "## Agent Guidance",
)

CONCRETE_CHECK_PATTERNS = (
    re.compile(r"\b(?:tests?|specs?|fixtures?|scripts?)/[^\s,.;)]+"),
    re.compile(r"`?\.github/workflows/[^\s,.;)`]+`?"),
    re.compile(r"\b(?:npm|pnpm|yarn|bun)\s+run\s+[\w:./-]+"),
    re.compile(r"\b(?:make|just)\s+[\w:./-]+"),
    re.compile(r"\bpython3?\s+(?:-m\s+[\w.:-]+|scripts?/[^\s,.;)]+)"),
    re.compile(r"\bpytest\s+(?:-[\w-]+|tests?/[^\s,.;)]+|[\w/.-]+)"),
    re.compile(r"\b(?:vitest|jest|ruff|mypy|eslint)\s+[\w/.:@-]+"),
    re.compile(r"\blint rule\s+`?[\w@./]+[-:/][\w@./:-]+`?"),
    re.compile(r"\bci gate\s+`?\.github/workflows/[^\s,.;)`]+`?"),
    re.compile(r"\bmanual review point\s+`?docs/checklists/[^\s,.;)`]+"),
    re.compile(r"\bfixture\s+`?(?:tests?|fixtures?)/[^\s,.;)`]+`?"),
)

PATH_REFERENCE_RE = re.compile(
    r"`?((?:tests?|specs?|fixtures?|scripts?|docs/checklists)/[^\s,;)`]+"
    r"|\.github/workflows/[^\s,;)`]+)`?",
    flags=re.IGNORECASE,
)

PACKAGE_SCRIPT_COMMAND_RE = re.compile(
    r"\b(?P<manager>npm|pnpm|yarn|bun)\s+run\s+(?P<script>[\w:./-]+)"
)

REJECTED_PHRASES = (
    "no test has been added",
    "no regression test",
    "no fixture",
    "not added yet",
    "should be added",
    "will be added",
    "to be added",
    "todo",
)

REJECTED_PROSE_PATTERNS = (
    re.compile(r"\b(?:is|are|was|were|only)\s+planned\b"),
    re.compile(r"\bplanned\s+(?:but|for|later|when|after)\b"),
)

NO_CHECK_BLOCKER_PATTERNS = (
    re.compile(
        r"\bbecause\b.{8,}\b(?:blocked|cannot|requires|depends on|no stable|"
        r"not available|impractical|credential|quota|network|"
        r"hardware|permission|sandbox|fixture|manual-only|nondeterministic)\b"
    ),
)

NO_CHECK_FUTURE_SIGNAL_PATTERNS = (
    re.compile(
        r"\brevisit\s+when\s+.{0,80}\b(?:stable sandbox|sandbox|fixture|"
        r"provider contract|api contract|schema|endpoint|mock|emulator|"
        r"credential|quota|permission|hardware|ci|workflow|tooling)\b"
    ),
    re.compile(
        r"\breview\s+when\s+.{0,80}\b(?:stable sandbox|sandbox|fixture|"
        r"provider contract|api contract|schema|endpoint|mock|emulator|"
        r"credential|quota|permission|hardware|ci|workflow|tooling)\b"
    ),
    re.compile(
        r"\btrigger\s+review\s+when\s+.{0,80}\b(?:stable sandbox|sandbox|"
        r"fixture|provider contract|api contract|schema|endpoint|mock|"
        r"emulator|credential|quota|permission|hardware|ci|workflow|tooling)\b"
    ),
    re.compile(
        r"\badd\s+(?:a\s+)?check\s+when\s+.{0,80}\b(?:stable sandbox|"
        r"sandbox|fixture|provider contract|api contract|schema|endpoint|"
        r"mock|emulator|credential|quota|permission|hardware|ci|workflow|"
        r"tooling)\b"
    ),
    re.compile(
        r"\bwhen\s+.{0,80}\b(?:stable sandbox|sandbox|fixture|"
        r"provider contract|api contract|schema|endpoint|mock|emulator|"
        r"credential|quota|permission|hardware|ci|workflow|tooling)\b"
        r".{0,40}\s+(?:is|are|becomes|become)\s+"
        r"(?:available|stable|supported)"
    ),
)


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def is_template(path: Path) -> bool:
    return path.name in ("000-template.md", "README.md")


def section_text(text: str, heading: str) -> str | None:
    if heading not in text:
        return None
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def has_no_check_reason(normalized_section: str) -> bool:
    if "no check is practical" not in normalized_section:
        return False
    return any(
        pattern.search(normalized_section) for pattern in NO_CHECK_BLOCKER_PATTERNS
    ) and any(
        pattern.search(normalized_section)
        for pattern in NO_CHECK_FUTURE_SIGNAL_PATTERNS
    )


def has_concrete_check(normalized_section: str) -> bool:
    return any(pattern.search(normalized_section) for pattern in CONCRETE_CHECK_PATTERNS)


def referenced_paths(section: str) -> list[str]:
    return sorted(
        {match.group(1).rstrip(".") for match in PATH_REFERENCE_RE.finditer(section)}
    )


def missing_referenced_paths(root: Path, section: str) -> list[str]:
    return [
        reference
        for reference in referenced_paths(section)
        if not (root / reference).exists()
    ]


def normalize_package_script(value: str) -> str:
    return value.rstrip(".,;)]}")


def root_package_scripts(root: Path) -> set[str]:
    package_json = root / "package.json"
    if not package_json.exists():
        return set()
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return set()
    package_scripts = data.get("scripts") if isinstance(data, dict) else None
    if not isinstance(package_scripts, dict):
        return set()
    return {str(name) for name in package_scripts}


def missing_package_script_commands(root: Path, section: str) -> list[str]:
    commands = sorted(
        {
            (match.group("manager"), normalize_package_script(match.group("script")))
            for match in PACKAGE_SCRIPT_COMMAND_RE.finditer(section)
        }
    )
    if not commands:
        return []

    scripts = root_package_scripts(root)
    return [
        f"{manager} run {script}"
        for manager, script in commands
        if script not in scripts
    ]


def validate_record(root: Path, path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            findings.append(Finding(path, f"missing required section: {section}"))

    detection_section = section_text(text, "## Detection Or Prevention Check")
    if detection_section is None:
        return findings

    normalized = " ".join(detection_section.lower().split())
    for phrase in REJECTED_PHRASES:
        if phrase in normalized:
            findings.append(
                Finding(path, f"non-committal detection/prevention prose: {phrase}")
            )
    for pattern in REJECTED_PROSE_PATTERNS:
        if pattern.search(normalized):
            findings.append(
                Finding(
                    path,
                    "non-committal detection/prevention prose: planned",
                )
            )

    if not has_concrete_check(normalized) and not has_no_check_reason(normalized):
        findings.append(
            Finding(
                path,
                (
                    "detection/prevention section must name a concrete test path, "
                    "fixture path, command, lint rule, smoke check, drift check, "
                    "CI workflow/gate, manual review point, or a no-check-practical "
                    "reason with concrete blocker and future review signal"
                ),
            )
        )

    for reference in missing_referenced_paths(root, detection_section):
        findings.append(
            Finding(
                path,
                f"detection/prevention references missing local path: {reference}",
            )
        )

    for command in missing_package_script_commands(root, detection_section):
        findings.append(
            Finding(
                path,
                (
                    "package-manager command references missing package.json "
                    f"script: {command}"
                ),
            )
        )

    return findings


def iter_failure_records(root: Path) -> list[Path]:
    failures_dir = root / "docs" / "failures"
    if not failures_dir.exists():
        return []
    return [
        path
        for path in sorted(failures_dir.glob("*.md"))
        if path.is_file() and not is_template(path)
    ]


def check_failure_memory(root: Path) -> int:
    findings: list[Finding] = []
    for path in iter_failure_records(root):
        findings.extend(validate_record(root, path))

    for finding in findings:
        print(f"{finding.path.relative_to(root)}: {finding.message}")

    return 1 if findings else 0


def main() -> int:
    return check_failure_memory(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())

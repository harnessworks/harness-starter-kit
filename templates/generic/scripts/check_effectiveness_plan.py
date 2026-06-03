#!/usr/bin/env python3
"""Validate adoption reports and harness effectiveness measurement reports."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "target",
    "out",
    ".next",
    ".turbo",
    ".gradle",
    "__pycache__",
    "harness-starter-kit",
}

TEMPLATE_PARTS = {
    "templates",
}

ADOPTION_FIELDS = (
    "Baseline available",
    "Comparable tasks to repeat or track",
    "Primary metric",
    "Review window",
    "Results location",
    "Task outcome records location",
)

GATE_PLACEMENT_FIELDS = (
    "Normal completion gate",
    "Deterministic behavior checks included in the normal gate",
    "Focused or manual checks outside the normal gate",
    "Reasons for focused/manual placement",
)

FAILURE_MEMORY_FIELDS = (
    "Recorded",
    "Detection or prevention check",
    "Skipped",
)

NO_FAILURE_RECORD_PHRASES = (
    "no failure record",
    "no failure note",
    "no recurring failure",
    "no user-visible runtime failure",
)

REJECTED_DETECTION_PHRASES = (
    "no test has been added",
    "no regression test",
    "no fixture",
    "not added yet",
    "should be added",
    "will be added",
    "to be added",
    "todo",
)

REJECTED_DETECTION_PROSE_PATTERNS = (
    re.compile(r"\b(?:is|are|was|were|only)\s+planned\b"),
    re.compile(r"\bplanned\s+(?:but|for|later|when|after)\b"),
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

FAILURE_RECORD_RE = re.compile(
    r"`?(docs/failures/[^\s,;)`]+)`?",
    flags=re.IGNORECASE,
)

NO_CHECK_BLOCKER_PATTERNS = (
    re.compile(
        r"\bbecause\b.{8,}\b(?:blocked|cannot|requires|depends on|no stable|"
        r"not available|impractical|credential|quota|network|hardware|"
        r"permission|sandbox|fixture|manual-only|nondeterministic)\b"
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

EFFECTIVENESS_SECTIONS = (
    "## Target",
    "## Task Set",
    "## Results",
    "## Interpretation",
)

TODO_RE = re.compile(r"\bTODO\b", flags=re.IGNORECASE)
SECTION_RE = re.compile(r"^##\s+", flags=re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that adoption reports contain gate-placement and "
            "measurement details, failure-memory linkage, and effectiveness "
            "reports contain required sections instead of placeholders."
        )
    )
    parser.add_argument(
        "--require-report",
        action="store_true",
        help="Fail when no adoption or effectiveness report is present.",
    )
    return parser.parse_args()


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRECTORIES for part in path.parts)


def is_template(path: Path) -> bool:
    return any(part in TEMPLATE_PARTS for part in path.parts)


def is_report(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.endswith(".md")
        and ("adoption-report" in name or "effectiveness-report" in name)
    )


def iter_reports(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.md"))
        if is_report(path.relative_to(root))
        and not is_ignored(path.relative_to(root))
        and not is_template(path.relative_to(root))
    ]


def field_value(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^(\s*)-\s*{re.escape(field)}:\s*(.*)$")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match is None:
            continue

        base_indent = len(match.group(1))
        parts = [match.group(2).strip()]
        for continuation in lines[index + 1 :]:
            stripped = continuation.strip()
            if not stripped:
                break
            indent = len(continuation) - len(continuation.lstrip())
            if indent <= base_indent:
                break
            parts.append(stripped)

        return " ".join(part for part in parts if part).strip()

    return None


def section_text(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    start_index = next(
        (index for index, line in enumerate(lines) if line.strip() == heading),
        None,
    )
    if start_index is None:
        return None

    section_lines = [lines[start_index]]
    for line in lines[start_index + 1 :]:
        if SECTION_RE.match(line):
            break
        section_lines.append(line)

    return "\n".join(section_lines)


def is_placeholder(value: str | None) -> bool:
    return value is None or not value or bool(TODO_RE.search(value))


def recorded_failure_exists(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().lower()
    return "docs/failures/" in normalized and not normalized.startswith("none")


def records_no_failure(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower().startswith("none")


def failure_record_references(value: str | None) -> list[str]:
    if value is None:
        return []
    return sorted(
        {match.group(1).rstrip(".") for match in FAILURE_RECORD_RE.finditer(value)}
    )


def references_missing_local_paths(root: Path, value: str | None) -> list[str]:
    if value is None:
        return []
    return [
        reference
        for reference in sorted(
            {match.group(1).rstrip(".") for match in PATH_REFERENCE_RE.finditer(value)}
        )
        if not (root / reference).exists()
    ]


def says_no_failure_record(value: str | None) -> bool:
    if value is None:
        return False
    normalized = " ".join(value.lower().split())
    return any(phrase in normalized for phrase in NO_FAILURE_RECORD_PHRASES)


def has_no_check_reason(value: str | None) -> bool:
    if value is None:
        return False
    normalized = " ".join(value.lower().split())
    if "no check is practical" not in normalized:
        return False
    return any(
        pattern.search(normalized) for pattern in NO_CHECK_BLOCKER_PATTERNS
    ) and any(pattern.search(normalized) for pattern in NO_CHECK_FUTURE_SIGNAL_PATTERNS)


def has_concrete_check(value: str | None) -> bool:
    if value is None:
        return False
    normalized = " ".join(value.lower().split())
    return any(pattern.search(normalized) for pattern in CONCRETE_CHECK_PATTERNS)


def validate_adoption_report(root: Path, path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    effectiveness_section = section_text(text, "## Effectiveness Measurement Plan")
    if effectiveness_section is None:
        findings.append(
            Finding(path, "missing ## Effectiveness Measurement Plan section")
        )
    else:
        for field in ADOPTION_FIELDS:
            value = field_value(effectiveness_section, field)
            if is_placeholder(value):
                findings.append(Finding(path, f"incomplete measurement field: {field}"))

    gate_section = section_text(text, "## Verification Gate Placement")
    if gate_section is None:
        findings.append(Finding(path, "missing ## Verification Gate Placement section"))
    else:
        for field in GATE_PLACEMENT_FIELDS:
            value = field_value(gate_section, field)
            if is_placeholder(value):
                findings.append(
                    Finding(path, f"incomplete gate-placement field: {field}")
                )

    failure_section = section_text(text, "## Failure Memory")
    if failure_section is None:
        findings.append(Finding(path, "missing ## Failure Memory section"))
    else:
        values: dict[str, str | None] = {}
        for field in FAILURE_MEMORY_FIELDS:
            value = field_value(failure_section, field)
            values[field] = value
            if is_placeholder(value):
                findings.append(
                    Finding(path, f"incomplete failure-memory field: {field}")
                )
        recorded_value = values.get("Recorded")
        detection_value = values.get("Detection or prevention check")
        failure_references = failure_record_references(recorded_value)
        if records_no_failure(recorded_value) and failure_references:
            findings.append(
                Finding(
                    path,
                    "contradictory failure-memory Recorded: none with docs/failures reference",
                )
            )
            for reference in failure_references:
                if not (root / reference).exists():
                    findings.append(
                        Finding(
                            path,
                            f"failure-memory Recorded references missing record: {reference}",
                        )
                    )
        if recorded_value is not None and not records_no_failure(recorded_value):
            if not failure_references:
                findings.append(
                    Finding(
                        path,
                        "failure-memory Recorded must list docs/failures/... or none",
                    )
                )
            for reference in failure_references:
                if not (root / reference).exists():
                    findings.append(
                        Finding(
                            path,
                            f"failure-memory Recorded references missing record: {reference}",
                        )
                    )

        if recorded_failure_exists(recorded_value):
            if says_no_failure_record(values.get("Detection or prevention check")):
                findings.append(
                    Finding(
                        path,
                        (
                            "contradictory failure-memory field: "
                            "Detection or prevention check"
                        ),
                    )
                )
            if says_no_failure_record(values.get("Skipped")):
                findings.append(
                    Finding(path, "contradictory failure-memory field: Skipped")
                )
            normalized_detection = " ".join((detection_value or "").lower().split())
            for phrase in REJECTED_DETECTION_PHRASES:
                if phrase in normalized_detection:
                    findings.append(
                        Finding(
                            path,
                            (
                                "non-committal failure-memory detection prose: "
                                f"{phrase}"
                            ),
                        )
                    )
            for pattern in REJECTED_DETECTION_PROSE_PATTERNS:
                if pattern.search(normalized_detection):
                    findings.append(
                        Finding(
                            path,
                            "non-committal failure-memory detection prose: planned",
                        )
                    )
            if not has_concrete_check(detection_value) and not has_no_check_reason(
                detection_value
            ):
                findings.append(
                    Finding(
                        path,
                        (
                            "incomplete failure-memory detection link: "
                            "Detection or prevention check"
                        ),
                    )
                )
            for reference in references_missing_local_paths(root, detection_value):
                findings.append(
                    Finding(
                        path,
                        (
                            "failure-memory detection references missing local path: "
                            f"{reference}"
                        ),
                    )
                )

    return findings


def validate_effectiveness_report(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for section in EFFECTIVENESS_SECTIONS:
        if section not in text:
            findings.append(Finding(path, f"missing required section: {section}"))
    if TODO_RE.search(text):
        findings.append(Finding(path, "effectiveness report still contains TODO"))
    return findings


def check_effectiveness_plan(root: Path, require_report: bool) -> int:
    reports = iter_reports(root)
    findings: list[Finding] = []

    if require_report and not reports:
        print("No adoption or effectiveness report found.")
        return 1

    for path in reports:
        text = path.read_text(encoding="utf-8")
        name = path.name.lower()
        if "adoption-report" in name:
            findings.extend(validate_adoption_report(root, path, text))
        if "effectiveness-report" in name:
            findings.extend(validate_effectiveness_report(path, text))

    for finding in findings:
        print(f"{finding.path.relative_to(root)}: {finding.message}")

    return 1 if findings else 0


def main() -> int:
    args = parse_args()
    return check_effectiveness_plan(Path.cwd(), args.require_report)


if __name__ == "__main__":
    raise SystemExit(main())

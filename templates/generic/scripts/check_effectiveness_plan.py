#!/usr/bin/env python3
"""Validate adoption reports and harness effectiveness measurement reports."""

from __future__ import annotations

import argparse
import json
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

TASK_OUTCOME_INCLUDE_FIELDS = (
    "include_in_effectiveness_report",
    "include_in_comparable_product_task_count",
)

REQUIRED_INCLUDED_TASK_OUTCOME_FIELDS = (
    "repository_ref",
    "run_id",
    "reviewer",
    "verification_command",
)

REQUIRED_INCLUDED_TASK_OUTCOME_BLOCKS = (
    "expected_boundary",
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

MAVEN_COMMAND_RE = re.compile(
    r"(?<![\w./\\-])(?P<runner>(?:\./|\.\\)?mvnw(?:\.cmd)?|mvn)\s+"
    r"(?P<args>[^`\n,;)\]}]+)",
    flags=re.IGNORECASE,
)
GRADLE_COMMAND_RE = re.compile(
    r"(?<![\w./\\-])(?P<runner>(?:\./|\.\\)?gradlew(?:\.bat)?|gradle)\s+"
    r"(?P<args>[^`\n,;)\]}]+)",
    flags=re.IGNORECASE,
)
GO_COMMAND_RE = re.compile(
    r"(?<![\w./\\-])go\s+(?:build|fmt|generate|list|mod|run|test|vet)\b"
    r"[^`\n,;)\]}]*",
    flags=re.IGNORECASE,
)

CONCRETE_CHECK_PATTERNS = (
    re.compile(r"\b(?:tests?|specs?|fixtures?|scripts?)/[^\s,.;)]+"),
    re.compile(r"`?\.github/workflows/[^\s,.;)`]+`?"),
    re.compile(r"\b(?:npm|pnpm|yarn|bun)\s+run\s+[\w:./-]+"),
    re.compile(
        r"\bmake(?:\s+[\w.-]+=[^\s,;)`\]}]+)*\s+(?!-)[\w:./-]+"
        r"(?=$|[\s,.;)`\]}])"
    ),
    re.compile(r"\bjust\s+(?!-)[\w:./-]+"),
    re.compile(r"\bpython3?\s+(?:-m\s+[\w.:-]+|scripts?/[^\s,.;)]+)"),
    re.compile(r"\bpytest\s+(?:-[\w-]+|tests?/[^\s,.;)]+|[\w/.-]+)"),
    MAVEN_COMMAND_RE,
    GRADLE_COMMAND_RE,
    GO_COMMAND_RE,
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
MAKE_COMMAND_RE = re.compile(
    r"\bmake(?:\s+[\w.-]+=[^\s,;)`\]}]+)*\s+(?!-)(?P<target>[\w:./-]+)"
    r"(?=$|[\s,.;)`\]}])"
)
JUST_COMMAND_RE = re.compile(r"\bjust\s+(?!-)(?P<recipe>[\w:./-]+)")
MAKEFILE_NAMES = ("GNUmakefile", "makefile", "Makefile")
JUSTFILE_NAMES = ("justfile", "Justfile", ".justfile")
MAVEN_WRAPPER_NAMES = ("mvnw", "mvnw.cmd")
GRADLE_BUILD_FILES = (
    "settings.gradle",
    "settings.gradle.kts",
    "build.gradle",
    "build.gradle.kts",
)
GRADLE_WRAPPER_NAMES = ("gradlew", "gradlew.bat")

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
COMPLETED_OUTCOME_PATTERNS = (
    re.compile(
        r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
        r"comparable\s+product-task\s+runs?\s+have\s+been\s+completed\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:all\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
        r"planned\s+product-task\s+records?\s+are\s+complete\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bproduct-task\s+outcomes\s+counted\s*\|\s*"
        r"(?:not available|unknown|n/a)\s*\|\s*"
        r"(?:[1-9]\d*|one|two|three|four|five|six|seven|eight|nine|ten)\b",
        flags=re.IGNORECASE,
    ),
)
STALE_NO_COMPLETED_PATTERNS = (
    re.compile(
        r"\bno\s+completed\s+(?:product[- ]task\s+)?records?\s+yet\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\bno\s+completed\s+product[- ]task\s+runs?\s+yet\b",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"\brecord\s+.{1,160}\btask\s+outcomes\s+as\s+they\s+run\b",
        flags=re.IGNORECASE,
    ),
)


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


def iter_task_outcomes(root: Path) -> list[Path]:
    paths: list[Path] = []
    for pattern in ("*.yaml", "*.yml"):
        for path in root.rglob(pattern):
            relative = path.relative_to(root)
            if is_ignored(relative) or is_template(relative):
                continue
            if "task-outcomes" in relative.parts or path.name.startswith("task-outcome"):
                paths.append(path)
    return sorted(set(paths))


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


def yaml_field_value(text: str, field: str) -> str | None:
    pattern = re.compile(
        rf"^[ \t]*{re.escape(field)}:[ \t]*(.*?)[ \t]*$",
        flags=re.MULTILINE,
    )
    match = pattern.search(text)
    if match is None:
        return None
    return match.group(1).split("#", 1)[0].strip()


def yaml_block_value(text: str, field: str) -> str | None:
    pattern = re.compile(
        rf"^(?P<indent>[ \t]*){re.escape(field)}:[ \t]*(?P<value>.*?)[ \t]*$",
        flags=re.MULTILINE,
    )
    match = pattern.search(text)
    if match is None:
        return None

    value = match.group("value").split("#", 1)[0].strip()
    if value:
        return value

    base_indent = len(match.group("indent"))
    lines = text[match.end() :].splitlines()
    parts: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent:
            break
        parts.append(stripped.split("#", 1)[0].strip())

    return " ".join(part for part in parts if part).strip() or None


def yaml_nested_field_value(text: str, parent: str, field: str) -> str | None:
    parent_pattern = re.compile(
        rf"^(?P<indent>[ \t]*){re.escape(parent)}:[ \t]*$",
        flags=re.MULTILINE,
    )
    parent_match = parent_pattern.search(text)
    if parent_match is None:
        return None

    base_indent = len(parent_match.group("indent"))
    lines = text[parent_match.end() :].splitlines()
    nested_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            nested_lines.append(line)
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent:
            break
        nested_lines.append(line)

    return yaml_field_value("\n".join(nested_lines), field)


def is_truthy_yaml_value(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().strip("\"'`").lower()
    return normalized in {"true", "yes", "1"}


def is_missing_or_placeholder_yaml_value(value: str | None) -> bool:
    if value is None:
        return True
    normalized = value.strip().strip("\"'`").lower()
    return (
        not normalized
        or normalized in {"todo", "unknown", "not recorded", "[]", "{}", "- []", "- {}"}
        or bool(TODO_RE.search(value))
    )


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


def normalize_package_script(value: str) -> str:
    return value.rstrip(".,;)]}")


def normalize_command_target(value: str) -> str:
    return value.rstrip(".,;)]}")


def normalize_command_reference(value: str) -> str:
    command = value.strip().strip("`")
    while command.endswith((";", ",", ")", "]", "}")):
        command = command[:-1].rstrip()
    if command.endswith(".") and not command.endswith("..."):
        command = command[:-1].rstrip()
    return command


def normalized_runner(value: str) -> str:
    runner = value.strip().lower().replace("\\", "/")
    if runner.startswith("./"):
        runner = runner[2:]
    return runner


def root_has_go_project(root: Path) -> bool:
    return (root / "go.mod").exists()


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


def root_make_targets(root: Path) -> set[str]:
    targets: set[str] = set()
    path = next(
        (root / name for name in MAKEFILE_NAMES if (root / name).exists()),
        None,
    )
    if path is None:
        return targets
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return targets
    for raw_line in lines:
        if not raw_line or raw_line[:1].isspace():
            continue
        line = raw_line.split("#", 1)[0].rstrip()
        if ":" not in line:
            continue
        target_part, rule_part = line.split(":", 1)
        if not target_part.strip() or "=" in target_part:
            continue
        if rule_part.lstrip().startswith("="):
            continue
        for target in target_part.split():
            if target and "%" not in target and not target.startswith("."):
                targets.add(target)
    return targets


def root_just_recipes(root: Path) -> set[str]:
    recipes: set[str] = set()
    for name in JUSTFILE_NAMES:
        path = root / name
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for raw_line in lines:
            if not raw_line or raw_line[:1].isspace():
                continue
            line = raw_line.split("#", 1)[0].rstrip()
            alias_match = re.match(r"alias\s+(?P<name>[\w.-]+)\s*:=", line)
            if alias_match is not None:
                recipes.add(alias_match.group("name"))
                continue
            if ":" not in line:
                continue
            recipe_part, rule_part = line.split(":", 1)
            if not recipe_part.strip():
                continue
            if rule_part.lstrip().startswith("="):
                continue
            recipe_part = recipe_part.strip()
            while recipe_part.startswith("[") and "]" in recipe_part:
                recipe_part = recipe_part.split("]", 1)[1].strip()
            if not recipe_part:
                continue
            recipe = recipe_part.split()[0].lstrip("@")
            if recipe and not recipe.startswith("["):
                recipes.add(recipe)
    return recipes


def missing_package_script_commands(root: Path, value: str | None) -> list[str]:
    if value is None:
        return []
    commands = sorted(
        {
            (match.group("manager"), normalize_package_script(match.group("script")))
            for match in PACKAGE_SCRIPT_COMMAND_RE.finditer(value)
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


def missing_make_commands(root: Path, value: str | None) -> list[str]:
    if value is None:
        return []
    commands = sorted(
        {
            normalize_command_target(match.group("target"))
            for match in MAKE_COMMAND_RE.finditer(value)
        }
    )
    if not commands:
        return []

    targets = root_make_targets(root)
    return [f"make {target}" for target in commands if target not in targets]


def missing_just_commands(root: Path, value: str | None) -> list[str]:
    if value is None:
        return []
    commands = sorted(
        {
            normalize_command_target(match.group("recipe"))
            for match in JUST_COMMAND_RE.finditer(value)
        }
    )
    if not commands:
        return []

    recipes = root_just_recipes(root)
    return [f"just {recipe}" for recipe in commands if recipe not in recipes]


def missing_maven_commands(root: Path, value: str | None) -> list[str]:
    if value is None:
        return []

    findings: list[str] = []
    has_pom = (root / "pom.xml").exists()

    for match in MAVEN_COMMAND_RE.finditer(value):
        command = normalize_command_reference(match.group(0))
        runner = normalized_runner(match.group("runner"))
        if runner in MAVEN_WRAPPER_NAMES and not (root / runner).exists():
            findings.append(f"maven wrapper command references missing wrapper: {command}")
        if not has_pom:
            findings.append(f"maven command references missing pom.xml: {command}")

    return sorted(set(findings))


def missing_gradle_commands(root: Path, value: str | None) -> list[str]:
    if value is None:
        return []

    findings: list[str] = []
    has_build_file = any((root / name).exists() for name in GRADLE_BUILD_FILES)

    for match in GRADLE_COMMAND_RE.finditer(value):
        command = normalize_command_reference(match.group(0))
        runner = normalized_runner(match.group("runner"))
        if runner in GRADLE_WRAPPER_NAMES and not (root / runner).exists():
            findings.append(f"gradle wrapper command references missing wrapper: {command}")
        if not has_build_file:
            findings.append(f"gradle command references missing build file: {command}")

    return sorted(set(findings))


def missing_go_commands(root: Path, value: str | None) -> list[str]:
    if value is None or root_has_go_project(root):
        return []
    return sorted(
        {
            (
                "go command references missing go.mod: "
                f"{normalize_command_reference(match.group(0))}"
            )
            for match in GO_COMMAND_RE.finditer(value)
        }
    )


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
            for command in missing_package_script_commands(root, detection_value):
                findings.append(
                    Finding(
                        path,
                        (
                            "failure-memory detection references missing "
                            f"package.json script: {command}"
                        ),
                    )
                )
            for command in missing_make_commands(root, detection_value):
                findings.append(
                    Finding(
                        path,
                        (
                            "failure-memory detection references missing "
                            f"Makefile target: {command}"
                        ),
                    )
                )
            for command in missing_just_commands(root, detection_value):
                findings.append(
                    Finding(
                        path,
                        (
                            "failure-memory detection references missing "
                            f"justfile recipe: {command}"
                        ),
                    )
                )
            for message in missing_maven_commands(root, detection_value):
                findings.append(
                    Finding(path, f"failure-memory detection {message}")
                )
            for message in missing_gradle_commands(root, detection_value):
                findings.append(
                    Finding(path, f"failure-memory detection {message}")
                )
            for message in missing_go_commands(root, detection_value):
                findings.append(
                    Finding(path, f"failure-memory detection {message}")
                )

    return findings


def validate_effectiveness_report(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for section in EFFECTIVENESS_SECTIONS:
        if section not in text:
            findings.append(Finding(path, f"missing required section: {section}"))
    if TODO_RE.search(text):
        findings.append(Finding(path, "effectiveness report still contains TODO"))
    if any(pattern.search(text) for pattern in COMPLETED_OUTCOME_PATTERNS) and any(
        pattern.search(text) for pattern in STALE_NO_COMPLETED_PATTERNS
    ):
        findings.append(
            Finding(path, "contradictory effectiveness-report completion language")
        )
    return findings


def validate_task_outcome(root: Path, path: Path, text: str) -> list[Finding]:
    report_include_value = yaml_field_value(text, "include_in_effectiveness_report")
    comparable_count_value = yaml_field_value(
        text, "include_in_comparable_product_task_count"
    )
    findings: list[Finding] = []

    if is_truthy_yaml_value(report_include_value) and is_missing_or_placeholder_yaml_value(
        comparable_count_value
    ):
        findings.append(
            Finding(
                path,
                (
                    "task outcome included in effectiveness report must declare "
                    "include_in_comparable_product_task_count"
                ),
            )
        )

    if is_truthy_yaml_value(comparable_count_value) and not is_truthy_yaml_value(
        report_include_value
    ):
        findings.append(
            Finding(
                path,
                (
                    "task outcome included in comparable product-task count must set "
                    "include_in_effectiveness_report to true"
                ),
            )
        )

    verification_command = yaml_field_value(text, "verification_command")
    for command in missing_make_commands(root, verification_command):
        findings.append(
            Finding(
                path,
                f"task outcome verification references missing Makefile target: {command}",
            )
        )
    for command in missing_just_commands(root, verification_command):
        findings.append(
            Finding(
                path,
                f"task outcome verification references missing justfile recipe: {command}",
            )
        )
    for message in missing_maven_commands(root, verification_command):
        findings.append(Finding(path, f"task outcome verification {message}"))
    for message in missing_gradle_commands(root, verification_command):
        findings.append(Finding(path, f"task outcome verification {message}"))
    for message in missing_go_commands(root, verification_command):
        findings.append(Finding(path, f"task outcome verification {message}"))

    truthy_include_fields = [
        field
        for field in TASK_OUTCOME_INCLUDE_FIELDS
        if is_truthy_yaml_value(yaml_field_value(text, field))
    ]
    if not truthy_include_fields:
        return findings

    name = path.name.lower()
    if "template" in name:
        findings.append(
            Finding(
                path,
                (
                    "task outcome template must not be included in effectiveness "
                    "or comparable product-task counts"
                ),
            )
        )
        return findings

    missing_required_fields = [
        field
        for field in REQUIRED_INCLUDED_TASK_OUTCOME_FIELDS
        if is_missing_or_placeholder_yaml_value(yaml_field_value(text, field))
    ]
    missing_required_blocks = [
        field
        for field in REQUIRED_INCLUDED_TASK_OUTCOME_BLOCKS
        if is_missing_or_placeholder_yaml_value(yaml_block_value(text, field))
    ]
    if missing_required_fields or missing_required_blocks:
        missing_fields = ", ".join(
            [*missing_required_fields, *missing_required_blocks]
        )
        findings.append(
            Finding(
                path,
                (
                    "included task outcome is missing required evidence field(s): "
                    f"{missing_fields}"
                ),
            )
        )

    prompt_ref = yaml_field_value(text, "prompt_ref")
    prompt_hash = yaml_field_value(text, "prompt_hash")
    if is_missing_or_placeholder_yaml_value(prompt_ref) and (
        is_missing_or_placeholder_yaml_value(prompt_hash)
    ):
        findings.append(
            Finding(
                path,
                (
                    "included task outcome must include prompt_ref or prompt_hash"
                ),
            )
        )

    first_pass_result = yaml_nested_field_value(
        text,
        "first_pass_verification",
        "result",
    )
    if is_missing_or_placeholder_yaml_value(first_pass_result):
        findings.append(
            Finding(
                path,
                (
                    "included task outcome is missing "
                    "first_pass_verification.result"
                ),
            )
        )

    placeholder_fields = [
        field
        for field in ("id", "run_id", "prompt_summary")
        if is_missing_or_placeholder_yaml_value(yaml_field_value(text, field))
    ]
    if placeholder_fields:
        findings.append(
            Finding(
                path,
                (
                    "placeholder task outcome must not be included in "
                    "effectiveness or comparable product-task counts"
                ),
            )
        )

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

    for path in iter_task_outcomes(root):
        findings.extend(
            validate_task_outcome(root, path, path.read_text(encoding="utf-8"))
        )

    for finding in findings:
        print(f"{finding.path.relative_to(root)}: {finding.message}")

    return 1 if findings else 0


def main() -> int:
    args = parse_args()
    return check_effectiveness_plan(Path.cwd(), args.require_report)


if __name__ == "__main__":
    raise SystemExit(main())

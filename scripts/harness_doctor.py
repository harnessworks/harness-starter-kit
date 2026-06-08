#!/usr/bin/env python3
"""Produce a six-element Harness Doctor score for a repository."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".cfg",
    ".ini",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

IGNORED_PARTS = {
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

AGENT_INSTRUCTION_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    ".cursorrules",
    ".cursor/rules",
    ".github/copilot-instructions.md",
)

DECISION_RECORD_SECTIONS = (
    "## Context",
    "## Decision",
)

FAILURE_RECORD_SECTIONS = (
    "## Why It Failed",
    "## Current Replacement",
    "## Agent Guidance",
)

KNOWN_CHECKS = {
    "scripts/check_structure.py": "structure",
    "scripts/check_docs_drift.py": "docs drift",
    "scripts/check_encoding_hygiene.py": "encoding hygiene",
    "scripts/check_failure_memory.py": "failure memory",
    "scripts/check_decision_memory.py": "decision memory",
    "scripts/check_effectiveness_plan.py": "effectiveness plan",
}


@dataclass(frozen=True)
class Signal:
    name: str
    score: int | None
    evidence: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        if self.score is None:
            return "unmeasured"
        if self.score >= 85:
            return "strong"
        if self.score >= 60:
            return "partial"
        if self.score >= 30:
            return "weak"
        return "missing"


@dataclass(frozen=True)
class Element:
    name: str
    signals: tuple[Signal, ...]

    @property
    def score(self) -> int:
        scored = [signal.score for signal in self.signals if signal.score is not None]
        if not scored:
            return 0
        return round(sum(scored) / len(scored))


@dataclass(frozen=True)
class CouplingFinding:
    severity: str
    kind: str
    detail: str


@dataclass(frozen=True)
class DoctorResult:
    elements: tuple[Element, ...]
    findings: tuple[CouplingFinding, ...]
    evidence: tuple[str, ...]
    missing: tuple[str, ...]

    @property
    def score(self) -> int:
        if not self.elements:
            return 0
        return round(sum(element.score for element in self.elements) / len(self.elements))


@dataclass(frozen=True)
class RepositoryEvidence:
    root: Path
    text_files: tuple[Path, ...]
    repository_text: str
    docs_text: str
    binding_text: str
    readme_text: str
    agent_files: tuple[Path, ...]
    agent_text: str
    workflows: tuple[Path, ...]
    workflow_text: str
    scripts: dict[str, str]
    known_checks: tuple[Path, ...]
    unknown_checks: tuple[Path, ...]
    bound_checks: dict[str, bool]
    decisions: tuple[Path, ...]
    failures: tuple[Path, ...]
    failure_records_missing_detection: tuple[Path, ...]
    task_outcomes: tuple[Path, ...]
    included_task_outcomes: tuple[Path, ...]
    effectiveness_reports: tuple[Path, ...]
    local_effectiveness_reports: tuple[Path, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan a repository for six-element Harness Doctor evidence and "
            "coupling findings. The score is a health diagnostic, not proof of "
            "agent effectiveness."
        )
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        help="Exit nonzero when the overall score is below this value.",
    )
    parser.add_argument(
        "--fail-on",
        action="append",
        choices=("critical-coupling",),
        default=[],
        help=(
            "Optional diagnostic gate. Use 'critical-coupling' to fail when "
            "critical coupling findings are present."
        ),
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def iter_text_files(root: Path, limit: int = 1000) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if len(files) >= limit:
            break
        rel = path.relative_to(root)
        if path.is_file() and not is_ignored(rel) and path.suffix in TEXT_EXTENSIONS:
            files.append(path)
    return files


def joined_text(paths: list[Path] | tuple[Path, ...]) -> str:
    return "\n".join(read_text(path) for path in paths)


def path_exists(root: Path, relative: str) -> bool:
    return (root / relative).exists()


def dir_has_files(root: Path, relative: str) -> bool:
    path = root / relative
    return path.is_dir() and any(child.is_file() for child in path.rglob("*"))


def relative_path(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def relative_evidence(root: Path, path: Path | None, fallback: str) -> str:
    if path is None:
        return fallback
    return relative_path(root, path)


def load_package_json(root: Path) -> dict[str, object]:
    package_json = root / "package.json"
    if not package_json.exists():
        return {}
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def package_scripts(root: Path) -> dict[str, str]:
    scripts = load_package_json(root).get("scripts", {})
    if not isinstance(scripts, dict):
        return {}
    return {str(key): str(value) for key, value in scripts.items()}


def has_script_matching(root: Path, pattern: str) -> bool:
    regex = re.compile(pattern, flags=re.IGNORECASE)
    return any(
        regex.search(name) or regex.search(value)
        for name, value in package_scripts(root).items()
    )


def files_matching(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(matches))


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def has_command_text(text: str, terms: tuple[str, ...]) -> bool:
    return any(term.lower() in text.lower() for term in terms)


def agent_instruction_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in AGENT_INSTRUCTION_PATHS:
        path = root / relative
        if path.is_file():
            files.append(path)
        if path.is_dir():
            files.extend(sorted(child for child in path.rglob("*") if child.is_file()))
    return files


def workflow_files(root: Path) -> list[Path]:
    return files_matching(
        root,
        (
            ".github/workflows/*.yml",
            ".github/workflows/*.yaml",
            ".gitlab-ci.yml",
            "Jenkinsfile",
            ".circleci/config.yml",
            "buildkite.yml",
            ".buildkite/*.yml",
        ),
    )


def docs_files(paths: list[Path], root: Path) -> list[Path]:
    return [
        path
        for path in paths
        if relative_path(root, path).startswith(("docs/", "commands/", "README"))
        or path.name in {"AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"}
    ]


def binding_files(paths: list[Path], root: Path) -> list[Path]:
    allowed_names = {
        "AGENTS.md",
        "CLAUDE.md",
        "CONTRIBUTING.md",
        "Jenkinsfile",
        "Makefile",
        "makefile",
        "Justfile",
        "justfile",
        "package.json",
        "pyproject.toml",
        ".pre-commit-config.yaml",
        ".pre-commit-config.yml",
    }
    selected: list[Path] = []
    for path in paths:
        rel = relative_path(root, path)
        is_binding_doc = (
            rel in {
                "docs/validation.md",
                "docs/adoption-workflow.md",
                "docs/prompts/apply-to-target-repo.md",
            }
            or rel.startswith("docs/checklists/")
            or rel.startswith("commands/")
        )
        if path.name in allowed_names or rel.startswith((".github/", ".circleci/", ".buildkite/")) or is_binding_doc:
            selected.append(path)
    return selected


def is_placeholder_record(path: Path, text: str) -> bool:
    name = path.name.lower()
    lowered = text.lower()
    placeholder_terms = (
        "todo",
        "yyyy-mm-dd",
        "template",
        "placeholder",
        "no known",
    )
    return (
        name == "readme.md"
        or "template" in name
        or any(term in lowered for term in placeholder_terms)
    )


def has_required_record_sections(path: Path, text: str) -> bool:
    normalized = text.lower()
    path_parts = {part.lower() for part in path.parts}
    if "failures" in path_parts:
        return all(section.lower() in normalized for section in FAILURE_RECORD_SECTIONS)
    if "decisions" in path_parts:
        return all(section.lower() in normalized for section in DECISION_RECORD_SECTIONS)
    return len(text.strip()) >= 80


def non_template_records(root: Path, relatives: tuple[str, ...]) -> list[Path]:
    records: list[Path] = []
    for relative in relatives:
        directory = root / relative
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            text = read_text(path)
            if is_placeholder_record(path, text):
                continue
            if not has_required_record_sections(path, text):
                continue
            records.append(path)
    return records


def has_detection_or_prevention_link(text: str) -> bool:
    lowered = text.lower()
    has_section = bool(
        re.search(
            r"^##\s+detection\s+or\s+prevention\s+check",
            text,
            flags=re.IGNORECASE | re.MULTILINE,
        )
    )
    check_terms = (
        "regression test",
        "fixture",
        "smoke check",
        "lint rule",
        "drift check",
        "ci gate",
        "manual review",
        "test",
        "tests/",
        "checks",
        "check_",
        "pytest",
        "unittest",
        "npm test",
        "no check",
        "not practical",
    )
    return has_section and any(term in lowered for term in check_terms)


def known_check_paths(root: Path) -> list[Path]:
    return [root / relative for relative in KNOWN_CHECKS if (root / relative).is_file()]


def unknown_check_paths(root: Path) -> list[Path]:
    known = {str(path) for path in known_check_paths(root)}
    return [
        path
        for path in sorted((root / "scripts").glob("check_*.py"))
        if str(path) not in known
    ]


def check_is_bound(root: Path, relative: str, text: str) -> bool:
    basename = Path(relative).name
    label = KNOWN_CHECKS.get(relative, "")
    needles = {relative, basename}
    if label:
        needles.add(label)
    return any(needle.lower() in text.lower() for needle in needles)


def check_references(text: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            set(
                match.group(0)
                for match in re.finditer(
                    r"scripts/[A-Za-z0-9_./-]*check[A-Za-z0-9_./-]*\.py",
                    text,
                )
            )
        )
    )


def command_reference_text(ev: RepositoryEvidence) -> str:
    return "\n".join(
        [
            ev.workflow_text,
            "\n".join(ev.scripts.values()),
            read_text(ev.root / "Makefile"),
            read_text(ev.root / "makefile"),
            read_text(ev.root / "Justfile"),
            read_text(ev.root / "justfile"),
        ]
    )


def purpose_text(ev: RepositoryEvidence) -> str:
    paths = [
        ev.root / "AGENTS.md",
        ev.root / "CLAUDE.md",
        ev.root / "README.md",
        ev.root / "CONTRIBUTING.md",
        ev.root / "docs" / "validation.md",
        ev.root / "docs" / "adoption-workflow.md",
    ]
    for directory in ("docs/conventions", "docs/domain", "docs/checklists"):
        root = ev.root / directory
        if root.is_dir():
            paths.extend(sorted(path for path in root.rglob("*.md") if path.is_file()))
    return joined_text(tuple(paths))


def check_has_documented_purpose(root: Path, relative: str, text: str) -> bool:
    basename = Path(relative).name
    label = KNOWN_CHECKS.get(relative, "")
    needles = {relative, basename}
    if label:
        needles.add(label)
    return any(needle.lower() in text.lower() for needle in needles)


def task_outcome_files(root: Path) -> list[Path]:
    patterns = (
        "docs/effectiveness/task-outcomes/*.yaml",
        "docs/effectiveness/task-outcomes/*.yml",
        "docs/examples/task-outcomes/*.yaml",
        "docs/examples/task-outcomes/*.yml",
    )
    return files_matching(root, patterns)


def yaml_scalar_value(text: str, field: str) -> str | None:
    match = re.search(
        rf"(?m)^\s*{re.escape(field)}\s*:\s*([^\n#]+)",
        text,
    )
    if not match:
        return None
    return match.group(1).strip().strip("'\"").lower()


def is_truthy_yaml_field(text: str, field: str) -> bool:
    value = yaml_scalar_value(text, field)
    return value in {"true", "yes", "1"}


def included_task_outcome_files(paths: tuple[Path, ...]) -> tuple[Path, ...]:
    included: list[Path] = []
    for path in paths:
        text = read_text(path)
        if is_truthy_yaml_field(text, "include_in_effectiveness_report") or is_truthy_yaml_field(
            text, "include_in_comparable_product_task_count"
        ):
            included.append(path)
    return tuple(included)


def effectiveness_report_files(root: Path) -> list[Path]:
    patterns = (
        "docs/effectiveness/*.md",
        "docs/examples/effectiveness-report*.md",
        "examples/*effectiveness-report*.md",
    )
    return files_matching(root, patterns)


def local_effectiveness_report_files(root: Path) -> list[Path]:
    return files_matching(root, ("docs/effectiveness/*.md",))


def collect_evidence(root: Path) -> RepositoryEvidence:
    text_files = tuple(iter_text_files(root))
    docs_text_files = tuple(docs_files(list(text_files), root))
    binding_text_files = tuple(binding_files(list(text_files), root))
    workflows = tuple(workflow_files(root))
    known_checks = tuple(known_check_paths(root))
    unknown_checks = tuple(unknown_check_paths(root))
    task_outcomes = tuple(task_outcome_files(root))
    binding_text = joined_text(binding_text_files)
    bound_checks = {
        relative_path(root, path): check_is_bound(root, relative_path(root, path), binding_text)
        for path in known_checks
    }
    failures = tuple(non_template_records(root, ("docs/failures",)))
    failure_records_missing_detection = tuple(
        path for path in failures if not has_detection_or_prevention_link(read_text(path))
    )
    return RepositoryEvidence(
        root=root,
        text_files=text_files,
        repository_text=joined_text(text_files),
        docs_text=joined_text(docs_text_files),
        binding_text=binding_text,
        readme_text=read_text(root / "README.md"),
        agent_files=tuple(agent_instruction_files(root)),
        agent_text=joined_text(agent_instruction_files(root)),
        workflows=workflows,
        workflow_text=joined_text(workflows),
        scripts=package_scripts(root),
        known_checks=known_checks,
        unknown_checks=tuple(unknown_checks),
        bound_checks=bound_checks,
        decisions=tuple(non_template_records(root, ("docs/decisions",))),
        failures=failures,
        failure_records_missing_detection=failure_records_missing_detection,
        task_outcomes=task_outcomes,
        included_task_outcomes=included_task_outcome_files(task_outcomes),
        effectiveness_reports=tuple(effectiveness_report_files(root)),
        local_effectiveness_reports=tuple(local_effectiveness_report_files(root)),
    )


def clamp_score(value: int) -> int:
    return max(0, min(100, value))


def proportional_score(count: int, total: int, points: int) -> int:
    if total <= 0:
        return 0
    return round((count / total) * points)


def signal(
    name: str,
    score: int | None,
    evidence: list[str] | tuple[str, ...] = (),
    missing: list[str] | tuple[str, ...] = (),
) -> Signal:
    return Signal(name, None if score is None else clamp_score(score), tuple(evidence), tuple(missing))


def exact_command_present(ev: RepositoryEvidence) -> bool:
    exact_command_terms = (
        "python",
        "pytest",
        "unittest",
        "npm",
        "pnpm",
        "yarn",
        "bun",
        "mvn",
        "gradle",
        "go test",
        "cargo",
        "make",
    )
    return has_command_text(ev.agent_text + ev.readme_text, exact_command_terms)


def test_command_present(ev: RepositoryEvidence) -> bool:
    return has_script_matching(ev.root, r"test") or has_command_text(
        ev.repository_text,
        ("pytest", "unittest", "npm test", "go test", "mvn test", "gradle test", "cargo test"),
    )


def lint_command_present(ev: RepositoryEvidence) -> bool:
    return has_script_matching(ev.root, r"lint|ruff|eslint|flake8") or has_command_text(
        ev.repository_text,
        ("lint", "ruff", "eslint", "flake8", "pylint"),
    )


def typecheck_command_present(ev: RepositoryEvidence) -> bool:
    return has_script_matching(ev.root, r"typecheck|type-check|mypy|tsc|pyright") or has_command_text(
        ev.repository_text,
        ("typecheck", "type-check", "mypy", "tsc", "pyright"),
    )


def local_validation_present(ev: RepositoryEvidence) -> bool:
    has_bound_unknown_check = any(
        check_is_bound(ev.root, relative_path(ev.root, path), ev.binding_text)
        for path in ev.unknown_checks
    )
    return (
        path_exists(ev.root, ".pre-commit-config.yaml")
        or path_exists(ev.root, ".pre-commit-config.yml")
        or has_script_matching(ev.root, r"check|validate|verify")
        or contains_any(ev.binding_text, ("python scripts/check", "python3 scripts/check"))
        or any(ev.bound_checks.values())
        or has_bound_unknown_check
        or path_exists(ev.root, "Makefile")
        or path_exists(ev.root, "Justfile")
    )


def build_instructions(ev: RepositoryEvidence) -> Element:
    stated_score = 0
    stated_evidence: list[str] = []
    stated_missing: list[str] = []
    if ev.agent_files:
        stated_score += 35
        stated_evidence.append(f"agent instructions: {relative_evidence(ev.root, ev.agent_files[0], '')}")
    else:
        stated_missing.append("No AGENTS.md, CLAUDE.md, Cursor rules, or Copilot instructions found")
    if contains_any(ev.agent_text + ev.readme_text, ("overview", "purpose", "this repository", "project")):
        stated_score += 15
        stated_evidence.append("project overview appears in README or agent instructions")
    else:
        stated_missing.append("Project overview is not clear in README or agent instructions")
    if exact_command_present(ev):
        stated_score += 20
        stated_evidence.append("exact command-like text appears in README or agent instructions")
    else:
        stated_missing.append("Exact build, test, lint, or validation commands are missing")
    if contains_any(ev.agent_text, ("architecture", "boundary", "directory rules", "constraints", "do not import", "forbidden", "do not", "never", "must not")):
        stated_score += 20
        stated_evidence.append("agent instructions include boundaries or forbidden actions")
    else:
        stated_missing.append("Architecture boundaries or forbidden actions are not documented")
    if contains_any(ev.agent_text, ("security", "secret", "credential", "safety", "privacy", "destructive")):
        stated_score += 10
        stated_evidence.append("agent instructions include safety or security notes")
    else:
        stated_missing.append("Safety or security notes are missing from agent instructions")

    routed_score = 0
    routed_evidence: list[str] = []
    routed_missing: list[str] = []
    memory_routes = sum(
        1
        for term in ("docs/decisions", "docs/failures", "docs/conventions", "docs/domain")
        if term in ev.agent_text
    )
    routed_score += proportional_score(memory_routes, 4, 40)
    if memory_routes:
        routed_evidence.append("agent instructions route to durable memory docs")
    else:
        routed_missing.append("Agent instructions do not route to decision, failure, convention, or domain docs")
    if contains_any(ev.agent_text + ev.readme_text, ("validation", "local checks", "run these checks", "harness doctor", "check_harness", "before committing")):
        routed_score += 25
        routed_evidence.append("instructions route agents toward validation checks")
    else:
        routed_missing.append("Instructions do not route agents toward validation checks")
    if contains_any(ev.agent_text, ("source of truth", "inspect", "readme", "docs/theory", "preserve")):
        routed_score += 20
        routed_evidence.append("instructions name source-of-truth or repository-inspection rules")
    else:
        routed_missing.append("Source-of-truth or repository-inspection guidance is missing")
    if ev.agent_files and len(ev.agent_text.splitlines()) <= 260:
        routed_score += 15
        routed_evidence.append("agent entry point is short enough to act as a route map")
    elif ev.agent_files:
        routed_score += 5
        routed_missing.append("Agent instruction entry point is large; review whether it still acts as a route map")
    else:
        routed_missing.append("No agent instruction entry point exists")

    proven_evidence = []
    if ev.task_outcomes or ev.effectiveness_reports:
        proven_evidence.append("task outcome or effectiveness evidence exists but is not counted in the score")

    return Element(
        "Instructions",
        (
            signal("Stated", stated_score, stated_evidence, stated_missing),
            signal("Routed", routed_score, routed_evidence, routed_missing),
            signal("Proven", None, proven_evidence),
        ),
    )


def build_constraints(ev: RepositoryEvidence) -> Element:
    known_count = len(ev.known_checks)
    bound_count = sum(1 for found in ev.bound_checks.values() if found)
    stated_score = proportional_score(known_count, len(KNOWN_CHECKS), 40)
    stated_evidence = [
        f"known check script: {relative_path(ev.root, path)}" for path in ev.known_checks[:6]
    ]
    stated_missing: list[str] = []
    if not ev.known_checks:
        stated_missing.append("No known harness check scripts found")
    if path_exists(ev.root, ".harness/structure-rules.json") or path_exists(ev.root, ".harness/decision-memory-rules.json"):
        stated_score += 15
        stated_evidence.append(".harness rule configuration exists")
    else:
        stated_missing.append("No .harness rule configuration found")
    if ev.workflows or ev.scripts:
        stated_score += 15
        stated_evidence.append("CI workflow or package scripts exist")
    else:
        stated_missing.append("No CI workflow or package scripts found")
    if contains_any(ev.repository_text, ("forbidden_patterns", "forbidden path", "forbidden_paths", "generated files", "do not edit", "source of truth")):
        stated_score += 20
        stated_evidence.append("repository text declares forbidden, generated-file, or source-of-truth constraints")
    else:
        stated_missing.append("Forbidden path, generated-file, or source-of-truth constraints are not visible")
    if lint_command_present(ev) or typecheck_command_present(ev) or path_exists(ev.root, ".pre-commit-config.yaml"):
        stated_score += 10
        stated_evidence.append("lint, typecheck, or pre-commit constraints are visible")
    else:
        stated_missing.append("Lint, typecheck, or pre-commit constraints are not visible")

    enforced_score = 0
    enforced_evidence: list[str] = []
    enforced_missing: list[str] = []
    if known_count:
        enforced_score += proportional_score(bound_count, known_count, 50)
        if bound_count:
            enforced_evidence.append(f"{bound_count}/{known_count} known check scripts are referenced by docs, commands, or CI")
        if bound_count < known_count:
            enforced_missing.append(f"{known_count - bound_count} known check scripts are not visibly bound to docs, commands, or CI")
    else:
        enforced_missing.append("No known check scripts are available to enforce constraints")
    if contains_any(ev.workflow_text, ("check_structure", "check_docs_drift", "check_encoding", "check_failure", "check_decision", "check_effectiveness", "harness_doctor")):
        enforced_score += 20
        enforced_evidence.append("CI references harness or drift checks")
    else:
        enforced_missing.append("CI does not visibly run harness or drift checks")
    if (
        has_script_matching(ev.root, r"check|validate|verify")
        or path_exists(ev.root, "Makefile")
        or path_exists(ev.root, "Justfile")
        or contains_any(ev.binding_text, ("python scripts/check", "python3 scripts/check"))
    ):
        enforced_score += 15
        enforced_evidence.append("local validation command is documented or available")
    else:
        enforced_missing.append("No local validation command found in docs, package scripts, Makefile, or Justfile")
    if test_command_present(ev) or lint_command_present(ev) or typecheck_command_present(ev):
        enforced_score += 15
        enforced_evidence.append("tests, lint, or typecheck provide enforcement feedback")
    else:
        enforced_missing.append("No test, lint, or typecheck command found")

    proven_evidence = []
    if ev.task_outcomes or ev.effectiveness_reports:
        proven_evidence.append("outcome evidence exists but constraint effectiveness is not scored by Doctor")

    return Element(
        "Constraints",
        (
            signal("Stated", stated_score, stated_evidence, stated_missing),
            signal("Enforced", enforced_score, enforced_evidence, enforced_missing),
            signal("Proven", None, proven_evidence),
        ),
    )


def build_feedback(ev: RepositoryEvidence) -> Element:
    exists_score = 0
    exists_evidence: list[str] = []
    exists_missing: list[str] = []
    if test_command_present(ev):
        exists_score += 25
        exists_evidence.append("test command appears in scripts or documentation")
    else:
        exists_missing.append("No test command found")
    if lint_command_present(ev):
        exists_score += 15
        exists_evidence.append("lint command appears in scripts or documentation")
    else:
        exists_missing.append("No lint command found")
    if typecheck_command_present(ev):
        exists_score += 15
        exists_evidence.append("typecheck command appears in scripts or documentation")
    else:
        exists_missing.append("No typecheck command found")
    if ev.workflows:
        exists_score += 20
        exists_evidence.append(f"CI workflow: {relative_path(ev.root, ev.workflows[0])}")
    else:
        exists_missing.append("No CI workflow found")
    if local_validation_present(ev):
        exists_score += 25
        exists_evidence.append("local validation script, package check, pre-commit, or task-runner command found")
    else:
        exists_missing.append("No local validation feedback path found")

    known_count = len(ev.known_checks)
    bound_count = sum(1 for found in ev.bound_checks.values() if found)
    coverage_score = 0
    coverage_evidence: list[str] = []
    coverage_missing: list[str] = []
    if known_count:
        coverage_score += proportional_score(bound_count, known_count, 60)
        coverage_evidence.append(f"feedback binding coverage for known checks: {bound_count}/{known_count}")
        if bound_count < known_count:
            coverage_missing.append("Some known checks are not visibly bound to validation docs, package scripts, or CI")
    else:
        coverage_missing.append("No known harness checks available for feedback coverage")
    memory_check_count = sum(
        1
        for relative in (
            "scripts/check_failure_memory.py",
            "scripts/check_decision_memory.py",
            "scripts/check_effectiveness_plan.py",
        )
        if relative in ev.bound_checks and ev.bound_checks[relative]
    )
    coverage_score += proportional_score(memory_check_count, 3, 20)
    if memory_check_count:
        coverage_evidence.append("feedback covers memory or evaluation checks")
    else:
        coverage_missing.append("Feedback does not visibly cover memory or evaluation checks")
    if contains_any(ev.binding_text, ("normal gate", "focused", "manual", "local validation", "before finishing", "before committing")):
        coverage_score += 20
        coverage_evidence.append("validation docs describe normal, focused, or manual checks")
    else:
        coverage_missing.append("Validation docs do not distinguish normal, focused, or manual checks")

    proven_evidence = []
    if ev.task_outcomes or ev.effectiveness_reports:
        proven_evidence.append("outcome evidence exists but feedback effectiveness is not scored by Doctor")

    return Element(
        "Feedback",
        (
            signal("Exists", exists_score, exists_evidence, exists_missing),
            signal("Coverage", coverage_score, coverage_evidence, coverage_missing),
            signal("Proven", None, proven_evidence),
        ),
    )


def build_memory(ev: RepositoryEvidence) -> Element:
    recorded_score = 0
    recorded_evidence: list[str] = []
    recorded_missing: list[str] = []
    memory_dirs = (
        ("docs/decisions", 20),
        ("docs/failures", 20),
        ("docs/conventions", 15),
        ("docs/domain", 10),
    )
    for relative, points in memory_dirs:
        if dir_has_files(ev.root, relative):
            recorded_score += points
            recorded_evidence.append(f"{relative} contains files")
        else:
            recorded_missing.append(f"{relative} is missing or empty")
    real_records = len(ev.decisions) + len(ev.failures)
    if real_records:
        recorded_score += 35
        recorded_evidence.append(f"{real_records} non-template decision or failure records found")
    else:
        recorded_missing.append("No non-template decision or failure records found")

    operationalized_score = 0
    operationalized_evidence: list[str] = []
    operationalized_missing: list[str] = []
    memory_routes = sum(
        1
        for term in ("docs/decisions", "docs/failures", "docs/conventions", "docs/domain")
        if term in ev.agent_text
    )
    operationalized_score += proportional_score(memory_routes, 4, 25)
    if memory_routes:
        operationalized_evidence.append("agent instructions point to memory directories")
    else:
        operationalized_missing.append("Agent instructions do not point to memory directories")
    if ev.failures:
        linked_failures = len(ev.failures) - len(ev.failure_records_missing_detection)
        operationalized_score += proportional_score(linked_failures, len(ev.failures), 35)
        if linked_failures:
            operationalized_evidence.append(f"{linked_failures}/{len(ev.failures)} failure records include detection/prevention linkage")
        if ev.failure_records_missing_detection:
            operationalized_missing.append(f"{len(ev.failure_records_missing_detection)} failure records lack detection/prevention linkage")
    else:
        operationalized_missing.append("No real failure records are available for recurrence-linkage review")
    memory_bound_checks = sum(
        1
        for relative in ("scripts/check_failure_memory.py", "scripts/check_decision_memory.py")
        if relative in ev.bound_checks and ev.bound_checks[relative]
    )
    operationalized_score += proportional_score(memory_bound_checks, 2, 25)
    if memory_bound_checks:
        operationalized_evidence.append("memory checks are visibly bound to validation docs, commands, or CI")
    else:
        operationalized_missing.append("Failure or decision memory checks are not visibly bound")
    if contains_any(ev.docs_text, ("decision-failure-memory", "failure memory", "decision memory", "recurrence", "regression test")):
        operationalized_score += 15
        operationalized_evidence.append("memory guidance explains recurrence or decision review")
    else:
        operationalized_missing.append("Memory guidance does not explain recurrence or decision review")

    proven_evidence = []
    if ev.task_outcomes or ev.effectiveness_reports:
        proven_evidence.append("task outcome or effectiveness evidence exists for later memory evaluation")

    return Element(
        "Memory",
        (
            signal("Recorded", recorded_score, recorded_evidence, recorded_missing),
            signal("Operationalized", operationalized_score, operationalized_evidence, operationalized_missing),
            signal("Proven", None, proven_evidence),
        ),
    )


def build_evaluation(ev: RepositoryEvidence) -> Element:
    exists_score = 0
    exists_evidence: list[str] = []
    exists_missing: list[str] = []
    if path_exists(ev.root, "docs/evaluation.md"):
        exists_score += 25
        exists_evidence.append("docs/evaluation.md exists")
    else:
        exists_missing.append("docs/evaluation.md is missing")
    if path_exists(ev.root, "docs/templates/effectiveness-report.md") or path_exists(ev.root, "docs/templates/task-outcome.yaml"):
        exists_score += 25
        exists_evidence.append("effectiveness report or task outcome template exists")
    else:
        exists_missing.append("Effectiveness report or task outcome template is missing")
    if path_exists(ev.root, "scripts/check_effectiveness_plan.py"):
        exists_score += 20
        exists_evidence.append("scripts/check_effectiveness_plan.py exists")
    else:
        exists_missing.append("Effectiveness plan checker is missing")
    if ev.task_outcomes or ev.effectiveness_reports:
        exists_score += 20
        exists_evidence.append("task outcome or effectiveness report files exist")
    else:
        exists_missing.append("No task outcome or effectiveness report files found")
    if contains_any(ev.repository_text, ("not proof of agent effectiveness", "do not prove", "not treated as effectiveness proof", "harness health")):
        exists_score += 10
        exists_evidence.append("docs separate harness health from agent effectiveness")
    else:
        exists_missing.append("Docs do not clearly separate harness health from agent effectiveness")

    coverage_score = 0
    coverage_evidence: list[str] = []
    coverage_missing: list[str] = []
    if contains_any(ev.repository_text, ("effectiveness measurement plan", "baseline available", "primary metric", "results location")):
        coverage_score += 25
        coverage_evidence.append("adoption or evaluation docs require an effectiveness measurement plan")
    else:
        coverage_missing.append("Effectiveness measurement plan fields are not visible")
    task_outcome_text = read_text(ev.root / "docs/templates/task-outcome.yaml")
    required_fields = (
        "repository_ref",
        "prompt_ref",
        "run_id",
        "reviewer",
        "verification_command",
        "first_pass_verification",
    )
    field_count = sum(1 for field in required_fields if field in task_outcome_text)
    coverage_score += proportional_score(field_count, len(required_fields), 20)
    if field_count:
        coverage_evidence.append(f"task outcome template includes {field_count}/{len(required_fields)} comparison fields")
    else:
        coverage_missing.append("Task outcome comparison fields are missing")
    if ev.bound_checks.get("scripts/check_effectiveness_plan.py", False):
        coverage_score += 25
        coverage_evidence.append("effectiveness plan checker is bound to docs, commands, or CI")
    else:
        coverage_missing.append("Effectiveness plan checker is not visibly bound")
    if contains_any(ev.repository_text, ("baseline-vs-harnessed", "harnessed-only", "wrong-file edits", "human rework", "first-pass verification")):
        coverage_score += 20
        coverage_evidence.append("evaluation docs describe comparable outcome metrics")
    else:
        coverage_missing.append("Comparable outcome metric language is missing")
    if contains_any(ev.repository_text, ("task outcome evidence", "include_in_comparable_product_task_count", "include_in_effectiveness_report")):
        coverage_score += 10
        coverage_evidence.append("task outcome inclusion rules are visible")
    else:
        coverage_missing.append("Task outcome inclusion rules are missing")

    proven_evidence = []
    if ev.task_outcomes or ev.effectiveness_reports:
        proven_evidence.append("task outcome or effectiveness files exist; inspect comparability before making outcome claims")

    return Element(
        "Evaluation",
        (
            signal("Exists", exists_score, exists_evidence, exists_missing),
            signal("Coverage", coverage_score, coverage_evidence, coverage_missing),
            signal("Proven", None, proven_evidence),
        ),
    )


def build_governance(ev: RepositoryEvidence) -> Element:
    exists_score = 0
    exists_evidence: list[str] = []
    exists_missing: list[str] = []
    command_count = sum(
        1
        for relative in (
            "commands/harness-doctor.md",
            "commands/harness-update.md",
            "commands/harness-refresh.md",
            "commands/harness-review.md",
        )
        if path_exists(ev.root, relative)
    )
    exists_score += proportional_score(command_count, 4, 30)
    if command_count:
        exists_evidence.append(f"{command_count}/4 harness command workflow docs found")
    else:
        exists_missing.append("Harness command workflow docs are missing")
    if contains_any(ev.agent_text, ("commit", "pr", "pull request", "dirty", "worktree", "stage")):
        exists_score += 20
        exists_evidence.append("agent instructions include commit, PR, or dirty-worktree guidance")
    else:
        exists_missing.append("Commit, PR, or dirty-worktree guidance is missing")
    if contains_any(ev.agent_text + ev.docs_text, ("approval", "explicit approval", "do not delete", "do not overwrite", "do not move", "archive", "re-clone")):
        exists_score += 20
        exists_evidence.append("approval gates for destructive or broad changes are visible")
    else:
        exists_missing.append("Approval gates for deleting, moving, overwriting, archiving, or re-cloning are missing")
    if path_exists(ev.root, ".harness/source.json") or contains_any(ev.repository_text, (".harness/source.json", "source tracking")):
        exists_score += 15
        exists_evidence.append("harness source tracking is present or documented")
    else:
        exists_missing.append("Harness source tracking is not present or documented")
    if contains_any(ev.repository_text, ("diagnostic only", "sub-agent", "pre-push", "review timing", "manual review")):
        exists_score += 15
        exists_evidence.append("diagnostic, review timing, sub-agent, or manual-review governance is visible")
    else:
        exists_missing.append("Diagnostic, review timing, sub-agent, or manual-review governance is missing")

    coverage_score = 0
    coverage_evidence: list[str] = []
    coverage_missing: list[str] = []
    if contains_any(ev.agent_text + ev.docs_text, ("source of truth", "preserve existing", "target repository is the source of truth")):
        coverage_score += 25
        coverage_evidence.append("source-of-truth governance is documented")
    else:
        coverage_missing.append("Source-of-truth governance is missing")
    if contains_any(ev.agent_text + ev.docs_text, ("delete", "move", "archive", "overwrite", "explicit approval")):
        coverage_score += 20
        coverage_evidence.append("destructive-change approval coverage is documented")
    else:
        coverage_missing.append("Destructive-change approval coverage is missing")
    if contains_any(ev.agent_text, ("dirty", "worktree", "git status", "commit", "pr", "pull request")):
        coverage_score += 15
        coverage_evidence.append("git hygiene coverage is documented")
    else:
        coverage_missing.append("Git hygiene coverage is missing")
    if command_count >= 3 or contains_any(ev.repository_text, ("/harness update", "/harness refresh", "/harness review")):
        coverage_score += 25
        coverage_evidence.append("update, refresh, or review governance paths are documented")
    else:
        coverage_missing.append("Update, refresh, or review governance paths are missing")
    if contains_any(ev.repository_text, ("diagnostic only", "must not modify", "do not modify files")):
        coverage_score += 15
        coverage_evidence.append("diagnostic-only or non-mutating command coverage is documented")
    else:
        coverage_missing.append("Diagnostic-only or non-mutating command coverage is missing")

    proven_evidence = []
    if ev.task_outcomes or ev.effectiveness_reports:
        proven_evidence.append("outcome evidence exists but governance effectiveness is not scored by Doctor")

    return Element(
        "Governance",
        (
            signal("Exists", exists_score, exists_evidence, exists_missing),
            signal("Coverage", coverage_score, coverage_evidence, coverage_missing),
            signal("Proven", None, proven_evidence),
        ),
    )


def coupling_findings(ev: RepositoryEvidence) -> tuple[CouplingFinding, ...]:
    findings: list[CouplingFinding] = []
    unbound_known = [
        relative
        for relative, bound in ev.bound_checks.items()
        if not bound
    ]
    for relative in unbound_known:
        findings.append(
            CouplingFinding(
                "warning",
                "Orphan Constraint",
                f"{relative} exists, but no visible docs, command, or CI binding was found.",
            )
        )
    for path in ev.unknown_checks:
        relative = relative_path(ev.root, path)
        if not check_is_bound(ev.root, relative, ev.binding_text):
            findings.append(
                CouplingFinding(
                    "warning",
                    "Orphan Constraint",
                    f"{relative} exists, but its validation binding is not visible.",
                )
            )
    command_refs = check_references(command_reference_text(ev))
    missing_workflow_refs = []
    for relative in command_refs:
        if not path_exists(ev.root, relative):
            missing_workflow_refs.append(relative)
    for relative in sorted(set(missing_workflow_refs)):
        findings.append(
            CouplingFinding(
                "critical",
                "Orphan Feedback",
                f"A workflow or local command references {relative}, but the local script was not found.",
            )
        )
    purpose = purpose_text(ev)
    for relative in command_refs:
        if relative in KNOWN_CHECKS or not path_exists(ev.root, relative):
            continue
        if not check_has_documented_purpose(ev.root, relative, purpose):
            findings.append(
                CouplingFinding(
                    "warning",
                    "Orphan Feedback",
                    f"{relative} is run by a workflow or local command, but no README, AGENTS, validation, convention, domain, or checklist purpose was found.",
                )
            )
    for path in ev.failure_records_missing_detection:
        findings.append(
            CouplingFinding(
                "critical",
                "Unoperationalized Memory",
                f"{relative_path(ev.root, path)} lacks a Detection Or Prevention Check section with a concrete recurrence signal.",
            )
        )
    if (ev.decisions or ev.failures) and not contains_any(ev.agent_text, ("docs/decisions", "docs/failures")):
        findings.append(
            CouplingFinding(
                "warning",
                "Unoperationalized Memory",
                "Decision or failure records exist, but agent instructions do not route future agents to them.",
            )
        )
    if (ev.decisions or ev.failures) and not (ev.included_task_outcomes or ev.local_effectiveness_reports):
        findings.append(
            CouplingFinding(
                "warning",
                "Unevaluated Memory",
                "Decision or failure records exist, but no included task outcome or local effectiveness report evidence was found.",
            )
        )
    if not contains_any(ev.agent_text + ev.docs_text, ("delete", "move", "archive", "overwrite", "explicit approval")):
        findings.append(
            CouplingFinding(
                "warning",
                "Ungoverned Change Type",
                "No explicit approval path was found for deleting, moving, archiving, or overwriting files.",
            )
        )
    if not contains_any(ev.agent_text + ev.docs_text, ("/harness review", "review timing", "pre-push", "manual review", "sub-agent")):
        findings.append(
            CouplingFinding(
                "warning",
                "Ungoverned Change Type",
                "No durable review path was found for substantial harness or integration-boundary changes.",
            )
        )
    if ev.failures and not dir_has_files(ev.root, "docs/conventions"):
        findings.append(
            CouplingFinding(
                "info",
                "Promotion Gap",
                "Failure records exist, but no conventions directory was found; review whether repeated failures need promotion.",
            )
        )
    elif ev.failures and not contains_any(ev.docs_text, ("convention", "agent guidance", "do not repeat", "recurrence")):
        findings.append(
            CouplingFinding(
                "info",
                "Promotion Gap",
                "Failure records exist; review whether repeated failures should be promoted into instructions, conventions, constraints, or checks.",
            )
        )
    return tuple(findings)


def analyze_repository(root: Path) -> DoctorResult:
    ev = collect_evidence(root)
    elements = (
        build_instructions(ev),
        build_constraints(ev),
        build_feedback(ev),
        build_memory(ev),
        build_evaluation(ev),
        build_governance(ev),
    )
    evidence: list[str] = []
    missing: list[str] = []
    for element in elements:
        for item in element.signals:
            evidence.extend(f"{element.name}/{item.name}: {value}" for value in item.evidence)
            missing.extend(f"{element.name}/{item.name}: {value}" for value in item.missing)
    return DoctorResult(
        elements=elements,
        findings=coupling_findings(ev),
        evidence=tuple(evidence),
        missing=tuple(missing),
    )


def grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B+"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def verdict(score: int, findings: tuple[CouplingFinding, ...]) -> str:
    critical_count = sum(1 for finding in findings if finding.severity == "critical")
    if score >= 90 and not critical_count:
        return "Production-ready baseline evidence with no critical coupling findings detected."
    if score >= 80:
        return "Strong baseline evidence; review coupling findings before treating the harness loop as complete."
    if score >= 70:
        return "Useful but incomplete baseline evidence; the next improvements should reconnect weak harness loops."
    if score >= 60:
        return "Basic baseline evidence; several harness elements or bindings are still thin."
    if score >= 40:
        return "Mostly ad-hoc baseline evidence; future agents may still depend on session-scoped context."
    return "Little durable baseline evidence for reliable coding-agent collaboration."


def top_risks(result: DoctorResult) -> list[str]:
    risks: list[str] = []
    critical = [finding for finding in result.findings if finding.severity == "critical"]
    warnings = [finding for finding in result.findings if finding.severity == "warning"]
    for finding in critical + warnings:
        risks.append(f"{finding.kind}: {finding.detail}")
        if len(risks) >= 3:
            return risks
    weak_elements = sorted(result.elements, key=lambda element: element.score)
    for element in weak_elements:
        if element.score < 70:
            risks.append(f"{element.name} is thin at {element.score}/100.")
        if len(risks) >= 3:
            return risks
    return risks or ["No major baseline risks detected by this scan."]


def recommended_actions(result: DoctorResult) -> list[str]:
    actions: list[str] = []
    for finding in result.findings:
        if finding.kind == "Orphan Constraint":
            actions.append("Wire unbound check scripts into local validation docs, package scripts, CI, or an explicit manual review point.")
        elif finding.kind == "Orphan Feedback":
            actions.append("Fix workflow references so every feedback signal points to an existing local script or documented rule.")
        elif finding.kind == "Unoperationalized Memory":
            actions.append("Connect decision or failure records to agent instructions, recurrence checks, CI gates, or manual review points.")
        elif finding.kind == "Unevaluated Memory":
            actions.append("Record task outcomes or effectiveness evidence for future comparable agent tasks.")
        elif finding.kind == "Ungoverned Change Type":
            actions.append("Document approval and review paths for destructive, broad, or high-risk harness changes.")
        elif finding.kind == "Promotion Gap":
            actions.append("Review repeated failures and promote stable lessons into instructions, conventions, constraints, or checks.")
        if len(actions) >= 3:
            break
    if len(actions) < 3:
        weak_elements = sorted(result.elements, key=lambda element: element.score)
        for element in weak_elements:
            if element.name == "Instructions" and element.score < 80:
                actions.append("Add or tighten agent instructions with exact commands, boundaries, safety notes, and routes to deeper docs.")
            elif element.name == "Constraints" and element.score < 80:
                actions.append("Add enforceable drift, structure, lint, type, or dependency-boundary checks for important rules.")
            elif element.name == "Feedback" and element.score < 80:
                actions.append("Document and wire the normal validation gate through local commands or CI.")
            elif element.name == "Memory" and element.score < 80:
                actions.append("Add real decision or failure records and link failures to recurrence-detection checks.")
            elif element.name == "Evaluation" and element.score < 80:
                actions.append("Add an effectiveness plan, task outcome template, or outcome records without treating them as proof by default.")
            elif element.name == "Governance" and element.score < 80:
                actions.append("Add source-of-truth, approval, review, update, refresh, or git hygiene rules.")
            if len(actions) >= 3:
                break
    deduped: list[str] = []
    for action in actions:
        if action not in deduped:
            deduped.append(action)
    return deduped[:3] or ["Keep existing harness evidence current and rerun Doctor after substantial harness changes."]


def print_report(root: Path, result: DoctorResult) -> None:
    score = result.score
    print("Harness Doctor Report")
    print()
    print(f"Score: {score}/100 (six-element baseline coupling scan)")
    print(f"Grade: {grade(score)} (baseline)")
    print()
    print("Verdict:")
    print(
        f"{verdict(score, result.findings)} This scan checks durable files and text "
        "patterns; review content quality before treating it as final."
    )
    print()
    print("Element Breakdown:")
    for element in result.elements:
        statuses = " · ".join(f"{signal.name} {signal.status}" for signal in element.signals)
        print(f"- {element.name}: {element.score}/100 | {statuses}")
    print()
    print("Coupling Findings:")
    if result.findings:
        for finding in result.findings:
            print(f"- {finding.severity} {finding.kind}: {finding.detail}")
    else:
        print("- No coupling findings detected by this scan.")
    print()
    print("Evidence:")
    if result.evidence:
        for item in result.evidence[:18]:
            print(f"- {item}")
        if len(result.evidence) > 18:
            print(f"- ... {len(result.evidence) - 18} more evidence items")
    else:
        print("- No baseline evidence detected.")
    print()
    print("Missing Or Weak Baseline Items:")
    if result.missing:
        for item in result.missing[:18]:
            print(f"- {item}")
        if len(result.missing) > 18:
            print(f"- ... {len(result.missing) - 18} more missing or weak items")
    else:
        print("- No missing baseline items detected.")
    print()
    print("Non-Scored Manual Review:")
    if any(signal.name == "Proven" and signal.evidence for element in result.elements for signal in element.signals):
        print("- Proven effectiveness: outcome evidence exists; inspect comparability before making improvement claims.")
    else:
        print("- Proven effectiveness: unmeasured; no task outcome or effectiveness evidence was found.")
    print("- Runtime execution/tooling: out of scope except for repository-visible commands, CI, scripts, and approval paths.")
    print()
    print("Top Risks:")
    for index, risk in enumerate(top_risks(result), start=1):
        print(f"{index}. {risk}")
    print()
    print("Recommended Next Actions:")
    for index, action in enumerate(recommended_actions(result), start=1):
        print(f"{index}. {action}")
    print()
    print("Note:")
    print(
        "This script does not modify files, does not replace agent judgment, "
        "and does not score agent effectiveness or runtime-only execution/tool protocols."
    )


def main() -> int:
    args = parse_args()
    root = Path(args.target).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Target is not a directory: {root}")
        return 2

    result = analyze_repository(root)
    print_report(root, result)

    failed = False
    if args.min_score is not None and result.score < args.min_score:
        print()
        print(f"Gate failed: score {result.score}/100 is below --min-score {args.min_score}.")
        failed = True
    if "critical-coupling" in args.fail_on and any(
        finding.severity == "critical" for finding in result.findings
    ):
        print()
        print("Gate failed: critical coupling findings are present.")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

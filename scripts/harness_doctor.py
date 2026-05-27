#!/usr/bin/env python3
"""Produce a baseline Harness Doctor score for a repository."""

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


@dataclass(frozen=True)
class Check:
    label: str
    points: int
    found: bool
    evidence: str


@dataclass(frozen=True)
class Category:
    name: str
    checks: tuple[Check, ...]

    @property
    def score(self) -> int:
        return sum(check.points for check in self.checks if check.found)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan a repository for baseline Harness Doctor evidence. The score "
            "is a starting point; content quality still needs agent review."
        )
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def iter_text_files(root: Path, limit: int = 800) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if len(files) >= limit:
            break
        rel = path.relative_to(root)
        if path.is_file() and not is_ignored(rel) and path.suffix in TEXT_EXTENSIONS:
            files.append(path)
    return files


def joined_text(paths: list[Path]) -> str:
    return "\n".join(read_text(path) for path in paths)


def path_exists(root: Path, relative: str) -> bool:
    return (root / relative).exists()


def dir_has_files(root: Path, relative: str) -> bool:
    path = root / relative
    return path.is_dir() and any(child.is_file() for child in path.rglob("*"))


def first_existing(root: Path, relatives: tuple[str, ...]) -> str | None:
    for relative in relatives:
        if path_exists(root, relative):
            return relative
    return None


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
    return any(regex.search(name) or regex.search(value) for name, value in package_scripts(root).items())


def files_matching(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(matches))


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def has_command_text(text: str, terms: tuple[str, ...]) -> bool:
    command_terms = "|".join(re.escape(term) for term in terms)
    return bool(re.search(rf"\b({command_terms})\b", text, flags=re.IGNORECASE))


def agent_instruction_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in AGENT_INSTRUCTION_PATHS:
        path = root / relative
        if path.is_file():
            files.append(path)
        if path.is_dir():
            files.extend(sorted(child for child in path.rglob("*") if child.is_file()))
    return files


def is_placeholder_record(path: Path, text: str) -> bool:
    name = path.name.lower()
    lowered = text.lower()
    placeholder_terms = (
        "todo",
        "yyyy-mm-dd",
        "template",
        "placeholder",
        "entrypoint",
        "entry point",
        "no known",
    )
    return (
        name == "readme.md"
        or "template" in name
        or any(term in lowered for term in placeholder_terms)
    )


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
            records.append(path)
    return records


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


def relative_evidence(root: Path, path: Path | None, fallback: str) -> str:
    if path is None:
        return fallback
    return str(path.relative_to(root))


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


def verdict(score: int) -> str:
    if score >= 90:
        return "Production-ready harness"
    if score >= 80:
        return "Strong harness"
    if score >= 70:
        return "Useful but incomplete"
    if score >= 60:
        return "Basic harness"
    if score >= 40:
        return "Mostly ad-hoc"
    return "No durable agent harness"


def score_repository(root: Path) -> list[Category]:
    text_files = iter_text_files(root)
    repository_text = joined_text(text_files)
    agent_files = agent_instruction_files(root)
    agent_text = joined_text(agent_files)
    readme_text = read_text(root / "README.md")
    workflows = workflow_files(root)
    workflow_text = joined_text(workflows)

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

    categories = [
        Category(
            "Agent Instructions",
            (
                Check(
                    "Agent instruction file exists",
                    5,
                    bool(agent_files),
                    relative_evidence(root, agent_files[0] if agent_files else None, "No agent instruction file found"),
                ),
                Check(
                    "Project overview is clear",
                    3,
                    contains_any(agent_text + readme_text, ("overview", "purpose", "this repository", "project")),
                    "README or agent instructions describe the project",
                ),
                Check(
                    "Exact build/test/lint commands exist",
                    4,
                    has_command_text(agent_text + readme_text, exact_command_terms),
                    "README or agent instructions include command-like text",
                ),
                Check(
                    "Architecture boundaries are documented",
                    4,
                    contains_any(agent_text, ("architecture", "boundary", "directory rules", "constraints", "do not import")),
                    "Agent instructions mention architecture boundaries or constraints",
                ),
                Check(
                    "Forbidden actions are documented",
                    2,
                    contains_any(agent_text, ("forbidden", "do not", "never", "must not")),
                    "Agent instructions include forbidden actions",
                ),
                Check(
                    "Security/safety notes exist",
                    2,
                    contains_any(agent_text, ("security", "secret", "credential", "safety", "privacy", "destructive")),
                    "Agent instructions include safety or security notes",
                ),
            ),
        ),
        Category(
            "Feedback Loops",
            (
                Check(
                    "Test command exists",
                    4,
                    has_script_matching(root, r"test")
                    or has_command_text(repository_text, ("pytest", "unittest", "npm test", "go test", "mvn test", "gradle test", "cargo test")),
                    "A test command appears in scripts or documentation",
                ),
                Check(
                    "Lint command exists",
                    4,
                    has_script_matching(root, r"lint|ruff|eslint|flake8")
                    or has_command_text(repository_text, ("lint", "ruff", "eslint", "flake8", "pylint")),
                    "A lint command appears in scripts or documentation",
                ),
                Check(
                    "Typecheck command exists",
                    3,
                    has_script_matching(root, r"typecheck|type-check|mypy|tsc|pyright")
                    or has_command_text(repository_text, ("typecheck", "type-check", "mypy", "tsc", "pyright")),
                    "A typecheck command appears in scripts or documentation",
                ),
                Check(
                    "CI workflow exists",
                    5,
                    bool(workflows),
                    relative_evidence(root, workflows[0] if workflows else None, "No CI workflow found"),
                ),
                Check(
                    "Pre-commit or local validation script exists",
                    2,
                    path_exists(root, ".pre-commit-config.yaml")
                    or path_exists(root, ".pre-commit-config.yml")
                    or has_script_matching(root, r"check|validate|verify")
                    or bool(files_matching(root, ("Makefile", "scripts/check_*.py"))),
                    "Pre-commit config, check script, or validation command found",
                ),
                Check(
                    "Validation instructions are documented",
                    2,
                    contains_any(agent_text + readme_text, ("local checks", "validation", "run these checks", "before committing")),
                    "README or agent instructions document validation",
                ),
            ),
        ),
        Category(
            "Durable Memory",
            (
                Check("docs/decisions exists", 5, dir_has_files(root, "docs/decisions"), "docs/decisions contains files"),
                Check("docs/failures exists", 5, dir_has_files(root, "docs/failures"), "docs/failures contains files"),
                Check("docs/conventions exists", 4, dir_has_files(root, "docs/conventions"), "docs/conventions contains files"),
                Check("docs/domain exists", 3, dir_has_files(root, "docs/domain"), "docs/domain contains files"),
                Check(
                    "At least one real decision or failure record exists",
                    3,
                    bool(non_template_records(root, ("docs/decisions", "docs/failures"))),
                    "Non-template decision or failure record found",
                ),
            ),
        ),
        Category(
            "Structural Safety",
            (
                Check(
                    "Structure check script exists",
                    5,
                    bool(files_matching(root, ("scripts/check_structure.py", "scripts/*structure*"))),
                    "Structure check script found",
                ),
                Check(
                    "Docs drift check exists",
                    4,
                    bool(files_matching(root, ("scripts/check_docs_drift.py", "scripts/*docs*drift*"))),
                    "Docs drift check script found",
                ),
                Check(
                    "Generated file protection exists",
                    3,
                    contains_any(repository_text, ("generated", "do not edit", "generated files"))
                    or contains_any(read_text(root / ".gitignore"), ("dist", "build", "generated")),
                    "Generated file protection appears in docs, checks, or ignore rules",
                ),
                Check(
                    "Forbidden path checks exist",
                    3,
                    contains_any(repository_text, ("forbidden_patterns", "forbidden path", "forbidden drift-prone", "forbidden_paths")),
                    "Forbidden path checks appear in scripts or rules",
                ),
                Check(
                    "Architecture/dependency boundary checks exist",
                    3,
                    contains_any(repository_text, ("dependency boundary", "import boundary", "no-restricted-imports", "depcruise", "dependency-cruiser")),
                    "Architecture or dependency boundary checks appear in repository files",
                ),
                Check(
                    "CI runs at least one structural check",
                    2,
                    contains_any(workflow_text, ("check_structure", "check_docs_drift", "harness_doctor", "docs drift", "structure")),
                    "CI references a structural or drift check",
                ),
            ),
        ),
        Category(
            "Adoption Clarity",
            (
                Check(
                    "README explains harness purpose",
                    4,
                    contains_any(readme_text, ("harness", "agent", "purpose", "ai coding")),
                    "README explains harness purpose",
                ),
                Check("Quickstart exists", 4, "quick start" in readme_text.lower() or "quickstart" in readme_text.lower(), "README includes quickstart"),
                Check(
                    "Before/after example exists",
                    4,
                    contains_any(repository_text, ("before/after", "before and after", "adoption report", "example reports")),
                    "Before/after or adoption examples found",
                ),
                Check(
                    "Adoption report template exists",
                    3,
                    path_exists(root, "docs/templates/adoption-report.md"),
                    "docs/templates/adoption-report.md exists",
                ),
                Check(
                    "Profiles/examples exist",
                    3,
                    path_exists(root, "templates/profiles") or path_exists(root, "examples"),
                    "Profiles or examples directory exists",
                ),
                Check(
                    "Known limitations are documented",
                    2,
                    contains_any(readme_text, ("known limitations", "not automatic", "does not", "limitations")),
                    "README documents limitations or non-goals",
                ),
            ),
        ),
    ]
    return categories


def print_report(root: Path, categories: list[Category]) -> None:
    score = sum(category.score for category in categories)
    print("Harness Doctor Report")
    print()
    print(f"Score: {score}/100")
    print(f"Grade: {grade(score)}")
    print()
    print("Verdict:")
    print(f"{verdict(score)}. This baseline is based on file and text evidence; review content quality before treating it as final.")
    print()
    print("Breakdown:")
    for category in categories:
        print(f"- {category.name}: {category.score}/20")
    print()
    print("Evidence:")
    for category in categories:
        for check in category.checks:
            if check.found:
                print(f"- {check.label}: {check.evidence}")
    print()
    print("Missing Or Weak Baseline Items:")
    missing = [
        (category.name, check)
        for category in categories
        for check in category.checks
        if not check.found
    ]
    if missing:
        for category_name, check in missing:
            print(f"- {category_name}: {check.label} ({check.points} pts)")
    else:
        print("- No missing baseline items detected.")
    print()
    print("Note:")
    print("This script does not modify files and does not replace agent judgment.")


def main() -> int:
    args = parse_args()
    root = Path(args.target).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Target is not a directory: {root}")
        return 2

    print_report(root, score_repository(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

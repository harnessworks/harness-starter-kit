#!/usr/bin/env python3
"""Bootstrap a generic harness skeleton into a target repository.

This script does not perform full harness adoption. For real adoption, use the
prompt-first workflow so an agent can inspect and adapt to the target repo.
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".txt",
    ".mjs",
    ".js",
}

IGNORED_TEMPLATE_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}

OPTIONAL_CI_PATHS = {
    Path(".github") / "workflows" / "harness-check.yml",
}


@dataclass(frozen=True)
class CopyResult:
    source: Path
    destination: Path
    action: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Bootstrap generic harness skeleton files into a target repo. "
            "Full harness adoption is prompt-first and agent-driven."
        )
    )
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        help="Target repository directory.",
    )
    parser.add_argument(
        "--profile",
        choices=(
            "generic",
            "python",
            "typescript",
            "nextjs",
            "django",
            "flask",
            "spring",
            "android",
            "fastapi",
            "react",
            "vue",
            "go",
            "rust",
        ),
        default="generic",
        help="Optional stack profile. Profiles add reference snippets only.",
    )
    parser.add_argument(
        "--project-name",
        help="Project name to render into templates. Defaults to target folder name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show skeleton files that would be written without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    parser.add_argument(
        "--with-ci",
        action="store_true",
        help="Also copy the optional GitHub Actions harness workflow skeleton.",
    )
    return parser.parse_args()


def render_text(value: str, project_name: str, profile: str) -> str:
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROFILE}}": profile,
    }
    for key, replacement in replacements.items():
        value = value.replace(key, replacement)
    return value


def copy_tree(
    source_root: Path,
    target_root: Path,
    project_name: str,
    profile: str,
    dry_run: bool,
    force: bool,
    include_ci: bool,
) -> list[CopyResult]:
    results: list[CopyResult] = []

    for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
        relative = source.relative_to(source_root)
        if any(part in IGNORED_TEMPLATE_PARTS for part in relative.parts):
            continue
        if not include_ci and relative in OPTIONAL_CI_PATHS:
            continue
        destination = target_root / relative

        if destination.exists() and not force:
            results.append(CopyResult(source, destination, "skip-existing"))
            continue

        action = "overwrite" if destination.exists() else "create"
        results.append(CopyResult(source, destination, action))

        if dry_run:
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in TEXT_SUFFIXES:
            content = source.read_text(encoding="utf-8")
            destination.write_text(
                render_text(content, project_name, profile),
                encoding="utf-8",
            )
        else:
            shutil.copy2(source, destination)

    return results


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    target = args.target.resolve()
    project_name = args.project_name or target.name

    if not target.exists():
        raise SystemExit(f"Target directory does not exist: {target}")
    if not target.is_dir():
        raise SystemExit(f"Target is not a directory: {target}")

    generic_root = repo_root / "templates" / "generic"
    profile_root = repo_root / "templates" / "profiles" / args.profile

    results: list[CopyResult] = []
    results.extend(
        copy_tree(
            generic_root,
            target,
            project_name,
            args.profile,
            args.dry_run,
            args.force,
            args.with_ci,
        )
    )

    if args.profile != "generic":
        profile_destination = target / "docs" / "harness" / "profiles" / args.profile
        results.extend(
            copy_tree(
                profile_root,
                profile_destination,
                project_name,
                args.profile,
                args.dry_run,
                args.force,
                True,
            )
        )

    for result in results:
        print(f"{result.action:14} {result.destination}")

    created = sum(1 for result in results if result.action == "create")
    overwritten = sum(1 for result in results if result.action == "overwrite")
    skipped = sum(1 for result in results if result.action == "skip-existing")

    print()
    print(
        f"Summary: {created} created, {overwritten} overwritten, {skipped} skipped."
    )
    if args.dry_run:
        print("Dry run only. No files were written.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

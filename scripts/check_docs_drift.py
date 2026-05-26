#!/usr/bin/env python3
"""Detect stale file and command references in agent-facing docs."""

from __future__ import annotations

import re
import shlex
import sys
from pathlib import Path


DOC_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
)

IGNORED_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
)

OPTIONAL_REFERENCES = {
    "CLAUDE.md",
    "./harness-starter-kit",
    "target-repo/harness-starter-kit",
}


def iter_existing_docs(root: Path) -> list[Path]:
    docs = [root / name for name in DOC_FILES if (root / name).exists()]
    docs.extend(sorted((root / "docs").rglob("*.md")) if (root / "docs").exists() else [])
    return docs


def extract_backtick_references(text: str) -> set[str]:
    return set(re.findall(r"`([^`\n]+)`", text))


def looks_like_path(reference: str) -> bool:
    if reference in OPTIONAL_REFERENCES:
        return False
    if reference.startswith(IGNORED_PREFIXES):
        return False
    if any(token in reference for token in ("*", "<", ">", "{{", "}}")):
        return False
    if " " in reference:
        return False
    return "/" in reference or "\\" in reference or reference in DOC_FILES


def referenced_path_exists(root: Path, doc: Path, reference: str) -> bool:
    normalized = reference.strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return (root / normalized).exists() or (doc.parent / normalized).exists()


def looks_like_command(reference: str) -> bool:
    command_roots = {
        "python",
        "pytest",
        "npm",
        "pnpm",
        "yarn",
        "ruff",
        "mypy",
        "pre-commit",
        "eslint",
        "tsc",
    }
    try:
        first = shlex.split(reference, posix=False)[0]
    except (IndexError, ValueError):
        return False
    return first in command_roots


def check_docs(root: Path) -> int:
    missing_paths: list[tuple[Path, str]] = []

    for doc in iter_existing_docs(root):
        text = doc.read_text(encoding="utf-8")
        for reference in sorted(extract_backtick_references(text)):
            if looks_like_command(reference):
                continue
            if looks_like_path(reference) and not referenced_path_exists(
                root, doc, reference
            ):
                missing_paths.append((doc, reference))

    for doc, reference in missing_paths:
        print(f"Missing referenced path in {doc.relative_to(root)}: {reference}")

    return 1 if missing_paths else 0


def main() -> int:
    return check_docs(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())


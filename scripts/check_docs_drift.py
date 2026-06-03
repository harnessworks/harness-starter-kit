#!/usr/bin/env python3
"""Detect stale file references and broken local Markdown links in docs."""

from __future__ import annotations

from dataclasses import dataclass
import re
import shlex
from pathlib import Path
from urllib.parse import unquote, urlsplit


DOC_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
)

IGNORED_SCHEMES = {"http", "https", "mailto"}

OPTIONAL_REFERENCES = {
    "CLAUDE.md",
    ".gradle",
    ".gradle/",
    ".cxx",
    ".cxx/",
    ".next",
    ".next/",
    ".harness/source.json",
    ".venv",
    ".venv/",
    ".vite",
    ".vite/",
    "coverage",
    "coverage/",
    "captures",
    "captures/",
    "db.sqlite3",
    "dist",
    "dist/",
    "build",
    "build/",
    "harness-starter-kit",
    "harness-starter-kit/",
    "instance",
    "instance/",
    "node_modules",
    "node_modules/",
    "out",
    "out/",
    "target",
    "target/",
    "vendor",
    "vendor/",
    "target-repo/harness-starter-kit",
    "scripts/check_harness.py",
    "tsconfig.tsbuildinfo",
    "venv",
    "venv/",
}

OPTIONAL_REFERENCE_PREFIXES = (
    ".venv/",
    "venv/",
    "env/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    "__pycache__/",
    ".gradle/",
    ".vite/",
    "node_modules/",
    "target/",
)

BACKTICK_RE = re.compile(r"`([^`\n]+)`")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
PLACEHOLDER_TOKENS = ("*", "...", "<", ">", "{{", "}}")


@dataclass(frozen=True)
class Reference:
    value: str
    source: str


def iter_existing_docs(root: Path) -> list[Path]:
    docs = [root / name for name in DOC_FILES if (root / name).exists()]
    docs.extend(sorted((root / "docs").rglob("*.md")) if (root / "docs").exists() else [])
    return docs


def clean_markdown_link_target(target: str) -> str:
    value = target.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing != -1:
            return value[1:closing].strip()

    try:
        parts = shlex.split(value, posix=True)
    except ValueError:
        parts = value.split()
    return parts[0] if parts else ""


def extract_references(text: str) -> set[Reference]:
    references = {
        Reference(value=match, source="inline-code")
        for match in BACKTICK_RE.findall(text)
    }
    references.update(
        Reference(value=target, source="markdown-link")
        for target in (
            clean_markdown_link_target(match)
            for match in MARKDOWN_LINK_RE.findall(text)
        )
        if target
    )
    return references


def is_external_reference(reference: str) -> bool:
    parts = urlsplit(reference.strip())
    return bool(parts.scheme and (parts.scheme in IGNORED_SCHEMES or "://" in reference))


def normalize_reference(reference: str) -> str:
    value = reference.strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1].strip()

    parts = urlsplit(value)
    path = unquote(parts.path).replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path


def is_ignored_reference(reference: str) -> bool:
    if is_external_reference(reference):
        return True
    if reference.strip().startswith("#"):
        return True
    if any(token in reference for token in PLACEHOLDER_TOKENS):
        return True

    normalized = normalize_reference(reference)
    if not normalized:
        return True
    if normalized in OPTIONAL_REFERENCES:
        return True
    return any(normalized.startswith(prefix) for prefix in OPTIONAL_REFERENCE_PREFIXES)


def looks_like_path(reference: Reference) -> bool:
    if is_ignored_reference(reference.value):
        return False

    normalized = normalize_reference(reference.value)
    if " " in normalized:
        return False
    if reference.source == "markdown-link":
        return True
    return "/" in normalized or "\\" in reference.value or normalized in DOC_FILES


def referenced_path_exists(root: Path, doc: Path, reference: str) -> bool:
    normalized = normalize_reference(reference)
    path = Path(normalized)
    if path.is_absolute():
        return path.exists()
    return (root / path).exists() or (doc.parent / path).exists()


def looks_like_command(reference: str) -> bool:
    command_roots = {
        "python",
        "python.exe",
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
    normalized = normalize_reference(first)
    command_name = Path(normalized).name.lower()
    return first in command_roots or command_name in command_roots


def check_docs(root: Path) -> int:
    missing_paths: list[tuple[Path, str]] = []

    for doc in iter_existing_docs(root):
        text = doc.read_text(encoding="utf-8")
        for reference in sorted(extract_references(text), key=lambda item: item.value):
            if reference.source == "inline-code" and looks_like_command(reference.value):
                continue
            if looks_like_path(reference) and not referenced_path_exists(
                root, doc, reference.value
            ):
                missing_paths.append((doc, reference.value))

    for doc, reference_value in missing_paths:
        print(f"Missing referenced path in {doc.relative_to(root)}: {reference_value}")

    return 1 if missing_paths else 0


def main() -> int:
    return check_docs(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())

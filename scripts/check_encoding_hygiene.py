#!/usr/bin/env python3
"""Detect invalid UTF-8 and common mojibake markers in text files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".cfg",
    ".gradle",
    ".java",
    ".js",
    ".json",
    ".kt",
    ".kts",
    ".md",
    ".mjs",
    ".properties",
    ".py",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

DEFAULT_RULES = {
    "ignored_directories": [
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
    ],
    "mojibake_markers": [
        "\ufffd",
        "\u00c3",
        "\u00c2",
        "\u00e2\u20ac\u2122",
        "\u00e2\u20ac\u0153",
        "\u00e2\u20ac\ufffd",
        "\u00ec\u2022",
        "\u00ec\u201e",
        "\u00ec\u2014",
        "\u00ed\u2022",
        "\u00eb\u00a5",
        "\u00eb\u0160",
        "\u00ea\u00b0",
    ],
}


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def load_rules(root: Path) -> dict[str, list[str]]:
    rules_path = root / ".harness" / "encoding-rules.json"
    if not rules_path.exists():
        return DEFAULT_RULES
    return json.loads(rules_path.read_text(encoding="utf-8"))


def is_ignored(path: Path, ignored_directories: set[str]) -> bool:
    return any(part in ignored_directories for part in path.parts)


def iter_text_files(root: Path, ignored_directories: set[str]) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path.suffix in TEXT_EXTENSIONS
        and not is_ignored(path.relative_to(root), ignored_directories)
    ]


def check_encoding(root: Path) -> int:
    rules = load_rules(root)
    ignored_directories = set(rules.get("ignored_directories", []))
    markers = rules.get("mojibake_markers", [])
    findings: list[Finding] = []

    for path in iter_text_files(root, ignored_directories):
        relative = path.relative_to(root)
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            findings.append(
                Finding(relative, f"invalid UTF-8 at byte {exc.start}: {exc.reason}")
            )
            continue

        for marker in markers:
            if marker and marker in text:
                escaped = marker.encode("unicode_escape").decode("ascii")
                findings.append(
                    Finding(relative, f"possible mojibake marker: {escaped}")
                )
                break

    for finding in findings:
        print(f"{finding.path}: {finding.message}")

    return 1 if findings else 0


def main() -> int:
    return check_encoding(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())

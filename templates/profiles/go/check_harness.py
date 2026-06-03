#!/usr/bin/env python3
"""Run local harness checks for a Go project."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    current = Path(__file__).resolve()
    if current.parent.name == "scripts":
        return current.parents[1]

    cwd = Path.cwd()
    if (cwd / "scripts" / "check_docs_drift.py").exists():
        return cwd

    for candidate in (current.parent, *current.parents):
        if (candidate / "go.mod").exists():
            return candidate
    return cwd


ROOT = repo_root()


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Go harness checks.")
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Run only vet and harness drift checks.",
    )
    args = parser.parse_args()

    run(["go", "build", "./..."])
    run(["go", "vet", "./..."])

    lint_configs = (".golangci.yml", ".golangci.yaml", ".golangci.toml")
    if shutil.which("golangci-lint") and any((ROOT / name).exists() for name in lint_configs):
        run(["golangci-lint", "run"])

    if not args.skip_tests:
        run(["go", "test", "-count=1", "./..."])

    run([sys.executable, "scripts/check_docs_drift.py"])
    run([sys.executable, "scripts/check_structure.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

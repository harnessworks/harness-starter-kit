#!/usr/bin/env python3
"""Run local harness checks for a Rust project."""

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
        if (candidate / "Cargo.toml").exists():
            return candidate
    return cwd


ROOT = repo_root()


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Rust harness checks.")
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Run only build, clippy, and harness drift checks.",
    )
    args = parser.parse_args()

    run(["cargo", "build"])

    if shutil.which("cargo-clippy"):
        run(["cargo", "clippy", "--all-targets"])

    if not args.skip_tests:
        run(["cargo", "test"])

    run([sys.executable, "scripts/check_docs_drift.py"])
    run([sys.executable, "scripts/check_structure.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

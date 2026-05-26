#!/usr/bin/env python3
"""Run local harness checks for a Flask project."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WINDOWS_VENV_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
POSIX_VENV_PYTHON = ROOT / ".venv" / "bin" / "python"


def project_python() -> str:
    if WINDOWS_VENV_PYTHON.exists():
        return str(WINDOWS_VENV_PYTHON)
    if POSIX_VENV_PYTHON.exists():
        return str(POSIX_VENV_PYTHON)
    return sys.executable


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Flask harness checks.")
    parser.add_argument(
        "--app",
        default="sample_flask",
        help="Flask app import path for `python -m flask --app ... routes`.",
    )
    parser.add_argument(
        "--tests",
        default="tests",
        help="Test directory for unittest discovery.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    python = project_python()
    run([python, "-m", "unittest", "discover", "-s", args.tests])
    run([python, "-m", "flask", "--app", args.app, "routes"])
    run([python, "scripts/check_docs_drift.py"])
    run([python, "scripts/check_structure.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

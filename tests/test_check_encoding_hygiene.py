from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK = REPO_ROOT / "scripts" / "check_encoding_hygiene.py"


class EncodingHygieneTests(unittest.TestCase):
    def run_check(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECK)],
            cwd=target,
            capture_output=True,
            text=True,
        )

    def test_valid_utf8_localized_text_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "res").mkdir()
            (target / "res" / "strings.xml").write_text(
                (
                    '<resources><string name="hello">'
                    "\uc548\ub155\ud558\uc138\uc694"
                    "</string></resources>\n"
                ),
                encoding="utf-8",
            )

            result = self.run_check(target)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_invalid_utf8_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "bad.md").write_bytes(b"# bad\n\xff\n")

            result = self.run_check(target)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("invalid UTF-8", result.stdout)

    def test_common_mojibake_marker_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "README.md").write_text(
                "Korean text was decoded incorrectly: \u00ec\u2022\u02c6\n",
                encoding="utf-8",
            )

            result = self.run_check(target)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("possible mojibake marker", result.stdout)


if __name__ == "__main__":
    unittest.main()

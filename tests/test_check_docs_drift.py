from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_docs_drift.py"


class CheckDocsDriftTests(unittest.TestCase):
    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=root,
            capture_output=True,
            text=True,
        )

    def test_markdown_links_to_existing_files_and_fragments_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Sample",
                        "[Guide](docs/guide.md#quick-start)",
                        "[License](LICENSE)",
                        "[External](https://example.com/docs)",
                        "[Anchor](#sample)",
                    ]
                ),
                encoding="utf-8",
            )
            (docs / "guide.md").write_text("# Guide\n", encoding="utf-8")

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_missing_markdown_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Sample\n\n[Missing](docs/missing.md)\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("docs/missing.md", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_optional_generated_paths_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Sample",
                        "`node_modules/`",
                        "`./harness-starter-kit`",
                        "`db.sqlite3`",
                        "`target/`",
                        "`.gradle/`",
                        "`.vite/`",
                        "`tsconfig.tsbuildinfo`",
                        "[Local clone](harness-starter-kit/)",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_virtualenv_python_commands_are_not_treated_as_missing_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Sample",
                        "Run:",
                        r"`.\.venv\Scripts\python.exe manage.py check`",
                        r"`.\.venv\Scripts\python.exe scripts\check_harness.py`",
                        "`.venv/bin/python manage.py test`",
                        r"`.\.venv\Scripts\python.exe`",
                        "`.venv/bin/python`",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()

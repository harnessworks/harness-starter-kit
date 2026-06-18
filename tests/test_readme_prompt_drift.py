from __future__ import annotations

import html
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_INDEX = REPO_ROOT / "site" / "index.html"
SWITCHER_LINK_RE = re.compile(
    r"\[(?P<label>[^\]]+)\]\((?P<target>README(?:\.[^)]+)?\.md)\)"
)
CURRENT_LANGUAGE_RE = re.compile(r"\*\*(?P<label>[^*]+)\*\*")
PROMPT_MARKERS = (
    "Ask an agent:",
    "Read ./harness-starter-kit",
    "Requirements:",
)


def readme_files() -> list[Path]:
    return sorted(
        REPO_ROOT.glob("README*.md"),
        key=lambda path: (path.name != "README.md", path.name),
    )


def localized_readmes() -> list[Path]:
    return [path for path in readme_files() if path.name != "README.md"]


def agent_prompt_blocks(readme: Path) -> list[str]:
    text = readme.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)\n```", text, flags=re.DOTALL)
    return [
        block
        for block in blocks
        if any(marker in block for marker in PROMPT_MARKERS)
    ]


def site_adoption_prompt() -> str:
    text = SITE_INDEX.read_text(encoding="utf-8")
    match = re.search(
        r'<pre id="prompt-text"><code>(.*?)</code></pre>',
        text,
        flags=re.DOTALL,
    )
    if match is None:
        raise AssertionError("site/index.html prompt-text block not found")
    return html.unescape(match.group(1))


def language_switcher_entries(
    readme: Path,
) -> tuple[str, list[tuple[str, str | None]]]:
    text = readme.read_text(encoding="utf-8")
    for line in text.splitlines():
        entries: list[tuple[str, str | None]] = []
        for part in line.split(" | "):
            linked = SWITCHER_LINK_RE.fullmatch(part)
            if linked:
                entries.append((linked.group("label"), linked.group("target")))
                continue

            current = CURRENT_LANGUAGE_RE.fullmatch(part)
            if current:
                entries.append((current.group("label"), None))
                continue

            entries = []
            break

        current_count = sum(1 for _label, target in entries if target is None)
        if len(entries) > 1 and current_count == 1:
            return line, entries

    raise AssertionError(f"{readme.name} language switcher not found")


class ReadmePromptDriftTests(unittest.TestCase):
    def test_readmes_explain_command_flow_by_user_stage(self) -> None:
        expectations = {
            "README.md": ("## Command Flow", "First time", "Daily work", "Maintenance"),
            "README.ko.md": ("## 명령 흐름", "처음 사용", "일상 작업", "유지보수"),
            "README.ja.md": ("## コマンドフロー", "初回", "日常作業", "メンテナンス"),
            "README.zh-CN.md": ("## 命令流程", "首次使用", "日常工作", "维护"),
            "README.zh-TW.md": ("## 指令流程", "初次使用", "日常工作", "維護"),
        }

        for filename, (heading, first, daily, maintenance) in expectations.items():
            with self.subTest(readme=filename):
                text = (REPO_ROOT / filename).read_text(encoding="utf-8")

                self.assertIn(heading, text)
                self.assertIn(first, text)
                self.assertIn(daily, text)
                self.assertIn(maintenance, text)
                self.assertIn("/harness adopt", text)
                self.assertIn("commands/harness-adopt.md", text)
                self.assertIn("$harness adopt", text)
                self.assertIn("/harness-agent-skills:harness adopt", text)

                self.assertLess(text.index(first), text.index(daily))
                self.assertLess(text.index(daily), text.index(maintenance))

    def test_localized_readmes_are_valid_utf8(self) -> None:
        for path in localized_readmes():
            with self.subTest(readme=path.name):
                try:
                    path.read_bytes().decode("utf-8")
                except UnicodeDecodeError as exc:
                    self.fail(
                        f"{path.name} is not valid UTF-8 at byte {exc.start}: "
                        f"{exc.reason}"
                    )

    def test_language_switcher_highlights_only_current_language(self) -> None:
        readmes = readme_files()
        readme_names = {path.name for path in readmes}
        parsed = {
            path.name: language_switcher_entries(path)
            for path in readmes
        }
        canonical_labels = [label for label, _target in parsed["README.md"][1]]
        label_by_target: dict[str, str] = {}

        for _switcher, entries in parsed.values():
            for label, target in entries:
                if target is None:
                    continue
                self.assertIn(target, readme_names)
                if target in label_by_target:
                    self.assertEqual(label_by_target[target], label)
                else:
                    label_by_target[target] = label

        self.assertEqual(readme_names, set(label_by_target))

        for filename, (switcher, entries) in parsed.items():
            with self.subTest(readme=filename):
                labels = [label for label, _target in entries]
                linked_target_list = [target for _label, target in entries if target]
                current_labels = [label for label, target in entries if target is None]

                self.assertEqual(canonical_labels, labels)
                self.assertEqual(len(readme_names), len(entries))
                self.assertEqual(1, len(current_labels))
                self.assertEqual(len(readme_names) - 1, len(linked_target_list))
                self.assertEqual(readme_names - {filename}, set(linked_target_list))
                self.assertEqual(label_by_target[filename], current_labels[0])
                self.assertEqual(2, switcher.count("**"))

    def test_first_localized_readme_agent_prompt_stays_english(self) -> None:
        expected_blocks = agent_prompt_blocks(REPO_ROOT / "README.md")
        self.assertGreaterEqual(len(expected_blocks), 1)
        expected = expected_blocks[0]
        self.assertIn("/harness review", expected)
        self.assertIn("/harness review sub-agent", expected)
        self.assertIn("commands/harness-review.md", expected)
        self.assertIn("explicit permission", expected)

        for path in localized_readmes():
            with self.subTest(readme=path.name):
                actual = agent_prompt_blocks(path)
                self.assertGreaterEqual(len(actual), 1)
                self.assertEqual(expected, actual[0])

    def test_site_copy_prompt_matches_readme_prompt(self) -> None:
        expected_blocks = agent_prompt_blocks(REPO_ROOT / "README.md")
        self.assertGreaterEqual(len(expected_blocks), 1)
        self.assertEqual(expected_blocks[0], site_adoption_prompt())


if __name__ == "__main__":
    unittest.main()

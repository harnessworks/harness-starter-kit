# 0011. Refresh Benchmark Oracle Line Wrap Drift

## Date Observed

2026-06-11

## Failure Type

Benchmark verification false negative and failed harness check.

## Goal

The `command-workflow-refresh-benchmark-guidance` benchmark should accept
normal Markdown wrapping when the required refresh workflow concepts are
present. The oracle should remain deterministic and still require the benchmark
task path, stale prompt and verification-command checks, expected and forbidden
boundary review, runner-output assumptions, and changes to both expected files.

## What Happened Or Was Tried

A Codex adapter dry run against the starter-kit repository at commit
`497db091d591c710e973f43e148019a4d84e94fe` completed eight benchmark tasks.
Seven succeeded. The failed `command-workflow-refresh-benchmark-guidance` run
changed only `commands/harness-refresh.md` and
`tests/test_repository_hygiene.py`, had no wrong-file edits, had no
forbidden-file edits, and exited successfully. The refresh workflow oracle still
failed because it searched raw Markdown for exact substrings that Codex had
line-wrapped.

## Why It Failed

- Failed check or CI failure: the deterministic benchmark oracle rejected a
  semantically correct refresh workflow update.
- The oracle checked raw Markdown instead of normalized text.
- Required phrases such as stale verification commands and runner-output
  assumptions could be split across line breaks by normal Markdown wrapping.

## Current Replacement

`benchmarks/tasks/command-workflow-refresh-benchmark-guidance.json` now
normalizes whitespace before checking required refresh workflow concepts in
`commands/harness-refresh.md` and `tests/test_repository_hygiene.py`. The
oracle still requires both expected files to appear in `git status`, so a no-op
agent cannot satisfy the task by relying on pre-existing repository content.

## Detection Or Prevention Check

`python3 -m unittest tests.test_benchmark_tasks` includes
`test_command_workflow_oracle_accepts_line_wrapped_concepts` and
`test_command_workflow_oracle_rejects_missing_runner_output_concept`, which run
the refresh workflow oracle in a temporary git repository against wrapped and
missing-concept fixtures. The broader `python3 -m unittest discover -s tests`
gate also runs this coverage.

## Agent Guidance

When maintaining Markdown-oriented benchmark oracles, normalize whitespace
before checking concept phrases unless exact formatting is the behavior being
measured. Keep at least one positive fixture for wrapped Markdown and one
negative fixture for a missing required concept.

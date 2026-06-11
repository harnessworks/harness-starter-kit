# Benchmarks

This directory contains repository-owned benchmark task definitions for
`harness-agent-benchmark-runner`.

Task specs intentionally keep `repo.ref` set to `main` so the benchmark suite
tracks the canonical starter-kit baseline requested by the task definition.
For controlled comparisons, record the runner result's resolved
`repository_ref` or pass `--repo-ref <commit-sha>` when launching the runner.

The task JSON owns the prompt, expected file boundary, forbidden file boundary,
and deterministic project-specific oracle commands. The runner repository
should stay generic and should not need project-specific benchmark logic.

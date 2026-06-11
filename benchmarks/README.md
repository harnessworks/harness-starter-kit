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

## Task Catalog

| Task | Measures |
| --- | --- |
| `small-bugfix-docs-drift-uv-command` | Small bugfix implementation with focused regression coverage and narrow script/test boundaries. |
| `docs-only-evaluation-benchmark-ownership` | Docs-only boundary control and deterministic text verification. |
| `forbidden-file-structure-ignore-runner-output` | Forbidden-file guard behavior around sensitive, generated, metadata, and runner-output paths. |
| `failure-memory-benchmark-noop-oracle-gap` | Failure-memory discipline for benchmark no-op false positives caused by weak oracles. |
| `decision-memory-benchmark-ownership-adr` | Decision-memory discipline for benchmark ownership and runner separation. |
| `profile-boundary-go-race-check` | Stack-profile scope control for a Go-only guidance update. |
| `installer-non-destructive-list-profiles` | Non-destructive installer behavior with focused implementation and tests. |
| `command-workflow-refresh-benchmark-guidance` | Command workflow alignment across refresh guidance and repository-hygiene coverage. |

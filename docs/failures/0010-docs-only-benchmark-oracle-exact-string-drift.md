# 0010. Docs-Only Benchmark Oracle Exact String Drift

## Date Observed

2026-06-11

## Failure Type

Benchmark verification false negative and failed harness check.

## Goal

The docs-only benchmark should verify that an agent documents the required
benchmark ownership concepts without requiring one exact sentence layout. The
oracle should stay deterministic, scoped to `docs/evaluation.md`, and strict
enough to reject generic benchmark prose that omits ownership or boundary
semantics.

## What Happened Or Was Tried

A Codex adapter dry run against the harnessworks starter-kit repository at
commit `fbcb14e1bfc0b2156a3e1e52efa24fc72cccc9b0` changed only
`docs/evaluation.md`, had no wrong-file edits, had no forbidden-file edits, and
exited successfully. The benchmark still failed because the oracle required
exact substrings for the benchmark path, project-specific oracle ownership, and
boundary-versus-verification wording.

## Why It Failed

- Failed check or CI failure: the deterministic benchmark oracle rejected a
  semantically correct docs-only update.
- The oracle treated exact sentence fragments as the contract instead of the
  required concepts.
- The check did not normalize case or whitespace, so harmless Markdown wrapping
  and wording variation could fail the run.

## Current Replacement

`benchmarks/tasks/docs-only-evaluation-benchmark-ownership.json` now extracts
the `## Deterministic Benchmark Tasks` section, normalizes whitespace and case,
and checks concept groups for `benchmarks/tasks/`, project-specific oracle
ownership in this repository instead of the runner repository,
`expected_files`, `forbidden_files`, and the separation between boundary
adherence and verification success.

## Detection Or Prevention Check

`python3 -m unittest tests.test_benchmark_tasks` includes
`test_docs_only_task_oracle_accepts_concept_equivalent_wording` and
`test_docs_only_task_oracle_rejects_runner_owned_oracles`, which execute the
docs-only task oracle in a temporary git repository against positive and
negative documentation fixtures. The broader `python3 -m unittest discover -s
tests` gate also runs this coverage.

## Agent Guidance

When maintaining docs-only benchmark tasks, keep the oracle deterministic and
specific to the requested section, but validate required concepts instead of
one preferred prose style. For documentation tasks, normalize case and
whitespace before checking concept coverage unless exact formatting is the
behavior being measured.

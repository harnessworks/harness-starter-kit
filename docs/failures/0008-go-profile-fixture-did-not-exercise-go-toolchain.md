# 0008. Go Profile Fixture Did Not Exercise The Go Toolchain

## Date Observed

2026-06-08

## Failure Type

Failed check and harness verification gap.

## Goal

The Go profile ships `templates/profiles/go/check_harness.py`, which runs
`go build ./...`, `go vet ./...`, and `go test ./...`. The smoke fixture should
let that check run successfully end to end, so the Go verification path the kit
recommends to target repositories is actually exercised.

## What Happened Or Was Tried

The `go-basic` fixture contained only `go.mod` and `README.md`, with no `.go`
source or test. No test ran the installed Go profile `check_harness.py` against
the fixture; the smoke suite only checked that profile snippets were installed
and that the generic drift scripts ran.

When the Go profile `check_harness.py` was finally run against the source-less
fixture (with `go1.26.4` installed locally), it failed: `go build ./...` passed
vacuously with `matched no packages` (exit 0), but `go vet ./...` exited 1
(`no packages to vet`) and `go test ./...` exited 1 (`no packages to test`).
Because `check_harness.py` runs each step with `check=True`, the Go check path
was broken on the fixture and nobody noticed.

## Why It Failed

- Failed check or CI failure: the Go profile check path failed at `go vet`
  against the only fixture that represented a Go target.
- The fixture was a shape stub without a buildable package, so the Go toolchain
  matched zero packages.
- No smoke or end-to-end test executed the profile's own `check_harness.py`, so
  the broken path stayed invisible behind the snippet-install smoke test.

## Current Replacement

The `go-basic` fixture now ships a real `gobasic` package
(`tests/fixtures/go-basic/calculator.go` and
`tests/fixtures/go-basic/calculator_test.go`) so `go build`, `go vet`, and
`go test` succeed. A new smoke test installs the Go profile and runs the
installed `check_harness.py` against the fixture when `go` is available,
skipping when `go` is absent. The same pattern already guards the Rust profile.

## Detection Or Prevention Check

`tests/test_smoke_fixtures.py` adds
`test_go_profile_check_harness_runs_go_path`, which installs the Go profile and
runs the installed Go profile `check_harness.py` against the buildable fixture,
asserting a zero exit code. It is guarded with
`@unittest.skipUnless(shutil.which("go"), ...)` so the real Go toolchain steps
run wherever the toolchain is installed and skip safely on the Python-only CI.
The supporting fixture sources are `tests/fixtures/go-basic/calculator.go` and
`tests/fixtures/go-basic/calculator_test.go`.

## Agent Guidance

When a profile's `check_harness.py` runs a compiler or test command, give its
fixture a minimal buildable target and add a skip-safe smoke test that runs the
installed `check_harness.py` against that fixture. Do not rely on snippet-install
smoke tests alone: a `./...`-style command can pass vacuously on `build` while
failing on `vet`/`test`, so confirm the whole toolchain path with a real
package before finishing similar profile work.

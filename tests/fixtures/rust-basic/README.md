# Rust Basic Fixture

A minimal Rust crate used to smoke-test harness adoption. It ships a `src/lib.rs`
library target so `cargo build` and `cargo test` succeed, letting the Rust
profile's `check_harness.py` exercise the real Cargo path.

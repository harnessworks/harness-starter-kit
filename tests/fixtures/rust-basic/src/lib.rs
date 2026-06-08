//! Minimal library target so `cargo build`/`cargo test` have something to compile.

/// Adds two integers.
///
/// Present so the fixture is a real Cargo target that the Rust profile's
/// `check_harness.py` can build and test during smoke checks.
pub fn add(left: i64, right: i64) -> i64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds_two_numbers() {
        assert_eq!(add(2, 2), 4);
    }
}

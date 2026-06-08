// Package gobasic provides a tiny buildable target so the Go profile's
// check_harness.py can run go build, go vet, and go test against a real
// package during smoke checks.
package gobasic

// Add returns the sum of two integers.
func Add(a, b int) int {
	return a + b
}

# Go Basic Fixture

A minimal Go module used to smoke-test harness adoption. It ships a real
`gobasic` package (`calculator.go` + `calculator_test.go`) so `go build`,
`go vet`, and `go test` succeed, letting the Go profile's `check_harness.py`
exercise the real Go toolchain path.

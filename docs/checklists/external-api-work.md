# External API Work Checklist

Use this checklist when agent work touches a live external API, public-data API,
auth provider, webhook, payment provider, map service, or backend fixture that
can return provider-specific errors.

The goal is to make API work repeatable. A harness should not solve the domain
problem for the agent, but it should make the failure modes explicit and
verifiable.

## Boundary First

- Identify the server-only boundary that calls the external API.
- Identify the config source for base URL, API key, service key, timeout, and
  live/mock mode.
- Keep secrets out of client components, logs, screenshots, reports, and failure
  records.
- Redact query parameters and headers before printing request URLs or debug
  payloads.
- Document whether live calls are required for local verification or whether a
  fixture/mock is the normal path.

## Response Model

Handle these cases as separate states instead of collapsing them into a single
error:

| Case | Expected handling |
| --- | --- |
| Transport failure | Preserve a sanitized reason and fail health/smoke checks clearly. |
| TLS or certificate failure | Record the runtime and endpoint involved; add failure memory if it should not recur. |
| Provider error envelope | Parse provider error codes even when the HTTP status is 200. |
| Provider text error | Treat responses such as `401 text/plain Unauthorized` as provider or transport errors, not as unsupported parser formats. |
| Empty or zero-result response | Return a deliberate empty state, not a crash or fake success. |
| Malformed JSON or XML | Report parser context without logging secrets or full personal data payloads. |
| Schema drift | Keep a focused fixture or smoke check for the changed fields. |

For public-data APIs, check whether the provider returns XML, JSON, text error
messages, or mixed envelopes under the same endpoint. Do not assume content type
alone tells the full story.

## Live And Mock Fallbacks

- Make live/mock selection explicit through the target repository's existing
  config pattern.
- Do not silently fall back from live data to mock data in production paths.
- If fallback is intentional, expose the fallback reason in a server-only log,
  health response, or diagnostic endpoint without leaking secrets.
- Keep fixtures small and representative: success, zero-result, provider error,
  and malformed response are usually more useful than a large golden payload.

## Health And Smoke Checks

Add a target-specific verification script when repeated API work depends on
runtime behavior that lint, typecheck, and build cannot prove. A useful script
can live under a target path such as `scripts/check_<provider>.mjs` or
`scripts/check_<provider>.py`.

Prefer checks that:

- verify required environment variables are present without printing values
- call a safe endpoint or fixture
- assert success, zero-result, provider-error envelope, and provider text-error
  handling where practical
- print a short summary of the axis checked, such as env, transport, parser,
  empty-state, and redaction
- exit nonzero on real failures
- can be run independently from the full `check:harness` gate

## Durable Memory

Use `docs/checklists/decision-failure-memory.md` to decide where the API work
belongs:

- Use a decision record when the work chooses an API boundary, live/mock policy,
  runtime strategy, data model, or fallback policy.
- Use a failure record when a provider behavior, TLS issue, 5xx path, secret
  leak risk, schema mismatch, or repeated integration mistake should not recur.
- Use domain docs when the work defines provider terms, response states, or
  business meanings that future agents need.
- Use a final report or check note for a narrow implementation fix covered by
  existing docs and tests.

## Completion Check

Before reporting completion for external API work, name:

- the endpoint or fixture path verified
- the live/mock mode used
- the redaction behavior checked
- the empty-result behavior checked or why it was not applicable
- the provider error envelope or provider text-error behavior checked
- the command run for API smoke verification, if any
- whether decision memory or failure memory was recorded or intentionally
  skipped

# Harness Review Workflow

Use this diagnostic review to challenge the current change set from an opposing
harness-engineering perspective. Do not modify files unless the user explicitly
asks to apply fixes after seeing the review.

## Procedure

1. Inspect the current diff and relevant repository guidance.
2. Review whether the change preserves the target repository as source of
   truth.
3. Check for:
   - blind template copying
   - unnecessary automation
   - missing enforceable checks
   - missing decision or failure memory
   - stale docs, examples, component maps, prompts, or validation docs
   - changed command workflows without matching tests or docs
   - missing validation evidence
4. For `/harness review sub-agent`, use a read-only reviewer subagent only when
   the active runtime permits it. If unavailable, blocked, or failed, fall back
   to single-agent review and report the reason.
5. The parent agent owns reviewer mode and fallback reason. Do not ask the
   subagent to assess reviewer mode, fallback reason, or subagent availability.
   Do not copy those fields from subagent output.
6. Check gate placement: deterministic, local, non-network, reasonably fast
   checks that agents should repeat belong in the documented normal completion
   gate. Record the normal completion gate unless there is a focused or manual
   placement reason.
7. Lead with findings ordered by severity. If there are no actionable findings,
   say that clearly and name any residual test gaps.

## Report Format

```text
Harness Review Report

Invocation: </harness review or /harness review sub-agent>
Reviewer mode: <single-agent, sub-agent, or fallback with reason>

Findings:
- <severity> <file:line or artifact>: <issue, risk, and recommendation>

Open Questions:
- <question or none>

Missing Checks Or Evidence:
- <gap or none>

Overreach / Source-of-Truth Risks:
- <risk or none>

Summary:
- <short summary>

Recommended Next Actions:
1. <action>
2. <action>
3. <action>
```

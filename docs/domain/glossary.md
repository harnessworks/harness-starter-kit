# Domain Glossary

This project does not have business-domain terms. It does have product language
that agents should use consistently when changing docs, templates, or scripts.

| Term | Meaning | Notes |
| --- | --- | --- |
| Harness | Repository-level instructions, constraints, feedback loops, and memory for coding agents. | A harness is project-scoped, not chat-scoped. |
| Target repository | The repository receiving harness files from this starter kit. | The target repository remains the source of truth. |
| Template | A generic file copied into a target repository. | Templates should be conservative and safe by default. |
| Profile | Optional stack-specific guidance for Python, TypeScript, or another ecosystem. | Profiles provide snippets, not full build-system rewrites. |
| Drift check | A script that detects stale docs, temporary files, or structure that no longer matches project rules. | Drift checks should be lightweight enough to run locally. |
| Knowledge store | Durable context under `docs/decisions`, `docs/failures`, `docs/conventions`, and `docs/domain`. | Empty folders are less useful than one real record. |
| Adoption report | The final summary after applying the kit to a target repository. | It should list changed files, checks, assumptions, and manual steps. |
| Effectiveness measurement plan | The adoption-time plan for measuring whether harness rules reduce repeated agent mistakes. | If no baseline exists, record the next comparable tasks and review window. |
| Optional CI | The GitHub Actions harness workflow shipped with the generic templates. | Install it only with `--with-ci` after confirming GitHub Actions fits the target repository. |

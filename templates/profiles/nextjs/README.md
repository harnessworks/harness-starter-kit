# Next.js Harness Profile

Use these snippets when the target project is a Next.js app, especially an App
Router project.

These files are agent reference material, not automatic transformations. Merge
only the pieces that fit the target project's existing tools.

Apply this profile by priority: always preserve the target package manager,
generated-file rules, and exact local checks; document external API/auth setup
when present; consider decision records only when changing router, runtime,
state, or integration policy; use a short report/check note for narrow fixes.

## Recommended Checks

- `next build` for production build validation.
- `tsc --noEmit --incremental false` for a non-emitting TypeScript check.
- `scripts/check_docs_drift.py` for stale documentation references.
- `scripts/check_structure.py` for temporary or drift-prone files.

Expose a single local verification command in `package.json`:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit --incremental false",
    "check:docs": "python scripts/check_docs_drift.py",
    "check:structure": "python scripts/check_structure.py",
    "check:harness": "npm run typecheck && npm run build && npm run check:docs && npm run check:structure"
  }
}
```

Use `npm.cmd` instead of `npm` when running commands from Windows PowerShell if
script execution policy blocks `npm.ps1`.

Keep live API smoke checks as separate scripts unless they are stable and safe
in the target repository's normal environment. If a project adds a focused
script such as `scripts/check_<api>.mjs`, document what it verifies and whether
it belongs in `check:harness`.

## Profile Absorption Notes

When Next.js is introduced after generic adoption:

- Merge useful scripts from `package-scripts.harness.json` into `package.json`
  instead of replacing the target's scripts.
- Merge relevant ignores from `gitignore.harness.txt`, especially `.next/`,
  `node_modules/`, `tsconfig.tsbuildinfo`, generated output, and the local
  `harness-starter-kit/` clone.
- Keep the target package manager as source of truth; do not add npm, pnpm, or
  yarn only because this profile mentions them.
- Review any `tsconfig.json` or `next-env.d.ts` changes made by Next.js during
  setup, then keep intentional changes instead of reverting them blindly.
- Update `AGENTS.md` with Next.js commands, source directories, generated
  paths, route conventions, and completion checks.
- Update `docs/conventions/coding.md` with App Router, data fetching, component
  boundary, styling, and testing conventions.
- Consider a decision record when changing or selecting Next.js, an app/router
  structure, runtime strategy, or state management approach. When the task only
  follows the existing architecture or makes a narrow fix, a final report or
  check note is enough.
- In the final report, list which snippets were adopted, adapted, skipped, or
  deferred.

## App Router Checklist

- Keep secrets and provider credentials in server-only code. Do not expose them
  through client components, serialized props, screenshots, or logs.
- Use `NEXT_PUBLIC_` variables only for values intentionally safe for the
  browser. Server-only route handlers and server components should read private
  env vars directly through the target's existing config pattern.
- For `app/api/<route>/route.ts`, decide whether the route is a thin proxy, a
  validation boundary, or a product endpoint. Record a decision only when that
  boundary is new or changes integration policy.
- Choose the runtime deliberately for route handlers that depend on Node APIs,
  TLS behavior, certificates, streaming, or provider SDKs. Do not assume Edge
  and Node runtimes handle external calls the same way.
- In server components, keep data fetching close to the existing route,
  service, or cache pattern. Avoid moving external API calls into client
  components to work around env handling.
- Model empty API results, provider errors, and malformed payloads as explicit
  states. A zero-result response should not be treated as a parser failure.
- For live/mock fallback, make the mode explicit and avoid silent production
  fallback unless the target has already chosen that policy.
- Add or adapt a focused smoke script when a route handler's external API,
  redaction, empty-result, or provider-error behavior cannot be proven by
  typecheck and build.

## Next.js Notes

- Do not rely on `next lint` for current Next.js projects unless the target
  project already has a working lint command. Newer Next versions may not expose
  `next lint` as a valid command.
- `next build` may update `tsconfig.json` and `next-env.d.ts` during initial
  project setup. Review those changes instead of reverting them blindly.
- Ignore generated files and local reference clones: `.next/`, `node_modules/`,
  `tsconfig.tsbuildinfo`, and `harness-starter-kit/`.
- Do not commit the local `harness-starter-kit/` clone unless the target
  intentionally keeps it as a submodule or reference.
- Add a dedicated test runner only when build and typecheck no longer cover the
  user-facing behavior being changed.

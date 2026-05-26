# Adoption Workflow

Use this workflow when `harness-starter-kit` has been cloned or downloaded
inside another repository and an agent is applying it from the target root.

The target repository is the current working directory. The
`./harness-starter-kit` directory is reference material during adoption; do not
edit it unless the user asks to change the kit itself.

## 1. Read The Target Repository

Collect the current shape before changing anything:

- language and framework
- package manager
- test commands
- lint and format commands
- CI provider
- directory layout
- existing docs and agent instruction files

## 2. Identify Existing Harness Pieces

Many projects already have part of a harness:

- `README.md` or contribution docs
- tests
- CI
- lint configuration
- architecture docs
- decision records

Reuse these instead of duplicating them.

## 3. Add Or Update `AGENTS.md`

The first useful harness artifact is usually a short `AGENTS.md`.

It should answer:

- What is this project?
- Which commands should agents run?
- Which directories have special rules?
- What should agents avoid?
- What must be true before a change is complete?

## 4. Add A Knowledge Store

Create these directories if the target has no equivalent:

```text
docs/
|-- decisions/
|-- failures/
|-- conventions/
`-- domain/
```

Start small. Empty directories are less useful than one real decision or failure
record.

## 5. Add Constraints

Match constraints to the stack:

- Python: Ruff, mypy, import-linter, vulture, pre-commit
- Django: `manage.py check`, `manage.py test`, virtual environment and
  development database ignores, and migration review rules
- Flask: app factory checks, `python -m unittest discover -s tests`, Flask
  route table checks, and instance-data ignores
- TypeScript: ESLint, TypeScript strictness, dependency boundary rules,
  unused-export checks
- Next.js: `next build`, `tsc --noEmit --incremental false`, generated-file
  ignores, and a review of any `tsconfig.json` or `next-env.d.ts` changes made
  by Next itself
- Any stack: CI checks, formatting checks, forbidden-file scans

Prefer existing tools when possible.

## 6. Add Feedback Loops

Make the common path fast:

- local check command
- pre-commit checks when the project already uses them
- CI workflow only when it matches the target repository's CI provider
- clear test names and error messages

Agents improve fastest when feedback is quick and concrete.

## 7. Add Garbage Collection

Install lightweight drift checks:

- missing files referenced by docs
- forbidden temporary filenames
- stale commands in `AGENTS.md`
- unused code checks for the chosen stack

Run them manually at first, then wire them into CI once they are stable. The
installer only adds the GitHub Actions workflow when `--with-ci` is provided.

## 8. Report Adoption

Finish with a short adoption report. Use
`docs/templates/adoption-report.md` as a shape and compare against
`examples/node-adoption-report.md`, `examples/nextjs-adoption-report.md`,
`examples/django-adoption-report.md`, or `examples/flask-adoption-report.md`
when the target stack is similar.

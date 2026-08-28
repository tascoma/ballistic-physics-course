---
description: Build one course module from its CURRICULUM.md specification
argument-hint: <module number, e.g. 07>
---

Build course module **$1**.

Follow the authoring contract in `CLAUDE.md` exactly. The short version, in
order — do not skip steps and do not reorder them:

## 1. Read before writing

- The spec for module $1 in `CURRICULUM.md`. It is the contract: objectives,
  mathematics, what to build, which figures, what to test, and **author
  pitfalls specific to this module**. Read the pitfalls carefully; they exist
  because this module has a known way to go wrong.
- `docs/notation.md` — use its symbols, do not invent competing ones.
- `docs/units-and-conventions.md`.
- `docs/style-guide.md` if you have not written a module this session.

If the spec is wrong or incomplete, **fix `CURRICULUM.md` first**, then build.
Do not improvise around a bad spec.

## 2. Check prerequisites

```bash
uv run pytest
uv run python tools/check_curriculum.py
```

Both must be green. Confirm every file this module's prerequisites were
supposed to build actually exists — see the library build map in
`CURRICULUM.md`. If a prerequisite is missing, **stop and report it**; do not
stub it.

## 3. Scaffold

```bash
uv run python tools/new_module.py $1
```

This creates the directory, the lesson skeleton with correct front matter, and
a stub script for each figure the spec requires.

## 4. Library code first, with tests

Write the code in `src/ballistics/` before the lesson. Get
`uv run pytest` green. Writing prose about an API that does not exist yet
produces lessons that describe code you then have to bend to match.

Include the limiting-case test the spec names (drag → 0 gives the vacuum
solution, and so on). From M17 onward, add a golden-file regression case.

## 5. The lesson

`modules/NN-slug/README.md`, in the fixed twelve-section order from `CLAUDE.md`.
Derive everything. Carry one worked numeric example in shooting units all the
way through.

## 6. Figures

Read the `dataviz` skill first. Then, for each figure the spec lists: write the
script, run it, **look at the PNG**, and only then write its caption and its
"what to notice" note in the lesson.

## 7. Exercises

5–8 in `exercises/exercises.md`, mixing hand calculation, derivation, code,
interpretation, and judgement. Complete worked solutions in `solutions.md`.

## 8. Verify

```bash
uv run pytest
uv run python tools/build_figures.py $1
uv run python tools/build_figures.py $1 --check   # must be byte-identical
uv run python tools/check_curriculum.py
uv run ruff check .
```

## 9. Bookkeeping

- Flip module $1 to `[x]` in the `CURRICULUM.md` progress table.
- Set `status: complete` in the lesson's front matter.
- Add new terms to `docs/glossary.md` with the module number.
- Add any new sources to `docs/references.md`.
- Record any new dataset in `data/README.md`, including whether it is synthetic.

## Reminders that matter for this repository

- **Build only module $1.** Not the next one, not a preview of it.
- **The honesty rule.** If this module imports an empirical model rather than
  deriving it — spin drift, aerodynamic jump, Miller's rule, banded BCs — say so
  in the lesson body, name the source, and state the validity range.
- **Seed all randomness.** Figures must regenerate byte-identically.
- **Unit suffixes on every variable.** A bare `velocity` is a bug.
- **Sign conventions** for wind, twist hand, and hemisphere are where errors
  hide. Write the test first and state the expected result in plain English.

Report at the end: what was built, test results, figures generated, and anything
in the spec you had to change and why.

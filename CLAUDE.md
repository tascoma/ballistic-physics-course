# Authoring contract

Rules for building course modules in this repository.

**Read [`CURRICULUM.md`](CURRICULUM.md) for what to build. This file is how to
build it.**

---

## The one rule that matters most

**Build one module per session, and only the module asked for.**

The curriculum is 30 modules deep. Building ahead burns context, produces
material that later modules will contradict, and defeats the point of the
sequencing. If a module feels thin, that is usually because a later module owns
the rest of the topic -- check the spec before expanding.

---

## Before writing anything

1. **Read the module's spec** in `CURRICULUM.md`. It is the contract: objectives,
   mathematics, what to build, which figures, what to test, and the author
   pitfalls specific to that module. The pitfalls exist because that module has
   a known way to go wrong.
2. **Read [`docs/notation.md`](docs/notation.md)** and use its symbols. Do not
   invent a competing symbol for a quantity that already has one.
3. **Read [`docs/units-and-conventions.md`](docs/units-and-conventions.md)**.
4. **Verify the prerequisites exist and pass**: `uv run pytest`. If a
   prerequisite module's code is missing, stop and report it -- do not stub it.
5. **Check the library build map** in `CURRICULUM.md` to see what already exists
   and what this module owns.

If the spec turns out to be wrong or incomplete, **fix the spec in
`CURRICULUM.md` first**, then build. Do not improvise around a bad spec and
leave the file lying.

---

## Build procedure

```bash
uv run python tools/new_module.py NN        # scaffolds modules/NN-slug/ from templates/
```

Then, in this order:

1. **Library code first**, in `src/ballistics/`, with tests, until
   `uv run pytest` is green. Writing the lesson before the code produces prose
   describing an API that does not exist.
2. **The lesson**, `modules/NN-slug/README.md`, in the fixed section order below.
3. **Figure scripts**, in `modules/NN-slug/code/`. Run them. **Look at every
   PNG.** Then write its caption and its "what to notice" note.
4. **Exercises and solutions**, in `modules/NN-slug/exercises/`.
5. **Verify**:
   ```bash
   uv run pytest
   uv run python tools/build_figures.py NN
   uv run python tools/check_curriculum.py
   uv run ruff check .
   ```
6. **Update the bookkeeping**: flip the module to `[x]` in `CURRICULUM.md`'s
   progress table, add new terms to `docs/glossary.md`, add any new sources to
   `docs/references.md`, and record any new dataset in `data/README.md`.

---

## Lesson structure

Every `modules/NN-slug/README.md` uses this structure. `templates/module/README.md`
ships it as a skeleton. Section order is fixed; a section with nothing to say may
be dropped, but the order of what remains does not change.

```
---
id: 07
title: Trajectory in a Vacuum
slug: vacuum-trajectory
part: "II — Classical Mechanics of Projectiles"
prereqs: [6]
builds: ["ballistics/vacuum.py"]
figures: ["m07-fig01-angle-family", "m07-fig02-analytic-vs-rk4"]
status: complete
---
```

| § | Section | Contents |
|---|---|---|
| — | Title + promise | One sentence: what the reader will be able to do |
| — | Header block | Prerequisites · What you will build · Estimated time |
| 1 | Why this matters | A concrete range scenario this module answers |
| 2 | Learning objectives | 3-6 checkboxes, each measurable |
| 3 | Concepts | Prose and derivations. Every algebraic step shown |
| 4 | The mathematics | Formal statements, boxed key results, one worked numeric example in real shooting units |
| 5 | Building the code | What is added to `ballistics/`, and *why it is designed that way* |
| 6 | Visualising it | Figures, each with a caption and a "what to notice" |
| 7 | Limits and sanity checks | Degenerate cases, what this model cannot do, what breaks it |
| 8 | Field takeaways | 3-5 bullets a shooter can act on at the range |
| 9 | Exercises | Link to `exercises/` |
| 10 | Key equations | The summary card a reader would screenshot |
| 11 | References | Pointers into `docs/references.md` |
| 12 | What's next | The specific gap the next module fills |

The front matter is parsed by `tools/check_curriculum.py`. Keep it valid YAML.

---

## Invariants

These hold in every module. They are not style preferences.

**SI inside, imperial at the edges.** Library internals are metres, kilograms,
seconds, kelvin, pascals, radians. Two documented exceptions: ballistic
coefficient and sectional density stay in lb/in², and Miller's stability rule is
natively imperial. Both are labelled at every call site.

**Every variable name carries its unit.** `range_m`, `velocity_mps`, `twist_in`,
`drop_moa`. A bare `velocity` is a bug.

**No new dependencies without asking.** numpy, scipy, matplotlib, pandas,
pytest, ruff. That is the whole list. In particular: no units library (M01
teaches dimensional analysis by hand) and no third-party ballistics library
(the reader is building one).

**Every public function documents its units** in the docstring, for arguments
and for the return value.

**Every module adds tests.** Known values, limiting cases, and from M17 onward a
golden-file regression case.

**All randomness is seeded.** `np.random.default_rng(SEED)` with `SEED` a
module-level constant, stated in the figure caption. Figures must regenerate
byte-identically or `tools/build_figures.py` becomes diff noise.

**Prose and figures use imperial; code uses SI.** The audience is shooters. The
worked example in each module carries one realistic load all the way through so
every intermediate value is checkable.

---

## The honesty rule

Some effects in this course cannot be derived from a point-mass model. Spin
drift, aerodynamic jump, banded ballistic coefficients, Miller's stability rule,
and the free-recoil gas factor are empirical fits or imports from
higher-fidelity work.

Where that is the case, the lesson **must**:

- say so plainly, in the body, not in a footnote
- name the source
- state the range of validity
- where models disagree, show the disagreement rather than silently picking one

A reader must always be able to tell which of their numbers are physics and
which are curve fits. This is the difference between this course and a manual.

The same applies to data. Synthetic datasets are labelled synthetic in the file
header, in the lesson, and in `data/README.md`, and their generator script is
committed. Never present generated data as measured.

---

## Mathematics

- LaTeX in `$...$` and `$$...$$`. GitHub renders both.
- **Derive things.** "It can be shown that" is not acceptable in a course whose
  entire premise is that the reader should understand their solver.
- Use `docs/notation.md` symbols.
- Every module has **one worked numeric example** in real shooting units,
  carried through completely, so a reader can check their arithmetic against it.
- State assumptions when they are made, not in a closing caveat.

---

## Figures

Read the `dataviz` skill before writing figure code.

- `from ballistics.viz import apply_style, save_figure`; call `apply_style()`
  before creating any figure.
- Save with `save_figure(fig, NN, "figKK-slug")`. Naming is enforced.
- One script per figure: `code/figKK_slug.py`, with a `main()`.
- **Colour follows the entity, not the plot order.** Physical effects use
  `ballistics.viz.style.EFFECT_COLORS` so that "orange is wind" holds across the
  whole course.
- Two or more series always get a legend; four or fewer should also be direct-
  labelled. Colour must never be the only channel carrying identity.
- Scatter-like forms (any series can neighbour any other) are capped at 3 series
  by `cycle_colors(n, scatter=True)`. Facet instead of adding a hue.
- Never a dual y-axis. Two measures of different scale means two panels.
- Exaggerated vertical scales on trajectory plots **must** say so in the caption.
- Every figure gets a caption *and* a "what to notice". A figure that teaches
  nothing the prose cannot gets cut.

---

## Exercises

5-8 per module, in `exercises/exercises.md`, with complete worked answers in
`exercises/solutions.md`. Mix the types:

- **Hand calculation** — arithmetic with a stated tolerance
- **Derivation** — reproduce or extend a result from the lesson
- **Code** — extend the library, with an expected output to check against
- **Interpretation** — read a figure, or diagnose a described situation
- **Judgement** — a decision with a defensible answer and stated tradeoffs

Solutions show the work, not just the number.

---

## Anti-patterns

Things that have a specific way of going wrong here.

**Running ahead.** Teaching drag properly in the orientation module, or
introducing 6DOF concepts in the spin-drift module. Check the spec's scope.

**Wrapping instead of building.** `scipy.integrate.solve_ivp` exists, and M05
must not simply call it. Write the integrator, then show scipy agrees, then say
when to use which.

**Silent API changes.** Extending an earlier file is fine. Changing an earlier
public signature requires updating every call site, that module's tests, and its
figures, in the same session, with the change documented in the lesson. Three
such changes are anticipated and listed in `CURRICULUM.md`; a fourth means
something was designed wrong earlier and should be fixed there.

**Unsourced numbers.** Especially in `INSTRUMENT_UNCERTAINTY` (M24), which feeds
the uncertainty budget in M26 and the hit-probability model in M27. An
unsourced value there quietly corrupts three modules.

**Uninterpreted figures.** A plot with no "what to notice" is decoration.

**Sign-convention drift.** Wind direction (M03/M18), twist hand (M21/M22), and
hemisphere (M23) are the three places sign errors hide. Write the test first and
state the expected result in plain English as a cross-check.

**Fixing a spec by ignoring it.** If `CURRICULUM.md` is wrong, change
`CURRICULUM.md`.

---

## Commands

| Command | Does |
|---|---|
| `uv sync` | install |
| `uv run pytest` | the whole suite |
| `uv run pytest tests/test_m07_vacuum.py -v` | one module's tests |
| `uv run python tools/new_module.py NN` | scaffold a module directory |
| `uv run python tools/build_figures.py` | regenerate every figure |
| `uv run python tools/build_figures.py NN` | regenerate one module's figures |
| `uv run python tools/check_curriculum.py` | verify modules match their specs |
| `uv run ruff check . --fix` | lint |

`/build-module NN` runs this procedure. `/review-module NN` checks a finished
module against the contract.

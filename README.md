# Ballistic Physics

A course in the physics and mathematics of exterior ballistics, built for people
who want to understand what their ballistic solver is doing rather than trust it.

It starts at algebra and trigonometry and ends with a validated, field-grade
3DOF solver that you wrote yourself: drag models, real atmosphere, wind, spin
drift, aerodynamic jump, Coriolis, an uncertainty budget, and a truing workflow
that calibrates the whole thing against your own range data.

Nothing is imported that the course should teach. Every equation is derived,
every model that is an empirical fit says so, and every number in every figure
is reproducible by running one script.

## What you need coming in

High-school algebra and trigonometry. That is all. Vectors, derivatives,
integrals, differential equations, and numerical integration are taught inside
the course, in that order, before any of them is needed.

You do not need prior physics, and you do not need to be a programmer -- but you
should be willing to read and run Python.

## What you get coming out

By the capstone you will be able to:

- Derive the equations of motion for a projectile and integrate them numerically.
- Explain what a ballistic coefficient actually is, and why the number on the box
  is not the number your bullet has.
- Compute air density from a weather meter and say how much a wrong pressure
  reading costs you at 1000 yards.
- Predict crosswind deflection from first principles, and explain why it is not
  simply wind speed times time of flight.
- Say how much of your miss was wind call, muzzle velocity spread, rangefinder
  error, or your rifle -- with numbers.
- True a solver against DOPE without fooling yourself.
- State what your model cannot do, and what a 6DOF model would add.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone <this repo>
cd ballistic-physics-course
uv sync
uv run pytest          # everything built so far should be green
```

That is the whole install. `uv` handles the Python version and the scientific
stack from `pyproject.toml`.

## How to take the course

Work through `modules/` in order. Each module is a directory:

```
modules/07-vacuum-trajectory/
├── README.md          the lesson -- read this
├── code/              scripts that generate every figure in the lesson
├── assets/            the generated figures (committed, so the lesson reads standalone)
├── exercises/         problems, and full worked solutions
└── data/              any data the module needs
```

Read the lesson. Run the figure scripts and change the numbers -- that is where
the intuition comes from. Do the exercises before reading the solutions.

Each module adds real code to `src/ballistics/`. By the end, that package is a
working ballistic solver, and you wrote all of it.

```bash
uv run python modules/07-vacuum-trajectory/code/fig01_trajectory_family.py
```

**Start here:** [`CURRICULUM.md`](CURRICULUM.md) is the full map -- all 30
modules, what each one teaches, and what it builds.

## Conventions worth knowing before you read any code

- **Everything inside the library is SI.** Metres, kilograms, seconds, kelvin,
  pascals, radians. Imperial units live only at the edges.
- **Every variable name carries its unit**: `range_m`, `velocity_mps`,
  `twist_in`, `drop_moa`. If you see a bare `velocity`, it is a bug.
- **One exception:** ballistic coefficient stays in lb/in², because that is its
  definition. It is named `bc_lbin2` so you cannot forget.
- **Coordinates:** origin at the muzzle, +x downrange, +y up, +z to the
  shooter's right.

Full detail in [`docs/units-and-conventions.md`](docs/units-and-conventions.md)
and [`docs/notation.md`](docs/notation.md).

## Repository layout

| Path | What it is |
|---|---|
| [`CURRICULUM.md`](CURRICULUM.md) | The full course specification -- all 30 module specs, and the library build map |
| [`CLAUDE.md`](CLAUDE.md) | The authoring contract: rules for writing a module |
| [`modules/`](modules/) | The lessons, one directory per module |
| [`src/ballistics/`](src/ballistics/) | The library the course builds, module by module |
| [`docs/`](docs/) | Notation, units, glossary, references, style guide |
| [`data/`](data/) | Shared datasets -- drag tables, sample DOPE -- each with stated provenance |
| [`tests/`](tests/) | The test suite; every module adds to it |
| [`tools/`](tools/) | Scaffolding, figure regeneration, curriculum consistency checks |

## Scope

This course covers **exterior ballistics** -- the bullet's flight from muzzle to
target -- using a **3DOF point-mass model** with modelled corrections for the
rotational effects. That is the same class of model behind every commercial
ballistic solver, and it is accurate enough to make first-round hits.

Deliberately out of scope: 4DOF/6DOF rigid-body aeroballistics, interior
ballistics, terminal ballistics, CFD, and reloading. Each gets an honest
"here's what it is and where to read about it" entry in
[`docs/appendix-further-study.md`](docs/appendix-further-study.md).

## A note on the models

Some effects in this course -- spin drift, aerodynamic jump, banded ballistic
coefficients -- cannot be derived from a point-mass model. They are empirical
fits or approximations borrowed from higher-fidelity work. Where that is the
case, the lesson says so plainly, names the source, and states the range over
which the model is valid. You should know which of your numbers are physics and
which are curve fits.

## Safety

This is a physics course about projectile motion. It teaches prediction, not
marksmanship, and it is no substitute for firearms safety training. Follow the
four rules, know your target and what is beyond it, and understand that a
solver's confidence interval is not a safety margin.

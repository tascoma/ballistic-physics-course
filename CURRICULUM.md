# Curriculum

The complete specification of the course: thirty modules, what each teaches,
what it builds, and how it is verified.

**This file is the contract.** A module is built by reading its spec below and
following the procedure in [`CLAUDE.md`](CLAUDE.md). A spec that is not
self-sufficient is a bug in this file -- fix it here rather than improvising in
the module.

---

## Progress

Legend: `[ ]` not started · `[~]` in progress · `[x]` complete

| | Module | | | Module |
|---|---|---|---|---|
| `[x]` | **00** What a Ballistic Solution Is | | `[ ]` | **15** Equations of Motion with Drag |
| `[x]` | **01** Units and Dimensional Analysis | | `[ ]` | **16** Solver Engineering |
| `[ ]` | **02** Angles and Angular Measure | | `[ ]` | **17** Validation and Verification |
| `[ ]` | **03** Vectors and Coordinate Systems | | `[ ]` | **18** Crosswind Deflection and Lag Time |
| `[ ]` | **04** Derivatives and Integrals | | `[ ]` | **19** Real Wind Fields |
| `[ ]` | **05** ODEs and Numerical Integration | | `[ ]` | **20** Spin and Gyroscopic Stability |
| `[ ]` | **06** Newton, Momentum, Energy | | `[ ]` | **21** Spin Drift and Yaw of Repose |
| `[ ]` | **07** Trajectory in a Vacuum | | `[ ]` | **22** Aerodynamic Jump |
| `[ ]` | **08** Sight Geometry and Zeroing | | `[ ]` | **23** Coriolis and Eötvös |
| `[ ]` | **09** Air Density and the Atmosphere | | `[ ]` | **24** Instrumentation and Measurement Error |
| `[ ]` | **10** Speed of Sound and Mach | | `[ ]` | **25** The Statistics of Precision |
| `[ ]` | **11** Where Drag Comes From | | `[ ]` | **26** Error Propagation and Uncertainty |
| `[ ]` | **12** The Drag Coefficient Curve | | `[ ]` | **27** Hit Probability |
| `[ ]` | **13** Ballistic Coefficient and Drag Models | | `[ ]` | **28** DOPE, Truing, and Calibration |
| `[ ]` | **14** Custom and Doppler Drag Curves | | `[ ]` | **29** Capstone |

---

## How the course is designed

Five decisions shape everything below.

**1. Nothing is used before it is derived.** Vectors precede wind. Calculus
precedes trajectories. Numerical integration precedes drag. If a module needs a
tool, an earlier module built it. The prerequisite chain in each spec is real,
not decorative.

**2. Every model gets a validation baseline.** The vacuum trajectory (M07) has a
closed-form solution, so it becomes the test that the numerical solver is
correct. Then the numerical solver becomes the baseline for the drag model, and
so on up. By M17 there is a regression suite; by M29 the whole thing is checked
end to end.

**3. Approximations are labelled.** Spin drift, aerodynamic jump, and banded
ballistic coefficients cannot be derived from a point-mass model. They are
empirical fits imported from higher-fidelity work. Those modules say so, name
the source, and state the validity range. A reader must always know which of
their numbers are physics and which are curve fits.

**4. One load runs through the whole course.** See below. Every module's worked
example uses it, so the reader watches the same trajectory get progressively
more accurate as effects are added, and can compare any module's numbers to any
other's.

**5. The field content is not an afterthought.** Instrumentation, dispersion
statistics, uncertainty budgets, and truing are Part IX and X because they are
where the physics meets a rifle. A solver you cannot calibrate or whose error
you cannot bound is a toy.

### The running example

Every module's worked example uses this load unless it has a specific reason not
to. Values are nominal published figures; Module 13 examines how much to trust
the BC.

| | Primary load | Contrast load |
|---|---|---|
| Cartridge | 6.5 Creedmoor | .308 Winchester |
| Bullet | 140 gr Berger Hybrid Target | 175 gr Sierra MatchKing |
| Mass | 140 gr (9.07 g) | 175 gr (11.34 g) |
| Calibre | 0.264 in (6.71 mm) | 0.308 in (7.82 mm) |
| G7 BC | 0.315 lb/in² | 0.243 lb/in² |
| Muzzle velocity | 2700 fps (823.0 m/s) | 2600 fps (792.5 m/s) |
| Twist | 1:8 in, right-hand | 1:11.25 in, right-hand |
| Sight height | 1.75 in above bore | 1.75 in above bore |
| Zero | 100 yd | 100 yd |

The contrast load exists so that modules can show *why* a comparison matters --
the .308 goes transonic sooner, drifts more, and drops harder, which makes
several effects legible that a single load would hide.

### The spiral

Some topics are deliberately visited twice, at different depth. This is not
redundancy; the second pass is only possible because of what was built in
between.

| Topic | First pass | Second pass |
|---|---|---|
| Zeroing | M08, geometrically, in a vacuum | M16, as root-finding on a real trajectory |
| Wind | M18, uniform, with a closed-form approximation | M19, varying along the path |
| Effect magnitudes | M00, quoted from reference data | M29, computed by the reader's own solver |
| Error | M01, rounding and significant figures | M26, a full propagated uncertainty budget |
| Drag | M11, where the force comes from | M13, how it is parameterised for real bullets |

---
## Part 0 — Orientation

### M00 · What a Ballistic Solution Actually Is

`modules/00-orientation/` · no prerequisites · ~1.5 h

**Promise.** By the end you can name every force acting on a bullet in flight,
say roughly how big each one is at 100, 500, and 1000 yards, and explain what
the rest of the course is going to do about them.

**Objectives.** The reader can:
- Trace the path from trigger press to impact and name each stage.
- List the physical effects a solver models, ranked by magnitude at a given range.
- State which effects matter at 300 yards and which only appear past 1000.
- Run the course code and regenerate a figure.
- Read the course's unit and coordinate conventions.

**Mathematics.** Orders of magnitude and percentages only. No formulas are
derived; this module is a map, not a lesson.

**Physics.** Qualitative survey: gravity, drag, wind, gyroscopic effects,
Earth rotation. Each gets a paragraph and a forward reference to its module.

**Builds.** Nothing in `src/ballistics/`. This is deliberate -- the reader has
no tools yet.

**Data.** `modules/00-orientation/data/effect_magnitudes.csv`, a small table for
the running example at 100-yard increments to 1200 yards, with six effect
columns: drop, wind deflection, spin drift, aerodynamic jump, and Coriolis split
into its horizontal (latitude) and vertical (Eötvös, azimuth) parts. Six, not
five, because Figure 01 ranks six effects and because M23 treats the two
Coriolis components separately.

**The file is model output, not measurement, and the lesson must say so in its
body.** It is produced by
`modules/00-orientation/data/generate_effect_magnitudes.py`, a standalone
reference implementation shipped with this module. That script imports nothing
from `src/ballistics/` and is deliberately *not* the library the reader is about
to build -- it exists only so the reader has honest numbers on day one. The
lesson names it, names the empirical fits inside it (Litz for spin drift and
aerodynamic jump, Miller for gyroscopic stability), and states its assumptions:
atmosphere, wind, latitude, azimuth, and zero.

Module 17 regenerates this file from the reader's own solver and diffs it -- that
is the payoff. It means something because the two implementations are
independent, and because M00 was honest about where its numbers came from.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m00-fig01-effect-magnitudes` | Horizontal bars, each effect's magnitude in inches, faceted by range (100/500/1000 yd), log x-axis | Drop dominates by two orders of magnitude; wind is second; Coriolis is invisible until 1000 yd. Log scale is required or four of the six effects vanish. |
| 02 | `m00-fig02-solution-pipeline` | Block diagram: inputs (load, atmosphere, wind, geometry) → model → outputs (elevation, windage, ToF, velocity) | Every input is something you must *measure*, and Part IX is about how badly you measure them. |
| 03 | `m00-fig03-trajectory-anatomy` | Annotated single trajectory: bore line, line of departure, line of sight, near zero, apex, far zero, drop. Drawn at a **200-yard zero over 0–250 yd**, not the course's 100-yard zero, and the caption says which | The bullet is *above* the sight line for most of its flight — true at a 200-yard zero, false at 100, which is why the figure states its zero. Vertical scale is exaggerated ~50× and the caption must say so. |

**Exercises.** 5, all estimation: order-of-magnitude reasoning about time of
flight, drop, and lead. No formulas required; the point is to establish
intuition the later modules will sharpen or correct.

**Tests.** `tests/test_m00_orientation.py`, schema only. No physics is tested
here -- there is no library code yet. It checks that the CSV parses, that its
columns carry the exact names and unit suffixes M17 will look for, that the range
grid is complete, and that the provenance header survived. A column quietly
renamed seventeen modules from now should fail loudly rather than break M17's
diff in silence. `tools/check_curriculum.py` verifies the figures exist.

**Author pitfalls.**
- Do not derive anything here. The temptation to explain drag properly in the
  orientation module is strong and produces a bad Module 11.
- Figure 03's vertical exaggeration must be stated in the caption; an unlabelled
  exaggerated trajectory teaches a false mental image of a rainbow arc.
- The shipped data is model output, not measurement. Flag it as such in the
  lesson body, not just in `data/README.md`, and name both its generator and the
  empirical fits inside it.

---

## Part I — Mathematical Foundations

### M01 · Units, Measurement, and Dimensional Analysis

`modules/01-units/` · prereq M00 · ~2 h

**Promise.** You will stop making unit errors, and you will be able to check any
equation in this course -- or any ballistics forum post -- for dimensional sense
before you trust it.

**Objectives.** The reader can:
- Convert among grains, grams, fps, m/s, yards, metres, inches, inHg, hPa, °F, K.
- Test an equation for dimensional homogeneity and reject a wrong one.
- Distinguish accuracy from precision, and absolute from relative error.
- Apply significant-figure discipline and explain when it stops mattering.
- Explain why the library is SI internally despite an imperial audience.

**Mathematics.** Unit algebra as multiplication by one. Dimensional analysis
(M, L, T basis). Significant figures. Absolute vs relative error. Error
accumulation over repeated operations.

**Builds.**

`src/ballistics/units.py`

| Function | Purpose |
|---|---|
| `grains_to_kg`, `kg_to_grains` | mass |
| `fps_to_mps`, `mps_to_fps` | velocity |
| `yards_to_m`, `m_to_yards`, `inches_to_m`, `m_to_inches` | length |
| `feet_to_m`, `m_to_feet` | altitude |
| `inhg_to_pa`, `pa_to_inhg`, `hpa_to_pa` | pressure |
| `f_to_k`, `k_to_f`, `c_to_k`, `k_to_c` | temperature |
| `ftlb_to_j`, `j_to_ftlb` | energy |
| `mph_to_mps`, `mps_to_mph`, `kt_to_mps` | wind speed |
| `moa_to_rad`, `rad_to_moa`, `mil_to_rad`, `rad_to_mil`, `deg_to_rad`, `rad_to_deg`, `smoa_to_rad`, `rad_to_smoa` | angle. SMOA is a unit, so it is converted here; M02 owns the subtension *geometry* |

`src/ballistics/constants.py`

| Constant | Value | Note |
|---|---|---|
| `G0_MPS2` | 9.80665 | standard gravity |
| `GRAINS_PER_KG`, `M_PER_YARD`, ... | exact | conversion factors, defined exactly where the definition is exact |
| `ICAO_SEA_LEVEL` | dict | p, T, RH, ρ, a — the reference conditions |

Conversion factors are **exact by definition** where they are (1 yard ≡ 0.9144 m,
1 grain ≡ 64.79891 mg, 1 inch ≡ 25.4 mm) and the module says which are exact and
which are measured. This matters for the round-trip tests.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m01-fig01-unit-landscape` | Grouped bar / dot plot of the same physical quantity expressed in every unit a shooter meets | The numbers span orders of magnitude for one unchanged physical fact. |
| 02 | `m01-fig02-moa-vs-mil-subtension` | Subtension in inches vs range for 1 MOA, 1 SMOA, 1 mil | One MOA and one SMOA differ by 0.472 in at 1000 yd — which sounds harmless until you notice a 1000-yard come-up is ~31 of them, so confusing the two is about 15 in of elevation. |
| 03 | `m01-fig03-rounding-drift` | Cumulative error from rounding an intermediate value, over 1000 integration steps, at 3/4/6 significant figures | Rounding at 3 sig figs destroys a trajectory; this motivates float discipline in M05. |

**Exercises.** 7: conversion drills with a stated tolerance; dimensional
analysis of $F_D = \tfrac{1}{2}\rho v^2 C_D A$ *before* the reader has seen it
derived (they can confirm $C_D$ must be dimensionless); one deliberately
dimensionally-wrong formula to catch; a sig-figs judgement call.

**Tests.** `tests/test_m01_units.py` — round-trip identity to machine precision
for every pair; known-value checks (2700 fps = 822.96 m/s exactly, 140 gr =
9.0718 g, 29.9213 inHg = 101325 Pa to within 0.2 Pa, 1 MOA = 2.908882e-4 rad,
MOA / SMOA = $\pi/3$ exactly).

Two of those are traps. 140 gr is 9.0718 g, not the 9.0720 g you get from a
rounded 64.8 mg per grain; and 29.92 inHg is 101320.76 Pa, 4.24 Pa short of
standard pressure, so a test written against it is too loose to catch a real
conversion bug. Use 29.9213 inHg.

**Author pitfalls.**
- Get the MOA/SMOA distinction exactly right; it is the module's most useful
  single fact and is very commonly stated wrong.
- 1 grain = 64.79891 mg exactly. Not 64.8.
- Do not introduce `pint`. Section 2 of `docs/units-and-conventions.md` explains
  why, and the exercises depend on the reader doing the analysis by hand.

---

### M02 · Angles, Trigonometry, and Angular Measure

`modules/02-angles/` · prereq M01 · ~2 h

**Promise.** You will understand why your scope's clicks do what they do, be
able to range a target with your reticle, and know exactly when the small-angle
approximation stops being safe.

**Objectives.** The reader can:
- Solve the firing-geometry right triangles with sin, cos, tan.
- Derive subtension $s = R\tan\theta$ and state the error in the $s \approx R\theta$ form.
- Convert among MOA, SMOA/IPHY, mil, and degrees without confusion.
- Range a target from its reticle subtension, and compute the error that a
  10% target-size guess introduces.
- Set up the geometry of an inclined shot (solved in M08).

**Mathematics.** Right-triangle trig, radian measure, arc vs chord, the
small-angle approximation $\tan\theta \approx \theta$ with its
$\theta^3/3$ leading error term, error propagation through division (for
reticle ranging).

**Builds.** `src/ballistics/angles.py`

| Function | Purpose |
|---|---|
| `subtension_m(angle_rad, range_m)` | exact, `range_m * tan(angle_rad)` |
| `angle_for_offset_rad(offset_m, range_m)` | exact, `atan2` |
| `mil_ranging_m(target_size_m, mils)` | range from reticle subtension |
| `mil_ranging_error(target_size_m, size_err, mils, mil_err)` | propagated range uncertainty |
| `moa_subtension_in(range_yd)`, `smoa_subtension_in(range_yd)` | presentation helpers |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m02-fig01-small-angle-error` | Relative error of $\theta$ vs $\tan\theta$, log-log, with the course's working angle range shaded | Below ~1° the error is under 0.01%; at 5° it is 0.25%. For elevation *angles* this is fine; for *corrections* it never matters. The plot tells you where the line is. |
| 02 | `m02-fig02-reticle-ranging` | Diagram of reticle ranging plus an error band: range uncertainty vs assumed-target-size uncertainty | A 10% target-size error is a 10% range error, which at 800 yd is 80 yd and a clean miss. This is why laser rangefinders won. |
| 03 | `m02-fig03-angular-units` | Subtension of 1 MOA / 1 SMOA / 1 mil / 0.1 mil vs range, direct-labelled | 0.1 mil and 1/4 MOA are nearly the same click value out to 600 yd, then separate. |

**Exercises.** 6: click arithmetic on a real dial; a mil-ranging problem with
error bars; find the range at which the small-angle approximation costs one
inch; MOA vs SMOA on a 1000-yard correction.

**Tests.** `tests/test_m02_angles.py` — known subtensions (1 MOA at 100 yd =
1.047 in; 1 mil at 100 m = 10 cm exactly); round-trip `angle_for_offset` ∘
`subtension`; ranging formula against hand-computed values.

**Author pitfalls.**
- "1 mil = 3.6 inches at 100 yards" is an approximation of an exact metric fact
  (1 mil = 10 cm at 100 m = 3.6 in at 100 yd is *exactly* right only because
  100 yd = 91.44 m and 0.001 × 91.44 m = 9.144 cm = 3.6 in). Work it through;
  do not hand-wave.
- Use `atan`, not division, in `angle_for_offset_rad` -- the module is about
  knowing the difference.

---

### M03 · Vectors and Coordinate Systems

`modules/03-vectors/` · prereq M02 · ~2.5 h

**Promise.** You will be able to break any velocity or wind into components, and
you will know exactly what frame every number in this course lives in.

**Objectives.** The reader can:
- Add, scale, and normalise 3D vectors; compute dot and cross products and say
  what each *means* physically.
- Decompose a wind given as a clock direction into course-frame components.
- State the course's coordinate convention from memory and explain why the
  x-axis follows the line of sight rather than the ground.
- Distinguish bore line, line of departure, and line of sight.
- Rotate a vector between frames with a rotation matrix.

**Mathematics.** Vector algebra, unit vectors, dot product as projection, cross
product as perpendicular/area/rotation, 3×3 rotation matrices, change of basis,
handedness.

**Builds.** `src/ballistics/frames.py`

| Function | Purpose |
|---|---|
| `unit(v)`, `norm(v)` | thin wrappers with the course's error behaviour on zero vectors |
| `rot_x(a)`, `rot_y(a)`, `rot_z(a)` | rotation matrices |
| `wind_vector_mps(speed_mps, clock_hour, ...)` | clock direction → course frame; **the single place the from/toward convention flips** |
| `wind_from_bearing_mps(speed_mps, bearing_rad, azimuth_rad)` | compass form, for M23 |
| `incline_gravity(g, incline_rad)` | gravity in the tilted line-of-sight frame |
| `los_frame(incline_rad, azimuth_rad)` | basis for the course frame given rifle orientation |

This module writes the frame diagram into `docs/units-and-conventions.md` §4 if
it is not already accurate there, and must not contradict it.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m03-fig01-course-frame` | 3D axes with muzzle, line of sight, bore line, and gravity drawn in | The x-axis follows the *sight line*, so on an incline it is not horizontal, and gravity gains an x-component. |
| 02 | `m03-fig02-wind-clock` | Polar plot: full-value/half-value crosswind component vs clock direction | A 4 o'clock wind is 87% of full value, not 50% — the common "half value" rule is wrong by a lot. |
| 03 | `m03-fig03-incline-decomposition` | Gravity resolved in the tilted frame at 0°, 15°, 30°, 45° | The component perpendicular to the sight line is $g\cos\phi$ — the seed of the rifleman's rule, and of its failure. |

**Exercises.** 6: component decomposition; the dot product as "how much of this
wind is crosswind"; a cross product for the direction of a rotational effect;
one exercise establishing that a 45° wind is 71% and a 4 o'clock wind is 87%.

**Tests.** `tests/test_m03_frames.py` — rotation matrices are orthonormal with
determinant +1; `wind_vector_mps` sign conventions (3 o'clock wind gives
$W_z < 0$); round-trip rotations.

**Author pitfalls.**
- The wind sign convention is the highest-risk thing in the whole course. Every
  later wind figure depends on it. Write the test first.
- Clock directions: 12 o'clock is a headwind (from downrange), 3 o'clock is from
  the shooter's right. Since $\vec W$ is the direction air *moves*, a 3 o'clock
  wind has $W_z < 0$. State this three times.
- Do not introduce quaternions. This is a 3DOF course; rotation matrices are
  sufficient and quaternions would be scope creep.

---

### M04 · Rates of Change: Derivatives and Integrals

`modules/04-calculus/` · prereq M03 · ~3 h

**Promise.** Calculus, taught only as far as this course needs it, using
trajectories as the entire motivating example.

**Objectives.** The reader can:
- Explain the derivative as a limit of average rates, and read $dv/dt$ aloud correctly.
- Move between position, velocity, and acceleration in both directions.
- Differentiate polynomials and exponentials; apply the chain rule.
- Interpret a definite integral as accumulated change and state the fundamental
  theorem in their own words.
- Compute a derivative numerically and explain why the step size cannot be
  arbitrarily small.

**Mathematics.** Limits, the difference quotient, derivative rules (power,
sum, product, chain), the derivative of $e^x$, definite integrals as area,
Riemann sums, the fundamental theorem of calculus, numerical differentiation
(forward vs central) and the truncation/round-off tradeoff, trapezoid and
Simpson quadrature.

**Builds.** `src/ballistics/numeric.py`

| Function | Purpose |
|---|---|
| `forward_difference(f, x, h)` | $O(h)$ |
| `central_difference(f, x, h)` | $O(h^2)$ |
| `optimal_step(f, x)` | the $\sqrt{\epsilon}$ heuristic, with the reasoning in the docstring |
| `trapezoid(f, a, b, n)`, `simpson(f, a, b, n)` | quadrature |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m04-fig01-secant-to-tangent` | Small multiples: secant lines converging to the tangent as $h\to0$ | The derivative is a limit, and the picture *is* the definition. |
| 02 | `m04-fig02-riemann-convergence` | Riemann sums with 4, 8, 16, 64 rectangles under a velocity curve, with the accumulated-distance error annotated | The integral of velocity is distance; more rectangles is a better answer, and the error has a *rate*. |
| 03 | `m04-fig03-numerical-derivative-error` | Error of forward vs central difference vs step size, log-log, showing the round-off wall | Two error sources fight: truncation falls as $h$ shrinks, round-off rises. There is an optimal $h$, and this is why M05 cares about step size. |
| 04 | `m04-fig04-kinematic-triptych` | Stacked $x(t)$, $v(t)$, $a(t)$ for a real decelerating bullet | The slope of each panel is the panel below it. Velocity is *not* linear, which is why average-velocity estimates of time of flight are wrong. |

**Exercises.** 7: differentiate/integrate by hand; the average-velocity fallacy
worked numerically; find the optimal step size empirically; a chain-rule problem
on drag as a function of speed as a function of time.

**Tests.** `tests/test_m04_numeric.py` — derivatives of known functions to
tolerance; central difference demonstrably second-order; quadrature exact for
polynomials of the appropriate degree.

**Author pitfalls.**
- Motivate from ballistics throughout. A reader who wanted a generic calculus
  course would not be here.
- Figure 03 is the module's keystone. Get the round-off wall right by actually
  computing it in float64, not by drawing a schematic.

---

### M05 · Differential Equations and Numerical Integration

`modules/05-odes/` · prereq M04 · ~4 h · **keystone module**

**Promise.** This is the engine of every ballistic solver ever written. After
this module you can integrate any equation of motion, and you can prove your
answer is converged rather than hoping.

**Objectives.** The reader can:
- Recognise an initial value problem and state one for a projectile.
- Implement Euler, Heun (RK2), and RK4 from the Taylor expansion.
- Distinguish local truncation error from global error and predict how each
  scales with step size.
- Measure a method's convergence order empirically and confirm it matches theory.
- Choose a step size from a stated accuracy requirement rather than by feel.
- Explain what an adaptive solver does and when to reach for one.
- Detect an event (a zero crossing) during integration and locate it accurately.

**Mathematics.** ODEs and IVPs; Taylor expansion as the source of every
Runge-Kutta method; local vs global truncation error; order of accuracy and how
to measure it from a log-log slope; stability and why explicit methods can blow
up; embedded RK pairs and adaptive step control; event detection by root-finding
on a dense output.

**Builds.** `src/ballistics/integrators.py`

| Function | Purpose |
|---|---|
| `euler(f, y, t, h)`, `heun(f, y, t, h)`, `rk4(f, y, t, h)` | single steps, written to be *read* |
| `integrate(f, y0, t_span, h, events=None, method="rk4")` | fixed-step driver with dense output |
| `Event(name, g, direction, terminal)` | event specification: a scalar function whose zero crossing is the event |
| `locate_event(...)` | Brent refinement of a bracketed crossing |
| `convergence_order(f, y0, exact, t_end, steps)` | measures a method's order — used by tests and by M17 |

`integrate` returns a `Solution` with `t`, `y`, and `events`, plus an
interpolant. Its API is used unchanged by every solver module after this, so it
is designed here with that in mind.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m05-fig01-method-comparison` | Euler, Heun, RK4 vs the exact solution of a known ODE, same step count | Euler is visibly wrong at a step size where RK4 is indistinguishable from exact. |
| 02 | `m05-fig02-convergence-orders` | Global error vs step size, log-log, all three methods, with reference slopes 1, 2, 4 | The slopes are the *orders*. This plot is how you prove an integrator is correct, and it recurs in M17. |
| 03 | `m05-fig03-accuracy-vs-cost` | Error vs number of function evaluations | RK4 costs 4× per step and buys far more than 4× the accuracy. This is why nobody uses Euler. |
| 04 | `m05-fig04-event-detection` | A trajectory crossing a threshold, with naive per-step detection vs Brent refinement | Step-granular event detection is wrong by up to a full step; a 1000-yard zero found this way can be off by yards. |

**Exercises.** 8: implement RK2 from the Taylor expansion; measure the
convergence order of a method you were given; find the step size meeting a 1 cm
accuracy budget over 1000 m; break Euler with a stiff problem; add an event.

**Tests.** `tests/test_m05_integrators.py` — measured convergence order within
0.1 of theory for each method; exponential decay and simple harmonic motion
against exact solutions; event location accurate to 1e-9 on a known crossing.

**Author pitfalls.**
- This module's API is load-bearing for eleven later modules. Design
  `integrate`, `Solution`, and `Event` carefully and do not change them later
  without a documented migration.
- Derive RK4 from Taylor expansion far enough that it stops looking like magic
  coefficients. A reader who takes RK4 on faith will not trust their own solver.
- Do not simply wrap `scipy.solve_ivp`. Write the methods; *then* show that
  scipy agrees, and explain when to use it (M16 revisits this).

---
## Part II — Classical Mechanics of Projectiles

### M06 · Newton's Laws, Momentum, and Energy

`modules/06-newton/` · prereq M05 · ~2.5 h

**Promise.** The three laws, applied to the two things a shooter actually cares
about: what the bullet does downrange, and what the rifle does to your shoulder.

**Objectives.** The reader can:
- State Newton's three laws and apply the second to a projectile.
- Compute kinetic energy and momentum in both SI and shooting units.
- Compute free recoil energy and velocity, including the propellant gas term.
- Explain impulse and estimate barrel time.
- Explain why "energy at target" is a weak proxy for terminal effect, and why
  momentum is not a better one.

**Mathematics.** $F=ma$, $p=mv$, $KE=\tfrac12 mv^2$, impulse-momentum theorem,
conservation of momentum applied to the rifle-bullet-gas system, work-energy
theorem.

**Physics.** Inertia, force, mass; action-reaction as the origin of recoil;
why the gas column matters (it can be a third of felt recoil).

**Builds.** `src/ballistics/energy.py`

| Function | Purpose |
|---|---|
| `kinetic_energy_j(mass_kg, velocity_mps)` | |
| `momentum_kgmps(mass_kg, velocity_mps)` | |
| `free_recoil(rifle_kg, bullet_kg, charge_kg, mv_mps, gas_factor=1.75)` | returns recoil velocity and energy; `gas_factor` documented as an empirical multiplier with its source |
| `power_factor(mass_gr, velocity_fps)` | the competition metric, included because readers will meet it |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m06-fig01-recoil-comparison` | Free recoil energy for a set of common cartridges in a constant-weight rifle | Recoil scales with bullet mass *and* charge mass; the gas term is not negligible. |
| 02 | `m06-fig02-energy-momentum-downrange` | KE and momentum vs range for the two running loads, normalised to muzzle | Energy falls off much faster than momentum, because energy goes as $v^2$. Two loads can rank differently depending on which metric you pick — which is the point. |
| 03 | `m06-fig03-recoil-sensitivity` | Recoil energy vs rifle weight and vs charge weight | Rifle weight is the lever you actually control. |

**Exercises.** 6: recoil for the reader's own rifle; the $v^2$ consequence;
a conservation-of-momentum problem; an impulse/barrel-time estimate.

**Tests.** `tests/test_m06_energy.py` — known KE values (140 gr at 2700 fps ≈
2266 ft·lb); momentum conservation in the recoil calculation; power factor
against a published example.

**Author pitfalls.**
- Free recoil formulas vary in how they treat propellant gas. State which form
  is used and cite it; `gas_factor` is empirical and must be labelled as such
  per the honesty rule.
- Resist terminal ballistics. "Energy at target" gets a paragraph on why it is a
  weak proxy and a pointer to `docs/appendix-further-study.md`, not a treatment.

---

### M07 · Trajectory in a Vacuum

`modules/07-vacuum-trajectory/` · prereq M06 · ~3 h

**Promise.** The first complete trajectory, derived from scratch and solved
exactly -- which makes it the yardstick that proves your numerical solver works.

**Objectives.** The reader can:
- Derive $x(t)$ and $y(t)$ for a projectile under constant gravity, by integration.
- Compute apex height, time of flight, and range in closed form.
- Solve for the launch angle that reaches a given range, and explain the two roots.
- Explain why 45° maximises vacuum range and predict why air changes that.
- Use the analytic solution to verify a numerical integrator.

**Mathematics.** Integrating constant acceleration twice; eliminating $t$ to get
the parabola; the range equation $R = v_0^2\sin 2\theta / g$; quadratic roots and
their meaning (the low and high trajectory to the same target).

**Builds.** `src/ballistics/vacuum.py`

| Function | Purpose |
|---|---|
| `position(t, v0_mps, angle_rad)` | exact $(x,y)$ |
| `time_of_flight_s(v0_mps, angle_rad, y_end_m=0.0)` | |
| `range_m(v0_mps, angle_rad)` | |
| `apex(v0_mps, angle_rad)` | height and time |
| `angle_for_range_rad(v0_mps, range_m, high=False)` | both roots |
| `derivatives(t, state)` | the ODE form, for feeding to `integrate` — the bridge to M15 |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m07-fig01-angle-family` | Vacuum trajectories at 15°/30°/45°/60°/75°, complementary pairs sharing a colour | Complementary angles reach the same range; 45° is the maximum. |
| 02 | `m07-fig02-analytic-vs-rk4` | Two panels: trajectories overlaid (indistinguishable), and the RK4−analytic residual in millimetres | Sub-millimetre agreement over a kilometre. **This is what "the integrator is correct" looks like**, and it is the template for every validation in the course. |
| 03 | `m07-fig03-vacuum-vs-reality` | The vacuum trajectory for the running load against its real (precomputed, from M00 data) trajectory | Vacuum predicts 1.4 miles of range. Air is not a correction to this problem; it dominates it. |

**Exercises.** 7: derive the range equation; find both launch angles to a given
range; compute the vacuum drop at 1000 yd and compare to reality; show
numerically that RK4 converges to the analytic answer; explain the 45° result.

**Tests.** `tests/test_m07_vacuum.py` — analytic identities (complementary
angles, apex at $v_0^2\sin^2\theta/2g$); **`rk4` integration of `derivatives`
matches the closed form to < 1 mm over 1000 m** — the first cross-module
validation, and the pattern M15 and M17 reuse.

**Author pitfalls.**
- Figure 02 is the most important figure in Part II. It must show the residual
  in a second panel with real units, not just two overlapping curves.
- Keep the vacuum-vs-real comparison honest: it uses M00's precomputed data
  because the drag solver does not exist yet. Say so.

---

### M08 · Sight Geometry, Line of Sight, and Zeroing

`modules/08-zeroing/` · prereq M07 · ~3 h

**Promise.** Why a bullet crosses your line of sight twice, what a "zero"
actually is, and why the standard trick for shooting uphill is wrong.

**Objectives.** The reader can:
- Distinguish bore line, line of departure, and line of sight, and explain the
  role of sight height.
- Explain why there are two zero crossings and compute both.
- Produce a drop table relative to the line of sight rather than to the bore.
- Compute maximum point-blank range for a given vital-zone size.
- Set up an inclined shot correctly, and quantify the error of the rifleman's rule.

**Mathematics.** Intersecting a line with a parabola; root-finding to solve for
launch angle (first practical use of the M05 machinery); decomposing gravity in
a tilted frame; the $\cos\phi$ approximation and its residual.

**Physics.** The geometric relationship between sight, bore, and path. On
inclines: only the component of gravity perpendicular to the line of sight
causes deviation *from* that line, but the parallel component still changes
speed, which is exactly why the simple rule fails at steep angles and long range.

**Builds.** `src/ballistics/sight.py`

| Function | Purpose |
|---|---|
| `path_above_los_m(trajectory, sight_height_m)` | converts a bore-referenced path to a sight-referenced one |
| `find_zero_angle_rad(solver, zero_range_m, sight_height_m)` | root-find on launch angle; works with the vacuum solver now, the real one from M16 |
| `near_far_zeros_m(...)` | both crossings |
| `point_blank_range_m(..., vital_radius_m)` | |
| `riflemans_rule_range_m(range_m, incline_rad)` | the $R\cos\phi$ approximation, clearly labelled |
| `incline_solution(...)` | the correct treatment, for comparison |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m08-fig01-sight-geometry` | Bore line, line of sight, and path, with both zero crossings and the sight-height offset, vertical scale exaggerated (stated in caption) | The bullet starts 1.75 in *below* the sight line, crosses it near 25-40 yd, peaks above it, and crosses back at the far zero. |
| 02 | `m08-fig02-zero-choices` | Path above LOS for 100 / 200 / 300 yd zeros | A 200 yd zero keeps the bullet within ±3 in to past 250 yd; that is the entire argument for point-blank zeroing. |
| 03 | `m08-fig03-riflemans-rule-error` | Error of the rifleman's rule in inches, as a heatmap over incline angle × range | The rule is fine at 300 yd and any angle; it fails past 600 yd at steep angles. The failure region is the useful output. |

**Exercises.** 7: compute both zeros for the running load; choose a zero for a
stated use case and defend it; point-blank range for a 6-inch vital zone; the
rifleman's rule error at 45° and 1000 yd; why sight height changes near zero but
barely changes far zero.

**Tests.** `tests/test_m08_sight.py` — zero solver produces a path passing
through zero at the requested range to < 1 mm; two distinct crossings exist for
realistic sight heights; the incline solution reduces to the flat case at 0°.

**Author pitfalls.**
- The vertical exaggeration must be stated in every caption that uses it.
- The rifleman's rule is $R_{\text{eff}} = R\cos\phi$ applied to *range*, not a
  multiplier on drop. Getting this backwards is common; state the rule precisely
  before criticising it.
- This module uses the vacuum solver, so its numbers are not field-accurate. Say
  so and forward-reference M16.

---

## Part III — The Atmosphere

### M09 · Air Density, Pressure, Temperature, and Humidity

`modules/09-atmosphere/` · prereq M06 (and M01) · ~3 h

**Promise.** Drag is proportional to air density, so this module is where you
learn to compute the single most important environmental number, and to spot the
input error that ruins more firing solutions than any other.

**Objectives.** The reader can:
- Compute air density from pressure, temperature, and humidity.
- Explain the difference between station pressure and sea-level-corrected
  pressure, and why entering the wrong one is a large error.
- Explain why humid air is *less* dense than dry air.
- Implement the ICAO standard atmosphere and evaluate it at altitude.
- Compute density altitude and use it as a single-number summary.
- Rank temperature, pressure, humidity, and altitude by their effect on density.

**Mathematics.** Ideal gas law $p = \rho R T$; Dalton's law of partial
pressures; the Buck equation for saturation vapour pressure; hydrostatic balance
$dp/dh = -\rho g$ integrated with a constant lapse rate to give the barometric
formula (derived, not quoted).

**Physics.** Why a water molecule (18 g/mol) is lighter than the N₂ (28) and O₂
(32) it displaces, so humidity lowers density -- counter to most people's
intuition, and worth a full paragraph.

**Builds.** `src/ballistics/atmosphere.py` (part 1 of 2)

| Function | Purpose |
|---|---|
| `air_density_kgm3(pressure_pa, temp_k, rh=0.0)` | the workhorse |
| `saturation_vapor_pressure_pa(temp_k)` | Buck equation, cited |
| `isa(altitude_m)` | ICAO standard atmosphere: p, T, ρ |
| `pressure_from_altitude_pa(altitude_m, ...)` | barometric formula |
| `station_pressure_pa(sealevel_pa, altitude_m, temp_k)` | the correction people get wrong |
| `density_altitude_m(pressure_pa, temp_k, rh)` | |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m09-fig01-isa-profile` | ICAO pressure, temperature, and density vs altitude to 15 km, three panels | Density falls ~3% per 1000 ft near the surface. That is why the same load shoots flatter in Denver. |
| 02 | `m09-fig02-density-sensitivity` | Tornado chart: Δρ from realistic swings in T, p, RH, altitude | Pressure and temperature dominate; humidity is a rounding error at normal conditions, contrary to folklore. |
| 03 | `m09-fig03-station-vs-sealevel` | Drop error at 1000 yd from entering sea-level pressure when station pressure was required, vs shooter altitude | At 5000 ft the mistake is worth feet of vertical. This figure is the module's reason for existing. |

**Exercises.** 7: compute density for stated conditions; show humid air is
lighter; find the density altitude of a hot day at altitude; quantify the
station-pressure mistake; derive the barometric formula.

**Tests.** `tests/test_m09_atmosphere.py` — ICAO reference values at 0, 5 000,
11 000 m (and 36 089 ft, the tropopause) within published tolerance; sea-level
density 1.225 kg/m³; monotonic decrease of density with humidity at fixed p, T.

**Author pitfalls.**
- Most weather meters (Kestrel and similar) report **station** pressure;
  airport METARs and phone weather apps report **sea-level-corrected**. Solvers
  want station. This confusion is the single most common real-world solver input
  error and deserves the emphasis Figure 03 gives it.
- Derive the barometric formula. Quoting it wastes the calculus taught in M04.

---

### M10 · Speed of Sound, Mach Number, and the Transonic Region

`modules/10-mach/` · prereq M09 · ~2 h

**Promise.** Drag depends on Mach number, not speed -- so before drag, you need
to know what the air's speed of sound is on the day you are shooting.

**Objectives.** The reader can:
- Compute the speed of sound from temperature and explain why pressure does not
  appear.
- Convert velocity to Mach number for given conditions.
- Define the subsonic, transonic, and supersonic regimes by Mach number.
- Explain qualitatively why the transonic region disturbs a bullet.
- Compute the range at which a given load goes transonic, and show how much that
  range moves with conditions.

**Mathematics.** $a = \sqrt{\gamma R_d T}$ derived from the adiabatic bulk
modulus; the small humidity correction; $M = v/a$.

**Physics.** Sound as a pressure wave; why the speed depends only on temperature
for an ideal gas; shock formation as the bullet outruns its own pressure
disturbance; why the transonic passage is destabilising (drag rises steeply and
the centre of pressure moves).

**Builds.** `src/ballistics/atmosphere.py` (part 2)

| Function | Purpose |
|---|---|
| `speed_of_sound_mps(temp_k, rh=0.0)` | |
| `mach(velocity_mps, temp_k, rh=0.0)` | |
| `transonic_range_m(trajectory, temp_k)` | the range at M = 1.2 |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m10-fig01-speed-of-sound` | $a$ vs temperature over a realistic range, with humidity as a barely-visible second line | 20 m/s across a season. Pressure is absent, which surprises people. |
| 02 | `m10-fig02-mach-downrange` | Mach vs range for both running loads, with the transonic band shaded | The 6.5 CM stays supersonic ~250 yd further than the .308. The band, not a line, is the honest picture. |
| 03 | `m10-fig03-transonic-range-conditions` | Range at which the load reaches M 1.2, vs temperature and density altitude | "Supersonic to 1200 yards" is a claim about a *day*, not about a cartridge. |

**Exercises.** 6: speed of sound on a cold morning vs a hot afternoon; Mach at
600 yd; find the transonic range for the reader's load under two conditions;
explain why pressure is missing from the formula.

**Tests.** `tests/test_m10_mach.py` — 340.29 m/s at 288.15 K; monotonic in
temperature; humidity correction small and positive.

**Author pitfalls.**
- The transonic *band* is roughly M 0.8-1.2, not a point at M 1.0. Bullets get
  disturbed on the way down through it, well above M 1.0.
- Do not attempt the aerodynamics of transonic instability here — that requires
  the pitching-moment material this course does not cover. Give the qualitative
  picture and point at M20-M21 and the appendix.

---
## Part IV — Aerodynamic Drag

### M11 · Where Drag Comes From

`modules/11-drag-physics/` · prereq M10 · ~3 h

**Promise.** Before you use a drag coefficient, you should know what it is a
coefficient *of*. This module builds the drag equation from dimensional analysis
and explains the three physically distinct things it lumps together.

**Objectives.** The reader can:
- Name the three sources of drag on a bullet -- pressure/base drag, skin
  friction, wave drag -- and say which dominates at which Mach number.
- Explain the boundary layer and flow separation qualitatively.
- Compute a Reynolds number for a bullet and interpret it.
- Derive the form $F_D = \tfrac12 \rho v^2 C_D A$ by dimensional analysis and
  explain why $C_D$ must be dimensionless.
- Explain why $C_D$ is a function of Mach number rather than of speed.

**Mathematics.** Dimensional analysis / Buckingham-π applied to
$F_D = f(\rho, v, d, \mu, a)$, yielding $C_D = f(\text{Re}, M)$; Reynolds number;
Sutherland's law for viscosity.

**Physics.** Boundary layer, laminar vs turbulent, separation and the base wake;
shock waves and wave drag above M 1; why base drag is a large fraction of total
drag for a flat-based bullet and what a boattail does about it.

**Builds.** `src/ballistics/aero.py`

| Function | Purpose |
|---|---|
| `drag_force_n(density_kgm3, velocity_mps, cd, area_m2)` | |
| `reference_area_m2(diameter_m)` | $\pi d^2/4$ |
| `dynamic_pressure_pa(density_kgm3, velocity_mps)` | |
| `air_viscosity_pas(temp_k)` | Sutherland |
| `reynolds(density_kgm3, velocity_mps, length_m, temp_k)` | |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m11-fig01-drag-sources` | Stacked area: pressure, friction, and wave drag as fractions of total $C_D$ vs Mach, from published data (cited) | Wave drag appears from nothing at M 1 and then dominates. Below M 0.8 there is none at all. |
| 02 | `m11-fig02-flow-regimes` | Schematic: attached boundary layer, separation at the base, the bow shock above M 1 | The wake behind a flat base is a low-pressure region *pulling backwards*. That is base drag. |
| 03 | `m11-fig03-reynolds-range` | Reynolds number vs range for the running loads, with the transition band marked | Re stays high enough that the boundary layer is turbulent throughout — which is why $C_D$ ends up a function of Mach almost alone. |

**Exercises.** 6: dimensional analysis producing the drag equation; compute drag
force at the muzzle and compare it to the bullet's weight (it is ~50× larger,
which is the module's punchline); Reynolds number at three ranges; explain the
boattail.

**Tests.** `tests/test_m11_aero.py` — drag force against hand-computed values;
Sutherland viscosity at 288.15 K ≈ 1.789e-5 Pa·s; reference area for a 0.264 in
bullet.

**Author pitfalls.**
- The punchline of Figure 03 plus the exercise is that drag deceleration at the
  muzzle is on the order of 50 g. State it; it reframes gravity as the *small*
  force for the first half of the flight.
- Figure 01 uses published breakdown data. Cite the source in `data/README.md`
  and do not present a schematic as measurement.

---

### M12 · The Drag Coefficient Curve

`modules/12-cd-curve/` · prereq M11 · ~2.5 h

**Promise.** The drag coefficient is not a number; it is a curve. This module
teaches you to read one, and to interpolate it without introducing errors.

**Objectives.** The reader can:
- Read a $C_D$ vs Mach curve and identify the transonic rise.
- Explain physically why $C_D$ peaks just above M 1 and then falls.
- Compare the $C_D$ curves of different projectile shapes.
- Interpolate tabulated $C_D$ data and choose a scheme appropriate to the
  transonic knee.
- Explain why extrapolating past the table is dangerous, and guard against it.

**Mathematics.** Piecewise-linear vs cubic-spline vs PCHIP interpolation;
overshoot in splines near a knee; extrapolation guards.

**Builds.** `src/ballistics/drag.py` (part 1 of 3)

| Object | Purpose |
|---|---|
| `DragCurve(mach, cd, *, kind="pchip", name=None)` | callable Mach → $C_D$ |
| `DragCurve.from_csv(path)` | loads the standard table format |
| `DragCurve.__call__(mach)` | vectorised, raises outside the table range unless `clamp=True` |

Interpolation defaults to PCHIP (shape-preserving), and the module explains that
choice against the alternatives rather than asserting it.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m12-fig01-g1-g7-curves` | $C_D$ vs Mach for the G1 and G7 reference projectiles, overlaid, with the reference shapes drawn inset | Same qualitative shape, very different magnitude and knee position. A single number cannot capture the difference. |
| 02 | `m12-fig02-interpolation-knee` | Linear vs cubic spline vs PCHIP through sparse table points across M 0.9-1.2, zoomed | The cubic spline overshoots at the knee and produces a physically impossible $C_D$ dip. This is a real bug people ship. |
| 03 | `m12-fig03-shape-gallery` | $C_D$ curves for flat-base, boattail, and long-ogive forms | Shape changes the curve's *level* far more than its shape, which is what makes the form-factor idea in M13 work. |

**Exercises.** 6: read values off a curve; compute the $C_D$ ratio between M 2.0
and M 0.9; demonstrate spline overshoot numerically; explain the extrapolation
guard.

**Tests.** `tests/test_m12_drag_curve.py` — interpolation reproduces table nodes
exactly; PCHIP is monotone where the data is; out-of-range raises unless clamped.

**Author pitfalls.**
- Figure 02 must show a *real* overshoot computed from real sparse data, not an
  illustration. If the overshoot does not appear with a given sampling, find the
  sampling where it does — it is easy to produce and it is the point.
- The G1/G7 table data is created in M13 along with `data/drag_tables/`. M12 may
  need to create the two tables it plots; if so, it creates them in
  `data/drag_tables/` with full provenance and M13 uses them rather than
  duplicating.

---

### M13 · Ballistic Coefficient, Form Factor, and Drag Models

`modules/13-ballistic-coefficient/` · prereq M12 · ~3.5 h

**Promise.** What BC actually means, why the number on the box is not the number
your bullet has, and why a G7 BC is worth more than a G1 BC for a modern bullet.

**Objectives.** The reader can:
- Define sectional density and compute it.
- Define form factor as the ratio of a bullet's drag to a reference
  projectile's, and derive $\text{BC} = \text{SD}/i$.
- Explain the reference-projectile idea and the G-family of standard shapes.
- Explain why a G1 BC varies with velocity and must be banded, while a G7 BC for
  a modern bullet is nearly constant.
- Convert approximately between G1 and G7 BCs and state the uncertainty in doing so.
- Choose the right drag model for a given bullet and justify it.

**Mathematics.** $\text{SD} = m/d^2$; $i = C_D^{\text{bullet}}/C_D^{\text{ref}}$;
$\text{BC} = \text{SD}/i$; scaling a reference curve by the form factor;
retardation $= \rho v^2 C_D A / 2m$ rewritten in terms of BC.

**Builds.** `src/ballistics/drag.py` (part 2)

| Object | Purpose |
|---|---|
| `sectional_density_lbin2(mass_gr, diameter_in)` | |
| `form_factor(bc_lbin2, sd_lbin2)` | |
| `bc_from_form_factor(sd_lbin2, i)` | |
| `DragModel(bc_lbin2, family="G7")` | wraps a `DragCurve` + BC; provides `cd(mach)` and `retardation_mps2(velocity_mps, density_kgm3)` |
| `BandedDragModel(bands)` | velocity-banded G1 BCs, as published by some makers |
| `g1_to_g7_estimate(bc_g1)` | approximate, with the uncertainty stated in the return docstring |

**Data.** Creates `data/drag_tables/{g1,g2,g5,g6,g7,g8}.csv` in the standard
two-column Mach, $C_D$ format, with source and retrieval date recorded in
`data/README.md`. These tables are the published BRL/Ingalls-derived standard
drag functions; the provenance entry must name the specific source used.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m13-fig01-g1-vs-g7-drop` | Predicted drop for the *same* bullet using its G1 BC and its G7 BC, plus the difference in inches | They agree to 500 yd and diverge past it. At 1000 yd the disagreement is large enough to miss with. |
| 02 | `m13-fig02-banded-g1` | A published banded G1 BC as a step function, with the equivalent flat G7 BC | The bands exist because G1 is the wrong reference shape; they are patching a modelling error. |
| 03 | `m13-fig03-form-factor-gallery` | Form factor vs bullet shape for a set of real bullets, G1 and G7 references side by side | Against G7, modern match bullets cluster near $i \approx 1$; against G1 they scatter. That clustering *is* the argument for G7. |

**Exercises.** 7: compute SD and BC for a bullet from its mass and calibre;
derive $\text{BC}=\text{SD}/i$; convert a G1 BC to G7 and bound the error;
explain banding; pick a model for three different bullets and defend each.

**Tests.** `tests/test_m13_bc.py` — published SD/BC/form-factor triples for
real bullets within tolerance; retardation consistent with the M11 drag force
for the same conditions (a genuine cross-check between two derivations); the
banded model reduces to a flat model with one band.

**Author pitfalls.**
- **The units trap.** BC and SD are in lb/in². The retardation formula in SI
  needs the conversion, and getting it wrong yields answers wrong by a factor
  that looks plausible. Write the test first.
- Older G1 BCs were computed against Army Standard Metro, not ICAO. If the
  module uses published BCs it must say which standard they assume — this is a
  ~0.5% density difference and it is the kind of detail this course exists to
  get right.
- Be specific about what "the BC on the box" gets wrong (measurement conditions,
  bullet-to-bullet variation, marketing optimism) and cite independently
  measured comparisons rather than asserting it.

---

### M14 · Custom Drag Curves and Doppler-Derived Models

`modules/14-custom-drag/` · prereq M13 · ~2.5 h

**Promise.** How a bullet's actual drag curve gets measured, and what you gain
by using one instead of a scaled reference shape.

**Objectives.** The reader can:
- Explain how Doppler radar produces a $C_D$ vs Mach curve for a real bullet.
- Load a custom drag curve and use it in place of a G-model.
- Fit a scale factor to match a custom curve to measured drop data.
- Compare CDM, G7, and G1 predictions for the same bullet and identify where
  they diverge and why.
- State when a custom curve is worth the trouble and when it is not.

**Mathematics.** Least-squares fitting of a single scale factor; residual
analysis; goodness of fit; the difference between fitting a *shape* and fitting
a *scale*.

**Builds.** `src/ballistics/drag.py` (part 3)

| Object | Purpose |
|---|---|
| `CustomDragCurve.from_csv(path)` | a measured Mach/$C_D$ table for one specific bullet |
| `fit_scale_factor(measured, reference)` | least-squares scale of a reference curve to measurements |
| `compare_models(models, conditions)` | drop/drift/velocity table across models, for the figures and for M28 |

**Data.** `modules/14-custom-drag/data/` gets a synthetic measured curve for the
running load, **clearly labelled synthetic** in both the file header and the
lesson. It is generated by perturbing a G7 curve in a physically plausible way,
and the generator script is committed so the reader can see exactly what was
assumed.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m14-fig01-three-models` | Drop vs range for G1, G7, and the custom curve, same bullet | Agreement to 600 yd; divergence past it, and the divergence grows fastest in the transonic region. |
| 02 | `m14-fig02-residuals` | Residuals of each model against the "measured" curve, vs Mach | The residual is structured, not random — which is the signature of a *model* error rather than noise. |
| 03 | `m14-fig03-when-it-matters` | Model disagreement in inches vs range, with the reader's likely precision overlaid as a band | Below the range where model disagreement exceeds your group size, model choice is irrelevant. Above it, it dominates. |

**Exercises.** 6: fit a scale factor; interpret structured residuals; decide
whether a custom curve is justified for a stated use case; explain why a scale
factor cannot fix a shape mismatch.

**Tests.** `tests/test_m14_custom_drag.py` — scale-factor fit recovers a known
injected scale; a custom curve identical to G7 produces identical trajectories.

**Author pitfalls.**
- The synthetic data must be unmistakably labelled. Presenting generated data as
  radar measurements would violate the honesty rule and would also teach the
  reader to trust an unsourced curve.
- Figure 03 is the module's real contribution: model choice is a decision with a
  threshold, not an always-better.

---
## Part V — The 3DOF Solver

### M15 · Equations of Motion with Drag

`modules/15-equations-of-motion/` · prereq M14, M09, M05 · ~3.5 h

**Promise.** Everything built so far, assembled: a working ballistic solver.

**Objectives.** The reader can:
- Write the vector differential equation for a point mass under gravity and drag.
- Explain why it has no closed-form solution, and what that means practically.
- Implement the derivative function and integrate a complete trajectory.
- Extract a range table from a solution.
- Verify the solver reduces to the vacuum case when drag is removed.

**Mathematics.**

$$\dot{\vec{v}} = -\frac{\rho\, v\, C_D(M)\, A}{2m}\,\vec{v} + \vec{g}, \qquad \dot{\vec{r}} = \vec{v}$$

Note the form: writing the drag term with $\vec v$ rather than $v^2\hat v$ makes
the vector direction automatic and is less error-prone. Six-element state vector
$(x,y,z,v_x,v_y,v_z)$. Why $C_D(M)$ inside the integration makes the equation
non-autonomous in a way that forbids a closed form.

**Builds.** `src/ballistics/trajectory.py`

| Object | Purpose |
|---|---|
| `Projectile(mass_kg, diameter_m, drag_model, ...)` | frozen dataclass |
| `Conditions(pressure_pa, temp_k, rh, ...)` | frozen dataclass; computes and caches ρ and $a$ |
| `ShotState` | the six-element state, with named accessors |
| `derivatives(t, state, projectile, conditions)` | the right-hand side, fed to `integrate` from M05 |
| `solve_trajectory(projectile, conditions, v0_mps, angle_rad, ..., max_range_m)` | returns a `Trajectory` |
| `Trajectory` | dense solution with `at_range(range_m)`, `at_time(t)`, `to_dataframe()` |
| `range_table(trajectory, step_yd)` | the tabular output people actually read |

`Projectile` and `Conditions` are the course's primary data model from here on.
Design them once, here, carefully.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m15-fig01-drag-vs-vacuum` | The running load's real trajectory against its vacuum trajectory, same launch angle | The vacuum bullet flies four times as far. Drag is the dominant term, not a correction. |
| 02 | `m15-fig02-velocity-energy-tof` | Three panels: velocity, energy, and time of flight vs range | Time of flight is convex: the last 100 yards takes far longer than the first. This is why wind deflection grows faster than linearly. |
| 03 | `m15-fig03-cd-mach-along-path` | $C_D$ and Mach vs range on a twin plot, with the transonic band shaded | $C_D$ is nearly constant while supersonic, then climbs steeply. The solver is walking backwards up the curve from M12. |

**Exercises.** 7: write the derivative function from the equation; integrate and
compare to the published table; set drag to zero and recover M07 exactly; explain
the convexity of time of flight; compute the drag deceleration at the muzzle in g.

**Tests.** `tests/test_m15_trajectory.py` — **with $C_D=0$ the solver reproduces
M07's analytic solution to < 1 mm over 1000 m** (the limiting-case check);
speed decreases monotonically; energy decreases monotonically; the solution is
step-size converged at the default step.

**Author pitfalls.**
- Air density must be evaluated from `Conditions` and, if altitude varies along
  the path, updated — but for the ranges this course covers, constant density is
  a defensible simplification. Whichever is chosen, say so and quantify the error.
- The state vector layout and `Trajectory` API are used by every remaining
  module. Changing them later is expensive.
- Gravity is $(0,-g,0)$ in the course frame *only when the line of sight is
  horizontal*. Handle or explicitly defer the inclined case (M08 set it up).

---

### M16 · Solver Engineering: Zeroing, Events, Step Size, Output

`modules/16-solver-engineering/` · prereq M15 · ~3 h

**Promise.** Turning a trajectory integrator into a solver someone can actually
use: it finds its own launch angle, knows when it crossed the target, and tells
you why it chose the step size it did.

**Objectives.** The reader can:
- Solve for launch angle by root finding, and compare bisection, Newton, and Brent.
- Define events (apex, line-of-sight crossings, target range, transonic
  transition) and locate them accurately.
- Choose a step size from a stated accuracy budget and defend it with data.
- Design a range-card output and generate one.
- Explain when a 2D solve is sufficient and when the third dimension is required.

**Mathematics.** Root finding: bisection (robust, slow), Newton (fast, fragile),
Brent (both); bracketing and why the zeroing problem is well-bracketed;
convergence rates; the accuracy/cost tradeoff formalised.

**Builds.** `src/ballistics/solver.py`

| Function | Purpose |
|---|---|
| `zero_for_range(projectile, conditions, v0_mps, zero_range_m, sight_height_m)` | returns launch angle |
| `solve_for_target(...)` | full firing solution: elevation, windage, ToF, terminal velocity |
| `FiringSolution` | the result dataclass |
| `recommended_step(projectile, conditions, tolerance_m)` | derives $h$ from an error budget |

`src/ballistics/output.py`

| Function | Purpose |
|---|---|
| `range_card(solution, ranges_yd, units="mil")` | DataFrame |
| `format_range_card(...)` | the printable text form |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m16-fig01-root-finding` | Iterations to converge for bisection / Newton / Brent on the zeroing problem | Newton converges in 3 iterations and fails outside its basin; Brent is nearly as fast and never fails. That is why solvers use Brent. |
| 02 | `m16-fig02-step-size-pareto` | Drop error vs step size vs runtime, log-log, with the 1 cm budget line marked | There is a knee. Past it you are buying nothing. This figure justifies the default step size in the library. |
| 03 | `m16-fig03-events` | A trajectory with apex, near zero, far zero, transonic crossing, and target marked | Every one of these is a root of some scalar function of the state — that is what `Event` from M05 is for. |

**Exercises.** 7: zero the running load at 100 and 200 yd; find the step size for
a 1 cm budget and verify; add a custom event; produce a range card for a stated
scenario; explain when Newton fails here.

**Tests.** `tests/test_m16_solver.py` — the zeroing solution passes through zero
at the requested range to < 1 mm across a matrix of loads, ranges, and
conditions; event locations agree with dense-output refinement; `recommended_step`
actually meets its stated tolerance.

**Author pitfalls.**
- The zero must be defined relative to the *line of sight*, using M08's sight
  geometry, not relative to the bore. Getting this wrong shifts every subsequent
  number by the sight height.
- `recommended_step` must be validated, not asserted — the test is the point.

---

### M17 · Validation and Verification

`modules/17-validation/` · prereq M16 · ~3 h

**Promise.** How to know your solver is right. Not "looks reasonable" -- right,
with evidence, and a test suite that keeps it right.

**Objectives.** The reader can:
- State the difference between verification and validation and say which
  techniques address which.
- Run a grid-convergence study and confirm the observed order of accuracy.
- Design limiting-case tests that would catch a real bug.
- Compare solver output against published trajectory data and interpret the residuals.
- Build a regression suite with golden files, and explain why tolerances must be
  chosen deliberately.

**Mathematics.** Observed order of accuracy from three grid resolutions;
Richardson extrapolation; residual statistics; tolerance selection as a
statement about acceptable physical error, not about floating point.

**Builds.** `src/ballistics/validation.py`

| Function | Purpose |
|---|---|
| `grid_convergence(solve_fn, steps)` | observed order + Richardson estimate |
| `limiting_case_report(...)` | runs the standard degenerate checks |
| `compare_to_reference(trajectory, reference_df)` | residual statistics |
| `write_golden(name, df)`, `check_golden(name, df, tol)` | regression fixtures in `tests/fixtures/` |

**Deliverable, specific to this module.** Regenerate
`modules/00-orientation/data/effect_magnitudes.csv` using the reader's own
solver and diff it against the reference file M00 shipped. The lesson shows
the diff. This closes the loop opened in Module 00 and is the emotional payoff
of Part V -- the reader built the thing that produced the numbers they were
handed on day one.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m17-fig01-grid-convergence` | Solution error vs step size with the fitted observed order annotated | The observed order matches RK4's theoretical 4. If it did not, there is a bug — this is a *test*, drawn. |
| 02 | `m17-fig02-reference-residuals` | Residuals against published trajectory data vs range, with the tolerance band | Residuals should be small and unstructured. Structure means a model difference, and the caption must say what would be suspected. |
| 03 | `m17-fig03-loop-closed` | M00's shipped effect magnitudes vs the reader's own computed values | Same numbers, from your own code. Any disagreement is a finding, not an embarrassment — and the lesson must handle both outcomes honestly. |

**Exercises.** 6: run a convergence study; write a limiting-case test that
catches a bug the author deliberately describes; choose a tolerance and justify
it physically; interpret a structured residual.

**Tests.** `tests/test_m17_validation.py` plus the golden-file regression suite
in `tests/fixtures/`. From this module on, **every subsequent module adds a
golden-file case** so that later effects cannot silently change earlier answers.

**Author pitfalls.**
- If the regenerated M00 data does *not* match, do not quietly fix M00. Report
  the discrepancy in the lesson and explain it. That is the honest outcome and
  it is more instructive than agreement.
- Published reference tables carry their own assumptions (standard, BC source,
  sight height). Match them explicitly before comparing, and say what was
  matched.

---

## Part VI — Wind

### M18 · Crosswind Deflection and Lag Time

`modules/18-wind-basics/` · prereq M17 · ~3 h

**Promise.** The most important derivation in practical long-range shooting: why
a crosswind pushes a bullet sideways by *less* than wind speed times time of
flight, and by exactly how much less.

**Objectives.** The reader can:
- Explain that deflection is caused by the bullet's *lag* behind its vacuum
  time of flight, not by the wind "pushing it" for the whole flight.
- Derive the lag-time formula $D_z = W_z\,(T - x/v_0)$.
- Implement wind in the solver through air-relative velocity.
- Compare the lag approximation to the numerical solution and bound its error.
- Quantify the (small) effect of head and tail winds on drop.

**Mathematics.** Air-relative velocity $\vec v_{\text{air}} = \vec v - \vec W$;
the lag-time derivation; why the naive $W \times T$ estimate overpredicts by
roughly a factor of ten; first-order error of the approximation.

**Physics.** The bullet does not get blown sideways; it *turns into the wind*
(weathercocking) and its lateral velocity asymptotically approaches the wind's.
Deflection accumulates only in proportion to how far behind a vacuum bullet it
has fallen. This is genuinely counterintuitive and deserves the module's full
attention.

**Builds.** `src/ballistics/effects/wind.py` (part 1)

| Function | Purpose |
|---|---|
| `apply_wind(velocity_mps, wind_mps)` | the air-relative velocity used inside `derivatives` |
| `lag_time_deflection_m(wind_z_mps, tof_s, range_m, v0_mps)` | the closed-form approximation |
| `crosswind_component_mps(...)` | re-exported from `frames` for convenience |

`trajectory.derivatives` is extended to take a wind vector. This is a change to
an M15 API, so it follows the migration rule: the lesson documents it and the
M15 tests are updated in the same session.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m18-fig01-lag-vs-numerical` | Deflection vs range: numerical solution, lag-time formula, and the naive $W\times T$ estimate | The naive estimate is wrong by ~10×. The lag formula is within a few percent of the numerical answer out to 1000 yd. |
| 02 | `m18-fig02-deflection-vs-wind` | Deflection vs range for 5/10/15/20 mph full-value winds | Deflection is linear in wind speed but superlinear in range — because lag grows faster than time. |
| 03 | `m18-fig03-head-tail-wind` | Drop change from a 10 mph head vs tail wind, vs range | It is under an inch at 1000 yd. Head/tail wind is almost always ignorable, and now you know why rather than being told. |

**Exercises.** 7: derive the lag formula; compute deflection for a stated wind;
compare all three estimates at 1000 yd; explain weathercocking; show why
head/tail wind barely matters.

**Tests.** `tests/test_m18_wind.py` — zero wind reproduces M15's trajectory
exactly; the lag formula agrees with the numerical solution within a stated
percentage out to 1000 yd; deflection is linear in wind speed; a golden-file
regression case.

**Author pitfalls.**
- Get the sign convention right, from `frames.wind_vector` (M03). A 3 o'clock
  wind pushes the bullet left, so $W_z<0$ and $D_z<0$.
- The "bullet turns into the wind" explanation is the physical heart of the
  module. Do not skip to the formula.

---

### M19 · Real Wind Fields, Segmentation, and Sensitivity

`modules/19-wind-fields/` · prereq M18 · ~3 h

**Promise.** Wind is never one number. This module handles wind that changes
along the flight path, and answers the perennial argument about which wind
matters most.

**Objectives.** The reader can:
- Model wind that varies with downrange position.
- Derive and interpret the downrange wind-weighting function.
- Explain, with the weighting curve, why wind near the shooter matters more --
  and quantify how much more.
- Estimate wind from mirage, vegetation, and terrain, with honest error bars.
- Run a sensitivity analysis and rank wind against every other error source.

**Mathematics.** Superposition of per-segment deflection contributions; the
weighting function derived by differentiating the lag-time result with respect
to the wind at position $x$; sensitivity $\partial D_z/\partial W_z$.

**Builds.** `src/ballistics/effects/wind.py` (part 2)

| Object | Purpose |
|---|---|
| `SegmentedWind(boundaries_m, winds_mps)` | piecewise-constant wind field, callable by position |
| `wind_weighting_curve(trajectory)` | deflection sensitivity per unit downrange distance |
| `effective_wind_mps(trajectory, wind_field)` | the single uniform wind giving the same deflection |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m19-fig01-weighting-curve` | Contribution to total deflection per unit downrange distance, normalised | The first third of the flight path contributes disproportionately — but not as overwhelmingly as range folklore claims. The curve gives the actual number. |
| 02 | `m19-fig02-segmented-vs-uniform` | Deflection under a realistic segmented wind vs the uniform average of the same field | Averaging the wind is not the same as averaging the deflection, and the difference is a real miss. |
| 03 | `m19-fig03-error-budget-preview` | Deflection error from a ±2 mph wind-call error against errors from BC, MV, and range uncertainty, at 1000 yd | Wind dominates everything else combined. This figure sets up Part IX and should be referenced from M26. |

**Exercises.** 6: compute deflection under a segmented field; derive the
weighting curve; find the effective uniform wind; estimate the miss from a 2 mph
call error at three ranges.

**Tests.** `tests/test_m19_wind_fields.py` — a uniform `SegmentedWind` matches
M18's uniform result exactly; the weighting curve integrates to the total
deflection; `effective_wind_mps` round-trips.

**Author pitfalls.**
- "Muzzle wind matters most" is widely repeated and roughly true, but the
  commonly quoted weightings are folklore. Derive the curve and report what it
  actually says, including where it disagrees with the folklore.
- Mirage and vegetation estimation is craft, not physics. Present it as craft,
  with error bars, and do not dress it up.

---
## Part VII — Spin and Rotational Effects

> **Scope note for this whole part.** A point-mass model has no orientation, so
> it cannot produce spin drift or aerodynamic jump from first principles. The
> effects are real and are derived rigorously in 4DOF and 6DOF treatments. What
> this course does is import validated *models* of them, apply them correctly,
> and be explicit about what has been assumed. Every module in Part VII states
> this in its own words and links to `docs/appendix-further-study.md`.

### M20 · Spin, Rifling, and Gyroscopic Stability

`modules/20-stability/` · prereq M17 · ~3 h

**Promise.** Why rifling exists, what "1:8 twist" buys you, and how to tell
whether your bullet is stable before you shoot it.

**Objectives.** The reader can:
- Compute spin rate from twist rate and muzzle velocity.
- Explain gyroscopic stabilisation physically: the overturning aerodynamic
  moment versus the bullet's angular momentum.
- Compute the Miller stability factor and apply its velocity and atmospheric
  corrections.
- Interpret $S_g$ thresholds and explain what marginal stability costs.
- Explain spin decay and why $S_g$ *increases* along the trajectory.
- Explain the drag penalty of a marginally stabilised bullet.

**Mathematics.** $p = 2\pi v / n$; angular momentum $I_x p$; the overturning
moment; the Miller twist rule and its corrections for velocity and air density;
exponential spin decay.

**Physics.** The centre of pressure of a supersonic spitzer lies ahead of the
centre of gravity, so the aerodynamic moment is destabilising; spin converts
that overturning tendency into precession. Why longer bullets are harder to
stabilise (transverse moment of inertia grows faster than axial). Why $S_g$
rises downrange: spin decays slowly while velocity decays fast.

**Builds.** `src/ballistics/effects/stability.py`

| Function | Purpose |
|---|---|
| `spin_rate_radps(velocity_mps, twist_m)` | |
| `miller_sg(mass_gr, diameter_in, length_in, twist_in, velocity_fps, ...)` | the Miller rule, cited, in its native imperial units with an SI wrapper |
| `sg_corrected(sg, velocity_fps, pressure_pa, temp_k)` | velocity and atmospheric corrections |
| `spin_decay_radps(p0, range_m, ...)` | |
| `sg_along_trajectory(trajectory, ...)` | |

Miller's rule is empirical and dimensional; it is one of the few places the
library works in imperial internally. The docstring must say so and explain why.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m20-fig01-sg-vs-twist` | $S_g$ vs twist rate for a family of bullet lengths, with the 1.0 and 1.4 thresholds marked | Longer bullets need faster twist, steeply. The 1.4 threshold, not 1.0, is the practical target. |
| 02 | `m20-fig02-sg-vs-conditions` | $S_g$ vs density altitude and temperature | Cold dense air at sea level is the worst case. A load stable in Denver in July can be marginal in Michigan in January — this figure is the reason people get bitten. |
| 03 | `m20-fig03-sg-downrange` | $S_g$ vs range along the trajectory | $S_g$ *rises* downrange. Stability problems are a muzzle problem, not a distance problem. |

**Exercises.** 7: compute spin rate and $S_g$ for the running load; find the
minimum twist for a given bullet; evaluate the same load at two altitudes and
seasons; explain why $S_g$ rises downrange.

**Tests.** `tests/test_m20_stability.py` — Miller $S_g$ against published worked
examples; spin rate against hand calculation; monotonicity in twist and in length.

**Author pitfalls.**
- Miller's rule assumes a conventional lead-core jacketed bullet. For monolithic
  copper or heavily boat-tailed VLD forms it under-predicts required twist. Say so.
- $S_g > 1$ is the bare stability condition; $S_g \geq 1.4$ is the practical
  target because of the BC penalty and yaw-induced dispersion below it. Both
  numbers, with the reason for the gap.

---

### M21 · Spin Drift and the Yaw of Repose

`modules/21-spin-drift/` · prereq M20 · ~2.5 h

**Promise.** Why a right-hand-twist bullet drifts right, by an amount that grows
faster than linearly, and how much of that number you should trust.

**Objectives.** The reader can:
- Explain precession and the yaw of repose qualitatively.
- Explain why drift is always in the direction of twist, and why it is *not* a
  Magnus effect in the way it is usually described.
- Estimate spin drift with the standard published models.
- Add spin drift to a firing solution and state its magnitude versus range.
- State clearly what a point-mass model cannot tell them here.

**Mathematics.** The yaw of repose as the small equilibrium yaw angle at which
the gyroscopic precession rate matches the rate at which the velocity vector
turns under gravity; the resulting lateral force; Litz's empirical fit as a
function of $S_g$ and time of flight, and McCoy's more physical expression --
both presented, with their differences discussed.

**Physics.** As gravity turns the velocity vector downward, the gyroscopically
stabilised bullet's nose lags behind, settling at a small yaw angle to the
*right* for right-hand twist. That yaw produces a small lift force to the right.
Drift is the accumulated result. The common "Magnus effect" explanation is at
best incomplete and the module should say so.

**Builds.** `src/ballistics/effects/spin_drift.py`

| Function | Purpose |
|---|---|
| `spin_drift_m(sg, tof_s, right_hand=True)` | Litz's model, cited, with validity range in the docstring |
| `yaw_of_repose_rad(...)` | the more physical expression, for comparison |
| `apply_spin_drift(solution, ...)` | applied as a documented post-integration correction |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m21-fig01-drift-vs-range` | Spin drift vs range for both running loads, both models overlaid | Roughly 9 inches at 1000 yd for the 6.5 CM. Growth is faster than linear because it goes as $t^{1.83}$. The two models disagree by enough to see, which is the honest message. |
| 02 | `m21-fig02-drift-vs-sg` | Drift vs $S_g$ at fixed range | Faster twist means more drift. Over-stabilising has a cost. |
| 03 | `m21-fig03-lateral-effects` | Spin drift, Coriolis (forward reference), and a 1 mph wind error, on one chart vs range | A 1 mph wind-call error swamps spin drift until well past 800 yd. Perspective before precision. |

**Exercises.** 6: compute spin drift at four ranges; compare the two models and
account for the difference; determine the range past which spin drift exceeds a
1 mph wind error; explain the direction from the twist.

**Tests.** `tests/test_m21_spin_drift.py` — direction follows twist hand; drift
grows faster than linearly in time of flight; magnitude matches published values
for a known load within a stated tolerance.

**Author pitfalls.**
- **Honesty rule applies at full strength.** This is a correction from outside
  the model. Name the source, state the validity range, and state the
  disagreement between models rather than picking one silently.
- Do not repeat the "Magnus effect" folk explanation without correcting it.
- Litz's formula is dimensional and empirical (it takes $S_g$ and time of flight
  and returns inches). Wrap it carefully and label the units.

---

### M22 · Aerodynamic Jump and Crosswind Jump

`modules/22-aerodynamic-jump/` · prereq M21 · ~2.5 h

**Promise.** A crosswind moves your impact *vertically*. This surprises people,
it is measurable at long range, and it is a common misdiagnosis of "vertical
stringing".

**Objectives.** The reader can:
- Explain why a crosswind produces a vertical deflection.
- Get the sign right: which way, for which twist, for which wind direction.
- Estimate the magnitude with the standard model.
- Distinguish aerodynamic jump (an angular offset established at the muzzle)
  from wind deflection (accumulated along the path).
- Add it to a firing solution.

**Mathematics.** The angular impulse imparted during the initial yaw transient;
jump as a fixed *angle*, which is why the linear displacement grows linearly with
range while wind deflection grows faster; the standard estimate in terms of
$S_g$, bullet length, and crosswind component.

**Physics.** A crosswind gives the bullet an initial angle of attack. A spinning
bullet responds to a yawing disturbance with a *pitching* motion 90° out of
phase. The result is a small vertical velocity established almost immediately at
the muzzle, and therefore an angular offset that persists for the whole flight.

**Builds.** `src/ballistics/effects/aero_jump.py`

| Function | Purpose |
|---|---|
| `aerodynamic_jump_rad(sg, length_cal, crosswind_mps, ...)` | the standard model, cited |
| `apply_aero_jump(solution, ...)` | applies the angular offset at launch |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m22-fig01-jump-vs-crosswind` | Vertical impact shift vs crosswind speed, at 1000 yd, both twist directions | A 10 mph left-to-right wind lifts impact for a right-hand twist. Several inches at 1000 yd — smaller than wind deflection but not nothing. |
| 02 | `m22-fig02-jump-vs-deflection-scaling` | Jump and wind deflection vs range on the same axes, normalised | Jump grows *linearly* (a fixed angle); deflection grows faster. Their ratio changes with range, and the crossover is worth knowing. |
| 03 | `m22-fig03-combined-wind-effect` | The total impact shift vector from a pure crosswind: horizontal deflection plus vertical jump | The impact does not move horizontally. It moves diagonally. |

**Exercises.** 6: compute jump for a stated wind; get the sign right for a
left-hand twist; separate jump from deflection in a described group; explain why
jump is an angle and deflection is not.

**Tests.** `tests/test_m22_aero_jump.py` — sign flips with twist hand and with
wind direction; magnitude linear in crosswind; displacement linear in range.

**Author pitfalls.**
- Sign conventions here are the most error-prone in the course. Derive them from
  the M03 frame, write the test first, and state the result in plain English
  ("for a right-hand twist, a wind from the left raises impact") as a check.
- This is a model import, not a derivation. Honesty rule.

---

## Part VIII — Earth Effects

### M23 · Coriolis and the Eötvös Effect

`modules/23-coriolis/` · prereq M22 · ~2.5 h

**Promise.** The Earth rotates under the bullet. Here is exactly how much that
matters, where, and in which direction -- and where it is a distraction.

**Objectives.** The reader can:
- Explain what a rotating reference frame is and why fictitious forces appear.
- State the Coriolis acceleration and apply it to a projectile.
- Compute horizontal Coriolis drift as a function of latitude.
- Compute the vertical (Eötvös) effect as a function of firing azimuth.
- Add both to the solver and state the range at which each becomes worth dialling.

**Mathematics.** $\vec a_C = -2\vec\Omega\times\vec v$ in the rotating frame;
decomposing $\vec\Omega$ into local vertical and horizontal components at
latitude $\varphi$; the horizontal term depending on $\sin\varphi$ and the
vertical (Eötvös) term on $\cos\varphi\sin\psi$.

**Physics.** Why the horizontal deflection is to the right in the northern
hemisphere regardless of firing direction, while the vertical effect reverses
between easterly and westerly fire. Why Coriolis is a *frame* effect and no
force acts on the bullet.

**Builds.** `src/ballistics/effects/coriolis.py`

| Function | Purpose |
|---|---|
| `omega_vector_radps(latitude_rad, azimuth_rad)` | Earth's rotation in the course frame |
| `coriolis_acceleration_mps2(velocity_mps, latitude_rad, azimuth_rad)` | |
| `horizontal_drift_estimate_m(...)`, `eotvos_estimate_m(...)` | closed-form approximations for comparison |

Wired into `trajectory.derivatives` as a true acceleration term (unlike spin
drift, this one *is* derivable within the point-mass model, and the module
should point out the contrast with Part VII).

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m23-fig01-horizontal-vs-latitude` | Horizontal drift at 1000 yd vs latitude, both hemispheres | Zero at the equator, maximum at the poles, and it flips sign across the equator. Direction does not depend on which way you face. |
| 02 | `m23-fig02-eotvos-compass` | Polar plot of the vertical effect vs firing azimuth at a fixed latitude | Firing east lifts impact, west lowers it, north and south do neither. This one *does* depend on facing. |
| 03 | `m23-fig03-effect-ranking` | Coriolis (both components) against spin drift, wind, and a 0.5 mph wind-call error, vs range | Coriolis is below the noise floor until roughly 1000 yd, and even then a half-mph wind error is comparable. Dial it, but know its rank. |

**Exercises.** 6: compute both components for the reader's latitude; find the
range at which horizontal Coriolis exceeds one inch; explain the azimuth
dependence of one component and not the other; compare to a small wind error.

**Tests.** `tests/test_m23_coriolis.py` — zero horizontal drift at the equator;
sign flips across the equator; Eötvös zero for due-north fire, maximal for due
east; magnitudes match published values for a standard case.

**Author pitfalls.**
- Two separate effects with different symmetries. Do not merge them.
- Northern-hemisphere right-drift is independent of azimuth; the vertical effect
  is not. This asymmetry is the most commonly garbled part of the topic.
- Keep the perspective figure (03). Coriolis attracts more attention than its
  magnitude deserves, and the course should be honest about that while still
  modelling it correctly.

---
## Part IX — Measurement, Error, and Statistics

### M24 · Instrumentation and Measurement Error

`modules/24-instrumentation/` · prereq M17, M01 · ~3 h

**Promise.** Your solver's output is only as good as its inputs, and every input
comes from an instrument with its own error. This module characterises each one.

**Objectives.** The reader can:
- Describe how optical, magnetic, and Doppler chronographs work, and the error
  characteristics of each.
- Distinguish bias from noise, and explain why they need different fixes.
- Verify scope tracking with a tall-target test and compute the scale correction.
- Quantify the impact of rifle cant on impact position.
- State the trajectory consequence of a rangefinder error at a given range.
- Build a table of every input, its realistic uncertainty, and its consequence.

**Mathematics.** Bias vs random error; the tall-target scale factor
$k = \text{measured}/\text{commanded}$; cant error geometry
$\Delta z = \text{drop}\times\sin(\text{cant})$ with the accompanying vertical
term; propagating a range error into an elevation error through the local slope
of the drop curve.

**Builds.** `src/ballistics/instruments.py`

| Function | Purpose |
|---|---|
| `tall_target_scale(commanded_moa, measured_in, distance_yd)` | |
| `apply_tracking_correction(dial_rad, scale)` | |
| `cant_error_m(drop_m, cant_rad)` | horizontal and vertical components |
| `range_error_to_vertical_m(trajectory, range_m, range_error_m)` | |
| `mv_error_to_vertical_m(...)`, `bc_error_to_vertical_m(...)` | |
| `INSTRUMENT_UNCERTAINTY` | dict of realistic $1\sigma$ values, each with a cited or clearly-estimated basis |

`INSTRUMENT_UNCERTAINTY` is the input to M26's uncertainty budget, so its values
must be defensible and individually sourced or explicitly marked as estimates.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m24-fig01-cant-error` | Heatmap of horizontal impact error vs cant angle × range | 5° of cant — which is invisible without a level — costs several inches at 1000 yd. Cant error scales with *drop*, so it explodes at long range. |
| 02 | `m24-fig02-tracking-error` | Impact error from a 1% scope tracking error vs range | A 1% tracking error is within manufacturing tolerance and is worth most of a foot at 1000 yd. This is why you tall-target test. |
| 03 | `m24-fig03-input-error-ranking` | Vertical error at 1000 yd from realistic $1\sigma$ errors in MV, BC, range, pressure, temperature, cant | Ranks the inputs. Sets up M26, which does this properly with propagation. |

**Exercises.** 7: compute a tall-target scale correction from given data; find
the cant angle costing one MOA at 800 yd; convert a rangefinder error to an
elevation error; rank the reader's own equipment's contributions.

**Tests.** `tests/test_m24_instruments.py` — cant error zero at zero cant and
correct at 90°; tall-target scale round-trips; range-error propagation agrees
with a finite-difference of the solver.

**Author pitfalls.**
- Every uncertainty value in `INSTRUMENT_UNCERTAINTY` needs a stated basis.
  Unsourced numbers here would silently corrupt M26 and M27.
- Cant error has both a horizontal and a vertical component; the horizontal one
  is larger and is usually the only one discussed. Include both.

---

### M25 · The Statistics of Precision

`modules/25-precision-statistics/` · prereq M24 · ~3.5 h

**Promise.** How to measure your rifle's precision without fooling yourself --
and why almost every group size you have ever been told is nearly meaningless.

**Objectives.** The reader can:
- Define group size, extreme spread, mean radius, CEP, and R95, and say which
  estimator is efficient.
- Explain why extreme spread is a poor estimator and quantify how poor.
- Fit the Rayleigh model to a group and extract $\sigma_r$.
- Compute a confidence interval for dispersion from $n$ shots.
- Explain why a three-shot group tells you almost nothing, with a number.
- Combine independent dispersion sources in quadrature.

**Mathematics.** The bivariate normal impact model; the Rayleigh distribution as
its radial marginal; mean radius and CEP in terms of $\sigma_r$; the expected
extreme spread as an order statistic, growing with $n$; $\chi^2$ confidence
intervals for a variance estimate; root-sum-square combination of independent
dispersions.

**Builds.** `src/ballistics/stats/dispersion.py`

| Function | Purpose |
|---|---|
| `mean_radius_m(impacts)` | |
| `extreme_spread_m(impacts)` | |
| `rayleigh_sigma_from_impacts(impacts)` | maximum-likelihood fit |
| `cep_m(sigma_r)`, `r95_m(sigma_r)` | |
| `expected_extreme_spread(sigma_r, n)` | by simulation, cached |
| `dispersion_ci(impacts, confidence)` | |
| `combine_in_quadrature(*sigmas)` | |

**Data.** Seeded synthetic groups in `modules/25-precision-statistics/data/`,
generated by a committed script, clearly labelled.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m25-fig01-extreme-spread-vs-n` | Expected extreme spread vs shot count for a fixed true dispersion, with the spread of outcomes as a band | ES *grows* with sample size — a 10-shot group from the same rifle is bigger than a 5-shot group, by construction. Comparing groups of different sizes is meaningless. |
| 02 | `m25-fig02-three-shot-lottery` | Simulated 3-shot groups from one rifle, small multiples, all drawn from identical statistics | These look like different rifles. They are the same rifle. This is the module's most important figure. |
| 03 | `m25-fig03-confidence-vs-n` | Width of the 90% confidence interval on dispersion vs number of shots | You need ~20 shots for a ±20% answer. Nobody wants to hear it; the curve does not care. |
| 04 | `m25-fig04-estimator-efficiency` | Estimator variance for ES vs mean radius vs Rayleigh MLE, at equal $n$ | Mean radius uses every shot; extreme spread uses two and throws the rest away. |

**Exercises.** 7: compute all estimators for a given group; simulate 3-shot
groups and observe the spread of outcomes; find the shot count for a stated
confidence; combine ammunition and rifle dispersion in quadrature; critique a
magazine accuracy claim.

**Tests.** `tests/test_m25_dispersion.py` — CEP ≈ $1.1774\sigma_r$; mean radius
≈ $1.2533\sigma_r$; the Rayleigh fit recovers an injected $\sigma_r$ from a large
sample; quadrature combination is correct; **all randomness seeded**.

**Author pitfalls.**
- Every simulation in this module must be seeded, and the seed stated in the
  caption. `tools/build_figures.py` must produce byte-identical output.
- Figure 02 is the one readers will remember. Make it good: enough panels to be
  convincing, identical statistics, and a caption that says so plainly.
- Be careful with "MOA" claims: a group measured in inches at 100 yd converted
  to MOA is an angular *estimate* with the same terrible confidence interval as
  the underlying group.

---

### M26 · Error Propagation and the Uncertainty Budget

`modules/26-uncertainty/` · prereq M25 · ~3.5 h

**Promise.** A firing solution without an uncertainty is half an answer. This
module puts error bars on your drop and windage, and tells you which input to
fix first.

**Objectives.** The reader can:
- Propagate input uncertainty through the solver analytically to first order.
- Do the same by Monte Carlo, and say when each method is appropriate.
- Build a complete uncertainty budget for a firing solution.
- Identify the dominant error source at 300, 600, 1000, and 1500 yards.
- Produce a prediction interval on drop and windage and interpret it correctly.

**Mathematics.** GUM-style first-order propagation
$u_y^2 = \sum (\partial y/\partial x_i)^2 u_{x_i}^2$; finite-difference
sensitivities through the solver; Monte Carlo sampling; variance decomposition
and the difference between a sensitivity and a contribution; why first-order
propagation fails where the solver is nonlinear (the transonic region).

**Builds.** `src/ballistics/stats/uncertainty.py`

| Function | Purpose |
|---|---|
| `sensitivity_matrix(solve_fn, nominal_inputs, ranges_m)` | $\partial(\text{drop},\text{drift})/\partial x_i$ by central difference |
| `propagate_first_order(sensitivities, uncertainties)` | |
| `monte_carlo_trajectory(inputs, distributions, n, seed)` | |
| `uncertainty_budget(...)` | the table: source, $1\sigma$, sensitivity, contribution, % of variance |
| `prediction_interval(...)` | |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m26-fig01-budget-tornado` | Tornado chart of variance contributions, small-multipled by range (300/600/1000/1500 yd) | The ranking *changes with range*. At 300 yd it is the rifle; at 1000 yd it is the wind call; at 1500 yd the BC and transonic modelling take over. |
| 02 | `m26-fig02-monte-carlo-impacts` | Monte Carlo impact scatter at 1000 yd with 50% and 95% confidence ellipses, seed stated | The uncertainty is not circular — it is a wide, short ellipse, because wind error dominates horizontally. |
| 03 | `m26-fig03-prediction-band` | Drop curve with a 95% prediction band that widens with range | The band is the honest output of a solver. A single number is a point estimate pretending to be a fact. |
| 04 | `m26-fig04-linear-vs-mc` | First-order propagation vs Monte Carlo, vs range | They agree until the transonic region, where the solver's nonlinearity breaks the linear method. Knowing where your approximation fails is the skill. |

**Exercises.** 7: compute sensitivities by finite difference; build a budget for
the reader's own equipment; find the input worth fixing first at 1000 yd; run a
Monte Carlo and interpret the ellipse; find where linear propagation breaks.

**Tests.** `tests/test_m26_uncertainty.py` — first-order propagation agrees with
Monte Carlo in a regime known to be linear; sensitivities agree with analytic
values where available; **Monte Carlo is seeded and reproducible**; variance
contributions sum to the total.

**Author pitfalls.**
- Correlations between inputs are real (temperature and density; MV and
  temperature). First-order propagation as written assumes independence. Say so,
  and either handle the main correlation or explicitly bound the error from
  ignoring it.
- Seed everything.

---

### M27 · Hit Probability

`modules/27-hit-probability/` · prereq M26 · ~3 h

**Promise.** The question every other module has been building toward: what is
the probability that this shot hits, and what should you improve to raise it?

**Objectives.** The reader can:
- Combine rifle dispersion and firing-solution uncertainty into a single impact
  distribution.
- Compute hit probability for a target of given size at a given range.
- Distinguish precision from bias and explain why they need different remedies.
- Compute first-round hit probability and explain why it differs from steady-state.
- Rank possible equipment or skill improvements by their marginal effect on
  hit probability.

**Mathematics.** Combining independent bivariate normals; integrating a
bivariate normal over a rectangular or circular target region (closed form where
available, Monte Carlo otherwise); marginal analysis $\partial P_{\text{hit}}/\partial\sigma_i$.

**Builds.** `src/ballistics/stats/hit_probability.py`

| Function | Purpose |
|---|---|
| `CircularTarget(radius_m)`, `RectangularTarget(w, h)` | |
| `p_hit(target, sigma_x_m, sigma_y_m, bias_x_m=0, bias_y_m=0)` | |
| `p_hit_vs_range(...)` | |
| `first_round_hit_probability(...)` | includes solution uncertainty; subsequent shots do not |
| `improvement_value(baseline, improvements)` | Δ$P_{\text{hit}}$ per candidate improvement |

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m27-fig01-phit-vs-range` | $P_{\text{hit}}$ vs range for three target sizes | The falloff is steep and its location depends far more on the wind call than on the rifle. |
| 02 | `m27-fig02-improvement-heatmap` | $P_{\text{hit}}$ at 1000 yd over wind-call error × muzzle-velocity SD | The gradient is almost entirely in the wind-call direction. Buying better ammunition to fix a wind problem does not work. |
| 03 | `m27-fig03-marginal-value` | Δ$P_{\text{hit}}$ from each candidate improvement, ranked, at three ranges | The best investment changes with range. An honest answer to "what should I upgrade?" |
| 04 | `m27-fig04-precision-vs-bias` | Two impact distributions with equal $P_{\text{hit}}$, one wide and centred, one tight and offset | Same hit rate, completely different fixes. Diagnosis precedes treatment. |

**Exercises.** 7: compute $P_{\text{hit}}$ for a stated scenario; find the
maximum range for 90% hit probability; rank three upgrades by marginal value;
diagnose a described group as a precision or a bias problem; explain why
first-round probability is lower.

**Tests.** `tests/test_m27_hit_probability.py` — $P_{\text{hit}} \to 1$ as the
target grows and $\to 0$ as it shrinks; a circular target with $\sigma_x=\sigma_y$
matches the Rayleigh CDF exactly; bias reduces $P_{\text{hit}}$ monotonically;
Monte Carlo agrees with the closed form.

**Author pitfalls.**
- First-round hit probability must include *solution* uncertainty; follow-up
  shots after a spotted correction do not. Conflating them overstates
  first-round performance, which is the number that matters.
- The improvement ranking depends on the reader's baseline. Make the baseline
  explicit and easy to change.

---

## Part X — Field Application

### M28 · DOPE, Truing, and Solver Calibration

`modules/28-truing/` · prereq M27 · ~3.5 h

**Promise.** Bringing the model and the rifle into agreement, using real data,
without fooling yourself into a confidently wrong answer.

**Objectives.** The reader can:
- Collect and structure DOPE so it is actually usable.
- Decide whether to true muzzle velocity, ballistic coefficient, or both.
- Fit the correction by least squares and interpret the residuals.
- Explain why MV and BC are hard to separate from short-range data.
- Explain why truing on transonic data produces a confidently wrong model.
- Validate a trued solution on held-out data.

**Mathematics.** Least-squares fitting of one or two parameters; parameter
identifiability and the degenerate valley in the MV-BC likelihood surface;
train/test splitting; residual structure as a diagnostic.

**Physics.** MV errors dominate at short range (they shift the whole curve); BC
errors dominate at long range (they change its shape). That separation is what
makes joint truing possible at all, and it is why the *range spread* of your
DOPE matters more than the number of data points.

**Builds.** `src/ballistics/truing.py`

| Function | Purpose |
|---|---|
| `DopeRecord`, `load_dope(path)` | the data model and loader |
| `true_muzzle_velocity(dope, projectile, conditions)` | |
| `true_bc(dope, ...)` | |
| `joint_true(dope, ...)` | returns fitted MV and BC with a covariance |
| `residual_report(dope, solution)` | residuals plus a structure diagnostic |
| `holdout_validate(dope, ...)` | |

**Data.** `data/dope/` gets three **clearly labelled synthetic** sets: clean,
realistically noisy, and transonic-contaminated. The generator is committed. The
lesson states plainly that these are synthetic and explains what was assumed, so
the reader knows exactly what the fit is being asked to recover.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m28-fig01-residuals-before-after` | Drop residuals vs range, before and after truing | Before: structured, growing with range. After: unstructured and small. Structure in a residual is the signature of a model error. |
| 02 | `m28-fig02-mv-bc-identifiability` | Contours of fit error over the MV × BC plane, for short-range-only data and for well-spread data | Short-range data gives a long degenerate valley — many (MV, BC) pairs fit equally well. Well-spread data closes it. **This is the module's central insight.** |
| 03 | `m28-fig03-transonic-trap` | Truing on data that includes transonic points, and the resulting error extrapolated back to supersonic ranges | The fit looks excellent on the training data and is wrong everywhere else. A confidently wrong model is worse than an uncalibrated one. |
| 04 | `m28-fig04-holdout` | Predicted vs observed on held-out ranges, before and after | The only honest test of a fit is data it has not seen. |

**Exercises.** 7: true MV from short-range DOPE; attempt joint truing on
short-range data and observe the degeneracy; true on the transonic-contaminated
set and diagnose the failure; validate on holdout; design a DOPE collection plan
for the reader's own rifle.

**Tests.** `tests/test_m28_truing.py` — truing recovers a known injected MV and
BC offset from clean synthetic data; the covariance from short-range-only data
shows the expected strong correlation; holdout validation catches an
over-fitted transonic case.

**Author pitfalls.**
- The synthetic data must be generated by a committed script and labelled
  synthetic in the file header, the lesson, and `data/README.md`.
- Do not present truing as a way to fix bad inputs. Truing a wrong atmosphere
  into the BC produces a model that works exactly once, on that day, at that
  altitude. Say so.

---

### M29 · Capstone: A Complete, Validated Ballistic Solution

`modules/29-capstone/` · prereq: all · ~4 h

**Promise.** Everything, assembled, validated, and documented -- a solver you
understand completely, with honest error bars and a stated set of limitations.

**Objectives.** The reader can:
- Produce a complete firing solution including every effect in the course.
- Validate it end to end against reference data and their own DOPE.
- Generate a range card with uncertainty bands.
- Explain and justify every number the solver produces.
- State the model's limitations and what a higher-fidelity model would add.

**Builds.** `src/ballistics/api.py`

| Function | Purpose |
|---|---|
| `solve(load, conditions, wind, geometry, ranges)` | the one high-level entry point |
| `Solution` | complete result including uncertainty |

`src/ballistics/__main__.py` — a CLI: `uv run ballistics --help`, taking a load
and conditions and printing a range card.

**Deliverables beyond the usual.**
- `modules/29-capstone/report.md` — a short technical report on the running
  load: the full solution, every effect's contribution, the uncertainty budget,
  the validation evidence, and the stated limitations.
- A range card as both CSV and PNG.
- The complete test suite green.
- `tools/build_figures.py` regenerating every figure in the repository from a
  clean checkout.

**Figures.**

| # | Slug | Shows | What to notice |
|---|---|---|---|
| 01 | `m29-fig01-effect-decomposition` | Stacked contribution of every effect to total elevation and windage vs range | The answer to Module 00's opening question, now computed by the reader rather than quoted at them. |
| 02 | `m29-fig02-full-vs-m00` | The capstone solution against M00's original shipped estimates | The loop, closed for the second and final time. |
| 03 | `m29-fig03-range-card` | The finished range card with uncertainty bands | This is the deliverable. Every column traces to a module. |
| 04 | `m29-fig04-model-limits` | Solver uncertainty vs range with the transonic region marked and the 4/6DOF boundary annotated | Where this model stops being trustworthy, and why. Ending on the limitation, not the capability. |

**Exercises.** 5, all open-ended: produce a solution for the reader's own rifle;
identify their largest error source and make a plan; find a range where the model
should not be trusted and explain why; write the limitations section in their own
words.

**Tests.** The full suite, plus an end-to-end test of `api.solve` against the
golden fixtures accumulated from M17 onward.

**Author pitfalls.**
- The limitations section is not a formality. A reader who finishes believing
  the solver is exact has learned the wrong lesson from thirty modules.
- `api.solve` should compose the existing pieces, not reimplement them. If it
  needs new physics, something upstream was left incomplete.

---
## Library build map

Which module owns which file. Before building a module, check that its
prerequisites' files exist; if they do not, the prerequisite was skipped and the
module cannot be built as specified.

| File | Built in | Public API introduced |
|---|---|---|
| `viz/style.py`, `viz/io.py` | scaffold | `apply_style`, `save_figure` |
| `units.py`, `constants.py` | M01 | conversions, `G0_MPS2`, `ICAO_SEA_LEVEL` |
| `angles.py` | M02 | `subtension_m`, `mil_ranging_m` |
| `frames.py` | M03 | `rot_*`, `wind_vector_mps`, `los_frame` |
| `numeric.py` | M04 | `central_difference`, `trapezoid`, `simpson` |
| `integrators.py` | M05 | `rk4`, `integrate`, `Event`, `Solution` |
| `energy.py` | M06 | `kinetic_energy_j`, `free_recoil` |
| `vacuum.py` | M07 | `position`, `angle_for_range_rad`, `derivatives` |
| `sight.py` | M08 | `path_above_los_m`, `find_zero_angle_rad` |
| `atmosphere.py` | M09 → M10 | `air_density_kgm3`, `isa`, `speed_of_sound_mps`, `mach` |
| `aero.py` | M11 | `drag_force_n`, `reynolds`, `air_viscosity_pas` |
| `drag.py` | M12 → M13 → M14 | `DragCurve`, `DragModel`, `CustomDragCurve` |
| `trajectory.py` | M15 | `Projectile`, `Conditions`, `solve_trajectory`, `Trajectory` |
| `solver.py`, `output.py` | M16 | `zero_for_range`, `solve_for_target`, `range_card` |
| `validation.py` | M17 | `grid_convergence`, `check_golden` |
| `effects/wind.py` | M18 → M19 | `apply_wind`, `SegmentedWind`, `wind_weighting_curve` |
| `effects/stability.py` | M20 | `miller_sg`, `spin_rate_radps` |
| `effects/spin_drift.py` | M21 | `spin_drift_m` |
| `effects/aero_jump.py` | M22 | `aerodynamic_jump_rad` |
| `effects/coriolis.py` | M23 | `coriolis_acceleration_mps2` |
| `instruments.py` | M24 | `cant_error_m`, `tall_target_scale`, `INSTRUMENT_UNCERTAINTY` |
| `stats/dispersion.py` | M25 | `cep_m`, `mean_radius_m`, `rayleigh_sigma_from_impacts` |
| `stats/uncertainty.py` | M26 | `sensitivity_matrix`, `monte_carlo_trajectory` |
| `stats/hit_probability.py` | M27 | `p_hit`, `improvement_value` |
| `truing.py` | M28 | `joint_true`, `residual_report` |
| `api.py`, `__main__.py` | M29 | `solve`, the CLI |

### The API stability rule

A module may **extend** an earlier file freely. A module may **not silently
change** an earlier public API.

Three modules are known to need such a change, and each is expected to handle it
properly -- document the change in the lesson, update every affected call site,
and update the earlier module's tests and figures in the same session:

| Change | Where | Why |
|---|---|---|
| `derivatives` gains a wind argument | M18 changes M15 | wind enters through air-relative velocity |
| `derivatives` gains a Coriolis term | M23 changes M15 | Coriolis is a genuine acceleration |
| `find_zero_angle_rad` moves from the vacuum solver to the real one | M16 changes M08 | M08 could only use the vacuum solver |

Any *other* API change is a signal that an earlier module was designed wrong.
Fix the earlier module, and say so.

---

## Figure inventory

Roughly 90 figures across 30 modules, 2-4 per module. Every one:

- is generated by a committed script in that module's `code/`
- is saved through `ballistics.viz.save_figure` to `assets/mNN-figKK-slug.png`
- is committed, so the lesson renders on GitHub without running anything
- uses `ballistics.viz.style.apply_style()` and the fixed palette
- carries a **caption** and a **"what to notice"** note in the lesson
- regenerates byte-identically (seeded RNG where randomness is involved)

A figure without a "what to notice" gets cut. Decoration is not the standard;
the standard is that the figure teaches something the prose cannot.

Colour assignments for physical effects are fixed course-wide in
`ballistics.viz.style.EFFECT_COLORS`, so that "orange is wind" holds from M18 to
M29. Use them.

---

## Testing

| Level | What | Where |
|---|---|---|
| Unit | Every public function, with known values | `tests/test_mNN_*.py` |
| Limiting case | Drag → 0 gives the vacuum solution; wind → 0 gives the still-air solution; equator gives zero Coriolis drift | in the owning module's tests |
| Convergence | Observed order of accuracy matches theory | M05, M17 |
| Reference | Agreement with published trajectory data | M17 |
| Regression | Golden files, so later effects cannot silently change earlier answers | `tests/fixtures/`, from M17 on |
| End-to-end | `api.solve` against the accumulated fixtures | M29 |

Every module from M17 onward adds a golden-file case. Every test involving
randomness is seeded.

---

## What this course does not cover

Documented properly in [`docs/appendix-further-study.md`](docs/appendix-further-study.md):
4DOF modified point-mass and 6DOF rigid-body aeroballistics, interior ballistics,
terminal ballistics, CFD, and reloading. Each gets an honest description of what
it is, why the course stops short of it, and where to read next. The boundary is
deliberate, and a reader should finish knowing exactly where they are standing.

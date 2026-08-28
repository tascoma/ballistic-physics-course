# Beyond this course

This course covers **exterior ballistics** with a **3DOF point-mass model** and
modelled corrections for rotational effects. That boundary is deliberate. It is
where the accuracy-per-unit-complexity curve flattens for practical long-range
shooting, and it is the same class of model behind every commercial solver.

Here is what lies on the other side of it, why we stopped, and where to read next.

---

## 4DOF: the modified point-mass model

**What it is.** The point-mass model has no orientation, so a bullet is a
featureless dot. The modified point-mass model adds the yaw of repose as a
computed quantity rather than an empirical correction — four degrees of freedom
instead of three. Spin drift then *emerges* from the model instead of being
bolted on.

**Why we stopped short.** It needs aerodynamic coefficients most shooters cannot
obtain: the overturning moment coefficient $C_{M\alpha}$, the lift curve slope
$C_{L\alpha}$, and the Magnus moment. For a bullet whose published data is a
single BC, a 4DOF model is precision without accuracy.

**Where this course touches it.** Module 21 imports the yaw-of-repose result
that a 4DOF model would derive, and says so.

**Read next.** McCoy, *Modern Exterior Ballistics*, chapters on the modified
point-mass trajectory. NATO STANAG 4355 specifies a standard 4DOF model.

---

## 6DOF: rigid-body aeroballistics

**What it is.** The full treatment: three translational and three rotational
degrees of freedom, with the bullet's complete attitude evolving under the
aerodynamic moments. This is where pitching and yawing motion, dynamic
stability, tricyclic motion, and the real behaviour of a bullet through the
transonic region are properly described.

**Why we stopped short.** It requires the full aerodynamic coefficient set as a
function of Mach number and yaw angle, measured in a spark range or wind tunnel
or computed by CFD. That data exists for a handful of military projectiles and
essentially no commercial bullets. It also requires attitude representation
(Euler angles or quaternions) and a much more careful integrator.

**What you would gain.** A real explanation of transonic instability, of dynamic
(as opposed to gyroscopic) stability, of the epicyclic motion that produces
aerodynamic jump, and of the yaw-induced drag that penalises marginally
stabilised bullets.

**Where this course touches it.** Modules 20, 21, and 22 each import a result
that 6DOF derives. Module 10 waves at transonic instability without explaining it.

**Read next.** McCoy, chapters on the six-degree-of-freedom trajectory and on
linearised pitching and yawing motion. Then the ARL/BRL free-flight spark-range
reduction literature for how the coefficients are actually measured.

---

## Interior ballistics

**What it is.** Everything from primer ignition to muzzle exit: propellant burn
rate, the pressure-time curve, bore friction, barrel time, and the vibration of
the barrel that determines where the muzzle is pointing when the bullet leaves.

**Why we stopped short.** It is a distinct discipline with its own physics
(thermochemistry, gas dynamics, structural vibration), and it determines the
*inputs* to exterior ballistics rather than participating in it. This course
takes muzzle velocity as a measured quantity with an uncertainty (Modules 24
and 26) rather than predicting it.

**What you would gain.** An understanding of muzzle velocity variation — where
it comes from, and why temperature sensitivity of propellant matters at long
range. Also barrel harmonics and the load-tuning practices built on them.

**Read next.** Carlucci and Jacobson, *Ballistics*, Part I.

---

## Terminal ballistics

**What it is.** What happens on impact: penetration, expansion, fragmentation,
energy transfer.

**Why we stopped short.** It is a genuinely different subject, and the popular
metrics for it — "energy at target" especially — are weak proxies that this
course mentions only to caution against (Module 06).

**Read next.** Carlucci and Jacobson, Part III.

---

## Computational fluid dynamics

**What it is.** Numerically solving the flow field around the projectile to
compute drag and moment coefficients from geometry, instead of measuring them.

**Why we stopped short.** It is a specialist discipline, and for the reader's
purposes a measured drag curve (Module 14) is both more accurate and vastly
cheaper.

**Read next.** Any introductory CFD text, then the ARL reports on computed
aerodynamic coefficients for spin-stabilised projectiles.

---

## Reloading

Out of scope entirely. This course explains why muzzle velocity consistency
matters and how much it is worth (Modules 24 through 27); it does not tell you
how to achieve it. That is a practical craft with its own extensive literature
and its own safety requirements.

---

## What you should take away

A model's value is bounded by the quality of the data you can feed it. A 6DOF
model with guessed coefficients is worse than a 3DOF model with a measured drag
curve, because it will be confidently wrong in ways that are harder to detect.

The right question is never "what is the most sophisticated model?" but "what is
the most sophisticated model my data can support?" For a shooter with a
chronograph, a weather meter, and a published G7 BC, the answer is the model
this course builds.

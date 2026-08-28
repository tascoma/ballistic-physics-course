# References

Cite from this file rather than inventing a citation inside a module. If a
module uses a source not listed here, it adds it here in the same session.

## Primary texts

**McCoy, Robert L. — *Modern Exterior Ballistics: The Launch and Flight Dynamics
of Symmetric Projectiles*, 2nd ed., Schiffer, 2012.**
The canonical technical reference for exterior ballistics, and the source this
course defers to when treatments disagree. Covers the point-mass, modified
point-mass, and full 6DOF formulations with the aerodynamic coefficient theory
behind them. Everything in Part VII of this course that we import as a model,
McCoy derives properly. Requires calculus and differential equations.

**Litz, Bryan — *Applied Ballistics for Long-Range Shooting*, 4th ed., Applied
Ballistics LLC.**
The bridge between McCoy's rigour and the range. Source for the practical spin
drift and aerodynamic jump approximations used in Modules 21 and 22, and for the
argument that G7 is the right reference for modern match bullets.

**Litz, Bryan — *Ballistic Performance of Rifle Bullets*, Applied Ballistics LLC
(multiple volumes).**
Independently measured G1 and G7 ballistic coefficients and form factors for a
large set of commercial bullets. The reference for Module 13's claim that
published BCs and measured BCs differ.

**Litz, Bryan — *Accuracy and Precision for Long Range Shooting*, Applied
Ballistics LLC.**
Statistical treatment of group size, dispersion, and hit probability. Background
for Modules 25 and 27.

**Pejsa, Arthur J. — *Modern Practical Ballistics*, 2nd ed.**
An analytical approach that produces closed-form approximations to the
trajectory. Worth reading for contrast with this course's numerical approach,
and for its treatment of the retardation coefficient.

**Carlucci, Donald E., and Sidney S. Jacobson — *Ballistics: Theory and Design of
Guns and Ammunition*, 3rd ed., CRC Press, 2018.**
Engineering-level coverage of interior, exterior, and terminal ballistics. The
reference for the material this course declares out of scope.

## Specific results

**Miller, Donald — "A New Rule for Estimating Rifling Twist", *Precision
Shooting*, March 2005.**
The gyroscopic stability formula used in Module 20, with the velocity and
atmospheric corrections. Empirical, dimensional, and fitted to conventional
jacketed lead-core bullets — all stated in the module per the honesty rule.

**Buck, Arden L. — "New Equations for Computing Vapor Pressure and Enhancement
Factor", *Journal of Applied Meteorology* 20 (1981), 1527-1532.**
Saturation vapour pressure, used in Module 09's humidity correction.

**Ballistic Research Laboratory / Aberdeen Proving Ground — standard drag
function reports.**
Origin of the G-family reference drag curves (G1 through G8). The G1 function
descends from Mayevski's work and Ingalls' tables; G7 from the boattailed
reference projectile. Specific table provenance is recorded in
[`../data/README.md`](../data/README.md) when the tables are created in Module 13.

**Sierra Bullets — *Exterior Ballistics* reference section, Sierra Reloading
Manual.**
Source of published banded G1 ballistic coefficients, used in Module 13 to
illustrate why banding exists.

## Standards

**ISO 2533:1975 — Standard Atmosphere.**
The ICAO standard atmosphere implemented in Module 09.

**JCGM 100:2008 — *Evaluation of measurement data — Guide to the expression of
uncertainty in measurement* (GUM).**
The uncertainty propagation framework used in Module 26. Freely available from
the BIPM.

**NIST Special Publication 811 — *Guide for the Use of the International System
of Units*.**
Unit conversion factors and significant-figure conventions, Module 01.

## Numerical methods

**Press, W. H., et al. — *Numerical Recipes*, 3rd ed., Cambridge, 2007.**
Runge-Kutta methods, adaptive stepping, and Brent's root-finding method, all
used in Modules 05 and 16.

**Hairer, E., Nørsett, S. P., and Wanner, G. — *Solving Ordinary Differential
Equations I: Nonstiff Problems*, 2nd ed., Springer, 1993.**
The rigorous treatment behind Module 05's convergence-order material.

**Roache, Patrick J. — *Verification and Validation in Computational Science and
Engineering*, Hermosa, 1998.**
The verification/validation distinction and grid convergence studies, Module 17.

---

## A note on sourcing

Several results in this course are empirical fits rather than derivations:
Miller's stability rule, the spin drift and aerodynamic jump approximations, the
free-recoil gas factor, and banded ballistic coefficients. Each is cited at the
point of use, with its validity range stated, per the honesty rule in
[`../CLAUDE.md`](../CLAUDE.md). Where published models disagree — as they do for
spin drift — the course shows the disagreement rather than silently picking one.

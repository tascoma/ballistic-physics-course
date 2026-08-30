# Glossary

Every term the course uses, with the module number where it is properly
defined. Each module adds the terms it introduces.

---

**Accuracy** — How close a measurement is to the true value. Distinct from
*precision*: an instrument can be highly repeatable and consistently wrong, and
no amount of staring at its output will reveal the bias. Only comparison
against something independent will. (M01, M24, M25)

**Aerodynamic jump** — A vertical shift in impact caused by a *crosswind*,
arising from the spinning bullet's response to the initial yaw the wind imposes.
An angular offset established at the muzzle, so its linear effect grows linearly
with range. (M22)

**Ballistic coefficient (BC)** — A bullet's ability to resist drag relative to a
standard reference projectile, defined as sectional density divided by form
factor. Units are lb/in². Not a physical property of the bullet alone: it is a
statement about the bullet *and* the reference shape it is compared against. (M13)

**Ballistic solution** — The set of sight corrections that puts a bullet on a
target under stated conditions: elevation, windage, and usually time of flight
and remaining velocity. The output of a solver, and a prediction rather than a
measurement. (M00)

**Boattail** — A tapered rear section that reduces base drag by letting the flow
close more gradually behind the bullet. (M11)

**Click** — One detent of a scope turret. Common sizes are 1/4 MOA and 0.1 mil;
note that the 0.1 mil click is the *coarser* of the two, by the constant factor
4.32/pi = 1.375. Rounding a correction to a whole click leaves a residual of at
most half a click, which is about an inch at 1000 yards for either. (M02)

**Come-up** — The elevation correction dialled into the sight to hit at a given
range, measured from the zero. Distinct from *drop*: drop is measured from the
line the bore was pointed along, come-up from the line of sight, and the two
differ by whatever elevation the zero already built in. (M00, M08)

**Coriolis effect** — Apparent deflection of the bullet caused by the Earth
rotating beneath it during the flight. Horizontal (latitude-dependent) and
vertical (azimuth-dependent, the Eötvös effect) components. (M23)

**Density altitude** — The altitude in the standard atmosphere at which the air
density equals the density where you actually are. A single number summarising
pressure, temperature, and humidity. (M09)

**Dimensional analysis** — Checking an equation by the *dimensions* of its
terms — mass, length and time — rather than by its numbers. Written in square
brackets: a velocity is $[\mathrm{L}][\mathrm{T}]^{-1}$. It can prove an
equation wrong without any knowledge of the physics in it, and it can never
prove one right. (M01)

**Dimensional homogeneity** — The property that every term in a physically
meaningful equation has the same dimensions. The rule that dimensional analysis
tests. You cannot add a length to a time. (M01)

**Dimensionless** — Having no dimensions, so the same number in every unit
system. The drag coefficient, the form factor, Mach number and the gyroscopic
stability factor are all dimensionless; a ballistic coefficient, despite being
described as "a number", is not — it is a mass per unit area. (M01)

**DOPE** — "Data On Previous Engagements": recorded sight corrections that
produced hits at known ranges under known conditions. The empirical record used
to calibrate a solver. (M28)

**Drag coefficient ($C_D$)** — The dimensionless factor in the drag equation. A
*function of Mach number*, not a constant, and not a function of speed directly. (M11, M12)

**Elevation and windage** — The two angular corrections a firing solution
produces: vertical and horizontal respectively. Quoted in MOA or mils. (M00)

**Error, absolute and relative** — Absolute error carries the units of the
quantity (2700 ± 15 fps); relative error is the dimensionless ratio (0.56%).
Absolute errors add through sums; relative errors add through products, and a
power multiplies its exponent in — so squaring a quantity doubles its relative
error. (M01, M26)

**Eötvös effect** — The vertical component of the Coriolis effect. A bullet fired
with an eastward component strikes high and one fired westward strikes low,
because the Earth's rotation adds to or subtracts from the projectile's effective
speed about the Earth's axis. Independent of hemisphere, unlike the horizontal
component. (M00, M23)

**Exterior ballistics** — The flight of the projectile from muzzle exit to
impact. Distinct from interior ballistics (inside the barrel) and terminal
ballistics (after impact). The whole subject of this course. (M00)

**Extreme spread (ES)** — The largest centre-to-centre distance between any two
shots in a group. The most common precision measure and one of the worst: it
uses two shots and discards the rest, and its expected value grows with the
number of shots fired. (M25)

**Form factor ($i$)** — The ratio of a bullet's drag coefficient to that of a
reference projectile. $i<1$ means the bullet is more streamlined than the
reference. (M13)

**Full-value wind** — A crosswind blowing exactly perpendicular to the line of
fire, which produces the maximum deflection for a given wind speed. A wind at an
angle is quoted as a fraction of full value. (M00, M18)

**G1, G7** — Standard reference projectile shapes whose drag curves are
tabulated. G1 is a flat-based, blunt form from the 19th century; G7 is a
boattailed, long-ogive form that far better resembles a modern match bullet. (M12, M13)

**Grain** — The unit bullet and powder mass are quoted in. Exactly 1/7000 of a
pound, hence exactly 64.79891 mg. Not 64.8: the rounded value is wrong in the
fifth significant figure. (M01)

**Gyroscopic stability factor ($S_g$)** — The ratio of a bullet's stabilising
angular momentum to the destabilising aerodynamic overturning moment. $S_g>1$ is
required; $S_g\geq1.4$ is the practical target. (M20)

**Line of departure** — The direction the bullet actually travels as it leaves
the muzzle. Differs slightly from the bore line. (M03, M08)

**Line of sight (LOS)** — The straight line from the eye through the sight to the
target. The x-axis of this course's coordinate frame. (M03)

**Mach number ($M$)** — Speed divided by the local speed of sound. The variable
that drag actually depends on. (M10)

**Mil / milliradian** — Exactly 0.001 radian, subtending 10 cm at 100 m (3.6 in
at 100 yd). Not the 6400-mil artillery circle. (M01, M02)

**Mil ranging** — Estimating range from the number of mils a target of assumed
size subtends: range = size / (mils x 0.001). Its accuracy is limited almost
entirely by how well you know the target's size, since the range error is
directly proportional to the size error. (M02)

**Minute of angle (MOA)** — 1/60 of a degree, subtending 1.047 inches at 100
yards. Distinct from SMOA/IPHY, which is exactly 1 inch per 100 yards. (M01, M02)

**Point-blank range** — The maximum distance over which the trajectory stays
within a specified vertical window around the line of sight, so no holdover is
needed. (M08)

**Precision** — How tightly repeated measurements cluster, independent of
whether that cluster is anywhere near the truth. Distinct from *accuracy*. (M01, M25)

**Reticle** — The aiming reference inside a scope, usually carrying marks at
known angular spacing (mil-dot, MOA hash) so it can be used to measure
subtension as well as to aim. (M02)

**Sectional density (SD)** — Mass divided by the square of the diameter, in
lb/in². A property of the bullet independent of its shape. (M13)

**Significant figures** — The digits of a number that carry information. A
discipline for *reporting* answers, not for computing them: inside a
calculation, carry every digit the machine offers and round only at the end.
Rounding an intermediate compounds, and at three significant figures it can
destroy a trajectory outright. (M01)

**Slant range** — The distance to the target measured along the line of sight,
as opposed to the horizontal range beneath it. On an incline of angle phi the
two differ by a factor cos(phi). A laser rangefinder reports slant range. (M02)

**Small-angle approximation** — Replacing tan(theta) by theta, with theta in
radians. It understates the result by a relative theta^2/3: 27 parts per million
at a 31 MOA come-up, 0.25% at 5 degrees, 10% at 30 degrees. Free for anything
you dial; not free for the geometry of a steep shot. (M02)

**SMOA (IPHY)** — "Shooter's MOA", defined as exactly one inch per hundred
yards, i.e. the ratio 1/3600. A *different unit* from a true MOA and 4.51%
smaller; equivalently a true MOA is 4.72% larger. The ratio is exactly $\pi/3$,
which is where the familiar 1.047 inches at 100 yards comes from. Confusing the
two costs about 15 inches on a 1000-yard come-up. (M01, M02)

**Spin drift** — Lateral drift, in the direction of the rifling twist, caused by
the yaw of repose. Roughly 9 inches at 1000 yards for a typical match load. (M21)

**Standard gravity ($g$)** — Exactly 9.80665 m/s² (32.174049 ft/s²). A
*defined* value, not a measurement: real local gravity runs from about 9.780 at
the equator to 9.832 at the poles. (M01)

**Station pressure** — The actual atmospheric pressure where you are standing,
as opposed to the sea-level-corrected pressure that weather reports quote.
Solvers require station pressure; supplying the corrected value is a large and
common error. (M09)

**Subtension** — The length a given angle covers at a given range,
s = R tan(theta). Linear in range, so every subtension is a straight line
through the origin and the ratio of any two angular units is constant at every
distance. (M02)

**Time of flight (ToF)** — How long the bullet takes to reach a given range. The
quantity that most other effects scale against: gravity, spin drift, and Coriolis
all act over it, which is why anything that slows the bullet down makes
everything else larger. (M00)

**Transonic** — The Mach range roughly 0.8 to 1.2, where drag rises steeply and
the bullet is most easily disturbed. A band, not a point at $M=1$. (M10)

**Truing** — Adjusting a solver's muzzle velocity or ballistic coefficient so
its predictions match observed DOPE. (M28)

**Twist rate** — The distance in which the rifling makes one complete turn,
quoted as e.g. "1:8", one turn in 8 inches. Faster twist (smaller number) means
more spin and more stability. (M20)

**Yaw of repose** — The small steady angle between a bullet's axis and its
velocity vector, arising because a gyroscopically stabilised bullet's nose lags
as gravity turns the trajectory downward. The cause of spin drift. (M21)

**Zero** — The range at which the trajectory crosses the line of sight. There
are normally two crossings; "the zero" conventionally means the second. (M08)

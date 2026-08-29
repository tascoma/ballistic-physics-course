# Module 01 — Solutions

Full working. Where a number is exact, it is written exactly; where it is not,
the working says why.

---

### 1. Convert the contrast load

**Answers:** (a) 0.0113398092 kg = 11.3398 g. (b) 792.48 m/s exactly.
(c) 0.0078232 m = 7.8232 mm. (d) 0.28575 m/turn. (e) 3560.8 J = 2626.3 ft·lb.
(f) It does not convert — and that is the point.

**Working:**

**(a)** Multiply by the exact grain:

$$175\ \text{gr} \times 6.479891\times10^{-5}\ \frac{\text{kg}}{\text{gr}} = 1.13398092\times10^{-2}\ \text{kg} = 11.3398092\ \text{g}$$

Note it is 11.3398 g, not the 11.34 g you get from a rounded 64.8 mg per grain
— the same fifth-figure trap as the 140 gr bullet in the lesson.

**(b)** $2600 \times 0.3048 = 792.48$ m/s. Exact, because the foot is.

**(c)** $0.308 \times 0.0254 = 7.8232\times10^{-3}$ m = 7.8232 mm. This is why
a .308 is sometimes called a 7.82 mm.

**(d)** A 1:11.25 twist is one turn in 11.25 inches:

$$11.25 \times 0.0254 = 0.28575\ \text{m/turn}$$

**(e)** Convert *first*, then compute — never mix:

$$E = \tfrac{1}{2} \times 1.13398092\times10^{-2} \times 792.48^2 = \tfrac{1}{2} \times 1.13398092\times10^{-2} \times 628024.6 = 3560.84\ \text{J}$$

$$E = \frac{3560.84}{1.3558179483314} = 2626.34\ \text{ft·lb}$$

(The manual's $175 \times 2600^2/450240$ gives 2627.49 — 1.15 ft·lb high, the
same 0.044% as in the lesson, from the same stale $g$.)

**(f) The BC does not get converted.** This is the course's one deliberate
exception, and the reason is not laziness. Ballistic coefficient is defined in
lb/in², every published BC in the world is quoted in lb/in², and a "BC of
170.8 kg/m²" would match no bullet box, no manufacturer's table, and no other
source you will ever consult. Converting it would be internally consistent and
practically useless.

So it stays imperial and the variable name carries the exception at every call
site: `bc_lbin2`. If you did work out 0.243 × 703.07 = 170.85 kg/m², your
arithmetic was right and your judgement was wrong, which is a more interesting
kind of error than the reverse.

---

### 2. What kind of quantity is a ballistic coefficient?

**Answers:** (b) $[\mathrm{M}][\mathrm{L}]^{-2}$. (d) 0.2635 lb/in², matching
Sierra's 0.264. (e) $i = 1.0845$, dimensionless. (f) No.

**Working:**

**(a)** Divide the drag force by mass:

$$a = \frac{F_D}{m} = \frac{\tfrac{1}{2}\rho v^2 C_D A}{m} = \tfrac{1}{2}\rho v^2 \cdot \frac{C_D A}{m} = \frac{\tfrac{1}{2}\rho v^2}{\,m/(C_D A)\,}$$

The air contributes $\rho$, the flight contributes $v^2$, and everything left —
$m/(C_D A)$ — is the bullet. Written this way it sits in the *denominator*: the
bigger that group, the less the bullet decelerates. That is already the whole
idea of a ballistic coefficient, before anyone has defined one.

**(b)** $C_D$ is dimensionless (from §4), and $A$ is an area:

$$\left[\frac{m}{C_D A}\right] = \frac{[\mathrm{M}]}{[1] \cdot [\mathrm{L}]^2} = [\mathrm{M}][\mathrm{L}]^{-2}$$

A mass per unit area.

**(c)** $A = \pi d^2/4$, and $\pi/4$ is a pure number, so $[A] = [\mathrm{L}]^2$
and the group's dimensions are $[\mathrm{M}][\mathrm{L}]^{-2}$. Sectional
density is

$$[\text{SD}] = \left[\frac{m}{d^2}\right] = \frac{[\mathrm{M}]}{[\mathrm{L}]^2} = [\mathrm{M}][\mathrm{L}]^{-2}$$

The same. SD and the drag group differ only by the pure number $\pi/4$ and by
$C_D$ — which is exactly the gap the form factor fills.

**(d)** In the native units, mass in pounds and diameter in inches:

$$\text{SD} = \frac{175/7000}{0.308^2} = \frac{0.025}{0.094864} = 0.26354\ \text{lb/in}^2$$

Sierra publishes 0.264. Agreement to three figures, which is all their figure
claims.

**(e)** $i = \text{SD}/\text{BC} = 0.26354/0.243 = 1.0845$.

Its dimensions: SD and BC are both $[\mathrm{M}][\mathrm{L}]^{-2}$, so their
ratio is $[1]$. **The form factor is dimensionless**, and you can know that
without knowing what a form factor *is* — which is the habit this module is
building. ($i > 1$ means this bullet sheds velocity slightly faster than the G7
reference shape. Module 13 explains what that means and how much to trust it.)

**(f) No.** A ballistic coefficient is a mass per unit area,
$[\mathrm{M}][\mathrm{L}]^{-2}$, and lb/in² is a real unit rather than a
decorative label. This catches people out because BC is so often described as
"a number" — but the number is meaningless without lb/in² attached, exactly as
Figure 1.1 argues.

---

### 3. One of these three wind formulas cannot be right

**Answers:** (a) (c) is impossible — it is a time. (b) 72.1 in and 195.6 in.
(c) The lag form, (a). (d) Dimensional analysis rejects; it never accepts.

**Working:**

**(a)** Take each right-hand side apart. $[W_z] = [\mathrm{L}][\mathrm{T}]^{-1}$,
$[x] = [\mathrm{L}]$, $[v_0] = [\mathrm{L}][\mathrm{T}]^{-1}$, $[t] = [\mathrm{T}]$.

Formula (a): the bracket is $[\mathrm{T}] - \dfrac{[\mathrm{L}]}{[\mathrm{L}][\mathrm{T}]^{-1}} = [\mathrm{T}] - [\mathrm{T}] = [\mathrm{T}]$.
The subtraction is legal — both terms are times — which is itself part of the
check. Then

$$[D_z] = [\mathrm{L}][\mathrm{T}]^{-1} \cdot [\mathrm{T}] = [\mathrm{L}]\ \checkmark$$

Formula (b): $[\mathrm{L}][\mathrm{T}]^{-1} \cdot [\mathrm{L}] \div [\mathrm{L}][\mathrm{T}]^{-1} = [\mathrm{L}]\ \checkmark$

Formula (c):

$$\frac{[\mathrm{L}][\mathrm{T}]^{-1} \cdot [\mathrm{T}]^2}{[\mathrm{L}]} = \frac{[\mathrm{L}][\mathrm{T}]}{[\mathrm{L}]} = [\mathrm{T}]$$

**Formula (c) is a time.** Whatever it computes, it is not a distance, and no
choice of units will rescue it. Rejected in about twenty seconds, without
knowing one thing about how wind actually moves a bullet.

**(b)** Convert everything first: $W_z = 10 \times 0.44704 = 4.4704$ m/s,
$x = 914.4$ m, $v_0 = 822.96$ m/s, $t = 1.521$ s.

Formula (a) — note $x/v_0 = 914.4/822.96 = 1.1111$ s is the time the bullet
*would* have taken with no drag, so the bracket is the extra time drag cost it:

$$D_z = 4.4704 \times (1.521 - 1.1111) = 4.4704 \times 0.4099 = 1.8324\ \text{m} = 72.1\ \text{in}$$

Formula (b):

$$D_z = \frac{4.4704 \times 914.4}{822.96} = 4.9671\ \text{m} = 195.6\ \text{in}$$

**(c)** Module 00's table says 72.2 inches, so **formula (a)** is right, to
within a tenth of an inch. Formula (b) is wrong by a factor of 2.7 — it would
have you holding sixteen feet of wind instead of six.

**(d)** Both survivors are dimensionally perfect and they disagree by 170
inches. **Dimensional analysis rejects; it never accepts.** It removed one of
three candidates for free, and then had nothing whatever to say about which of
the remaining two to trust — that took a reference table, and in Module 18 it
will take a derivation.

---

### 4. Derive the 1.047

**Answers:** (a) $\pi/10800$. (b) $1/3600$. (c) $\pi/3$. (d) 1.0472 in and
10.4720 in. (e) 4.51% and 4.72%; different denominators.

**Working:**

**(a)** A full turn is $2\pi$ radians and 360 degrees, so one degree is
$\pi/180$ rad. A minute is one sixtieth of that:

$$1\ \text{MOA} = \frac{1}{60} \cdot \frac{\pi}{180} = \frac{\pi}{10800}\ \text{rad}$$

**(b)** One hundred yards is $100 \times 36 = 3600$ inches, and SMOA is one inch
of subtension at that distance, so as a ratio:

$$1\ \text{SMOA} = \frac{1}{3600}$$

**(c)** Divide:

$$\frac{\text{MOA}}{\text{SMOA}} = \frac{\pi/10800}{1/3600} = \frac{\pi}{10800} \times 3600 = \frac{3600\,\pi}{10800} = \frac{\pi}{3}$$

$$\frac{\pi}{3} = 1.0471975512$$

The 10800 is $3 \times 3600$, so the 3600 cancels and leaves a 3. Everything
else was already $\pi$.

**(d)** One SMOA subtends exactly 1 inch at 100 yards by definition, and one MOA
is $\pi/3$ times bigger:

- at 100 yd: $\pi/3 \times 1 = \mathbf{1.0472}$ inches
- at 1000 yd: $\pi/3 \times 10 = \mathbf{10.4720}$ inches

So the difference between them at 1000 yards is 0.472 inches per unit — the
number Figure 1.2 annotates.

**(e)** Two different questions with two different denominators.

*An SMOA is smaller than a MOA by what fraction of a MOA?*

$$1 - \frac{1}{\pi/3} = 1 - \frac{3}{\pi} = 1 - 0.95493 = 4.51\%$$

*A MOA is larger than an SMOA by what fraction of an SMOA?*

$$\frac{\pi}{3} - 1 = 0.04720 = 4.72\%$$

They differ because the first is a percentage *of the larger* quantity and the
second is a percentage *of the smaller* one. This is the ordinary asymmetry of
percentage change — a 50% fall needs a 100% rise to undo it — and it is worth
being careful with here, because "SMOA is 4.7% smaller" appears in print
constantly and is not quite right.

---

### 5. Add a conversion the library is missing

**Answers:** (a) Conventional. (d) 99991.79 Pa, 1.316% lower.
(e) 760.0000 mmHg, and it is not a coincidence.

**Working:**

**(a)** **Conventional, resting on a measurement** — the same group as
`PA_PER_INHG`, and for the same reason. A millimetre of mercury is defined as
the pressure exerted by a 1 mm column of mercury at a conventional density
(13595.1 kg/m³) under standard gravity. Standard gravity is defined and the
millimetre is defined, but that density was *measured*. So the factor is exact
in its definition and limited in its precision, and a test may not demand
bit-exact round-tripping through it.

There is a free internal consistency check here, and it is more instructive
than it first looks. The ratio of an inch of mercury to a millimetre of mercury
*must* be exactly 25.4 — the mercury density and the gravity cancel, leaving
nothing but the inch-to-millimetre ratio. Divide our two constants and you get

$$\frac{3386.389}{133.322387415} = 25.4000027$$

which is 25.4 to seven figures and not to eight. Nothing is wrong. The
discrepancy is the rounding in `PA_PER_INHG` itself: the unrounded value is
3386.388640341, and we store the seven-figure form. This is what a
*conventional* constant looks like from the inside — quoted to finite
precision, and consistent with its relatives only to that precision.

**(b)** Following the file's pattern:

```python
def mmhg_to_pa(pressure_mmhg: float) -> float:
    """Millimetres of mercury (torr) to pascals.

    Conventional, not exact: fixed by a measured mercury density. Army
    Standard Metro, the atmosphere behind many published G1 ballistic
    coefficients, is defined at 750 mmHg.
    """
    return pressure_mmhg * PA_PER_MMHG


def pa_to_mmhg(pressure_pa: float) -> float:
    """Pascals to millimetres of mercury (torr)."""
    return pressure_pa / PA_PER_MMHG
```

**(c)** One line in `PAIRS`:

```python
("pressure mmHg/Pa", mmhg_to_pa, pa_to_mmhg, 750.0),
```

All four parametrised round-trip tests pick it up automatically. That is the
payoff of listing the pairs in one place rather than writing a test per
function.

**(d)** $750 \times 133.322387415 = 99991.79$ Pa.

$$\frac{99991.79 - 101325}{101325} = -1.316\%$$

Army Standard Metro is **1.316% lower** in pressure than ICAO. Lower pressure
means thinner air, less drag, and a flatter trajectory — which is why Module 09
insists on knowing which standard a published BC was computed against. A
percent and a third does not sound like much until it has propagated through
1000 yards.

**(e)** $101325 / 133.322387415 = 759.99989$ mmHg — 760, to better than one
part in a million.

Not a coincidence. Standard atmospheric pressure was *originally defined* as
760 mmHg, and the modern definition of 101325 Pa exactly was chosen to preserve
it. The residual in the seventh digit is the gap between the old mercury-column
definition and the modern one in pascals. You are looking at a fossil of the
unit's history.

---

### 6. How many digits have you earned?

**Answers:** (a) 4.74 fps. (b) 0.175%. (c) About three. (d) It confuses
arithmetic precision with measurement accuracy. (e) A defensible answer either
way — see below.

**Working:**

**(a)** The standard error of a mean:

$$u(\bar{v}) = \frac{\sigma}{\sqrt{n}} = \frac{15}{\sqrt{10}} = 4.74\ \text{fps}$$

**(b)** $4.74/2712 = 0.00175 = \mathbf{0.175\%}$.

**(c)** Propagate it. Come-up is not simply proportional to velocity, but it is
smooth and monotonic in it, so a 0.175% velocity uncertainty produces a
correction uncertainty of the same rough order:

$$9.0617 \times 0.00175 \approx 0.016\ \text{mil}$$

The uncertainty lands in the *second* decimal place. So the report is good to
about 9.06 mil, and the "17" on the end is decoration —
**three significant figures, arguably four.** The fourth decimal is claiming a
precision of one part in ninety thousand from an input known to one part in
six hundred.

And note this is the *optimistic* answer: it assumes muzzle velocity is the only
uncertain input. It is not. The BC is a published figure of unknown provenance,
the range came from a laser rangefinder, and the air density came from a pocket
weather meter. Module 26 gathers all of them into one budget, and the answer
gets worse.

**(d)** The friend has confused two different things. The *arithmetic* is
indeed good to sixteen digits — §7 of the lesson makes exactly that point, and
Figure 1.3 shows what happens when it is not. But arithmetic precision is a
property of the computation, and what we are reporting is a property of the
*answer*, which inherits the uncertainty of its inputs. A perfectly exact
calculation on an uncertain input yields an uncertain output. Printing sixteen
digits of it tells you about the floating-point unit and nothing about the
rifle.

**(e)** Here is the defensible position, and the thing it turns on.

**In practice, no — it changes nothing you do.** Your turret has 0.1 mil clicks.
Both 9.0617 and 9.06 round to 9.1 mil, and there is no ninth-of-a-click
available to dial. The precision of the display is irrelevant because the
*output device is coarser than the uncertainty*: one click is 0.1 mil, and your
uncertainty is 0.016 mil, six times finer than the smallest correction you can
make.

**But it changes what you conclude when you miss.** If you believe the solution
is 9.0617 and you hit low, the solution looks exonerated and you start
questioning your position, your wind call, or the rifle. If you know it is
9.06 ± 0.02 and that the real budget is wider still, the solution is a
suspect like any other, and Module 28 is about how to interrogate it.

The general form: **displayed precision does not matter when the actuator is
coarser than the uncertainty, and matters enormously for diagnosis.** The digits
are harmless on the dial and misleading in the debrief.

---

### 7. What a chronograph's error does to muzzle energy

**Answers:** (a) 0.556%. (b) 1.111%. (c) ±25.2 ft·lb. (d) 25.11 and 25.25 —
not equal, and they should not be. (e) Measure velocity far more carefully.

**Working:**

**(a)** $15/2700 = 0.005556 = \mathbf{0.556\%}$.

**(b)** Energy goes as $v^2$, so by the rule for powers:

$$\frac{u(E)}{E} = |n| \frac{u(v)}{v} = 2 \times 0.556\% = \mathbf{1.111\%}$$

The relative uncertainty **doubles** crossing the square.

**(c)** $0.01111 \times 2265.8 = \mathbf{25.2\ \text{ft·lb}}$. So the honest
statement is 2266 ± 25 ft·lb — which, incidentally, means the 0.044% discrepancy
in the reloading manual's constant from §4 is *fifty times smaller* than the
uncertainty in the number it is computing. Worth knowing before anyone gets
excited about it.

**(d)** Brute force:

| $v$ (fps) | $E$ (ft·lb) | difference from 2265.80 |
|---|---|---|
| 2685 | 2240.70 | −25.11 |
| 2700 | 2265.80 | — |
| 2715 | 2291.05 | +25.25 |

The predicted ±25.2 sits neatly between them, and **the two sides are not
equal** — the upper interval is 0.14 ft·lb wider.

They should not be. $E \propto v^2$ is a curve, not a line, and the propagation
rule is a linearisation of it — a first-order Taylor expansion about the
nominal, which by construction is symmetric. The true function is convex, so it
rises slightly faster on the high side than it falls on the low side. The
asymmetry is 0.006% of the energy here, which is why linearisation is entirely
safe at this scale. Module 26 says where it stops being safe: when the
uncertainty is large enough, or the function curved enough, that the second-order
term stops being negligible — which is precisely the situation near the
transonic region, where the drag curve bends sharply.

**(e)** Drag force also goes as $v^2$, so velocity error doubles into drag error
too, and drag governs the time of flight, which governs every other effect in
Module 00's ranking. Meanwhile mass enters $\tfrac{1}{2}mv^2$ and $F=ma$
linearly — to the first power — so a 1% mass error stays a 1% error.

**Velocity is worth measuring roughly twice as carefully as mass**, and that is
before considering that bullet mass is controlled to a fraction of a percent at
the factory while muzzle velocity varies shot to shot, with temperature, and
with barrel condition. This is why Part IX spends a module on instrumentation
and why Module 28's truing procedure adjusts muzzle velocity first.

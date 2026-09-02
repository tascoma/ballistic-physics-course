# Module 02 — Exercises

Seven problems. Three are calculations you can check exactly, one is a
derivation, one extends the library, one asks you to read Figure 2.1, and the
last has no single right answer — it is a diagnosis, and the defence matters
more than the verdict.

Work them before reading the [solutions](solutions.md).

**The running load**, used throughout — the course's primary example:

| | |
|---|---|
| Cartridge | 6.5 Creedmoor |
| Bullet | 140 gr Berger Hybrid Target |
| Muzzle velocity | 2700 fps |
| Zero | 100 yd |
| Sight height | 1.75 in |

Its path relative to the line of sight, from Module 00's reference table —
**model output, not measurement**:

| Range (yd) | 500 | 600 | 700 | 800 | 900 | 1000 |
|---|---|---|---|---|---|---|
| Path (in) | −53.178 | −85.507 | −127.505 | −180.514 | −246.123 | −326.229 |

**Exact factors you should not have to look up again:**
1 in ≡ 25.4 mm · 1 yd ≡ 0.9144 m · 1 MOA = $\pi/10800$ rad ·
1 SMOA ≡ 1/3600 · 1 mil ≡ 0.001 rad · $\tan\theta = \theta + \theta^3/3 + \dots$

---

### 1. Dial it

*(hand calculation)*

Your target is at **700 yards**. Read the come-up off the table above.

**(a)** Convert that path to an angular come-up, in both MOA and mils. Use
$\arctan$, not division, and say how much difference it made.

**(b)** Your scope has **1/4 MOA** clicks. How many clicks is the come-up, before
rounding? Your friend's scope has **0.1 mil** clicks — how many for him?

**(c)** Your turret does 60 clicks per revolution and has no zero-stop. Starting
from a 100-yard zero, describe exactly what you turn: how many full
revolutions, and how many clicks past that.

**(d)** You can only dial whole clicks. For each scope, state the whole number
you dial and how far off the point of aim the shot lands as a result, in inches
at 700 yards. Which scope leaves the smaller residual here, and is that a
general result or an accident of this particular range?

*Tolerances: ±0.01 MOA and ±0.001 mil on (a); ±0.01 clicks on (b); ±0.01 in on (d).*

---

### 2. Range it, with error bars

*(hand calculation)*

Through a mil reticle you see a steel plate you believe is **20 inches wide**.
It spans **0.8 mil**. You trust your size estimate to **±15%** and your reticle
reading to **±0.1 mil**.

**(a)** What range does the formula give?

**(b)** Compute the two relative uncertainties, and combine them properly.

**(c)** State the range as a value with an uncertainty, in yards, and give the
one-standard-uncertainty band.

**(d)** In the lesson's worked example the reading error was nearly irrelevant —
it moved 10.00% to 10.62%. Here it is not. Compute each term's contribution and
say *why* this case is different, in terms of the structure of the formula
rather than the numbers.

**(e)** Using the table above, roughly what does the top of your band cost you
in elevation if the truth is at the bottom of it? A one-significant-figure
answer is fine; the point is the order of magnitude.

*Tolerances: ±1 yd on (a); ±0.5% on (b); ±2 yd on (c).*

---

### 3. Where the shortcut costs an inch

*(derivation)*

The small-angle approximation $s \approx R\theta$ understates a subtension. The
lesson gives the relative error as $\theta^2/3$; here you want the absolute one.

**(a)** Starting from the series $\tan\theta = \theta + \theta^3/3 + 2\theta^5/15 + \dots$,
write the absolute error $R(\tan\theta - \theta)$ to leading order.

**(b)** Solve for the angle at which that error equals exactly one inch, as a
function of $R$. Give the closed form.

**(c)** Evaluate it at 100, 600, and 1000 yards. Express each answer in degrees
*and* in MOA.

**(d)** The answers get *smaller* as range increases. Explain in one sentence why
that is the correct behaviour and not a sign of an algebra error.

**(e)** The largest come-up in this whole course is about 31 MOA. By what factor
would it have to grow before the approximation cost you an inch at 1000 yards?

*Tolerances: ±0.01° and ±1 MOA on (c).*

---

### 4. The unit that will cost you fifteen inches

*(hand calculation)*

Your ballistic app reports the 1000-yard come-up for the running load in
**SMOA** (some apps and most reticle-subtension charts do). Your turret is
**true MOA**. You do not notice.

**(a)** From the table, compute the come-up at 1000 yards in MOA and in SMOA.

**(b)** You dial the SMOA number on the MOA turret. How high does the shot land,
in inches at 1000 yards?

**(c)** Express that mistake in 1/4 MOA clicks. How many extra clicks did you
turn?

**(d)** The ratio MOA/SMOA is exactly $\pi/3$, about 4.7%. A 4.7% error sounds
small. Explain why it produces a miss here when a 4.7% error in, say, your
muzzle velocity would not.

*Tolerances: ±0.05 MOA on (a); ±0.5 in on (b).*

---

### 5. Make the ranging function exact

*(code)*

`mil_ranging_m` deliberately uses the linear form. Write a general companion
that does not.

**(a)** Add to `src/ballistics/angles.py`:

```python
def range_for_subtension_m(target_size_m: float, angle_rad: float) -> float:
    """Exact range to a target of known size subtending a known angle."""
```

using $\tan$ rather than the small-angle form, and raising `ValueError` for a
non-positive angle. Document units for both arguments and the return, and add
it to `__all__`.

**(b)** Write a test that the two functions agree to within a stated tolerance
for the lesson's worked example (40 in at 1.4 mil) and for exercise 2's case
(20 in at 0.8 mil).

**(c)** Compute the disagreement in *inches* for both cases. Then answer the
design question: given your numbers, was the library right to use the linear
form in `mil_ranging_m`? Justify it against the size of the reading error, not
against the size of the discrepancy alone.

*Expected: the two cases disagree by 0.019 in and 0.005 in respectively.*

---

### 6. Read the figure

*(interpretation)*

Look at Figure 2.1 in the lesson.

**(a)** The exact curve and the $\theta^2/3$ prediction are drawn on top of each
other and appear to be one line over most of the plot. At roughly what angle do
they visibly separate, and what term in the series is responsible?

**(b)** Both axes are logarithmic and the curve is a straight line. What is its
slope, and what does that slope tell you about the relationship that a linear
plot would have hidden?

**(c)** The plot spans 0.01° to 50°. Give a physical example, from this course,
of an angle at each end of that range.

---

### 7. The shot went high

*(judgement)*

A shooter reticle-ranges a steel torso at what they compute as 800 yards, dials
the come-up their app gives, and hits about 30 inches high. They are shooting
the running load in standard conditions with a 1/4 MOA turret. They ask you what
went wrong.

Four candidates:

1. They used $\theta$ instead of $\tan\theta$ somewhere in the geometry.
2. Their app reported SMOA and their turret is true MOA.
3. They rounded to the nearest whole click.
4. The plate is not the size they assumed.

**(a)** For each candidate, compute or bound the error it could produce at 800
yards, using the table and the lesson's results. Show the number.

**(b)** Rank them. Which single candidate can produce a 30-inch error, and which
are ruled out by more than an order of magnitude?

**(c)** You get to ask the shooter exactly **one** question before answering.
What is it, and what does each possible answer tell you? Defend the choice —
a defensible different question is a correct answer to this exercise.

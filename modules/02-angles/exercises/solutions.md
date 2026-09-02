# Module 02 — Solutions

Work shown, not just answers. Where a number comes from Module 00's reference
table it is **model output, not measurement**, and the solution says so.

---

## 1. Dial it

**(a)** At 700 yards the path is −127.505 in, so the come-up is its magnitude.
Convert both sides to metres first:

$$s = 127.505\ \text{in} \times 0.0254 = 3.23863\ \text{m}
\qquad R = 700 \times 0.9144 = 640.08\ \text{m}$$

$$\theta = \arctan\frac{3.23863}{640.08} = \arctan(0.00505973) = 0.00505969\ \text{rad}$$

In the shooting units:

$$\theta = \frac{0.00505969}{2.908882\times10^{-4}} = \boxed{17.39\ \text{MOA}}
\qquad
\theta = \frac{0.00505969}{0.001} = \boxed{5.060\ \text{mil}}$$

**How much did $\arctan$ matter?** The bare quotient is 0.00505973 rad; the
arctangent is 0.00505969. They differ by $4.3\times10^{-8}$ rad, which at 700
yards is $2.7\times10^{-5}$ m — about one thousandth of an inch. It made no
difference whatsoever, which is the honest answer and the one the lesson
predicts: the relative error is $\theta^2/3 = 8.5\times10^{-6}$.

**(b)** Divide by the click size.

$$n_{\text{MOA}} = \frac{17.39\ \text{MOA}}{0.25\ \text{MOA}} = \boxed{69.58\ \text{clicks}}
\qquad
n_{\text{mil}} = \frac{5.060\ \text{mil}}{0.1\ \text{mil}} = \boxed{50.60\ \text{clicks}}$$

Note the mil turret needs 19 fewer clicks for the identical correction. That is
the coarseness result from §3, not a finer instrument.

**(c)** 69.58 rounds to **70 clicks**. At 60 clicks per revolution:

$$70 = 1 \times 60 + 10$$

So: **one full revolution, then ten more clicks.** This is where the missing
zero-stop bites — the turret now reads "10" and looks exactly like a 10-click
correction. Forgetting the revolution is a 15 MOA error, which at 700 yards is
110 inches. It is by a wide margin the largest error available anywhere in this
module.

**(d)** Dial the whole click, then ask what angle you actually put on:

| Scope | Dial | Angle dialled | Wanted | Residual angle | At 700 yd |
|---|---|---|---|---|---|
| 1/4 MOA | 70 | 17.500 MOA | 17.386 MOA | +0.114 MOA | **+0.78 in** |
| 0.1 mil | 51 | 5.100 mil | 5.060 mil | +0.040 mil | **+1.02 in** |

Both land high, because both rounded up.

**Is the quarter-MOA scope's smaller residual general?** No — this one is an
accident. The residual depends on where the exact click count happens to fall
relative to a whole number, and that is effectively arbitrary at any given
range. What *is* general is the **bound**: the residual can never exceed half a
click, which at 700 yards is 0.92 in for the quarter-MOA turret and 1.26 in for
the tenth-mil. The quarter-MOA turret wins on the guaranteed worst case, always,
by the factor 1.375. It does not win at every individual range.

---

## 2. Range it, with error bars

**(a)** $s = 20\ \text{in} = 0.5080\ \text{m}$, $\theta = 0.8\ \text{mil} = 8\times10^{-4}$ rad.

$$R = \frac{0.5080}{8\times10^{-4}} = 635.0\ \text{m} = \boxed{694\ \text{yd}}$$

**(b)** The two relative uncertainties:

$$\frac{u_s}{s} = 0.15
\qquad\qquad
\frac{u_\theta}{\theta} = \frac{0.1}{0.8} = 0.125$$

In quadrature:

$$\frac{u_R}{R} = \sqrt{0.15^2 + 0.125^2} = \sqrt{0.022500 + 0.015625} = \sqrt{0.038125} = \boxed{0.1953}$$

19.53%.

**(c)** $u_R = 0.1953 \times 694.4 = 135.6$ yd.

$$R = \boxed{694 \pm 136\ \text{yd}}, \qquad \text{band } 559 \text{ to } 830\ \text{yd}$$

A 271-yard-wide bracket. That is not a range estimate; it is a rumour.

**(d)** The contributions to the variance:

| Term | Squared contribution | Share |
|---|---|---|
| size, $0.15^2$ | 0.022500 | 59% |
| reading, $0.125^2$ | 0.015625 | 41% |

Compare the lesson's example, where the shares were 94% and 6%.

**Why the difference is structural, not numerical.** The reading term is
$u_\theta/\theta$ — the *relative* precision of the reading. Your absolute
reading precision is roughly fixed by the reticle (±0.05 to ±0.1 mil), so the
relative precision is fixed by the **denominator**: how many mils the target
subtends. A target spanning 1.4 mil gives 0.036; one spanning 0.8 mil gives
0.125, three and a half times worse.

The general rule: **a small subtension is a bad measurement.** Far targets and
small targets both subtend few mils, and both make the reading term grow. The
lesson's claim that the reading error is negligible is true *for large
subtensions* and is not a universal law — which is exactly why the propagation
formula is worth having instead of a rule of thumb.

**(e)** If the plate is really at the bottom of the band (559 yd) and you dial
for the top (830 yd), then interpolating the table: the come-up at 559 yd is
12.34 MOA and at 830 yd is 23.03 MOA.

$$\Delta = 511.1\ \text{m} \times \left[\tan(23.03\ \text{MOA}) - \tan(12.34\ \text{MOA})\right] \approx 1.6\ \text{m}$$

About **63 inches — five feet high.** You would not see the splash.

---

## 3. Where the shortcut costs an inch

**(a)** From $\tan\theta = \theta + \theta^3/3 + 2\theta^5/15 + \dots$, the
absolute error in the subtension is

$$R\left(\tan\theta - \theta\right) = R\left(\frac{\theta^3}{3} + \frac{2\theta^5}{15} + \dots\right) \approx \boxed{\frac{R\theta^3}{3}}$$

**(b)** Set that equal to one inch and solve. Keeping $R$ and the inch in the
same length unit:

$$\frac{R\theta^3}{3} = 1\ \text{in}
\quad\Longrightarrow\quad
\theta^3 = \frac{3}{R}
\quad\Longrightarrow\quad
\boxed{\theta = \sqrt[3]{\frac{3\ \text{in}}{R}}}$$

**(c)** With $R$ in inches ($1\ \text{yd} = 36\ \text{in}$):

| $R$ | $R$ (in) | $\theta = (3/R)^{1/3}$ | degrees | MOA |
|---|---|---|---|---|
| 100 yd | 3,600 | 0.09410 rad | **5.39°** | **324** |
| 600 yd | 21,600 | 0.05179 rad | **2.97°** | **178** |
| 1000 yd | 36,000 | 0.04368 rad | **2.50°** | **150** |

Check the first one against the exact function:
$3600 \times (\tan 0.09410 - 0.09410) = 1.004$ in. Good to the accuracy of the
leading-order truncation.

**(d)** Because the error is $R\theta^3/3$ — it is **proportional to range**. A
fixed one-inch budget therefore buys you a smaller angle as $R$ grows. Nothing
about the approximation got worse; the same relative error is being cashed out
against a longer lever arm.

**(e)** At 1000 yards the threshold is 150 MOA and the largest come-up in the
course is 31.15 MOA:

$$\frac{150.2}{31.15} = \boxed{4.8\times}$$

The come-up would have to be nearly five times larger. Since the error goes as
$\theta^3$, the actual cost at 31 MOA is $(1/4.8)^3 \approx 1/111$ of an inch —
about nine thousandths. This is the quantitative version of "for corrections it
never matters."

---

## 4. The unit that will cost you fifteen inches

**(a)** At 1000 yd the path is −326.229 in, $R = 914.4$ m,
$s = 8.28622$ m.

$$\theta = \arctan\frac{8.28622}{914.4} = 0.00906158\ \text{rad}$$

$$\theta = \frac{0.00906158}{2.908882\times10^{-4}} = \boxed{31.15\ \text{MOA}}
\qquad
\theta = \frac{0.00906158}{1/3600} = \boxed{32.62\ \text{SMOA}}$$

The SMOA number is larger, because the SMOA is the smaller unit — it takes more
of them to make the same angle. This is the trap: the bigger number *looks* like
more correction, and it is not.

**(b)** You dial 32.62 turret-units, but each is a true MOA:

$$\theta_{\text{dialled}} = 32.62 \times 2.908882\times10^{-4} = 0.00948866\ \text{rad}$$

$$\Delta = 914.4\left[\tan(0.00948866) - \tan(0.00906158)\right] = 914.4 \times 4.2709\times10^{-4} = 0.3906\ \text{m}$$

$$\boxed{15.4\ \text{inches high}}$$

**(c)** In quarter-MOA clicks: the correct come-up is $31.15 \times 4 = 124.6$,
so you dial 125. The SMOA number gives $32.62 \times 4 = 130.5$, so you dial
130 or 131.

$$\boxed{\text{about 5 or 6 clicks too many}}$$

Which is worth noticing: **five clicks is not an obviously wrong-looking
number.** Nothing on the turret warns you.

**(d)** Because this 4.7% is applied to a quantity that is already *the
correction itself*, and the correction is large.

The come-up at 1000 yards is 326 inches of drop being cancelled. An error of
4.7% of the correction is $0.047 \times 326 \approx 15$ inches, and that lands
directly on the target as vertical dispersion.

A 4.7% error in muzzle velocity is different in kind: it propagates through the
whole trajectory, and the resulting change in *drop* is much less than 4.7% of
anything you can see at short range — it grows with time of flight. The general
lesson is that **an error in a correction is a miss; an error in an input is
whatever the physics makes of it**, which is usually smaller and always
range-dependent. Module 26 makes this comparison properly with a sensitivity
matrix.

---

## 5. Make the ranging function exact

**(a)** Added to `src/ballistics/angles.py`:

```python
def range_for_subtension_m(target_size_m: float, angle_rad: float) -> float:
    """Exact range to a target of known size subtending a known angle.

    The exact companion to :func:`mil_ranging_m`, which uses the small-angle
    form. Use this one when the angle is not small -- or when you want to
    demonstrate that it did not matter, which is exercise 5 of Module 02.

    Args:
        target_size_m: The target's true dimension, metres.
        angle_rad: Angle it subtends, radians. Must be positive.

    Returns:
        Range to the target, metres.

    Raises:
        ValueError: If ``angle_rad`` is not positive.
    """
    if angle_rad <= 0.0:
        raise ValueError(f"angle_rad must be positive, got {angle_rad}")
    return target_size_m / math.tan(angle_rad)
```

**(b)** The test:

```python
@pytest.mark.parametrize(
    ("target_size_in", "mils"),
    [(40.0, 1.4), (20.0, 0.8)],
)
def test_exact_and_linear_ranging_agree_at_reticle_angles(target_size_in, mils):
    """The tangent correction is far below the reading precision, so they agree."""
    target_size_m = inches_to_m(target_size_in)
    linear_m = mil_ranging_m(target_size_m, mils)
    exact_m = range_for_subtension_m(target_size_m, mil_to_rad(mils))
    assert exact_m == pytest.approx(linear_m, rel=1e-6)
    assert exact_m < linear_m          # tan(x) > x, so the exact range is shorter
```

**(c)** The disagreements:

| Case | Linear | Exact | Difference |
|---|---|---|---|
| 40 in at 1.4 mil | 793.6508 yd | 793.6503 yd | **0.019 in** |
| 20 in at 0.8 mil | 694.4444 yd | 694.4443 yd | **0.005 in** |

**Was the library right?** Yes, and the comparison that settles it is not
"0.019 inches is small" — it is against the *other* error in the same
calculation.

In exercise 2 the reading uncertainty alone was ±0.1 mil, which propagated to
**±87 yards** of range. The tangent correction is 0.0005 yards. The
approximation is smaller than the dominant uncertainty by a factor of about
**170,000**.

Using `atan` in `mil_ranging_m` would therefore be *false precision*: it would
make the function look more careful while changing no digit any user could
observe, and it would distract from the fact that the whole calculation is
dominated by a number the user guessed. Note that the honest defence required
knowing the size of the reading error — "the correction is tiny" on its own is
not an argument, because tiny compared to what is the entire question.

---

## 6. Read the figure

**(a)** They separate visibly at about **25°**. The responsible term is the
next one in the series, $2\theta^5/15$. Relative to the $\theta^2/3$ prediction
it contributes $2\theta^2/5$, so the prediction is short by 0.4% at 0.1 rad
(5.7°) and by 10% at 0.5 rad (29°) — which is where the eye starts to catch it.

**(b)** The slope is **2**. On log-log axes a power law $y = kx^p$ plots as a
straight line of slope $p$, so a slope of 2 says the error is proportional to
$\theta^2$ — which is precisely the $\theta^2/3$ result, read off the picture
rather than taken from the algebra.

A linear plot would have hidden this completely: over the plotted range the
error spans eight decades, so on linear axes everything below about 20° would be
indistinguishable from zero, and the reader would learn only "it is small",
never "it is small *in this specific way*". The exponent is the transferable
part — it is what lets you say the error falls by a factor of 100 for every
factor of 10 in angle.

**(c)** From this course:

- **0.01° (0.6 MOA)** — around the dispersion of a good rifle: a 0.6 MOA group,
  or a small windage correction. Also the scale of a single turret click
  (0.25 MOA = 0.004°).
- **50°** — a steep mountain or canyon shot, the regime Module 08 handles. Also
  the launch angles of artillery, which is where this course's point-mass model
  and the small-angle habit both stop being appropriate.

---

## 7. The shot went high

**(a)** At 800 yards, come-up 21.55 MOA (path −180.514 in), $R = 731.5$ m.

| # | Candidate | Computation | Error |
|---|---|---|---|
| 1 | $\theta$ for $\tan\theta$ | rel. error $\theta^2/3 = 1.31\times10^{-5}$, applied to 180.5 in | **0.002 in** |
| 2 | SMOA dialled on MOA | come-up is 22.56 SMOA; dialled as MOA gives $731.5[\tan(22.56\,\text{MOA}) - \tan(21.55\,\text{MOA})]$ | **8.5 in high** |
| 3 | Click rounding | at most half a 1/4 MOA click $= 731.5\tan(0.125\,\text{MOA})$ | **≤ 1.05 in** |
| 4 | Wrong plate size | a 10% size error puts the believed range at 880 yd; come-up 25.20 vs 21.55 MOA | **31 in high** |

**(b)** The ranking is not close:

$$\text{size guess (31 in)} \gg \text{SMOA mix-up (8.5 in)} > \text{click rounding (1.05 in)} \ggg \text{small-angle (0.002 in)}$$

**Only candidate 4 can produce 30 inches.** Candidate 2 is a real and common
error but is off by a factor of 3.5 — it cannot account for the miss alone,
though it could be a contributing part of it. Candidate 3 is bounded at about an
inch and is ruled out by a factor of 30. Candidate 1 is ruled out by a factor of
**fifteen thousand**; it is not a candidate at all, and the only reason to
compute it is to retire it permanently.

Note that candidate 1 is the one people worry about — it is the one that feels
like a mathematical mistake — and it is the one that is physically impossible as
an explanation. That inversion is most of the point of this module.

**(c)** **The question: "How do you know the plate is that size — did you
measure it, or is that the usual size?"**

Because the arithmetic says the size guess is the only single candidate that
reaches 30 inches, and it is the only input in the chain that was never
measured. Their come-up came from an app, their click count is arithmetic, their
turret is calibrated. The size is a memory.

What the answers tell you:

- *"I ranged it with a laser"* — then candidate 4 is out, and you are left with
  no single sufficient cause. Now look for a **combination** (SMOA mix-up plus
  rounding is 9.5 in, still short) or, more likely, something outside this
  module's four candidates entirely: a missed turret revolution (15 MOA = 110 in
  at 800 yd, easily enough), a wrong zero, or the wrong come-up row.
- *"It's a standard torso, they're all about 40 inches"* — candidate 4 is live
  and probably sufficient. Ask what a 36-inch plate would imply: 714 yards, and
  the 30-inch miss falls out.

**A defensible alternative question** is "Did the turret go past one full
revolution?" That is not the highest-prior cause given a 30-inch error
specifically, but it is the highest-*consequence* one — a missed revolution is
110 inches at this range, an order of magnitude worse than anything else on the
list, and it is cheap to rule out. Preferring to eliminate the catastrophic
failure first is a legitimate diagnostic strategy, and the exercise accepts it
provided the reasoning is stated.

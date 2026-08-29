# Module 00 — Solutions

Full working, not just answers. Two of these are exercises in being wrong
usefully, so the explanation matters more than the number.

---

### 1. Time of flight from average velocity

**Answer:** (a) 1.45 s. (b) Low by about 5%. (c) The straight line lies above the
real velocity curve, so the average is an overestimate and the time an
underestimate.

**Working:**

**(a)** 1000 yards is 3000 feet. The plain average of the two speeds is

$$\bar{v} \approx \frac{2700 + 1440}{2} = 2070 \text{ fps}$$

$$t \approx \frac{3000 \text{ ft}}{2070 \text{ fps}} = 1.449 \text{ s}$$

**(b)** The table says 1.521 s. The estimate is low by 0.072 s, or 4.7%.

**(c)** Drag depends on the *square* of speed, so a fast bullet is decelerating
hard and a slow one much less hard. Velocity therefore falls steeply out of the
muzzle and flattens out downrange — a curve that sags below the straight line
joining its endpoints:

```
 2700 |*.
      |  ' .                 <- straight line (what the average assumes)
      |     ' .
      |        '  .
      |    real  ↘   ' .
      |   curve         ' .
 1440 |                     '
      +------------------------
      0 yd                1000 yd
```

Taking the plain average of the endpoints is the same as pretending the bullet
followed that straight line. The straight line lies **above** the true curve
almost everywhere, so it assumes the bullet was faster than it really was, which
makes the flight look shorter than it really was.

The bullet spends a disproportionate share of its flight in the slow back half —
which is exactly why every effect in this course grows faster than linearly with
range.

*If you want a better estimate:* a bullet losing speed to drag decays roughly
exponentially with distance, and modelling it that way gives 1.55 s — within 2%
of the truth rather than 5% low. Module 05 does this properly.

---

### 2. Drop, if there were no air

**Answer:** (a) 447 inches. (b) 22% larger than the real 367 inches.
(c) Drag opposes the *downward* part of the motion too.

**Working:**

**(a)** With $t = 1.52$ s:

$$\tfrac{1}{2}gt^2 = \tfrac{1}{2}(32.17)(1.52)^2 = 37.2 \text{ ft} = 447 \text{ in}$$

**(b)** The real drop is 367 inches. The vacuum figure is 80 inches larger — 22%
high.

**(c)** The contradiction dissolves once you notice that **drag is not a
horizontal force.** Drag always acts directly opposite the bullet's velocity,
and the velocity is not horizontal for most of the flight.

Early on the bullet is travelling nearly level, and drag is nearly all backwards
— it slows the bullet down and does almost nothing vertically. But as gravity
turns the path downward, the velocity acquires a growing downward component, and
drag, pointing opposite, acquires a growing **upward** component. Over the back
half of the flight the air is holding the bullet up, slightly.

So drag does two opposing things to drop:

| | Effect on drop |
|---|---|
| Slows the bullet, lengthening the time of flight | **increases** it |
| Resists the downward motion once the path angles down | **decreases** it |

The question compared like with like — it used the *real* 1.52 s time of flight
for both — so the first effect was already baked into both numbers. What is left
is the second effect on its own, and it is worth 80 inches.

If you instead compare against a true vacuum trajectory, which would arrive in
1.11 s, the vacuum drop is only 20 feet against the real 31. That comparison
shows the first effect dominating. **Both comparisons are valid and they point
opposite ways**, which is why the question had to specify which time of flight to
use. Module 07 builds both trajectories and puts them on one plot.

---

### 3. Leading a walking target, and what it says about wind

**Answer:** (a) 19 inches, 1.8 mils. (b) 64 inches. (c) The bullet is already
moving with the walker's frame in neither case — but it *starts out* matching the
air's sideways motion nowhere, and it only ever acquires a fraction of the wind's
speed. See below.

**Working:**

**(a)** 3 mph is $3 \times 1.467 = 4.4$ ft/s.

$$4.4 \times 0.36 = 1.60 \text{ ft} = 19.2 \text{ in}$$

At 300 yards one mil is $0.036 \times 300 = 10.8$ inches, so this is
$19.2 / 10.8 = 1.8$ mils.

**(b)** 10 mph is 14.67 ft/s.

$$14.67 \times 0.36 = 5.3 \text{ ft} = 64 \text{ in}$$

**(c)** The real answer is 5.2 inches. The naive calculation is **12 times too
big**.

The difference is what the two calculations assume about the initial condition.

The walker is moving sideways at 4.4 ft/s for the whole 0.36 seconds, and nothing
resists that. The arithmetic is exact.

The wind calculation assumes the bullet is carried sideways at the full 14.67
ft/s from the instant it leaves the muzzle. It is not. The bullet leaves with
**zero** sideways velocity. What the crosswind does is push it sideways, and that
push is a drag force — it only exists while there is a *difference* between the
bullet's sideways speed and the air's. The bullet spends its whole flight slowly
accelerating sideways and never gets close to wind speed. It ends up with a small
fraction of it.

The right way to think about crosswind is not "the wind carries the bullet" but
"the bullet is slightly behind where it would be if it had never been pushed" —
a **lag**, not a ride. It is a much smaller number than people expect, and this
1-in-12 ratio is the single most useful thing in this exercise.

Module 18 derives the lag-time result properly. Note also that this ratio is not
a constant: it depends on the load and the range.

---

### 4. Does Coriolis matter?

**Answer:** (a) 46%. (b) About 1030 yards. (c) Figure 0.1 measures each effect
against the *other effects*; the plate measures it against the *target*. The
target is the one that decides whether you model it.

**Working:**

**(a)** From the data file, horizontal Coriolis at 1000 yards is 2.31 inches.

$$\frac{2.31}{5.0} = 46\%$$

Nearly half the margin, from the effect the figure makes look invisible.

**(b)** Half the margin is 2.5 inches. The file gives 2.31 inches at 1000 yards
and 2.87 at 1100, so interpolating:

$$1000 + 100 \times \frac{2.50 - 2.31}{2.87 - 2.31} \approx 1030 \text{ yd}$$

By 1200 yards it is 3.50 inches — 70% of the margin.

**(c)** The two impressions differ because they use different denominators.

**Figure 0.1 compares effects to each other.** On that comparison Coriolis is
genuinely tiny: 2.3 inches against 367 is a rounding error, and the figure is
right that if you are going to get one thing correct, it should not be this one.

**The plate compares effects to the target.** On that comparison 2.3 inches is
half your margin, because the target does not care how large your *other* errors
are. A miss is a miss.

The second comparison is the one that decides whether to model something. **The
threshold for "does this matter" is set by the target, not by the biggest effect
in the problem.** An effect is negligible when it is small compared to the size
of what you are shooting at — and, in practice, compared to the errors you cannot
eliminate.

That last clause is the honest caveat. Coriolis is usually ignored at 1000 yards
not because 2.3 inches is nothing, but because the shooter's wind call is
probably worth ±4 inches and their velocity spread another ±2, so correcting a
2.3-inch effect while a 4-inch one floats free is misplaced effort. The moment
you have driven those down — a good wind meter, a chronographed load, a calm
day — Coriolis stops being noise and starts being the thing standing between you
and centre. That is exactly the reasoning Module 26 formalises as an uncertainty
budget.

---

### 5. One afternoon

**Answer:** (b) The wind meter, in most circumstances. Worked reasoning below,
and (c) gives two circumstances that reverse it.

**Working:**

**(a)** The wind is the only one you can compute from this module.

A 10 mph full-value crosswind moves the bullet 43 inches at 800 yards, so each
mph is worth 4.3 inches. Improving your call from ±2 mph to ±1 mph takes your
wind error from **±8.6 inches to ±4.3 inches** — a 4.3-inch improvement.

For the other two you cannot get there from here, and saying so precisely is the
exercise. What you would need is a **sensitivity**: how many inches of elevation
change at 800 yards per 50 fps of muzzle velocity, and per 5% of BC. Those come
from running a solver twice and differencing — which is Module 26, and is exactly
what an uncertainty budget is.

A reasonable guess: both change the elevation by *something like* a few inches at
800 yards, because both act by changing the time of flight slightly, and 800
yards is not far enough for a small velocity change to compound dramatically.

*For reference, having built the solver:* +50 fps is worth **7.6 inches** of
elevation at 800 yards, and a 5% BC error is worth **4.3 inches**. So all three
effects are the same order of magnitude — a few inches — which is precisely why
this is a judgement call and not an arithmetic one.

**(b)** **The wind meter**, for two reasons that have nothing to do with it being
the largest number.

*It is the only error that is fresh every shot.* Muzzle velocity and BC are
approximately fixed properties of your rifle and ammunition. Get them wrong and
you get a **consistent** error — one you will discover the first time you shoot
at 800 yards, and can correct once and for all by dialling differently. Wind is
different every single shot. There is no dialling it out and no learning it once.
An error you can calibrate away is worth much less than an error you cannot.

*It is the only one you cannot get for free later.* Module 28 will show you how
to recover your effective muzzle velocity and BC from your own DOPE — the rifle
tells you what they are if you shoot it at distance and record the results. There
is no equivalent trick for wind.

**(c)** Two circumstances reverse it.

**You shoot in consistently calm conditions, or much further out.** If your wind
is reliably under 5 mph, the ±1 mph improvement is worth about 2 inches and stops
being the biggest lever. And past about 1000 yards, muzzle velocity error starts
compounding much faster than it does at 800 — a velocity spread that is invisible
at 800 opens vertical groups dramatically at 1200, because the slower rounds have
much longer to fall.

**Your BC figure is not 5% off but 15% off.** The published number on a bullet
box is a single figure for a quantity that actually varies with speed, and
independent measurements sometimes disagree with manufacturers by considerably
more than 5%. If yours is one of those, the BC option jumps to the top. Module 13
is about exactly this, and about why "the BC on the box" is a shakier number than
it looks.

The general shape of the answer — **fix what you cannot calibrate away, and
prefer errors you can measure over errors you must guess** — is worth more than
the ranking itself.

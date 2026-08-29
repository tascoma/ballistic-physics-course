# Module 00 — Exercises

Five estimation problems. None needs a formula you have not been given, and none
needs a solver. What they need is arithmetic and a sense of scale.

Two of them are designed so that **your estimate will be wrong**. That is the
point: knowing which direction an approximation errs in, and why, is worth more
than a number you cannot check. Work them before reading the
[solutions](solutions.md).

Everything you need is in the lesson's tables or in
[`../data/effect_magnitudes.csv`](../data/effect_magnitudes.csv).

Useful constants: 1 yard = 3 feet = 36 inches · 1 mph = 1.467 ft/s ·
$g$ = 32.17 ft/s² · at any range, 1 mil = 0.036 inches per yard (so 36 inches at
1000 yd, 10.8 inches at 300 yd).

---

### 1. Time of flight from average velocity

*(hand calculation)*

The running load leaves the muzzle at 2700 fps and is still doing about 1440 fps
when it arrives at 1000 yards.

**(a)** Treating its average speed as the plain average of those two numbers,
estimate the time of flight to 1000 yards.

**(b)** Compare your estimate with the 1.52 s in the lesson's table. Is it high
or low, and by what percentage?

**(c)** Explain the direction of the error. The velocity does not fall in a
straight line as the bullet goes downrange — it drops steeply at first and more
gently later. Sketch that curve, draw the straight line your average assumed,
and say which lies above the other.

*Tolerance: ±0.03 s on (a).*

---

### 2. Drop, if there were no air

*(hand calculation, then interpretation)*

A bullet in a vacuum falls $\tfrac{1}{2}gt^2$ below the line it was launched
along.

**(a)** Using the real time of flight of 1.52 s, compute that fall in inches.

**(b)** The table says the actual drop at 1000 yards is 367 inches. Your answer
should be substantially larger. By how much, as a percentage?

**(c)** Air resistance is what slows the bullet down, and slowing it down makes
the flight *longer*, which should make it fall *more*. Yet the real drop is less
than the vacuum figure computed from the real time of flight. Resolve the
apparent contradiction.

*Tolerance: ±10 inches on (a).*

---

### 3. Leading a walking target, and what it says about wind

*(hand calculation)*

A person walks at about 3 mph. You are shooting at 300 yards, where the time of
flight is 0.36 s.

**(a)** How far does the walker move during the bullet's flight? Give your answer
in inches and in mils.

**(b)** Now do the same arithmetic for a 10 mph crosswind: multiply 10 mph by the
time of flight, as though the wind carried the bullet along with it at full speed
from the moment it left the muzzle.

**(c)** The table says the real deflection from a 10 mph crosswind at 300 yards
is 5.2 inches. Your answer to (b) is more than ten times that. The walker
calculation was right and the wind calculation was badly wrong — what is
different about the two situations?

*Tolerance: ±2 inches on (a), ±5 inches on (b).*

---

### 4. Does Coriolis matter?

*(interpretation)*

Figure 0.1 makes Coriolis look negligible: at 1000 yards it is a 2.3-inch bar
next to a 367-inch one, more than two decades away on the log axis.

You are shooting a 10-inch steel plate, so you can afford to be 5 inches off
centre in any direction before you miss.

**(a)** At 1000 yards, what percentage of that 5-inch margin does horizontal
Coriolis consume on its own?

**(b)** Using the data file, find the range at which horizontal Coriolis alone
eats half the margin.

**(c)** Figure 0.1 and your answer to (a) give opposite impressions of the same
effect. Both are correct. What is each one measuring the effect *against*, and
which comparison is the right one when you are deciding whether to model
something?

---

### 5. One afternoon

*(judgement — there is a defensible answer, and stating the tradeoff is part of it)*

You shoot at 800 yards. You have one afternoon and can do exactly one of these:

1. **Chronograph your ammunition** and learn your true muzzle velocity, which you
   currently take from the box and could be off by 50 fps.
2. **Buy and learn a wind meter**, improving your wind calls from roughly ±2 mph
   to roughly ±1 mph.
3. **Get measured ballistic coefficient data** for your bullet instead of the
   manufacturer's published figure, which could be off by 5%.

At 800 yards this load needs 180 inches of elevation, and a 10 mph full-value
crosswind moves it 43 inches.

**(a)** Estimate what each error costs you in inches at 800 yards. For the wind,
scale the 43-inch figure. For muzzle velocity and BC you cannot compute the
effect from anything in this module — so instead, state what you would need to
know, and make a guess you are willing to be wrong about.

**(b)** Pick one and defend it.

**(c)** Name something in your ranking that could reverse it — a circumstance,
or a fact about one of the three options, that would make a different choice
correct.

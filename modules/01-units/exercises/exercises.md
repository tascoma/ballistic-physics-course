# Module 01 — Exercises

Seven problems. Two are conversion drills, two are derivations you can check
exactly, one is a formula to reject, one is code, and one has no single right
answer — it is a judgement about how many digits you have earned.

Work them before reading the [solutions](solutions.md).

**The contrast load**, used in several of these — the course's second load, so
that you are not always converting the same four numbers:

| | |
|---|---|
| Cartridge | .308 Winchester |
| Bullet | 175 gr Sierra MatchKing |
| Mass | 175 gr |
| Calibre | 0.308 in |
| Length | 1.240 in |
| G7 BC | 0.243 lb/in² |
| Muzzle velocity | 2600 fps |
| Twist | 1:11.25 in, right-hand |

**Exact factors you should not have to look up again:**
1 in ≡ 25.4 mm · 1 yd ≡ 0.9144 m · 1 gr ≡ 64.79891 mg · 1 lb ≡ 7000 gr ≡
0.45359237 kg · 1 fps ≡ 0.3048 m/s · 1 mph ≡ 0.44704 m/s ·
$g$ ≡ 9.80665 m/s² · 1 inHg = 3386.389 Pa · 1 MOA = $\pi/10800$ rad

---

### 1. Convert the contrast load

*(hand calculation)*

Put the whole spec sheet into SI, as `units.py` would.

**(a)** Bullet mass, in kilograms and in grams.
**(b)** Muzzle velocity, in m/s.
**(c)** Calibre, in metres and in millimetres.
**(d)** Twist rate, in metres per turn.
**(e)** Muzzle energy, in joules and in foot-pounds, via $\tfrac{1}{2}mv^2$.
**(f)** The G7 BC, in SI.

Part (f) is the interesting one. Think before you reach for a factor.

*Tolerances: ±0.0001 g on (a); exact on (b); ±0.0001 mm on (c); ±1 J and
±1 ft·lb on (e).*

---

### 2. What kind of quantity is a ballistic coefficient?

*(derivation)*

You met $F_D = \tfrac{1}{2}\rho v^2 C_D A$ in §4 and confirmed that $C_D$ must
be dimensionless. Push the same equation one step further.

**(a)** A bullet's *deceleration* from drag is $a = F_D/m$. Write $a$ out in
full and isolate the group of bullet properties — the terms that describe the
projectile rather than the air or the speed. You should find $m/(C_D A)$.

**(b)** What are the dimensions of $m/(C_D A)$?

**(c)** Sectional density is defined as $\text{SD} = m/d^2$, with $m$ in pounds
and $d$ in inches, giving the units lb/in². Show that SD has the same
dimensions as the group in (b). (Reference area is $A = \pi d^2/4$, and $\pi/4$
is a pure number.)

**(d)** Compute the contrast load's sectional density in lb/in². Sierra
publishes 0.264 for this bullet — do you get it?

**(e)** The form factor $i$ is defined by $\text{BC} = \text{SD}/i$. Given the
published G7 BC of 0.243 lb/in², what is $i$? What are *its* dimensions, and
how do you know?

**(f)** In one sentence: is a ballistic coefficient a dimensionless number?

*Tolerance: ±0.001 on (d) and (e).*

---

### 3. One of these three wind formulas cannot be right

*(interpretation)*

Three formulas for crosswind deflection $D_z$, all found in the wild. $W_z$ is
crosswind speed, $x$ is range, $v_0$ is muzzle velocity, and $t$ is time of
flight.

$$\text{(a)}\quad D_z = W_z\left(t - \frac{x}{v_0}\right) \qquad
\text{(b)}\quad D_z = \frac{W_z\, x}{v_0} \qquad
\text{(c)}\quad D_z = \frac{W_z\, t^2}{x}$$

**(a)** Work out the dimensions of each right-hand side. Which one cannot
possibly be a deflection, and what is it instead?

**(b)** Evaluate the two survivors for the running load at 1000 yards: a 10 mph
full-value crosswind, $x$ = 1000 yd, $v_0$ = 2700 fps, $t$ = 1.521 s. Give both
answers in inches.

**(c)** Module 00's reference table says the true figure is 72.2 inches. Which
survivor is right?

**(d)** State, in one sentence, what this tells you about the limits of
dimensional analysis.

*Tolerance: ±2 inches on (b).*

---

### 4. Derive the 1.047

*(derivation)*

Everyone who shoots knows that one MOA is "about 1.047 inches at 100 yards".
Derive it, and find out that the number is prettier than it looks.

**(a)** From the definition of a minute of angle, write $1\ \text{MOA}$ in
radians as an exact expression in $\pi$.

**(b)** From the definition of SMOA — one inch per hundred yards — write
$1\ \text{SMOA}$ as an exact fraction. (100 yards is 3600 inches.)

**(c)** Form the ratio MOA/SMOA and simplify. You should get a familiar
constant divided by a small integer.

**(d)** Use it to state, to four decimal places, what one MOA subtends at 100
yards and at 1000 yards.

**(e)** An SMOA is what percentage smaller than a true MOA? A true MOA is what
percentage larger than an SMOA? Explain in one sentence why these are not the
same number.

---

### 5. Add a conversion the library is missing

*(code)*

`units.py` has no millimetres of mercury, and it needs them: the older *Army
Standard Metro* atmosphere — the standard against which many published G1
ballistic coefficients were computed — is defined at **750 mmHg**, and Module 09
will have to compare the two standards.

**(a)** Add `PA_PER_MMHG = 133.322387415` to `constants.py`. Which of the three
provenance groups does it belong in, and why? (Hint: what is a millimetre of
mercury defined from?)

**(b)** Add `mmhg_to_pa` and `pa_to_mmhg` to `units.py`, following the file's
existing pattern, with docstrings that state their units.

**(c)** Add a round-trip case to `tests/test_m01_units.py`'s `PAIRS` list and
confirm the suite still passes.

**(d)** Compute Army Standard Metro's 750 mmHg in pascals. By what percentage
does it differ from ICAO's 101325 Pa, and in which direction?

**(e)** Convert 101325 Pa to mmHg. The answer is suspiciously round. Why?

*Expected: (d) 99991.79 Pa, 1.316% lower than ICAO. (e) 759.99989 mmHg.*

---

### 6. How many digits have you earned?

*(judgement)*

You chronograph ten shots of the running load. The mean is **2712 fps** with a
standard deviation of **15 fps**.

**(a)** Your ten-shot mean is an estimate of the true average muzzle velocity.
The uncertainty in a mean is the standard deviation divided by $\sqrt{n}$.
Compute it.

**(b)** As a relative uncertainty, what is that, as a percentage?

**(c)** Your app reports a 1000-yard come-up of **9.0617 mils**. How many of
those digits are carrying information? Justify your answer with the number from
(b), not with a rule about decimal places.

**(d)** A friend argues that since the come-up is a computed quantity and the
computation is exact to sixteen digits, reporting four decimals is fine. What
is wrong with that argument?

**(e)** You are now going to *dial* this correction on a turret with 0.1 mil
clicks. Does any of the above change what you actually do? This is the
judgement part, and there is a defensible answer either way — give yours and
say what it turns on.

---

### 7. What a chronograph's error does to muzzle energy

*(hand calculation)*

The running load: 140 gr at 2700 fps, muzzle energy 2265.8 ft·lb. Your
chronograph is good to **±15 fps**.

**(a)** Express ±15 fps as a relative uncertainty.

**(b)** Muzzle energy goes as $v^2$. Using the rule for powers, what is the
relative uncertainty in the energy?

**(c)** Convert that back to an absolute uncertainty, in foot-pounds.

**(d)** Check the rule by brute force: compute the muzzle energy at 2685 fps
and at 2715 fps and compare the swing with your answer to (c). Are the two
sides of the interval exactly equal? Should they be?

**(e)** Drag force also goes as $v^2$. Without doing any more arithmetic, say
what this implies about how carefully you should measure muzzle velocity
compared with, say, bullet mass.

*Tolerance: ±0.5 ft·lb on (c).*

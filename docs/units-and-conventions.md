# Units and conventions

These decisions are made once, here, and are not renegotiated inside a module.
Thirty modules of quiet convention drift is unrecoverable, so this file is
authoritative and any module that needs to change it must change it *here*,
explicitly, and fix whatever it breaks.

## 1. The library is SI on the inside

Every function in `src/ballistics/` takes and returns SI:

| Quantity | Unit |
|---|---|
| length | metre (m) |
| mass | kilogram (kg) |
| time | second (s) |
| temperature | kelvin (K) |
| pressure | pascal (Pa) |
| angle | radian (rad) |
| force | newton (N) |
| energy | joule (J) |

Imperial units exist only at the boundary: input parsing, range cards, and
figure axis labels. `ballistics.units` (built in Module 01) is the only place
conversions live.

**Why.** Shooting runs on a genuinely absurd unit set -- grains of mass, feet
per second, yards of range, inches of drop, minutes of angle, inches of mercury
of pressure, degrees Fahrenheit. Mixed-unit arithmetic is the single most
common source of silent errors in ballistics code, and unlike a crash, a
wrong-by-2.2× answer looks plausible. One internal system means every formula
from every textbook can be typed in as written, and dimensional analysis
actually works as a check.

## 2. Every variable name carries its unit

```python
range_m = 914.4          # good
velocity_mps = 823.0     # good
twist_in = 8.0           # good -- imperial at the boundary, and it says so
drop_moa = 8.2           # good

velocity = 823.0         # BUG. metres or feet per second?
```

This is enforced by convention and code review, not by a type system. We
deliberately do **not** use a units library like `pint`:

- The course *teaches* dimensional analysis (Module 01). Delegating it to a
  library would hide the very thing being taught.
- Wrapped quantities do not survive contact with `scipy.optimize` and
  `solve_ivp` without friction, and the ODE solver is the heart of the course.
- Suffixed floats are readable by someone who has never seen the library.

Standard suffixes:

| Suffix | Unit | | Suffix | Unit |
|---|---|---|---|---|
| `_m` | metres | | `_yd` | yards |
| `_mm` | millimetres | | `_in` | inches |
| `_kg` | kilograms | | `_gr` | grains |
| `_mps` | metres/second | | `_fps` | feet/second |
| `_s` | seconds | | `_ms` | milliseconds |
| `_k` | kelvin | | `_c`, `_f` | Celsius, Fahrenheit |
| `_pa` | pascals | | `_inhg`, `_hpa` | inches Hg, hectopascals |
| `_rad` | radians | | `_deg`, `_moa`, `_smoa`, `_mil` | degrees, MOA, SMOA/IPHY, milliradians |
| `_j` | joules | | `_ftlb` | foot-pounds |
| `_kgm3` | kg/m³ | | `_mph`, `_kt` | miles/hour, knots |

## 3. The one exception: ballistic coefficient stays in lb/in²

`bc_lbin2`, `sd_lbin2`. See the closing section of [`notation.md`](notation.md)
for why: every published BC in the world is in these units, and converting
would produce numbers matching no reference anywhere. The suffix makes the
exception visible at every call site.

## 4. Coordinate frames

**The course frame** is right-handed, with its origin at the muzzle:

- **+x** downrange, along the line of sight
- **+y** up, opposite gravity
- **+z** to the shooter's right

```
        +y (up)
         |
         |
         +--------- +x (downrange, along line of sight)
        /
       /
     +z (shooter's right)
```

So gravity is $\vec{g} = (0, -g, 0)$, spin drift from a right-hand twist is
**+z**, and a right-to-left wind has a **negative** $W_z$.

Three lines are distinct and are never conflated:

| Line | Definition |
|---|---|
| **Bore line** | the axis of the barrel, extended |
| **Line of departure** | the bullet's actual initial velocity direction (differs from the bore line by jump) |
| **Line of sight** | from the eye through the sight to the target -- the **x-axis** |

The bore points slightly *above* the line of sight, which is why a bullet
crosses the line of sight twice. Module 08 makes this precise.

**Inclined shots.** The x-axis follows the line of sight, so it tilts with the
rifle. Gravity does not, and in the tilted frame it acquires an x-component.
This is the honest way to handle inclination, and it is why the "rifleman's
rule" is an approximation rather than a fact.

**Wind.** $\vec{W}$ is the velocity of the air. Shooters name the direction wind
comes *from* ("3 o'clock wind" comes from the right, blowing left, so
$W_z < 0$). `frames.wind_vector()` is the single place that conversion happens.

## 5. Angles

Radians everywhere internally. At the boundary:

- **MOA** is exactly 1/60 of a degree, $2.908882\times10^{-4}$ rad. At 100 yards
  it subtends 1.047 inches, not 1.000.
- **SMOA** (also "IPHY", "shooter's MOA") is exactly 1 inch per 100 yards, so
  as a ratio it is exactly 1/3600. It is a *different unit*: an SMOA is 4.51%
  smaller than a true MOA, equivalently a true MOA is 4.72% larger than an
  SMOA. The ratio is exactly $\pi/3$. Per *unit* the gap looks small -- 0.472
  inches at 1000 yards -- but corrections are dialled by the dozen. A
  1000-yard come-up is around 31 MOA, and getting the unit wrong there is
  about 15 inches of elevation. Enough to miss with.
- **mil** is exactly 0.001 radian. Not the 6400-mil artillery circle.

## 6. Reference conditions

When a module says "standard conditions" without qualification it means the
**ICAO standard atmosphere at sea level**:

| | |
|---|---|
| Pressure | 101325 Pa (29.9213 inHg) |
| Temperature | 288.15 K (15 °C, 59 °F) |
| Relative humidity | 0 |
| Density | 1.225 kg/m³ |
| Speed of sound | 340.294 m/s |

This is the reference for drag tables and the default in `tests/conftest.py`.
Note that "standard" in the shooting world sometimes means the older *Army
Standard Metro* (750 mmHg, 15 °C, 78% RH, density 1.2260 kg/m³), which is what
older G1 BC figures were computed against. When a source matters, the module
says which standard it used.

## 7. Angular vs linear corrections

Drop and drift are computed in **metres** and converted to angular units for
presentation. Angular corrections are `atan(offset / range)`, never
`offset / range` -- the small-angle approximation is fine at 100 yards and
sloppy at 2000. Module 02 quantifies exactly how sloppy.

## 8. Numbers in prose

Lessons are written for shooters, so **prose and figures use imperial units**
(yards, inches, fps, grains, MOA/mil) with SI in parentheses where it helps.
**Code uses SI.** The worked example in each module carries a single realistic
load all the way through, so the reader can check every intermediate value.

## 9. Randomness is seeded

Any figure or example involving randomness uses
`np.random.default_rng(SEED)` with the seed declared as a module-level constant
and stated in the figure caption. Figures must regenerate byte-identically, or
`tools/build_figures.py` becomes noise in every diff.

"""Physical constants and unit conversion factors, grouped by where they come from.

Every number in this file is one of three things, and the difference matters
enough that it decides the layout:

**Exact by definition.** Somebody wrote the value down in a treaty or a
standard, and it is true the way "12 inches to the foot" is true. The 1959
international yard and pound agreement fixed ``1 yd = 0.9144 m`` and
``1 lb = 0.45359237 kg`` exactly, and everything imperial in this course
descends from those two lines. Standard gravity, ``G0_MPS2``, is also a defined
value -- it is not a measurement of gravity anywhere in particular, and local
$g$ genuinely differs from it by a few parts in ten thousand.

**Conventional, resting on a measurement.** ``PA_PER_INHG`` is the only one.
An inch of mercury is defined from a *measured* mercury density, so its last
digits are not free the way 0.0254 is free. It is quoted to seven figures and
that is all the precision there is.

**Derived.** Reciprocals and products of the above, written as expressions
rather than as decimal literals so they cannot drift from their definitions
and so the reader can see where they came from.

Module 01 explains why this distinction is worth a whole section of a lesson:
a round-trip test can demand bit-exact equality of an exact factor, and cannot
demand it of a conventional one.

One consequence shapes how this file is written. **Exact in decimal is not the
same as exact in binary.** Every factor here that has an exact decimal form is
written as that decimal literal, never derived by arithmetic from another one,
because Python parses a literal to the nearest double while arithmetic
compounds rounding. ``12 * M_PER_INCH`` is 0.30479999999999996, which is a
different double from ``0.3048`` -- and carried into ``fps_to_mps(2700)`` it
turns 822.96 into 822.9599999999999. The difference is a hundredth of a
micron per second and it will never move a bullet, but it is exactly the kind
of thing this module is about noticing. The definitional relationship lives in
the comment; the literal lives in the code.
"""

from __future__ import annotations

import math
from types import MappingProxyType

# --- Exact by definition: length -------------------------------------------
# International yard and pound agreement (1959). 1 in = 25.4 mm exactly, and
# the yard and foot follow from it.

M_PER_INCH = 0.0254
M_PER_FOOT = 0.3048       # = 12 in
M_PER_YARD = 0.9144       # = 36 in

# --- Exact by definition: mass ---------------------------------------------
# The avoirdupois pound is exactly 0.45359237 kg and there are exactly 7000
# grains in it, so the grain is exact too: 64.79891 mg. Not 64.8 -- the
# rounded value is wrong in the fifth significant figure, which is enough to
# move a muzzle energy by a couple of foot-pounds.

KG_PER_POUND = 0.45359237
GRAINS_PER_POUND = 7000
KG_PER_GRAIN = 6.479891e-05          # = KG_PER_POUND / 7000
GRAINS_PER_KG = 1.0 / KG_PER_GRAIN   # no exact decimal form; a reciprocal

# --- Exact by definition: speed --------------------------------------------
# A foot per second is exact because the foot is. A mile per hour is exact
# because the mile is 5280 ft. A knot is exactly one international nautical
# mile (1852 m, defined) per hour.

MPS_PER_FPS = 0.3048        # = 1 ft/s
MPS_PER_MPH = 0.44704       # = 5280 ft / 3600 s
MPS_PER_KNOT = 1852.0 / 3600.0   # no exact decimal form; 1852 m per hour

# --- Exact by definition: pressure -----------------------------------------

PA_PER_HPA = 100.0

# --- Exact by definition: energy -------------------------------------------
# A foot-pound is a foot times a pound-force, and a pound-force is a pound mass
# times *standard* gravity -- which is itself a defined number, so the whole
# product is exact.

J_PER_FTLB = 1.3558179483314004     # = 0.3048 * 0.45359237 * 9.80665

# --- Exact by definition: temperature --------------------------------------
# The kelvin/Celsius offset and the 5/9 Fahrenheit ratio are both definitional.
# Note these are *affine*: a temperature converts with the offset, a temperature
# *difference* converts without it. See ballistics.units.

KELVIN_OFFSET_C = 273.15
K_PER_DEG_F = 5.0 / 9.0
F_FREEZING = 32.0

# --- Exact by definition: angle --------------------------------------------
# A degree is 1/360 of a turn and a minute is 1/60 of a degree, so MOA is
# exact in terms of pi. A mil in this course is a true milliradian, exactly
# 0.001 rad -- never one of the artillery circles.
#
# SMOA ("shooter's MOA", IPHY) is defined as a *subtension ratio*: one inch per
# hundred yards, which is 1/3600 exactly. Strictly that makes it a tangent
# rather than an angle; as an angle it is atan(1/3600), which differs in the
# eleventh significant figure and never matters. We take the ratio as the
# definition because that is what the shooting world means by it, and because
# it makes MOA/SMOA come out as exactly pi/3.

RAD_PER_DEGREE = math.pi / 180.0
RAD_PER_MOA = math.pi / 10800.0      # pi / (180 * 60)
RAD_PER_MIL = 1.0e-3
RAD_PER_SMOA = 1.0 / 3600.0          # 1 inch per 100 yards

# --- Conventional, resting on a measurement --------------------------------
# An inch of mercury at 32 degF, per NIST SP 811. It is derived from a
# conventional mercury density (13595.1 kg/m^3) and standard gravity, and that
# density is measured, so this factor is the one number in this file whose
# trailing digits are not free. Standard sea-level pressure is 29.9213 inHg;
# the widely quoted 29.92 is 4.2 Pa short of it.

PA_PER_INHG = 3386.389

# --- Defined physical constants --------------------------------------------

#: Standard gravity, m/s^2. A *defined* value (CGPM 1901), not a measurement.
#: Local gravity varies from about 9.780 at the equator to 9.832 at the poles,
#: roughly 0.3%; Module 26 decides whether that is worth carrying.
G0_MPS2 = 9.80665

#: ICAO standard atmosphere at sea level -- the course's default conditions
#: whenever a module says "standard" without qualifying it. Read-only, because
#: a shared mutable module-level dict is a bug waiting for a long course.
#:
#: This is *not* Army Standard Metro (750 mmHg, 15 degC, 78% RH), against which
#: older G1 ballistic coefficients were computed. Module 09 explains why the
#: ~0.5% density difference between the two standards matters.
ICAO_SEA_LEVEL = MappingProxyType(
    {
        "pressure_pa": 101325.0,
        "temp_k": 288.15,
        "rh": 0.0,
        "density_kgm3": 1.225,
        "speed_of_sound_mps": 340.294,
    }
)

__all__ = [
    "F_FREEZING",
    "G0_MPS2",
    "GRAINS_PER_KG",
    "GRAINS_PER_POUND",
    "ICAO_SEA_LEVEL",
    "J_PER_FTLB",
    "KELVIN_OFFSET_C",
    "KG_PER_GRAIN",
    "KG_PER_POUND",
    "K_PER_DEG_F",
    "M_PER_FOOT",
    "M_PER_INCH",
    "M_PER_YARD",
    "MPS_PER_FPS",
    "MPS_PER_KNOT",
    "MPS_PER_MPH",
    "PA_PER_HPA",
    "PA_PER_INHG",
    "RAD_PER_DEGREE",
    "RAD_PER_MIL",
    "RAD_PER_MOA",
    "RAD_PER_SMOA",
]

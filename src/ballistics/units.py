"""Conversions between the units shooters use and the SI the library computes in.

This is the boundary layer. Everything inside ``src/ballistics/`` is metres,
kilograms, seconds, kelvin, pascals and radians; everything a shooter says is
not. These functions are the only sanctioned crossing point, and every one of
them names its units in its own docstring, because a function called
``convert`` that you have to read the source of is worse than no function.

Why forty small functions instead of one clever table
-----------------------------------------------------
A single ``convert(value, "fps", "mps")`` would be a third of the length. It
would also push every unit error from import time to run time, defeat every
editor's autocomplete, and make ``grep -r fps_to_mps`` -- the question "where
does this course turn a chronograph reading into physics?" -- unanswerable.
The functions below are deliberately boring. In the one file that all
twenty-eight remaining modules import, boring is the feature.

Naming is mechanical: ``<from>_to_<to>``, with the SI side of every pair
spelled the same way as the unit suffix convention in
``docs/units-and-conventions.md`` s.2. The call site should read as English::

    velocity_mps = fps_to_mps(chronograph_fps)

Temperature is the exception to watch
--------------------------------------
Mass, length, speed, pressure, energy and angle are *scales*: converting them
is multiplication by one, and it commutes with subtraction, so the same
function converts a value and a difference. Temperature is *affine* -- it has
an offset -- so ``f_to_k`` converts a temperature and emphatically does not
convert a temperature difference. A 10 degF spread in powder temperature is
5.6 K, not 260.9 K. Each temperature docstring says so; Module 09 is where it
starts to matter.
"""

from __future__ import annotations

from ballistics.constants import (
    F_FREEZING,
    GRAINS_PER_KG,
    J_PER_FTLB,
    K_PER_DEG_F,
    KELVIN_OFFSET_C,
    KG_PER_GRAIN,
    M_PER_FOOT,
    M_PER_INCH,
    M_PER_YARD,
    MPS_PER_FPS,
    MPS_PER_KNOT,
    MPS_PER_MPH,
    PA_PER_HPA,
    PA_PER_INHG,
    RAD_PER_DEGREE,
    RAD_PER_MIL,
    RAD_PER_MOA,
    RAD_PER_SMOA,
)

# --- Mass -------------------------------------------------------------------


def grains_to_kg(mass_gr: float) -> float:
    """Grains to kilograms. 1 gr = 64.79891 mg exactly (not 64.8)."""
    return mass_gr * KG_PER_GRAIN


def kg_to_grains(mass_kg: float) -> float:
    """Kilograms to grains."""
    return mass_kg * GRAINS_PER_KG


# --- Velocity ---------------------------------------------------------------


def fps_to_mps(velocity_fps: float) -> float:
    """Feet per second to metres per second. Exact: 1 fps = 0.3048 m/s."""
    return velocity_fps * MPS_PER_FPS


def mps_to_fps(velocity_mps: float) -> float:
    """Metres per second to feet per second."""
    return velocity_mps / MPS_PER_FPS


# --- Length -----------------------------------------------------------------


def yards_to_m(length_yd: float) -> float:
    """Yards to metres. Exact: 1 yd = 0.9144 m."""
    return length_yd * M_PER_YARD


def m_to_yards(length_m: float) -> float:
    """Metres to yards."""
    return length_m / M_PER_YARD


def inches_to_m(length_in: float) -> float:
    """Inches to metres. Exact: 1 in = 25.4 mm."""
    return length_in * M_PER_INCH


def m_to_inches(length_m: float) -> float:
    """Metres to inches."""
    return length_m / M_PER_INCH


def feet_to_m(length_ft: float) -> float:
    """Feet to metres. Exact: 1 ft = 0.3048 m. Used for altitude and for range."""
    return length_ft * M_PER_FOOT


def m_to_feet(length_m: float) -> float:
    """Metres to feet."""
    return length_m / M_PER_FOOT


# --- Pressure ---------------------------------------------------------------


def inhg_to_pa(pressure_inhg: float) -> float:
    """Inches of mercury (at 32 degF) to pascals.

    The one conversion factor in this library that rests on a measurement
    rather than a definition: an inch of mercury is fixed by a conventional
    mercury density. Standard sea-level pressure is 29.9213 inHg, not the
    29.92 usually quoted -- the rounded figure is 4.2 Pa short.
    """
    return pressure_inhg * PA_PER_INHG


def pa_to_inhg(pressure_pa: float) -> float:
    """Pascals to inches of mercury (at 32 degF)."""
    return pressure_pa / PA_PER_INHG


def hpa_to_pa(pressure_hpa: float) -> float:
    """Hectopascals (= millibars) to pascals. Exact: 1 hPa = 100 Pa."""
    return pressure_hpa * PA_PER_HPA


def pa_to_hpa(pressure_pa: float) -> float:
    """Pascals to hectopascals (= millibars)."""
    return pressure_pa / PA_PER_HPA


# --- Temperature ------------------------------------------------------------
# Affine, not scale. These convert temperatures, never temperature differences.


def f_to_k(temp_f: float) -> float:
    """Fahrenheit to kelvin. A *temperature*, not a temperature difference."""
    return (temp_f - F_FREEZING) * K_PER_DEG_F + KELVIN_OFFSET_C


def k_to_f(temp_k: float) -> float:
    """Kelvin to Fahrenheit. A *temperature*, not a temperature difference."""
    return (temp_k - KELVIN_OFFSET_C) / K_PER_DEG_F + F_FREEZING


def c_to_k(temp_c: float) -> float:
    """Celsius to kelvin. A *temperature*, not a temperature difference."""
    return temp_c + KELVIN_OFFSET_C


def k_to_c(temp_k: float) -> float:
    """Kelvin to Celsius. A *temperature*, not a temperature difference."""
    return temp_k - KELVIN_OFFSET_C


# --- Energy -----------------------------------------------------------------


def ftlb_to_j(energy_ftlb: float) -> float:
    """Foot-pounds (force) to joules. Exact: 1 ft-lbf = 1.3558179483314004 J."""
    return energy_ftlb * J_PER_FTLB


def j_to_ftlb(energy_j: float) -> float:
    """Joules to foot-pounds (force)."""
    return energy_j / J_PER_FTLB


# --- Wind speed -------------------------------------------------------------


def mph_to_mps(velocity_mph: float) -> float:
    """Miles per hour to metres per second. Exact: 1 mph = 0.44704 m/s."""
    return velocity_mph * MPS_PER_MPH


def mps_to_mph(velocity_mps: float) -> float:
    """Metres per second to miles per hour."""
    return velocity_mps / MPS_PER_MPH


def kt_to_mps(velocity_kt: float) -> float:
    """Knots to metres per second. Exact: 1 kt = 1852 m/h (nautical mile per hour)."""
    return velocity_kt * MPS_PER_KNOT


def mps_to_kt(velocity_mps: float) -> float:
    """Metres per second to knots."""
    return velocity_mps / MPS_PER_KNOT


# --- Angle ------------------------------------------------------------------
# Three angular units a shooter meets, and they are genuinely different sizes.
# MOA / SMOA = pi/3 exactly; see the module 01 lesson for the derivation.


def deg_to_rad(angle_deg: float) -> float:
    """Degrees to radians."""
    return angle_deg * RAD_PER_DEGREE


def rad_to_deg(angle_rad: float) -> float:
    """Radians to degrees."""
    return angle_rad / RAD_PER_DEGREE


def moa_to_rad(angle_moa: float) -> float:
    """True minutes of angle to radians. 1 MOA = 1/60 degree = 2.908882e-4 rad."""
    return angle_moa * RAD_PER_MOA


def rad_to_moa(angle_rad: float) -> float:
    """Radians to true minutes of angle."""
    return angle_rad / RAD_PER_MOA


def smoa_to_rad(angle_smoa: float) -> float:
    """SMOA ("shooter's MOA", IPHY) to radians.

    SMOA is defined as one inch per hundred yards, i.e. the ratio 1/3600. It is
    a *different unit* from a true MOA, 4.51% smaller, and mixing them up costs
    about 15 inches on a 1000-yard come-up. Module 02 builds the subtension
    geometry; this is only the unit.
    """
    return angle_smoa * RAD_PER_SMOA


def rad_to_smoa(angle_rad: float) -> float:
    """Radians to SMOA ("shooter's MOA", IPHY). See :func:`smoa_to_rad`."""
    return angle_rad / RAD_PER_SMOA


def mil_to_rad(angle_mil: float) -> float:
    """Milliradians to radians. Exactly 0.001 rad -- the true mil, not an artillery mil."""
    return angle_mil * RAD_PER_MIL


def rad_to_mil(angle_rad: float) -> float:
    """Radians to milliradians."""
    return angle_rad / RAD_PER_MIL


__all__ = [
    "c_to_k",
    "deg_to_rad",
    "f_to_k",
    "feet_to_m",
    "fps_to_mps",
    "ftlb_to_j",
    "grains_to_kg",
    "hpa_to_pa",
    "inches_to_m",
    "inhg_to_pa",
    "j_to_ftlb",
    "k_to_c",
    "k_to_f",
    "kg_to_grains",
    "kt_to_mps",
    "m_to_feet",
    "m_to_inches",
    "m_to_yards",
    "mil_to_rad",
    "moa_to_rad",
    "mph_to_mps",
    "mps_to_fps",
    "mps_to_kt",
    "mps_to_mph",
    "pa_to_hpa",
    "pa_to_inhg",
    "rad_to_deg",
    "rad_to_mil",
    "rad_to_moa",
    "rad_to_smoa",
    "smoa_to_rad",
    "yards_to_m",
]

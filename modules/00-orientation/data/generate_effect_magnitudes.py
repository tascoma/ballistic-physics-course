"""Generate ``effect_magnitudes.csv``: the reference table Module 00 hands the reader.

    uv run python modules/00-orientation/data/generate_effect_magnitudes.py

READ THIS BEFORE TRUSTING ANYTHING THIS SCRIPT PRODUCES
--------------------------------------------------------
The output is **model output, not measurement**. Nothing here was fired.

This script is a standalone reference implementation. It imports nothing from
``src/ballistics/`` and it is deliberately *not* the library the course builds:
Module 00 needs honest numbers on day one, before the reader has written a single
line of solver, and inventing a citation would be worse than generating the data
and saying where it came from. Module 17 rebuilds this table with the reader's
own solver and diffs it against this one. That comparison is worth something
precisely because the two implementations are independent.

Three of the six effects below are **empirical fits, not physics**, and each is
flagged at its own function:

* gyroscopic stability     -- Miller's rule (2005)
* spin drift               -- Litz's closed form in time of flight
* aerodynamic jump         -- Litz's per-mph angular approximation

The other three -- drop, crosswind deflection, and Coriolis -- fall out of
integrating the point-mass equations of motion, which is what Parts II-V of the
course teach the reader to do properly.

Everything internal is SI. Imperial appears only in the emitted columns, in the
two empirical fits that are natively imperial, and in the load description.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

# --- Provenance -------------------------------------------------------------

GENERATED_ON = "2026-08-29"
OUT_PATH = Path(__file__).resolve().parent / "effect_magnitudes.csv"

# --- Physical constants -----------------------------------------------------

G_MPS2 = 9.80665
OMEGA_EARTH_RADPS = 7.292115e-5

# ICAO standard atmosphere at sea level (docs/units-and-conventions.md, s.6).
RHO_KGM3 = 1.225
SPEED_OF_SOUND_MPS = 340.294
TEMP_R = 518.67          # 59 degF in Rankine, for Miller's rule
PRESSURE_INHG = 29.9213

# --- Unit conversions (imperial lives only at the boundary) -----------------

M_PER_YD = 0.9144
M_PER_IN = 0.0254
MPS_PER_FPS = 0.3048
MPS_PER_MPH = 0.44704
KG_PER_GRAIN = 6.479891e-5
#: 1 lb/in^2 of ballistic coefficient, in kg/m^2. BC stays imperial by course
#: convention (docs/notation.md); this is the only place it is converted.
KGM2_PER_LBIN2 = 0.45359237 / (M_PER_IN**2)
#: A true minute of angle: 1/60 degree. Not SMOA.
RAD_PER_MOA = math.radians(1.0 / 60.0)

# --- The running load (CURRICULUM.md, "The running example") ----------------

MASS_GR = 140.0
DIAMETER_IN = 0.264
LENGTH_IN = 1.360
BC_G7_LBIN2 = 0.315
MV_FPS = 2700.0
TWIST_IN = 8.0                 # 1:8, right-hand
SIGHT_HEIGHT_IN = 1.75
ZERO_YD = 100.0

# --- Scenario ---------------------------------------------------------------

CROSSWIND_MPH = 10.0           # full value, from 3 o'clock (the shooter's right)
LATITUDE_DEG = 40.0            # north -- central United States
#: Northeast. Deliberately not due east: at latitude 45 firing due east the two
#: Coriolis components come out numerically identical (sin 45 = cos 45), which
#: looks like a copy-paste error in the table rather than the coincidence it is.
AZIMUTH_DEG = 45.0

RANGES_YD = np.arange(100.0, 1201.0, 100.0)

DT_S = 1.0e-4

# --- The G7 standard drag function ------------------------------------------
#
# Zero-yaw drag coefficient of the G7 reference projectile against Mach number.
# The G-family curves originate in Ballistic Research Laboratory work at
# Aberdeen; G7 is the boattailed, long-ogive reference that resembles a modern
# match bullet far better than the 19th-century G1 form does. Module 13 ships
# the authoritative tables and records their provenance in data/README.md; this
# abbreviated copy exists only so Module 00 can stand alone.
#
# The shape that matters: flat near 0.12 while subsonic, a steep climb through
# the transonic band, a peak just past Mach 1, then a slow decline.

G7_MACH = np.array([
    0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
    0.55, 0.60, 0.65, 0.70, 0.725, 0.75, 0.775, 0.80, 0.825, 0.85,
    0.875, 0.90, 0.925, 0.95, 0.975, 1.00, 1.025, 1.05, 1.075, 1.10,
    1.125, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.50, 1.55, 1.60, 1.65,
    1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00, 2.05, 2.10, 2.15, 2.20,
    2.25, 2.30, 2.35, 2.40, 2.45, 2.50,
])
G7_CD = np.array([
    0.1198, 0.1197, 0.1196, 0.1194, 0.1193, 0.1194, 0.1194, 0.1194,
    0.1193, 0.1193, 0.1194, 0.1193, 0.1194, 0.1197, 0.1202, 0.1207,
    0.1215, 0.1226, 0.1242, 0.1266, 0.1306, 0.1368, 0.1464, 0.1660,
    0.2054, 0.2993, 0.3803, 0.4015, 0.4043, 0.4034, 0.4014, 0.3987,
    0.3955, 0.3884, 0.3810, 0.3732, 0.3657, 0.3580, 0.3440, 0.3376,
    0.3315, 0.3260, 0.3209, 0.3160, 0.3117, 0.3078, 0.3042, 0.3010,
    0.2980, 0.2951, 0.2922, 0.2892, 0.2864, 0.2835, 0.2807, 0.2779,
    0.2752, 0.2725, 0.2697,
])


def g7_cd(mach: float) -> float:
    """Zero-yaw drag coefficient of the G7 reference projectile. Dimensionless."""
    return float(np.interp(mach, G7_MACH, G7_CD))


# --- Empirical fit 1: gyroscopic stability, Miller's rule -------------------


def miller_sg() -> float:
    """Gyroscopic stability factor for the running load at ICAO sea level.

    EMPIRICAL FIT, NOT PHYSICS. Miller, "A New Rule for Estimating Rifling
    Twist", Precision Shooting, March 2005. The rule is dimensional, natively
    imperial, and fitted to conventional jacketed lead-core bullets; it has no
    derivation behind it and it does not know what a plastic tip or a monolithic
    copper bullet is. Valid roughly for 1.0 < Sg < 3.0 on such bullets. Module
    20 treats it properly, including where it fails.

    Returns:
        Dimensionless stability factor. Sg > 1 is required for stability;
        Sg >= 1.4 is the practical target.
    """
    length_cal = LENGTH_IN / DIAMETER_IN
    twist_cal = TWIST_IN / DIAMETER_IN

    sg = (30.0 * MASS_GR) / (
        twist_cal**2 * DIAMETER_IN**3 * length_cal * (1.0 + length_cal**2)
    )
    # Miller's velocity correction, normalised to 2800 fps.
    sg *= (MV_FPS / 2800.0) ** (1.0 / 3.0)
    # Miller's atmospheric correction, normalised to 59 degF and 29.92 inHg.
    sg *= (TEMP_R / 519.0) * (29.92 / PRESSURE_INHG)
    return sg


# --- Empirical fit 2: spin drift, Litz --------------------------------------


def spin_drift_in(tof_s: float, sg: float) -> float:
    """Lateral drift from the yaw of repose, in inches.

    EMPIRICAL FIT, NOT PHYSICS. Litz, Applied Ballistics for Long-Range
    Shooting: SD = 1.25 (Sg + 1.2) T^1.83, with T the time of flight in seconds
    and the result in inches. A point-mass model has no orientation and
    therefore cannot produce spin drift at all; this is a curve fit standing in
    for what a 4DOF or 6DOF model would derive. Fitted to conventional
    long-range match bullets at supersonic speed, and it is a single-parameter
    summary of a genuinely more complicated phenomenon. Module 21 treats it
    properly, and shows where published models disagree.

    The result is positive for a right-hand twist (drift to the shooter's
    right, +z in the course frame). This load's twist is right-hand.
    """
    return 1.25 * (sg + 1.2) * tof_s**1.83


# --- Empirical fit 3: aerodynamic jump, Litz --------------------------------


def aero_jump_moa_per_mph(sg: float) -> float:
    """Vertical jump induced by a crosswind, in MOA per mph of crosswind.

    EMPIRICAL FIT, NOT PHYSICS. Litz, Applied Ballistics for Long-Range
    Shooting: jump = 0.01 Sg - 0.0024 L + 0.032 MOA per mph, with L the bullet
    length in calibres. Fitted to conventional match bullets.

    Aerodynamic jump is an angular offset established in the first few metres of
    flight, as the crosswind imposes an initial yaw and the spinning bullet
    responds perpendicular to it. Because it is an *angle* set at the muzzle,
    its linear effect grows linearly with range rather than accelerating the way
    drop does.

    Sign: for a right-hand twist, a wind from 3 o'clock -- from the shooter's
    right -- jumps the bullet UP. This is the direction that surprises people,
    and it is the one Module 22 derives.
    """
    length_cal = LENGTH_IN / DIAMETER_IN
    return 0.01 * sg - 0.0024 * length_cal + 0.032


# --- The point-mass model ---------------------------------------------------


def _accel(
    vel_mps: np.ndarray,
    wind_mps: np.ndarray,
    omega_radps: np.ndarray | None,
) -> np.ndarray:
    """Acceleration on the projectile, in m/s^2, in the line-of-sight frame.

    Gravity, drag against the *air-relative* velocity, and optionally Coriolis.

    The drag term is the standard ballistic-coefficient form. Starting from
    a = rho v^2 Cd A / (2m) with A = pi d^2 / 4, and writing the bullet's own
    drag coefficient as i * Cd_ref, the bullet's shape and mass collapse into
    BC = m / (i d^2), leaving a = (pi/8) rho v^2 Cd_ref(M) / BC. Module 13
    derives this; here it is used as given.
    """
    v_air_mps = vel_mps - wind_mps
    speed_mps = float(np.linalg.norm(v_air_mps))
    mach = speed_mps / SPEED_OF_SOUND_MPS

    bc_kgm2 = BC_G7_LBIN2 * KGM2_PER_LBIN2
    drag_scale = (math.pi / 8.0) * RHO_KGM3 * g7_cd(mach) * speed_mps / bc_kgm2

    acc_mps2 = np.array([0.0, -G_MPS2, 0.0]) - drag_scale * v_air_mps

    if omega_radps is not None:
        acc_mps2 = acc_mps2 - 2.0 * np.cross(omega_radps, vel_mps)

    return acc_mps2


def earth_rotation_vector() -> np.ndarray:
    """Earth's angular velocity resolved into the course's line-of-sight frame.

    In the frame of docs/units-and-conventions.md s.4 -- +x downrange along the
    line of sight, +y up, +z to the shooter's right -- with the rifle pointed at
    azimuth psi clockwise from true north at latitude phi:

        Omega_x =  Omega cos(phi) cos(psi)
        Omega_y =  Omega sin(phi)
        Omega_z = -Omega cos(phi) sin(psi)

    Module 23 derives this and checks both hemispheres.
    """
    phi_rad = math.radians(LATITUDE_DEG)
    psi_rad = math.radians(AZIMUTH_DEG)
    return OMEGA_EARTH_RADPS * np.array([
        math.cos(phi_rad) * math.cos(psi_rad),
        math.sin(phi_rad),
        -math.cos(phi_rad) * math.sin(psi_rad),
    ])


def integrate(
    launch_angle_rad: float,
    max_range_m: float,
    *,
    wind_mps: np.ndarray | None = None,
    coriolis: bool = False,
    dt_s: float = DT_S,
) -> dict[str, np.ndarray]:
    """Fly the bullet with classical RK4 and return the sampled path.

    The origin is the muzzle and +x runs downrange along the line of sight, so
    the bullet starts one sight-height *below* the line of sight and is launched
    at ``launch_angle_rad`` above it.

    Returns:
        Dict of arrays: ``x_m``, ``y_m``, ``z_m``, ``t_s``.
    """
    wind = np.zeros(3) if wind_mps is None else wind_mps
    omega = earth_rotation_vector() if coriolis else None

    mv_mps = MV_FPS * MPS_PER_FPS
    pos_m = np.array([0.0, -SIGHT_HEIGHT_IN * M_PER_IN, 0.0])
    vel_mps = mv_mps * np.array([math.cos(launch_angle_rad), math.sin(launch_angle_rad), 0.0])

    xs, ys, zs, ts = [pos_m[0]], [pos_m[1]], [pos_m[2]], [0.0]
    t_s = 0.0

    while pos_m[0] < max_range_m:
        k1v = _accel(vel_mps, wind, omega)
        k2v = _accel(vel_mps + 0.5 * dt_s * k1v, wind, omega)
        k3v = _accel(vel_mps + 0.5 * dt_s * k2v, wind, omega)
        k4v = _accel(vel_mps + dt_s * k3v, wind, omega)

        k1p, k2p = vel_mps, vel_mps + 0.5 * dt_s * k1v
        k3p, k4p = vel_mps + 0.5 * dt_s * k2v, vel_mps + dt_s * k3v

        pos_m = pos_m + (dt_s / 6.0) * (k1p + 2.0 * k2p + 2.0 * k3p + k4p)
        vel_mps = vel_mps + (dt_s / 6.0) * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)
        t_s += dt_s

        xs.append(pos_m[0])
        ys.append(pos_m[1])
        zs.append(pos_m[2])
        ts.append(t_s)

    return {
        "x_m": np.array(xs),
        "y_m": np.array(ys),
        "z_m": np.array(zs),
        "t_s": np.array(ts),
    }


def sample(path: dict[str, np.ndarray], ranges_m: np.ndarray) -> dict[str, np.ndarray]:
    """Interpolate a flown path onto the requested downrange distances."""
    return {
        key: np.interp(ranges_m, path["x_m"], path[key])
        for key in ("y_m", "z_m", "t_s")
    }


def solve_zero_angle_rad(zero_range_m: float) -> float:
    """Find the launch angle that puts the bullet on the line of sight at the zero.

    Plain secant iteration on the miss distance. Module 16 does this properly,
    with a bracketing root-finder and an event-based crossing.
    """
    lo_rad, hi_rad = 0.0, math.radians(1.0)

    def miss_m(angle_rad: float) -> float:
        path = integrate(angle_rad, zero_range_m + 1.0)
        return float(np.interp(zero_range_m, path["x_m"], path["y_m"]))

    f_lo = miss_m(lo_rad)
    for _ in range(60):
        mid_rad = 0.5 * (lo_rad + hi_rad)
        f_mid = miss_m(mid_rad)
        if abs(f_mid) < 1e-9:
            return mid_rad
        if (f_lo < 0.0) == (f_mid < 0.0):
            lo_rad, f_lo = mid_rad, f_mid
        else:
            hi_rad = mid_rad
    return 0.5 * (lo_rad + hi_rad)


# --- Assembling the table ---------------------------------------------------


def build_table() -> tuple[dict[str, np.ndarray], dict[str, float]]:
    """Compute every effect at every range, by isolating one effect at a time.

    Each effect is the *difference* between a run with it and the baseline run
    without it. That is the only honest way to attribute a displacement when the
    effects are not independent -- Coriolis changes the time of flight, which
    changes the drop -- and it is the same decomposition Module 29 performs.
    """
    ranges_m = RANGES_YD * M_PER_YD
    max_range_m = float(ranges_m[-1]) + 5.0

    zero_angle_rad = solve_zero_angle_rad(ZERO_YD * M_PER_YD)

    baseline = sample(integrate(zero_angle_rad, max_range_m), ranges_m)

    wind_mps = np.array([0.0, 0.0, -CROSSWIND_MPH * MPS_PER_MPH])
    windy = sample(integrate(zero_angle_rad, max_range_m, wind_mps=wind_mps), ranges_m)

    spun = sample(integrate(zero_angle_rad, max_range_m, coriolis=True), ranges_m)

    sg = miller_sg()
    tof_s = baseline["t_s"]

    # Every other column below is a displacement from where the bullet would
    # have gone *without* that effect, so drop is measured the same way: below
    # the extended line of departure, which is where the bullet would keep going
    # if gravity switched off. That is the effect of gravity. Where the bullet
    # sits relative to your line of sight is a different question -- it depends
    # on the zero -- and it gets its own column.
    departure_line_m = -SIGHT_HEIGHT_IN * M_PER_IN + ranges_m * math.tan(zero_angle_rad)
    drop_in = (baseline["y_m"] - departure_line_m) / M_PER_IN
    path_in = baseline["y_m"] / M_PER_IN
    wind_in = (windy["z_m"] - baseline["z_m"]) / M_PER_IN
    spin_in = spin_drift_in(tof_s, sg)
    jump_in = (
        aero_jump_moa_per_mph(sg) * CROSSWIND_MPH * RAD_PER_MOA * ranges_m
    ) / M_PER_IN
    cor_h_in = (spun["z_m"] - baseline["z_m"]) / M_PER_IN
    cor_v_in = (spun["y_m"] - baseline["y_m"]) / M_PER_IN

    table = {
        "range_yd": RANGES_YD,
        "tof_s": tof_s,
        "drop_in": drop_in,
        "path_in": path_in,
        "wind_10mph_in": wind_in,
        "spin_drift_in": spin_in,
        "aero_jump_in": jump_in,
        "coriolis_horiz_in": cor_h_in,
        "coriolis_vert_in": cor_v_in,
    }
    meta = {"sg": sg, "zero_angle_moa": zero_angle_rad / RAD_PER_MOA}
    return table, meta


HEADER = """\
# effect_magnitudes.csv -- the six effects a ballistic solver models, ranked.
#
# SYNTHETIC: MODEL OUTPUT, NOT MEASUREMENT. Nothing here was fired.
# Generated {on} by generate_effect_magnitudes.py, in this directory --
# a standalone reference implementation that imports nothing from
# src/ballistics/ and is deliberately NOT the library this course builds.
# Module 17 regenerates this table from the reader's own solver and diffs it.
#
# Load: 6.5 Creedmoor, 140 gr Berger Hybrid Target, G7 BC {bc} lb/in^2,
#       {mv} fps muzzle velocity, 1:{twist} right-hand twist,
#       {sight} in sight height, {zero} yd zero ({zero_moa:.2f} MOA of launch angle).
# Atmosphere: ICAO standard, sea level (1.225 kg/m^3, 59 degF, 29.92 inHg).
# Wind: {wind} mph full-value crosswind from 3 o'clock (blowing right to left).
# Earth: latitude {lat} deg N, firing azimuth {az} deg (northeast).
# Gyroscopic stability (Miller): Sg = {sg:.2f}
#
# Two different vertical questions, two columns:
#   drop_in  -- how far gravity pulled the bullet below the extended line of
#               departure. This is the EFFECT of gravity, measured the same way
#               every other column is measured: displacement from where the
#               bullet would have gone without it. Independent of the zero.
#   path_in  -- where the bullet actually is relative to your line of sight,
#               given the {zero} yd zero. This is what you dial. It is zero at
#               the zero range by definition.
#
# Signs follow docs/units-and-conventions.md s.4: +y up, +z to the shooter's
# right. So drop_in and path_in are negative (below), wind_10mph_in is negative
# (a 3 o'clock wind pushes left), spin_drift_in is positive (right-hand twist
# drifts right), and aero_jump_in is positive (a 3 o'clock wind on a right-hand
# twist jumps the bullet UP).
#
# EMPIRICAL FITS, NOT PHYSICS -- three columns are curve fits imported from
# higher-fidelity work, because a point-mass model cannot produce them:
#   spin_drift_in  -- Litz, Applied Ballistics: 1.25 (Sg + 1.2) T^1.83
#   aero_jump_in   -- Litz, Applied Ballistics: 0.01 Sg - 0.0024 L + 0.032 MOA/mph
#   (both depend on Sg from Miller's rule, itself an empirical fit)
# drop, wind deflection, and Coriolis are integrated from the equations of
# motion. Modules 20, 21, and 22 treat the fits properly.
"""


def main() -> None:
    table, meta = build_table()

    header = HEADER.format(
        on=GENERATED_ON,
        bc=BC_G7_LBIN2,
        mv=int(MV_FPS),
        twist=int(TWIST_IN),
        sight=SIGHT_HEIGHT_IN,
        zero=int(ZERO_YD),
        zero_moa=meta["zero_angle_moa"],
        wind=int(CROSSWIND_MPH),
        lat=int(LATITUDE_DEG),
        az=int(AZIMUTH_DEG),
        sg=meta["sg"],
    )

    columns = list(table)
    lines = [header + ",".join(columns)]
    for i in range(len(RANGES_YD)):
        row = []
        for name in columns:
            value = float(table[name][i])
            row.append(f"{value:.0f}" if name == "range_yd" else f"{value:.3f}")
        lines.append(",".join(row))

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(Path(__file__).resolve().parents[3])}")

    # Anchors. These are published, widely-reproduced figures for this class of
    # load; if the generator wanders away from them, the generator is wrong.
    print(f"\n  Sg (Miller)   {meta['sg']:.2f}       published ~1.7-1.9 for this load")
    print(f"  launch angle  {meta['zero_angle_moa']:.2f} MOA")
    for yd in (500.0, 1000.0):
        i = int(np.where(RANGES_YD == yd)[0][0])
        path = table["path_in"][i]
        print(
            f"  {int(yd):>4} yd  ToF {table['tof_s'][i]:.3f} s   "
            f"come-up {abs(path) / (0.036 * yd):4.2f} mil   "
            f"wind {abs(table['wind_10mph_in'][i]):5.1f} in   "
            f"spin {table['spin_drift_in'][i]:5.1f} in"
        )
    print("\n  Published anchors for this load, 100 yd zero, sea level:")
    print("    1000 yd come-up  8.8-9.2 mil (~30 MOA)")
    print("    1000 yd velocity ~1450 fps")
    print("    1000 yd wind     ~70 in for 10 mph full value")
    print("    1000 yd spin     ~8-9 in (docs/glossary.md)")
    print("  If the generator wanders off these, the generator is wrong.")


if __name__ == "__main__":
    main()

"""Module 01: the conversion layer every later module depends on.

Three things are being protected here, and they are different in kind.

**Round-trip identity.** Converting out of SI and back must return the input to
machine precision. This catches a transposed factor, a divide that should be a
multiply, and a copy-paste between neighbouring pairs -- which, in a file of
thirty near-identical functions, is the realistic failure mode.

**Exactness.** Where a factor is exact by definition, the test asserts bit
equality, not approximate equality. That is a real claim about the code -- it
fails if someone rewrites ``M_PER_FOOT`` as ``12 * M_PER_INCH`` -- and the one
place it does *not* hold (the grain, whose exact decimal is not exactly a
double) is asserted separately with a comment saying why.

**Known values.** Numbers a reader can check against a bullet box or a weather
meter. Two of them are traps and are marked as such.
"""

from __future__ import annotations

import math

import pytest

from ballistics.constants import (
    G0_MPS2,
    ICAO_SEA_LEVEL,
    KG_PER_GRAIN,
    KG_PER_POUND,
    M_PER_FOOT,
    M_PER_INCH,
    M_PER_YARD,
    MPS_PER_MPH,
)
from ballistics.units import (
    c_to_k,
    deg_to_rad,
    f_to_k,
    feet_to_m,
    fps_to_mps,
    ftlb_to_j,
    grains_to_kg,
    hpa_to_pa,
    inches_to_m,
    inhg_to_pa,
    j_to_ftlb,
    k_to_c,
    k_to_f,
    kg_to_grains,
    kt_to_mps,
    m_to_feet,
    m_to_inches,
    m_to_yards,
    mil_to_rad,
    moa_to_rad,
    mph_to_mps,
    mps_to_fps,
    mps_to_kt,
    mps_to_mph,
    pa_to_hpa,
    pa_to_inhg,
    rad_to_deg,
    rad_to_mil,
    rad_to_moa,
    rad_to_smoa,
    smoa_to_rad,
    yards_to_m,
)

#: Every conversion pair in the library, with a value in a realistic range for
#: the quantity. Adding a pair to units.py without adding it here should feel
#: like an omission, so the list is exhaustive on purpose.
PAIRS = [
    ("mass gr/kg", grains_to_kg, kg_to_grains, 140.0),
    ("velocity fps/mps", fps_to_mps, mps_to_fps, 2700.0),
    ("length yd/m", yards_to_m, m_to_yards, 1000.0),
    ("length in/m", inches_to_m, m_to_inches, 1.75),
    ("length ft/m", feet_to_m, m_to_feet, 5000.0),
    ("pressure inHg/Pa", inhg_to_pa, pa_to_inhg, 29.9213),
    ("pressure hPa/Pa", hpa_to_pa, pa_to_hpa, 1013.25),
    ("temperature F/K", f_to_k, k_to_f, 59.0),
    ("temperature C/K", c_to_k, k_to_c, 15.0),
    ("energy ftlb/J", ftlb_to_j, j_to_ftlb, 2265.8),
    ("wind mph/mps", mph_to_mps, mps_to_mph, 10.0),
    ("wind kt/mps", kt_to_mps, mps_to_kt, 8.7),
    ("angle deg/rad", deg_to_rad, rad_to_deg, 1.5),
    ("angle MOA/rad", moa_to_rad, rad_to_moa, 31.0),
    ("angle SMOA/rad", smoa_to_rad, rad_to_smoa, 31.0),
    ("angle mil/rad", mil_to_rad, rad_to_mil, 9.1),
]


# --- Round trips ------------------------------------------------------------


@pytest.mark.parametrize(("name", "to_si", "from_si", "value"), PAIRS, ids=[p[0] for p in PAIRS])
def test_round_trip_returns_the_input(name, to_si, from_si, value, tolerances):
    assert from_si(to_si(value)) == pytest.approx(value, rel=tolerances["unit_roundtrip"])


@pytest.mark.parametrize(("name", "to_si", "from_si", "value"), PAIRS, ids=[p[0] for p in PAIRS])
def test_round_trip_holds_at_zero(name, to_si, from_si, value, tolerances):
    # Catches an offset applied in one direction only -- the failure mode the
    # affine temperature conversions are exposed to and the scale ones are not.
    assert from_si(to_si(0.0)) == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize(("name", "to_si", "from_si", "value"), PAIRS, ids=[p[0] for p in PAIRS])
def test_conversions_are_monotonic(name, to_si, from_si, value):
    # A sign error survives a round trip; it does not survive this.
    assert to_si(value) < to_si(value + 1.0)


# --- Exactness --------------------------------------------------------------
# These assert bit equality, not approximate equality. That is the point.


def test_length_factors_are_exact_by_definition():
    # 1959 international yard and pound agreement.
    assert inches_to_m(1.0) == 0.0254
    assert feet_to_m(1.0) == 0.3048
    assert yards_to_m(1.0) == 0.9144


def test_length_factors_agree_with_each_other_to_within_one_ulp():
    # Three feet is a yard, exactly, in the world. It is *not* exactly a yard
    # in float64: 3 * 0.3048 is 0.9144000000000001, one unit in the last place
    # above 0.9144. Nothing is wrong with the constants -- each is the nearest
    # double to its exact decimal -- but the arithmetic between them rounds.
    #
    # The honest claim, and the one worth protecting, is that the disagreement
    # stays at the last bit. If a future edit derives one factor from another
    # (12 * M_PER_INCH is 0.30479999999999996, a full ULP low before the
    # multiply even starts) the error grows and this catches it.
    assert abs(feet_to_m(3.0) - yards_to_m(1.0)) <= math.ulp(0.9144)
    assert abs(inches_to_m(36.0) - yards_to_m(1.0)) <= math.ulp(0.9144)
    assert abs(inches_to_m(12.0) - feet_to_m(1.0)) <= math.ulp(0.3048)


def test_a_metre_of_disagreement_is_never_a_metre_of_bullet():
    # Scale check on the paragraph above, so nobody mistakes it for a problem.
    # One ULP at 1000 yards is under a nanometre. The bullet is 6.7 mm across.
    one_ulp_m = math.ulp(yards_to_m(1000.0))
    assert one_ulp_m < 1e-9


def test_the_grain_is_exact_in_decimal_but_not_in_binary():
    # 1 lb = 7000 gr and 1 lb = 0.45359237 kg, both exact, so 1 gr is exactly
    # 64.79891 mg -- in decimal. In binary, the nearest double to 6.479891e-5
    # and the quotient 0.45359237/7000 are one ULP apart. constants.py takes
    # the literal, so this is approx and not ==, and the module says why.
    assert grains_to_kg(7000.0) == pytest.approx(KG_PER_POUND, rel=1e-15)
    assert KG_PER_GRAIN == 6.479891e-05


def test_speed_and_pressure_factors_are_exact():
    assert fps_to_mps(1.0) == 0.3048
    assert mph_to_mps(1.0) == 0.44704
    assert hpa_to_pa(1.0) == 100.0
    # A knot is 1852 m/h exactly, but 1852/3600 has no exact decimal form and
    # so no exact double: 3600 knots round-trips to 1852.0000000000002.
    assert kt_to_mps(3600.0) == pytest.approx(1852.0, rel=1e-15)


def test_a_temperature_difference_is_not_a_temperature():
    # The affine trap. 10 degF of powder-temperature spread is 5.6 K, and
    # f_to_k(10.0) is not the answer to that question.
    assert f_to_k(10.0) == pytest.approx(260.928, abs=1e-3)
    difference_k = f_to_k(70.0) - f_to_k(60.0)
    assert difference_k == pytest.approx(5.5556, abs=1e-4)


# --- Known values -----------------------------------------------------------


def test_the_running_loads_muzzle_velocity(primary_load):
    # 2700 fps is the course's running load. Exact, because the foot is.
    assert fps_to_mps(primary_load["mv_fps"]) == 822.96


def test_the_running_loads_bullet_mass(primary_load):
    # 9.0718 g. NOT 9.0720 g -- that is what a rounded 64.8 mg per grain gives,
    # and it is wrong in the fifth significant figure.
    mass_g = grains_to_kg(primary_load["mass_gr"]) * 1000.0
    assert mass_g == pytest.approx(9.0718474, abs=1e-7)
    assert mass_g != pytest.approx(9.0720, abs=1e-5)


def test_standard_pressure_in_inches_of_mercury():
    # 29.9213 inHg is standard sea level to within 0.2 Pa. The commonly quoted
    # 29.92 is 4.2 Pa short, which is too loose to catch a real conversion bug.
    assert inhg_to_pa(29.9213) == pytest.approx(101325.0, abs=0.2)
    assert pa_to_inhg(101325.0) == pytest.approx(29.9213, abs=1e-4)
    assert abs(inhg_to_pa(29.92) - 101325.0) > 4.0


def test_standard_temperature_in_fahrenheit():
    assert f_to_k(59.0) == 288.15          # exact in binary; 27 * 5/9 is 15.0
    assert k_to_f(288.15) == pytest.approx(59.0, abs=1e-12)
    assert c_to_k(15.0) == 288.15


def test_one_moa_in_radians():
    assert moa_to_rad(1.0) == pytest.approx(2.908882e-4, rel=1e-6)
    assert mil_to_rad(1.0) == 1.0e-3


def test_moa_over_smoa_is_exactly_pi_over_three():
    # The module's headline fact, and the reason 1 MOA subtends 1.047 inches at
    # 100 yards rather than 1.000.
    assert moa_to_rad(1.0) / smoa_to_rad(1.0) == pytest.approx(math.pi / 3.0, rel=1e-15)


def test_confusing_moa_with_smoa_costs_fifteen_inches_at_a_thousand():
    # Stated in plain English because this is the mistake the module exists to
    # prevent, in the direction it actually happens: an app or a reticle chart
    # reports the come-up in SMOA/IPHY, and it gets dialled on a true-MOA
    # turret. Same number, bigger unit, so the shot goes high.
    #
    # The running load needs 326.229 in of come-up at 1000 yd (Module 00's
    # reference table), which is 32.6 SMOA or 31.1 MOA.
    range_m = yards_to_m(1000.0)
    comeup_rad = math.atan(inches_to_m(326.229) / range_m)
    dialled_smoa = rad_to_smoa(comeup_rad)
    assert dialled_smoa == pytest.approx(32.6, abs=0.1)

    over_m = range_m * (math.tan(moa_to_rad(dialled_smoa)) - math.tan(comeup_rad))
    assert m_to_inches(over_m) == pytest.approx(15.4, abs=0.1)


def test_the_muzzle_energy_of_the_running_load(primary_load):
    # Not library code -- M06 owns energy.py. This checks that the lesson's
    # worked example is reproducible from the conversions, and that it lands on
    # the ~2266 ft-lb a 6.5 Creedmoor box quotes.
    mass_kg = grains_to_kg(primary_load["mass_gr"])
    velocity_mps = fps_to_mps(primary_load["mv_fps"])
    energy_j = 0.5 * mass_kg * velocity_mps**2
    assert energy_j == pytest.approx(3072.0, abs=0.1)
    assert j_to_ftlb(energy_j) == pytest.approx(2265.8, abs=0.1)


def test_the_reloading_manual_constant_encodes_a_stale_gravity(primary_load):
    # E_ftlb = m_gr * v_fps^2 / 450240 is in every manual. Derived honestly the
    # divisor is 2 * 7000 * g in ft/s^2, and standard gravity gives 450436.7.
    # The published 450240 implies g = 32.16, so it reads about 0.04% high.
    divisor = 2 * 7000 * m_to_feet(G0_MPS2)
    assert divisor == pytest.approx(450436.7, abs=0.1)

    manual_ftlb = primary_load["mass_gr"] * primary_load["mv_fps"] ** 2 / 450240
    honest_ftlb = primary_load["mass_gr"] * primary_load["mv_fps"] ** 2 / divisor
    assert manual_ftlb == pytest.approx(2266.8, abs=0.1)
    assert honest_ftlb == pytest.approx(2265.8, abs=0.1)
    assert manual_ftlb / honest_ftlb - 1.0 == pytest.approx(4.4e-4, rel=0.05)


# --- The shared reference conditions ----------------------------------------


def test_icao_sea_level_matches_the_test_suites_fixture(icao_sea_level):
    # constants.ICAO_SEA_LEVEL and the conftest fixture describe the same
    # atmosphere. Twenty-eight modules is a long time for them to drift apart.
    assert dict(ICAO_SEA_LEVEL) == icao_sea_level


def test_icao_sea_level_is_read_only():
    with pytest.raises(TypeError):
        ICAO_SEA_LEVEL["pressure_pa"] = 0.0


def test_icao_sea_level_converts_to_the_values_a_weather_meter_shows():
    assert pa_to_inhg(ICAO_SEA_LEVEL["pressure_pa"]) == pytest.approx(29.9213, abs=1e-4)
    assert k_to_f(ICAO_SEA_LEVEL["temp_k"]) == pytest.approx(59.0, abs=1e-9)


def test_every_conversion_constant_is_positive():
    for value in (M_PER_INCH, M_PER_FOOT, M_PER_YARD, MPS_PER_MPH, KG_PER_GRAIN, G0_MPS2):
        assert value > 0.0

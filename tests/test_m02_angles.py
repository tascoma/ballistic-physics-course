"""Module 02: the geometry that turns an angle into inches on a target.

Four kinds of claim are protected here, and they fail in different ways.

**Known values.** The three numbers a shooter can check against a scope box:
one MOA is 1.0472 inches at 100 yards, one SMOA is 1.0000, one mil is 3.6000.
If any of these moves, a conversion factor upstream in Module 01 moved.

**The exactness trap.** "1 mil is 10 cm at 100 m" is exact in the *linear*
form and not exact under ``tan``. The test asserts the tangent value and then
asserts the size of the gap, because a test that demanded ``== 0.1`` would
encode the very approximation this module exists to quantify. This is the one
test in the file that would still pass if the code were wrong in the way the
lesson warns about, so it is written to fail loudly instead.

**Round trips.** ``angle_for_offset_rad`` and ``subtension_m`` are inverses,
and ``angle_for_clicks`` and ``clicks_for_angle`` are inverses. Round trips
catch a transposed argument, which is the realistic failure mode for a
two-argument function whose arguments are both floats.

**Propagation structure.** The ranging error is a quadrature sum, and the two
properties that makes true -- a lone relative error passes through unchanged,
and two errors combine to less than their sum -- are asserted as properties
rather than as numbers, so they keep their meaning if the example changes.
"""

from __future__ import annotations

import math

import pytest

from ballistics.angles import (
    CLICK_RAD,
    angle_for_clicks,
    angle_for_offset_rad,
    clicks_for_angle,
    mil_ranging_error_m,
    mil_ranging_m,
    moa_subtension_in,
    smoa_subtension_in,
    subtension_m,
)
from ballistics.constants import (
    M_PER_INCH,
    M_PER_YARD,
    RAD_PER_MIL,
    RAD_PER_MOA,
    RAD_PER_SMOA,
)
from ballistics.units import inches_to_m, m_to_yards, mil_to_rad, moa_to_rad

HUNDRED_YD_M = 100.0 * M_PER_YARD


# --- Known values a reader can check against a scope box --------------------


def test_one_moa_at_100_yards_is_1_0472_inches():
    """A true MOA subtends 1.0472 in at 100 yd -- famously *not* one inch."""
    assert moa_subtension_in(100.0) == pytest.approx(1.0471976, abs=5e-8)


def test_one_smoa_at_100_yards_is_one_inch_by_definition():
    """SMOA is defined as an inch per hundred yards, so this is the definition."""
    assert smoa_subtension_in(100.0) == pytest.approx(1.0, abs=5e-8)


def test_one_mil_at_100_yards_is_3_6_inches():
    """The 3.6 in figure, exact to seven places under tan."""
    subtended_in = subtension_m(RAD_PER_MIL, HUNDRED_YD_M) / M_PER_INCH
    assert subtended_in == pytest.approx(3.6000012, abs=5e-8)


def test_moa_is_larger_than_smoa_by_pi_over_three():
    """MOA/SMOA is exactly pi/3 as *angles*, and very slightly more as subtensions.

    Module 01 proved the ratio of the two units is exactly pi/3. The ratio of
    what they *subtend* is the ratio of their tangents, which is larger by
    2.5 parts in a billion. Both are asserted, because the gap between them is
    precisely the distinction this module exists to make -- and it is nine
    orders of magnitude below anything a shooter can measure.
    """
    assert RAD_PER_MOA / RAD_PER_SMOA == pytest.approx(math.pi / 3.0, rel=1e-15)

    subtension_ratio = moa_subtension_in(100.0) / smoa_subtension_in(100.0)
    assert subtension_ratio == pytest.approx(math.pi / 3.0, rel=1e-8)
    assert subtension_ratio > math.pi / 3.0


# --- The exactness trap -----------------------------------------------------


def test_one_mil_at_100_m_is_not_exactly_10_cm():
    """"1 mil = 10 cm at 100 m" is exact in the linear form only.

    ``subtension_m`` uses tan, so it returns 0.10000003333 m. The gap is the
    small-angle error, and this module is about knowing it is there. Asserting
    equality with 0.1 here would bake the approximation into the test suite.
    """
    exact_m = subtension_m(RAD_PER_MIL, 100.0)
    linear_m = 100.0 * RAD_PER_MIL

    assert linear_m == 0.1
    assert exact_m != 0.1
    assert exact_m == pytest.approx(0.10000003333334667, abs=1e-17)

    # theta**3/3 is the leading term of tan(theta) - theta.
    gap_m = exact_m - linear_m
    assert gap_m == pytest.approx(RAD_PER_MIL**3 / 3.0 * 100.0, rel=1e-6)
    assert gap_m == pytest.approx(3.333e-8, rel=1e-3)


@pytest.mark.parametrize("angle_rad", [1e-3, 1e-2, 1e-1])
def test_small_angle_relative_error_follows_theta_squared_over_three(angle_rad):
    """The relative error of the linear form is theta**2/3, over three decades.

    The next term of tan is 2*theta**5/15, so the theta**2/3 prediction is
    itself short by a relative 2*theta**2/5. Asserting that law rather than a
    flat tolerance means the test states the actual mathematics: the prediction
    improves quadratically as the angle shrinks, which is why it is exact
    enough to ignore at the angles a rifle dials and useless at 45 degrees.
    """
    relative = (math.tan(angle_rad) - angle_rad) / angle_rad
    predicted = angle_rad**2 / 3.0

    assert relative > predicted
    assert abs(relative - predicted) / predicted == pytest.approx(
        0.4 * angle_rad**2, rel=5e-3
    )


def test_small_angle_law_cannot_be_checked_below_a_milliradian():
    """Below ~1 mrad, floating point runs out before the mathematics does.

    ``tan(theta) - theta`` is catastrophic cancellation: at theta = 1e-4 the
    difference is 3.3e-13 while the operands are 1e-4, so roughly seven of a
    double's sixteen digits survive. The theta**2/3 prediction still holds to
    six figures, but the 2*theta**2/5 *correction* to it needs the ninth, which
    is gone. This is Module 01's rounding lesson showing up as a hard limit on
    what a test can assert, so the assertion here is deliberately the weaker one.
    """
    angle_rad = 1e-4
    relative = (math.tan(angle_rad) - angle_rad) / angle_rad
    assert relative == pytest.approx(angle_rad**2 / 3.0, rel=1e-6)


def test_small_angle_error_at_one_and_five_degrees():
    """The two figures the lesson and Figure 01 quote: 0.0102% and 0.2546%."""
    for degrees, expected_pct in ((1.0, 0.0102), (5.0, 0.2546)):
        angle_rad = math.radians(degrees)
        relative_pct = 100.0 * (math.tan(angle_rad) - angle_rad) / angle_rad
        assert relative_pct == pytest.approx(expected_pct, abs=5e-5)


# --- Round trips ------------------------------------------------------------


@pytest.mark.parametrize("range_m", [1.0, HUNDRED_YD_M, 914.4, 2000.0])
@pytest.mark.parametrize("angle_rad", [-0.05, -1e-4, 0.0, 1e-4, 0.05, 0.3])
def test_angle_offset_round_trip(angle_rad, range_m, tolerances):
    """subtension then angle_for_offset returns the angle, to machine precision."""
    offset_m = subtension_m(angle_rad, range_m)
    assert angle_for_offset_rad(offset_m, range_m) == pytest.approx(
        angle_rad, abs=tolerances["angle_rad"]
    )


def test_negative_offset_is_a_negative_angle():
    """An impact 15 in low at 600 yd is a *negative* angle -- a down correction.

    Stated in plain English because sign conventions are where this course's
    errors hide: +y is up, so below the line of sight is negative, and the
    angle must carry that sign through unchanged.
    """
    low_m = inches_to_m(-15.0)
    angle_rad = angle_for_offset_rad(low_m, 600.0 * M_PER_YARD)
    assert angle_rad < 0.0
    assert angle_rad / RAD_PER_MOA == pytest.approx(-2.3873, abs=1e-4)


def test_angle_for_offset_at_zero_range_is_a_right_angle():
    """atan2, not division: zero range returns pi/2 rather than raising."""
    assert angle_for_offset_rad(0.1, 0.0) == pytest.approx(math.pi / 2.0)


def test_subtension_is_linear_in_range():
    """Doubling the range doubles the subtension, exactly. Hence a constant ratio."""
    angle_rad = moa_to_rad(1.0)
    assert subtension_m(angle_rad, 800.0) == pytest.approx(
        2.0 * subtension_m(angle_rad, 400.0), rel=1e-12
    )


# --- Reticle ranging --------------------------------------------------------


def test_mil_ranging_against_hand_computed_value():
    """A 40 in target subtending 1.4 mil is at 725.7 m (793.7 yd).

    Hand check: 40 in = 1.016 m; 1.4 mil = 0.0014 rad; 1.016 / 0.0014 = 725.71 m.
    """
    range_m = mil_ranging_m(inches_to_m(40.0), 1.4)
    assert range_m == pytest.approx(725.714, abs=1e-3)
    assert m_to_yards(range_m) == pytest.approx(793.65, abs=1e-2)


def test_mil_ranging_inverts_the_linear_subtension():
    """Ranging is the linear form run backwards, so it round-trips with it."""
    target_size_m = 1.0
    range_m = 800.0
    mils = target_size_m / (range_m * RAD_PER_MIL)
    assert mil_ranging_m(target_size_m, mils) == pytest.approx(range_m, rel=1e-12)


@pytest.mark.parametrize(
    ("target_size_m", "mils"),
    [(1.0, 0.0), (1.0, -1.4), (0.0, 1.4), (-1.0, 1.4)],
)
def test_mil_ranging_rejects_nonpositive_inputs(target_size_m, mils):
    with pytest.raises(ValueError):
        mil_ranging_m(target_size_m, mils)


# --- Error propagation ------------------------------------------------------


def test_ten_percent_size_error_alone_is_a_ten_percent_range_error():
    """Proportional, at every range. This is why a better scope does not help."""
    target_size_m = 1.0
    for mils in (0.8, 1.4, 4.0):
        range_m = mil_ranging_m(target_size_m, mils)
        error_m = mil_ranging_error_m(target_size_m, 0.10 * target_size_m, mils, 0.0)
        assert error_m / range_m == pytest.approx(0.10, rel=1e-12)


def test_errors_combine_in_quadrature_not_linearly():
    """Two 10% errors give 14.1%, not 20%. The larger term swallows the smaller."""
    both = mil_ranging_error_m(1.0, 0.10, 1.0, 0.10)
    one = mil_ranging_error_m(1.0, 0.10, 1.0, 0.0)
    other = mil_ranging_error_m(1.0, 0.0, 1.0, 0.10)

    assert both > one
    assert both < one + other
    assert both / mil_ranging_m(1.0, 1.0) == pytest.approx(math.sqrt(0.02), rel=1e-12)


def test_worked_example_uncertainty():
    """The lesson's worked example: 10% size guess, 0.05 mil read -> 10.62%, +-84 yd."""
    target_size_m = inches_to_m(40.0)
    range_m = mil_ranging_m(target_size_m, 1.4)
    error_m = mil_ranging_error_m(target_size_m, 0.10 * target_size_m, 1.4, 0.05)

    assert error_m / range_m == pytest.approx(0.1062, abs=5e-5)
    assert m_to_yards(error_m) == pytest.approx(84.3, abs=0.05)


def test_ranging_error_rejects_negative_uncertainties():
    with pytest.raises(ValueError):
        mil_ranging_error_m(1.0, -0.1, 1.4, 0.0)
    with pytest.raises(ValueError):
        mil_ranging_error_m(1.0, 0.1, 1.4, -0.05)


# --- Turret clicks ----------------------------------------------------------


def test_click_round_trip(tolerances):
    angle_rad = moa_to_rad(31.15)
    for click_rad in CLICK_RAD.values():
        clicks = clicks_for_angle(angle_rad, click_rad)
        assert angle_for_clicks(clicks, click_rad) == pytest.approx(
            angle_rad, abs=tolerances["angle_rad"]
        )


def test_tenth_mil_click_is_coarser_than_a_quarter_moa_click():
    """The lesson's headline: the mil click is 37.5% *bigger*, not finer.

    Stated in plain English because it is the claim the original spec got
    backwards: one tenth-mil detent moves the reticle further than one
    quarter-MOA detent, so a quarter-MOA turret has the finer resolution.
    """
    ratio = CLICK_RAD["tenth_mil"] / CLICK_RAD["quarter_moa"]
    assert ratio > 1.0
    assert ratio == pytest.approx(4.32 / math.pi, rel=1e-12)
    assert ratio == pytest.approx(1.3751, abs=5e-5)


def test_click_ratio_does_not_change_with_range():
    """Two angular units have a constant ratio -- they never converge or separate."""
    ratios = [
        subtension_m(CLICK_RAD["tenth_mil"], r) / subtension_m(CLICK_RAD["quarter_moa"], r)
        for r in (HUNDRED_YD_M, 5.0 * HUNDRED_YD_M, 10.0 * HUNDRED_YD_M)
    ]
    assert ratios[0] == pytest.approx(ratios[1], rel=1e-9)
    assert ratios[1] == pytest.approx(ratios[2], rel=1e-9)


def test_thousand_yard_comeup_click_counts():
    """The running load's 1000 yd come-up: 124.6 quarter-MOA or 90.6 tenth-mil clicks.

    Come-up is from Module 00's effect_magnitudes.csv (path -326.229 in at
    1000 yd), which is model output, not measurement.
    """
    range_m = 1000.0 * M_PER_YARD
    comeup_rad = angle_for_offset_rad(inches_to_m(326.229), range_m)

    assert comeup_rad / RAD_PER_MOA == pytest.approx(31.15, abs=5e-3)
    assert clicks_for_angle(comeup_rad, CLICK_RAD["quarter_moa"]) == pytest.approx(
        124.6, abs=0.05
    )
    assert clicks_for_angle(comeup_rad, CLICK_RAD["tenth_mil"]) == pytest.approx(90.6, abs=0.05)


def test_half_click_residual_at_1000_yards():
    """Worst-case rounding residual is half a click: 1.31 in (MOA) / 1.80 in (mil)."""
    range_m = 1000.0 * M_PER_YARD
    for name, expected_in in (("quarter_moa", 1.31), ("tenth_mil", 1.80)):
        half_click_rad = CLICK_RAD[name] / 2.0
        residual_in = subtension_m(half_click_rad, range_m) / M_PER_INCH
        assert residual_in == pytest.approx(expected_in, abs=5e-3)


@pytest.mark.parametrize("click_rad", [0.0, -1e-4])
def test_clicks_reject_nonpositive_click_size(click_rad):
    with pytest.raises(ValueError):
        clicks_for_angle(mil_to_rad(1.0), click_rad)
    with pytest.raises(ValueError):
        angle_for_clicks(10.0, click_rad)

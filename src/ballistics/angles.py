"""Turning angles into distances on a target, and distances back into angles.

Module 01 established what the angular *units* are -- that a MOA is
``pi/10800`` radians, that an SMOA is a different unit 4.51% smaller, that a
mil is exactly 0.001 radian. This file is the *geometry*: what those units are
worth in inches once there is a target out there, and how to run the
relationship backwards to range that target from your reticle.

The exact relationship, and the one everybody uses instead
----------------------------------------------------------
An angle ``theta`` at a range ``R`` subtends

    s = R * tan(theta)          exact
    s = R * theta               the small-angle form, theta in radians

and the second is wrong by a relative ``theta**2 / 3``. At the angles a rifle
shooter dials -- a 1000-yard come-up on the course's running load is about half
a degree -- that error is four parts in a million, which is a hundred times
smaller than your ability to hold the rifle still. The approximation is not
merely acceptable there; it is invisible.

**This file still uses ``tan`` and ``atan2`` everywhere.** Not because the
difference matters at 31 MOA, but because it costs one function call to never
have to ask. The moment an angle in this course stops being small -- a steep
incline in Module 08, a launch angle in Module 07 at artillery elevations -- the
linear form starts lying, and it lies quietly. Code that is exact by
construction cannot develop that bug later. Module 02's lesson plots exactly
where the line is, so the reader can see what is being bought.

Why ``atan2`` rather than ``atan(offset / range)``
--------------------------------------------------
They agree everywhere except at ``range_m = 0``, where the division raises and
``atan2`` returns a right angle -- which is the correct answer to "what angle
does a one-inch offset subtend at zero range". A solver that root-finds on
launch angle will evaluate that endpoint, and an exception there is a bug that
only shows up under the root finder.

Presentation helpers are the one place imperial goes in and imperial comes out
-----------------------------------------------------------------------------
``moa_subtension_in`` and ``smoa_subtension_in`` take yards and return inches.
That violates the SI-inside rule on purpose and in exactly one direction: they
exist to print the two numbers a shooter checks a scope against, and rendering
them through metres at every call site would obscure the one fact they carry.
Their names say ``_in``, they are grouped together below, and nothing else in
this file works that way.
"""

from __future__ import annotations

import math
from types import MappingProxyType

from ballistics.constants import (
    M_PER_INCH,
    M_PER_YARD,
    RAD_PER_MIL,
    RAD_PER_MOA,
    RAD_PER_SMOA,
)

# --- Subtension: an angle becomes a length on the target --------------------


def subtension_m(angle_rad: float, range_m: float) -> float:
    """Length subtended by an angle at a range. Radians and metres in, metres out.

    Exact: ``range_m * tan(angle_rad)``, not the small-angle form. A positive
    angle subtends a positive length; the sign carries through, so a negative
    angle (a left or down correction) returns a negative length.

    Args:
        angle_rad: Subtended angle, radians.
        range_m: Distance to the target, metres.

    Returns:
        Subtended length at that range, metres.
    """
    return range_m * math.tan(angle_rad)


def angle_for_offset_rad(offset_m: float, range_m: float) -> float:
    """Angle subtended by an offset at a range. Metres in, radians out.

    The inverse of :func:`subtension_m`, and the function every correction in
    this course is computed with: an impact 15 inches low at 600 yards is
    ``atan2`` of those two numbers, never their quotient.

    Uses ``atan2`` rather than ``atan(offset_m / range_m)`` so that
    ``range_m = 0`` returns a right angle instead of raising.

    Args:
        offset_m: Displacement perpendicular to the line of sight, metres.
            Positive is up or right, per ``docs/units-and-conventions.md`` s.4.
        range_m: Distance to the target, metres.

    Returns:
        Subtended angle, radians, with the sign of ``offset_m``.
    """
    return math.atan2(offset_m, range_m)


# --- Reticle ranging: the target's known size becomes a range ---------------


def mil_ranging_m(target_size_m: float, mils: float) -> float:
    """Range to a target of known size that subtends a known number of mils.

    The classic reticle formula. Because a mil is exactly 0.001 radian, this is
    ``target_size_m / (mils * 0.001)`` -- the small-angle form, deliberately.
    Reticle subtensions are read to about a tenth of a mil, which is five
    thousand times coarser than the tangent correction at these angles, so
    using ``atan`` here would be false precision dressed up as rigour.

    Args:
        target_size_m: The target's true dimension in the direction measured,
            metres. This is a *guess* in the field, and it dominates the error.
        mils: Subtension read from the reticle, in mils. Must be positive.

    Returns:
        Range to the target, metres.

    Raises:
        ValueError: If ``mils`` is not positive, or ``target_size_m`` is not
            positive. Both are user input read off a scope under time pressure,
            and a silent negative range is worse than a traceback.
    """
    if mils <= 0.0:
        raise ValueError(f"mils must be positive, got {mils}")
    if target_size_m <= 0.0:
        raise ValueError(f"target_size_m must be positive, got {target_size_m}")
    return target_size_m / (mils * RAD_PER_MIL)


def mil_ranging_error_m(
    target_size_m: float,
    target_size_err_m: float,
    mils: float,
    mils_err: float,
) -> float:
    """Standard uncertainty in a mil-ranged range, propagated from its two inputs.

    Range is a quotient, so the *relative* uncertainties add in quadrature and
    the absolute one scales with the range itself:

        u_R / R = sqrt( (u_S / S)**2 + (u_m / m)**2 )

    Two consequences the lesson draws out. A 10% error in your size guess is a
    10% error in range, at every range -- the relationship is proportional, so
    it never improves with a better scope. And because the terms add in
    quadrature, the larger one swallows the smaller: a 10% size guess combined
    with a 3.6% reading error gives 10.6%, not 13.6%.

    Args:
        target_size_m: Assumed target dimension, metres.
        target_size_err_m: Standard uncertainty in that assumption, metres.
            Non-negative.
        mils: Subtension read from the reticle, in mils. Must be positive.
        mils_err: Standard uncertainty in the reading, in mils. Non-negative.

    Returns:
        Standard uncertainty in the ranged distance, metres.

    Raises:
        ValueError: If either uncertainty is negative, or if
            :func:`mil_ranging_m` rejects the central values.
    """
    if target_size_err_m < 0.0 or mils_err < 0.0:
        raise ValueError(
            f"uncertainties must be non-negative, got "
            f"target_size_err_m={target_size_err_m}, mils_err={mils_err}"
        )
    range_m = mil_ranging_m(target_size_m, mils)
    relative = math.hypot(target_size_err_m / target_size_m, mils_err / mils)
    return range_m * relative


# --- Presentation: imperial in, imperial out. See the module docstring. -----


def moa_subtension_in(range_yd: float) -> float:
    """What one true MOA is worth, in inches, at a range in yards.

    1.0472 inches at 100 yards -- the number that is *not* one inch, and the
    reason SMOA was invented. Imperial in and imperial out; see the module
    docstring for why this one function family is allowed to be.

    Args:
        range_yd: Range, yards.

    Returns:
        Subtension of one MOA at that range, inches.
    """
    return range_yd * M_PER_YARD * math.tan(RAD_PER_MOA) / M_PER_INCH


def smoa_subtension_in(range_yd: float) -> float:
    """What one SMOA (IPHY) is worth, in inches, at a range in yards.

    1.0000 inches at 100 yards, to seven decimal places, because that is the
    definition of the unit rather than a fact about it. The residual in the
    eighth place is the tangent correction, and it is the only thing separating
    a subtension *ratio* from an angle.

    Args:
        range_yd: Range, yards.

    Returns:
        Subtension of one SMOA at that range, inches.
    """
    return range_yd * M_PER_YARD * math.tan(RAD_PER_SMOA) / M_PER_INCH


# --- Turret clicks: a correction becomes a number of detents ----------------

#: The click sizes a rifle scope actually comes with, in radians, so that no
#: figure or exercise in this course carries ``0.0001`` as a bare literal.
#: Read-only for the same reason ``ICAO_SEA_LEVEL`` is: a shared mutable
#: module-level dict is a bug waiting for a long course.
#:
#: Note the ratio that the M02 lesson is built on: a tenth-mil click is
#: ``4.32 / pi = 1.3751`` times a quarter-MOA click. That is a constant, so the
#: mil turret is coarser by 37.5% at 100 yards and at 1000 yards alike.
CLICK_RAD = MappingProxyType(
    {
        "half_moa": RAD_PER_MOA / 2.0,
        "quarter_moa": RAD_PER_MOA / 4.0,
        "eighth_moa": RAD_PER_MOA / 8.0,
        "tenth_mil": RAD_PER_MIL / 10.0,
        "twentieth_mil": RAD_PER_MIL / 20.0,
    }
)


def clicks_for_angle(angle_rad: float, click_rad: float) -> float:
    """How many clicks a correction is, **unrounded**.

    Deliberately fractional. Rounding to a whole detent is the caller's
    decision, and the leftover is the whole subject of Module 02's third
    figure: you cannot dial 124.6 clicks, so you dial 125 and accept the
    residual. A function that rounded here would hide the quantity being
    taught.

    Args:
        angle_rad: The correction, radians.
        click_rad: Size of one click, radians. See :data:`CLICK_RAD`.

    Returns:
        The correction in clicks, fractional.

    Raises:
        ValueError: If ``click_rad`` is not positive.
    """
    if click_rad <= 0.0:
        raise ValueError(f"click_rad must be positive, got {click_rad}")
    return angle_rad / click_rad


def angle_for_clicks(clicks: float, click_rad: float) -> float:
    """The angle a number of clicks actually puts on the turret.

    The inverse of :func:`clicks_for_angle`. Pass it a *rounded* click count to
    get the angle you really dialled, and difference that against what you
    wanted to see the quantisation residual.

    Args:
        clicks: Number of clicks, whole or fractional.
        click_rad: Size of one click, radians. See :data:`CLICK_RAD`.

    Returns:
        The dialled angle, radians.

    Raises:
        ValueError: If ``click_rad`` is not positive.
    """
    if click_rad <= 0.0:
        raise ValueError(f"click_rad must be positive, got {click_rad}")
    return clicks * click_rad


__all__ = [
    "CLICK_RAD",
    "angle_for_clicks",
    "angle_for_offset_rad",
    "clicks_for_angle",
    "mil_ranging_error_m",
    "mil_ranging_m",
    "moa_subtension_in",
    "smoa_subtension_in",
    "subtension_m",
]

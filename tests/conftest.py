"""Shared fixtures for the course test suite.

The two loads defined here are the course's running example (see CURRICULUM.md).
Every module's worked example uses them, so the tests can check that a module's
published numbers are actually what its code produces.

These fixtures return plain dicts rather than library objects because the
library objects that will hold them (``Projectile``, ``Conditions``) are not
built until Module 15. Modules from 15 onward should add fixtures that
construct the real objects from these values.
"""

from __future__ import annotations

import pytest

#: Absolute tolerances, chosen as statements about acceptable *physical* error
#: rather than about floating point. A module may tighten these; loosening one
#: requires saying why in the test.
TOL = {
    "position_m": 1e-3,      # 1 mm over a kilometre of flight
    "velocity_mps": 1e-3,
    "angle_rad": 1e-9,
    "density_kgm3": 1e-4,
    "unit_roundtrip": 1e-12,  # conversions must be exact to machine precision
}


@pytest.fixture(scope="session")
def tolerances() -> dict:
    """The shared tolerance table, for tests that would rather ask than import."""
    return TOL


@pytest.fixture(scope="session")
def primary_load() -> dict:
    """6.5 Creedmoor, 140 gr Berger Hybrid Target -- the course's running example."""
    return {
        "name": "6.5 Creedmoor / 140 gr Berger Hybrid Target",
        "mass_gr": 140.0,
        "diameter_in": 0.264,
        "length_in": 1.360,
        "bc_g7_lbin2": 0.315,
        "mv_fps": 2700.0,
        "twist_in": 8.0,
        "right_hand_twist": True,
        "sight_height_in": 1.75,
        "zero_yd": 100.0,
    }


@pytest.fixture(scope="session")
def contrast_load() -> dict:
    """.308 Winchester, 175 gr Sierra MatchKing -- the comparison load.

    It goes transonic sooner and drifts more than the primary load, which makes
    several effects legible that a single load would hide.
    """
    return {
        "name": ".308 Winchester / 175 gr Sierra MatchKing",
        "mass_gr": 175.0,
        "diameter_in": 0.308,
        "length_in": 1.240,
        "bc_g7_lbin2": 0.243,
        "mv_fps": 2600.0,
        "twist_in": 11.25,
        "right_hand_twist": True,
        "sight_height_in": 1.75,
        "zero_yd": 100.0,
    }


@pytest.fixture(scope="session")
def icao_sea_level() -> dict:
    """ICAO standard atmosphere at sea level -- the course's default conditions.

    Note this is *not* Army Standard Metro, against which older G1 ballistic
    coefficients were computed. Module 09 explains the difference.
    """
    return {
        "pressure_pa": 101325.0,
        "temp_k": 288.15,
        "rh": 0.0,
        "density_kgm3": 1.225,
        "speed_of_sound_mps": 340.294,
    }

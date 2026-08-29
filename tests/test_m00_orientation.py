"""Module 00's shipped reference table: schema, not physics.

There is no library code in Module 00, so there is nothing here to test
numerically. What these tests protect is a *contract with Module 17*, which
regenerates ``effect_magnitudes.csv`` from the reader's own solver and diffs it
against this file. Seventeen modules is a long time for a column name to drift.
A rename should fail loudly here rather than quietly break that payoff.

The physics in the generator is deliberately not asserted on. It is model output
from a standalone reference implementation, and Module 17 is where it gets
checked against something independent.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

DATA = (
    Path(__file__).resolve().parents[1]
    / "modules"
    / "00-orientation"
    / "data"
    / "effect_magnitudes.csv"
)

#: The exact schema Module 17 will regenerate. Order matters; so do the unit
#: suffixes, which are the course's standing convention.
EXPECTED_COLUMNS = [
    "range_yd",
    "tof_s",
    "drop_in",
    "path_in",
    "wind_10mph_in",
    "spin_drift_in",
    "aero_jump_in",
    "coriolis_horiz_in",
    "coriolis_vert_in",
]

EXPECTED_RANGES_YD = [float(yd) for yd in range(100, 1201, 100)]


@pytest.fixture(scope="module")
def raw_text() -> str:
    assert DATA.exists(), (
        f"{DATA} is missing. Regenerate it with:\n"
        "  uv run python modules/00-orientation/data/generate_effect_magnitudes.py"
    )
    return DATA.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rows(raw_text: str) -> list[dict[str, float]]:
    body = [ln for ln in raw_text.splitlines() if not ln.startswith("#")]
    return [
        {key: float(value) for key, value in row.items()}
        for row in csv.DictReader(body)
    ]


def test_provenance_header_survives(raw_text: str):
    # data/README.md requires a provenance block in the file itself, so that a
    # CSV separated from this repository is still traceable. It must also say
    # plainly that nothing here was measured.
    header = "\n".join(ln for ln in raw_text.splitlines() if ln.startswith("#"))
    assert "MODEL OUTPUT, NOT MEASUREMENT" in header
    assert "generate_effect_magnitudes.py" in header
    assert "EMPIRICAL FITS" in header
    for assumption in ("ICAO", "3 o'clock", "latitude", "azimuth", "zero"):
        assert assumption in header, f"header does not state its {assumption} assumption"


def test_columns_are_exactly_the_m17_contract(rows):
    assert list(rows[0]) == EXPECTED_COLUMNS


def test_every_column_carries_its_unit(rows):
    # docs/units-and-conventions.md s.2: a bare name is a bug.
    for name in rows[0]:
        assert name.rsplit("_", 1)[-1] in {"yd", "s", "in"}, name


def test_range_grid_is_complete(rows):
    assert [row["range_yd"] for row in rows] == EXPECTED_RANGES_YD


def test_drop_grows_monotonically_with_range(rows):
    drops = [abs(row["drop_in"]) for row in rows]
    assert drops == sorted(drops)
    assert all(a < b for a, b in zip(drops, drops[1:], strict=False))


def test_time_of_flight_grows_monotonically_with_range(rows):
    tofs = [row["tof_s"] for row in rows]
    assert all(a < b for a, b in zip(tofs, tofs[1:], strict=False))


def test_signs_match_the_stated_conventions(rows):
    # docs/units-and-conventions.md s.4, restated in the file's own header.
    # Written out in plain English because sign conventions are where errors
    # hide, and a test that just says "> 0" does not say what it believes.
    for row in rows:
        at = f"at {row['range_yd']:.0f} yd"
        # Gravity pulls the bullet below the line of departure, always.
        assert row["drop_in"] < 0.0, f"drop should be below the line of departure {at}"
        # A 3 o'clock wind blows right to left: -z.
        assert row["wind_10mph_in"] < 0.0, f"a 3 o'clock wind should push left {at}"
        # A right-hand twist drifts right: +z.
        assert row["spin_drift_in"] > 0.0, f"right-hand twist should drift right {at}"
        # A 3 o'clock wind on a right-hand twist jumps the bullet up: +y.
        assert row["aero_jump_in"] > 0.0, f"3 o'clock wind should jump the bullet up {at}"
        # Northern hemisphere: horizontal Coriolis deflects right.
        assert row["coriolis_horiz_in"] > 0.0, f"northern hemisphere deflects right {at}"
        # Firing with an easterly component: the Eotvos effect lifts the bullet.
        assert row["coriolis_vert_in"] > 0.0, f"an easterly azimuth should lift {at}"


def test_the_bullet_is_on_the_line_of_sight_at_the_zero(rows):
    at_zero = next(row for row in rows if row["range_yd"] == 100.0)
    assert at_zero["path_in"] == pytest.approx(0.0, abs=1e-3)


def test_path_and_drop_are_different_questions(rows):
    # A frequent misreading: treating "drop" and "where the bullet is relative
    # to your line of sight" as the same number. They differ by the launch
    # angle, which is exactly what the zero buys you.
    for row in rows:
        assert abs(row["drop_in"]) > abs(row["path_in"])

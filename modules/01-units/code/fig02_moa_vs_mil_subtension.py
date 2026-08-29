"""Figure m01-fig02-moa-vs-mil-subtension.

What one MOA, one SMOA, and one mil are actually worth in inches, and what it
costs to confuse the first two.

Left panel: subtension against range. It shows the sizes, and it shows that at
this scale MOA and SMOA are visually the same line -- which is the whole reason
people mix them up.

Right panel: the consequence, using the course's running load. The come-up
comes from Module 00's reference table, converted to an angle at each range;
the plotted quantity is how far off the impact lands if a solver reports that
come-up in SMOA and it gets dialled on a true-MOA turret. That is a real and
common mismatch: some apps and most reticle-subtension charts are IPHY, most
turrets are true MOA.

Two panels rather than one, because subtension and error are different scales,
and a second y-axis on one plot invents a relationship that is not there.

No randomness, so this regenerates byte-identically by construction.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ballistics.units import (
    inches_to_m,
    m_to_inches,
    moa_to_rad,
    rad_to_smoa,
    smoa_to_rad,
    yards_to_m,
)
from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import TEXT_MUTED, annotate_series, cycle_colors

M00_DATA = (
    Path(__file__).resolve().parents[2] / "00-orientation" / "data" / "effect_magnitudes.csv"
)

RANGES_YD = [float(r) for r in range(0, 1201, 25)]

#: Three angular units, one physical fact each. Categorical: they are
#: identities, not an ordered scale.
UNITS = [
    ("1 mil", lambda a: a * 1.0e-3),
    ("1 MOA", moa_to_rad),
    ("1 SMOA", smoa_to_rad),
]


def subtension_in(angle_rad: float, range_yd: float) -> float:
    """Exact subtension in inches. tan, not the small-angle form -- M02 says why."""
    return m_to_inches(yards_to_m(range_yd) * math.tan(angle_rad))


def comeup_smoa(path_in: float, range_yd: float) -> float:
    """The load's come-up at this range, as a number of SMOA.

    ``path_in`` is the bullet's height relative to the line of sight, negative
    below it, so the correction needed is its magnitude.
    """
    range_m = yards_to_m(range_yd)
    return rad_to_smoa(math.atan(inches_to_m(abs(path_in)) / range_m))


def main() -> None:
    apply_style()
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    colors = cycle_colors(len(UNITS))

    # --- Left: what each unit is worth ------------------------------------
    for (label, to_rad), color in zip(UNITS, colors, strict=True):
        values_in = [subtension_in(to_rad(1.0), r) for r in RANGES_YD]
        left.plot(RANGES_YD, values_in, color=color, label=label, zorder=3)
        nudge = {"1 mil": 0.0, "1 MOA": 1.9, "1 SMOA": -1.9}[label]
        annotate_series(left, RANGES_YD[-1], values_in[-1], label, color, dx=30, dy=nudge)

    left.set_xlim(0, 1500)
    left.set_ylim(0, 48)
    left.set_xticks([0, 300, 600, 900, 1200])
    left.set_xlabel("range (yards)")
    left.set_ylabel("subtension of one unit (inches)")
    left.set_title("One unit, at range", loc="left")
    left.legend(loc="upper left")
    left.annotate(
        "0.47 in apart at 1000 yd:\none line, to the eye",
        xy=(1010, 10.4),
        xytext=(560, 17),
        fontsize=8.5,
        color=TEXT_MUTED,
        arrowprops={"arrowstyle": "-", "color": TEXT_MUTED, "linewidth": 0.8},
    )

    # --- Right: what confusing two of them costs --------------------------
    table = pd.read_csv(M00_DATA, comment="#")
    ranges_yd = table["range_yd"].tolist()
    error_in = []
    for range_yd, path_in in zip(ranges_yd, table["path_in"], strict=True):
        dialled = comeup_smoa(path_in, range_yd)          # the number the app printed
        range_m = yards_to_m(range_yd)
        # Dialled on a true-MOA turret instead of an IPHY one: same number,
        # bigger unit, so the shot goes high by the difference.
        over_m = range_m * (math.tan(moa_to_rad(dialled)) - math.tan(smoa_to_rad(dialled)))
        error_in.append(m_to_inches(over_m))

    right.plot(ranges_yd, error_in, color=colors[1], zorder=3)
    right.fill_between(ranges_yd, 0, error_in, color=colors[1], alpha=0.12, zorder=2)

    for range_yd, value_in in ((1000.0, error_in[ranges_yd.index(1000)]),):
        right.plot([range_yd], [value_in], "o", color=colors[1], zorder=4)
        right.annotate(
            f"{value_in:.1f} in high at 1000 yd\n(a {comeup_smoa(-326.229, 1000.0):.0f}-unit come-up)",
            xy=(range_yd, value_in),
            xytext=(-190, 6),
            textcoords="offset points",
            fontsize=8.5,
            color=TEXT_MUTED,
        )

    right.set_xlim(0, 1250)
    right.set_ylim(0, 30)
    right.set_xticks([0, 300, 600, 900, 1200])
    right.set_xlabel("range (yards)")
    right.set_ylabel("impact error (inches high)")
    right.set_title("Dialling an SMOA come-up on an MOA turret", loc="left")

    fig.suptitle(
        "MOA, SMOA and mil are three different units — and two of them look alike",
        x=0.5,
        y=1.0,
        fontsize=12,
        color=TEXT_MUTED,
    )
    fig.text(
        0.5,
        -0.04,
        "Right panel uses the course's running load (6.5 Creedmoor, 140 gr, 2700 fps, 100 yd "
        "zero); come-up from Module 00's reference table, which is model output, not measurement.",
        ha="center",
        fontsize=8,
        color=TEXT_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, 1, "fig02-moa-vs-mil-subtension")


if __name__ == "__main__":
    main()

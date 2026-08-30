"""Figure m02-fig03-click-resolution.

What a turret click is worth, and what is left over when you can only dial
whole ones.

This figure replaces a specified one whose premise was false. The original
asked to show that "0.1 mil and 1/4 MOA are nearly the same click value out to
600 yd, then separate". They are not and they cannot be: subtension is linear
in range, so the ratio of any two angular units is a constant. A tenth-mil
click is 4.32/pi = 1.3751 times a quarter-MOA click at 100 yards and at 1000
yards alike. CURRICULUM.md now says so.

Left: the come-up for the running load, in clicks. The mil turret needs fewer
clicks for the same correction, which is the same fact as its clicks being
bigger -- that is, coarser. "Mil turrets are finer" has it backwards.

Right: the residual. You cannot dial 124.6 clicks, so you dial 125 and land
somewhere other than where you aimed. The sawtooth is that leftover, and the
dashed envelope is the half-click bound it can never exceed. The bound grows
linearly with range and is still under two inches at 1000 yards, which is the
real conclusion: click quantisation is not what makes you miss.

Come-up is derived from Module 00's effect_magnitudes.csv, which is model
output, not measurement.

No randomness, so this regenerates byte-identically by construction.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ballistics.angles import CLICK_RAD, angle_for_offset_rad, subtension_m
from ballistics.units import inches_to_m, m_to_inches, rad_to_moa, yards_to_m
from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import SURFACE, TEXT_MUTED, annotate_series, cycle_colors

M00_DATA = (
    Path(__file__).resolve().parents[2] / "00-orientation" / "data" / "effect_magnitudes.csv"
)

#: The two turrets a shooter actually chooses between.
TURRETS = (
    ("1/4 MOA", "quarter_moa"),
    ("0.1 mil", "tenth_mil"),
)

RANGES_YD = np.arange(100.0, 1000.5, 2.5)


def comeup_rad(ranges_yd: np.ndarray) -> np.ndarray:
    """The running load's come-up at each range, from Module 00's table."""
    table = pd.read_csv(M00_DATA, comment="#")
    path_in = np.interp(
        ranges_yd,
        table["range_yd"].to_numpy(dtype=float),
        table["path_in"].to_numpy(dtype=float),
    )
    return np.array(
        [
            angle_for_offset_rad(inches_to_m(abs(drop_in)), yards_to_m(range_yd))
            for drop_in, range_yd in zip(path_in, ranges_yd, strict=True)
        ]
    )


def main() -> None:
    apply_style()
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.4, 4.8))
    colors = cycle_colors(len(TURRETS))

    angles_rad = comeup_rad(RANGES_YD)

    for (label, key), color in zip(TURRETS, colors, strict=True):
        click_rad = CLICK_RAD[key]
        clicks = angles_rad / click_rad

        # --- Left: how many clicks that correction is ----------------------
        left.plot(RANGES_YD, clicks, color=color, label=label, zorder=3)
        annotate_series(left, RANGES_YD[-1], clicks[-1], label, color, dx=22, dy=0)

    # --- Right: what is left after rounding to a whole click --------------
    # The half-click envelope is the content; the dots are a sample of the
    # actual residual at ranges a shooter would really dial. Plotting the raw
    # sawtooth at full resolution draws 360 near-vertical strokes per series
    # and reads as noise, which teaches nothing the bound does not.
    dial_yd = np.arange(100.0, 1000.5, 50.0)
    dial_rad = comeup_rad(dial_yd)

    for (label, key), color in reversed(list(zip(TURRETS, colors, strict=True))):
        click_rad = CLICK_RAD[key]
        envelope_in = np.array(
            [
                m_to_inches(subtension_m(click_rad / 2.0, yards_to_m(range_yd)))
                for range_yd in RANGES_YD
            ]
        )
        right.fill_between(
            RANGES_YD, -envelope_in, envelope_in, color=color,
            alpha=0.16 if key == "quarter_moa" else 0.11, linewidth=0.0, zorder=2,
        )
        right.plot(RANGES_YD, envelope_in, color=color, linewidth=1.0, zorder=3)
        right.plot(RANGES_YD, -envelope_in, color=color, linewidth=1.0, zorder=3)
        right.annotate(
            f"{label}:  ±{envelope_in[-1]:.2f} in",
            xy=(1000.0, envelope_in[-1]), xytext=(-6, 4), textcoords="offset points",
            fontsize=8.5, color=TEXT_MUTED, ha="right", va="bottom", zorder=6,
        )

        residual_in = np.array(
            [
                m_to_inches(
                    subtension_m(np.round(wanted / click_rad) * click_rad - wanted,
                                 yards_to_m(range_yd))
                )
                for wanted, range_yd in zip(dial_rad, dial_yd, strict=True)
            ]
        )
        right.plot(
            dial_yd, residual_in, "o", color=color, markersize=5.0,
            markeredgecolor=SURFACE, markeredgewidth=1.4, linestyle="none",
            label=label, zorder=5,
        )

    # --- Left panel furniture ---------------------------------------------
    thousand = np.searchsorted(RANGES_YD, 1000.0)
    for (_label, key), color in zip(TURRETS, colors, strict=True):
        clicks_1000 = angles_rad[thousand] / CLICK_RAD[key]
        left.plot([1000.0], [clicks_1000], "o", color=color, markersize=6.5,
                  markeredgecolor=SURFACE, markeredgewidth=2.0, zorder=4)

    left.text(
        575.0, 33.0,
        f"{angles_rad[thousand] / CLICK_RAD['quarter_moa']:.0f} quarter-MOA clicks "
        f"at 1000 yd,\n"
        f"or {angles_rad[thousand] / CLICK_RAD['tenth_mil']:.0f} tenth-mil ones. "
        "Fewer clicks\nmeans bigger ones: mil is coarser.",
        fontsize=8.5, color=TEXT_MUTED, ha="left", va="top", linespacing=1.5,
    )

    left.set_xlim(100.0, 1090.0)
    left.set_ylim(0.0, 130.0)
    left.set_xticks([100, 400, 700, 1000])
    left.set_xlabel("range (yards)")
    left.set_ylabel("clicks of elevation from a 100 yd zero")
    left.set_title("The same come-up, on two turrets", loc="left")
    left.legend(loc="upper left", bbox_to_anchor=(0.0, 0.72))

    # --- Right panel furniture --------------------------------------------
    right.axhline(0.0, color=TEXT_MUTED, linewidth=0.9, zorder=1)
    right.set_xlim(100.0, 1000.0)
    right.set_ylim(-2.6, 2.6)
    right.set_xticks([100, 400, 700, 1000])
    right.set_xlabel("range (yards)")
    right.set_ylabel("impact error from rounding to a whole click (inches)")
    right.set_title("What the rounding leaves behind", loc="left")
    right.legend(loc="lower left", ncols=2, title="residual at ranges you would dial")
    right.get_legend().get_title().set_fontsize(8.5)
    right.get_legend().get_title().set_color(TEXT_MUTED)

    fig.text(
        0.5, -0.04,
        "Course's running load (6.5 Creedmoor, 140 gr, 2700 fps, 100 yd zero); come-up derived "
        "from Module 00's reference table, which is model output, not measurement. Positive "
        "residual is an impact above the point of aim.",
        ha="center", fontsize=8, color=TEXT_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, 2, "fig03-click-resolution")


if __name__ == "__main__":
    main()

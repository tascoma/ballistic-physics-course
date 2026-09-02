"""Figure m02-fig02-reticle-ranging.

Ranging a target with the reticle, and why the answer is only ever as good as
the guess you fed it.

Left: the geometry. A target of known size ``S`` subtending ``theta`` in the
reticle sits at ``R = S / theta``, with ``theta`` in radians -- which is why
the mil, being exactly a milliradian, makes this arithmetic rather than
trigonometry. **The diagram is not to scale**: the real triangle for the worked
example is 794 yards long and 40 inches tall, a ratio of about 700:1, which
would draw as a horizontal line.

Right: the consequence. Range is proportional to the size guess, so a 10%
error in the guess is a 10% error in the range at every distance -- the band
widens linearly and no better optic narrows it. The reading error is shown
separately to make the quadrature visible: it is the smaller term, and adding
it to a 10% size error moves the total from 10.0% to 10.6%.

The elevation consequence is annotated rather than plotted, because drop is a
different measure on a different scale and this course does not put two scales
on one axis. It comes from Module 00's reference table, which is model output.

No randomness, so this regenerates byte-identically by construction.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ballistics.angles import angle_for_offset_rad, mil_ranging_error_m, mil_ranging_m
from ballistics.units import inches_to_m, m_to_inches, m_to_yards, yards_to_m
from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import AXIS, GRID, SURFACE, TEXT_MUTED, TEXT_SECONDARY, cycle_colors

M00_DATA = (
    Path(__file__).resolve().parents[2] / "00-orientation" / "data" / "effect_magnitudes.csv"
)

#: The worked example carried through the whole module.
TARGET_SIZE_IN = 40.0
MILS_READ = 1.4
SIZE_ERROR_FRACTION = 0.10
MILS_ERROR = 0.05


def elevation_miss_in(true_range_yd: float, believed_range_yd: float) -> float:
    """Inches high when a come-up for one range is dialled at another.

    Reads the running load's path from Module 00's reference table -- model
    output, not measurement -- and interpolates between its 100-yard rows.
    """
    table = pd.read_csv(M00_DATA, comment="#")
    ranges_yd = table["range_yd"].to_numpy(dtype=float)
    path_in = table["path_in"].to_numpy(dtype=float)

    def comeup_rad(range_yd: float) -> float:
        drop_in = abs(float(np.interp(range_yd, ranges_yd, path_in)))
        return angle_for_offset_rad(inches_to_m(drop_in), yards_to_m(range_yd))

    dialled_rad = comeup_rad(believed_range_yd)
    correct_rad = comeup_rad(true_range_yd)
    true_range_m = yards_to_m(true_range_yd)
    return m_to_inches(true_range_m * (math.tan(dialled_rad) - math.tan(correct_rad)))


def draw_geometry(ax, color: str) -> None:
    """The ranging triangle, schematic and deliberately not to scale."""
    half = 0.30
    ax.plot([0.0, 1.0], [0.0, 0.0], color=AXIS, linewidth=0.9, linestyle=(0, (4, 3)), zorder=2)
    for sign in (1.0, -1.0):
        ax.plot([0.0, 1.0], [0.0, sign * half], color=color, linewidth=1.6, zorder=3)

    # The target, with a mil ruler beside it.
    ax.plot([1.0, 1.0], [-half, half], color=TEXT_SECONDARY, linewidth=4.0,
            solid_capstyle="butt", zorder=4)
    for i in range(8):
        y = -half + i * (2 * half / 7.0)
        ax.plot([1.045, 1.075], [y, y], color=AXIS, linewidth=0.9, zorder=3)
    ax.plot([1.06, 1.06], [-half, half], color=AXIS, linewidth=0.9, zorder=3)
    ax.annotate(
        "1.4 mil\nin the reticle", xy=(1.075, 0.0), xytext=(1.11, 0.0),
        fontsize=8.5, color=TEXT_MUTED, va="center", ha="left", linespacing=1.4,
    )

    # The angle at the eye.
    arc = np.linspace(-math.atan(half), math.atan(half), 60)
    ax.plot(0.30 * np.cos(arc), 0.30 * np.sin(arc), color=TEXT_MUTED, linewidth=0.9, zorder=3)
    ax.text(0.345, 0.0, "θ", fontsize=11, color=TEXT_SECONDARY, va="center", ha="left")

    ax.plot([0.0], [0.0], "o", color=color, markersize=7,
            markeredgecolor=SURFACE, markeredgewidth=2.0, zorder=5)
    ax.text(0.0, -0.075, "you", fontsize=8.5, color=TEXT_MUTED, ha="center", va="top")

    ax.annotate("", xy=(1.0, -0.44), xytext=(0.0, -0.44),
                arrowprops={"arrowstyle": "<->", "color": AXIS, "linewidth": 0.9})
    ax.text(0.5, -0.40, "R = ?  the answer", fontsize=8.5, color=TEXT_MUTED,
            ha="center", va="bottom")
    ax.text(1.0, half + 0.045, "S = 40 in\nyour guess", fontsize=8.5, color=TEXT_MUTED,
            ha="center", va="bottom", linespacing=1.4)

    ax.text(
        0.0, -0.545, "R = S / θ",
        fontsize=11, color=TEXT_SECONDARY, ha="left", va="bottom",
    )
    ax.text(
        0.235, -0.535, "θ in radians — so a mil reading is just ÷ 0.001",
        fontsize=8.5, color=TEXT_MUTED, ha="left", va="bottom",
    )

    ax.set_xlim(-0.10, 1.42)
    ax.set_ylim(-0.66, 0.52)
    ax.axis("off")
    ax.set_title("The geometry (not to scale)", loc="left")


def main() -> None:
    apply_style()
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.4, 4.8), width_ratios=(1.0, 1.12))
    size_color, read_color, both_color = cycle_colors(3)

    draw_geometry(left, size_color)

    # --- Right: how the answer's uncertainty grows with the guess's --------
    target_size_m = inches_to_m(TARGET_SIZE_IN)
    nominal_yd = m_to_yards(mil_ranging_m(target_size_m, MILS_READ))
    size_error_pct = np.linspace(0.0, 25.0, 200)

    def band_yd(size_pct, mils_err):
        return np.array([
            m_to_yards(
                mil_ranging_error_m(target_size_m, target_size_m * p / 100.0, MILS_READ, mils_err)
            )
            for p in size_pct
        ])

    size_only = band_yd(size_error_pct, 0.0)
    combined = band_yd(size_error_pct, MILS_ERROR)
    read_only = band_yd(np.zeros_like(size_error_pct), MILS_ERROR)

    right.fill_between(size_error_pct, 0.0, combined, color=both_color, alpha=0.10, zorder=2)
    right.plot(size_error_pct, combined, color=both_color, zorder=5,
               label=f"both, with a ±{MILS_ERROR} mil read")
    right.plot(size_error_pct, size_only, color=size_color, zorder=4,
               label="size guess alone")
    right.plot(size_error_pct, read_only, color=read_color, linestyle=(0, (5, 2)),
               linewidth=1.6, zorder=3, label=f"±{MILS_ERROR} mil read alone")

    # The worked example.
    example_yd = m_to_yards(
        mil_ranging_error_m(
            target_size_m, target_size_m * SIZE_ERROR_FRACTION, MILS_READ, MILS_ERROR
        )
    )
    miss_in = elevation_miss_in(nominal_yd, nominal_yd + example_yd)
    right.plot([10.0], [example_yd], "o", color=both_color, markersize=7.5,
               markeredgecolor=SURFACE, markeredgewidth=2.0, zorder=6)
    right.annotate(
        f"a 10 % size guess on a {nominal_yd:.0f} yd target\n"
        f"is ±{example_yd:.0f} yd — and dialling for that\n"
        f"puts the shot {miss_in:.0f} in high",
        xy=(10.0, example_yd), xytext=(12.9, 24.0), textcoords="data",
        fontsize=8.5, color=TEXT_MUTED, ha="left", va="center", linespacing=1.5, zorder=6,
        arrowprops={"arrowstyle": "-", "color": TEXT_MUTED, "linewidth": 0.8,
                    "shrinkA": 4, "shrinkB": 6},
        bbox={"facecolor": SURFACE, "edgecolor": "none", "pad": 3.0, "alpha": 0.9},
    )

    right.set_xlim(0.0, 25.0)
    right.set_ylim(0.0, 210.0)
    right.set_xticks([0, 5, 10, 15, 20, 25])
    right.set_xticklabels(["0", "5 %", "10 %", "15 %", "20 %", "25 %"])
    right.set_xlabel("error in the assumed target size")
    right.set_ylabel(f"uncertainty in the ranged distance (yards, at {nominal_yd:.0f} yd)")
    right.set_title("What that guess costs you", loc="left")
    right.legend(loc="upper left")
    right.set_axisbelow(True)
    right.grid(color=GRID, linewidth=0.8)

    fig.text(
        0.5, -0.04,
        "Right panel: the two errors add in quadrature, so the larger swallows the smaller — "
        "10 % and 3.6 % combine to 10.6 %, not 13.6 %. Elevation figure uses the course's "
        "running load and Module 00's reference table, which is model output, not measurement.",
        ha="center", fontsize=8, color=TEXT_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, 2, "fig02-reticle-ranging")


if __name__ == "__main__":
    main()

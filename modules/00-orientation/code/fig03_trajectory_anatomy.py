"""Figure m00-fig03-trajectory-anatomy.

The parts of a trajectory, named, on a real one.

Two honesty problems this figure has to solve.

First, the vertical scale. Drawn true to life over 250 yards the trajectory is
indistinguishable from a straight line, so the y-axis is stretched enormously.
An unlabelled stretch teaches a rainbow-arc mental image that is simply false,
so the exaggeration factor is *computed from the rendered axes* and printed on
the plot. It is not a number anybody typed in, and it cannot drift.

Second, the zero. The course's running zero is 100 yards, but at a 100-yard zero
the bullet is above the line of sight only between roughly 25 and 100 yards and
below it for everything beyond -- the crossings are cramped into the left edge
and the figure teaches nothing. This one is drawn at a 200-yard zero, which is a
common field zero for this load, and says so.

The bore line and the line of departure are drawn as one line. They genuinely
differ, by the jump the rifle imparts as the bullet exits -- a few tenths of an
MOA. Drawing that gap would mean inventing a number that Module 22 is the one
qualified to supply, so the figure names the distinction instead of faking it.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import (
    PALETTE,
    SURFACE,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

# The reference model that produced this module's data. It lives in data/
# because it is not part of the library the reader builds.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "data"))
import generate_effect_magnitudes as ref  # noqa: E402

ZERO_YD = 200.0
MAX_YD = 250.0


def main() -> None:
    apply_style()

    zero_angle_rad = ref.solve_zero_angle_rad(ZERO_YD * ref.M_PER_YD)
    path = ref.integrate(zero_angle_rad, MAX_YD * ref.M_PER_YD + 2.0)

    x_yd = path["x_m"] / ref.M_PER_YD
    y_in = path["y_m"] / ref.M_PER_IN
    keep = x_yd <= MAX_YD
    x_yd, y_in = x_yd[keep], y_in[keep]

    sight_height_in = ref.SIGHT_HEIGHT_IN
    bore_in = -sight_height_in + x_yd * (36.0 * math.tan(zero_angle_rad))

    apex_i = int(np.argmax(y_in))
    crossings = np.where(np.sign(y_in[:-1]) != np.sign(y_in[1:]))[0]
    near_zero_yd = float(np.interp(0.0, [y_in[crossings[0]], y_in[crossings[0] + 1]],
                                   [x_yd[crossings[0]], x_yd[crossings[0] + 1]]))

    fig, ax = plt.subplots(figsize=(10.5, 4.6))

    ax.axhline(0.0, color=TEXT_SECONDARY, linewidth=1.2, zorder=2)
    ax.plot(x_yd, bore_in, color=TEXT_MUTED, linewidth=1.1, linestyle=(0, (6, 4)), zorder=2)
    ax.plot(x_yd, y_in, color=PALETTE[0], linewidth=2.4, zorder=4)

    ax.set_xlim(-4, MAX_YD + 34)
    ax.set_ylim(-8.5, 5.6)
    ax.set_xlabel("range (yards)")
    ax.set_ylabel("height above line of sight (inches)")
    ax.grid(axis="x", visible=False)

    def mark(x, y, text, dx, dy, ha="center"):
        ax.plot([x], [y], marker="o", markersize=6, color=PALETTE[0],
                markeredgecolor=SURFACE, markeredgewidth=1.4, zorder=5)
        ax.annotate(
            text, xy=(x, y), xytext=(x + dx, y + dy), ha=ha, fontsize=8.6,
            color=TEXT_PRIMARY, zorder=6,
            arrowprops={"arrowstyle": "-", "color": TEXT_MUTED, "linewidth": 0.8},
        )

    mark(0.0, -sight_height_in, "Muzzle\n1.75 in below the sight", 3, -3.6, ha="left")
    mark(near_zero_yd, 0.0, f"Near zero\n{near_zero_yd:.0f} yd", -5, -2.5, ha="right")
    mark(x_yd[apex_i], y_in[apex_i],
         f"Apex\n{y_in[apex_i]:.1f} in high at {x_yd[apex_i]:.0f} yd", 0, 2.0)
    mark(ZERO_YD, 0.0, f"Far zero\n{ZERO_YD:.0f} yd", -2, 2.6, ha="center")
    mark(MAX_YD, float(y_in[-1]), f"{abs(y_in[-1]):.1f} in low\nat {MAX_YD:.0f} yd", 6, -1.4,
         ha="left")

    # Direct labels: three lines, so colour never carries identity alone.
    # The bore line leaves the top of the axes long before the right edge --
    # that divergence is the point of it -- so it is labelled where it is still
    # on the plot rather than at its end.
    bore_label_x = 62.0
    ax.annotate(
        "Bore line\n(the line of departure differs\nfrom it by jump — M22)",
        xy=(bore_label_x, float(np.interp(bore_label_x, x_yd, bore_in))),
        xytext=(bore_label_x - 8, 4.4), ha="right", va="top", fontsize=8.4,
        color=TEXT_MUTED,
        arrowprops={"arrowstyle": "-", "color": TEXT_MUTED, "linewidth": 0.8},
    )
    ax.annotate("Line of sight", xy=(MAX_YD + 4, 0.42), fontsize=8.8,
                color=TEXT_SECONDARY, va="center", ha="left")
    ax.annotate("Trajectory", xy=(152, float(np.interp(152, x_yd, y_in)) + 0.9),
                fontsize=9.2, color=PALETTE[0], va="bottom", ha="center")

    ax.set_title(
        "Anatomy of a trajectory — 6.5 Creedmoor, 140 gr, 2700 fps, 200 yd zero",
        loc="left",
    )

    # The exaggeration factor, measured off the rendered axes rather than
    # asserted, so it cannot drift when the figure size changes.
    fig.canvas.draw()
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    x_span_in = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 36.0
    y_span_in = ax.get_ylim()[1] - ax.get_ylim()[0]
    exaggeration = (x_span_in / bbox.width) / (y_span_in / bbox.height)

    ax.annotate(
        f"VERTICAL SCALE EXAGGERATED {exaggeration:.0f}×.\n"
        "Drawn true to life this whole curve is a straight line —\n"
        "the bullet never rises more than a few inches.",
        xy=(0.5, 0.045), xycoords="axes fraction", ha="center", va="bottom",
        fontsize=8.4, color=TEXT_SECONDARY,
        bbox={"facecolor": SURFACE, "edgecolor": TEXT_MUTED, "linewidth": 0.8,
              "boxstyle": "round,pad=0.45"},
        zorder=7,
    )

    fig.tight_layout()
    save_figure(fig, 0, "fig03-trajectory-anatomy")
    print(f"  (exaggeration {exaggeration:.1f}x, near zero {near_zero_yd:.1f} yd)")


if __name__ == "__main__":
    main()

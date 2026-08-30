"""Figure m02-fig01-small-angle-error.

Where the small-angle approximation stops being safe, and where it never
matters.

The quantity plotted is the *relative* error of using ``theta`` in place of
``tan(theta)``: ``(tan(theta) - theta) / theta``. Relative rather than
absolute, because the question a shooter has is "what fraction of my
correction is this costing me", and that fraction is independent of range --
which is exactly what makes the answer usable as a single line.

Log-log, because the interesting behaviour spans six decades of error across
three decades of angle, and on linear axes the whole useful region is a flat
line on the floor. The straight line on log-log is the point: a slope of 2 is
the visual signature of ``theta**2/3``, so the reader can see the power law
rather than take it on faith. The dashed prediction is drawn over the exact
curve to show they are the same line until the angle stops being small.

Two shaded bands, because there are two different questions:

  * **corrections** -- the angles you dial. The running load's 1000-yard
    come-up is 31 MOA, about half a degree. The error there is parts per
    million.
  * **elevation and incline angles** -- the angles the *geometry* involves,
    which reach 30 degrees or more on a steep shot and are handled in M08.

No randomness, so this regenerates byte-identically by construction.
"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np

from ballistics.units import rad_to_moa
from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import SURFACE, TEXT_MUTED, cycle_colors

#: The come-up for the running load at 1000 yd, from Module 00's reference
#: table (path -326.229 in). Model output, not measurement.
COMEUP_1000YD_RAD = math.atan(326.229 * 0.0254 / (1000.0 * 0.9144))

#: Angles called out on the curve, as (degrees, label, offset in points).
#: Offsets put every label in the empty half of the plot: the come-up above
#: and left of the diagonal, the rest below and right of it.
MARKERS = (
    (rad_to_moa(COMEUP_1000YD_RAD) / 60.0, "31 MOA — the 1000 yd come-up", (-8, 20), "right"),
    (1.0, "1 degree", (12, -14), "left"),
    (5.0, "5 degrees", (12, -14), "left"),
    (30.0, "30 degrees — a steep incline", (-10, 16), "right"),
)

MAX_DEGREES = 50.0


def format_error(relative: float) -> str:
    """Percent reads as 0.00 below a ten-thousandth, so switch to ppm there."""
    if relative < 1e-4:
        return f"{relative * 1e6:.0f} parts per million"
    return f"{relative:.2%}".replace("%", " %")


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    exact_color, predicted_color = cycle_colors(2)

    degrees = np.logspace(-2.0, math.log10(MAX_DEGREES), 600)
    radians = np.radians(degrees)
    relative = (np.tan(radians) - radians) / radians
    predicted = radians**2 / 3.0

    # --- The two regimes, shaded before the data so the marks sit on top ----
    ax.axvspan(0.0, 1.0, color=exact_color, alpha=0.07, zorder=1)
    ax.axvspan(5.0, MAX_DEGREES, color=predicted_color, alpha=0.07, zorder=1)

    # Band captions sit on the floor of the plot, clear of the diagonal.
    ax.text(
        0.0125, 2.2e-9, "angles you DIAL\ncorrections live here",
        fontsize=8.5, color=TEXT_MUTED, ha="left", va="bottom", linespacing=1.4,
    )
    ax.text(
        MAX_DEGREES * 0.93, 2.2e-9, "angles the GEOMETRY involves\ninclines, Module 08",
        fontsize=8.5, color=TEXT_MUTED, ha="right", va="bottom", linespacing=1.4,
    )

    # --- The exact error, and the theta**2/3 prediction over it -------------
    ax.plot(degrees, relative, color=exact_color, label="exact:  (tan θ − θ) / θ", zorder=4)
    ax.plot(
        degrees, predicted, color=predicted_color, linestyle=(0, (5, 2)), linewidth=1.6,
        label="prediction:  θ² / 3", zorder=5,
    )

    # --- One percent, the line nobody should cross without knowing ---------
    ax.axhline(0.01, color=TEXT_MUTED, linewidth=0.9, zorder=3)
    ax.text(
        0.0125, 0.0125, "1 % error", fontsize=8.5, color=TEXT_MUTED,
        ha="left", va="bottom",
    )

    for degrees_at, label, (dx, dy), align in MARKERS:
        radians_at = math.radians(degrees_at)
        error_at = (math.tan(radians_at) - radians_at) / radians_at
        ax.plot(
            [degrees_at], [error_at], "o", color=exact_color, markersize=6.5,
            markeredgecolor=SURFACE, markeredgewidth=2.0, zorder=6,
        )
        ax.annotate(
            f"{label}\n{format_error(error_at)}",
            xy=(degrees_at, error_at), xytext=(dx, dy), textcoords="offset points",
            fontsize=8.5, color=TEXT_MUTED, linespacing=1.4, ha=align, zorder=6,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, MAX_DEGREES)
    ax.set_ylim(1e-9, 1.0)
    ax.set_xticks([0.01, 0.1, 1.0, 10.0])
    ax.set_xticklabels(["0.01°", "0.1°", "1°", "10°"])
    ax.set_xlabel("angle")
    ax.set_ylabel("relative error of using θ instead of tan θ")
    ax.set_title("The small-angle approximation, and where it runs out", loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.99))

    fig.text(
        0.5, -0.03,
        "Both axes logarithmic. The slope-2 straight line is the signature of the θ²/3 law; "
        "the two curves visibly separate only past ~25°. Come-up from Module 00's reference table, "
        "which is model output, not measurement.",
        ha="center", fontsize=8, color=TEXT_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, 2, "fig01-small-angle-error")


if __name__ == "__main__":
    main()

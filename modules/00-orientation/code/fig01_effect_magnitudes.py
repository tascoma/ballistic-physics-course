"""Figure m00-fig01-effect-magnitudes.

Every effect a ballistic solver models, ranked by size, at three ranges.

The x-axis is logarithmic because the effects span four orders of magnitude: on
a linear axis the drop bar is the only one you can see. Because a log axis makes
bar *length* untrustworthy as an encoding, every bar carries its actual value.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import EFFECT_COLORS, TEXT_MUTED, TEXT_SECONDARY

DATA = Path(__file__).resolve().parent.parent / "data" / "effect_magnitudes.csv"


def two_sig_figs(value_in: float) -> str:
    """Two significant figures, so 0.019 and 0.016 do not both print as 0.02."""
    if value_in >= 100.0:
        return f"{value_in:,.0f} in"
    if value_in >= 10.0:
        return f"{value_in:.0f} in"
    if value_in >= 1.0:
        return f"{value_in:.1f} in"
    if value_in >= 0.1:
        return f"{value_in:.2f} in"
    return f"{value_in:.3f} in"

PANEL_RANGES_YD = (100, 500, 1000)

#: Colour follows the entity, course-wide (ballistics.viz.style.EFFECT_COLORS),
#: so "orange is wind" here still means wind in Module 29.
#:
#: Drop wears the drag colour rather than a colour of its own. At 1000 yards
#: drop is as much a drag phenomenon as a gravity one -- drag sets the time of
#: flight, and time of flight is what gravity acts over -- so the label says
#: both and the colour points at the module that explains the size of it.
EFFECTS = [
    ("drop_in", "Drop\n(gravity × drag)", EFFECT_COLORS["drag"]),
    ("wind_10mph_in", "Wind\n(10 mph full value)", EFFECT_COLORS["wind"]),
    ("spin_drift_in", "Spin drift", EFFECT_COLORS["spin_drift"]),
    ("aero_jump_in", "Aerodynamic jump", EFFECT_COLORS["aero_jump"]),
    ("coriolis_horiz_in", "Coriolis\n(horizontal)", EFFECT_COLORS["coriolis"]),
    ("coriolis_vert_in", "Coriolis\n(vertical, Eötvös)", EFFECT_COLORS["coriolis"]),
]


def main() -> None:
    apply_style()
    frame = pd.read_csv(DATA, comment="#").set_index("range_yd")

    fig, axes = plt.subplots(
        1, len(PANEL_RANGES_YD), figsize=(11.0, 4.4), sharey=True
    )

    labels = [label for _, label, _ in EFFECTS]
    colors = [color for _, _, color in EFFECTS]
    positions = range(len(EFFECTS))

    for ax, range_yd in zip(axes, PANEL_RANGES_YD, strict=True):
        row = frame.loc[range_yd]
        values_in = [abs(row[column]) for column, _, _ in EFFECTS]

        ax.barh(list(positions), values_in, color=colors, height=0.62, zorder=3)

        # A log axis makes bar length a bad encoding, so state every number.
        for y, value in zip(positions, values_in, strict=True):
            ax.annotate(
                two_sig_figs(value),
                xy=(value, y),
                xytext=(5, 0),
                textcoords="offset points",
                va="center",
                fontsize=8.5,
                color=TEXT_SECONDARY,
            )

        ax.set_xscale("log")
        ax.set_xlim(0.008, 1600)
        ax.set_xlabel("displacement (inches, log scale)")
        ax.set_title(f"{range_yd} yd", pad=8)
        ax.set_yticks(list(positions), labels)
        ax.invert_yaxis()
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)

    axes[0].set_ylabel("")
    fig.suptitle(
        "How big is each effect?  6.5 Creedmoor, 140 gr, 2700 fps",
        x=0.5,
        y=0.99,
        fontsize=12,
        color=TEXT_SECONDARY,
    )
    fig.text(
        0.5,
        -0.04,
        "Reference model output, not measurement — see this module's data/ directory. "
        "Magnitudes shown; direction is in the table.",
        ha="center",
        fontsize=8,
        color=TEXT_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, 0, "fig01-effect-magnitudes")


if __name__ == "__main__":
    main()

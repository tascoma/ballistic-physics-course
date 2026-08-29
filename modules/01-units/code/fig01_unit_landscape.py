"""Figure m01-fig01-unit-landscape.

Four facts about the course's running load, each expressed in every unit a
shooter is likely to meet it in.

Nothing about the bullet changes across a row. Only the number does, and it
changes by orders of magnitude, which is why the axis is logarithmic and why
every point carries its value: on a log axis, position is a weak encoding and
the numbers are the point of the figure rather than a decoration on it.

One physical fact per facet means one series per facet, so every dot wears
palette slot 1. A ramp here would double-encode magnitude as hue and say
nothing the axis does not already say.

No randomness, so this regenerates byte-identically by construction.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from ballistics.units import (
    fps_to_mps,
    grains_to_kg,
    inches_to_m,
    kg_to_grains,
    m_to_feet,
    m_to_inches,
    m_to_yards,
    mps_to_fps,
    mps_to_mph,
    pa_to_hpa,
    pa_to_inhg,
    yards_to_m,
)
from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import PALETTE, TEXT_MUTED, TEXT_PRIMARY, TEXT_SECONDARY

DOT_COLOR = PALETTE[0]

# The running load, and one standard atmosphere. Each facet is (title, note,
# [(unit label, value)]), with the SI form of the quantity computed first so
# every other entry is derived from the same physical fact.
MUZZLE_VELOCITY_MPS = fps_to_mps(2700.0)
BULLET_MASS_KG = grains_to_kg(140.0)
RANGE_M = yards_to_m(1000.0)
PRESSURE_PA = 101325.0

FACETS = [
    (
        "Muzzle velocity",
        "6.5 Creedmoor, 140 gr",
        [
            ("m/s", MUZZLE_VELOCITY_MPS),
            ("fps", mps_to_fps(MUZZLE_VELOCITY_MPS)),
            ("mph", mps_to_mph(MUZZLE_VELOCITY_MPS)),
            ("km/h", MUZZLE_VELOCITY_MPS * 3.6),
        ],
    ),
    (
        "Bullet mass",
        "the same bullet, on four scales",
        [
            ("kg", BULLET_MASS_KG),
            ("g", BULLET_MASS_KG * 1000.0),
            ("grains", kg_to_grains(BULLET_MASS_KG)),
            ("pounds", kg_to_grains(BULLET_MASS_KG) / 7000.0),
        ],
    ),
    (
        "Range",
        "one thousand yards",
        [
            ("m", RANGE_M),
            ("yards", m_to_yards(RANGE_M)),
            ("feet", m_to_feet(RANGE_M)),
            ("inches", m_to_inches(RANGE_M)),
        ],
    ),
    (
        "Station pressure",
        "ICAO standard, sea level",
        [
            ("Pa", PRESSURE_PA),
            ("hPa (mbar)", pa_to_hpa(PRESSURE_PA)),
            ("inHg", pa_to_inhg(PRESSURE_PA)),
            ("psi", PRESSURE_PA * inches_to_m(1.0) ** 2 / 4.4482216152605),
        ],
    ),
]


def label(value: float) -> str:
    """Four significant figures, and never scientific notation at these sizes.

    Four because the figure is asking the reader to check a conversion, and
    three would hide the difference between 9.072 g and the 9.072 they would
    get from a rounded grain.
    """
    if value >= 1000.0:
        return f"{value:,.0f}"
    return f"{float(f'{value:.4g}'):g}"


def main() -> None:
    apply_style()
    fig, axes = plt.subplots(1, 4, figsize=(12.0, 4.2))

    for ax, (title, note, entries) in zip(axes, FACETS, strict=True):
        labels = [name for name, _ in entries]
        values = [value for _, value in entries]
        positions = list(range(len(entries)))

        ax.scatter(values, positions, s=70, color=DOT_COLOR, zorder=4)
        # A hairline from the axis to the dot, so the eye can find its row on a
        # scale this wide without a heavy grid.
        for y, value in zip(positions, values, strict=True):
            ax.plot([min(values) / 14, value], [y, y], color=DOT_COLOR, linewidth=0.7,
                    alpha=0.35, zorder=3)
            ax.annotate(
                label(value),
                xy=(value, y),
                xytext=(0, 11),
                textcoords="offset points",
                ha="center",
                fontsize=8.5,
                color=TEXT_SECONDARY,
            )

        ax.set_xscale("log")
        ax.set_xlim(min(values) / 14, max(values) * 14)
        ax.set_ylim(-0.8, len(entries) - 0.3)
        ax.set_yticks(positions, labels)
        ax.invert_yaxis()
        ax.annotate(
            title,
            xy=(0, 1.0),
            xycoords="axes fraction",
            xytext=(0, 26),
            textcoords="offset points",
            fontsize=11,
            color=TEXT_PRIMARY,
        )
        ax.annotate(
            note,
            xy=(0, 1.0),
            xycoords="axes fraction",
            xytext=(0, 12),
            textcoords="offset points",
            fontsize=8.5,
            color=TEXT_MUTED,
        )
        ax.set_xlabel("value (log scale)")
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)

    fig.suptitle(
        "The same four physical facts, in the units a shooter actually meets",
        x=0.5,
        y=1.10,
        fontsize=12,
        color=TEXT_SECONDARY,
    )
    fig.text(
        0.5,
        -0.09,
        "Nothing about the bullet, the distance, or the air changes down a column — only the "
        "number does.\nAcross the four facets the same four facts are written as numbers "
        "from 0.009 to 101,325: seven orders of magnitude.",
        ha="center",
        fontsize=8,
        color=TEXT_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, 1, "fig01-unit-landscape")


if __name__ == "__main__":
    main()

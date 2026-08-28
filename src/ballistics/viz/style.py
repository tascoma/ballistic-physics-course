"""One visual language for every figure in the course.

The course ships roughly ninety static PNGs embedded in markdown lessons. They
have to read as one system, and they have to stay legible for colorblind readers
and in print. This module is the single place that decides how they look.

Why a fixed palette and not matplotlib's default cycle
------------------------------------------------------
Matplotlib cycles colors by *position in the plot call order*, which means the
same physical quantity changes color between figures, and a series dropped from
one chart repaints all the others. Here, color follows the *entity*: assign
slots explicitly and consistently, e.g. drag effects always slot 2, wind always
slot 3, across every module.

The palette below is the validated default from the ``dataviz`` skill, light
mode. It passed the lightness band, chroma floor, adjacent-pair colorblind
separation (worst adjacent dE 9.1), and normal-vision separation (worst 19.6)
checks against the light surface. Two consequences bind every figure:

* **Relief rule.** Slots 3 (aqua), 4 (yellow), and 5 (magenta) fall below 3:1
  contrast against the surface. Any figure using them must carry visible
  identity that is not color: a legend, direct labels, or both. Every figure in
  this course does anyway.
* **Scatter cap.** The adjacent-pair guarantee only covers forms where series
  sit next to each other (lines, stacked areas, grouped bars). For forms where
  every series can touch every other -- scatter, bubble, small multiples --
  only the first three slots are separation-safe. Use ``SCATTER_MAX_SERIES``.
  Past three, facet the chart or fold the tail into "other".

Figures are committed as PNGs on a light surface, so there is no dark variant:
a PNG cannot respond to the reader's theme. GitHub renders light images in dark
mode without complaint, which is why the surface is near-white rather than
transparent -- a transparent background would put dark ink on a dark page.
"""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib as mpl

# --- Surfaces and ink -------------------------------------------------------

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
TEXT_MUTED = "#87857c"
GRID = "#e2e1dc"
AXIS = "#c3c2b7"

# --- Categorical: assign by entity, in fixed order, never cycled ------------

PALETTE: tuple[str, ...] = (
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
)

#: Slots beyond this are not separation-safe when every series can neighbour
#: every other (scatter, bubble, small multiples). Facet or fold instead.
SCATTER_MAX_SERIES = 3

# --- Sequential: one hue, light to dark, for continuous magnitude -----------

SEQUENTIAL: tuple[str, ...] = (
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
)

#: For an *ordinal* ramp (discrete ordered categories) the lightest step must
#: still be visible against the surface: start no lighter than this index.
ORDINAL_MIN_INDEX = 3

# --- Diverging: two poles that read as opposite, neutral gray midpoint ------

DIVERGING_LOW = "#2a78d6"   # blue
DIVERGING_MID = "#f0efec"   # neutral gray -- never a hue at the midpoint
DIVERGING_HIGH = "#d03b3b"  # red

# --- Status: reserved meanings, never reused as "series 5" ------------------

STATUS = {
    "good": "#0ca30c",
    "warning": "#fab219",
    "serious": "#ec835a",
    "critical": "#d03b3b",
}

# --- Course-wide entity assignments ----------------------------------------

#: Physical effects keep the same color in every figure that shows them, so a
#: reader who learns "orange is wind" in Module 18 still reads it that way in
#: the capstone. Modules that plot these quantities must use these slots.
EFFECT_COLORS = {
    "vacuum": TEXT_MUTED,
    "drag": PALETTE[0],
    "wind": PALETTE[1],
    "spin_drift": PALETTE[2],
    "aero_jump": PALETTE[3],
    "coriolis": PALETTE[4],
    "measured": PALETTE[7],
}

FIGSIZE = (8.0, 5.0)
DPI = 200


def apply_style() -> None:
    """Install the course figure style into matplotlib's global rcParams.

    Call once at the top of every figure script, before creating any figure.
    Grid and axes are deliberately recessive: the data marks should be the
    highest-contrast thing on the canvas.
    """
    mpl.rcParams.update(
        {
            # Canvas
            "figure.figsize": FIGSIZE,
            "figure.dpi": DPI,
            "savefig.dpi": DPI,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.25,
            # Type -- text wears text tokens, never a series color
            "font.family": ["DejaVu Sans"],
            "font.size": 10,
            "text.color": TEXT_PRIMARY,
            "axes.titlesize": 12,
            "axes.titleweight": "medium",
            "axes.titlecolor": TEXT_PRIMARY,
            "axes.titlepad": 12,
            "axes.labelsize": 10,
            "axes.labelcolor": TEXT_SECONDARY,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "xtick.color": TEXT_SECONDARY,
            "ytick.color": TEXT_SECONDARY,
            # Recessive frame
            "axes.edgecolor": AXIS,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 3,
            "ytick.major.size": 3,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            # Recessive grid
            "axes.grid": True,
            "axes.grid.axis": "both",
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "grid.alpha": 1.0,
            "axes.axisbelow": True,
            # Marks
            "lines.linewidth": 1.8,
            "lines.markersize": 6,
            "lines.solid_capstyle": "round",
            "patch.linewidth": 0.0,
            "axes.prop_cycle": mpl.cycler(color=list(PALETTE)),
            # Legend -- always present for two or more series
            "legend.frameon": False,
            "legend.fontsize": 9,
            "legend.labelcolor": TEXT_SECONDARY,
            "legend.handlelength": 1.6,
            "legend.borderpad": 0.4,
            "legend.columnspacing": 1.4,
        }
    )


def cycle_colors(n: int, *, scatter: bool = False) -> list[str]:
    """Return the first ``n`` categorical slots, in fixed order.

    Args:
        n: Number of series.
        scatter: True for forms where any series can neighbour any other
            (scatter, bubble, small multiples), which caps the safe count at
            :data:`SCATTER_MAX_SERIES`.

    Raises:
        ValueError: If ``n`` exceeds what the palette can separate. This is a
            hard error rather than a wraparound on purpose -- a ninth series is
            never a generated hue. Facet the chart, or fold the tail into an
            "other" group.
    """
    limit = SCATTER_MAX_SERIES if scatter else len(PALETTE)
    if not 1 <= n <= limit:
        kind = "all-pairs (scatter-like)" if scatter else "adjacent-pair"
        raise ValueError(
            f"{n} series exceeds the {kind} separation limit of {limit}. "
            "Facet the chart or fold the tail into an 'other' group rather "
            "than generating a new hue."
        )
    return list(PALETTE[:n])


def sequential_steps(n: int, *, ordinal: bool = False) -> list[str]:
    """Return ``n`` evenly spaced steps from the sequential blue ramp.

    Args:
        n: Number of steps.
        ordinal: True for discrete ordered categories, which forbids steps so
            light they recede into the surface.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    lo = ORDINAL_MIN_INDEX if ordinal else 0
    hi = len(SEQUENTIAL) - 1
    if n == 1:
        return [SEQUENTIAL[hi]]
    span = hi - lo
    return [SEQUENTIAL[lo + round(i * span / (n - 1))] for i in range(n)]


def annotate_series(ax, x, y, label: str, color: str, *, dx: float = 0.0, dy: float = 0.0):
    """Direct-label a series at ``(x, y)`` in the ink color, not the series color.

    Direct labels are the preferred identity channel; the legend is the backup.
    The label wears a text token so that color never has to carry meaning alone.
    """
    return ax.annotate(
        label,
        xy=(x, y),
        xytext=(x + dx, y + dy),
        color=TEXT_SECONDARY,
        fontsize=9,
        va="center",
        bbox={"facecolor": SURFACE, "edgecolor": "none", "pad": 1.5, "alpha": 0.85},
    )


def cvd_safe_series(labels: Sequence[str], *, scatter: bool = False) -> dict[str, str]:
    """Map series labels to fixed palette slots, in the order given."""
    return dict(zip(labels, cycle_colors(len(labels), scatter=scatter), strict=True))

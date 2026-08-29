"""Figure m00-fig02-solution-pipeline.

What a ballistic solver actually is, as a diagram: four groups of measured
inputs, one model, four numbers out.

The point of the figure is the left-hand column. Every input is something a
human being has to measure with an instrument, and the accuracy of the whole
chain is bounded by the worst of them -- which is why Part IX exists. The module
references on each box are where that measurement's error is quantified.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import (
    GRID,
    PALETTE,
    SEQUENTIAL,
    SURFACE,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

INPUTS = [
    ("Load", "bullet, BC, muzzle velocity", "M13 · M24 · M28"),
    ("Atmosphere", "pressure, temperature, humidity", "M09 · M10"),
    ("Wind", "speed and direction, along the path", "M18 · M19"),
    ("Geometry", "range, sight height, zero, incline", "M08 · M23"),
]

OUTPUTS = [
    ("Elevation", "how much to come up", "MOA or mils"),
    ("Windage", "how much to hold off", "MOA or mils"),
    ("Time of flight", "how long until impact", "seconds"),
    ("Velocity", "and energy, at the target", "fps · ft·lb"),
]

MODEL_LINES = [
    "equations of motion",
    "integrated step by step",
    "",
    "drag from a $C_D$ curve",
    "+ spin drift",
    "+ aerodynamic jump",
    "+ Coriolis",
]

BOX_W, BOX_H = 0.235, 0.175
LEFT_X, RIGHT_X = 0.015, 0.75
MODEL_X, MODEL_W = 0.395, 0.21
ROW_Y = [0.75, 0.52, 0.29, 0.06]


def box(ax, x, y, w, h, *, face, edge, lw=1.1):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.004,rounding_size=0.012",
            facecolor=face,
            edgecolor=edge,
            linewidth=lw,
            zorder=2,
        )
    )


def arrow(ax, x0, y0, x1, y1, color):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.1,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=1,
        )
    )


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(11.0, 5.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.09, 1.0)
    ax.axis("off")

    model_mid_y = 0.5 * (ROW_Y[0] + BOX_H + ROW_Y[-1])

    # --- the model, drawn first so the arrows land on top of nothing ---------
    model_y0, model_y1 = ROW_Y[-1] + 0.005, ROW_Y[0] + BOX_H - 0.005
    box(
        ax,
        MODEL_X,
        model_y0,
        MODEL_W,
        model_y1 - model_y0,
        face=SEQUENTIAL[0],
        edge=PALETTE[0],
        lw=1.4,
    )
    ax.text(
        MODEL_X + MODEL_W / 2,
        model_y1 - 0.075,
        "THE MODEL",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=PALETTE[0],
    )
    # Centre the block between the title and the footer rather than hanging it
    # from the top, which leaves the box visibly bottom-empty.
    spacing = 0.055
    block_mid = 0.5 * ((model_y1 - 0.11) + (model_y0 + 0.08))
    block_top = block_mid + spacing * (len(MODEL_LINES) - 1) / 2.0
    for i, line in enumerate(MODEL_LINES):
        ax.text(
            MODEL_X + MODEL_W / 2,
            block_top - i * spacing,
            line,
            ha="center",
            va="center",
            fontsize=8.8,
            color=TEXT_SECONDARY,
        )
    ax.text(
        MODEL_X + MODEL_W / 2,
        model_y0 + 0.045,
        "Parts II–VIII",
        ha="center",
        va="center",
        fontsize=8,
        color=TEXT_MUTED,
    )

    # --- inputs and outputs -------------------------------------------------
    for row_y, (title, detail, modules) in zip(ROW_Y, INPUTS, strict=True):
        box(ax, LEFT_X, row_y, BOX_W, BOX_H, face=SURFACE, edge=GRID)
        ax.text(LEFT_X + 0.014, row_y + BOX_H - 0.048, title,
                fontsize=10, fontweight="bold", color=TEXT_PRIMARY, va="center")
        ax.text(LEFT_X + 0.014, row_y + BOX_H - 0.098, detail,
                fontsize=8.4, color=TEXT_SECONDARY, va="center")
        ax.text(LEFT_X + 0.014, row_y + 0.032, modules,
                fontsize=7.6, color=TEXT_MUTED, va="center")
        arrow(ax, LEFT_X + BOX_W, row_y + BOX_H / 2,
              MODEL_X, model_mid_y, PALETTE[0])

    for row_y, (title, detail, unit) in zip(ROW_Y, OUTPUTS, strict=True):
        box(ax, RIGHT_X, row_y, BOX_W, BOX_H, face=SURFACE, edge=GRID)
        ax.text(RIGHT_X + 0.014, row_y + BOX_H - 0.048, title,
                fontsize=10, fontweight="bold", color=TEXT_PRIMARY, va="center")
        ax.text(RIGHT_X + 0.014, row_y + BOX_H - 0.098, detail,
                fontsize=8.4, color=TEXT_SECONDARY, va="center")
        ax.text(RIGHT_X + 0.014, row_y + 0.032, unit,
                fontsize=7.6, color=TEXT_MUTED, va="center")
        arrow(ax, MODEL_X + MODEL_W, model_mid_y,
              RIGHT_X, row_y + BOX_H / 2, PALETTE[0])

    # --- column headings ----------------------------------------------------
    for x, label in (
        (LEFT_X + BOX_W / 2, "MEASURED INPUTS"),
        (RIGHT_X + BOX_W / 2, "THE FIRING SOLUTION"),
    ):
        ax.text(x, 0.955, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=TEXT_MUTED)

    # --- the actual point of the figure -------------------------------------
    ax.annotate(
        "Every box on this side is a number somebody had to measure.\n"
        "None of them is exact. Part IX (M24–M27) is about how wrong\n"
        "they are, and what that costs you at the target.",
        xy=(LEFT_X + BOX_W / 2, -0.005),
        ha="center",
        va="top",
        fontsize=8.6,
        color=TEXT_SECONDARY,
    )

    fig.tight_layout()
    save_figure(fig, 0, "fig02-solution-pipeline")


if __name__ == "__main__":
    main()

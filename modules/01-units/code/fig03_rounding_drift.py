"""Figure m01-fig03-rounding-drift.

What rounding an intermediate value to 3, 4, or 6 significant figures does to
the answer after a thousand steps.

The recurrence below is a deliberately trivial stand-in for a trajectory --
velocity decaying as the square of speed, position accumulating -- chosen so
its endpoint lands near 1000 yards after 1.5 seconds, which is roughly what the
course's running load does. It is **not** a ballistic solver and makes no claim
to be one; Module 05 writes the real integrator and Module 15 gives it real
physics. All this figure needs is a loop whose output depends on every step
before it, which is the property that makes rounding accumulate.

Only the *intermediate* is rounded. The position accumulator stays in float64
throughout, so the curves measure rounding propagating through the physics
rather than the coarseness of the output register.

No randomness, so this regenerates byte-identically by construction.
"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt

from ballistics.units import m_to_inches, m_to_yards
from ballistics.viz import apply_style, save_figure
from ballistics.viz.style import TEXT_MUTED, TEXT_SECONDARY, annotate_series, sequential_steps

#: Decay constant, 1/m, tuned so the float64 run covers ~1000 yd in 1.5 s.
K_PER_M = 0.000625
DT_S = 0.0015
N_STEPS = 1000
V0_MPS = 822.96          # 2700 fps, the running load

SIG_FIGS = (3, 4, 6)
PLATE_IN = 10.0          # the 10-inch plate from Module 00's scenario


def round_sig(value: float, digits: int) -> float:
    """Round to ``digits`` significant figures. Zero has no significant figures."""
    if value == 0.0:
        return 0.0
    return round(value, -int(math.floor(math.log10(abs(value)))) + (digits - 1))


def run(sig: int | None = None) -> list[float]:
    """Return downrange position in metres at each step, rounding v to ``sig`` figures."""
    velocity_mps, position_m = V0_MPS, 0.0
    track_m = []
    for _ in range(N_STEPS):
        velocity_mps -= K_PER_M * velocity_mps * velocity_mps * DT_S
        if sig is not None:
            velocity_mps = round_sig(velocity_mps, sig)
        position_m += velocity_mps * DT_S
        track_m.append(position_m)
    return track_m


def main() -> None:
    apply_style()

    reference_m = run()
    range_yd = [m_to_yards(x) for x in reference_m]

    fig, ax = plt.subplots(figsize=(8.4, 5.2))

    # Significant figures are an *ordered* category, so they get the ordinal
    # ramp rather than categorical hues: darker means more digits kept.
    colors = sequential_steps(len(SIG_FIGS), ordinal=True)

    ax.axhline(PLATE_IN, color=TEXT_MUTED, linewidth=1.0, zorder=2)
    ax.annotate(
        "a 10-inch plate",
        xy=(30, PLATE_IN),
        xytext=(0, 5),
        textcoords="offset points",
        fontsize=8.5,
        color=TEXT_MUTED,
    )

    for digits, color in zip(SIG_FIGS, colors, strict=True):
        track_m = run(digits)
        error_in = [abs(m_to_inches(a - b)) for a, b in zip(track_m, reference_m, strict=True)]
        ax.plot(range_yd, error_in, color=color, zorder=3)
        annotate_series(ax, range_yd[-1], error_in[-1], f"{digits} sig figs", color, dx=25)

    ax.set_yscale("log")
    ax.set_xlim(0, 1230)
    ax.set_ylim(1e-4, 4e4)
    ax.set_xlabel("downrange distance (yards)")
    ax.set_ylabel("error in position vs float64 (inches, log scale)")
    ax.set_title(
        "Rounding one intermediate value, 1000 times",
        loc="left",
    )
    fig.text(
        0.5,
        -0.03,
        "A stand-in decay recurrence, not a ballistic solver: velocity is rounded after each "
        "step, position is not.\nThe 3-sig-fig run stalls at 730 m/s, because the change per "
        "step falls below the last digit it keeps.",
        ha="center",
        fontsize=8,
        color=TEXT_MUTED,
    )
    ax.tick_params(axis="both", colors=TEXT_SECONDARY)
    fig.tight_layout()
    save_figure(fig, 1, "fig03-rounding-drift")


if __name__ == "__main__":
    main()

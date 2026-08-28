"""Scaffold smoke tests.

These check the infrastructure the whole course sits on: the package imports,
the figure style is installable, and the palette rules the ``dataviz`` skill
validated are actually enforced by the code rather than only documented.
"""

from __future__ import annotations

import matplotlib
import pytest

matplotlib.use("Agg")

import ballistics  # noqa: E402
from ballistics.viz import apply_style, figure_path  # noqa: E402
from ballistics.viz.style import (  # noqa: E402
    PALETTE,
    SCATTER_MAX_SERIES,
    SEQUENTIAL,
    cycle_colors,
    sequential_steps,
)


def test_package_imports():
    assert ballistics.__version__


def test_apply_style_is_idempotent():
    apply_style()
    apply_style()
    assert matplotlib.rcParams["lines.linewidth"] == 1.8


def test_palette_is_the_validated_eight():
    # These exact hexes, in this exact order, passed the dataviz validator's
    # adjacent-pair CVD and normal-vision gates on the light surface. Changing
    # one means re-running scripts/validate_palette.js, not editing this test.
    assert PALETTE[0] == "#2a78d6"
    assert len(PALETTE) == 8
    assert len(set(PALETTE)) == 8


def test_cycle_colors_is_stable_and_ordered():
    # Colour follows the entity, not the plot order: asking for fewer series
    # must not repaint the survivors.
    assert cycle_colors(3) == list(PALETTE[:3])
    assert cycle_colors(5)[:3] == cycle_colors(3)


def test_cycle_colors_refuses_to_invent_a_ninth_hue():
    with pytest.raises(ValueError, match="separation limit"):
        cycle_colors(len(PALETTE) + 1)


def test_scatter_forms_are_capped_at_three_series():
    # Under an all-pairs pairlist the fourth slot puts yellow beside orange,
    # which fails the separation floor. Facet instead.
    assert cycle_colors(SCATTER_MAX_SERIES, scatter=True)
    with pytest.raises(ValueError, match="all-pairs"):
        cycle_colors(SCATTER_MAX_SERIES + 1, scatter=True)


def test_sequential_ramp_is_light_to_dark_and_ordinal_clips_the_pale_end():
    assert sequential_steps(1) == [SEQUENTIAL[-1]]
    assert sequential_steps(4)[0] == SEQUENTIAL[0]
    # An ordinal ramp must not start so pale it recedes into the surface.
    assert sequential_steps(4, ordinal=True)[0] != SEQUENTIAL[0]


def test_figure_path_enforces_the_naming_convention():
    with pytest.raises(ValueError, match="mNN-figKK"):
        figure_path(7, "some_figure")


def test_figure_path_requires_the_module_to_exist():
    # Guards against a figure script silently writing into a directory that
    # does not correspond to any module.
    with pytest.raises(FileNotFoundError, match="new_module.py"):
        figure_path(99, "fig01-nonexistent")

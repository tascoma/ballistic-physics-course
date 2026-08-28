"""Figure infrastructure shared by every course module.

This subpackage is scaffolding, not course content: it exists so that all ~90
figures across the course share one visual language. Course modules import
``apply_style`` and ``save_figure`` and otherwise write plain matplotlib.
"""

from ballistics.viz.io import figure_path, module_dir, save_figure
from ballistics.viz.style import (
    DIVERGING_HIGH,
    DIVERGING_LOW,
    DIVERGING_MID,
    EFFECT_COLORS,
    PALETTE,
    SCATTER_MAX_SERIES,
    SEQUENTIAL,
    STATUS,
    annotate_series,
    apply_style,
    cvd_safe_series,
    cycle_colors,
    sequential_steps,
)

__all__ = [
    "DIVERGING_HIGH",
    "DIVERGING_LOW",
    "DIVERGING_MID",
    "EFFECT_COLORS",
    "PALETTE",
    "SCATTER_MAX_SERIES",
    "SEQUENTIAL",
    "STATUS",
    "annotate_series",
    "apply_style",
    "cvd_safe_series",
    "cycle_colors",
    "figure_path",
    "module_dir",
    "save_figure",
    "sequential_steps",
]

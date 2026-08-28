"""Where figures go, and how they get there.

Every figure in the course is produced by a script in ``modules/NN-slug/code/``
and lands in ``modules/NN-slug/assets/`` as a committed PNG, so the markdown
lesson renders on GitHub without anyone running any code.

Naming is mechanical so ``tools/build_figures.py`` and ``tools/check_curriculum.py``
can verify that every figure a lesson references actually exists:

    script:  modules/07-vacuum-trajectory/code/fig02_analytic_vs_rk4.py
    output:  modules/07-vacuum-trajectory/assets/m07-fig02-analytic-vs-rk4.png
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt

#: Repository root, found by walking up from this file (src/ballistics/viz/io.py).
REPO_ROOT = Path(__file__).resolve().parents[3]
MODULES_DIR = REPO_ROOT / "modules"


def module_dir(module_id: int | str) -> Path:
    """Return the directory for a module given its numeric id.

    Modules are named ``NN-slug``, and the slug is not passed in, so this
    globs for the one directory whose number matches.

    Raises:
        FileNotFoundError: If no module directory has that number.
        ValueError: If more than one does, which means someone created a
            duplicate and the repository is ambiguous.
    """
    nn = f"{int(module_id):02d}"
    matches = sorted(MODULES_DIR.glob(f"{nn}-*"))
    if not matches:
        raise FileNotFoundError(
            f"No module directory {nn}-* in {MODULES_DIR}. "
            f"Create it with: uv run python tools/new_module.py {nn}"
        )
    if len(matches) > 1:
        raise ValueError(f"Ambiguous module {nn}: {[m.name for m in matches]}")
    return matches[0]


def figure_path(module_id: int | str, name: str) -> Path:
    """Build the canonical asset path for a figure.

    Args:
        module_id: Module number, e.g. ``7`` or ``"07"``.
        name: Figure slug, e.g. ``"fig02-analytic-vs-rk4"``. A leading
            ``mNN-`` is added if absent.
    """
    nn = f"{int(module_id):02d}"
    slug = name if name.startswith(f"m{nn}-") else f"m{nn}-{name}"
    if not re.fullmatch(r"m\d{2}-fig\d{2}-[a-z0-9-]+", slug):
        raise ValueError(
            f"Figure name {slug!r} must match mNN-figKK-kebab-slug, "
            "e.g. m07-fig02-analytic-vs-rk4"
        )
    return module_dir(nn) / "assets" / f"{slug}.png"


def save_figure(fig, module_id: int | str, name: str, *, close: bool = True) -> Path:
    """Save a figure to its canonical path and report where it went.

    Prints the path so ``tools/build_figures.py`` output doubles as a manifest
    of what was regenerated.
    """
    path = figure_path(module_id, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    if close:
        plt.close(fig)
    print(f"  wrote {path.relative_to(REPO_ROOT)}")
    return path

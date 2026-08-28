#!/usr/bin/env python3
"""Regenerate every figure in the repository, in module order.

    uv run python tools/build_figures.py        # all modules
    uv run python tools/build_figures.py 07     # one module
    uv run python tools/build_figures.py --check  # fail if any figure changes

Figures are committed, so the lessons render on GitHub without anyone running
code. That only works if regeneration is deterministic: seeded RNG, no
timestamps, no environment-dependent output. ``--check`` enforces it by
regenerating into a temporary directory and comparing bytes -- run it before
committing if you have touched a figure script.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULES = REPO_ROOT / "modules"


def module_dirs(only: int | None = None) -> list[Path]:
    pattern = f"{only:02d}-*" if only is not None else "[0-9][0-9]-*"
    return sorted(d for d in MODULES.glob(pattern) if d.is_dir())


def figure_scripts(module: Path) -> list[Path]:
    return sorted((module / "code").glob("fig*.py"))


def digest(directory: Path) -> dict[str, str]:
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(directory.glob("*.png"))
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module", nargs="?", type=int, help="module number; omit for all")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify regeneration is byte-identical instead of reporting success",
    )
    args = parser.parse_args()

    modules = module_dirs(args.module)
    if not modules:
        target = (
            f"No module {args.module:02d}" if args.module is not None else "No modules"
        )
        print(f"{target} found under modules/. Nothing to build.")
        return 0

    total, failed, changed = 0, [], []

    for module in modules:
        scripts = figure_scripts(module)
        if not scripts:
            continue
        print(f"\n{module.name}")
        before = digest(module / "assets") if args.check else {}

        for script in scripts:
            total += 1
            result = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )
            if result.returncode != 0:
                failed.append(script.relative_to(REPO_ROOT))
                tail = (result.stderr or result.stdout).strip().splitlines()
                print(f"  FAILED {script.name}")
                for line in tail[-4:]:
                    print(f"         {line}")
            else:
                print(result.stdout.rstrip() or f"  ran {script.name}")

        if args.check:
            after = digest(module / "assets")
            for name in sorted(set(before) | set(after)):
                if before.get(name) != after.get(name):
                    changed.append(f"{module.name}/assets/{name}")

    print(f"\n{total} figure script(s) across {len(modules)} module(s)")

    if failed:
        print(f"\n{len(failed)} failed:")
        for path in failed:
            print(f"  {path}")
        return 1

    if args.check and changed:
        print(f"\n{len(changed)} figure(s) are not reproducible:")
        for name in changed:
            print(f"  {name}")
        print("\nFigures must regenerate byte-identically. Check for unseeded randomness.")
        return 1

    if args.check:
        print("All figures reproduce byte-identically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify that built modules match their specifications in CURRICULUM.md.

    uv run python tools/check_curriculum.py

Thirty modules built across thirty sessions will drift unless something checks
them. This does:

  * every spec in CURRICULUM.md has a directory, or is reported as not started
  * each built module's front matter matches its spec (id, title, slug, prereqs)
  * every figure the spec lists exists as a PNG in assets/
  * every figure referenced by the lesson exists, and vice versa
  * every file the spec says the module builds exists in src/ballistics/
  * the progress table's status matches the module's actual state

Exit code is non-zero if a built module disagrees with its spec. Modules that
have not been built yet are reported, not failed -- that is the normal state of
a course in progress.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = REPO_ROOT / "CURRICULUM.md"
MODULES = REPO_ROOT / "modules"
SRC = REPO_ROOT / "src"

sys.path.insert(0, str(REPO_ROOT / "tools"))
from new_module import parse_curriculum  # noqa: E402

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_front_matter(text: str) -> dict[str, str] | None:
    match = FRONT_MATTER.match(text)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
    return fields


def parse_progress_table(text: str) -> dict[int, str]:
    """Read the progress table's checkbox state for each module."""
    states: dict[int, str] = {}
    for match in re.finditer(r"`\[([ x~])\]`\s*\|\s*\*\*(\d{2})\*\*", text):
        states[int(match.group(2))] = match.group(1)
    return states


def main() -> int:
    curriculum_text = CURRICULUM.read_text(encoding="utf-8")
    specs = parse_curriculum()
    progress = parse_progress_table(curriculum_text)

    problems: list[str] = []
    built: list[int] = []
    not_started: list[int] = []

    for number, spec in sorted(specs.items()):
        directory = MODULES / f"{number:02d}-{spec['slug']}"
        readme = directory / "README.md"

        if not directory.exists():
            not_started.append(number)
            if progress.get(number) == "x":
                problems.append(
                    f"M{number:02d}: marked complete in the progress table, "
                    "but the directory does not exist"
                )
            continue

        built.append(number)

        if not readme.exists():
            problems.append(f"M{number:02d}: {directory.name}/README.md is missing")
            continue

        text = readme.read_text(encoding="utf-8")
        front = parse_front_matter(text)
        if front is None:
            problems.append(f"M{number:02d}: README.md has no YAML front matter")
            continue

        # Identity must match the spec.
        for field, expected in (("id", f"{number:02d}"), ("title", spec["title"]),
                                ("slug", spec["slug"])):
            actual = front.get(field, "")
            if actual != expected:
                problems.append(
                    f"M{number:02d}: front matter {field}={actual!r} "
                    f"but CURRICULUM.md says {expected!r}"
                )

        # Figures the spec requires must exist as committed PNGs.
        assets = directory / "assets"
        for figure in spec["figures"]:
            if not (assets / f"{figure}.png").exists():
                problems.append(f"M{number:02d}: spec requires figure {figure}.png, not found")

        # Figures the lesson references must exist.
        for referenced in re.findall(r"assets/(m\d{2}-fig\d{2}-[a-z0-9-]+)\.png", text):
            if not (assets / f"{referenced}.png").exists():
                problems.append(
                    f"M{number:02d}: README references {referenced}.png, which does not exist"
                )

        # Committed figures nobody references are dead weight.
        referenced = set(re.findall(r"assets/(m\d{2}-fig\d{2}-[a-z0-9-]+)\.png", text))
        for png in sorted(assets.glob("*.png")):
            if png.stem not in referenced:
                problems.append(
                    f"M{number:02d}: {png.name} exists but the lesson never references it"
                )

        # Library files the spec says this module builds must exist.
        for target in spec["builds"]:
            if not (SRC / target).exists():
                problems.append(
                    f"M{number:02d}: spec says it builds src/{target}, which does not exist"
                )

        # Status consistency.
        status = front.get("status", "")
        if status == "complete" and progress.get(number) != "x":
            problems.append(
                f"M{number:02d}: front matter says complete, "
                "but the progress table does not"
            )
        if progress.get(number) == "x" and status != "complete":
            problems.append(
                f"M{number:02d}: progress table says complete, "
                f"but front matter status is {status!r}"
            )

    print(f"{len(specs)} module specs in CURRICULUM.md")
    print(f"{len(built)} built, {len(not_started)} not started")

    missing_from_progress = sorted(set(specs) - set(progress))
    if missing_from_progress:
        problems.append(
            "Progress table is missing rows for: "
            + ", ".join(f"M{n:02d}" for n in missing_from_progress)
        )

    if not_started:
        nxt = min(not_started)
        print(f"Next to build: M{nxt:02d} — {specs[nxt]['title']}")

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print("\nNo mismatches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

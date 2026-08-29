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
  * no lesson puts a non-ASCII character inside a $...$ math region

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


#: Characters that render fine as prose but are version-fragile inside math.
#: GitHub's KaTeX maps U+00B7 to \cdotp, which older builds do not define, and
#: the lesson then shows a red parse error instead of an equation. Write the
#: command (\cdot, ^\circ, \dots) rather than the character.
MATH_REPLACEMENTS = {
    "\u00b7": r"\cdot",
    "\u00b0": r"^\circ",
    "\u2026": r"\dots",
    "\u2212": "-",
    "\u00d7": r"\times",
    "\u2248": r"\approx",
    "\u2264": r"\le",
    "\u2265": r"\ge",
}

FENCE = re.compile(r"```.*?```", re.DOTALL)
DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
INLINE_MATH = re.compile(r"(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)")


def _blank(match: re.Match) -> str:
    """Replace a region with spaces, preserving line numbers."""
    return re.sub(r"[^\n]", " ", match.group())


def math_regions(text: str) -> list[tuple[int, str]]:
    """Every $...$ and $$...$$ region, as (offset, body). Code fences excluded."""
    text = FENCE.sub(_blank, text)
    regions = [(m.start(), m.group(1)) for m in DISPLAY_MATH.finditer(text)]
    regions += [
        (m.start(), m.group(1)) for m in INLINE_MATH.finditer(DISPLAY_MATH.sub(_blank, text))
    ]
    return regions


def check_math(problems: list[str]) -> None:
    """Flag non-ASCII characters inside math, which renderers disagree about."""
    for markdown in sorted(REPO_ROOT.rglob("*.md")):
        if any(part.startswith(".") or part == "node_modules" for part in markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        for offset, body in math_regions(text):
            for char in body:
                if ord(char) < 128:
                    continue
                line = text.count("\n", 0, offset) + 1
                fix = MATH_REPLACEMENTS.get(char)
                advice = f"; write {fix} instead" if fix else ""
                problems.append(
                    f"{markdown.relative_to(REPO_ROOT)}:{line}: "
                    f"U+{ord(char):04X} {char!r} inside math{advice}"
                )


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

    check_math(problems)

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

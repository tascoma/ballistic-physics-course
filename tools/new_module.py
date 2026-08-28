#!/usr/bin/env python3
"""Scaffold a module directory from templates/module/.

    uv run python tools/new_module.py 07
    uv run python tools/new_module.py 07 --dry-run

The module's number, title, slug, part, and prerequisites are read out of
CURRICULUM.md rather than passed on the command line, so the scaffold cannot
drift from the spec. The spec heading it looks for is:

    ### M07 · Trajectory in a Vacuum

and the line after it:

    `modules/07-vacuum-trajectory/` · prereq M06 · ~3 h
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = REPO_ROOT / "CURRICULUM.md"
TEMPLATE = REPO_ROOT / "templates" / "module"
MODULES = REPO_ROOT / "modules"

SPEC_HEADING = re.compile(r"^### M(\d{2}) · (.+?)\s*$", re.MULTILINE)


def parse_curriculum() -> dict[int, dict]:
    """Extract every module spec's identity from CURRICULUM.md."""
    text = CURRICULUM.read_text(encoding="utf-8")
    specs: dict[int, dict] = {}
    headings = list(SPEC_HEADING.finditer(text))

    for i, match in enumerate(headings):
        number = int(match.group(1))
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        body = text[match.end() : end]

        path_match = re.search(r"`modules/(\d{2})-([a-z0-9-]+)/`", body)
        if not path_match:
            raise ValueError(
                f"Module {number:02d} spec has no `modules/NN-slug/` path line. "
                "Every spec must name its directory on the line after the heading."
            )

        # Prerequisites live on the same line as the directory path:
        #   `modules/15-equations-of-motion/` · prereq M14, M09, M05 · ~3.5 h
        path_line = body[path_match.start() : body.find("\n", path_match.start())]
        if re.search(r"prereq[s]?:?\s*all", path_line):
            prereqs = [n for n in range(number)]
        else:
            prereqs = [int(n) for n in re.findall(r"\bM(\d{2})\b", path_line)]

        # The part heading is the most recent "## Part ..." above this spec.
        part = ""
        for part_match in re.finditer(r"^## (Part .+?)\s*$", text[: match.start()], re.MULTILINE):
            part = part_match.group(1)

        specs[number] = {
            "id": number,
            "title": match.group(2).strip(),
            "slug": path_match.group(2),
            "part": part,
            "prereqs": prereqs,
            "builds": sorted(set(re.findall(r"`src/(ballistics/[a-z0-9_/]+\.py)`", body))),
            "figures": sorted(set(re.findall(r"`(m\d{2}-fig\d{2}-[a-z0-9-]+)`", body))),
        }

    return specs


def render_front_matter(spec: dict) -> str:
    def yaml_list(values) -> str:
        return "[" + ", ".join(str(v) for v in values) + "]"

    def yaml_strlist(values) -> str:
        return "[" + ", ".join(f'"{v}"' for v in values) + "]"

    return (
        "---\n"
        f"id: {spec['id']:02d}\n"
        f"title: {spec['title']}\n"
        f"slug: {spec['slug']}\n"
        f'part: "{spec["part"]}"\n'
        f"prereqs: {yaml_list(spec['prereqs'])}\n"
        f"builds: {yaml_strlist(spec['builds'])}\n"
        f"figures: {yaml_strlist(spec['figures'])}\n"
        "status: draft\n"
        "---\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int, help="module number, e.g. 7")
    parser.add_argument("--dry-run", action="store_true", help="print what would be created")
    args = parser.parse_args()

    specs = parse_curriculum()
    if args.number not in specs:
        print(f"No spec for module {args.number:02d} in CURRICULUM.md", file=sys.stderr)
        print(f"Specs found: {sorted(specs)}", file=sys.stderr)
        return 1

    spec = specs[args.number]
    target = MODULES / f"{spec['id']:02d}-{spec['slug']}"

    if target.exists() and not args.dry_run:
        print(f"{target.relative_to(REPO_ROOT)} already exists; refusing to overwrite.")
        return 1

    print(f"Module {spec['id']:02d} — {spec['title']}")
    print(f"  part:     {spec['part']}")
    print(f"  prereqs:  {spec['prereqs'] or 'none'}")
    print(f"  builds:   {spec['builds'] or 'nothing in the library'}")
    print(f"  figures:  {len(spec['figures'])}")
    print(f"  target:   {target.relative_to(REPO_ROOT)}")

    if args.dry_run:
        print("\n--dry-run: nothing written. Front matter would be:\n")
        print(render_front_matter(spec))
        return 0

    shutil.copytree(TEMPLATE, target)

    readme = target / "README.md"
    body = readme.read_text(encoding="utf-8")
    body = body.replace("{{FRONT_MATTER}}", render_front_matter(spec).rstrip("\n"))
    body = body.replace("{{NN}}", f"{spec['id']:02d}")
    body = body.replace("{{TITLE}}", spec["title"])
    readme.write_text(body, encoding="utf-8")

    # A figure stub per specified figure, so the author cannot forget one.
    for figure in spec["figures"]:
        fig_match = re.fullmatch(r"m\d{2}-(fig\d{2})-([a-z0-9-]+)", figure)
        if not fig_match:
            continue
        script = target / "code" / f"{fig_match.group(1)}_{fig_match.group(2).replace('-', '_')}.py"
        script.write_text(
            f'"""Figure {figure}.\n\nSee the spec for module {spec["id"]:02d} in CURRICULUM.md '
            f'for what this figure must show\nand what the reader should notice in it.\n"""\n\n'
            "import matplotlib.pyplot as plt\n\n"
            "from ballistics.viz import apply_style, save_figure\n\n\n"
            "def main() -> None:\n"
            "    apply_style()\n"
            "    fig, ax = plt.subplots()\n"
            "    raise NotImplementedError(\n"
            f'        "Figure {figure} is specified in CURRICULUM.md but not yet built."\n'
            "    )\n"
            f'    save_figure(fig, {spec["id"]}, "{figure}")\n\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n",
            encoding="utf-8",
        )

    print(f"\nCreated {target.relative_to(REPO_ROOT)} with {len(spec['figures'])} figure stubs.")
    print("Next: write the library code and its tests, then the lesson.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

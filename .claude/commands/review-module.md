---
description: Review a finished course module against the authoring contract
argument-hint: <module number, e.g. 07>
---

Review module **$1** against its specification and the authoring contract.
Report findings; do not fix anything unless asked.

Read the spec for module $1 in `CURRICULUM.md`, then `CLAUDE.md` and
`docs/style-guide.md`, then the module itself.

## Check, in this order

**Correctness first.** The physics and the mathematics.
- Is every derivation actually valid, with no skipped steps that hide an error?
- Do the numbers in the worked example reproduce? Run them.
- Do the numbers in the lesson prose match what the code produces?
- Are the sign conventions right — wind direction, twist hand, hemisphere —
  checked against `docs/units-and-conventions.md` §4 rather than assumed?
- Are unit conversions correct, especially anything touching BC in lb/in²?

**Spec compliance.**
- Every learning objective in the spec addressed?
- Every figure the spec lists present, and does it show what the spec says?
- Every file the spec says it builds present, with the specified API?
- Tests present, including the limiting-case check the spec names?
- Front matter matches the spec?

**The honesty rule.**
- Is any empirical model presented as a derivation?
- Is every imported model's source named and validity range stated?
- Is synthetic data labelled synthetic in the file, the lesson, *and*
  `data/README.md`?
- Are assumptions stated where they are made?

**Figures.**
- Does every figure have both a caption and a "what to notice"?
- Any figure that teaches nothing the prose cannot — cut it.
- Colour by entity, not plot order? `EFFECT_COLORS` used where applicable?
- Any dual y-axis? Any exaggerated vertical scale not stated in the caption?
- Does `uv run python tools/build_figures.py $1 --check` pass?

**Scope.**
- Does it run ahead into a later module's material?
- Does it silently change an earlier public API? (Three such changes are
  anticipated and listed in `CURRICULUM.md`; a fourth is a design problem.)

**Writing.**
- Filler phrases, overselling, hedging?
- Does it explain *why* before *what*?
- Would a reader with algebra and trig, and every prior module, actually follow it?

## Then run

```bash
uv run pytest
uv run python tools/build_figures.py $1 --check
uv run python tools/check_curriculum.py
uv run ruff check .
```

Report findings ranked by severity, with file and line references. Distinguish
errors from suggestions.

# Style guide

How the course reads, sounds, and looks. [`CLAUDE.md`](../CLAUDE.md) is the
procedure; this is the craft.

---

## Voice

**Write to a competent adult who does not yet know this specific thing.** The
reader has a rifle, some patience, and no physics degree. They are not a
beginner at everything — just at this.

**Explain the why before the what.** A formula without its motivation is a
lookup table, and the reader already has a ballistic app if that is all they
want. The entire premise of the course is that understanding beats trusting.

**Prefer the concrete.** "At 1000 yards a 10 mph crosswind moves your impact
about 70 inches" beats "crosswind deflection is significant at long range."

**Do not oversell.** Not everything is surprising, critical, or crucial. Save
the emphasis for the genuinely counterintuitive results — and the course has
several: humid air is lighter, extreme spread grows with sample size, a
crosswind moves impact vertically, wind deflection is a tenth of the naive
estimate.

**Admit uncertainty.** "Published models disagree here by about 15%; both are
shown" is better writing than picking one and sounding confident.

**No filler.** Cut "it is important to note that", "as we will see", "simply",
"just", "obviously". If it is obvious, the reader does not need the sentence.

---

## Structure

Follow the twelve-section lesson order in `CLAUDE.md`. Within a section:

- **Short paragraphs.** Three to five sentences.
- **One idea per paragraph.**
- **Tables for anything with more than three parallel items.**
- **Bold for the load-bearing claim** in a dense paragraph, sparingly.
- **Headings that state a claim**, not a topic: "Why humid air is lighter" beats
  "Humidity".

---

## Mathematics

- LaTeX in `$...$` inline and `$$...$$` for display. GitHub renders both.
- **Show every step.** The reader is here to follow a derivation, not to
  recognise one.
- Define every symbol on first use in a module, even if it is in
  [`notation.md`](notation.md).
- Give the physical meaning of a result immediately after stating it.
- Every module gets **one worked numeric example** in shooting units, carried
  through completely.
- Box or table the key result so it can be found again without re-reading.

---

## Code

- The lesson shows the code **that matters**. Not the imports, not the
  boilerplate, not the whole file.
- Explain the design, not the syntax. *Why* is `Conditions` a frozen dataclass?
  Why PCHIP and not a cubic spline?
- Docstrings state units for every argument and return value.
- Comments explain **why**, never what. `# convert to SI` on a line that
  converts to SI is noise; `# Miller's rule is dimensional and native to
  imperial units` is not.
- Names carry units (`range_m`), and read as English at the call site.
- Prefer clear over clever. This is teaching code that also has to be correct.

---

## Figures

Read the `dataviz` skill before writing figure code. The rules that bind:

- `apply_style()` first, `save_figure()` last.
- **Colour follows the entity.** Use `EFFECT_COLORS` for physical effects so
  that "orange is wind" holds across thirty modules.
- Legend for two or more series; direct labels too, for four or fewer.
- Never a dual y-axis. Two scales means two panels.
- Log scales when the data spans orders of magnitude — which, in this course,
  is often. Say so in the caption.
- Exaggerated vertical scales on trajectory plots **must** be stated in the
  caption. An unlabelled exaggerated trajectory teaches a false mental picture.
- Annotate the interesting point on the plot itself. If the reader has to hunt
  for what you meant, the annotation was the missing part.

**Every figure gets a caption and a "what to notice".** The caption says what is
plotted. The "what to notice" says what it means. A figure with nothing to
notice should be cut — decoration is not the standard.

---

## Units in prose

**Prose and figures use imperial**; the audience is shooters. **Code uses SI.**
Give the SI equivalent in parentheses where it aids understanding, not
reflexively.

Ranges in yards. Drop and drift in inches, and in MOA or mils where that is how
you would dial it. Velocity in fps. Bullet mass in grains. Temperature in
Fahrenheit. Pressure in inHg, since that is what the meter reads.

---

## Honesty

From [`CLAUDE.md`](../CLAUDE.md), because it is a writing rule as much as a
technical one:

- Say when a model is an empirical fit rather than a derivation.
- Name the source and the validity range.
- Show model disagreement rather than picking one silently.
- Label synthetic data as synthetic, in the file, the lesson, and `data/README.md`.
- State assumptions where they are made, not in a closing caveat nobody reads.

The reader must always be able to tell which of their numbers are physics and
which are curve fits. That distinction is what separates this course from a
manual, and it is worth some awkward sentences to preserve.

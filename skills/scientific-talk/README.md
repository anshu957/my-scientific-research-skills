# scientific-talk

A [Claude Code](https://claude.com/claude-code) skill for building scientific
talk decks — journal clubs, lab meetings, conference talks — that are
figure-forward, one claim per slide, and structured as an argument rather than a
summary.

It is opinionated on purpose. A talk is not a document: the audience gets one
pass, at your pace, from the back of a room. So the figures are the content, each
slide makes one claim that its figure actually demonstrates, and everything else
— the n's, the statistics, the caveats — goes into the speaker notes, where a
presenter can use it and an audience is not asked to read it.

```
┌──────────────────────────────────────────────────────────────┐
│ Measure | Trajectories split at about 70 days                │  ← the claim
│                                                               │
│        ┌───────────────────────┐    diverge, then die         │  ← ≤2 short labels
│        │                       │                              │
│        │      one figure       │    Groups separate a hundred │  ← one takeaway line
│        │                       │    days before any death.    │
│        └───────────────────────┘    Fig. 3B                   │  ← provenance
│                                                               │
│ LAB NAME — INSTITUTION                                     14 │
└──────────────────────────────────────────────────────────────┘
```

## What it does

- **Measures your house style** off a reference deck (your own past talk) with
  `inspect_pdf.py` — page size, type sizes, accent colour, footer geometry — so
  the output looks like your slides, not like a template.
- **Cuts panels out of journal figures** reproducibly. Crop rectangles live in
  `crops.json` in PDF points, so a crop can be nudged and re-run. Handles the
  things that make this annoying in practice: neighbouring panels bleeding into a
  rectangular crop (`whiteout`), colour washes from zoom connectors (`detint`),
  and **progressive builds** — two crops of the same rectangle with different
  whiteouts give identical size and position with panels revealed one click at a
  time.
- **Builds the .pptx** from a single JSON file holding every word and each
  slide's panels, so slide order and figures cannot drift apart. Text stays
  editable; nothing is baked into an image. Layout is chosen to make the figure
  as large as the slide allows.
- **Checks the layout** and renders PIL previews from the *same* geometry the
  .pptx gets, so you can see the deck without opening PowerPoint: headline
  overflow, takeaway wrap, figures leaving the body area or shrunk below print
  size, overlapping shapes.
- **Carries the craft**, not just the mechanics: `references/talk-craft.md` is a
  review checklist for the things that actually sink talks — an arc that lists
  instead of building, headlines whose figures do not show the claim, panels
  designed for a reader rather than a viewer — plus a delivery plan (time budget,
  planned pauses, how to frame someone else's work in a journal club).

## Install

```bash
git clone https://github.com/<you>/scientific-talk ~/.claude/skills/scientific-talk
```

Any location Claude Code loads skills from works — `~/.claude/skills/` for all
projects, `.claude/skills/` inside a project for one. Then just ask:

> make a journal club deck from this paper — 50 minutes, figure-forward

Requirements: Python 3.9+, `pymupdf`, `pillow`, `python-pptx` (and `matplotlib`
for the example). An Arial-like TTF is used for text measurement; macOS and most
Linux font packages have one.

```bash
pip install pymupdf pillow python-pptx matplotlib
```

## Try the example

Nothing in the example is copyrighted: it generates a synthetic multi-panel
"journal figure", then takes it apart into a talk.

```bash
cd example
python3 make_source_figure.py                      # -> source_figure.pdf
python3 ../scripts/crop_panels.py .                # -> figures/panels/*.png
python3 ../scripts/build_deck.py .                 # -> talk.pptx
python3 ../scripts/preview_deck.py . --sheets      # -> figures/preview/*.png
```

`example/narrative.json` is worth reading: it shows a title slide, a statement
slide, a two-step build, a two-panel result slide, a summary whose headline is an
assertion, a limitations slide, and a backup slide.

## Using your own style

```bash
python3 scripts/inspect_pdf.py your_old_deck.pdf --pages
python3 scripts/inspect_pdf.py your_old_deck.pdf --spans 5      # sizes, fonts, colours
python3 scripts/inspect_pdf.py your_old_deck.pdf --drawings 5   # rules, bands
python3 scripts/inspect_pdf.py your_old_deck.pdf --render 5     # then look at it
```

Put the resulting spec in `assets/local/design_spec.local.json` (git-ignored,
along with any logos in `assets/local/`) and every future deck picks it up. A
single talk can override it with a `design_spec.json` of its own.

Resolution order: `<talk>/design_spec.json` → `assets/local/design_spec.local.json`
→ `assets/design_spec.example.json`.

## Layout

```
scientific-talk/
├── SKILL.md                     the workflow Claude follows
├── scripts/
│   ├── inspect_pdf.py           measure a reference deck
│   ├── crop_panels.py           crops.json -> 400-dpi panel PNGs
│   ├── build_deck.py            design_spec + narrative + panels -> .pptx
│   └── preview_deck.py          same geometry, rendered with PIL
├── references/
│   ├── talk-craft.md            review checklist + delivery plan
│   ├── narrative-schema.md      every field of narrative.json
│   └── design-spec.md           how to measure a house style
├── assets/
│   ├── design_spec.example.json neutral default
│   └── local/                   your spec and logos (git-ignored)
└── example/                     runnable worked example
```

## Notes

The craft in `references/talk-craft.md` owes an obvious debt to Jean-luc
Doumont's *Trees, maps and theorems*, Michael Alley's assertion–evidence format,
and Susan McConnell's talks on designing scientific presentations. The text is
original; the ideas are theirs and worth reading in full.

Slide decks you build are yours. Note that figure panels cropped from a published
paper are the publisher's — fine for presenting, not for redistribution, so keep
built decks and cropped panels out of public repositories (this repo's
`.gitignore` already does that for you).

MIT licensed.

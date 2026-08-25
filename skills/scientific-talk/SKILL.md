---
name: scientific-talk
description: Build a scientific talk deck (.pptx) — journal club on a paper, lab meeting, conference talk, thesis committee, or a talk from the user's own notes and figures — that is figure-forward, one claim per slide, arc-driven, and matched to the user's house style. Use this whenever the user asks for slides, a deck, a presentation, a journal club, "present this paper", "make slides from these figures/results", or wants an existing deck restructured, tightened, or reviewed for talk quality. Also use it when someone asks how to organize or deliver a scientific talk, since it carries the arc, slide-grammar, and delivery conventions.
---

# Scientific talk decks

A talk is not a document. The audience gets one pass, at your pace, from the back
of a room. That single constraint drives everything here: figures are the content,
each slide makes one claim its figure actually demonstrates, and the density that
would be a paragraph on a slide goes into the speaker notes where it belongs.

The failure mode this skill exists to prevent is the deck that is really a
summary: correct, dense, and unwatchable — a list of six true things instead of
an argument that builds.

## Workflow

Six phases. Do not skip 1 — the arc is the deliverable that everything else
serves, and it is much cheaper to fix a story before 30 slides exist.

### 1. Establish the house style

If the user names or supplies a reference deck (their own past talk, a lab
template), measure it — do not eyeball it:

```bash
python3 <skill>/scripts/inspect_pdf.py ref.pdf --pages
python3 <skill>/scripts/inspect_pdf.py ref.pdf --spans 5     # sizes, fonts, colours
python3 <skill>/scripts/inspect_pdf.py ref.pdf --drawings 5  # rules, bands
python3 <skill>/scripts/inspect_pdf.py ref.pdf --render 5    # then Read the PNG
```

Write the numbers into `design_spec.json` in the talk directory
(`references/design-spec.md` has the schema and the measuring recipe). With no
reference deck, `assets/design_spec.example.json` is the default: 720 × 405 pt,
`Section |` in black + the claim in dark red, one figure, one italic takeaway,
a footer rule, no logos. Ask whose name, logo and colour belong on it rather
than assuming — and once you know, keep that spec as
`assets/local/design_spec.local.json`, which overrides the example for every
future talk.

Imitating the user's own deck matters more than any aesthetic preference of
yours: the audience already reads that layout fluently, and the user will not
have to re-learn their own slides the morning of the talk.

### 2. Decide the arc, in writing, before any slide exists

Write `ARC.md`: the through-line in one sentence, the movements, and a
slide-by-slide table (number, section, the claim, which figure carries it).
Get it right here — inserting a slide later is cheap, re-deriving the story is not.

Two starting shapes, both of which you should adapt rather than fill in:

- **Journal club** — Setup (what could not be done before) → Measure (how they
  built the readout) → Reduce (how the data became analyzable) → Result →
  Validate (why you believe it) → Predict/Perturb → Summary + limitations.
- **Own data** — Question → Why it was not answerable → What we built →
  What we found (one movement per real finding) → What it means → What is next.

Three properties make an arc rather than a list, and they are worth checking
explicitly before you build:

1. **The payoff is promised in the first 90 seconds.** Say the punchline on
   slide 2 and the methods become evidence the audience is auditing rather than
   a toll they are paying.
2. **Read the headlines in order, as a list, with nothing else.** They should
   narrate the argument on their own. If two consecutive headlines could swap
   without loss, the middle is a list — fix it there, not with transitions.
3. **Every section hands off.** The last slide of a movement raises the question
   the next one answers.

Also decide the **time budget** now: roughly 1.5–2 min per content slide, and
for a discussion format target ~45 min of material in a 60-min slot, because the
rest will be taken by interruption whether or not you plan for it.

### 3. Cut the panels

Journal figures are built for a reader with unlimited time. Cut them down.

```bash
python3 <skill>/scripts/crop_panels.py . --labels fig 2   # panel-label bboxes on a page
python3 <skill>/scripts/crop_panels.py . --page fig 2     # render the page, then Read it
python3 <skill>/scripts/crop_panels.py .                  # render every crop in crops.json
```

Panel labels (bold, ≥ 9.5 pt) give you the anchor coordinates; the rendered page
tells you where the panel actually ends. Write rectangles in POINTS into
`crops.json` so they can be nudged and re-run.

Then **look at every crop you made** (a contact sheet is fastest). Multi-panel
journal figures bleed into each other: expect clipped axis labels and stray
glyphs from neighbours. Fix by adjusting the rectangle, or by painting the
intruder out with `whiteout` — that is what it is for.

Three moves that are worth reaching for, because they turn a paper figure into a
slide figure:

- **Split a panel across slides** when its headline promises more than one thing.
- **Zoom** — one row of a 45-row panel, blown up, before the full texture.
- **Build** — the same crop twice with different `whiteout` rectangles gives
  identical size and position with panels revealed one click at a time. Use it
  for the payoff slide and anywhere a busy panel hides the thing you are pointing at.

### 4. Write the words

All words live in `narrative.json` (schema: `references/narrative-schema.md`),
including each slide's panels, so slide order and figures cannot drift apart.

Per slide: `section`, `headline` (the claim, ≤ 90 chars), `takeaway` (one
sentence, ≤ 165 chars), `credit`, ≤ 2 `annotations` (≤ 30 chars), and `notes`.

- The **headline is an assertion, not a topic** — "Trajectories split at about
  70 days", not "Aging trajectories". A question works when the next slide
  answers it.
- The figure on the slide must **demonstrate that exact claim**. If the headline
  says "not body size", the body-size panel is on the slide; if it is only in the
  notes, either add the panel or weaken the claim. This is the single most common
  defect in otherwise good decks, and a sharp audience always catches it.
- **The notes carry everything else**: n's, statistics, methods, caveats, and
  the delivery cues (`POINT`, `SAY`, `MY READ`, `PAUSE`, `IF SHORT`). Notes are
  spoken, so write them as cues, not paragraphs to be read aloud.
- Every number must come from the source. Keep a "verified numbers" block in
  `ARC.md` and pull from it rather than from memory.

### 5. Build and QA — look at the slides

```bash
python3 <skill>/scripts/build_deck.py .              # -> the .pptx + layout warnings
python3 <skill>/scripts/preview_deck.py . --sheets   # PIL previews + contact sheets
python3 <skill>/scripts/preview_deck.py . --clean    # remove them when done
```

The builder warns about headline overflow, takeaway wrap, figures leaving the
body area or shrunk below 0.7× print size, and overlapping shapes. Warnings are
necessary, not sufficient: **Read the contact sheets**. Ask of each slide, from
the back of the room — can I read the claim in three seconds, is the figure as
large as the slide allows, is my eye led to the thing being claimed?

The most common silent defect is a figure that is height-capped while a third of
the slide width sits empty. The builder already prefers whichever layout makes
the figure bigger; if a slide still looks starved, shorten the headline to one
line (that alone buys ~28 pt of figure height) or split the slide.

### 6. Review the talk, not just the slides

Before declaring it done, run the checklist in `references/talk-craft.md`
(assertion–evidence mismatches, slides that earn their place, builds, backups,
speaker-notes shape, delivery plan). If subagents are available and the user has
opted into that, a fresh reviewer agent with that checklist finds things the
builder cannot see; otherwise walk it yourself.

Then deliver, alongside the .pptx: `ARC.md` (the plan), `narrative.json` (where
to edit words), and a short delivery plan — per-section time budget, 3–4 planned
pause-and-ask points, and, for a journal club, how to frame someone else's work.

## Hard limits

| element | limit | why |
|---|---|---|
| headline | ≤ 90 chars, ≤ 2 lines | a third line eats the figure and stops being readable at a glance |
| takeaway | ≤ 165 chars, one sentence | it is a line to land, not a paragraph to read |
| annotations | ≤ 2, ≤ 30 chars | more than two and they compete with the figure |
| bullets | summary slide only | bullets on a data slide mean the figure is not carrying it |
| figures per slide | 1, sometimes 2 tightly related | two claims on one slide means neither lands |
| body text | none | if it must be said and not shown, it belongs in the notes |

## Working with the user's own material

When the talk is the user's own work rather than a paper, the workflow is
unchanged but the inputs differ: figures come from their files (PDF/PNG/SVG —
crop the same way, or place directly if already single-panel), and numbers come
from their notes. Ask for what is missing rather than inventing it, and mark any
claim you inferred so they can check it. Their unpublished results deserve the
same assertion–evidence discipline as a published paper's.

## Scaling with subagents

For a full-length deck the phases parallelize cleanly — style measurement, panel
cropping, and narrative writing are independent, and a reviewer pass at the end
is a separate job. Only fan out if the user has asked for multi-agent work; the
arc (phase 2) stays with you either way, because it is the one thing that must
be coherent across every slide.

## Bundled resources

- `scripts/inspect_pdf.py` — measure a reference deck (spans, colours, drawings, render)
- `scripts/crop_panels.py` — `crops.json` → 400-dpi panel PNGs; label finder; whiteout/detint/builds
- `scripts/build_deck.py` — `design_spec.json` + `narrative.json` + panels → .pptx, with layout checks
- `scripts/preview_deck.py` — the same geometry rendered with PIL, so preview and .pptx cannot drift
- `references/talk-craft.md` — the review checklist and the delivery plan (read it in phase 6, or earlier when planning the arc)
- `references/narrative-schema.md` — every field, the layout rules, builds, backup slides
- `references/design-spec.md` — how to measure a house style; the full spec schema
- `example/` — a runnable worked example built from a synthetic figure
- `assets/design_spec.example.json` — a neutral, unbranded default style
- `assets/local/` — your own spec and logos, if you have them (git-ignored)

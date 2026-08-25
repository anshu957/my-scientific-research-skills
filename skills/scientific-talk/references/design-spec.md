# design_spec.json — measuring and encoding a house style

The builder invents no look of its own: every coordinate, size and colour comes
from this file. It is resolved in this order, first hit wins:

1. `design_spec.json` in the talk directory — this talk only
2. `assets/local/design_spec.local.json` — your house style, git-ignored
3. `assets/design_spec.example.json` — the bundled neutral default

## Measuring a reference deck

Export the deck to PDF, then measure rather than guess — a style copied by eye is
recognizably not the user's style, and that is the first thing they notice.

```bash
python3 scripts/inspect_pdf.py ref.pdf --pages          # page size in points, slide list
python3 scripts/inspect_pdf.py ref.pdf --spans 5        # bbox, size, font, colour per span
python3 scripts/inspect_pdf.py ref.pdf --drawings 5     # filled rects/polys: rules, bands
python3 scripts/inspect_pdf.py ref.pdf --images 5       # logo bboxes
python3 scripts/inspect_pdf.py ref.pdf --render 5       # PNG — Read it to confirm placement
```

Sample at least four slides: the title slide, a results slide with a takeaway,
the busiest slide, and the summary. Take from them:

- page size; headline left margin, baseline, size, line spacing, and its two-tone
  structure (section vs claim colour);
- the takeaway's size/style/colour and where it sits relative to the figure;
- the credit style; the footer rule y/thickness/colour and its text style;
- the title slide: title block, accent band, logo boxes, presenter/date block.

Colours print as `RRGGBB`, ready to paste.

## Schema

```json
{
  "deck":   {"out": "talk.pptx"},
  "page":   {"w": 720, "h": 405},
  "fonts":  {"headline": {"name": "Arial", "size": 26, "bold": true},
             "takeaway": {"name": "Arial", "size": 14, "italic": true},
             "credit":   {"name": "Arial", "size": 12},
             "footer":   {"name": "Arial", "size": 10.5, "bold": true},
             "body":     {"name": "Arial", "size": 14}},
  "colors": {"headline_section": "000000", "headline_claim": "980000",
             "takeaway": "000000", "credit": "000000", "citation": "005789",
             "footer_text": "04A7F1", "footer_rule": "04A7F1", "accent_band": "04A7F1"},
  "headline":  {"x": 6.8, "y": 3.3, "max_w": 700, "line_spacing": 35.9},
  "body_area": {"x": 8, "y": 46, "w": 704, "h": 260},
  "takeaway":  {"x": 32, "y": 312, "max_w": 640},
  "credit":    {"x": 18, "y": 350},
  "footer":    {"rule_y": 376, "rule_h": 2.7, "text_x": 12.2, "text_y": 383.5,
                "text": "LAB NAME — INSTITUTION",
                "chevron": [[175.5, 377.3], [193.6, 377.3], [175.5, 398.7]]},
  "title_slide": {"title": {"x": 43.9, "y": 110.6, "max_w": 650, "size": 28},
                  "citation_y": 212.0,
                  "band": {"x": 0, "y": 320.9, "w": 720, "h": 84.1},
                  "band_notch": [[177.6, 337.5], [231.6, 337.5], [231.6, 391.0]],
                  "logos": [{"path": "lab_logo.png",
                             "x": 23.94, "y": 338.32, "w": 151.16, "h": 39.58}],
                  "meta": {"x": 460.0, "y": 336.7, "size": 13.5}},
  "observations": ["free-text notes for the builder"]
}
```

All lengths are POINTS with origin at the top-left of the slide.

- `body_area` is the band figures are placed in; its floor is overridden by the
  builder (306 pt with a takeaway underneath, 372 pt with a side takeaway).
- `chevron` / `band_notch` are optional decorative polygons — omit the keys
  entirely for a plain style.
- `logos` are resolved against `figures/logos/` in the talk directory, then
  `assets/local/`, then `assets/`. Missing files are skipped, not fatal, so a
  spec with logos still builds on a machine that does not have them.
- Use font families PowerPoint can resolve on the presenting machine (Arial is
  the safe default); note the true font of the reference deck in `observations`.

## Adapting to a different house style

Change the spec, not the builder. A different lab usually means: page size,
`headline_claim` colour, footer text/colour, logos, and the title band. Everything
downstream — layout choice, auto-shrink, warnings — follows automatically.

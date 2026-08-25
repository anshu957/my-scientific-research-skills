---
name: figure-hygiene
description: Produce clean, publication-quality scientific figures. Governs what goes inside a figure (one title = the key biological question, only strictly-necessary labels, NO explanatory/stats text on the plot) AND how it is rendered and saved (vector PDF into figures/, stable overwrite-able name, a journal rcParams style, a colorblind-safe palette). All figure detail (method, stats, how to read it) goes in a figure_captions.md kept in sync. Use whenever creating or editing any figure or plot in a scientific project.
---

# Figure hygiene

The plot shows data; words go in the caption file. Every figure is spare — and it
leaves the machine as a publication-grade vector file, not a screenshot.

## Workflow

1. **Look at the data first.** Read a few rows / dtypes / shape before plotting.
   Verify any library API you call actually exists in the installed version.
2. **Pick the narrowest plot** that answers the one question. Big matrix → cluster
   it; group comparison → box/strip, not a bar of means.
3. **Show what the labels claim.** If the figure asserts structure, the figure must
   *show* the evidence for it — never just assert it in an axis label. Clustering a
   matrix means drawing the **dendrogram(s)** (use `seaborn.clustermap`, not a
   reordered `imshow`); a heatmap whose axis says "clustered" with no visible tree is
   an unverifiable claim. If a grouping variable matters (sex, condition, genotype),
   annotate it as **row/column colors** with a small legend, so the reader can see
   whether the structure lines up with it.
4. **Style, then render** (sections below).
5. **QA — run the bundled checker, then look.** From the experiment folder:
   `python3 <skill>/qa.py .` — it renders every PDF in `figures/` to a PNG in
   `figures/_figqa/`, flags rasters, off-column sizes, and any figure missing a
   caption entry (nonzero exit if a rule is violated). **Then actually open the
   PNGs** and check: nothing clipped, every glyph legible at print size, colors
   distinguishable in grayscale/colorblind. A figure you have not looked at is not
   done. Clean up with `python3 <skill>/qa.py --clean .`.
6. **Write the caption entry** before you call it done.

## Inside the figure
- Exactly **one title**: the key biological question the figure answers (e.g. "Which
  syllables does each mutant use differently from its control?"). No subtitle, no
  second title.
- Axis labels and a legend **only where strictly necessary** — no restating obvious
  axes, no repeated units, no legend if one series.
- **No** explanatory sentences, method notes, footnotes, asterisk keys, or
  interpretation text drawn on the figure.

## Output contract
- **Vector PDF only**, saved into a `figures/` folder in the experiment directory.
  Never a raster screenshot; never a second parallel format (no `.png` twin).
- **Stable, descriptive filename** (`NN_slug.pdf`) so re-running **overwrites** the
  same file. No `_v2`, no timestamps, no per-iteration variants. Delete a figure you
  supersede in the same step.
- `savefig(path, bbox_inches="tight", pad_inches=0.03)` so nothing is cropped and
  there is no giant margin. Keep text as text (do not rasterize the whole figure);
  rasterize only heavy layers (e.g. a dense heatmap image) if file size demands it.

## Publication style
Set once, before plotting (matplotlib):

```python
import matplotlib as mpl
mpl.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300,
    "font.family": "sans-serif", "font.size": 8,
    "axes.titlesize": 9, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.8, "xtick.direction": "out", "ytick.direction": "out",
    "lines.linewidth": 1.2, "pdf.fonttype": 42, "ps.fonttype": 42,  # editable text in PDF
})
```

- **Size to the column, not to the default box.** Single column ≈ 3.3 in (~85 mm)
  wide; double column ≈ 6.9 in (~175 mm). Set `figsize` explicitly; don't ship
  seaborn's default aspect.
- **Despine** (top/right off, done above); thin spines and ticks.
- Keep tick counts low; drop chartjunk gridlines unless they aid reading.

## Palette
Use one fixed, colorblind-safe set across all figures in a project (Okabe–Ito):

```python
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#CC79A7",
             "#E69F00", "#56B4E9", "#F0E442", "#000000"]
```

For sequential/continuous maps use `viridis` / `cividis` (perceptually uniform,
grayscale-safe). Two-group biology default: blue `#0072B2` vs vermillion `#D55E00`.

## The caption file
- One `figure_captions.md` lives in the same experiment folder
  (`experiments/exp-NNNN_slug/`).
- Per figure: filename, one line on what it shows, the method/stats detail
  (test, n's, linkage, p-values), and how to read it (what any marks mean).
- **Update it whenever a figure is added or changed.** A figure with no caption entry
  is incomplete. Stats reported here — never drawn on the figure.

## Bundled
- `qa.py` — renders every `figures/*.pdf` to a PNG for eyeballing and checks the rules
  (PDF-only, column-width sizing, every figure has a caption entry). Run it in step 4.


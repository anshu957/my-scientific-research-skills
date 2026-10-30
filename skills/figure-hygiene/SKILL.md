---
name: figure-hygiene
description: Produce clean, single scientific figures for viewing on screen (notebooks, lab meetings, slides, sharing). Governs how the plot form is chosen (reasoned from the question and the data), what goes inside the figure (one title = the key question, only strictly-necessary labels, NO explanatory/stats text on the plot) AND how it is rendered and saved (vector PDF into figures/, named by its question, overwritten on re-run, Arial, screen-legible sizes, a colorblind-safe palette). All figure detail (method, stats, how to read it) goes in a figure_captions.md kept in sync. Use whenever creating or editing any figure or plot in a scientific project, including when someone just hands over data and says "make a figure for this analysis". Not for exact-size journal panels of a multi-panel figure (that is figure-set).
---

# Figure hygiene

The plot shows data; words go in the caption file. Every figure is spare — and it
leaves the machine as a clean vector file, not a screenshot. **One figure = one
question = one panel** — never subplots. A second question is a second figure. These
figures are made to be **read on screen**; journal-size panels are a separate job
(figure-set).

## Workflow

0. **Find the question.** If the request names it, use it. If the user only hands
   over data ("here's my data, make a figure for this analysis"), infer the question
   from the analysis, the column names and any notes; if several questions are in
   play, that is several figures, one each. If the question can't be inferred, that is
   the one thing to ask.
1. **Look at the data first.** Read a few rows / dtypes / shape / n per group before
   plotting. Verify any library API you call actually exists in the installed version.
2. **Choose the form by reasoning, not by rule** — with `references/chart-selection.md`
   as the reference (no web search needed). Answer its §5 reasoning script, match the
   question in its §2 table, let its §3 data-size rules override, and check §4 for
   anti-patterns. In short: state the one question the figure
   answers, the type of each variable (continuous / categorical / count / matrix /
   paired), and the comparison the reader must make. Put that comparison on the most
   accurate encoding (position > length > angle > area > color) and prefer forms that
   show the raw data over a summary. Pick the narrowest plot that does this. Examples,
   not rules: a group comparison usually wants points + box/violin rather than a bar
   of means; a big matrix usually wants clustering.
3. **Ask when it is genuinely ambiguous — only then.** If the question, the comparison,
   the grouping, or which data subset to show is unclear, or two forms are equally
   defensible but would tell different stories, ask before plotting: one short
   message, at most a few questions, each with your proposed default. The same goes for a choice of statistic that changes the answer (e.g.
   pooled vs within-group, AUC vs effect size, univariate vs model-based, CI of the
   mean vs prediction interval, Pearson vs Spearman). If the
   request and the data make it clear, just proceed and name the choice in the caption.
4. **Show what the labels claim.** If the figure asserts structure, the figure must
   *show* the evidence for it — never just assert it in an axis label. Clustering a
   matrix means drawing the **dendrogram(s)** (use `seaborn.clustermap`, not a
   reordered `imshow`); a heatmap whose axis says "clustered" with no visible tree is
   an unverifiable claim. If a grouping variable matters (sex, condition, genotype)
   and the rows/columns are **samples** (animals, cells, wines), annotate it as
   **row/column colors** with a small legend, so the reader can see whether the
   structure lines up with it. This does not apply when rows and columns are features
   (e.g. a feature × feature correlation matrix) — there, say in the caption which
   samples were pooled. In a symmetric matrix, **mask the diagonal** (self-correlation
   = 1) so it doesn't become the most saturated thing on the figure — fill it light
   grey, not white (white reads as 0 on a diverging map), and precompute the linkage
   since NaNs break clustermap's own clustering — and draw one
   dendrogram (rows); the column tree would repeat it. A samples × features matrix
   keeps both trees. Move the clustermap colorbar out of the default top-left slot,
   where it collides with the tree (`cbar_pos`); its title goes on `fig.suptitle`.
   Annotation bars must not share a hue family (e.g. genotype blue/vermillion, sex in
   greys — not vermillion next to orange), and the legend names each bar.
5. **Style, then render** (sections below).
6. **Write the caption entry** (see "The caption file") — QA checks for it.
7. **QA — run the bundled checker, then look.** From the folder that holds
   `figures/`, with the same python you plot with:
   `python <this-skill-dir>/qa.py .` (if your setup wraps python runs, e.g. a RAM
   monitor, wrap this too). It needs PyMuPDF (`pip install pymupdf`) or poppler.
   It renders every PDF in `figures/` to a PNG in `figures/_figqa/`, reports each
   figure's size, and flags rasters, a missing caption entry, or any font other than
   Arial (nonzero exit if a rule is violated). **Then actually open the PNGs** and
   check: nothing clipped, every glyph legible when the PDF is viewed at 100%, colors
   distinguishable in grayscale/colorblind, every rule in "Inside the figure" met. A
   figure you have not looked at is not done. Fix, re-render, re-check. Clean up with
   the same command plus `--clean`.

## Inside the figure
- Exactly **one title**: the key question the figure answers (e.g. "Does the drug
  slow tumour growth?"), in **bold**, with
  clear air between it and the plot (`axes.titlepad` below). No subtitle, no second
  title. Default is `ax.set_title`. It must sit fully inside the canvas: with long tick labels, centre it on the
  figure (`fig.suptitle`) rather than the axes, and create the figure with
  `layout="constrained"` so the gap stays the same at any height.
- Axis labels and a legend **only where strictly necessary** — no restating obvious
  axes, no repeated units, no legend if one series.
- **No** explanatory sentences, method notes, footnotes, asterisk keys, or
  interpretation text drawn on the figure.
- **Every color and mark must be decodable on the figure itself** — by a legend, a
  colorbar, or direct labels. Color that only the caption explains is noise; color that
  repeats what the tick labels already say is redundant — drop it and use one color.
  Once there are two kinds of mark (e.g. points + a fit line + its band, or data + a
  reference line), each gets a short legend entry ("Patients", "Linear fit", "95% CI");
  the caption gives the detail. Put the legend where it covers no data.
- **Order by the plotted value.** When rows/categories are ranked, sort them by the
  exact quantity on the axis, so the order is visibly monotonic. If a different order
  is meaningful (experimental, natural), it must be obvious from the labels.

## Perception (Tufte, Cleveland–McGill)
Check the figure against these before QA:
- **Show the data.** Raw points over summaries when n allows; uncertainty drawn light
  and *behind* the data, never as the boldest thing.
- **Most accurate encoding for the key comparison:** position on a common scale >
  length > angle > area > color. Values to be compared share one aligned axis.
- **No lie factor.** Length/area encodings (bars, areas) start at zero; position
  encodings (dots, lines) may zoom to the data range. A broken axis or a second y-axis
  is fine when scales genuinely differ (e.g. one outlier group, two quantities in
  different units on one x); mark the break visibly, color each y-axis like its series,
  and make sure the reader can't misread a crossing of two series as meaningful.
- **Data-ink.** Erase ink that carries no data: frames, backgrounds, heavy gridlines,
  3D, shadows, bevels, legend boxes. Keep ink that aids reading (a light reference line
  at the null, e.g. 0 or AUC 0.5: thin, grey, dashed, behind the data).
- **Aspect ratio:** when slope is the message, size the plot so key slopes sit near
  45°; otherwise follow the size rules below.
- **Preattentive pop-out.** At most one accent color for the thing the question is
  about; everything else muted. If one category covers most of the marks, it gets the
  neutral (grey/black) and the minority gets the accent. The same color means the same
  thing throughout a project.
- **Gestalt:** keep labels next to what they name (proximity); a legend sits inside
  the plot in empty space, not outside it.

## Output contract
- **Vector PDF only**, saved into a `figures/` folder in the folder you are working in
  (the experiment/analysis directory; create `figures/` if absent). If the project
  has its own layout (e.g. `experiments/exp-NNNN_slug/`), that folder is the one. The plotting script
  sits next to `figures/`, so the figure can be regenerated.
  Never a raster screenshot; never a second parallel format (no `.png` twin).
- **Name the file by the key question it answers**: `NN_<question-slug>.pdf`, a short
  snake_case compression of the title question (e.g. title "Does the drug slow tumour
  growth?" → `02_does_drug_slow_tumour_growth.pdf`). `NN` numbers figures in the order
  they were made (01, 02, …). Keep it to ~6 words.
- **Stable name, overwrite on re-run.** No `_v2`, no timestamps, no per-iteration
  variants — git is the history. Rename only if the question itself changes, and delete
  the old file in the same step. To compare alternatives, render them temporarily, pick
  one, delete the rest.
- `savefig(path, bbox_inches="tight", pad_inches=0.03)` so nothing is cropped and
  there is no giant margin. Keep text as text (do not rasterize the whole figure);
  rasterize only heavy layers (e.g. a dense heatmap image) if file size demands it.

## Screen style
Set once, before plotting (matplotlib). **Arial always** — name it explicitly; a bare
`"sans-serif"` silently falls back to DejaVu Sans. If Arial isn't installed (common on
Linux/HPC), install it (e.g. `ttf-mscorefonts-installer`, or copy `Arial*.ttf` into
`~/.fonts` and delete `~/.cache/matplotlib`). Using R/ggplot2 or another library? The
same rules apply; translate this block (`base_family = "Arial"`, same sizes,
`cairo_pdf`).

```python
import matplotlib as mpl
mpl.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300,
    "font.family": "Arial", "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlepad": 16,
    "figure.titlesize": 13, "figure.titleweight": "bold",
    "axes.labelsize": 12, "legend.frameon": False,
    "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 1.0, "xtick.major.width": 1.0, "ytick.major.width": 1.0,
    "xtick.direction": "out", "ytick.direction": "out",
    "lines.linewidth": 1.8, "lines.markersize": 5,
    "pdf.fonttype": 42, "ps.fonttype": 42,  # editable text in PDF
})
```

- **Size for the screen.** Set the **canvas** (`figsize`) to about **6 in wide**
  (≈150 mm) for a single plot; the tight save trims empty margin, so the saved file
  comes out a little smaller — that is expected, don't compensate. At this width
  10–13 pt text reads comfortably when the PDF opens at 100% or drops onto a slide.
  Set the height from the data's aspect (≈4–4.5 in for most plots; square for matrices
  and scatters; ~0.25 in per row for long ranked lists); go wider (up to ~9 in) only
  when the content needs it (many categories, a big heatmap). Don't ship seaborn's
  default aspect.
- **Type and lines scale together.** Keep ≤ 4 text sizes (13 title / 12 label / 10 tick
  and legend). Axes and ticks 1.0 pt; data lines 1.5–2 pt; scatter points ~20–30 pt²;
  box/whisker strokes ~1.0 pt. Data should be visibly heavier than the axes.
- **Despine** (top/right off, done above).
- Keep tick counts low; drop chartjunk gridlines unless they aid reading.

## Palette
Use one fixed, colorblind-safe set across all figures in a project (Okabe–Ito):

```python
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#CC79A7",
             "#E69F00", "#56B4E9", "#F0E442", "#000000"]
```

For sequential/continuous maps use `viridis` / `cividis` (perceptually uniform,
grayscale-safe). For signed values (correlations, log-fold changes) use a diverging map
(`RdBu_r`) centered at 0 with symmetric limits. Two-group biology default: blue
`#0072B2` vs vermillion `#D55E00`.

## The caption file
- One `figure_captions.md` lives next to `figures/` (the experiment/analysis folder).
- Per figure: filename, one line on what it shows, the method/stats detail
  (test, n's, linkage, p-values), and how to read it (what any marks mean).
- **Update it whenever a figure is added or changed.** A figure with no caption entry
  is incomplete. Stats reported here — never drawn on the figure.

## Bundled
- `references/chart-selection.md` — question → plot-form guide: encoding principles,
  intent → form table, data-size overrides, anti-patterns, a 5-line reasoning script.
  Use it in step 2.
- `qa.py` — renders every `figures/*.pdf` to a PNG for eyeballing and checks the rules
  (PDF-only, Arial-only, every figure has a caption entry). Run it in step 7.


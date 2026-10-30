# Choosing the visualization

The chart form is a decision, not a default. Pick it by reasoning from two things:
**what question the figure answers** and **the shape of the data you have**. A bar
chart is not a neutral starting point; it is one specific claim (a comparison of a
single number per category), and it is the wrong claim most of the time.

Read this file when you are deciding *what kind of plot to draw*. It is organized as:
(1) the guiding principles, (2) an intent → form table, (3) data-shape heuristics that
override the table, (4) the common anti-patterns and what to do instead.

## 1. Principles that decide encoding

- **Match the encoding to how accurately people read it.** People judge *position on a
  common scale* most accurately, then *length*, then *angle/slope*, then *area*, then
  *color/shade* (Cleveland–McGill). Put the quantity you most want the reader to compare
  on a position encoding (a dot's x, a point's height). Reserve area and color for the
  variable that matters least or for a categorical grouping. This single ranking is why a
  dot plot usually beats a bar, and why a pie (angle/area) is almost always worse than a
  bar (length).
- **Show the data, not just a summary of it.** A mean with an error bar hides the sample
  size, the spread, the skew, and the outliers, all of which a reviewer will ask about.
  If the data are few enough to draw, draw them.
- **Show uncertainty.** If you plot a summary, show its uncertainty, and be explicit about
  which one: a 95% CI, a bootstrap interval, and ±1 SD say different things. Default to a
  CI for "is this difference real?" and to the raw spread (SD/quartiles) for "how variable
  is this?".
- **One message per figure.** Decide the single sentence the figure must let the reader
  conclude, then choose the form that makes that sentence visible at a glance. If two
  messages compete, that is two panels, not one busy plot.
- **Order carries meaning.** Sort categories by the value being shown, or by a
  natural/experimental order. Alphabetical order is almost never the meaningful one.

## 2. Intent → form

Find the row that matches the *question*, then let §3 adjust for your data size.

| The question the figure answers | Default form | Notes / when to switch |
| --- | --- | --- |
| How is one continuous variable distributed? | histogram or KDE; **ECDF** when tails/quantiles matter | ECDF needs no bin choice and shows every point's percentile. |
| How does a continuous variable compare across a few groups? | **box or violin with the points overlaid** (a "raincloud"); strip/swarm if n is small | Not a bar of means. The bar throws away the distribution the comparison is about. |
| One summary number across many categories? | **ordered dot plot / lollipop**, horizontal | Beats a bar: less ink, labels read left-to-right, and dozens of rows fit. |
| Relationship between two continuous variables? | **scatter**, add a LOESS/regression line if a trend is the point | Large n → 2D density, hexbin, or alpha-blend to fight overplotting. |
| Trend over an ordered or continuous x (time, dose, K)? | **line**; band for the uncertainty | Points too if x is sampled sparsely. One line per group, direct-labeled. |
| Parts of a whole? | **stacked bar** (one bar) or, for a few parts, a labeled dot plot | Pie only for 2–3 slices with very different sizes. Never a pie for many. |
| How composition changes across an ordered x? | **stacked area** (proportions) or a set of stacked bars | Keep the most important band on the baseline where it is readable. |
| Ranking of items? | **ordered horizontal bar or dot plot** | Sort by value; that ordering *is* the finding. |
| Many-vs-many values (correlation, similarity, usage matrix)? | **heatmap** | If you claim structure/blocks, cluster it and **draw the dendrogram** (`clustermap`), don't just reorder. Diverging map centered at 0 for signed values. |
| Paired / repeated measurements (before–after, matched)? | **slope chart** (paired lines) or a plot of the per-pair *difference* | Preserves the pairing that a two-box comparison discards. |
| Counts across two categorical variables? | grouped or stacked bar, **mosaic**, or a count heatmap | Heatmap scales best when both variables have many levels. |
| Effect sizes / estimates across models or conditions? | **forest plot** (point + CI per row) | The canonical way to compare coefficients with their uncertainty. |
| Overlap between sets? | **UpSet plot** for >3 sets; Venn only for 2–3 | Venn diagrams collapse past three sets. |
| Flows or transitions between states? | **Sankey / alluvial**, or a directed graph if the topology matters | Use sparingly; they are easy to make illegible. |
| Geographic variation? | choropleth (rates) or a symbol map (counts) | Normalize by area/population before shading a choropleth. |

## 3. Data-shape heuristics (these override the table)

- **Small n per group (roughly < ~20):** show every point (strip/swarm/beeswarm), with a
  light summary (median bar, box) behind it. A violin or KDE on a handful of points invents
  a smooth density that is not in the data.
- **Large n, scattered:** overplotting hides the mass. Switch to 2D density, hexbin, or
  contour, or keep the scatter but add alpha and a summary line.
- **Many categories (say > ~12):** go horizontal so labels are readable, order by value,
  and prefer dots to bars (less ink per row). Consider whether the reader needs all of them
  or just the head and tail.
- **Skewed / multi-order-of-magnitude values:** use a log scale (and say so on the axis),
  or the distribution collapses against one edge.
- **Compositional data (rows sum to 1):** a difference of 2 percentage points near 0% is not
  the same as near 50%; consider whether raw counts tell the story more honestly.
- **Time series with many series:** direct-label the few that matter and grey the rest, or
  use small multiples (one panel per series) instead of a spaghetti plot.

## 4. Anti-patterns → the fix

- **Bar chart of group means ("dynamite plot"):** hides the distribution and implies a count
  where there is none. → box/violin + points, or a dot plot of the summary with its CI.
- **Pie / donut with many slices:** angle and area are read poorly and the slices are hard to
  order. → ordered bar or dot plot; keep a pie only for 2–3 very unequal parts.
- **Dual y-axes:** invites a false visual correlation and lets the author set the apparent
  relationship by scaling. → two stacked panels sharing the x-axis, or plot a derived ratio.
- **Truncated y-axis on bars:** bars encode length from zero; a cut axis exaggerates
  differences. → keep the baseline at zero for bars, or use a dot plot (which may start
  anywhere) instead.
- **Rainbow / jet colormap:** not perceptually uniform and not colorblind-safe; creates false
  banding. → viridis/cividis for sequential, a diverging map (e.g. RdBu) centered on the
  meaningful midpoint for signed data.
- **Color as the quantitative channel when precision matters:** shade is read imprecisely. →
  move the quantity to a position/length encoding; keep color for category or as a secondary
  cue.
- **3D bars/surfaces for 2D data:** perspective distorts comparison. → a flat heatmap or
  small multiples.
- **A heatmap axis labeled "clustered" with no tree drawn:** an unverifiable claim. → draw the
  dendrogram(s) so the ordering is shown, not asserted.

## 5. A quick reasoning script

Before writing plotting code, answer these in one or two lines each (in your head or in the
caption draft):

1. What is the one question this figure answers?
2. What is each variable — continuous, categorical (ordered?), count, proportion, a matrix?
3. What comparison does the reader need to make by eye, and how many items/points is that?
4. Which form from §2 puts that comparison on the most accurate encoding, given the n from §3?
5. What must be shown to back the claim (the points, the uncertainty, the cluster tree)?

If two forms are close, pick the one that shows more of the raw data. You can always simplify
later; you cannot recover data you summarized away.

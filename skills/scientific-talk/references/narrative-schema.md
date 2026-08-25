# narrative.json — every word, and which figure carries it

`narrative.json` is the deck's source of truth. Panels live here too, next to the
words, so inserting a slide can never desynchronize the story from the figures.
Edit this file, not the builder.

```json
{"slides": [ { ...slide... }, { ...slide... } ]}
```

Slides are rendered in list order; `n` is the slide number shown in the footer
and should be 1..N (renumber after inserting).

## Content slide

```json
{
  "n": 14,
  "section": "Individuate",
  "headline": "Trajectories of future short- and long-lived animals split at about 70 days",
  "takeaway": "Animals that will die before 200 days already diverge in behavioral space at ~70 days, a hundred days before death.",
  "credit": "Fig. 3B",
  "annotations": ["branch point ~70 d"],
  "panels": {"rows": [["fig3B_traj_by_lifespan"]]},
  "notes": "CLAIM — ...\nPOINT — ...\nSAY — ...\nMY READ — ...\nPAUSE / IF SHORT — ..."
}
```

| field | required | notes |
|---|---|---|
| `n` | yes | slide number, footer bottom-right |
| `section` | no | black `Section \| ` prefix on the headline; `""` for title/summary/discussion |
| `headline` | yes | the claim or question, ≤ 90 chars, ≤ 2 lines |
| `takeaway` | no | one italic sentence, ≤ 165 chars; `""` to omit |
| `credit` | no | tiny provenance, e.g. `Fig. 3B`, `fig. S13B`, `unpublished` |
| `annotations` | no | ≤ 2 accent-coloured labels, ≤ 30 chars, no arrows |
| `panels` | no | `{"rows": [[name, name], [name]]}` — panel PNG basenames from `figures/panels/` |
| `notes` | no | speaker notes, in full; see the five-field shape in `talk-craft.md` |

`panels.rows` is a list of rows; panels within a row sit side by side at a common
height, rows stack. Extra keys `row_weights` (relative row heights) and
`fill_width_rows` (indices of rows scaled to the full body width, e.g. a wide
banner diagram) are available for the rare multi-row slide.

## Layout the builder picks for you

- **Side layout** — takeaway/credit/annotations in a right-hand column, figure
  running the full slide height. Chosen automatically when it makes the figure
  bigger, which is most single squarish panels.
- **Wide layout** — figure across the body, takeaway underneath. Chosen for wide
  pairs and banners. A short banner pulls its takeaway up to meet it rather than
  leaving a hole.

You do not select these; the builder takes whichever yields the larger figure.
To make a figure bigger, give it a one-line headline or fewer panels.

## Special slides

**Title** (`n: 1`) — uses `title`, `red_word` (the word set in the accent colour),
`authors`, `citation`, `presenter_line` (`"Journal Club | Name | 05 August 2026"`,
split on `|`).

**Statement slide** — `lines: ["...", "...", "..."]`, up to ~4 one-line
statements, no figure. Use for the motivating slide and the limitations slide.

**Summary** — `bullets: ["...", ...]`, ≤ 5, one line each. The only slide in the
deck that gets bullets; its headline should be the assertion the talk earned, not
the word "Summary".

**Build steps** — consecutive slides with the *same* `headline`, `takeaway` and
`credit`, whose panels are crops of identical geometry with progressively more
revealed (see `whiteout` in `crops.json`). They read as one slide advancing.

**Backup** — after the last content slide, `section: "Backup"`, one per
predictable question. They cost nothing until asked.

## Editing conventions

- Numbers only from the source; keep a verified-numbers block in `ARC.md`.
- When you change a headline, re-check that the panel still demonstrates it.
- Renumber `n` after any insertion, then rebuild — the footer numbers come from here.

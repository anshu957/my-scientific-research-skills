"""Build a scientific talk deck from narrative.json + design_spec.json + panel PNGs.

    python3 build_deck.py [talk_dir] [-o out.pptx]

Reads, in `talk_dir` (default: cwd):
    design_spec.json   the visual system (page size, fonts, colours, coordinates)
    narrative.json     {"slides": [...]} -- every word, plus each slide's panels
    figures/panels/    the cropped figure PNGs the slides reference

Writes the .pptx (name taken from design_spec["deck"]["out"] or `talk.pptx`) and
prints layout warnings. preview_deck.py imports plan_slide() from here so the
PIL preview and the .pptx can never drift apart.

The single source of truth for geometry is ``plan_slide()``: it returns a flat
list of drawing items in POINTS on the page described by design_spec. build() renders those
items to python-pptx shapes; preview_deck_v2.py renders the same items with PIL,
so the preview and the .pptx cannot drift apart.

Item kinds
    rect  {x,y,w,h,fill}
    poly  {pts:[(x,y)...],fill}
    image {path,x,y,w,h}
    text  {x,y,w,size,line_spacing,align,runs:[(txt,color,bold,italic)],
           lines:[[(frag,style)...]], tbox:(x0,y0,x1,y1), role}
"""
import json
import os
import sys

from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Emu, Pt

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(next((a for a in sys.argv[1:] if not a.startswith("-")), "."))
PANELS = os.path.join(ROOT, "figures", "panels")
LOGOS = os.path.join(ROOT, "figures", "logos")

# spec resolution: this talk -> your private house style -> the bundled example
_spec_path = next(p for p in (
    os.path.join(ROOT, "design_spec.json"),
    os.path.join(SKILL, "assets", "local", "design_spec.local.json"),
    os.path.join(SKILL, "assets", "design_spec.example.json"),
) if os.path.exists(p))
SPEC = json.load(open(_spec_path))
NARR = json.load(open(os.path.join(ROOT, "narrative.json")))["slides"]
DECK = SPEC.get("deck", {})
OUTPPTX = os.path.join(ROOT, DECK.get("out", "talk.pptx"))
if "-o" in sys.argv:
    OUTPPTX = os.path.abspath(sys.argv[sys.argv.index("-o") + 1])

SW, SH = SPEC["page"]["w"], SPEC["page"]["h"]          # 720 x 405 pt
C = SPEC["colors"]
BLACK, RED = C["headline_section"], C["headline_claim"]
BLUE = C["footer_rule"]
JOURNAL_BLUE = C.get("citation", "005789")

# ---------------------------------------------------------------- geometry ---
HL_X, HL_Y, HL_W = SPEC["headline"]["x"], SPEC["headline"]["y"], 690.0
BODY_X, BODY_W = SPEC["body_area"]["x"], SPEC["body_area"]["w"]     # 8 .. 712
FIG_BOT_TAKEAWAY = 306.0        # figure floor when the takeaway sits underneath
FIG_BOT_FULL = 372.0            # figure floor when the takeaway sits beside it
TAKE_X, TAKE_Y, TAKE_W = SPEC["takeaway"]["x"], SPEC["takeaway"]["y"], 640.0
CRED_X, CRED_Y = SPEC["credit"]["x"], SPEC["credit"]["y"]
F = SPEC["footer"]
TALL_FIG_WCAP = 520.0           # keep a text column free in "tall" layouts
GUTTER_MIN = 118.0              # gutter wide enough to hold annotations

# ------------------------------------------------ panel plan (binding: ARC) ---
# Panel assignment now lives in narrative.json ("panels": {"rows": [[...]]}) so
# that slide order and panels cannot drift apart when slides are inserted.
PLAN = {sl["n"]: sl["panels"] for sl in NARR if sl.get("panels")}

# a single squarish panel is wasted in a full-width band: give it the full slide
# height and put the takeaway in a right-hand column instead (design_spec p.18).
TALL_AR_MAX = 1.62
ROW_GAP = 10.0
COL_GAP = 18.0

FONT_DIR = next((d for d in ("/System/Library/Fonts/Supplemental",
                             "/usr/share/fonts/truetype/msttcorefonts",
                             "/usr/share/fonts/truetype/liberation")
                 if os.path.isdir(d)), "/System/Library/Fonts/Supplemental")
_FONTS, _AR = {}, {}


def _font(bold=False, italic=False, px=200):
    key = (bold, italic, px)
    if key not in _FONTS:
        stem = ["Arial", "LiberationSans"]
        suffix = (" Bold Italic" if bold and italic else " Bold" if bold else
                  " Italic" if italic else "")
        cands = [f"{st}{suffix.replace(' ', sep)}.ttf".replace(" ", sep)
                 for st in stem for sep in (" ", "-")]
        cands += ["Arial.ttf", "LiberationSans-Regular.ttf"]
        path = next((os.path.join(FONT_DIR, c) for c in cands
                     if os.path.exists(os.path.join(FONT_DIR, c))), None)
        if path is None:
            raise SystemExit(f"no Arial-like TTF found in {FONT_DIR}")
        _FONTS[key] = ImageFont.truetype(path, px)
    return _FONTS[key]


def tw(text, size, bold=False, italic=False):
    """Width of `text` in points at `size` pt Arial."""
    return _font(bold, italic).getlength(text) * size / 200.0


def aspect(name):
    if name not in _AR:
        with Image.open(os.path.join(PANELS, name + ".png")) as im:
            _AR[name] = im.size[0] / im.size[1]
    return _AR[name]


# ------------------------------------------------------------ text wrapping ---
def _flatten(runs):
    s = "".join(r[0] for r in runs)
    st = []
    for r in runs:
        st += [r[1]] * len(r[0])
    return s, st


def wrap_runs(runs, size, maxw):
    """Wrap styled runs to `maxw` pt. Returns [[(fragment, style), ...], ...]."""
    s, st = _flatten(runs)
    out, i = [], 0
    for para in s.split("\n"):
        words, start = [], i
        pos = start
        for w in para.split(" "):
            words.append((pos, w))
            pos += len(w) + 1
        line = []                      # list of (i0, i1) char spans
        cur = ""
        for pos, w in words:
            trial = (cur + " " + w) if cur else w
            if cur and tw(trial, size, st[pos][1], st[pos][2]) > maxw:
                out.append(_spans(s, st, line))
                line, cur = [], ""
                trial = w
            line.append((pos, pos + len(w)))
            cur = trial
        out.append(_spans(s, st, line))
        i = pos
    return out


def _spans(s, st, spans):
    """Merge char spans into (fragment, style) pairs, joining with spaces."""
    if not spans:
        return [("", (BLACK, False, False))]
    chars = []
    for k, (a, b) in enumerate(spans):
        if k:
            chars.append((" ", st[a]))
        for j in range(a, b):
            chars.append((s[j], st[j]))
    frags = []
    for ch, style in chars:
        if frags and frags[-1][1] == style:
            frags[-1][0] += ch
        else:
            frags.append([ch, style])
    return [(f, style) for f, style in frags]


def line_text(line):
    return "".join(f for f, _ in line)


def mk_text(x, y, w, size, runs, line_spacing=None, align="l", role="",
            italic_default=False):
    ls = line_spacing or size * 1.2
    lines = wrap_runs(runs, size, w)
    n = len(lines)
    widths = [tw(line_text(ln), size, ln[0][1][1], ln[0][1][2]) for ln in lines]
    asc = 0.30 * size                      # box top -> cap top, measured
    top = y + asc - 0.06 * size
    bot = y + asc + (n - 1) * ls + 0.80 * size
    if align == "r":
        x0, x1 = x + w - max(widths), x + w
    else:
        x0, x1 = x, x + max(widths)
    return dict(kind="text", x=x, y=y, w=w, size=size, line_spacing=ls,
                align=align, runs=runs, lines=lines, nlines=n, role=role,
                tbox=(x0, top, x1, bot))


# ------------------------------------------------------------- figure fitting ---
def fit_row(ars, W, H, gap=COL_GAP):
    """Widths/heights for one row of panels inside W x H, aspect preserved."""
    n = len(ars)
    avail = W - gap * (n - 1)
    if n > 1 and max(ars) / min(ars) > 2.2:
        p = [a ** 0.5 for a in ars]
        ws = [avail * q / sum(p) for q in p]
        hs = [w / a for w, a in zip(ws, ars)]
        for _ in range(4):
            over = [i for i, h in enumerate(hs) if h > H + 1e-6]
            if not over:
                break
            rest = [i for i in range(n) if i not in over]
            free = avail - sum(H * ars[i] for i in over)
            if not rest or free <= 0:
                ws, hs = [H * a for a in ars], [H] * n
                break
            pr = sum(p[i] for i in rest)
            for i in over:
                ws[i], hs[i] = H * ars[i], H
            for i in rest:
                ws[i] = free * p[i] / pr
                hs[i] = ws[i] / ars[i]
    else:
        ws, hs = [H * a for a in ars], [H] * n
    k = min(1.0, avail / sum(ws), H / max(hs))
    return [w * k for w in ws], [h * k for h in hs]


def place_rows(rows, weights, X, Y, W, H, path_of, fill_width=()):
    """Lay out rows of panels; returns (items, bbox).

    Rows listed in `fill_width` are scaled to the full width W and take whatever
    height that implies; the remaining height is shared by the other rows in
    proportion to `weights`.
    """
    items = []
    fixed = {}
    for i in fill_width:
        ars = [aspect(n) for n in rows[i]]
        fixed[i] = (W - COL_GAP * (len(ars) - 1)) / sum(ars)
    free = H - ROW_GAP * (len(rows) - 1) - sum(fixed.values())
    wsum = sum(w for i, w in enumerate(weights) if i not in fixed) or 1.0
    yy = Y
    x0b, y0b, x1b, y1b = 1e9, 1e9, -1e9, -1e9
    for ri, (names, wt) in enumerate(zip(rows, weights)):
        rh = fixed[ri] if ri in fixed else free * wt / wsum
        ars = [aspect(n) for n in names]
        ws, hs = fit_row(ars, W, rh)
        total = sum(ws) + COL_GAP * (len(names) - 1)
        x = X + (W - total) / 2.0
        for nm, w, h in zip(names, ws, hs):
            y = yy + (rh - h) / 2.0
            items.append(dict(kind="image", path=path_of(nm), x=x, y=y, w=w, h=h,
                              name=nm))
            x0b, y0b = min(x0b, x), min(y0b, y)
            x1b, y1b = max(x1b, x + w), max(y1b, y + h)
            x += w + COL_GAP
        yy += rh + ROW_GAP
    return items, (x0b, y0b, x1b, y1b)


# ------------------------------------------------------------------ headline ---
def headline_runs(spec):
    section, head = spec.get("section", ""), spec["headline"]
    if section:
        return [(section + " | ", (BLACK, True, False)), (head, (RED, True, False))]
    return [(head, (BLACK, True, False))]


def headline_item(spec):
    runs = headline_runs(spec)
    for size in (26, 24, 22, 20):
        it = mk_text(HL_X, HL_Y, HL_W, size, runs,
                     line_spacing=round(size * 1.38, 1), role="headline")
        if it["nlines"] <= 2:
            break
    body_top = round(HL_Y + 0.30 * size + (it["nlines"] - 1) * it["line_spacing"]
                     + size + 8.0, 1)
    return it, body_top


def footer_items(n=None):
    it = [
        dict(kind="rect", x=0, y=F["rule_y"], w=SW, h=F["rule_h"], fill=BLUE),

        mk_text(F["text_x"], F["text_y"] - 1.5, 300, SPEC["fonts"]["footer"]["size"],
                [(F["text"], (BLUE, True, False))], role="footer"),
    ]
    if F.get("chevron"):                      # optional decorative notch
        it.append(dict(kind="poly", fill=BLUE,
                       pts=[tuple(p) for p in F["chevron"]]))
    if n is not None:
        it.append(mk_text(SW - 46.0, F["text_y"] - 1.5, 28,
                          SPEC["fonts"]["footer"]["size"],
                          [(str(n), (BLUE, True, False))], align="r", role="pagenum"))
    return it


# ------------------------------------------------------------------ planners ---
def plan_title(spec):
    items = []
    T = SPEC["title_slide"]
    t = spec["title"]
    rw = spec.get("red_word", "")
    if rw and rw in t:
        i = t.index(rw)
        runs = [(t[:i], (BLACK, True, False)), (rw, (RED, True, False)),
                (t[i + len(rw):], (BLACK, True, False))]
        runs = [r for r in runs if r[0]]
    else:
        runs = [(t, (BLACK, True, False))]
    items.append(mk_text(T["title"]["x"], T["title"]["y"], T["title"]["max_w"],
                         T["title"]["size"], runs, line_spacing=38.6,
                         role="title"))
    auth, cit = spec.get("authors", ""), spec.get("citation", "")
    if auth or cit:                                # skip the line entirely when blank
        cit_runs = [(auth, (JOURNAL_BLUE, False, False))]
        cit_runs.append((("  ·  " if auth else "") + cit, (BLACK, False, False)))
        cit_runs = [r for r in cit_runs if r[0]]
        items.append(mk_text(T["title"]["x"], T.get("citation_y", 212.0), 640, 14,
                             cit_runs, line_spacing=18.0, role="citation"))
    b = T["band"]
    items.append(dict(kind="rect", x=b["x"], y=b["y"], w=b["w"], h=b["h"], fill=BLUE))
    if T.get("band_notch"):
        items.append(dict(kind="poly", fill="FFFFFF",
                          pts=[tuple(p) for p in T["band_notch"]]))
    for lg in T.get("logos", []):
        cands = ([lg["path"]] if os.path.isabs(lg["path"]) else
                 [os.path.join(d, os.path.basename(lg["path"])) for d in
                  (LOGOS, os.path.join(SKILL, "assets", "local"),
                   os.path.join(SKILL, "assets"))])
        path = next((c for c in cands if os.path.exists(c)), None)
        if path:
            items.append(dict(kind="image", path=path, x=lg["x"], y=lg["y"],
                              w=lg["w"], h=lg["h"], name=os.path.basename(path)))
    pres = [p.strip() for p in spec.get("presenter_line", "|").split("|")] + ["", ""]
    items.append(mk_text(T["meta"].get("x", 460.0), T["meta"]["y"] - 3.0, 230, T["meta"]["size"],
                         [(pres[0], (BLACK, True, False))], align="r", role="meta1"))
    items.append(mk_text(T["meta"].get("x", 460.0), T["meta"]["y"] + 20.6, 230, T["meta"]["size"],
                         [(pres[1], (RED, True, False)),
                          (" | " + pres[2], (BLACK, True, False))],
                         align="r", role="meta2"))
    return items, []


def _takeaway(spec, x, y, w, role="takeaway", max_lines=2,
              sizes=(14, 13, 12.5, 12, 11.5)):
    """Takeaway, auto-shrunk until it fits `max_lines`."""
    txt = spec.get("takeaway", "")
    if not txt:
        return None
    for s in sizes:
        it = mk_text(x, y, w, s, [(txt, (C["takeaway"], False, True))],
                     line_spacing=round(s * 1.2, 1), role=role)
        if it["nlines"] <= max_lines:
            break
    return it


def plan_content(spec):
    warn = []
    items = []
    hl, body_top = headline_item(spec)
    items.append(hl)
    cfg = PLAN[spec["n"]]
    rows = cfg["rows"]
    weights = cfg.get("row_weights", [1.0] * len(rows))
    fillw = tuple(cfg.get("fill_width_rows", ()))
    anns = spec.get("annotations", [])

    def path_of(nm):
        return os.path.join(PANELS, nm + ".png")

    # Pick whichever layout makes the figure larger: the takeaway underneath
    # (figure floor 306) or beside it in a right-hand column (floor 372, but a
    # narrower band). Most panels here are height-limited, so the side column
    # usually wins and buys ~30% linear size.
    def block_h(W, H):
        _, bb = place_rows(rows, weights, BODY_X, body_top, W, H, path_of, fillw)
        return bb[3] - bb[1]

    if fillw:
        tall = False                    # a full-width banner row needs all 704 pt
    else:
        tall = (block_h(TALL_FIG_WCAP, FIG_BOT_FULL - body_top)
                > 1.06 * block_h(BODY_W, FIG_BOT_TAKEAWAY - body_top))

    if tall:
        H = FIG_BOT_FULL - body_top
        figs, bb = place_rows(rows, weights, BODY_X, body_top, TALL_FIG_WCAP, H,
                              path_of, fillw)
        items += figs
        cx = bb[2] + 22.0
        cw = 712.0 - cx
        ty = body_top + 0.22 * (bb[3] - bb[1])
        tk = _takeaway(spec, cx, ty, cw, role="takeaway_side", max_lines=5,
                       sizes=(14, 13.5, 13, 12.5, 12))
        if tk:
            items.append(tk)
            ty = tk["tbox"][3] + 14.0
        if spec.get("credit"):
            items.append(mk_text(cx, ty, cw, SPEC["fonts"]["credit"]["size"],
                                 [(spec["credit"], (C["credit"], False, False))],
                                 role="credit"))
            ty += 22.0
        for a in anns:
            it = mk_text(cx, ty, cw, 12, [(a, (RED, False, False))], role="annotation")
            items.append(it)
            ty = it["tbox"][3] + 6.0
    else:
        H = FIG_BOT_TAKEAWAY - body_top
        # probe at full width, then decide whether the annotations get their own
        # right-hand column (figure re-centred in what is left) or a strip below.
        probe, pbb = place_rows(rows, weights, BODY_X, body_top, BODY_W, H, path_of,
                                fillw)
        acol = 0.0
        if anns:
            need = min(max(max(tw(a, 12) for a in anns) + 6.0, GUTTER_MIN - 18),
                       170.0)
            if BODY_W - (pbb[2] - pbb[0]) >= need + 26.0:
                acol = need
        if acol:
            figs, bb = place_rows(rows, weights, BODY_X, body_top,
                                  BODY_W - acol - 18.0, H, path_of, fillw)
        else:
            shrink = 22.0 if anns else 0.0
            figs, bb = place_rows(rows, weights, BODY_X, body_top, BODY_W,
                                  H - shrink, path_of, fillw)
        items += figs
        if acol:
            ax, aw = BODY_X + BODY_W - acol, acol
            ay = bb[1] + 2.0
            for a in anns:
                it = mk_text(ax, ay, aw, 12, [(a, (RED, False, False))],
                             role="annotation")
                items.append(it)
                ay = it["tbox"][3] + 7.0
        elif anns:
            ax = bb[0]
            ay = bb[3] + 4.0
            for a in anns:
                w = tw(a, 12) + 2
                if ax + w > BODY_X + BODY_W:
                    warn.append(f"slide {spec['n']}: annotation dropped (no room): {a!r}")
                    continue
                items.append(mk_text(ax, ay, w, 12, [(a, (RED, False, False))],
                                     role="annotation"))
                ax += w + 26.0
        # a short figure (a wide banner, say) would otherwise leave a hole between
        # itself and a takeaway pinned to y = TAKE_Y; pull the takeaway up to it.
        ann_bot = max([i["tbox"][3] for i in items if i.get("role") == "annotation"]
                      + [bb[3]])
        ty = min(TAKE_Y, max(ann_bot + 16.0, bb[3] + 16.0))
        tk = _takeaway(spec, TAKE_X, ty, TAKE_W)
        if tk:
            items.append(tk)
        if spec.get("credit"):
            items.append(mk_text(CRED_X, CRED_Y, 400, SPEC["fonts"]["credit"]["size"],
                                 [(spec["credit"], (C["credit"], False, False))],
                                 role="credit"))
    items += footer_items(spec["n"])
    return items, warn


def plan_lines(spec):
    """No-figure slide: a few short statement lines (slides 2 and 28)."""
    items = []
    hl, body_top = headline_item(spec)
    items.append(hl)
    lines = spec["lines"]
    floor = (300.0 if spec.get("takeaway") else 340.0)
    top = body_top + 22.0
    W = 664.0

    def lay(size, gap):
        y, out = top, []
        for ln in lines:
            it = mk_text(TAKE_X, y, W, size, [(ln, (BLACK, False, False))],
                         line_spacing=round(size * 1.25, 1), role="line")
            out.append(it)
            y = it["tbox"][3] + gap
        return out

    sizes = (20, 19, 18, 17, 16, 15, 14)
    pick = None
    for size in sizes:                        # prefer a size where none wrap
        laid = lay(size, size * 0.7)
        if (all(it["nlines"] == 1 for it in laid)
                and laid[-1]["tbox"][3] <= floor):
            pick = size
            break
    if pick is None:
        for size in sizes:
            laid = lay(size, size * 0.7)
            if laid[-1]["tbox"][3] <= floor:
                pick = size
                break
        pick = pick or sizes[-1]
    laid = lay(pick, pick * 0.7)
    if len(lines) > 1:                        # spread the block over the body
        used = sum(it["tbox"][3] - it["tbox"][1] for it in laid)
        gap = min(pick * 2.1, max(pick * 0.7,
                                  (floor - top - used) / (len(lines) - 1)))
        laid = lay(pick, gap)
    items += laid
    tk = _takeaway(spec, TAKE_X, TAKE_Y, TAKE_W)
    if tk:
        items.append(tk)
    items += footer_items(spec["n"])
    return items, []


def plan_summary(spec):
    items = []
    hl, body_top = headline_item(spec)
    items.append(hl)
    bl = spec["bullets"]
    bx, tx, twid = 22.9, 49.4, 644.0
    top, floor = body_top + 6.0, 336.0

    def lay(size, gap):
        ls = round(size * 1.38, 1)
        y, out = top, []
        for b in bl:
            g = mk_text(bx, y, 20, size, [("●", (BLACK, False, False))],
                        line_spacing=ls, role="bullet_glyph")
            t = mk_text(tx, y, twid, size, [(b, (BLACK, False, False))],
                        line_spacing=ls, role="bullet")
            out += [g, t]
            y = t["tbox"][3] + gap
        return out

    for size in (14, 13.5, 13, 12.5, 12):
        laid = lay(size, 24.0)
        if laid[-1]["tbox"][3] <= floor:
            break
    used = sum(t["tbox"][3] - t["tbox"][1] for t in laid[1::2])
    gap = min(size * 2.6, max(24.0, (floor - top - used) / (len(bl) - 1)))
    items += lay(size, gap)
    items += footer_items(spec["n"])
    return items, []


def plan_slide(spec):
    if spec["n"] == 1:
        return plan_title(spec)
    if spec.get("bullets"):
        return plan_summary(spec)
    if spec.get("lines"):
        return plan_lines(spec)
    return plan_content(spec)


# ----------------------------------------------------------------- QA checks ---
def check(spec, items):
    n = spec["n"]
    warn = []
    hl = next((i for i in items if i.get("role") == "headline"), None)
    body_top = None
    if hl:
        if hl["nlines"] > 2:
            warn.append(f"slide {n}: headline is {hl['nlines']} lines")
        if hl["tbox"][2] > HL_X + HL_W + 0.5:
            warn.append(f"slide {n}: headline overflows box width")
        body_top = hl["tbox"][3] + 2.0
    side = any(i.get("role") == "takeaway_side" for i in items)
    for it in items:
        if it.get("role") == "takeaway" and it["nlines"] > 2:
            warn.append(f"slide {n}: takeaway wraps to {it['nlines']} lines")
        if it.get("role") == "takeaway_side" and it["nlines"] > 5:
            warn.append(f"slide {n}: side takeaway wraps to {it['nlines']} lines")
    figs = [i for i in items if i["kind"] == "image" and i["name"].startswith("fig")]
    for f in figs:
        floor = FIG_BOT_FULL if side else FIG_BOT_TAKEAWAY
        if (f["x"] < BODY_X - 0.5 or f["x"] + f["w"] > BODY_X + BODY_W + 0.5
                or (body_top and f["y"] < body_top - 3.0)
                or f["y"] + f["h"] > floor + 0.5):
            warn.append(f"slide {n}: figure {f['name']} outside body area "
                        f"[{f['x']:.0f},{f['y']:.0f},{f['x']+f['w']:.0f},"
                        f"{f['y']+f['h']:.0f}] floor={floor:.0f}")
        with Image.open(f["path"]) as im:
            print_w = im.size[0] / 400.0 * 72.0      # panel size as printed (400 dpi)
        if f["w"] < 0.70 * print_w:
            warn.append(f"slide {n}: figure {f['name']} shown at "
                        f"{f['w'] / print_w:.2f}x print size ({f['w']:.0f} pt)")
    # pairwise overlap of anything with visible extent
    boxes = []
    for it in items:
        if it["kind"] == "text":
            if it["role"] in ("footer",):
                continue
            boxes.append((it["role"] or "text", it["tbox"]))
        elif it["kind"] == "image":
            boxes.append((it["name"], (it["x"], it["y"], it["x"] + it["w"],
                                       it["y"] + it["h"])))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 1.5 and oy > 1.5:
                warn.append(f"slide {n}: OVERLAP {boxes[i][0]} / {boxes[j][0]} "
                            f"({ox:.0f}x{oy:.0f} pt)")
    return warn


# ------------------------------------------------------------------- render ---
def _rgb(h):
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _noline(sh):
    sh.line.fill.background()
    sh.shadow.inherit = False


def render_pptx(prs, spec, items):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    for it in items:
        if it["kind"] == "rect":
            sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(it["x"]), Pt(it["y"]),
                                    Pt(it["w"]), Pt(it["h"]))
            sh.fill.solid()
            sh.fill.fore_color.rgb = _rgb(it["fill"])
            _noline(sh)
        elif it["kind"] == "poly":
            pts = [(Emu(int(Pt(x))), Emu(int(Pt(y)))) for x, y in it["pts"]]
            fb = s.shapes.build_freeform(pts[0][0], pts[0][1])
            fb.add_line_segments(pts[1:], close=True)
            sh = fb.convert_to_shape()
            sh.fill.solid()
            sh.fill.fore_color.rgb = _rgb(it["fill"])
            _noline(sh)
        elif it["kind"] == "image":
            s.shapes.add_picture(it["path"], Pt(it["x"]), Pt(it["y"]),
                                 Pt(it["w"]), Pt(it["h"]))
        elif it["kind"] == "text":
            h = it["tbox"][3] - it["y"] + 6
            tb = s.shapes.add_textbox(Pt(it["x"]), Pt(it["y"]), Pt(it["w"]), Pt(h))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            tf.vertical_anchor = MSO_ANCHOR.TOP
            tf.auto_size = MSO_AUTO_SIZE.NONE
            p = tf.paragraphs[0]
            p.line_spacing = Pt(it["line_spacing"])
            p.space_before = Pt(0)
            p.space_after = Pt(0)
            p.alignment = PP_ALIGN.RIGHT if it["align"] == "r" else PP_ALIGN.LEFT
            for txt, (col, bold, ital) in it["runs"]:
                r = p.add_run()
                r.text = txt
                r.font.name = SPEC["fonts"]["headline"].get("name", "Arial")
                r.font.size = Pt(it["size"])
                r.font.bold = bold
                r.font.italic = ital
                r.font.color.rgb = _rgb(col)
    notes_tf = s.notes_slide.notes_text_frame
    notes_tf.text = spec.get("notes", "")
    for para in notes_tf.paragraphs:            # bigger notes: readable from a lectern
        for run in para.runs:
            run.font.size = Pt(18)
    return s


def build(verbose=True):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Pt(SW), Pt(SH)
    all_warn, summary = [], []
    for spec in NARR:
        items, warn = plan_slide(spec)
        warn = warn + check(spec, items)
        all_warn += warn
        render_pptx(prs, spec, items)
        panels = [i["name"] for i in items
                  if i["kind"] == "image" and i["name"].startswith("fig")]
        summary.append((spec["n"], spec.get("section", "") or "-",
                        spec.get("headline") or spec.get("title", ""), panels))
    prs.save(OUTPPTX)
    if verbose:
        for w in all_warn:
            print("WARN", w)
        print(f"{len(NARR)} slides -> {OUTPPTX}")
        if not all_warn:
            print("no layout warnings")
    return all_warn, summary


if __name__ == "__main__":
    build()

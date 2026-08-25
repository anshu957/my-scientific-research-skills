"""Crop figure sub-panels out of paper/reference PDFs into slide-ready PNGs.

Journal figures are laid out for a reader with unlimited time. A talk needs one
panel at a time, big. This script does that reproducibly: crop rectangles live in
`crops.json` in POINTS (the PDF's own coordinate system), so a crop can be nudged
and re-run instead of being re-made by hand in an image editor.

    python3 crop_panels.py [talk_dir]                  # render every crop
    python3 crop_panels.py [talk_dir] --labels fig1 2  # panel-label coordinates
    python3 crop_panels.py [talk_dir] --page fig1 2    # render a page to look at

`crops.json`:
{
  "dpi": 400,
  "pdfs": {"fig": "../paper.pdf", "sm": "../paper_sm.pdf"},
  "crops": [
    ["fig1A_rig", "fig", 2, [108, 34, 258, 164]],
    ["fig1C_timeline", "fig", 2, [388, 34, 493, 164]]
  ],
  "whiteout": {"fig1C_timeline": [[388, 100, 392.5, 164]]},
  "detint":   {"fig1J_day": [[142, 207, 235], [209, 236, 247]]}
}

whiteout paints page-coordinate rectangles white AFTER cropping: neighbouring
panels bleed into any rectangular crop of a Science/Nature figure, and painting
the intruder out beats shrinking the crop until the axis labels are gone.
detint replaces exact wash colours (zoom connectors, highlight bands) with white
without touching text or saturated colour bars.

Two crops of the same rectangle with different whiteouts = a progressive build:
identical size and position, later panels revealed one click at a time.
"""
import json
import os
import sys

import fitz
from PIL import Image, ImageDraw

ROOT = os.path.abspath(next((a for a in sys.argv[1:] if not a.startswith("-")), "."))
CFG = json.load(open(os.path.join(ROOT, "crops.json")))
OUT = os.path.join(ROOT, "figures", "panels")
DPI = CFG.get("dpi", 400)


def _doc(key):
    path = CFG["pdfs"][key]
    return fitz.open(path if os.path.isabs(path) else os.path.join(ROOT, path))


def labels(key, page_i):
    """Panel-label spans on a figure page: the anchors for every crop box.

    Real panel labels are bold and >= 9.5 pt; the same letters at ~7.5 pt are the
    caption text underneath, which is why the size filter matters.
    """
    page = _doc(key)[int(page_i)]
    for b in page.get_text("dict")["blocks"]:
        if b["type"]:
            continue
        for line in b["lines"]:
            for sp in line["spans"]:
                t = sp["text"].strip()
                if len(t) == 1 and t.isalpha() and t.isupper() and sp["size"] >= 9.0:
                    print(f"{t}  bbox={[round(v, 1) for v in sp['bbox']]}  "
                          f"size={sp['size']:.1f}  {sp['font']}")


def render_page(key, page_i, dpi=110):
    out = os.path.join(ROOT, "figures", f"page_{key}{page_i}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    _doc(key)[int(page_i)].get_pixmap(dpi=dpi).save(out)
    print(out, "-- open it with Read and measure against the label bboxes")


def detint(im, colours, tol=10):
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            for tr, tg, tb in colours:
                if abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol:
                    px[x, y] = (255, 255, 255)
                    break
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    docs = {}
    for name, key, page_i, rect in CFG["crops"]:
        docs.setdefault(key, _doc(key))
        pix = docs[key][page_i].get_pixmap(dpi=DPI, clip=fitz.Rect(*rect))
        path = os.path.join(OUT, name + ".png")
        pix.save(path)
        im = Image.open(path).convert("RGB")          # flatten alpha onto white
        if name in CFG.get("detint", {}):
            im = detint(im, CFG["detint"][name])
        if name in CFG.get("whiteout", {}):
            s = DPI / 72.0
            dr = ImageDraw.Draw(im)
            for wx0, wy0, wx1, wy1 in CFG["whiteout"][name]:
                dr.rectangle([(wx0 - rect[0]) * s, (wy0 - rect[1]) * s,
                              (wx1 - rect[0]) * s, (wy1 - rect[1]) * s], fill="white")
        im.save(path)
        print(f"{name:34s} {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    if "--labels" in sys.argv:
        i = sys.argv.index("--labels")
        labels(sys.argv[i + 1], sys.argv[i + 2])
    elif "--page" in sys.argv:
        i = sys.argv.index("--page")
        render_page(sys.argv[i + 1], sys.argv[i + 2])
    else:
        main()

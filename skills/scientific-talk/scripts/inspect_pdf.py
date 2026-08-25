"""Measure an existing deck (or any PDF) so a new deck can imitate it exactly.

House style is not a vibe: it is a page size, two type sizes, one accent colour
and a set of coordinates. Read them off the reference deck instead of guessing.

    python3 inspect_pdf.py deck.pdf --pages            # page count + size + first lines
    python3 inspect_pdf.py deck.pdf --spans 5          # text: bbox, size, font, colour
    python3 inspect_pdf.py deck.pdf --drawings 5       # filled rects/polys (bars, rules)
    python3 inspect_pdf.py deck.pdf --render 5 [dpi]   # PNG to look at with Read
    python3 inspect_pdf.py deck.pdf --images 5         # embedded image bboxes (logos)

Colours print as RRGGBB hex, ready to paste into design_spec.json.
"""
import sys

import fitz


def hexc(c):
    return f"{c:06X}" if isinstance(c, int) else str(c)


def main():
    path = sys.argv[1]
    d = fitz.open(path)
    if "--pages" in sys.argv:
        print(f"{len(d)} pages, {d[0].rect.width:.0f} x {d[0].rect.height:.0f} pt")
        for i, p in enumerate(d):
            head = " | ".join(p.get_text().split("\n")[:4])
            print(f"{i:3d}  {head[:150]}")
        return
    i = sys.argv.index(next(a for a in sys.argv if a.startswith("--")))
    mode, page_i = sys.argv[i], int(sys.argv[i + 1])
    page = d[page_i]
    if mode == "--spans":
        for b in page.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for line in b["lines"]:
                for sp in line["spans"]:
                    if not sp["text"].strip():
                        continue
                    print(f"{[round(v, 1) for v in sp['bbox']]}  {sp['size']:5.1f}pt  "
                          f"#{hexc(sp['color'])}  {sp['font']:28s} {sp['text'][:60]!r}")
    elif mode == "--drawings":
        for dr in page.get_drawings():
            if dr.get("fill") is None:
                continue
            col = "".join(f"{int(round(c * 255)):02X}" for c in dr["fill"])
            r = dr["rect"]
            print(f"fill #{col}  rect=[{r.x0:.1f}, {r.y0:.1f}, {r.x1:.1f}, {r.y1:.1f}]  "
                  f"items={len(dr['items'])}")
    elif mode == "--images":
        for im in page.get_image_info():
            print(f"bbox={[round(v, 1) for v in im['bbox']]}  {im['width']}x{im['height']}")
    elif mode == "--render":
        dpi = int(sys.argv[i + 2]) if len(sys.argv) > i + 2 else 110
        out = f"page{page_i}.png"
        page.get_pixmap(dpi=dpi).save(out)
        print(out)


if __name__ == "__main__":
    main()

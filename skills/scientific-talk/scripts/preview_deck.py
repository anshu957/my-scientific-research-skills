"""Render approximate PNG previews of a deck and report layout problems.

Geometry is imported from build_deck.plan_slide(), so the preview shows the
same boxes the .pptx gets -- look at these BEFORE opening PowerPoint. Fonts are the real Arial TTFs from
/System/Library/Fonts/Supplemental, so wrapping matches PowerPoint closely.

    python3 preview_deck.py [talk_dir]            # previews + warnings
    python3 preview_deck.py [talk_dir] --sheets   # also 4-up contact sheets (read these)
    python3 preview_deck.py [talk_dir] --clean    # delete the preview PNGs again

Warnings reported (from build_deck.check): headline overflowing its box or
running past 2 lines, takeaway wrapping past 2 lines, a figure leaving the body
area or shown far below its printed size, and any two shapes overlapping.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_deck as bd

PPI = 110
K = PPI / 72.0
OUT = os.path.join(bd.ROOT, "figures", "preview")
_F = {}


def font(size_pt, bold=False, italic=False):
    px = max(6, int(round(size_pt * K)))
    key = (px, bold, italic)
    if key not in _F:
        name = ("Arial Bold.ttf" if bold else
                "Arial Italic.ttf" if italic else "Arial.ttf")
        _F[key] = ImageFont.truetype(os.path.join(bd.FONT_DIR, name), px)
    return _F[key]


def rgb(h):
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def render(items, guides=False):
    W, H = int(bd.SW * K), int(bd.SH * K)
    im = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(im)
    if guides:
        dr.rectangle([bd.BODY_X * K, 40 * K,
                      (bd.BODY_X + bd.BODY_W) * K, bd.FIG_BOT_FULL * K],
                     outline=(225, 225, 225))
    for it in items:
        if it["kind"] == "rect":
            dr.rectangle([it["x"] * K, it["y"] * K,
                          (it["x"] + it["w"]) * K, (it["y"] + it["h"]) * K],
                         fill=rgb(it["fill"]))
        elif it["kind"] == "poly":
            dr.polygon([(x * K, y * K) for x, y in it["pts"]], fill=rgb(it["fill"]))
        elif it["kind"] == "image":
            pic = Image.open(it["path"])
            box = (max(1, int(it["w"] * K)), max(1, int(it["h"] * K)))
            pic = pic.resize(box, Image.LANCZOS)
            pos = (int(it["x"] * K), int(it["y"] * K))
            if pic.mode == "RGBA":
                im.paste(pic, pos, pic)
            else:
                im.paste(pic.convert("RGB"), pos)
        elif it["kind"] == "text":
            for i, line in enumerate(it["lines"]):
                y = (it["y"] + i * it["line_spacing"] + 0.05 * it["size"]) * K
                widths = [bd.tw(f, it["size"], s[1], s[2]) for f, s in line]
                x = it["x"] + (it["w"] - sum(widths) if it["align"] == "r" else 0)
                for (frag, style), wpt in zip(line, widths):
                    dr.text((x * K, y), frag, font=font(it["size"], style[1],
                                                        style[2]),
                            fill=rgb(style[0]))
                    x += wpt
            if guides:
                b = it["tbox"]
                dr.rectangle([b[0] * K, b[1] * K, b[2] * K, b[3] * K],
                             outline=(255, 150, 150))
    return im


def main():
    clean = "--clean" in sys.argv
    if clean:
        if os.path.isdir(OUT):
            for f in os.listdir(OUT):
                os.remove(os.path.join(OUT, f))
            os.rmdir(OUT)
        print("removed", OUT)
        return
    guides = "--guides" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    warns, ims = [], []
    for spec in bd.NARR:
        items, w = bd.plan_slide(spec)
        w = w + bd.check(spec, items)
        warns += w
        im = render(items, guides=guides)
        im.save(os.path.join(OUT, "slide%02d.png" % spec["n"]))
        ims.append(im)
    if "--sheets" in sys.argv:
        per, sc = 4, 0.52
        for k in range(0, len(ims), per):
            grp = [i.resize((int(i.width * sc), int(i.height * sc)), Image.LANCZOS)
                   for i in ims[k:k + per]]
            cw, ch = grp[0].width, grp[0].height
            sheet = Image.new("RGB", (cw, ch * len(grp)), (170, 170, 170))
            for j, g in enumerate(grp):
                sheet.paste(g, (0, j * ch))
            sheet.save(os.path.join(OUT, "sheet%02d.png" % (k // per + 1)))
    for x in warns:
        print("WARN", x)
    print(f"{len(ims)} previews in {OUT}" + ("" if warns else "; no warnings"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""figure-hygiene QA: render every figure so it can be looked at, and check the rules.

Usage:
    python3 qa.py [DIR]      # DIR contains a figures/ folder (default: cwd)
    python3 qa.py --clean [DIR]

For each PDF in DIR/figures/ it:
  - renders page 1 to a PNG in DIR/figures/_figqa/  (throwaway; --clean removes it)
  - reports the physical size (no width rule: single figures are sized for screen)
  - flags any embedded font that is not Arial (e.g. a DejaVu Sans fallback)
  - flags rasters (.png/.jpg) sitting in figures/  (hygiene: vector PDF only)
  - flags any PDF with no entry in figure_captions.md (looked for in DIR, then figures/)

A figure you have not looked at is not done. After this runs, OPEN the PNGs in
_figqa/ and check each one: nothing clipped, every glyph legible at print size,
colors distinguishable in grayscale.

Exit code is nonzero if any rule is violated, so it can gate a build.
"""
import sys
from pathlib import Path


def render(pdf: Path, out_dir: Path):
    """Rasterize page 1 -> PNG. Returns (png_path, width_in, height_in) or (None,..)."""
    out = out_dir / (pdf.stem + "_qa.png")
    try:
        import fitz  # PyMuPDF
        d = fitz.open(pdf); p = d[0]
        p.get_pixmap(dpi=130).save(out)
        r = p.rect
        return out, r.width / 72, r.height / 72
    except ImportError:
        pass
    # fallback: pdftoppm (poppler)
    import subprocess, shutil
    if shutil.which("pdftoppm"):
        subprocess.run(["pdftoppm", "-png", "-r", "130", "-singlefile",
                        str(pdf), str(out.with_suffix(""))], check=True)
        return out, None, None
    print("  ! no PDF rasterizer (pip install pymupdf, or install poppler)")
    return None, None, None


def fonts(pdf: Path):
    """Embedded font names (subset prefix stripped), or None if no reader."""
    try:
        import fitz
        names = {f[3] for page in fitz.open(pdf) for f in page.get_fonts()}
    except ImportError:
        import subprocess, shutil
        if not shutil.which("pdffonts"):
            return None
        out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout
        names = {l.split()[0] for l in out.splitlines()[2:] if l.strip()}
    return {n.split("+", 1)[-1] for n in names}


def main():
    args = [a for a in sys.argv[1:]]
    clean = "--clean" in args
    args = [a for a in args if a != "--clean"]
    base = Path(args[0]) if args else Path.cwd()
    figs = base / "figures" if (base / "figures").is_dir() else base
    qa_dir = figs / "_figqa"

    if clean:
        if qa_dir.is_dir():
            for f in qa_dir.iterdir():
                f.unlink()
            qa_dir.rmdir()
            print(f"removed {qa_dir}")
        return 0

    if not figs.is_dir():
        print(f"no figures/ folder at {base}"); return 1

    pdfs = sorted(figs.glob("*.pdf"))
    strays = sorted(figs.glob("*.png")) + sorted(figs.glob("*.jpg")) + sorted(figs.glob("*.jpeg"))
    # captions live in the experiment folder; accept figures/ too
    cap = next((p for p in (base / "figure_captions.md", figs / "figure_captions.md")
                if p.exists()), base / "figure_captions.md")
    cap_txt = cap.read_text() if cap.exists() else ""

    problems = 0
    qa_dir.mkdir(exist_ok=True)
    print(f"figures/: {len(pdfs)} PDF(s) in {figs}\n")

    for pdf in pdfs:
        png, w, h = render(pdf, qa_dir)
        line = f"  {pdf.name}"
        if w:
            line += f"  {w:.2f} x {h:.2f} in"
        fs = fonts(pdf)
        bad = sorted(f for f in (fs or ()) if not f.startswith("Arial"))
        if bad:
            line += f"  ! non-Arial font(s): {', '.join(bad)}"; problems += 1
        if pdf.name not in cap_txt:
            line += "  ! NO caption entry"; problems += 1
        if png:
            line += f"  -> {png.relative_to(figs)}"
        print(line)

    if not cap.exists():
        print("\n  ! figure_captions.md missing"); problems += 1
    for s in strays:
        print(f"  ! raster in figures/ (PDF only): {s.name}"); problems += 1

    print(f"\nLOOK at the PNGs in {qa_dir.relative_to(base) if qa_dir.is_relative_to(base) else qa_dir}"
          f" — a figure you have not looked at is not done.")
    print(f"clean up with:  {sys.executable} {Path(__file__)} --clean {base}")
    print(f"\n{'PASS — no rule violations' if problems == 0 else f'{problems} problem(s) to fix'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

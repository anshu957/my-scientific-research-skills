"""Generate a synthetic multi-panel 'journal figure' PDF for the worked example.

Real papers are copyrighted, so the example ships a generator instead of a paper:
this writes source_figure.pdf, a two-page figure with panels A-F laid out the way
a journal figure is -- panels packed edge to edge, labels in bold at the top-left
of each -- which is exactly the layout crop_panels.py exists to take apart.

    python3 make_source_figure.py
"""
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

rng = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({"font.size": 7, "axes.linewidth": 0.6,
                     "xtick.labelsize": 6, "ytick.labelsize": 6})


def label(ax, letter):
    ax.text(-0.22, 1.12, letter, transform=ax.transAxes,
            fontsize=11, fontweight="bold", va="top")


def page1():
    fig = plt.figure(figsize=(7.2, 4.4))
    gs = fig.add_gridspec(2, 3, hspace=0.55, wspace=0.45,
                          left=0.09, right=0.97, top=0.90, bottom=0.12)

    ax = fig.add_subplot(gs[0, 0]); label(ax, "A")
    t = np.linspace(0, 24, 400)
    ax.plot(t, 1.6 + np.sin(2 * np.pi * t / 24 - 1.2), lw=1, color="k")
    ax.set_xlabel("time of day (h)"); ax.set_ylabel("activity (a.u.)")
    ax.set_title("Daily activity", fontsize=8)

    ax = fig.add_subplot(gs[0, 1]); label(ax, "B")
    n = np.arange(1, 16)
    ax.plot(n, 100 * (1 - np.exp(-n / 4.5)), "o-", ms=3, lw=1, color="k")
    ax.set_xlabel("component"); ax.set_ylabel("variance explained (%)")
    ax.set_title("Model order", fontsize=8)

    ax = fig.add_subplot(gs[0, 2]); label(ax, "C")
    im = rng.normal(size=(40, 60)).cumsum(axis=1)
    ax.imshow(im, aspect="auto", cmap="Greys")
    ax.set_xlabel("day"); ax.set_ylabel("state")
    ax.set_title("State usage across life", fontsize=8)

    ax = fig.add_subplot(gs[1, 0]); label(ax, "D")
    for c, off in (("#1f77b4", 0.0), ("#e8b23a", -0.9)):
        x = np.linspace(0, 10, 120)
        ax.plot(x, off + np.sin(x / 2) + rng.normal(0, 0.08, x.size), lw=1, color=c)
    ax.set_xlabel("age (a.u.)"); ax.set_ylabel("PC1")
    ax.set_title("Trajectories by group", fontsize=8)

    ax = fig.add_subplot(gs[1, 1]); label(ax, "E")
    a = rng.normal(6.2, 0.8, 40); b = rng.normal(4.9, 0.9, 40)
    ax.plot(np.ones_like(a) + rng.normal(0, .05, 40), a, ".", ms=3, color="#1f77b4")
    ax.plot(2 * np.ones_like(b) + rng.normal(0, .05, 40), b, ".", ms=3, color="#e8b23a")
    ax.hlines([a.mean(), b.mean()], [0.8, 1.8], [1.2, 2.2], color="k", lw=1)
    ax.set_xticks([1, 2]); ax.set_xticklabels(["group 1", "group 2"])
    ax.set_ylabel("peak velocity"); ax.set_title("At fixed age  P < 0.0001", fontsize=8)

    ax = fig.add_subplot(gs[1, 2]); label(ax, "F")
    x = np.sort(rng.uniform(20, 320, 300))
    ax.plot(x, x + rng.normal(0, 22, x.size), ".", ms=2, color="0.35")
    ax.plot([20, 320], [20, 320], color="#b32020", lw=1)
    ax.text(0.05, 0.92, "R = 0.94", transform=ax.transAxes, fontsize=7, style="italic")
    ax.set_xlabel("true age (d)"); ax.set_ylabel("estimated age (d)")
    ax.set_title("Model estimate", fontsize=8)
    return fig


def main():
    out = os.path.join(HERE, "source_figure.pdf")
    with PdfPages(out) as pdf:
        pdf.savefig(page1())
    print(out)


if __name__ == "__main__":
    main()

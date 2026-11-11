# 2장 §2 1) 조건부확률: Aa × Aa 퍼넷 사각형에서 "우성 표현형 = 4칸 중 3칸, 그중 Aa = 2칸 → 2/3"
# 숫자는 본문과 같음: 각 칸 1/2 × 1/2 = 1/4, 답 2/3 (1/2이 아님), 시뮬레이션 0.665
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch02")

LABELS = {
    "ko": dict(p1="① 4칸 모두", p2="② 우성 표현형만 셈", mom="엄마", dad="아빠",
               each="각 칸 1/2 × 1/2 = 1/4",
               lg_cond="우성 표현형 3칸", lg_event="그중 Aa 2칸", lg_out="aa: 조건 밖",
               eq="P(Aa | 우성 표현형) = 2칸 / 3칸 =", ans="2/3",
               note="(1/2이 아님 · 시뮬레이션 0.665)"),
    "en": dict(p1="① All 4 cells", p2="② Count dominant phenotype only", mom="Mother", dad="Father",
               each="each cell 1/2 × 1/2 = 1/4",
               lg_cond="dominant: 3 cells", lg_event="Aa: 2 cells", lg_out="aa: left out",
               eq="P(Aa | dominant) = 2 cells / 3 cells =", ans="2/3",
               note="(not 1/2 · simulation 0.665)"),
}
COND_C, EVENT_C, EDGE_C = STEPS[2], STEPS[0], PRIMARY
GENO = [["AA", "Aa"], ["aA", "aa"]]          # rows = father's allele, columns = mother's allele
CS, YT = 0.95, 3.55                          # cell size, top of the grids
YB = YT - 2 * CS
GAP = 0.04


def frame(ax, t, x0):
    """Parent labels and allele letters around a 2 × 2 grid with left edge x0 (all horizontal)."""
    label(ax, x0 + CS, YT + 0.5, t["mom"], fs=11.5, c=TEXT2)
    label(ax, x0 - 0.42, YB + CS, t["dad"], fs=11.5, c=TEXT2, ha="right")
    for k, a in enumerate("Aa"):
        label(ax, x0 + CS * (k + 0.5), YT + 0.2, a, fs=13, w="bold")
        label(ax, x0 - 0.2, YT - CS * (k + 0.5), a, fs=13, w="bold")


def cell(ax, x0, r, c, fc, ec="none", ls="-", lw=1.0, tc=None):
    x, y = x0 + c * CS, YT - (r + 1) * CS
    box(ax, x + GAP, y + GAP, CS - 2 * GAP, CS - 2 * GAP, fc=fc, ec=ec, lw=lw, ls=ls, r=0.06)
    label(ax, x + CS / 2, y + CS / 2, GENO[r][c], fs=14, w="bold", c=tc or on(fc))


def right_edge(fig, txt):
    fig.canvas.draw()
    return txt.get_window_extent().x1 / fig.dpi   # axis spans the figure in inches


def draw(t, path):
    fig, ax = new(8.4, 4.7)

    # ① full Punnett square: four equal cells
    xa = 1.0
    label(ax, 0.1, 4.45, t["p1"], fs=12.5, w="bold", ha="left")
    frame(ax, t, xa)
    for r in range(2):
        for c in range(2):
            cell(ax, xa, r, c, FAINT, ec=LINE, lw=1.2, tc=TEXT)
    label(ax, xa + CS, YB - 0.35, t["each"], fs=11.5, c=TEXT2)

    arrow(ax, xa + 2 * CS + 0.15, YB + CS, 3.55, YB + CS, color="#9AA1AB", lw=1.6, ms=13)

    # ② condition: dominant phenotype (3 cells); event inside it: Aa (2 cells)
    xb = 4.6
    label(ax, 3.7, 4.45, t["p2"], fs=12.5, w="bold", ha="left")
    frame(ax, t, xb)
    cell(ax, xb, 0, 0, COND_C)
    cell(ax, xb, 0, 1, EVENT_C)
    cell(ax, xb, 1, 0, EVENT_C)
    cell(ax, xb, 1, 1, "white", ec=TEXT2, ls=(0, (3, 2)), lw=1.1, tc=TEXT2)
    L = [(xb, YT), (xb + 2 * CS, YT), (xb + 2 * CS, YT - CS), (xb + CS, YT - CS),
         (xb + CS, YB), (xb, YB)]
    ax.add_patch(mp.Polygon(L, closed=True, fill=False, ec=EDGE_C, lw=2.4, joinstyle="round", zorder=6))

    # key to the right of grid ②
    sx, sw = xb + 2 * CS + 0.22, 0.24
    keys = [(YT - 0.3, dict(fc=COND_C, ec=EDGE_C, lw=2.0), t["lg_cond"], TEXT),
            (YT - 0.75, dict(fc=EVENT_C, ec="none"), t["lg_event"], TEXT),
            (YB + CS / 2, dict(fc="white", ec=TEXT2, lw=1.1, ls=(0, (3, 2))), t["lg_out"], TEXT2)]
    for y, st, txt, col in keys:
        box(ax, sx, y - sw / 2, sw, sw, r=0.04, **st)
        label(ax, sx + sw + 0.12, y, txt, fs=11.5, c=col, ha="left")

    # answer (the one accent in this figure)
    ya = 0.6
    box(ax, 0.1, ya - 0.36, 8.2, 0.72, fc=FAINT, ec="none", r=0.1)
    t1 = label(ax, 0.3, ya, t["eq"], fs=13, w="bold", ha="left")
    x2 = right_edge(fig, t1) + 0.12
    t2 = label(ax, x2, ya, t["ans"], fs=18, w="bold", c=ACCENT_INK, ha="left")
    x3 = right_edge(fig, t2) + 0.15
    label(ax, x3, ya, t["note"], fs=11.5, c=TEXT2, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"punnett{suffix}.png"))

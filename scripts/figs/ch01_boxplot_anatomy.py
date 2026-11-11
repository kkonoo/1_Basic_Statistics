# 1장 §5 2) Boxplot의 각 부분: 중앙값, Q1·Q3(상자 높이 = IQR), 수염(1.5 × IQR 안의 가장 먼 값까지), 수염 밖의 점
# 값은 설명용 가상 자료(눈금·숫자 없음). 상자 끝은 R boxplot()처럼 fivenum()의 경첩으로 계산
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch01")

VALS = [3.1, 3.6, 3.9, 4.2, 4.4, 4.6, 4.8, 5.0, 5.3, 5.7, 6.1, 8.9]   # 설명용


def fivenum(v):
    s, n = sorted(v), len(v)
    n4 = math.floor((n + 3) / 2) / 2
    d = [1, n4, (n + 1) / 2, n + 1 - n4, n]
    return [0.5 * (s[math.floor(i) - 1] + s[math.ceil(i) - 1]) for i in d]


_, Q1, MED, Q3, _ = fivenum(VALS)
IQR_ = Q3 - Q1
FENCE_HI, FENCE_LO = Q3 + 1.5 * IQR_, Q1 - 1.5 * IQR_
W_HI = max(v for v in VALS if v <= FENCE_HI)
W_LO = min(v for v in VALS if v >= FENCE_LO)
OUTS = [v for v in VALS if v > FENCE_HI or v < FENCE_LO]

LABELS = {
    "ko": dict(q3="Q3 (75%)", med="중앙값 (50%)", q1="Q1 (25%)",
               iqr="IQR = Q3 − Q1", iqr_sub="= 상자 높이 (가운데 50%)",
               whisk="수염 (whisker)", whisk_sub="상자에서 1.5 × IQR 안의 가장 먼 값까지",
               low="아래 수염도 같은 규칙", fence="Q3 + 1.5 × IQR", span="1.5 × IQR",
               out="이상치 후보", out_sub="수염 밖의 점", dots="점 = 값 하나"),
    "en": dict(q3="Q3 (75%)", med="Median (50%)", q1="Q1 (25%)",
               iqr="IQR = Q3 − Q1", iqr_sub="= box height (middle 50%)",
               whisk="Whisker", whisk_sub="to the farthest value within 1.5 × IQR of the box",
               low="lower whisker: same rule", fence="Q3 + 1.5 × IQR", span="1.5 × IQR",
               out="Possible outlier", out_sub="point beyond the whisker", dots="each dot = one value"),
}
GUIDE = mix(TEXT2, 0.45)


def draw(t, path):
    fig, ax = new(7.3, 5.4)
    sy = lambda v: 0.55 + (v - 2.7) * 0.72
    BX0, BX1 = 2.0, 3.2                      # box
    CX = (BX0 + BX1) / 2
    CAP = 0.25
    RX = 3.6                                 # right label column
    WHITE = dict(fc="white", ec="none", pad=1.5)

    # raw points beside the box (n is small → show them)
    px = 0.45
    for k, v in enumerate(sorted(VALS)):
        dx = [0.0, -0.11, 0.11][k % 3]
        ax.add_patch(mp.Circle((px + dx, sy(v)), 0.065, fc=STEPS[0], ec="white", lw=0.8, zorder=4))
    label(ax, 0.1, 0.3, t["dots"], fs=11, c=TEXT2, ha="left")

    # guides from the points to the box: Q1, median, Q3 split the points
    for v, key in [(Q3, "q3"), (MED, "med"), (Q1, "q1")]:
        ax.plot([0.1, BX0], [sy(v)] * 2, color=GUIDE, lw=1.0, ls=(0, (2, 3)), zorder=1)
        label(ax, 1.85, sy(v), t[key], fs=12, w="bold", ha="right", bbox=WHITE)

    # box, median, whiskers
    box(ax, BX0, sy(Q1), BX1 - BX0, sy(Q3) - sy(Q1), fc=STEPS[3], ec=PRIMARY, lw=1.6, r=0.02, z=2)
    ax.plot([BX0, BX1], [sy(MED)] * 2, color=PRIMARY, lw=4, solid_capstyle="butt", zorder=3)
    for a, b in [(Q3, W_HI), (Q1, W_LO)]:
        ax.plot([CX, CX], [sy(a), sy(b)], color=PRIMARY, lw=1.6, zorder=3)
        ax.plot([CX - CAP, CX + CAP], [sy(b)] * 2, color=PRIMARY, lw=1.6, zorder=3)

    # 1.5 × IQR reach above Q3 (left bracket) and the limit line
    bx = 1.9
    ax.plot([bx + 0.07, bx, bx, bx + 0.07], [sy(Q3), sy(Q3), sy(FENCE_HI), sy(FENCE_HI)],
            color=TEXT2, lw=1.1, zorder=3)
    label(ax, bx - 0.12, (sy(Q3) + sy(FENCE_HI)) / 2, t["span"], fs=11.5, c=TEXT2, ha="right")
    ax.plot([bx, RX - 0.1], [sy(FENCE_HI)] * 2, color=TEXT2, lw=1.1, ls=(0, (4, 3)), zorder=2)
    label(ax, RX, sy(FENCE_HI), t["fence"], fs=11.5, c=TEXT2, ha="left")

    # outlier: the one accent
    for v in OUTS:
        ax.add_patch(mp.Circle((CX, sy(v)), 0.085, fc=ACCENT, ec=ACCENT_INK, lw=1.0, zorder=5))
        ax.plot([CX + 0.14, RX - 0.1], [sy(v)] * 2, color=GUIDE, lw=1.0, zorder=2)
        label(ax, RX, sy(v) + 0.11, t["out"], fs=12.5, w="bold", c=ACCENT_INK, ha="left")
        label(ax, RX, sy(v) - 0.13, t["out_sub"], fs=11, c=TEXT2, ha="left")

    # IQR bracket on the right of the box
    ib = BX1 + 0.14
    ax.plot([ib - 0.07, ib, ib, ib - 0.07], [sy(Q1), sy(Q1), sy(Q3), sy(Q3)],
            color=TEXT2, lw=1.1, zorder=3)
    ym = (sy(Q1) + sy(Q3)) / 2
    ax.plot([ib, RX - 0.1], [ym, ym], color=GUIDE, lw=1.0, zorder=2)
    label(ax, RX, ym + 0.12, t["iqr"], fs=12.5, w="bold", ha="left")
    label(ax, RX, ym - 0.13, t["iqr_sub"], fs=11, c=TEXT2, ha="left")

    # whisker labels
    ax.plot([CX + CAP + 0.05, RX - 0.1], [sy(W_HI)] * 2, color=GUIDE, lw=1.0, zorder=2)
    label(ax, RX, sy(W_HI) + 0.11, t["whisk"], fs=12.5, w="bold", ha="left")
    label(ax, RX, sy(W_HI) - 0.13, t["whisk_sub"], fs=11, c=TEXT2, ha="left")
    ax.plot([CX + CAP + 0.05, RX - 0.1], [sy(W_LO)] * 2, color=GUIDE, lw=1.0, zorder=2)
    label(ax, RX, sy(W_LO), t["low"], fs=11.5, c=TEXT, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"boxplot_anatomy{suffix}.png"))

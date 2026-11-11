# 6장 §3.1 라벨 섞기: 값은 그대로 두고 Chow/HFD 라벨만 다시 나눠 평균 차이를 구함
# 값은 6장 자료(set.seed(20261016))와 같음. 섞은 예 3개는 combn(12, 6)의 100·299·129번째 열
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch06")

chow = [4.73, 5.31, 3.58, 7.07, 5.14, 4.71]          # 마우스 1–6
hfd = [6.75, 5.76, 6.90, 5.30, 5.68, 6.40]           # 마우스 7–12
x = chow + hfd
ROWS = [  # mice called "HFD" (1-based), True = the real labels
    ([7, 8, 9, 10, 11, 12], True),
    ([1, 2, 4, 5, 9, 10], False),
    ([1, 3, 5, 9, 10, 12], False),
    ([1, 2, 4, 7, 10, 12], False),
]

LABELS = {
    "ko": dict(real="실제 라벨", shuf="섞기", diff="차이 1.04",
               note="$H_0$가 참이면 라벨은 의미가 없음 → 12마리를 아무렇게나 6 + 6으로 나눔",
               more="⋮  나누는 방법은 모두 924가지",
               axis="Cd36 발현 (log2 CPM)",
               res1="평균 차이 924개 = 귀무분포",
               res2="|차이| ≥ 1.04인 나누기 78가지  →  p = 78 / 924 = 0.084"),
    "en": dict(real="Real labels", shuf="Shuffle", diff="difference 1.04",
               note="If $H_0$ is true the labels mean nothing → split the 12 mice 6 + 6 at random",
               more="⋮  924 possible splits in total",
               axis="Cd36 expression (log2 CPM)",
               res1="924 mean differences = null distribution",
               res2="78 splits with |difference| ≥ 1.04  →  p = 78 / 924 = 0.084"),
}
HFD_C, CHOW_C = PRIMARY, "#8C939D"


def draw(t, path):
    fig, ax = new(8.0, 6.9)
    X0, X1, V0, V1 = 1.9, 7.0, 3.4, 7.3
    sx = lambda v: X0 + (v - V0) / (V1 - V0) * (X1 - X0)
    lane, r, band = 0.18, 0.075, 0.42

    def row(yc, hfd_ids, real, k):
        name = t["real"] if real else f"{t['shuf']} {'①②③'[k - 1]}"
        label(ax, 0.1, yc, name, fs=12.5, w="bold", ha="left")
        label(ax, X0 - 0.15, yc + lane, "HFD", fs=11, w="bold", c=HFD_C, ha="right")
        label(ax, X0 - 0.15, yc - lane, "Chow", fs=11, w="bold", c=CHOW_C, ha="right")
        box(ax, X0 - 0.05, yc - band, X1 - X0 + 0.1, 2 * band, fc=FAINT, ec="none", r=0.06, z=1)
        for v in [4, 5, 6, 7]:   # faint guides inside the band only
            ax.plot([sx(v)] * 2, [yc - band, yc + band], color=LINE, lw=0.8, zorder=1.5)
        means = {}
        for grp, col, dy in [("H", HFD_C, lane), ("C", CHOW_C, -lane)]:
            ids = [i for i in range(1, 13) if (i in hfd_ids) == (grp == "H")]
            vals = sorted(x[i - 1] for i in ids)
            last = -9
            for v in vals:                       # lift a dot that would sit on its neighbour
                lift = (0.12 if dy > 0 else -0.12) if sx(v) - last < 2 * r else 0   # away from the middle
                ax.add_patch(mp.Circle((sx(v), yc + dy + lift), r, fc=col, ec="white", lw=0.8, zorder=4))
                last = sx(v) if not lift else -9
            m = sum(vals) / 6
            means[grp] = m
            ax.plot([sx(m)] * 2, [yc + dy - 0.13, yc + dy + 0.13], color=col, lw=3, zorder=5,
                    solid_capstyle="butt")
        ax.annotate("", xy=(sx(means["H"]), yc), xytext=(sx(means["C"]), yc),
                    arrowprops=dict(arrowstyle="-|>", color=TEXT, lw=1.3, shrinkA=0, shrinkB=0,
                                    mutation_scale=10), zorder=6)
        if real:
            label(ax, X1 + 0.1, yc, t["diff"], fs=12, w="bold", ha="left")

    y = 6.4
    row(y, *ROWS[0], 0)
    label(ax, 0.1, y - 0.81, t["note"], fs=11.5, c=TEXT2, ha="left")
    for k, (ids, real) in enumerate(ROWS[1:], start=1):
        row(y - 0.62 - k * 1.0, ids, real, k)
    y_last = y - 0.62 - 3 * 1.0
    label(ax, X0, y_last - 0.66, t["more"], fs=11.5, c=TEXT2, ha="left")

    # shared value axis under the rows
    ya = y_last - 1.0
    ax.plot([sx(V0 + 0.1), sx(V1 - 0.1)], [ya, ya], color="#9AA1AB", lw=1)
    for v in [4, 5, 6, 7]:
        ax.plot([sx(v)] * 2, [ya, ya - 0.06], color="#9AA1AB", lw=1)
        label(ax, sx(v), ya - 0.2, str(v), fs=11, c="#4B5563")
    label(ax, (X0 + X1) / 2, ya - 0.45, t["axis"], fs=11.5, c=TEXT)

    # result
    yb = ya - 1.2
    box(ax, 0.1, yb - 0.32, 7.6, 0.64, fc=STEPS[3], ec="none", r=0.1)
    label(ax, 0.3, yb + 0.12, t["res1"], fs=12, w="bold", ha="left")
    label(ax, 0.3, yb - 0.15, t["res2"], fs=12, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"permutation{suffix}.png"))

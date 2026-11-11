# 11장 §3 변동의 층: 전체 평균 μ = 6.0 → 연구실 5곳(위 층, 연구실 사이 SD 0.5) → 연구실마다 마우스 10마리(아래 층, 마우스 사이 SD 0.8)
# 설정과 포함률(0.691, 0.943)은 본문과 같음. 연구실 수준과 마우스 점의 위치는 설명용(축에 숫자 없음)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch11")

MU, N_LAB, N_MOUSE, SD_MOUSE = 6.0, 5, 10, 0.8
LAB_EFF = [0.55, -0.35, 0.10, -0.70, 0.30]          # illustrative a_l (lab 1 on top)
rng = np.random.default_rng(7)
MICE = []
for a in LAB_EFF:                                    # illustrative mice, centred on each lab level
    e = rng.normal(0, SD_MOUSE, N_MOUSE)
    MICE.append(MU + a + (e - e.mean()))

LABELS = {
    "ko": dict(root="전체 평균\n$\\mu$ = 6.0", lab="연구실", mu="$\\mu$",
               axis="Cd36 발현",
               lev="연구실 수준 $\\mu + a_l$", lev_layer="위 층 · 연구실 사이 SD 0.5",
               mouse="마우스 10마리 $y_{lj}$", mouse_layer="아래 층 · 마우스 사이 SD 0.8",
               cov="95% 구간의 실제 포함률",
               naive="마우스 50마리를 독립으로\n(아래 층만)",
               level="연구실 평균 5개로\n(위 층까지)"),
    "en": dict(root="Overall mean\n$\\mu$ = 6.0", lab="Lab", mu="$\\mu$",
               axis="Cd36 expression",
               lev="Lab level $\\mu + a_l$", lev_layer="upper layer · between labs, SD 0.5",
               mouse="10 mice $y_{lj}$", mouse_layer="lower layer · between mice, SD 0.8",
               cov="Actual coverage of the 95% interval",
               naive="50 mice as independent\n(lower layer only)",
               level="5 lab means\n(upper layer included)"),
}
LAB_C = ramp(N_LAB)
GUIDE = "#9AA1AB"


def level_bar(ax, x, y0, y1, col, lw=3.2):
    ax.plot([x, x], [y0, y1], color=col, lw=lw, zorder=5, solid_capstyle="butt")


def draw(t, path):
    fig, ax = new(8.0, 7.2)
    X0, X1, V0, V1 = 2.75, 7.85, 3.4, 8.6
    sx = lambda v: X0 + (v - V0) / (V1 - V0) * (X1 - X0)
    ys = [6.25, 5.5, 4.75, 4.0, 3.25]
    band, r = 0.28, 0.065
    keep = r + 0.07                                  # dots stay this far from the lab-level bar

    # tree: overall mean → labs
    nx, nw, nh, yc_root = 0.05, 1.4, 0.74, ys[2]
    box(ax, nx, yc_root - nh / 2, nw, nh, fc=FAINT, ec=LINE, lw=1.2)
    label(ax, nx + nw / 2, yc_root, t["root"], fs=12, w="bold", linespacing=1.3)
    spine = 1.6
    ax.plot([nx + nw, spine], [yc_root, yc_root], color=GUIDE, lw=1.3, zorder=2)
    ax.plot([spine, spine], [ys[-1], ys[0]], color=GUIDE, lw=1.3, zorder=2)

    for k, (yc, vals, col) in enumerate(zip(ys, MICE, LAB_C)):
        ax.plot([spine, 1.72], [yc, yc], color=GUIDE, lw=1.3, zorder=2)
        label(ax, 1.78, yc, f"{t['lab']} {k + 1}", fs=12, w="bold", ha="left")
        box(ax, X0 - 0.05, yc - band, X1 - X0 + 0.1, 2 * band, fc=FAINT, ec="none", r=0.06, z=1)
        bx = sx(MU + LAB_EFF[k])
        # move dots that would sit on the bar to alternate sides of it
        pxs, side = [], 1
        for v in sorted(np.clip(vals, V0 + 0.15, V1 - 0.15)):
            px = sx(v)
            if abs(px - bx) < keep:
                px = bx + side * keep
                side = -side
            pxs.append(px)
        placed = []                                  # simple beeswarm: first free lane
        for px in sorted(pxs):
            best, best_d = 0.0, -1
            for off in [0.0, 0.13, -0.13, 0.2, -0.2]:
                d = min([np.hypot(px - qx, off - qy) for qx, qy in placed] or [9])
                if d >= 2 * r + 0.01:
                    best = off
                    break
                if d > best_d:
                    best, best_d = off, d
            placed.append((px, best))
            ax.add_patch(mp.Circle((px, yc + best), r, fc=col, ec="white", lw=0.8, zorder=4))
        level_bar(ax, bx, yc - band + 0.03, yc + band - 0.03, col)

    # overall mean line and one lab offset a_1
    ax.plot([sx(MU)] * 2, [ys[-1] - band - 0.05, 6.8], color="#6B7280", lw=1.1,
            ls=(0, (4, 3)), zorder=2.5)
    label(ax, sx(MU), 6.98, t["mu"], fs=12.5, w="bold")
    ya1 = ys[0] + band + 0.14
    arrow(ax, sx(MU), ya1, sx(MU + LAB_EFF[0]), ya1, color=TEXT2, lw=1.3, ms=10)
    label(ax, sx(MU + LAB_EFF[0]) + 0.08, ya1, "$a_1$", fs=12, c=TEXT2, ha="left")

    # value axis (no numbers: positions are illustrative)
    ya = 2.75
    arrow(ax, X0, ya, X1, ya, color=GUIDE, lw=1.1, ms=10)
    label(ax, (X0 + X1) / 2, ya - 0.25, t["axis"], fs=11.5)

    # key: the two layers
    yk1, yk2, xg, xt, xl = 2.05, 1.7, 0.3, 0.55, 2.35
    level_bar(ax, xg, yk1 - 0.13, yk1 + 0.13, PRIMARY)
    label(ax, xt, yk1, t["lev"], fs=11.5, ha="left")
    label(ax, xl, yk1, t["lev_layer"], fs=11.5, w="bold", ha="left")
    ax.add_patch(mp.Circle((xg, yk2), r, fc=PRIMARY, ec="white", lw=0.8, zorder=4))
    label(ax, xt, yk2, t["mouse"], fs=11.5, ha="left")
    label(ax, xl, yk2, t["mouse_layer"], fs=11.5, w="bold", ha="left")

    # coverage result (the one accent: 0.691)
    box(ax, 0.1, 0.1, 7.8, 1.28, fc=STEPS[3], ec="none", r=0.1)
    label(ax, 0.3, 1.12, t["cov"], fs=12, w="bold", ha="left")
    label(ax, 0.3, 0.52, "0.691", fs=18, w="bold", c=ACCENT_INK, ha="left")
    label(ax, 1.25, 0.52, t["naive"], fs=11.5, ha="left", linespacing=1.3)
    label(ax, 4.1, 0.52, "0.943", fs=18, w="bold", c=TEXT, ha="left")
    label(ax, 5.05, 0.52, t["level"], fs=11.5, ha="left", linespacing=1.3)
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"hierarchy{suffix}.png"))

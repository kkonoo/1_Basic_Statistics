# 0장 §3 반복 단위: 대조군·처리군 각 2마리 → 마우스마다 세포 500개 (참값은 그룹 차이 없음)
# 숫자는 본문과 같음: 세포 2000개로 t-검정 p = 3.6e-23, 마우스별 평균(pseudobulk) p = 0.66 (set.seed(7))
# 점의 위치·개수는 설명용 (마우스 1이 높은 개체라는 본문 설명만 따름; 세포는 마우스당 36개만 그림)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch00")

LEVEL = [6.1, 4.4, 4.65, 4.8]          # illustrative per-mouse levels (mouse 1 high), no numbers shown
rng = np.random.default_rng(7)
CELLS = [np.clip(rng.normal(LEVEL[m], 1.0, 36), 2.5, 8.1) for m in range(4)]
JIT_TREE = [rng.uniform(-0.55, 0.55, 36) for _ in range(4)]
JIT_POOL = [rng.uniform(-0.22, 0.22, 72) for _ in range(2)]

LABELS = {
    "ko": dict(ctrl="대조군 (Ctrl)", trt="처리군 (Trt)", mouse="마우스", truth="참값:\n그룹 차이 없음",
               cells500="세포 500개",
               note="세포는 자기 마우스의 고유 수준(가로선) 주위에 모임 → 같은 마우스의 세포끼리 독립이 아님",
               h1="① 세포를 표본으로 세면", s1="세포 2000개를 독립 표본처럼 t-검정",
               h2="② 마우스를 표본으로 세면", s2="마우스별 평균(pseudobulk)으로 t-검정",
               g1="대조군", g2="처리군", false="→ 가짜 차이", ok="차이 없음 = 참값"),
    "en": dict(ctrl="Control (Ctrl)", trt="Treated (Trt)", mouse="Mouse", truth="truth:\nno group difference",
               cells500="500 cells",
               note="Cells cluster around their mouse's own level (line) → not independent of each other",
               h1="① Counting cells", s1="t-test on 2000 cells as if independent",
               h2="② Counting mice", s2="t-test on per-mouse means (pseudobulk)",
               g1="Ctrl", g2="Trt", false="→ a false difference", ok="no difference = truth"),
}
GC = [CAT[0], CAT[0], CAT[1], CAT[1]]
MX = [1.15, 3.0, 5.2, 7.05]


def draw(t, path):
    fig, ax = new(8.2, 7.15)

    # ── nested structure: group → mouse → cells ──
    for g, (gx, col, name) in enumerate([(2.075, CAT[0], t["ctrl"]), (6.125, CAT[1], t["trt"])]):
        box(ax, gx - 1.0, 6.5, 2.0, 0.5, fc=col, ec="none")
        label(ax, gx, 6.75, name, fs=12.5, w="bold", c=on(col))
        for m in (2 * g, 2 * g + 1):
            arrow(ax, gx + (-0.35 if m % 2 == 0 else 0.35), 6.5, MX[m], 6.1, lw=1.3, ms=10)
    label(ax, 4.1, 6.72, t["truth"], fs=11.5, c=TEXT2, linespacing=1.3)

    yb, yh = 3.8, 1.7
    sy = lambda v: yb + 0.1 + (v - 2.4) / 5.8 * (yh - 0.2)
    for m in range(4):
        mx, col = MX[m], GC[m]
        box(ax, mx - 0.6, 5.65, 1.2, 0.45, fc=mix(col, 0.15), ec="none")
        label(ax, mx, 5.875, f"{t['mouse']} {m + 1}", fs=12, w="bold", c=col)
        box(ax, mx - 0.75, yb, 1.5, yh, fc=FAINT, ec="none", r=0.08, z=1)
        for v, j in zip(CELLS[m], JIT_TREE[m]):
            ax.add_patch(mp.Circle((mx + j, sy(v)), 0.035, fc=mix(col, 0.5), ec="white", lw=0.4, zorder=3))
        ax.plot([mx - 0.66, mx + 0.66], [sy(LEVEL[m])] * 2, color=col, lw=2.6, zorder=4,
                solid_capstyle="butt")
        label(ax, mx, 3.62, t["cells500"], fs=11, c=TEXT2)
    label(ax, 4.1, 3.25, t["note"], fs=11.5, c=TEXT2)

    # ── two ways of counting n ──
    py = lambda v: 0.6 + (v - 2.2) / 6.2 * 1.4
    for k, x0 in enumerate([0.1, 4.2]):
        box(ax, x0, 0.1, 3.9, 2.85, fc="white", ec=LINE, lw=1.2, r=0.1, z=1)
        label(ax, x0 + 0.2, 2.65, t["h1" if k == 0 else "h2"], fs=12.5, w="bold", ha="left")
        label(ax, x0 + 0.2, 2.33, t["s1" if k == 0 else "s2"], fs=11, c=TEXT2, ha="left")
        box(ax, x0 + 0.15, 0.5, 1.45, 1.6, fc=FAINT, ec="none", r=0.06, z=1.5)
        cx = [x0 + 0.52, x0 + 1.23]
        for g in range(2):
            col = CAT[g]
            label(ax, cx[g], 0.3, t["g1" if g == 0 else "g2"], fs=11, w="bold", c=col)
            if k == 0:   # every cell pooled by group
                vals = np.concatenate([CELLS[2 * g], CELLS[2 * g + 1]])
                for v, j in zip(vals, JIT_POOL[g]):
                    ax.add_patch(mp.Circle((cx[g] + j, py(v)), 0.024, fc=mix(col, 0.5), ec="white",
                                           lw=0.3, zorder=3))
                gm = vals.mean()
            else:        # one value per mouse
                means = [CELLS[m].mean() for m in (2 * g, 2 * g + 1)]
                for v, dxm in zip(means, (-0.1, 0.1)):
                    ax.add_patch(mp.Circle((cx[g] + dxm, py(v)), 0.06, fc=col, ec="white", lw=0.8,
                                           zorder=5))
                gm = sum(means) / 2
            ax.plot([cx[g] - 0.3, cx[g] + 0.3], [py(gm)] * 2, color=col, lw=2.6, zorder=4,
                    solid_capstyle="butt")

        tx = x0 + 1.75
        label(ax, tx, 1.78, "n = 2000" if k == 0 else "n = 4", fs=16, w="bold", ha="left")
        label(ax, tx, 1.33, r"p = 3.6 × 10$^{-23}$" if k == 0 else "p = 0.66", fs=13, ha="left")
        if k == 0:
            label(ax, tx, 0.78, t["false"], fs=12, w="bold", ha="left")
        else:   # the one accent: the correct unit gives the true answer
            pill(ax, tx, 0.78, t["ok"], fc=ACCENT, tc=ON_ACCENT, fs=12, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"replication_unit{suffix}.png"))

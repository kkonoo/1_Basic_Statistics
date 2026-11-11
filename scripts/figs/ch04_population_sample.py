# 4장 §1–2 모집단 → 표본 → 추정값 → 표집분포: 10마리 실험 한 번이 표본평균 하나를 주고, 1000번 반복하면 표집분포
# 숫자는 본문과 같음: 모집단 10만 마리, μ = 51.2, σ = 40.4, 표본 하나(set.seed(1)) 평균 57.5,
# 1000번 반복(set.seed(2)) 표본평균의 평균 50.4, SD 12.1. 점 위치와 막대 모양은 설명용
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch04")

LABELS = {
    "ko": dict(pop="모집단", pop_sub="고지방식 마우스\n10만 마리",
               param="모수", mu="μ = 51.2 mg/g", sigma="σ = 40.4 mg/g", param_note="고정, 보통 모름",
               sample="표본 (n = 10)", estimator="추정량 $\\bar{x}$", estimate="추정값",
               sdist="표집분포", sdist_sub="$\\bar{x}$ 1000개",
               row1="실험 1: 표본 하나 → 추정값 하나", row2="실험 2", row3="실험 1000",
               more="⋮  1000번 반복", mean="평균 50.4 ≈ μ", sd="SD 12.1"),
    "en": dict(pop="Population", pop_sub="100,000 mice\non a high-fat diet",
               param="Parameters", mu="μ = 51.2 mg/g", sigma="σ = 40.4 mg/g", param_note="fixed but unknown",
               sample="Sample (n = 10)", estimator="estimator $\\bar{x}$", estimate="Estimate",
               sdist="Sampling\ndistribution", sdist_sub="1000 $\\bar{x}$ values",
               row1="Experiment 1: one sample → one estimate", row2="Experiment 2", row3="Experiment 1000",
               more="⋮  repeated 1000 times", mean="mean 50.4 ≈ μ", sd="SD 12.1"),
}
MOUSE = PRIMARY          # mice (population and samples): primary family
MEAN_C = CAT[1]          # sample means (chips and histogram)


def draw(t, path):
    fig, ax = new(8.0, 5.2)
    ROWS = [3.95, 2.8, 1.25]
    head_y = 4.85

    # ── population ──────────────────────────────────────────────
    px, pw, py0, py1 = 0.1, 2.0, 0.65, 4.55
    box(ax, px, py0, pw, py1 - py0, fc=STEPS[3], ec="none", r=0.12)
    label(ax, px + pw / 2, 4.25, t["pop"], fs=13, w="bold")
    label(ax, px + pw / 2, 3.8, t["pop_sub"], fs=11.5, c=TEXT2, linespacing=1.25)
    rng = np.random.default_rng(4)
    pts = []
    while len(pts) < 70:                                   # illustrative cloud of mice
        p = (rng.uniform(0.3, 1.9), rng.uniform(2.2, 3.4))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.11 ** 2 for q in pts):
            pts.append(p)
    for (x, y) in pts:
        ax.add_patch(mp.Circle((x, y), 0.042, fc=MOUSE, ec="none", zorder=3))
    box(ax, 0.25, 0.8, 1.7, 1.2, fc="white", ec="none", r=0.08, z=3)
    label(ax, 1.1, 1.78, t["param"], fs=12, w="bold", c=PRIMARY)
    label(ax, 1.1, 1.5, t["mu"], fs=11.5)
    label(ax, 1.1, 1.24, t["sigma"], fs=11.5)
    label(ax, 1.1, 0.98, t["param_note"], fs=11, c=TEXT2)

    # ── column headings ─────────────────────────────────────────
    sx, sw, sh = 2.6, 1.35, 0.5
    cx, cw, chh = 4.85, 0.95, 0.44
    hx0, hx1 = 6.45, 7.9
    label(ax, sx + sw / 2, head_y, t["sample"], fs=12.5, w="bold")
    label(ax, cx + cw / 2, head_y, t["estimate"], fs=12.5, w="bold")
    label(ax, (hx0 + hx1) / 2, head_y, t["sdist"], fs=12.5, w="bold", linespacing=1.15)
    label(ax, (sx + sw + cx) / 2, 4.34, t["estimator"], fs=11.5, c=TEXT2)

    # ── experiments: sample → x̄ ─────────────────────────────────
    targets = [3.15, 2.7, 2.2]
    for k, yc in enumerate(ROWS):
        arrow(ax, px + pw + 0.05, yc, sx - 0.03, yc, color=TEXT2, lw=1.4, ms=11)
        box(ax, sx, yc - sh / 2, sw, sh, fc=FAINT, ec=LINE, r=0.08)
        x0 = sx + sw / 2 - 4.5 * 0.12
        for i in range(10):
            ax.add_patch(mp.Circle((x0 + i * 0.12, yc), 0.045, fc=MOUSE, ec="none", zorder=3))
        arrow(ax, sx + sw + 0.05, yc, cx - 0.03, yc, color=TEXT2, lw=1.4, ms=11)
        if k == 0:     # the one accent: one experiment gives one estimate
            box(ax, cx, yc - chh / 2, cw, chh, fc=ACCENT, ec="none", r=chh / 2, z=3)
            label(ax, cx + cw / 2, yc, "$\\bar{x}$ = 57.5", fs=12, w="bold", c=ON_ACCENT)
        else:
            box(ax, cx, yc - chh / 2, cw, chh, fc=MEAN_C, ec="none", r=chh / 2, z=3)
            label(ax, cx + cw / 2, yc, "$\\bar{x}$", fs=12.5, w="bold", c=on(MEAN_C))
        arrow(ax, cx + cw + 0.05, yc, hx0 - 0.08, targets[k], color=TEXT2, lw=1.3, ms=10)

    label(ax, sx, ROWS[0] - 0.42, t["row1"], fs=11.5, w="bold", ha="left")
    label(ax, sx, ROWS[1] - 0.42, t["row2"], fs=11, c=TEXT2, ha="left")
    label(ax, sx, 1.92, t["more"], fs=11.5, c=TEXT2, ha="left")
    label(ax, sx, ROWS[2] - 0.42, t["row3"], fs=11, c=TEXT2, ha="left")

    # ── sampling distribution (sketch, taller so it sits under its heading) ──
    base = 1.75
    hts = [0.15, 0.42, 0.78, 1.1, 1.0, 0.76, 0.5, 0.3, 0.15]   # illustrative shape
    bw = (hx1 - hx0) / len(hts)
    for i, h in enumerate(hts):
        box(ax, hx0 + i * bw + 0.01, base, bw - 0.02, h * 1.95, fc=MEAN_C, ec="none", r=0.0)
    ax.plot([hx0 - 0.03, hx1 + 0.03], [base, base], color="#9AA1AB", lw=1.1, zorder=3)
    label(ax, (hx0 + hx1) / 2, 4.2, t["sdist_sub"], fs=11, c=TEXT2)
    label(ax, (hx0 + hx1) / 2, 1.45, t["mean"], fs=11.5)
    label(ax, (hx0 + hx1) / 2, 1.15, t["sd"], fs=11.5)
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"population_sample{suffix}.png"))

# 7장 §1–2 두 세계의 t 분포: 효과 없음(Δ = 0)과 효과 있음(Δ = 1.0)에서 α, β, 검정력
# 설정은 7장과 같음: 그룹당 6마리, σ = 0.8, 양측 α = 0.05, 등분산 t-검정(자유도 10)
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch07")

n, sigma, delta, df = 6, 0.8, 1.0, 10
ncp = delta / (sigma * math.sqrt(2 / n))                 # 2.165
x = np.linspace(-4.6, 7.2, 1200)


def t_pdf(t, k):
    c = math.gamma((k + 1) / 2) / (math.sqrt(k * math.pi) * math.gamma(k / 2))
    return c * (1 + t ** 2 / k) ** (-(k + 1) / 2)


def nct_pdf(t, k, d):
    """Non-central t density by integrating over the chi-square variable."""
    v = np.linspace(1e-6, 80, 6000)[:, None]
    chi = v ** (k / 2 - 1) * np.exp(-v / 2) / (2 ** (k / 2) * math.gamma(k / 2))
    s = np.sqrt(v / k)
    phi = np.exp(-(t[None, :] * s - d) ** 2 / 2) / math.sqrt(2 * math.pi)
    return np.trapezoid(chi * s * phi, v[:, 0], axis=0)


f0, f1 = t_pdf(x, df), nct_pdf(x, df, ncp)
dx = x[1] - x[0]
crit = 2.228139                                          # qt(0.975, 10)
power = (f1[x >= crit].sum() + f1[x <= -crit].sum()) * dx
alpha = (f0[np.abs(x) >= crit].sum()) * dx
print(f"alpha ≈ {alpha:.3f}, power ≈ {power:.3f}")      # 0.050, 0.50 (본문: 검정력 0.50, 시뮬레이션 0.503)

LABELS = {
    "ko": dict(null="효과 없는 세계 (Δ = 0)", alt="효과 있는 세계 (Δ = 1.0)", crit="기각 경계",
               alpha="α = 0.05\n(양쪽 꼬리 합)", power="검정력\n0.50", beta="β = 0.50\n효과가 있는데 놓침",
               ch6="6장의 실험\nt = 1.95", xlab="t 통계량 (그룹당 6마리, 자유도 10)"),
    "en": dict(null="No effect (Δ = 0)", alt="True effect (Δ = 1.0)", crit="rejection cut-off",
               alpha="α = 0.05\n(both tails)", power="power\n0.50", beta="β = 0.50\nmissed a real effect",
               ch6="Ch. 6 experiment\nt = 1.95", xlab="t statistic (6 mice per group, 10 df)"),
}
NULL_C = "#8C939D"


def draw(t, path):
    fig, ax = plt.subplots(figsize=(8.0, 4.3))
    ax.spines["left"].set_visible(False); ax.set_yticks([])
    top = f0.max() * 1.32
    # β: under the alternative, inside the cut-offs (the one accent in this figure)
    m = (x > -crit) & (x < crit)
    ax.fill_between(x[m], f1[m], color=mix(ACCENT, 0.6), lw=0, zorder=1)
    # power: under the alternative, beyond the cut-off
    m = x >= crit
    ax.fill_between(x[m], f1[m], color=mix(PRIMARY, 0.45), lw=0, zorder=1)
    # α: tails of the null
    for m in (x >= crit, x <= -crit):
        ax.fill_between(x[m], f0[m], color=mix(NULL_C, 0.75), lw=0, zorder=2)
    ax.plot(x, f0, color=NULL_C, lw=2, zorder=3)
    ax.plot(x, f1, color=PRIMARY, lw=2, zorder=3)
    for c in (-crit, crit):
        ax.plot([c, c], [0, top * 0.9], color="#6B7280", lw=1.1, ls=(0, (4, 3)), zorder=4)
    ax.text(crit, top * 0.93, t["crit"], ha="center", va="bottom", fontsize=11, color=TEXT2)
    ax.text(-crit, top * 0.93, t["crit"], ha="center", va="bottom", fontsize=11, color=TEXT2)

    ax.text(-0.15, f0.max() * 1.05, t["null"], ha="center", va="bottom", fontsize=12.5,
            fontweight="bold", color="#5B626C")
    i1 = f1.argmax()
    ax.text(x[i1] + 0.75, f1.max() * 1.05, t["alt"], ha="left", va="bottom", fontsize=12.5,
            fontweight="bold", color=PRIMARY)
    ax.text(3.35, 0.07, t["power"], ha="center", va="center", fontsize=12, fontweight="bold",
            color="white", linespacing=1.25, zorder=5)
    ax.annotate(t["beta"], xy=(1.3, 0.12), xytext=(-4.4, 0.27), fontsize=11.5, fontweight="bold",
                color=ACCENT_INK, ha="left", va="center", linespacing=1.35, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_INK, lw=1.3, connectionstyle="arc3,rad=-0.2"))
    ax.annotate(t["alpha"], xy=(-2.75, 0.012), xytext=(-4.4, 0.115), fontsize=11, color="#4B5563",
                ha="left", va="center", linespacing=1.3,
                arrowprops=dict(arrowstyle="-|>", color="#9AA1AB", lw=1.1))
    # chapter 6's single experiment
    ax.plot([1.95], [0], marker="^", ms=10, color=TEXT, clip_on=False, zorder=7)
    ax.text(1.95, -0.065, t["ch6"], ha="center", va="top", fontsize=11, color=TEXT, linespacing=1.2)

    ax.set_xlim(x[0], x[-1]); ax.set_ylim(0, top * 1.08)
    ax.set_xticks([-4, -2, 0, 2, 4, 6])
    ax.tick_params(axis="x", labelsize=11.5, pad=4)
    ax.set_xlabel(t["xlab"], fontsize=12, labelpad=48)
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"power_two_worlds{suffix}.png"))

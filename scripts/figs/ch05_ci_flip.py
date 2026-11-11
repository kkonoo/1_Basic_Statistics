# 5장 §2 1) σ를 안다면: x̄ ± 1.96σ/√n이 왜 95%로 μ를 잡는지
# 위: μ는 고정, x̄가 실험마다 흔들려 95%가 μ ± 1.96σ/√n 띠 안에 떨어짐
# 아래: 같은 x̄들로 만든 구간. 띠 안의 x̄ → 구간이 μ를 포함, 띠 밖의 x̄ → 놓침
# x̄ 위치는 설명용(숫자 없음). 숫자는 본문의 1.96, 95%뿐
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch05")

SE = r"$1.96\,\sigma/\sqrt{n}$"
LABELS = {
    "ko": dict(p1=r"① $\mu$는 고정, $\bar{x}$가 실험마다 흔들림",
               band=r"$\mu \pm 1.96\,\sigma/\sqrt{n}$ : $\bar{x}$의 95%가 이 안에 떨어짐",
               p2=r"② 각 $\bar{x}$로 만든 구간 $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$",
               hit=r"$\mu$ 포함", miss=r"$\mu$ 놓침",
               msg1=rf"$\bar{{x}}$가 $\mu$에서 {SE} 안  =  $\mu$가 $\bar{{x}}$에서 {SE} 안  (같은 사건)",
               msg2=r"그래서 실험을 반복하면 $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$ 구간의 95%가 $\mu$를 포함함"),
    "en": dict(p1=r"① $\mu$ is fixed, $\bar{x}$ varies by experiment",
               band=r"$\mu \pm 1.96\,\sigma/\sqrt{n}$ : 95% of $\bar{x}$ fall here",
               p2=r"② $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$ for each $\bar{x}$",
               hit=r"contains $\mu$", miss=r"misses $\mu$",
               msg1=rf"$\bar{{x}}$ within {SE} of $\mu$  =  $\mu$ within {SE} of $\bar{{x}}$  (same event)",
               msg2=r"So over repeated experiments, 95% of the intervals $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$ contain $\mu$"),
}

# x̄ offsets from μ in units of 1.96σ/√n (illustrative); |offset| > 1 = outside the band
OFF = [-0.15, 0.75, -0.9, 0.35, 1.3, -0.6]


def draw(t, path):
    fig, ax = new(8.0, 6.6)
    MU, HW, YT = 3.9, 1.25, 5.4          # μ position, half-width 1.96σ/√n (inches), top line y

    # ① μ fixed, x̄ scattered around it
    label(ax, 0.1, 6.4, t["p1"], fs=12.5, w="bold", ha="left")
    box(ax, MU - HW, YT - 0.26, 2 * HW, 0.52, fc=STEPS[2], ec="none", r=0.06, z=1)
    ax.plot([0.6, 7.0], [YT, YT], color=TEXT2, lw=1, zorder=2)
    ax.plot([MU, MU], [YT - 0.36, YT + 0.36], color=TEXT, lw=2.2, zorder=3, solid_capstyle="butt")
    label(ax, MU, YT - 0.56, r"$\mu$", fs=13, w="bold")
    label(ax, MU, YT + 0.56, t["band"], fs=12)

    # ② the interval from each x̄ (white backing so guide lines never show through the label)
    ys = [4.05 - 0.42 * k for k in range(len(OFF))]
    label(ax, 0.1, 4.55, t["p2"], fs=12.5, w="bold", ha="left",
          bbox=dict(fc="white", ec="none", pad=2))
    ax.plot([MU, MU], [ys[-1] - 0.3, ys[0] + 0.3], color=TEXT2, lw=1.2, ls=(0, (4, 3)), zorder=2)
    label(ax, MU, ys[-1] - 0.48, r"$\mu$", fs=12.5, w="bold")

    for off, y in zip(OFF, ys):
        xd = MU + off * HW
        miss = abs(off) > 1
        # same x̄ on the top line, joined to its interval by a faint guide
        ax.add_patch(mp.Circle((xd, YT), 0.085, fc=PRIMARY, ec="white", lw=0.8, zorder=4))
        ax.plot([xd, xd], [YT - 0.09, y + 0.09], color=LINE, lw=1, ls=(0, (1.5, 2)), zorder=1)
        col = ACCENT_INK if miss else STEPS[0]      # the one accent: the interval that misses μ
        ax.plot([xd - HW, xd + HW], [y, y], color=col, lw=3, zorder=3, solid_capstyle="butt")
        for xe in (xd - HW, xd + HW):
            ax.plot([xe, xe], [y - 0.1, y + 0.1], color=col, lw=1.6, zorder=3)
        ax.add_patch(mp.Circle((xd, y), 0.075, fc=ACCENT_INK if miss else PRIMARY,
                               ec="white", lw=0.8, zorder=4))
        if miss:
            label(ax, 7.05, y, t["miss"], fs=11, w="bold", c=TEXT, ha="left")
        else:
            label(ax, 7.05, y, t["hit"], fs=11, c=TEXT2, ha="left")

    # message
    box(ax, 0.1, 0.2, 7.8, 0.9, fc=STEPS[3], ec="none", r=0.1)
    label(ax, 0.3, 0.83, t["msg1"], fs=12.5, w="bold", ha="left")
    label(ax, 0.3, 0.47, t["msg2"], fs=12, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"ci_flip{suffix}.png"))

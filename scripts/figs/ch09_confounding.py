# 9장 §2 교란: 종양 순도가 유전자 A와 B를 함께 움직임. A–B 사이에는 화살표 없음
# 숫자는 본문과 같음: Pearson r = 0.56, 순도의 영향을 뺀 상관 −0.03 (p = 0.87), lm(B ~ A + 순도)의 A 계수 −0.03
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch09")

LABELS = {
    "ko": dict(p1="① 겉보기", p2="② 순도를 감안하면",
               purity="종양 순도", conf="교란변수", geneA="유전자 A", geneB="유전자 B",
               push="순도 높을수록\n둘 다 높게", r="r = 0.56", looks="관련 있어 보임",
               truth="A와 B 사이 조절 관계는 없음 (참값)",
               removed="순도의 영향을 뺀 A와 B", rres="r = −0.03 (p = 0.87)",
               verdict="관계 없음 → 참값과 맞음",
               lm="회귀에 순도를 함께 넣어도\nA의 계수 −0.03, p = 0.87"),
    "en": dict(p1="① What we see", p2="② Accounting for purity",
               purity="Tumour purity", conf="confounder", geneA="Gene A", geneB="Gene B",
               push="higher purity →\nboth read higher", r="r = 0.56", looks="looks related",
               truth="No regulation between A and B (truth)",
               removed="A and B with purity removed", rres="r = −0.03 (p = 0.87)",
               verdict="No relation = the truth",
               lm="With purity in the regression:\ncoefficient of A −0.03, p = 0.87"),
}
PUR, GA, GB = PRIMARY, CAT[1], CAT[2]


def draw(t, path):
    fig, ax = new(8.0, 4.4)

    def gene(x, y, w, h, text, fc):
        box(ax, x, y, w, h, fc=fc, ec="none")
        label(ax, x + w / 2, y + h / 2, text, fs=12.5, w="bold", c=on(fc))

    # ① 겉보기: 순도 → A, 순도 → B, A–B는 점선(화살표 없음)
    label(ax, 0.1, 4.2, t["p1"], fs=12.5, w="bold", ha="left")
    box(ax, 1.35, 3.0, 2.0, 0.8, fc=PUR, ec="none")
    label(ax, 2.35, 3.52, t["purity"], fs=13, w="bold", c=on(PUR))
    label(ax, 2.35, 3.2, t["conf"], fs=11, c=on(PUR))

    gw, gh, gy = 1.4, 0.6, 1.0
    gene(0.2, gy, gw, gh, t["geneA"], GA)
    gene(3.1, gy, gw, gh, t["geneB"], GB)
    arrow(ax, 1.9, 3.0, 0.9, gy + gh, color=TEXT2, lw=1.6, ms=13)
    arrow(ax, 2.8, 3.0, 3.8, gy + gh, color=TEXT2, lw=1.6, ms=13)
    label(ax, 2.35, 2.3, t["push"], fs=11, c=TEXT2, linespacing=1.3)

    yd = gy + gh / 2
    ax.plot([1.68, 3.02], [yd, yd], color=TEXT2, lw=1.5, ls=(0, (4, 3)), zorder=3)
    label(ax, 2.35, yd + 0.22, t["r"], fs=12.5, w="bold")
    label(ax, 2.35, yd - 0.22, t["looks"], fs=11, c=TEXT2)
    label(ax, 2.35, 0.5, t["truth"], fs=11, c=TEXT2)

    # divider
    ax.plot([4.85, 4.85], [0.3, 4.2], color=LINE, lw=1.2)

    # ② 순도를 감안하면: 상관이 사라짐 (강조색은 여기 한 곳)
    cx = 6.5
    label(ax, 5.1, 4.2, t["p2"], fs=12.5, w="bold", ha="left")
    label(ax, cx, 3.55, t["removed"], fs=11, c=TEXT2)
    gene(5.25, 2.65, 1.0, 0.5, t["geneA"], GA)
    gene(6.75, 2.65, 1.0, 0.5, t["geneB"], GB)
    label(ax, cx, 2.2, t["rres"], fs=12.5, w="bold")
    box(ax, 5.25, 1.2, 2.5, 0.55, fc=ACCENT, ec="none", r=0.1)
    label(ax, cx, 1.475, t["verdict"], fs=12, w="bold", c=ON_ACCENT)
    label(ax, cx, 0.55, t["lm"], fs=11, c=TEXT2, linespacing=1.35)
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"confounding{suffix}.png"))

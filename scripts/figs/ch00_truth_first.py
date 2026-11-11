# 0장 §5 이 책을 읽는 법: 실제 실험(참값을 모름)과 이 책의 방식(참값을 먼저 정하고 채점)을 나란히 비교
# 숫자는 본문과 같음: 참값 예시 평균 100, 차이 1.0
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch00")

LABELS = {
    "ko": dict(real="실제 실험", book="이 책",
               truth_q="참값 = ?", never="영원히 모름",
               data="자료", method="통계 방법", answer="답",
               nocheck="맞는 답인지 확인할 길이 없음",
               s1="① 참값을 먼저 정함", s1b="평균 100, 차이 1.0",
               s2="② 시뮬레이션", s2b="참값에서 자료를 만듦",
               s3="③ 통계 방법 적용", s3b="답을 냄",
               s4="④ 채점", s4b="결과를 참값과 비교",
               known="참값을 알고 있으니 비교할 수 있음",
               seed="set.seed()로 난수를 고정 → 같은 코드를 실행하면 같은 결과"),
    "en": dict(real="Real experiment", book="This book",
               truth_q="Truth = ?", never="never known",
               data="Data", method="Statistical method", answer="Answer",
               nocheck="no way to check whether it is right",
               s1="① Set the truth", s1b="mean 100, diff 1.0",
               s2="② Simulate", s2b="data from the truth",
               s3="③ Apply method", s3b="get an answer",
               s4="④ Score", s4b="compare with the truth",
               known="truth is known → we can compare",
               seed="set.seed() fixes the random numbers → same code, same result"),
}


def draw(t, path):
    fig, ax = new(8.3, 4.9)
    bw, gap = 1.8, 0.3
    xs = [0.1 + k * (bw + gap) for k in range(4)]          # four aligned columns
    cx = [x + bw / 2 for x in xs]

    # ── 실제 실험 ───────────────────────────────────────────────
    y1, h1 = 3.9, 0.7
    label(ax, 0.1, 4.6, t["real"], fs=12.5, w="bold", ha="left")
    # truth: unknown (dashed, grey) in the same column as ①
    box(ax, xs[0], y1 - h1 / 2, bw, h1, fc="white", ec=TEXT2, lw=1.2, ls="--")
    label(ax, cx[0], y1 + 0.14, t["truth_q"], fs=12, w="bold", c=TEXT2)
    label(ax, cx[0], y1 - 0.17, t["never"], fs=11, c=TEXT2)
    for k, txt in zip([1, 2, 3], [t["data"], t["method"], t["answer"]]):
        box(ax, xs[k], y1 - h1 / 2, bw, h1, fc=FAINT, ec=LINE, lw=1.2)
        label(ax, cx[k], y1, txt, fs=12, w="bold")
    for k in [1, 2]:
        arrow(ax, xs[k] + bw + 0.03, y1, xs[k + 1] - 0.03, y1, lw=1.4, ms=11)
    # answer ↔ truth: cannot be compared (dashed, no arrowhead)
    ax.add_patch(mp.FancyArrowPatch((cx[3], y1 - h1 / 2 - 0.03), (cx[0], y1 - h1 / 2 - 0.03),
                                    arrowstyle="-", color=TEXT2, lw=1.2, ls=(0, (4, 3)),
                                    connectionstyle="arc3,rad=-0.15", shrinkA=0, shrinkB=0, zorder=3))
    label(ax, (cx[0] + cx[3]) / 2, 2.88, t["nocheck"], fs=11.5, c=TEXT2)

    # ── 이 책 ───────────────────────────────────────────────────
    y2, h2 = 1.85, 0.9
    label(ax, 0.1, 2.5, t["book"], fs=12.5, w="bold", ha="left")
    cols = ramp(4)
    steps = [(t["s1"], t["s1b"]), (t["s2"], t["s2b"]), (t["s3"], t["s3b"]), (t["s4"], t["s4b"])]
    for k, ((head, sub), fc) in enumerate(zip(steps, cols)):
        box(ax, xs[k], y2 - h2 / 2, bw, h2, fc=fc, ec="none")
        label(ax, cx[k], y2 + 0.17, head, fs=12, w="bold", c=on(fc))
        label(ax, cx[k], y2 - 0.19, sub, fs=11, c=on(fc))
    for k in range(3):
        arrow(ax, xs[k] + bw + 0.03, y2, xs[k + 1] - 0.03, y2, lw=1.4, ms=11)
    # truth → scoring: the comparison is possible
    arrow(ax, cx[0], y2 - h2 / 2 - 0.03, cx[3], y2 - h2 / 2 - 0.03, color=TEXT2, lw=1.3, ms=11,
          rad=0.15)
    label(ax, (cx[0] + cx[3]) / 2, 0.75, t["known"], fs=11.5, c=TEXT)

    label(ax, 0.1, 0.3, t["seed"], fs=11, c=TEXT2, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"truth_first{suffix}.png"))

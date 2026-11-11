# 4장 §5 2) 정확도와 정밀도: bias(작음/큼) × SE(큼/작음) 과녁 2 × 2
# 점 위치는 설명용(숫자 없음). 메시지는 본문 표와 같음: SE는 표본 크기로, bias는 설계로 줄임
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch04")

LABELS = {
    "ko": dict(se_big="SE 큼", se_small="SE 작음", bias_small="bias 작음", bias_big="bias 큼",
               p_tl="정확하지만 흔들림", p_tr="정확하고 정밀함", p_bl="치우치고 흔들림",
               p_br="정밀하게 틀린 답", more_n="n을 늘리면", stays="bias는 그대로", design="설계",
               leg_mu="과녁 가운데 = 참값 μ", leg_dot="점 하나 = 실험 한 번의 추정값",
               msg1="n을 늘리면 SE는 줄지만 bias는 줄지 않음",
               msg2="bias는 설계로 줄임: 무작위 추출, 무작위 배정, 눈가림, 같은 batch"),
    "en": dict(se_big="large SE", se_small="small SE", bias_small="small bias", bias_big="large bias",
               p_tl="accurate, not precise", p_tr="accurate and precise", p_bl="biased and imprecise",
               p_br="precisely wrong", more_n="larger n", stays="bias stays", design="design",
               leg_mu="target centre = true value μ", leg_dot="one dot = estimate from one experiment",
               msg1="Larger n shrinks SE but not bias",
               msg2="Bias is cut by design: random sampling, random assignment, blinding, same batch"),
}

# one shared cloud shape (illustrative), centred, so panels differ only in spread and offset
Z = np.clip(np.random.default_rng(7).standard_normal((12, 2)), -1.8, 1.8)
Z = Z - Z.mean(axis=0)
SD_BIG, SD_SMALL = 0.2, 0.055
OFF = (0.3, 0.2)                       # bias: the cloud's centre sits away from μ
RINGS = [0.62, 0.44, 0.26, 0.09]
DOT = PRIMARY


def centre_mark(ax, x, y, s=0.06):
    ax.plot([x - s, x + s], [y, y], color=TEXT2, lw=1.4, zorder=4)
    ax.plot([x, x], [y - s, y + s], color=TEXT2, lw=1.4, zorder=4)


def target(ax, cx, cy, sd, biased):
    for k, r in enumerate(RINGS):
        ax.add_patch(mp.Circle((cx, cy), r, fc=FAINT if k % 2 == 0 else "white",
                               ec=LINE, lw=1.2, zorder=2 + k * 0.01))
    centre_mark(ax, cx, cy)
    ox, oy = OFF if biased else (0, 0)
    for zx, zy in Z:
        ax.add_patch(mp.Circle((cx + ox + sd * zx, cy + oy + sd * zy), 0.045,
                               fc=DOT, ec="white", lw=0.7, zorder=6))


def draw(t, path):
    fig, ax = new(8.0, 6.6)
    cxL, cxR = 2.5, 5.5
    cyT, cyB = 5.35, 3.35
    R = RINGS[0]

    # column and row headings
    label(ax, cxL, 6.3, t["se_big"], fs=12.5, w="bold")
    label(ax, cxR, 6.3, t["se_small"], fs=12.5, w="bold")
    label(ax, 0.1, cyT, t["bias_small"], fs=12.5, w="bold", ha="left")
    label(ax, 0.1, cyB, t["bias_big"], fs=12.5, w="bold", ha="left")

    # four targets
    target(ax, cxL, cyT, SD_BIG, False)
    target(ax, cxR, cyT, SD_SMALL, False)
    target(ax, cxL, cyB, SD_BIG, True)
    target(ax, cxR, cyB, SD_SMALL, True)

    # panel names (the one accent: precise but wrong, the chapter's warning)
    ly = R + 0.28
    label(ax, cxL, cyT - ly, t["p_tl"], fs=12, w="bold")
    label(ax, cxR, cyT - ly, t["p_tr"], fs=12, w="bold")
    label(ax, cxL, cyB - ly, t["p_bl"], fs=12, w="bold")
    pill(ax, cxR, cyB - ly, t["p_br"], fc=ACCENT, tc=ON_ACCENT, fs=12, h=0.34)

    # larger n: left → right in both rows (SE shrinks, bias does not move)
    xa, xb = cxL + R + 0.18, cxR - R - 0.18
    for cy in (cyT, cyB):
        arrow(ax, xa, cy, xb, cy, color=TEXT2, lw=1.5, ms=12)
        label(ax, (xa + xb) / 2, cy + 0.22, t["more_n"], fs=11.5, w="bold", c=TEXT)
    label(ax, (xa + xb) / 2, cyB - 0.22, t["stays"], fs=11.5, c=TEXT2)

    # design: bottom → top on the right
    xv = cxR + R + 0.45
    arrow(ax, xv, cyB + 0.1, xv, cyT - 0.1, color=TEXT2, lw=1.5, ms=12)
    label(ax, xv + 0.14, (cyT + cyB) / 2, t["design"], fs=11.5, w="bold", c=TEXT, ha="left")

    # legend
    yl = 1.85
    centre_mark(ax, 0.25, yl)
    label(ax, 0.42, yl, t["leg_mu"], fs=11, c=TEXT2, ha="left")
    ax.add_patch(mp.Circle((4.05, yl), 0.045, fc=DOT, ec="white", lw=0.7, zorder=6))
    label(ax, 4.2, yl, t["leg_dot"], fs=11, c=TEXT2, ha="left")

    # key message
    yb = 0.95
    box(ax, 0.1, yb - 0.4, 7.8, 0.8, fc=STEPS[3], ec="none", r=0.1)
    label(ax, 0.3, yb + 0.16, t["msg1"], fs=12, w="bold", ha="left")
    label(ax, 0.3, yb - 0.17, t["msg2"], fs=11.5, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"accuracy_precision{suffix}.png"))

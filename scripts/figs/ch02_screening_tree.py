# 2장 §3.2 드문 질병의 선별검사: 신생아 10만 명을 환자/건강 → 양성/음성으로 나눔 (본문 표를 그림으로)
# 숫자는 본문 표와 같음: 유병률 1/5000, 민감도·특이도 99%
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch02")

LABELS = {
    "ko": dict(root="신생아\n10만 명", sick="환자", healthy="건강", pos="양성", neg="음성",
               prev="유병률 1/5000", sens="민감도 99%", fp="1%가 양성", spec="특이도 99%",
               pool="양성 1,019.6명", true_pos="진짜 환자 19.8", false_pos="가짜 양성 999.8",
               result="양성 중 진짜 환자", ratio="19.8 / 1,019.6 =", pct="1.94%"),
    "en": dict(root="100,000\nnewborns", sick="Affected", healthy="Healthy", pos="Positive", neg="Negative",
               prev="prevalence 1/5000", sens="sensitivity 99%", fp="1% test positive", spec="specificity 99%",
               pool="1,019.6 positives", true_pos="true cases 19.8", false_pos="false positives 999.8",
               result="Affected among positives", ratio="19.8 / 1,019.6 =", pct="1.94%"),
}
SICK, WELL = CAT[0], CAT[1]


def draw(t, path):
    fig, ax = new(8.0, 5.3)
    bw, bh = 1.72, 0.62

    def node(x, yc, text, fc, ec="none"):
        box(ax, x, yc - bh / 2, bw, bh, fc=fc, ec=ec, lw=1.2)
        label(ax, x + bw / 2, yc, text, fs=12.5, w="bold", c=on(fc), linespacing=1.25)

    def edge(x1, y1, x2, y2, text, above=True, side=False):
        arrow(ax, x1, y1, x2, y2, color="#9AA1AB", lw=1.4, ms=11)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if side:   # steep edge: put the label to the left of the line
            label(ax, mx - 0.12, my + 0.12, text, fs=11, c=TEXT2, ha="right")
        else:
            label(ax, mx, my + (0.2 if above else -0.2), text, fs=11, c=TEXT2)

    # ① 10만 명 → 환자 / 건강 → 양성 / 음성
    x0, x1, x2 = 0.1, 2.75, 5.4
    y_root, y_s, y_h = 3.35, 4.3, 2.4
    node(x0, y_root, t["root"], FAINT, ec=LINE)
    node(x1, y_s, f"{t['sick']} 20", SICK)
    node(x1, y_h, f"{t['healthy']} 99,980", WELL)
    edge(x0 + bw, y_root + 0.12, x1, y_s, t["prev"], side=True)
    edge(x0 + bw, y_root - 0.12, x1, y_h, "", above=False)

    leaves = [  # y, text, fill, edge label
        (4.75, f"{t['pos']} 19.8", SICK, t["sens"]),
        (3.85, f"{t['neg']} 0.2", mix(SICK, 0.12), ""),
        (2.85, f"{t['pos']} 999.8", WELL, t["fp"]),
        (1.95, f"{t['neg']} 98,980.2", mix(WELL, 0.12), t["spec"]),
    ]
    for k, (y, text, fc, el) in enumerate(leaves):
        ys = y_s if k < 2 else y_h
        node(x2, y, text, fc)
        arrow(ax, x1 + bw, ys + (0.1 if y > ys else -0.1), x2, y, color="#9AA1AB", lw=1.4, ms=11)
        if el:   # label ends just left of the leaf box so long (English) labels never run into it
            label(ax, x2 - 0.12, y + (0.24 if y > ys else -0.24), el, fs=11, c=TEXT2, ha="right")

    # ② 양성끼리 모으면: 막대 길이 = 사람 수
    bx, by, bwid, bhh = 0.1, 0.55, 5.2, 0.5
    label(ax, bx, by + bhh + 0.32, t["pool"], fs=12.5, w="bold", ha="left")
    tot = 19.8 + 999.8
    w_true = bwid * 19.8 / tot
    box(ax, bx, by, w_true, bhh, fc=SICK, ec="none", r=0.0)
    box(ax, bx + w_true, by, bwid - w_true, bhh, fc=WELL, ec="none", r=0.0)
    label(ax, bx + w_true + 0.12, by + bhh / 2, t["false_pos"], fs=12, w="bold", c="white", ha="left")
    ax.plot([bx + w_true / 2, bx + w_true / 2], [by - 0.04, by - 0.22], color=SICK, lw=1.3)
    label(ax, bx, by - 0.38, t["true_pos"], fs=11.5, w="bold", c=SICK, ha="left")

    # ③ 결론 (강조색은 여기 한 곳)
    rx = bx + bwid + 0.45
    label(ax, rx, by + bhh + 0.32, t["result"], fs=12.5, w="bold", ha="left")
    label(ax, rx, by + bhh / 2, t["ratio"], fs=12, c=TEXT, ha="left")
    label(ax, rx, by - 0.36, t["pct"], fs=18, w="bold", c=ACCENT_INK, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"screening_tree{suffix}.png"))

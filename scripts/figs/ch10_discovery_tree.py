# 10장 §1 유전자 2만 개를 p < 0.05로 검정: 진짜 DE / 변화 없음 → 발견 / 발견 아님 (본문 표를 그림으로)
# 숫자는 본문 표와 같음: 20,000 = 2,000 (10%) + 18,000 (90%), 발견 2,615 = 1,685 + 930, 가짜 비율 0.356 (36%)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch10")

LABELS = {
    "ko": dict(root="유전자\n20,000개", de="진짜 DE", null="변화 없음",
               de_share="10%", null_share="90%", fp="약 5%",
               pool="p < 0.05 발견 2,615개", true_d="진짜 1,685", false_d="가짜 930",
               result="발견 중 가짜 비율", ratio="930 / 2,615 = 0.356", pct="36%가 가짜"),
    "en": dict(root="20,000\ngenes", de="True DE", null="Unchanged",
               de_share="10%", null_share="90%", fp="about 5%",
               pool="2,615 discoveries at p < 0.05", true_d="true 1,685", false_d="false 930",
               result="Share that is false", ratio="930 / 2,615 = 0.356", pct="36% false"),
}
DE_C, NULL_C = CAT[0], CAT[1]


def draw(t, path):
    fig, ax = new(8.0, 5.3)
    bw, bh = 1.95, 0.62

    def node(x, yc, text, fc, ec="none"):
        box(ax, x, yc - bh / 2, bw, bh, fc=fc, ec=ec, lw=1.2)
        label(ax, x + bw / 2, yc, text, fs=12.5, w="bold", c=on(fc), linespacing=1.25)

    def edge(x1, y1, x2, y2, text, up=True):
        arrow(ax, x1, y1, x2, y2, lw=1.4, ms=11)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # label sits left of the line, on the side away from it
        label(ax, mx - 0.12, my + (0.12 if up else -0.12), text, fs=11, c=TEXT2, ha="right")

    # ① 20,000개 → 진짜 DE / 변화 없음 → p < 0.05 / p ≥ 0.05
    x0, x1, x2 = 0.1, 2.75, 5.5
    y_root, y_d, y_n = 3.35, 4.3, 2.4
    node(x0, y_root, t["root"], FAINT, ec=LINE)
    node(x1, y_d, f"{t['de']} 2,000", DE_C)
    node(x1, y_n, f"{t['null']} 18,000", NULL_C)
    edge(x0 + bw, y_root + 0.12, x1, y_d, t["de_share"], up=True)
    edge(x0 + bw, y_root - 0.12, x1, y_n, t["null_share"], up=False)

    leaves = [  # y, text, fill, edge label
        (4.75, "p < 0.05  1,685", DE_C, ""),
        (3.85, "p ≥ 0.05  315", mix(DE_C, 0.12), ""),
        (2.85, "p < 0.05  930", NULL_C, t["fp"]),
        (1.95, "p ≥ 0.05  17,070", mix(NULL_C, 0.12), ""),
    ]
    for k, (y, text, fc, el) in enumerate(leaves):
        ys = y_d if k < 2 else y_n
        node(x2, y, text, fc)
        arrow(ax, x1 + bw, ys + (0.1 if y > ys else -0.1), x2, y, lw=1.4, ms=11)
        if el:   # ends just left of the leaf box so the English label never runs into it
            label(ax, x2 - 0.12, y + (0.24 if y > ys else -0.24), el, fs=11, c=TEXT2, ha="right")

    # ② 발견끼리 모으면: 막대 길이 = 유전자 수
    bx, by, bwid, bhh = 0.1, 0.55, 5.0, 0.5
    label(ax, bx, by + bhh + 0.32, t["pool"], fs=12.5, w="bold", ha="left")
    w_true = bwid * 1685 / 2615
    box(ax, bx, by, w_true, bhh, fc=DE_C, ec="none", r=0.0)
    box(ax, bx + w_true, by, bwid - w_true, bhh, fc=NULL_C, ec="none", r=0.0)
    label(ax, bx + 0.12, by + bhh / 2, t["true_d"], fs=12, w="bold", c=on(DE_C), ha="left")
    label(ax, bx + w_true + 0.12, by + bhh / 2, t["false_d"], fs=12, w="bold", c=on(NULL_C), ha="left")

    # ③ 결론 (강조색은 여기 한 곳) — leaf column에 맞춰 정렬
    rx = x2
    label(ax, rx, by + bhh + 0.32, t["result"], fs=12.5, w="bold", ha="left")
    label(ax, rx, by + bhh / 2, t["ratio"], fs=12, c=TEXT, ha="left")
    label(ax, rx, by - 0.36, t["pct"], fs=18, w="bold", c=ACCENT_INK, ha="left")
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"discovery_tree{suffix}.png"))

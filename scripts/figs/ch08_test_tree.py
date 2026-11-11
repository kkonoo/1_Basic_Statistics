# 8장 §1 검정 고르기 지도: 네 가지 질문(결과 변수 → 그룹 수 → 짝 → 분포 가정)을 차례로 따라가는 나무
# 잎은 본문 지도 표의 칸과 하나씩 대응함 (표는 본문에 그대로 둠). 숫자 없음, 실습·장 번호만 표와 같음
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch08")

LABELS = {
    "ko": dict(
        marks=["① 결과 변수", "② 그룹 수", "③ 짝", "④ 분포 가정"],
        cont="연속형", count="count\n(RNA-seq)", cat="범주형", rel="연속형 vs\n연속형",
        g2="2그룹", g3="3그룹 이상", grp="그룹", gxc="그룹 × 범주", relation="관계",
        unp="짝 없음", pair="짝 있음", norm="정규에 가까움", skew="치우침·이상치",
        welch=("두 표본 t-검정 (Welch)", "실습 1"),
        wrs=("Wilcoxon 순위합", "Mann-Whitney · 실습 1"),
        pt=("paired t-검정", "실습 5"),
        wsr=("Wilcoxon 부호순위", "실습 5"),
        anova=("일원 분산분석 (ANOVA)", "실습 2"),
        kw=("Kruskal-Wallis", "실습 2"),
        rm=("반복측정 ANOVA·혼합모형", ""),
        fried=("Friedman", ""),
        nb=("음이항 모형", "DESeq2, edgeR · 6절"),
        cpair=("짝을 모형에 넣음", "~ patient + condition"),
        chi=("카이제곱 / Fisher exact", "칸이 작으면 Fisher · 실습 3, 4"),
        mcn=("McNemar", "실습 6"),
        corr=("상관·회귀", "9장"),
    ),
    "en": dict(
        marks=["① Outcome", "② Groups", "③ Paired?", "④ Distribution"],
        cont="Continuous", count="Count\n(RNA-seq)", cat="Categorical", rel="Continuous vs\ncontinuous",
        g2="2 groups", g3="3+ groups", grp="groups", gxc="group ×\ncategory", relation="relation",
        unp="unpaired", pair="paired", norm="near normal", skew="skewed, outliers",
        welch=("Two-sample t-test (Welch)", "Lab 1"),
        wrs=("Wilcoxon rank-sum", "Mann-Whitney · Lab 1"),
        pt=("Paired t-test", "Lab 5"),
        wsr=("Wilcoxon signed-rank", "Lab 5"),
        anova=("One-way ANOVA", "Lab 2"),
        kw=("Kruskal-Wallis", "Lab 2"),
        rm=("Repeated-measures ANOVA", "or mixed model"),
        fried=("Friedman", ""),
        nb=("Negative binomial model", "DESeq2, edgeR · §6"),
        cpair=("Pair term in the model", "~ patient + condition"),
        chi=("Chi-square / Fisher exact", "Fisher if small · Labs 3, 4"),
        mcn=("McNemar", "Lab 6"),
        corr=("Correlation, regression", "Ch. 9"),
    ),
}

# (node key, children); a str child is a leaf (test) key. Order = chapter's question 1 (연속형 / count / 범주형)
TREE = [
    ("cont", [
        ("g2", [("unp", [("norm", "welch"), ("skew", "wrs")]),
                ("pair", [("norm", "pt"), ("skew", "wsr")])]),
        ("g3", [("unp", [("norm", "anova"), ("skew", "kw")]),
                ("pair", [("norm", "rm"), ("skew", "fried")])]),
    ]),
    ("count", [("grp", [("unp", "nb"), ("pair", "cpair")])]),
    ("cat", [("gxc", [("unp", "chi"), ("pair", "mcn")])]),
    ("rel", [("relation", "corr")]),
]
BRANCH_C = CAT[:4]            # outcome types are parallel items → CAT, no accent in this figure

COLS = [(0.0, 1.4), (1.6, 0.95), (2.75, 0.8), (3.75, 1.4), (5.35, 2.8)]   # x, width per column
PITCH, LEAF_H = 0.58, 0.5
W, H = 8.15, 8.9


def draw(t, path):
    fig, ax = new(W, H)
    for k, mark in enumerate(t["marks"]):          # short marks for the four questions
        x, w = COLS[k]
        label(ax, x + w / 2, H - 0.22, mark, fs=12, w="bold", c=TEXT2)
    cur = [H - 0.78]                               # y of the next leaf row

    def leaf(key, y, c):
        x, w = COLS[4]
        name, sub = t[key]
        box(ax, x, y - LEAF_H / 2, w, LEAF_H, fc=mix(c, 0.3), ec="none")
        if sub:
            label(ax, x + 0.12, y + 0.105, name, fs=11.5, w="bold", ha="left")
            label(ax, x + 0.12, y - 0.115, sub, fs=11, c=TEXT2, ha="left")
        else:
            label(ax, x + 0.12, y, name, fs=11.5, w="bold", ha="left")

    def node(depth, key, y, c):
        x, w = COLS[depth]
        text = t[key]
        n = text.count("\n") + 1
        if depth == 0:
            h, fc, fs, wt = 0.44 + 0.2 * (n - 1), c, 12, "bold"
        else:
            h, fc, fs, wt = 0.38 + 0.19 * (n - 1), mix(c, 0.14), 11.5, "regular"
        box(ax, x, y - h / 2, w, h, fc=fc, ec="none")
        label(ax, x + w / 2, y, text, fs=fs, w=wt, c=on(fc), linespacing=1.15)

    def link(d0, y0, d1, y1, c):
        x0 = COLS[d0][0] + COLS[d0][1]
        x1 = COLS[d1][0]
        xm = x0 + (COLS[d0 + 1][0] - x0) / 2
        ax.plot([x0, xm, xm, x1], [y0, y0, y1, y1], color=mix(c, 0.55), lw=1.3, zorder=1,
                solid_joinstyle="round", solid_capstyle="round")

    def place(nd, depth, c):
        key, kids = nd
        if isinstance(kids, str):                  # answer goes straight to its test
            y = cur[0]
            cur[0] -= PITCH
            leaf(kids, y, c)
            link(depth, y, 4, y, c)
        else:
            ys = []
            for i, k in enumerate(kids):
                if depth == 0 and i > 0:
                    cur[0] -= 0.1                  # small gap between 2그룹 and 3그룹 이상
                ys.append(place(k, depth + 1, c))
            y = sum(ys) / len(ys)
            for yc in ys:
                link(depth, y, depth + 1, yc, c)
        node(depth, key, y, c)
        return y

    for i, (nd, c) in enumerate(zip(TREE, BRANCH_C)):
        if i > 0:
            cur[0] -= 0.22                         # gap between outcome types
        place(nd, 0, c)
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"test_tree{suffix}.png"))

# 3장 도입부·§6 분포 고르기: 이항 → 포아송 → 음이항, 평균이 크면 정규로 가까워지는 관계도
# 칸의 내용(무엇을 세는지, 평균·분산, 오믹스 예)은 §6 표와 같음. λ = 3 / 100은 §4 1)의 그림과 같음
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "ch03")

LABELS = {
    "ko": dict(
        names=["이항분포", "포아송분포", "음이항분포", "정규분포"],
        nota=["Binomial(n, p)", "Poisson(λ)", "NB(μ, φ)", "N(μ, σ²)"],
        what=["n번 중 성공 수", "드문 사건의 개수", "개체마다 평균이 다른 count", "연속, 대칭"],
        mv=["평균 np · 분산 np(1 − p)", "평균 = 분산 = λ", "평균 μ · 분산 μ + φμ²", "평균 μ · 분산 σ²"],
        ex=["유전형, 대립유전자 특이 read,\n세포 유형 수", "기술적 반복 read count",
            "생물학적 반복 RNA-seq, UMI\n→ DESeq2·edgeR", "체중, log 발현량"],
        a1="n 아주 큼, p 아주 작음\nλ = np",
        a2="마우스마다 참 수준 λ가 다름 (감마분포)\n분산 ≫ 평균: 과산포",
        a3="평균이\n크면",
        fit="포아송 λ = 3: 안 맞음\nλ = 100: 잘 맞음"),
    "en": dict(
        names=["Binomial", "Poisson", "Negative\nbinomial", "Normal"],
        nota=["Binomial(n, p)", "Poisson(λ)", "NB(μ, φ)", "N(μ, σ²)"],
        what=["successes in n trials", "count of rare events", "counts, mean varies by animal",
              "continuous, symmetric"],
        mv=["mean np · variance np(1 − p)", "mean = variance = λ", "mean μ · variance μ + φμ²",
            "mean μ · variance σ²"],
        ex=["genotype, allele-specific reads,\ncell-type counts", "technical-replicate read counts",
            "biological-replicate RNA-seq, UMI\n→ DESeq2 · edgeR", "body weight, log expression"],
        a1="n very large, p very small\nλ = np",
        a2="true level λ differs by mouse (gamma)\nvariance ≫ mean: overdispersion",
        a3="large\nmean",
        fit="Poisson λ = 3: poor fit\nλ = 100: good fit"),
}
COLS = [CAT[0], CAT[1], CAT[2], CAT[3]]   # four parallel distributions, no accent


def draw(t, path):
    fig, ax = new(7.9, 5.85)
    X0, BW, TW, BH, GAP = 0.05, 4.35, 1.45, 1.35, 0.85
    ys = [5.8 - BH, 5.8 - 2 * BH - GAP, 5.8 - 3 * BH - 2 * GAP]   # bottoms: binomial, Poisson, NB

    def text_stack(x, yc, k):
        """what / mean-variance / example lines, vertically centred on yc."""
        ex = t["ex"][k].split("\n")
        step = 0.255
        n = 2 + len(ex)
        y = yc + step * (n - 1) / 2
        label(ax, x, y, t["what"][k], fs=11.5, w="bold", ha="left")
        label(ax, x, y - step, t["mv"][k], fs=11.5, ha="left")
        for j, line in enumerate(ex):
            label(ax, x, y - step * (2 + j), line, fs=11, c=TEXT2, ha="left")

    # ① left column: binomial → Poisson → negative binomial
    for k in range(3):
        c, y0 = COLS[k], ys[k]
        yc = y0 + BH / 2
        box(ax, X0, y0, BW, BH, fc=mix(c, 0.12), ec="none")
        box(ax, X0, y0, TW, BH, fc=c, ec="none")
        box(ax, X0 + TW - 0.1, y0, 0.1, BH, fc=c, ec="none", r=0.0)   # square off the tab's right side
        name = t["names"][k]
        two = "\n" in name
        label(ax, X0 + TW / 2, yc + (0.2 if two else 0.14), name, fs=13, w="bold", c=on(c),
              linespacing=1.1)
        label(ax, X0 + TW / 2, yc - (0.34 if two else 0.2), t["nota"][k], fs=11.5, c=on(c))
        text_stack(X0 + TW + 0.18, yc, k)

    ax_x = X0 + TW / 2
    for k, key in [(0, "a1"), (1, "a2")]:
        top, bot = ys[k], ys[k + 1] + BH
        arrow(ax, ax_x, top - 0.04, ax_x, bot + 0.04, lw=1.6, ms=12)
        label(ax, ax_x + 0.25, (top + bot) / 2, t[key], fs=11.5, ha="left", linespacing=1.35)

    # ② normal box on the right, between Poisson and NB
    c = COLS[3]
    NX, NW, HH, BOD = X0 + BW + 0.95, 2.5, 0.45, 1.0
    yc_n = (ys[1] + ys[2] + BH) / 2
    n_bot = yc_n - (HH + BOD) / 2
    box(ax, NX, n_bot, NW, HH + BOD, fc=mix(c, 0.18), ec="none")
    box(ax, NX, n_bot + BOD, NW, HH, fc=c, ec="none")
    box(ax, NX, n_bot + BOD, NW, 0.1, fc=c, ec="none", r=0.0)        # square off the strip's bottom
    label(ax, NX + NW / 2, n_bot + BOD + HH / 2, f"{t['names'][3]}  {t['nota'][3]}",
          fs=12.5, w="bold", c=on(c))
    text_stack(NX + 0.15, n_bot + BOD / 2, 3)
    label(ax, NX, n_bot - 0.14, t["fit"], fs=11, c=TEXT2, ha="left", va="top", linespacing=1.35)

    # arrows from Poisson and NB: large mean → normal approximation
    xr = X0 + BW
    arrow(ax, xr + 0.04, ys[1] + BH / 2, NX - 0.04, yc_n + 0.36, lw=1.6, ms=12)
    arrow(ax, xr + 0.04, ys[2] + BH / 2, NX - 0.04, yc_n - 0.36, lw=1.6, ms=12)
    label(ax, (xr + NX) / 2, yc_n, t["a3"], fs=11, c=TEXT, linespacing=1.2)
    save(fig, path)


if __name__ == "__main__":
    for lang, suffix in [("ko", ""), ("en", "_en")]:
        draw(LABELS[lang], os.path.join(OUT, f"distribution_map{suffix}.png"))

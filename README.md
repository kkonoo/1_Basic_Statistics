# 1. Basic Statistics

https://kkonoo.github.io/1_Basic_Statistics/

오믹스 데이터를 처음 다루는 대학원생을 위한 기초통계 Quarto 사이트입니다. 확률변수와 분포에서 시작해 p-value, 신뢰구간, 다중검정까지 시뮬레이션으로 다룹니다. 구성과 배포 방식은 [3_linear_regression](https://github.com/kkonoo/3_linear_regression)과 같습니다.

## 파일 구조

```
.
├── _quarto.yml                  # 사이트 설정, 사이드바 목차
├── index.qmd                    # 홈 (강의 안내, 장 목록)
├── chapters/                    # 장별 .qmd (00–11)
├── assets/                      # CSS, AI 위젯 초기화
├── _extensions/ai-chat/         # AI 학습 도우미 위젯
└── .github/workflows/deploy.yml # main에 push하면 GitHub Pages로 배포
```

## 작성 원칙

- 외부 자료(PH125.4x, dsbook, Data Analysis for the Life Sciences)는 구조만 참고하고 문장·코드는 새로 씁니다. dsbook 사본은 CC BY-NC-ND라 번역·개작이 안 됩니다.
- 실습 자료는 장 안에서 `set.seed()`로 만듭니다. 참값을 알고 시작합니다.
- 코드는 base R만 씁니다.
- 각 장 YAML의 `ai-context`에 그 장의 핵심 내용과 실습 결과 수치를 적습니다.

## 로컬 미리보기

```bash
quarto preview
```

## 처음 배포할 때

GitHub 저장소 → Settings → Pages → Source를 **GitHub Actions**로 바꿉니다.

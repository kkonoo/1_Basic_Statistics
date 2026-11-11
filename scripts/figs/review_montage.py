"""Stack PNGs at the width the page will show them (default 607 px = body column on a 1280 px
laptop), so you can judge readability the way a reader sees it.
Usage: python3 review_montage.py a.png b.png ... -w 607 -o review.png"""
import argparse
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument("pngs", nargs="+"); ap.add_argument("-w", type=int, default=607)
ap.add_argument("-o", default="review.png"); ap.add_argument("--cols", type=int, default=2)
a = ap.parse_args()
ims = [Image.open(p).convert("RGB") for p in a.pngs]
for p, i in zip(a.pngs, ims):
    print(f"{p}: {i.size[0] / 200:.2f} in at 200 dpi" + ("  ⚠ > 8.5 in" if i.size[0] / 200 > 8.6 else ""))
ims = [i.resize((a.w, int(i.size[1] * a.w / i.size[0]))) for i in ims]
cols = [ims[k::a.cols] for k in range(a.cols)]
H = max(sum(i.size[1] + 16 for i in c) for c in cols if c)
M = Image.new("RGB", (a.cols * (a.w + 20), H), "white")
for k, c in enumerate(cols):
    y = 0
    for i in c:
        M.paste(i, (k * (a.w + 20), y)); y += i.size[1] + 16
M.save(a.o); print("wrote", a.o, M.size)

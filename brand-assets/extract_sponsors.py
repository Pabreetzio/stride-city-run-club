"""
Extract individual sponsor logos from "Sponsors Logo.ai" into /public/sponsors.

The source file (brand-assets/Sponsors Logo.ai) is a single-page Adobe
Illustrator / PDF that Ari (club organizer) emailed over. It holds all sponsor
logos in a 2-column grid. This script renders the page, segments each logo by
projecting non-white content into horizontal/vertical bands, trims whitespace,
normalizes near-white backgrounds to pure white, and writes web-sized PNGs.

Re-run with: python brand-assets/extract_sponsors.py
Requires: PyMuPDF (fitz), Pillow, numpy
"""
import os
import fitz
import numpy as np
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "brand-assets", "Sponsors Logo.ai")
OUT = os.path.join(ROOT, "public", "sponsors")
os.makedirs(OUT, exist_ok=True)

doc = fitz.open(SRC)
pix = doc[0].get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)  # 9000x9000
img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
W, H = img.size
mask = np.asarray(img.convert("L")) < 245  # content = darker than near-white


def runs(occ, min_gap):
    idx = np.where(occ)[0]
    if len(idx) == 0:
        return []
    bands, s, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > min_gap:
            bands.append((s, prev))
            s = i
        prev = i
    bands.append((s, prev))
    return bands


# Split the two columns at the whitest column near the horizontal center.
colsum = mask.sum(axis=0)
mid = W // 2
region = slice(int(mid - 0.12 * W), int(mid + 0.12 * W))
gutter = region.start + int(np.argmin(colsum[region]))

# Detect logo bands per column. min_gap merges within-logo gaps (icon<->text)
# while keeping separate logos apart.
seg = {}
for label, xs, xe in [("L", 0, gutter), ("R", gutter, W)]:
    sub = mask[:, xs:xe]
    rowocc = sub.sum(axis=1) > (0.002 * (xe - xs))
    for y0, y1 in runs(rowocc, int(0.026 * H)):
        band = sub[y0:y1 + 1, :]
        cx = np.where(band.sum(axis=0) > 0)[0]
        seg.setdefault(label, []).append((y0, y1, cx.min() + xs, cx.max() + xs))

names_L = ["edge-city-brewery", "hawthornes-pizza", "anytime-fitness", "smoothie-king"]
names_R = ["move-with-ari", "east-side-animal-hospital", "mora"]
boxes = {}
for n, (y0, y1, x0, x1) in zip(names_L, seg["L"]):
    boxes[n] = (x0, y0, x1, y1)
for n, (y0, y1, x0, x1) in zip(names_R, seg["R"]):
    boxes[n] = (x0, y0, x1, y1)

# Smoothie King is wider than one column and its "KING" crosses the center
# gutter into MoRA's row, so override those two with hand-verified splits.
boxes["smoothie-king"] = (1001, 7315, 4402, 7775)
boxes["mora"] = (5453, 6119, 6890, 7989)


def trim(im, thresh=14):
    g = im.convert("L")
    diff = ImageChops.difference(g, Image.new("L", im.size, 255))
    diff = diff.point(lambda x: 255 if x > thresh else 0)
    bb = diff.getbbox()
    return im.crop(bb) if bb else im


def whiten(im, floor=235):
    """Snap near-white / lightly-tinted background pixels to pure white."""
    a = np.asarray(im).copy()
    light = (a[:, :, 0] >= floor) & (a[:, :, 1] >= floor) & (a[:, :, 2] >= floor)
    a[light] = 255
    return Image.fromarray(a)


for name, (x0, y0, x1, y1) in boxes.items():
    c = whiten(trim(img.crop((x0, y0, x1 + 1, y1 + 1))))
    pad = int(max(c.size) * 0.06)
    canvas = Image.new("RGB", (c.size[0] + 2 * pad, c.size[1] + 2 * pad), (255, 255, 255))
    canvas.paste(c, (pad, pad))
    if max(canvas.size) > 800:
        r = 800 / max(canvas.size)
        canvas = canvas.resize((round(canvas.size[0] * r), round(canvas.size[1] * r)), Image.LANCZOS)
    canvas.save(os.path.join(OUT, f"{name}.png"))
    print(f"{name}: {canvas.size}")

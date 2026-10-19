"""Side-by-side before/after contact sheets for matched Phase 03 cameras.
python tools/phase03_compare_sheet.py <before_dir> <after_dir> <out.jpg> name[,name...]"""
import sys, os
from PIL import Image, ImageDraw
before, after, out, names = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(",")
W, H = 640, 360
sheet = Image.new("RGB", (W * 2, (H + 18) * len(names)), "white")
d = ImageDraw.Draw(sheet)
for i, n in enumerate(names):
    for j, folder in enumerate((before, after)):
        p = os.path.join(folder, n + ".png")
        if os.path.exists(p):
            sheet.paste(Image.open(p).convert("RGB").resize((W, H)), (j * W, i * (H + 18) + 18))
        d.text((j * W + 4, i * (H + 18) + 3), ("BEFORE " if j == 0 else "AFTER ") + n, fill="black")
sheet.save(out, quality=86)

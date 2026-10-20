"""Contact sheet of a frame burst: python -I tools/phase05_contact_sheet.py <dir> <glob> <out.jpg> [cols]"""
import sys, glob, os
from PIL import Image, ImageDraw
d, pat, out = sys.argv[1], sys.argv[2], sys.argv[3]
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 4
files = sorted(glob.glob(os.path.join(d, pat)))
w, h = 480, 270
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * (h + 18)), (20, 20, 20))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((w, h))
    x, y = (i % cols) * w, (i // cols) * (h + 18)
    sheet.paste(im, (x, y + 18))
    ImageDraw.Draw(sheet).text((x + 4, y + 3), os.path.basename(f)[:70], fill=(255, 255, 0))
sheet.save(out, quality=88)
print(out, len(files))

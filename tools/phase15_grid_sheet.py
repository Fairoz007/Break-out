"""Grid contact sheet with clip labels: python tools/phase15_grid_sheet.py DIR [cols]"""
import glob, os, sys
from PIL import Image, ImageDraw
d = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 8
fs = sorted(f for f in glob.glob(os.path.join(d, '*.png')) if 'sheet' not in os.path.basename(f))
rows = (len(fs) + cols - 1) // cols; s = Image.new('RGB', (cols * 150, rows * 216), (20, 20, 20)); dr = ImageDraw.Draw(s)
for i, f in enumerate(fs):
    x, y = (i % cols) * 150, (i // cols) * 216; s.paste(Image.open(f).convert('RGB').resize((150, 200)), (x, y + 16))
    dr.text((x + 2, y + 2), os.path.basename(f).split('__')[-1][:-4][:24], fill=(230, 230, 230))
s.save(os.path.join(d, 'sheet_all_clips.png')); print(len(fs), os.path.join(d, 'sheet_all_clips.png'))

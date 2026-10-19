"""Contact sheet of autopilot screenshots: python tools/phase03_contact_sheet.py <dir> <out.jpg> [step] [start] [count]"""
import sys, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]
step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
count = int(sys.argv[5]) if len(sys.argv) > 5 else 12
files = sorted(f for f in os.listdir(d) if f.endswith(".png"))[start::step][:count]
W, H, cols = 480, 270, 3
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, (H + 16) * rows), "white")
dr = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    x, y = (i % cols) * W, (i // cols) * (H + 16)
    sheet.paste(Image.open(os.path.join(d, f)).convert("RGB").resize((W, H)), (x, y + 16))
    dr.text((x + 3, y + 2), f[:70], fill="black")
sheet.save(out, quality=85)
print(len(files))

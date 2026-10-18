"""Assemble rendered previews into a labelled contact sheet. python -I tools/phase15_contact_sheet.py OUT.png img1 img2 ..."""
import os, sys
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size; cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
s = 0.5; tw, th = int(w*s), int(h*s)
sheet = Image.new('RGB', (cols*tw, rows*(th+16)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
for i, (im, f) in enumerate(zip(ims, files)):
    x, y = (i % cols)*tw, (i // cols)*(th+16)
    sheet.paste(im.resize((tw, th)), (x, y+16)); d.text((x+3, y+2), os.path.basename(f)[:44], fill=(230, 230, 230))
sheet.save(out); print(out, sheet.size)

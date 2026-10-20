"""Phase 06 (D06-010): corrections-officer insignia for the guard/Rusk uniform texture.

The Rocketbox security uniform (rb_tomas_rusk, Map #16) carries "SECURITY ★ OFFICER" sleeve patches and a
"SECURITY" chest name bar, which read as private security. This repaints a copy: patches become
"BLACKRIDGE ★ CORRECTIONS" (original star, rim and fabric shading kept), the name bar reads "CORRECTIONS".
The original texture is untouched; character_visual.gd TEXTURE_FIXES swaps the copy in at load (GLB, rig and
blendshapes unchanged).
python3 -I tools/phase06_guard_insignia.py
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

R = Path(__file__).resolve().parents[1]
SRC = R / 'assets/characters/acquisition_20261019/rocketbox_facial/rb_tomas_rusk_Map #16.png'
OUT = R / 'assets/characters/phase06/guard_body_corrections.png'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PATCHES = [(314, 1070), (1758, 1070)]   # measured centres of the two sleeve patches (diameter ~97 px)
NAME_BAR = (1108, 932, 1181, 952)        # measured bounds of the chest name bar


def font(size):
    try:
        return ImageFont.truetype(BOLD, size)
    except OSError:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size)


def arc_text(layer, cx, cy, radius, text, size, top=True, fill=(38, 40, 44, 255)):
    """Draw text along a circle (top arc reads left-to-right clockwise, bottom arc counter-clockwise)."""
    f = font(size)
    widths = [f.getlength(ch) for ch in text]
    total = sum(widths) + 0.5 * size * (len(text) - 1) * 0.12
    span = total / radius
    ang = -math.pi / 2 - span / 2 if top else math.pi / 2 + span / 2
    for ch, w in zip(text, widths):
        step = (w + 0.06 * size) / radius
        a = ang + step / 2 if top else ang - step / 2
        tile = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((size, size), ch, font=f, fill=fill, anchor='mm')
        rot = math.degrees(a + math.pi / 2) if top else math.degrees(a - math.pi / 2)
        tile = tile.rotate(-rot, resample=Image.BICUBIC)
        x, y = cx + radius * math.cos(a), cy + radius * math.sin(a)
        layer.alpha_composite(tile, (int(x - size), int(y - size)))
        ang = ang + step if top else ang - step


def main():
    img = Image.open(SRC).convert('RGBA')
    px = np.asarray(img).astype(np.float32)
    for cx, cy in PATCHES:
        r_patch = 44
        # clear the old lettering ring: fill the annulus between the star and the rim with the patch's own cloth
        # tone, keeping its shading (low-pass of the original) so it still looks printed on fabric
        box = (cx - 52, cy - 52, cx + 52, cy + 52)
        region = img.crop(box)
        blur = region.filter(ImageFilter.GaussianBlur(9))
        arr = np.asarray(region).astype(np.float32)
        barr = np.asarray(blur).astype(np.float32)
        yy, xx = np.mgrid[0:104, 0:104]
        d = np.hypot(xx - 52, yy - 52)
        inner = d < 21                      # original embroidered star: kept
        disc = d < 49.5                     # whole patch incl. the old lettering and rim
        cloth = (d > 22) & (d < 38)
        base = np.median(arr[cloth][:, :3], axis=0)
        shade = np.clip(barr[..., :3].mean(-1, keepdims=True) / max(barr[cloth][:, :3].mean(), 1), 0.85, 1.12)
        newdisc = np.clip(base[None, None] * shade, 0, 255)
        rim = (d >= 45.0) & (d < 49.5)
        newdisc = np.where(rim[..., None], np.array([46.0, 48.0, 52.0])[None, None], newdisc)
        edge = (d >= 49.5) & (d < 51.5)     # soft blend into the sleeve
        uni = np.median(arr[(d > 51.5)][:, :3], axis=0)
        arr[..., :3] = np.where((disc & ~inner)[..., None], newdisc, arr[..., :3])
        arr[..., :3] = np.where(edge[..., None], (arr[..., :3] + uni[None, None]) / 2, arr[..., :3])
        new = Image.fromarray(arr.astype(np.uint8), 'RGBA')
        layer = Image.new('RGBA', new.size, (0, 0, 0, 0))
        arc_text(layer, 52, 52, 35, 'BLACKRIDGE', 12, top=True)
        arc_text(layer, 52, 52, 35, 'CORRECTIONS', 11, top=False)
        new.alpha_composite(layer)
        img.paste(new, box[:2])
    # name bar: repaint its face and letter it
    x0, y0, x1, y1 = NAME_BAR
    bar = np.asarray(img.crop((x0, y0, x1 + 1, y1 + 1))).astype(np.float32)
    face = np.median(bar[2:-2, 2:-2, :3].reshape(-1, 3)[bar[2:-2, 2:-2, :3].reshape(-1, 3).mean(1) > 150], axis=0)
    d = ImageDraw.Draw(img)
    d.rectangle((x0 + 2, y0 + 2, x1 - 2, y1 - 2), fill=tuple(int(v) for v in face) + (255,))
    size = 12
    while size > 6 and font(size).getlength('CORRECTIONS') > (x1 - x0) - 6:
        size -= 1
    d.text(((x0 + x1) / 2, (y0 + y1) / 2 + 0.5), 'CORRECTIONS', font=font(size), fill=(30, 32, 36, 255), anchor='mm')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.convert('RGB').save(OUT)
    print('GUARD_INSIGNIA', OUT.relative_to(R))


if __name__ == '__main__':
    main()

"""Phase 06 (D06-011): uniform variants for generic inmates so they stop matching Adrian's overshirt exactly.

Source: the Rocketbox m012 prison texture (rb_prisoner_npc). Only orange *shirt* texels change (the trouser UV
blocks, skin, belt and shoes are left alone), so styling stays institutional:
  B  "rust"  - older, darker, sun-faded issue shirt
  C  "work"  - grey work-detail shirt over the orange trousers
Variant A is the unchanged texture. character_visual.gd picks a variant per NPC name (stable hash).
python3 -I tools/phase06_inmate_variants.py
"""
from pathlib import Path
from PIL import Image
import numpy as np

R = Path(__file__).resolve().parents[1]
SRC = R / 'assets/characters/acquisition_20261019/rocketbox_facial/rb_prisoner_npc_m012_body_color_prison.png'
OUT = R / 'assets/characters/phase06'
# trouser UV blocks in the m012 layout (fractions of the texture; measured from the texture, see the sheet)
TROUSERS = [(0.0, 0.0, 0.29, 0.44), (0.71, 0.0, 1.0, 0.44)]


def main():
    img = np.asarray(Image.open(SRC).convert('RGB')).astype(np.float32) / 255.0
    H, W, _ = img.shape
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    mx, mn = img.max(-1), img.min(-1)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    hue = np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) % 360
    # orange cloth only: skin is less saturated, leather is darker and browner
    orange = (hue > 8) & (hue < 32) & (sat > 0.68) & (mx > 0.16)
    yy, xx = np.mgrid[0:H, 0:W]
    trousers = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in TROUSERS:
        trousers |= (xx >= x0 * W) & (xx < x1 * W) & (yy >= y0 * H) & (yy < y1 * H)
    hands = (yy > 0.82 * H) & ((xx < 0.28 * W) | (xx > 0.72 * W))   # hand UV islands (skin)
    shirt = orange & ~trousers & ~hands
    # grow the mask a few texels into the island padding so mipmaps do not bleed orange at seams
    m = shirt.copy()
    for _ in range(4):
        grown = m.copy()
        grown[1:] |= m[:-1]; grown[:-1] |= m[1:]; grown[:, 1:] |= m[:, :-1]; grown[:, :-1] |= m[:, 1:]
        m = grown & ~trousers & ~hands & (r > g * 1.15) & (sat > 0.45)
    lum = img @ np.array([0.299, 0.587, 0.114], np.float32)
    mean_l = lum[shirt].mean()
    rel = np.clip(lum / mean_l, 0.4, 1.7)[..., None]
    variants = {
        'inmate_shirt_rust.png': np.array([0.46, 0.20, 0.10]),
        'inmate_shirt_work.png': np.array([0.50, 0.51, 0.50]),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, col in variants.items():
        out = img.copy()
        out[m] = np.clip(col[None] * rel[m], 0, 1)
        Image.fromarray((out * 255).astype(np.uint8)).save(OUT / name)
        print('INMATE_VARIANT', name, 'shirt texels', int(m.sum()))


if __name__ == '__main__':
    main()

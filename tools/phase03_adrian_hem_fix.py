"""D03-009: repair Adrian's prison-sweater texture (MIT Rocketbox Male_Adult_02 derivative).

The Phase 01.5 recolour labelled triangles along the sweater hem and cuffs as trouser/skin regions, leaving grey
and cream zigzags inside the sweater UV islands (visible as a jagged hem in close shots). This pass reclassifies
texels from the ORIGINAL Rocketbox texture: every texel that is cream knit there (warm, light, low chroma, not
skin) becomes prison orange, shaded by the original luminance, so hem and cuffs are continuous knit.

    python tools/phase03_adrian_hem_fix.py
Writes assets/characters/phase03/adrian_body_prison_p03.png (+ a mask preview for review).
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

R = Path(__file__).resolve().parents[1]
orig = np.asarray(Image.open(R / "asset_library/original_downloads/phase15_discovery/microsoft_rocketbox/Adults/Male_Adult_02/Textures/m003_body_color.tga").convert("RGB")).astype(np.float32) / 255
cur = np.asarray(Image.open(R / "assets/characters/acquisition_20261019/rocketbox_facial/rb_adrian_cross_m003_body_color_prison.png").convert("RGB")).astype(np.float32) / 255
r, g, b = orig[..., 0], orig[..., 1], orig[..., 2]
lum = orig @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
cream = (r > 0.42) & (g > 0.38) & (b > 0.30) & ((r - b) < 0.22) & ((g / np.maximum(r, 1e-3)) > 0.84)
# knit is cream in the original and already orange (most of the island) in the current derivative
orange_now = (cur[..., 0] > 0.45) & (cur[..., 0] - cur[..., 2] > 0.25)
mask = cream
H, W = mask.shape
yy, xx = np.mgrid[0:H, 0:W]
shoes = (yy > 0.68 * H) & (((xx > 0.22 * W) & (xx < 0.43 * W)) | ((xx > 0.58 * W) & (xx < 0.80 * W)))   # shoe islands (cream laces)
mask &= ~shoes
# inside the torso island, darker-shaded knit that the old pass turned grey also belongs to the sweater
sat = cur.max(axis=2) - cur.min(axis=2)
torso = (xx > 0.33 * W) & (xx < 0.67 * W) & (yy > 0.05 * H) & (yy < 0.83 * H)
sleeves = (yy > 0.43 * H) & (yy < 0.83 * H) & ((xx < 0.31 * W) | (xx > 0.69 * W))
mask |= (torso | sleeves) & (sat < 0.12) & (lum > 0.22)
# seam texels the old pass left near-white (underarm side seam), judged on the current derivative
cur_sat = cur.max(axis=2) - cur.min(axis=2)
mask |= (torso | sleeves) & (cur_sat < 0.15) & (cur.mean(axis=2) > 0.55)
mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
ref_lum = np.median(lum[mask & orange_now])
target = np.median(cur[mask & orange_now].reshape(-1, 3) / np.clip((lum[mask & orange_now] / ref_lum)[:, None], 0.35, 1.6), axis=0)
shade = np.clip(lum / ref_lum, 0.35, 1.6)[..., None]
out = cur.copy()
fix = mask & ~orange_now
out[mask] = np.clip(target * shade[mask], 0, 1)
dst = R / "assets/characters/phase03"
dst.mkdir(parents=True, exist_ok=True)
Image.fromarray((out * 255).astype(np.uint8)).save(dst / "adrian_body_prison_p03.png")
prev = R / "docs/phase03/visual_evidence/character"
prev.mkdir(parents=True, exist_ok=True)
side = np.concatenate([cur, out, np.repeat(fix[..., None], 3, 2).astype(np.float32)], axis=1)
Image.fromarray((side * 255).astype(np.uint8)).resize((1536, 512)).save(prev / "adrian_hem_texture_before_after_mask.jpg")
print({"knit_px": int(mask.sum()), "repaired_px": int(fix.sum()), "target_rgb": [round(float(x), 3) for x in target]})

"""Phase 04 character likeness texture pass (derivatives of MIT Microsoft Rocketbox textures).

Brings Adrian Cross and Noah Reyes closer to docs/characters/*.md without touching geometry, rigs or blendshapes.
UV positions come from rest-pose raycasts (tools/phase04_uv_raycast.py → tests/phase04/evidence/*_uv_hits.json).

Adrian (ADRIAN_CROSS.md: "short dark hair with a grey temple, healed left eyebrow cut, faded grey prison shirt,
orange overshirt"):
  - salt-and-pepper grey at the left temple on the hair cards (Map #11) and painted scalp hair (Map #5);
  - a healed cut through the left brow (Map #5);
  - a faded grey crew-neck shirt filling the sweater's V-neck (Map #5 chest region), so orange reads as overshirt.
Noah (NOAH_REYES.md: "blue prison undershirt, orange trousers, repaired boots, small burn on right wrist"):
  - fashion denim flattened to plain prison chambray; white sneakers to worn dark-brown leather; wrist burn.

    python tools/phase04_character_textures.py
Writes assets/characters/phase04/*.png and docs/phase04/visual_evidence/character/texture_edits.jpg.
"""
import json, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

R = Path(__file__).resolve().parents[1]
SRC = R / "assets/characters/acquisition_20261019/rocketbox_facial"
OUT = R / "assets/characters/phase04"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255


def save(a, name):
    Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(OUT / name)


def px(uv, shape):
    return uv[0] * shape[1], (1.0 - uv[1]) * shape[0]


def lum(a):
    return a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)


def disc_weight(shape, centres, radius):
    """Smooth union of discs (radius px) around centres → weight map 0..1."""
    h, w = shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    wgt = np.zeros((h, w), np.float32)
    for cx, cy in centres:
        x0, x1, y0, y1 = int(max(cx - radius * 2, 0)), int(min(cx + radius * 2, w)), int(max(cy - radius * 2, 0)), int(min(cy + radius * 2, h))
        d = np.sqrt((xx[y0:y1, x0:x1] - cx) ** 2 + (yy[y0:y1, x0:x1] - cy) ** 2)
        wgt[y0:y1, x0:x1] = np.maximum(wgt[y0:y1, x0:x1], np.clip(1.0 - d / radius, 0, 1) ** 0.7)
    return wgt


hits_a = json.loads((R / "tests/phase04/evidence/adrian_uv_hits.json").read_text())
hits_n = json.loads((R / "tests/phase04/evidence/noah_uv_hits.json").read_text())
report = {}

# ---------------- Adrian: hair cards (Map #11)
hair = load(SRC / "rb_adrian_cross_Map #11-Map #11.png")
# every hair face whose rest-pose centre lies in the left-temple volume (rays alone reach only the outer card)
faces = json.loads((R / "tests/phase04/evidence/adrian_temple_faces.json").read_text())["temple_faces"]
cent = [px(v, hair.shape) for k, v in hits_a.items() if k.startswith("temple_h_") and v] + [px((u, vv), hair.shape) for m, u, vv in faces if m == "m003_opacity"]
w = disc_weight(hair.shape, cent, 64.0)          # hair cards are long strips: grey the whole strand near the temple
grey = np.repeat(lum(hair)[..., None] * 0.55 + 0.33, 3, 2) * np.array([1.0, 1.0, 0.97], np.float32)
if os.environ.get("P04_DEBUG_RED"):
    grey = np.zeros_like(hair) + np.array([1.0, 0.0, 0.0], np.float32)
speckle = (rng.random(hair.shape[:2]) < 0.55)[..., None]                 # salt-and-pepper, not a flat dye
hair_out = hair * (1 - (w * 0.85)[..., None] * speckle) + grey * (w * 0.85)[..., None] * speckle
alpha = np.asarray(Image.open(SRC / "rb_adrian_cross_Map #11-Map #11.png").getchannel("A"))   # hair-card transparency
Image.fromarray(np.dstack([(np.clip(hair_out, 0, 1) * 255).astype(np.uint8), alpha])).save(OUT / "adrian_hair_p04.png")
report["adrian_temple_hair_hits"] = len(cent)

# ---------------- Adrian: head (Map #5): scalp temple grey, brow cut, grey shirt in the V
head = load(SRC / "rb_adrian_cross_Map #5.png")
cent = [px(v, head.shape) for k, v in hits_a.items() if k.startswith("temple_s_") and v] + [px((u, vv), head.shape) for m, u, vv in faces if m == "m003_head"]
w = disc_weight(head.shape, cent, 34.0)
# The visible temple hair is the painted scalp (the sparse cards barely show there, verified with P04_DEBUG_RED):
# strong salt-and-pepper grey so it reads at gameplay distance.
g2 = np.repeat(lum(head)[..., None] * 0.35 + 0.50, 3, 2) * np.array([1.0, 1.0, 0.98], np.float32)
if os.environ.get("P04_DEBUG_RED"):
    g2 = np.zeros_like(head) + np.array([0.0, 1.0, 0.0], np.float32)
sp = (rng.random(head.shape[:2]) < 0.72)[..., None]
head = head * (1 - (w * 0.9)[..., None] * sp) + g2 * (w * 0.9)[..., None] * sp
report["adrian_temple_scalp_hits"] = len(cent)
b_hi, b_lo = hits_a.get("brow_5"), hits_a.get("brow_6")
mid = hits_a.get("brow_2")
if b_hi and mid:
    hx, hy = px(b_hi, head.shape)
    mx, my = px(mid, head.shape)
    lx, ly = (2 * mx - hx, 2 * my - hy) if not b_lo or abs(b_lo[1] - mid[1]) > 0.05 else px(b_lo, head.shape)
    skin = head[int(hy - 30):int(hy - 18), int(hx - 6):int(hx + 6)].reshape(-1, 3).mean(0)   # forehead above the brow
    scar = Image.new("L", (head.shape[1], head.shape[0]), 0)
    dx, dy = lx - hx, ly - hy
    n = max((dx * dx + dy * dy) ** 0.5, 1e-3)
    dx, dy = dx / n * 21.0 + 3.0, dy / n * 21.0                    # ~42 px (~2 cm) slightly diagonal nick through the brow
    ImageDraw.Draw(scar).line([(mx - dx, my - dy), (mx + dx, my + dy)], fill=255, width=11)   # ~5 mm healed gap
    m = np.asarray(scar.filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)[..., None] / 255
    scar_col = np.clip(skin * 0.55 + np.array([0.80, 0.68, 0.64]) * 0.45, 0, 1)          # healed: pale, faintly pink
    head = head * (1 - m) + scar_col * m
    report["adrian_brow_cut_px"] = [round(hx), round(hy), round(lx), round(ly)]
H, W = head.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = xx / W, 1 - yy / H
vmask = (v > 0.252) & (v < 0.345) & (np.abs(u - 0.5) < (v - 0.25) * 1.9 + 0.004)
shirt = np.array([0.47, 0.48, 0.48], np.float32)
shade = np.clip(lum(head) / max(np.median(lum(head)[vmask]), 1e-3), 0.6, 1.3)[..., None]
knit = 1 + (rng.random((H, W)) - 0.5)[..., None] * 0.05
band = ((v > 0.328) & vmask)[..., None]                                                   # crew-neck rib at the top edge
fall = (1.08 - 0.25 * np.clip((0.345 - v) / 0.09, 0, 1))[..., None]          # light falls off down into the V
col = shirt * shade * knit * fall * np.where(band, 0.82, 1.0)
soft = np.asarray(Image.fromarray((vmask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.0))).astype(np.float32)[..., None] / 255
head = head * (1 - soft) + col * soft
report["adrian_shirt_px"] = int(vmask.sum())
save(head, "adrian_head_p04.png")

# ---------------- Noah: body (chambray shirt, leather boots, wrist burn)
body = load(SRC / "rb_noah_reyes_m007_body_color_prison.png")
H, W = body.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]
r, g, b = body[..., 0], body[..., 1], body[..., 2]
denim = (b - r > 0.08) & (b > 0.25)
L = lum(body)
blur = np.asarray(Image.fromarray((L * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
flat = 0.15 * L + 0.85 * blur                                                              # keep folds, drop denim wash/fades
ref = np.median(flat[denim])
chambray = np.array([0.30, 0.40, 0.55], np.float32) * np.clip(flat / ref, 0.55, 1.35)[..., None]
body = np.where(denim[..., None], chambray, body)
sat = body.max(2) - body.min(2)
shoes = (yy > 0.60 * H) & (sat < 0.12) & (lum(body) > 0.42) & ~((xx < 0.2 * W) & (yy > 0.85 * H))
leather = np.array([0.20, 0.13, 0.085], np.float32) * np.clip(lum(body) / 0.75, 0.5, 1.4)[..., None]
body = np.where(shoes[..., None], leather, body)
cent = [px(v, body.shape) for k, v in hits_n.items() if v]
if cent:
    cx = sum(c[0] for c in cent) / len(cent); cy = sum(c[1] for c in cent) / len(cent)
    burn = disc_weight(body.shape, [(cx + rng.normal(0, 3), cy + rng.normal(0, 3)) for _ in range(5)], 9.0)
    body = body * (1 - burn[..., None] * 0.55) + np.array([0.48, 0.22, 0.17], np.float32) * burn[..., None] * 0.55
    report["noah_burn_px"] = [round(cx), round(cy)]
report["noah_denim_px"] = int(denim.sum()); report["noah_shoe_px"] = int(shoes.sum())
save(body, "noah_body_prison_p04.png")

# review sheet
prev = R / "docs/phase04/visual_evidence/character"
prev.mkdir(parents=True, exist_ok=True)
pairs = [(SRC / "rb_adrian_cross_Map #5.png", OUT / "adrian_head_p04.png"), (SRC / "rb_adrian_cross_Map #11-Map #11.png", OUT / "adrian_hair_p04.png"),
         (SRC / "rb_noah_reyes_m007_body_color_prison.png", OUT / "noah_body_prison_p04.png")]
sheet = Image.new("RGB", (1536, 1024))
for i, (a, bb) in enumerate(pairs):
    sheet.paste(Image.open(a).convert("RGB").resize((512, 512)), (i * 512, 0))
    sheet.paste(Image.open(bb).convert("RGB").resize((512, 512)), (i * 512, 512))
sheet.save(prev / "texture_edits.jpg", quality=88)
(R / "tests/phase04/evidence/character_textures.json").write_text(json.dumps(report, indent=1))
print(report)

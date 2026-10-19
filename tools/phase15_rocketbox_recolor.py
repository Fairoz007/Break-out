"""Recolour Rocketbox clothing texture regions into prison-uniform colours (original derivative of MIT assets).
python tools/phase15_rocketbox_recolor.py <uvdump.json> <textures_dir> <out_dir> <spec.json>
spec: {"top": [r,g,b], "forearm": [r,g,b] | null, "legs": [r,g,b], "feet": [r,g,b] | null, "island_vote": bool}
Garment pixels keep their luminance (folds, seams, stitching) and take the new hue. Pixels close to the
avatar's skin colour (sampled from the head texture) are left untouched so exposed skin stays skin."""
import json, sys, colorsys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
dump, tex_dir, out_dir, spec = json.loads(Path(sys.argv[1]).read_text()), Path(sys.argv[2]), Path(sys.argv[3]), json.loads(Path(sys.argv[4]).read_text())
out_dir.mkdir(parents=True, exist_ok=True)
head = next(tex_dir.glob('*head_color.tga'))
h = np.asarray(Image.open(head).convert('RGB')).astype(np.float32) / 255
H, W, _ = h.shape; face = h[int(H * 0.35):int(H * 0.65), int(W * 0.3):int(W * 0.7)].reshape(-1, 3)
skin = np.median(face, axis=0)
report = {'skin_reference_rgb': skin.round(3).tolist(), 'textures': {}}
def island_vote(tris):
    # Each triangle takes the majority region of its UV island (triangles joined through shared UV corners).
    # Fixes region labels that cut across a garment panel, e.g. Noah's jacket hem tagged as legs.
    parent = {}
    def find(k):
        while parent.setdefault(k, k) != k: parent[k] = parent[parent[k]]; k = parent[k]
        return k
    keys = [[(img, round(u, 5), round(v, 5)) for u, v in uv] for _, img, uv in tris]
    for ks in keys:
        for k in ks[1:]: parent[find(k)] = find(ks[0])
    votes = {}
    for (r, _, _), ks in zip(tris, keys): votes.setdefault(find(ks[0]), {}).setdefault(r, 0); votes[find(ks[0])][r] += 1
    return [(max(votes[find(ks[0])].items(), key=lambda kv: kv[1])[0], img, uv) for (_, img, uv), ks in zip(tris, keys)]
by_img = {}
for mesh, tris in dump.items():
    if spec.get('island_vote'): tris = island_vote(tris)
    for r, img, uv in tris:
        if img and 'body' in img.lower() and spec.get(r): by_img.setdefault(img, []).append((r, uv))
for img, tris in by_img.items():
    src = Image.open(tex_dir / img).convert('RGB'); w, hgt = src.size
    arr = np.asarray(src).astype(np.float32) / 255
    out = arr.copy(); stats = {}
    raw = {}
    for r in sorted({t[0] for t in tris}):
        mask = Image.new('L', (w, hgt), 0); dr = ImageDraw.Draw(mask)
        for rr, uv in tris:
            if rr == r: dr.polygon([(u * w, (1 - v) * hgt) for u, v in uv], fill=255)
        raw[r] = mask
    for r in sorted(raw):
        if not isinstance(spec.get(r), list): continue
        # spec may also carry 'only_blue': {region: true}
        m = np.asarray(raw[r].filter(ImageFilter.MaxFilter(13))) > 127  # cover UV seams / padding
        for o in raw:  # QAF: the dilation must not claim texels inside another region's islands (Noah jacket-hem bleed)
            if o != r: m &= ~(np.asarray(raw[o]) > 127)
        # skin test on chromaticity (lighting-independent), cleaned with a median filter
        chroma = arr / np.maximum(arr.sum(axis=2, keepdims=True), 1e-4); sk = skin / skin.sum()
        is_skin = (np.linalg.norm(chroma - sk, axis=2) < spec.get('skin_tol', 0.03)) & (arr.max(axis=2) > 0.18)
        is_skin = np.asarray(Image.fromarray((is_skin * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9))) > 127
        garment = m & ~is_skin if spec.get('keep_skin', True) else m
        if spec.get('only_blue', {}).get(r):  # e.g. denim trouser hems inside the foot region; shoes untouched
            garment &= (arr[..., 2] - arr[..., 0]) > 0.04
        if spec.get('only_bright', {}).get(r):  # light trouser hems (khaki) above dark shoes
            garment &= arr.max(axis=2) > spec['only_bright'][r]
        lum = arr @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
        if spec.get('flatten'):  # suppress printed patterns (stripes/logos) but keep large folds
            blur = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(spec['flatten']))).astype(np.float32) / 255
            lum = np.where(garment, 0.35 * lum + 0.65 * blur, lum)
        ref = np.median(lum[garment]) if garment.any() else 0.5
        tgt = np.array(spec[r], dtype=np.float32)
        shade = np.clip(lum / max(ref, 1e-3), 0.35, 1.6)[..., None]
        out[garment] = np.clip(tgt * shade[garment], 0, 1)
        stats[r] = {'mask_px': int(m.sum()), 'garment_px': int(garment.sum()), 'skin_kept_px': int((m & ~garment).sum())}
    p = out_dir / (Path(img).stem + '_prison.png'); Image.fromarray((out * 255).astype(np.uint8)).save(p)
    report['textures'][img] = {'output': str(p), 'regions': stats}
(out_dir / 'recolor_report.json').write_text(json.dumps(report, indent=1)); print(json.dumps(report)[:600])

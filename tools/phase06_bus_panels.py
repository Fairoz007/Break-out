"""Phase 06 (D05-018): painted-steel panel detail for the prison bus body (was flat white P3_BusPaint).

Generates one tile covering 2.4 m (horizontal) x 3.2 m (ground to roof): riveted vertical panel seams every 1.2 m,
horizontal skin seams at 1.7 m and 2.9 m, road grime and spray darkening toward the sills,
faint drip streaks, and a matching tangent-space normal map (seams pressed in, rivets raised). env_intake.gd maps it
with world triplanar UVs on the P3_BusPaint surfaces only (glass, lamps, doors, wheels and decals untouched).
python3 -I tools/phase06_bus_panels.py
"""
from pathlib import Path
from PIL import Image
import numpy as np

R = Path(__file__).resolve().parents[1]
OUT = R / 'assets/props/phase06'
W, H = 1536, 2048            # 2.4 m x 3.2 m -> 640 px/m
PX = W / 2.4


def main():
    rng = np.random.default_rng(11)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    height_m = (H - 1 - yy) / PX            # image top = roof (3.2 m), bottom = ground
    x_m = xx / PX
    hgt = np.zeros((H, W), np.float32)      # height field for the normal map (metres * scale)
    # vertical seams every 1.2 m with rivets every 7.5 cm
    for sx in (0.0, 1.2, 2.4):
        d = np.abs(x_m - sx)
        hgt -= np.exp(-(d / 0.0025) ** 2) * 1.0
        for ry in np.arange(0.05, 3.2, 0.075):
            hgt += np.exp(-(((x_m - sx - 0.018) ** 2 + (height_m - ry) ** 2) / 0.004 ** 2)) * 0.8
            hgt += np.exp(-(((x_m - sx + 0.018) ** 2 + (height_m - ry) ** 2) / 0.004 ** 2)) * 0.8
    for sy in (1.7, 2.9):                   # horizontal skin seams
        hgt -= np.exp(-((height_m - sy) / 0.0025) ** 2) * 1.0
    rub = np.zeros_like(height_m, dtype=bool)   # no rub strip: the model's navy livery band sits at that height
    hgt += rub * 1.5
    # albedo: off-white institutional paint with low-frequency mottling, grime toward the sills, drip streaks
    base = np.array([0.80, 0.81, 0.79], np.float32)
    mott = sum(np.sin(x_m * f + p) * np.cos(height_m * g + q) * a for f, g, p, q, a in
               ((3.1, 2.3, 0.4, 1.1, 0.015), (7.7, 5.9, 2.0, 0.3, 0.01), (19.0, 13.0, 1.3, 2.2, 0.006)))
    grime = np.clip(1.0 - height_m / 1.35, 0, 1) ** 1.3 * 0.62             # road spray band
    noise = rng.random((H // 96, W // 96)).astype(np.float32)
    noise = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255
    streak_x = rng.random(9) * 2.4
    streaks = np.zeros((H, W), np.float32)
    for sx in streak_x:
        top = rng.uniform(1.75, 2.85)
        streaks += np.exp(-((x_m - sx) / 0.02) ** 2) * np.clip((top - height_m) / 0.6, 0, 1) * (height_m < top) * rng.uniform(0.02, 0.05)
    shade = 1.0 + mott - grime * (0.6 + 0.4 * noise) - streaks - np.clip(-hgt, 0, 1) * 0.35
    alb = base[None, None] * shade[..., None]
    alb[rub] = np.array([0.18, 0.19, 0.2]) * (0.9 + 0.2 * noise[rub][:, None])   # black rubber rub strip
    alb = np.clip(alb, 0, 1)
    # normal map from the height field
    gy, gx = np.gradient(hgt * 2.0)
    n = np.stack([-gx, gy, np.ones_like(gx)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    OUT.mkdir(parents=True, exist_ok=True)
    Image.fromarray((alb * 255).astype(np.uint8)).save(OUT / 'bus_panel_albedo.png')
    Image.fromarray(((n * 0.5 + 0.5) * 255).astype(np.uint8)).save(OUT / 'bus_panel_normal.png')
    print('BUS_PANELS', OUT.relative_to(R))


if __name__ == '__main__':
    main()

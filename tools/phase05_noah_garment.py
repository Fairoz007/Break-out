"""Phase 05 (D05-001/002): Noah Reyes prison uniform as real garment geometry.

NOAH_REYES.md: "Blue prison undershirt, orange trousers, repaired boots ... small burn on right wrist".
The Rocketbox Male_Adult_12 derivative wore a denim trucker jacket (recoloured in Phase 04, still a jacket,
cuffs hid the wrist). Every Rocketbox adult male here shares one 80-joint Biped skeleton with identical rest
transforms (tests/phase05/rig_compare.gd), so garments transfer bone-for-bone:

  * Noah keeps his own head (175 ARKit shapes), trousers and boots (UV islands dominated by pelvis/legs/feet).
  * Torso, arms and hands come from the Rocketbox m001 short-sleeve work shirt (sculpted folds, collar, real
    forearm skin) -- the jacket and its tee are removed, not recoloured.
  * Shirt texels are recoloured to faded prison blue, arm skin is colour-matched to Noah's own hands,
    and a small healed burn is painted on the outer right wrist.
  * A separate undershirt layer (its own mesh surface and material) covers the chest in the collar opening.

blender -b -P tools/phase05_noah_garment.py   ->  .../rocketbox_facial/rb_noah_reyes_p05_garment_rest.glb
then tools/phase05_characters.sh (hair pass, 37-clip transfer, copy into assets/characters/phase05)
"""
import bpy, bmesh, json, sys, math, hashlib, collections
import numpy as np
from pathlib import Path
from mathutils import Vector

R = Path(__file__).resolve().parents[1]
SRC = R / 'asset_library/converted/acquisition_20261019/rocketbox_facial'
OUT = SRC / 'rb_noah_reyes_p05_garment_rest.glb'   # then tools/phase05_hair.py -> rb_noah_reyes_p05_rest.glb
EVID = R / 'tests/phase05/evidence/noah_garment'
EVID.mkdir(parents=True, exist_ok=True)
UPPER = ('Spine', 'Spine1', 'Spine2', 'Neck', 'Clavicle', 'UpperArm', 'Forearm', 'Hand', 'Finger')
LOWER = ('Pelvis', 'Thigh', 'Calf', 'Foot', 'Toe0')
log = {}


def region(bone):
    b = bone.replace('Bip01 ', '')
    for k in LOWER:
        if k in b:
            return 'lower'
    for k in UPPER:
        if k in b:
            return 'upper'
    return 'other'


def load(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.type == 'MESH' and o.name.startswith('Icosphere'):
            bpy.data.objects.remove(o, do_unlink=True)
    new = [o for o in bpy.data.objects if o not in before]
    mesh = next(o for o in new if o.type == 'MESH')
    arm = next(o for o in new if o.type == 'ARMATURE')
    return mesh, arm


def face_regions(ob):
    """Dominant skeletal region per face (by summed weights of its vertices)."""
    gname = {g.index: g.name for g in ob.vertex_groups}
    out = []
    for p in ob.data.polygons:
        acc = collections.Counter()
        for vi in p.vertices:
            for g in ob.data.vertices[vi].groups:
                acc[region(gname[g.group])] += g.weight
        out.append(acc.most_common(1)[0][0] if acc else 'other')
    return out


def uv_islands(ob, mat_index):
    """Faces of one material grouped into UV islands (connected through shared UV-coincident edges)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    uv = bm.loops.layers.uv.active
    faces = [f for f in bm.faces if f.material_index == mat_index]
    parent = {f.index: f.index for f in faces}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for f in faces:
        for loop in f.loops:
            e = loop.edge
            for other in e.link_faces:
                if other is f or other.material_index != mat_index:
                    continue
                # same island only if the edge's UVs coincide on both sides
                a0, a1 = loop[uv].uv, loop.link_loop_next[uv].uv
                ol = next(l for l in other.loops if l.edge == e)
                b0, b1 = ol[uv].uv, ol.link_loop_next[uv].uv
                if ((a0 - b1).length < 1e-5 and (a1 - b0).length < 1e-5) or ((a0 - b0).length < 1e-5 and (a1 - b1).length < 1e-5):
                    ra, rb = find(f.index), find(other.index)
                    if ra != rb:
                        parent[ra] = rb
    islands = collections.defaultdict(list)
    for f in faces:
        islands[find(f.index)].append(f.index)
    bm.free()
    return list(islands.values())


def image_of(mat):
    for n in mat.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image and 'color' in n.image.name.lower():
            return n.image, n
    for n in mat.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image:
            return n.image, n
    raise RuntimeError('no image on ' + mat.name)


def pixels(img):
    a = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    return a.reshape(img.size[1], img.size[0], 4)


def face_texel_mask(ob, face_ids, w, h):
    """Boolean texel mask covered by the given faces' UV triangles."""
    me = ob.data
    uvl = me.uv_layers.active.data
    mask = np.zeros((h, w), dtype=bool)
    for fi in face_ids:
        p = me.polygons[fi]
        pts = [uvl[li].uv for li in p.loop_indices]
        for k in range(1, len(pts) - 1):
            _raster(mask, pts[0], pts[k], pts[k + 1], w, h)
    return mask


def _raster(mask, a, b, c, w, h):
    xs = [a.x * w, b.x * w, c.x * w]
    ys = [a.y * h, b.y * h, c.y * h]
    x0, x1 = max(int(min(xs)) - 1, 0), min(int(max(xs)) + 2, w)
    y0, y1 = max(int(min(ys)) - 1, 0), min(int(max(ys)) + 2, h)
    if x1 <= x0 or y1 <= y0:
        return
    gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
    d = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
    if abs(d) < 1e-9:
        return
    l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / d
    l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / d
    l3 = 1 - l1 - l2
    inside = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
    mask[y0:y1, x0:x1] |= inside


def rgb_to_hsv(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    s = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return s, mx


# ------------------------------------------------------------------------------------------------- build
bpy.ops.wm.read_factory_settings(use_empty=True)
noah, rig = load(SRC / 'rb_noah_reyes_rest.glb')
silas, srig = load(SRC / 'rb_silas_bell_rest.glb')
# identical rest skeletons: drive the donor with Noah's armature
for m in silas.modifiers:
    if m.type == 'ARMATURE':
        m.object = rig
silas.parent = rig
for o in list(srig.children):
    if o != silas:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.data.objects.remove(srig, do_unlink=True)

n_mats = [m.name for m in noah.data.materials]
s_mats = [m.name for m in silas.data.materials]
n_body, s_body = n_mats.index('m007_body'), s_mats.index('m001_body')

# Noah: drop the jacket/tee/hands islands, keep the trousers and boots islands and the head.
nreg = face_regions(noah)
drop_n = []
# the game renders Noah's lower body with the Phase 04 override (character_visual.gd TEXTURE_FIXES), where the
# jacket is navy: test islands and faces against that texture, not only the GLB's own
ovr = R / 'assets/characters/phase04/noah_body_prison_p04.png'
img_n0 = bpy.data.images.load(str(ovr)) if ovr.exists() else image_of(noah.data.materials[n_body])[0]
PN0 = pixels(img_n0)
for isl in uv_islands(noah, n_body):
    c = collections.Counter(nreg[f] for f in isl)
    m = face_texel_mask(noah, isl, *img_n0.size)
    mean = PN0[..., :3][m].mean(0) if m.any() else np.zeros(3)
    # jacket hem/pocket scraps sit on pelvis bones but are denim blue; trousers and boots are orange/brown
    if c['upper'] >= c['lower'] or mean[2] > mean[0]:
        drop_n += isl
        continue
    # single navy faces (jacket hem/pocket scraps) inside otherwise orange islands
    uvl_n = noah.data.uv_layers.active.data
    for fi in isl:
        p_ = noah.data.polygons[fi]
        u = sum((uvl_n[li].uv for li in p_.loop_indices), Vector((0, 0))) / p_.loop_total
        tx, ty = min(int(u.x * img_n0.size[0]), img_n0.size[0] - 1), min(int(u.y * img_n0.size[1]), img_n0.size[1] - 1)
        col = PN0[ty, tx, :3]
        if col[2] > col[0] * 1.05:
            drop_n.append(fi)
# Donor: keep torso/arms/hands islands of the body, drop its legs and its head.
sreg = face_regions(silas)
keep_s = []
s_islands = uv_islands(silas, s_body)
for isl in s_islands:
    c = collections.Counter(sreg[f] for f in isl)
    if c['upper'] > c['lower']:
        keep_s += isl
log['noah_body_faces_removed'] = len(drop_n)
log['donor_faces_kept'] = len(keep_s)

# ---- donor texture: blue shirt, Noah-toned skin, wrist burn
img_s, node_s = image_of(silas.data.materials[s_body])
img_n, _ = image_of(noah.data.materials[n_body])
W, H = img_s.size
# base: the clean original Rocketbox m001 texture (same UVs); the prison retexture had a dark triangle artifact
orig = R / 'asset_library/original_downloads/phase15_discovery/microsoft_rocketbox/Adults/Male_Adult_11/Textures/m001_body_color.tga'
img_o = bpy.data.images.load(str(orig))
assert tuple(img_o.size) == (W, H)
P = pixels(img_o).copy()
P[..., 3] = 1.0
PN = pixels(img_n)

# Noah's own hand skin (reference tone) from his hand islands
hand_faces_n = [i for i, p in enumerate(noah.data.polygons) if p.material_index == n_body and nreg[i] == 'upper'
                and any('Hand' in noah.vertex_groups[g.group].name or 'Finger' in noah.vertex_groups[g.group].name
                        for v in p.vertices for g in noah.data.vertices[v].groups if g.weight > 0.6)]
mask_nh = face_texel_mask(noah, hand_faces_n, *img_n.size)
noah_skin = PN[..., :3][mask_nh]
sat_n, val_n = rgb_to_hsv(noah_skin)
noah_skin = noah_skin[(val_n > 0.12) & (sat_n > 0.15)]

# classify texels of the kept islands: skin is bright and pinkish, the original shirt dark olive
keep_mask = np.zeros((H, W), dtype=bool)
for isl in s_islands:
    if set(isl) & set(keep_s):
        keep_mask |= face_texel_mask(silas, isl, W, H)
col_all = P[..., :3]
skin_mask = keep_mask & (col_all[..., 0] > 0.33) & (col_all[..., 0] > col_all[..., 1] * 1.12) & (col_all[..., 0] > col_all[..., 2] * 1.25)
shirt_core = keep_mask & ~skin_mask
# dilate the shirt into the island padding (mip bleed showed orange/olive outlines at seams)
shirt_mask = shirt_core.copy()
for _ in range(6):
    g = shirt_mask.copy()
    g[1:] |= shirt_mask[:-1]; g[:-1] |= shirt_mask[1:]; g[:, 1:] |= shirt_mask[:, :-1]; g[:, :-1] |= shirt_mask[:, 1:]
    shirt_mask = g & ~skin_mask
# skin padding too (pale seams would bleed into the toned arms through mipmaps)
pink = (col_all[..., 0] > 0.33) & (col_all[..., 0] > col_all[..., 1] * 1.08) & (col_all[..., 0] > col_all[..., 2] * 1.2)
for _ in range(8):
    g = skin_mask.copy()
    g[1:] |= skin_mask[:-1]; g[:-1] |= skin_mask[1:]; g[:, 1:] |= skin_mask[:, :-1]; g[:, :-1] |= skin_mask[:, 1:]
    skin_mask = g & pink & ~shirt_core
log['texels'] = {'skin': int(skin_mask.sum()), 'shirt': int(shirt_mask.sum())}

# shirt -> faded prison blue keeping the fabric shading (luminance ratio, clamped)
lum = P[..., :3] @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
mean_l = lum[shirt_core].mean() if shirt_core.any() else 0.5
blue = np.array([0.24, 0.35, 0.52], dtype=np.float32)
P[..., :3][shirt_mask] = np.clip(blue[None] * np.clip(lum[shirt_mask] / mean_l, 0.45, 1.6)[:, None], 0, 1)
# skin -> Noah's tone: per-channel mean/std transfer from the donor's skin to Noah's hands
src = P[..., :3][skin_mask]
src_ok = src[(src.max(-1) > 0.12)]
mu_s, sd_s = src_ok.mean(0), src_ok.std(0) + 1e-4
mu_n, sd_n = noah_skin.mean(0), noah_skin.std(0) + 1e-4
# multiplicative tone shift keeps the donor's pore/fold detail at its own contrast (a std transfer amplified noise)
P[..., :3][skin_mask] = np.clip(src * (mu_n / mu_s)[None], 0, 1)
log['skin_transfer'] = {'donor_mean': mu_s.round(3).tolist(), 'noah_mean': mu_n.round(3).tolist()}

# burn: outer right wrist, ~3 x 2 cm, healed (pinkish centre, darker rim), painted through 3D distance
me = silas.data
gi = {g.name: g.index for g in silas.vertex_groups}
rh = rig.pose.bones['Bip01 R Hand'].head if False else rig.data.bones['Bip01 R Hand'].head_local
rf = rig.data.bones['Bip01 R Forearm'].head_local
mw = rig.matrix_world
wrist = mw @ rh
elbow = mw @ rf
axis = (wrist - elbow).normalized()
centre_guess = wrist - axis * 0.035
mws = silas.matrix_world
cand = [(mws @ v.co, v.index) for v in me.vertices if any(g.group == gi['Bip01 R Forearm'] and g.weight > 0.4 for g in v.groups)]
# outer (dorsal) side: farthest from the body centreline among the vertices near the wrist ring
ring = [c for c in cand if abs((c[0] - centre_guess).dot(axis)) < 0.012]
centre = max(ring, key=lambda c: (c[0] - centre_guess - axis * (c[0] - centre_guess).dot(axis)).dot(Vector((0, 0, 1)) + Vector((0, 0, 0))))[0] if ring else centre_guess
# pick the vertex on the back of the wrist: largest component along the hand's back normal (approx +Z up in A-pose)
if ring:
    centre = max(ring, key=lambda c: c[0].z)[0]
log['burn_centre'] = [round(x, 4) for x in centre]
uvl = me.uv_layers.active.data
rng = np.random.default_rng(7)
burn_faces = 0
for p in me.polygons:
    if p.index not in set(keep_s):
        continue
    vs = [mws @ me.vertices[v].co for v in p.vertices]
    if min((v - centre).length for v in vs) > 0.04:
        continue
    burn_faces += 1
    loops = list(p.loop_indices)
    for k in range(1, len(loops) - 1):
        tri = [loops[0], loops[k], loops[k + 1]]
        uvs = [uvl[t].uv for t in tri]
        pos = [vs[0], vs[k], vs[k + 1]]
        xs = [u.x * W for u in uvs]; ys = [u.y * H for u in uvs]
        x0, x1 = max(int(min(xs)) - 1, 0), min(int(max(xs)) + 2, W)
        y0, y1 = max(int(min(ys)) - 1, 0), min(int(max(ys)) + 2, H)
        d = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if x1 <= x0 or y1 <= y0 or abs(d) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / d
        l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / d
        l3 = 1 - l1 - l2
        inside = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
        if not inside.any():
            continue
        px = np.stack([l1 * pos[0][j] + l2 * pos[1][j] + l3 * pos[2][j] for j in range(3)], -1)
        rel = px - np.array(centre)
        along = rel @ np.array(axis)
        across = np.sqrt(np.maximum((rel ** 2).sum(-1) - along ** 2, 0))
        # irregular healed burn ~4.4 x 3 cm wrapping the back/outer wrist: low-frequency warp of the edge,
        # mottled interior (shiny pink-brown scar tissue, darker hyperpigmented margin)
        warp = sum(np.sin(px[..., 0] * f1 * 100 + ph) * np.cos(px[..., 1] * f2 * 100 + ph * 1.7) * amp
                   for f1, f2, ph, amp in ((1.9, 2.3, 0.4, 0.22), (4.1, 3.7, 1.9, 0.12), (7.3, 6.1, 2.8, 0.06)))
        r = np.sqrt((along / 0.022) ** 2 + (across / 0.015) ** 2) + warp
        mott = sum(np.sin(px[..., 2] * f * 100 + ph) for f, ph in ((9.0, 0.3), (17.0, 1.1), (29.0, 2.2))) / 3.0
        a = np.clip((1.0 - r) * 3.0, 0, 1) * inside
        a = a * (0.8 + 0.2 * mott)
        rim = np.clip(1 - np.abs(r - 0.97) / 0.12, 0, 1) * inside * 0.55
        if (a > 0.05).any():
            bb = log.setdefault('burn_texel_bbox', [W, H, 0, 0])
            ys_, xs_ = np.nonzero(a > 0.05)
            bb[0] = min(bb[0], int(x0 + xs_.min())); bb[1] = min(bb[1], int(y0 + ys_.min()))
            bb[2] = max(bb[2], int(x0 + xs_.max())); bb[3] = max(bb[3], int(y0 + ys_.max()))
        sub = P[y0:y1, x0:x1, :3]
        scar = np.array([0.52, 0.30, 0.27], dtype=np.float32)
        dark = np.array([0.20, 0.11, 0.09], dtype=np.float32)
        sub[:] = sub * (1 - a[..., None] * 0.8) + (scar * (0.9 + 0.1 * mott[..., None])) * (a[..., None] * 0.8)
        sub[:] = sub * (1 - rim[..., None]) + dark * rim[..., None]
log['burn_faces'] = burn_faces

new_img = bpy.data.images.new('noah_p05_upper_color', W, H, alpha=True)
new_img.pixels.foreach_set(P.ravel())
new_img.filepath_raw = str(EVID / 'noah_p05_upper_color.png')
new_img.file_format = 'PNG'
new_img.save()
new_img.pack()
up_mat = silas.data.materials[s_body].copy()
up_mat.name = 'noah_p05_upper'
image_of(up_mat)[1].image = new_img
silas.data.materials[s_body] = up_mat

# delete donor faces outside the kept set (head + legs), keeping the new undershirt faces
bm = bmesh.new()
bm.from_mesh(me)
bm.faces.ensure_lookup_table()
keep = set(keep_s)
dead = [f for f in bm.faces if f.index not in keep]
bmesh.ops.delete(bm, geom=dead, context='FACES')
bm.to_mesh(me)
bm.free()

bm = bmesh.new()
bm.from_mesh(noah.data)
bm.faces.ensure_lookup_table()
dn = set(drop_n)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index in dn], context='FACES')
bm.to_mesh(noah.data)
bm.free()

# trouser waistband under the new shirt hem: any of Noah's body faces lying within 3 cm of the donor shirt
# surface (either side) is covered by the shirt; remove it so it cannot poke through while moving.
from mathutils.bvhtree import BVHTree
smw = silas.matrix_world
tree = BVHTree.FromPolygons([smw @ v.co for v in silas.data.vertices], [tuple(p.vertices) for p in silas.data.polygons])
nmw = noah.matrix_world
nrot = nmw.to_3x3().normalized()
covered = []
for p in noah.data.polygons:
    if p.material_index != n_body:
        continue
    c = nmw @ p.center
    nrm = (nrot @ p.normal).normalized()
    for d in (nrm, -nrm):
        hit = tree.ray_cast(c, d, 0.03)
        if hit[0] is not None:
            covered.append(p.index)
            break
bm = bmesh.new()
bm.from_mesh(noah.data)
bm.faces.ensure_lookup_table()
cv = set(covered)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index in cv], context='FACES')
bm.to_mesh(noah.data)
bm.free()
log['trouser_faces_under_shirt_removed'] = len(covered)

# ---- separate undershirt: the chest and lower neck in the collar opening belong to Noah's head mesh (Spine2/Neck
# dominated head faces); a duplicate of those faces, pushed out 2.5 mm, becomes the grey cotton undershirt layer.
gname_n = {g.index: g.name for g in noah.vertex_groups}
n_head = [m.name for m in noah.data.materials].index('m007_head')
chest_ids = []
for p in noah.data.polygons:
    if p.material_index != n_head:
        continue
    acc = collections.Counter()
    for vi in p.vertices:
        for g in noah.data.vertices[vi].groups:
            acc[gname_n[g.group]] += g.weight
    if acc and acc.most_common(1)[0][0] in ('Bip01 Spine2', 'Bip01 Neck'):
        chest_ids.append(p.index)
bm = bmesh.new()
bm.from_mesh(noah.data)
bm.faces.ensure_lookup_table()
dup = bmesh.ops.duplicate(bm, geom=[bm.faces[i] for i in chest_ids])
nf = [g for g in dup['geom'] if isinstance(g, bmesh.types.BMFace)]
nv = [g for g in dup['geom'] if isinstance(g, bmesh.types.BMVert)]
under = bpy.data.materials.new('noah_p05_undershirt')
under.use_nodes = True
bsdf = under.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value = (0.58, 0.58, 0.56, 1)
bsdf.inputs['Roughness'].default_value = 0.92
noah.data.materials.append(under)
u_idx = len(noah.data.materials) - 1
for f in nf:
    f.material_index = u_idx          # split faces keep it through the cut below
bm.normal_update()
shape_layers = list(bm.verts.layers.shape.values())
for v in nv:
    off = v.normal * 0.0025 / max(noah.matrix_world.to_scale().x, 1e-6)
    v.co += off
    for sl in shape_layers:      # every facial shape key gets the offset too, or blinks pull it back to the skin
        v[sl] += off
# round crew neckline: cut the duplicate with a horizontal plane at the base of the Adam's apple, keep below
neck_z = (rig.matrix_world @ rig.data.bones['Bip01 Neck'].head_local).z
inv = noah.matrix_world.inverted()
cut_co = inv @ Vector((0, 0, neck_z + 0.006))   # head mesh ends ~1.49 m inside the collar
cut_no = (inv.to_3x3() @ Vector((0, 0, 1))).normalized()
geom = nf + list({e for f in nf for e in f.edges}) + nv
bmesh.ops.bisect_plane(bm, geom=geom, plane_co=cut_co, plane_no=cut_no, clear_outer=True)
bm.to_mesh(noah.data)
bm.free()
log['undershirt_faces'] = sum(1 for p in noah.data.polygons if p.material_index == u_idx)

# join donor into Noah (vertex groups merge by bone name; Noah's shape keys extend with basis positions)
bpy.ops.object.select_all(action='DESELECT')
silas.select_set(True)
noah.select_set(True)
bpy.context.view_layer.objects.active = noah
bpy.ops.object.join()
noah.name = 'm007_hipoly_81_bones'
bpy.ops.object.material_slot_remove_unused()
log['final'] = {'verts': len(noah.data.vertices), 'faces': len(noah.data.polygons), 'materials': [m.name for m in noah.data.materials],
                'shape_keys': len(noah.data.shape_keys.key_blocks) if noah.data.shape_keys else 0,
                'unweighted': sum(1 for v in noah.data.vertices if not v.groups)}

bpy.ops.export_scene.gltf(filepath=str(OUT), export_format='GLB', export_animations=False, export_skins=True)
log['out'] = str(OUT.relative_to(R)).replace('\\', '/')
log['sha256'] = hashlib.sha256(OUT.read_bytes()).hexdigest()
(EVID / 'noah_garment_build.json').write_text(json.dumps(log, indent=1))
print('NOAH_GARMENT', json.dumps(log['final']))

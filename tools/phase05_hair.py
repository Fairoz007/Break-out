"""Phase 05 (D05-003/004): short realistic hair as geometry for Adrian Cross and Noah Reyes.

Both leads had a painted, cap-like hair shell (Noah) or a thick helmet with long cards over the ears and nape
(Adrian; ADRIAN_CROSS.md asks for "short dark hair with a grey temple", NOAH_REYES.md "wavy black cropped hair").

  1. Hair region: head-material vertices whose head-texture texel is dark hair, above the brow line or behind
     the ears (eyebrows and stubble excluded).
  2. Adrian: the long hair cards (m003_opacity) are removed and the hair volume is pulled in onto a real skull --
     the bald Rocketbox m012 inmate scalp, which is registered to the same facial rig -- plus a 2 mm scalp.
     Every shape key receives the same displacement, so facial animation is unaffected.
  3. Hair shells: N stacked copies of the hair faces offset along the normal (Adrian 1.3 cm on top tapering to
     0.45 cm over the ears and nape; Noah 0.75 cm), each its own alpha-masked material. One strand texture
     stores strand height in alpha; shell k shows strands taller than k/N, and its UVs drift along the hair
     flow so each strand leans like combed hair (Noah: tight random drift, cropped curls). Roots are darker.
     Adrian's temples get salt-and-pepper grey strands instead of the old painted blotches.
  4. The scalp under the shells is repainted a uniform hair-base colour (no photo curls, no blotches).

blender -b -P tools/phase05_hair.py -- <in_rest.glb> <out_rest.glb> adrian|noah
"""
import bpy, bmesh, sys, json, math, hashlib, collections
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

R = Path(__file__).resolve().parents[1]
SRC = R / 'asset_library/converted/acquisition_20261019/rocketbox_facial'
argv = sys.argv[sys.argv.index('--') + 1:]
IN, OUT, STYLE = Path(argv[0]), Path(argv[1]), argv[2]
EVID = R / 'tests/phase05/evidence/hair' / STYLE
EVID.mkdir(parents=True, exist_ok=True)
log = {'style': STYLE, 'in': str(IN), 'out': str(OUT)}
CFG = {
    'adrian': dict(line_px=22, shells=10, top=0.013, side=0.0045, drift=0.016, density=0.26, curl=0.0, base=(0.035, 0.027, 0.022),
                   strand=(0.20, 0.15, 0.11), grey=(0.56, 0.55, 0.53), reshape=True, head_tex_override=R / 'assets/characters/phase04/adrian_head_p04.png'),
    'noah': dict(line_px=6, shells=8, top=0.0075, side=0.005, drift=0.004, density=0.34, curl=1.0, base=(0.014, 0.012, 0.011),
                 strand=(0.085, 0.072, 0.064), grey=None, reshape=False, head_tex_override=None),
}[STYLE]
rng = np.random.default_rng(11 if STYLE == 'adrian' else 23)


def load(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    new = [o for o in bpy.data.objects if o not in before]
    for o in list(new):
        if o.type == 'MESH' and o.name.startswith('Icosphere'):
            bpy.data.objects.remove(o, do_unlink=True)
    new = [o for o in bpy.data.objects if o not in before]
    return next(o for o in new if o.type == 'MESH'), next(o for o in new if o.type == 'ARMATURE'), new


def pixels(img):
    a = np.empty(img.size[0] * img.size[1] * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    return a.reshape(img.size[1], img.size[0], 4)


def tex_node(mat):
    for n in mat.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image and n.outputs['Color'].links and any(
                l.to_socket.name == 'Base Color' for l in n.outputs['Color'].links):
            return n
    return next(n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image)


bpy.ops.wm.read_factory_settings(use_empty=True)
ob, rig, _ = load(IN)
skull, srig, snew = load(SRC / 'rb_prisoner_npc_rest.glb')
mw = ob.matrix_world
mats = [m.name for m in ob.data.materials]
head_i = next(i for i, n in enumerate(mats) if n.endswith('_head'))
# --- skull reference: the bald inmate's head faces in world space
sm = skull.matrix_world
s_head = next(i for i, m in enumerate(skull.data.materials) if m.name.endswith('_head'))
sverts = [sm @ v.co for v in skull.data.vertices]
sfaces = [tuple(p.vertices) for p in skull.data.polygons if p.material_index == s_head]
skull_tree = BVHTree.FromPolygons(sverts, sfaces)
for o in snew:
    bpy.data.objects.remove(o, do_unlink=True)

eye = (rig.matrix_world @ rig.data.bones['Bip01 LEye'].head_local + rig.matrix_world @ rig.data.bones['Bip01 REye'].head_local) / 2
headb = rig.matrix_world @ rig.data.bones['Bip01 Head'].head_local
log['eye'] = list(eye)

# --- remove long hair cards (Adrian)
if STYLE == 'adrian':
    op_i = [i for i, n in enumerate(mats) if 'opacity' in n]
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    dead = [f for f in bm.faces if f.material_index in op_i]
    log['hair_card_faces_removed'] = len(dead)
    bmesh.ops.delete(bm, geom=dead, context='FACES')
    bm.to_mesh(ob.data); bm.free()

# --- head texture
hnode = tex_node(ob.data.materials[head_i])
if CFG['head_tex_override'] and Path(CFG['head_tex_override']).exists():
    himg = bpy.data.images.load(str(CFG['head_tex_override']))   # keeps the Phase 04 brow cut
else:
    himg = hnode.image
HW, HH = himg.size
HP = pixels(himg).copy()
# classify hair on the original Rocketbox head texture (the Phase 04 one has bright grey temple blotches)
HPo = pixels(himg)             # Phase 04 texture: its grey temple paint is low-saturation (hair, not skin)
lum = pixels(hnode.image)[..., :3] @ np.array([0.299, 0.587, 0.114], dtype=np.float32)

me = ob.data
uvl = me.uv_layers.active.data
vuv = collections.defaultdict(list)
for p in me.polygons:
    if p.material_index != head_i:
        continue
    for li, vi in zip(p.loop_indices, p.vertices):
        vuv[vi].append(Vector(uvl[li].uv))
# adaptive darkness threshold: 55% of this character's own forehead-skin luminance
fore = []
for vi in vuv:
    rel = mw @ me.vertices[vi].co - eye
    if 0.0 < rel.z < 0.02 and (mw @ me.vertices[vi].co).y < eye.y + 0.01 and abs(rel.x) < 0.03:
        for uv in vuv[vi]:
            fore.append(lum[min(int(uv.y * HH), HH - 1), min(int(uv.x * HW), HW - 1)])
dark_thr = 0.55 * float(np.median(fore)) if fore else 0.2
log['dark_threshold'] = dark_thr


def is_hair_vertex(vi):
    co = mw @ me.vertices[vi].co
    rel = co - eye
    depth = co.y - eye.y            # Blender: the character faces -Y, so larger y is further back
    above_brow = rel.z > 0.028
    temples = rel.z > -0.075 and depth > 0.03                    # temples, sideburns, over the ears
    nape = rel.z > -0.16 and depth > 0.10                       # behind the ears down to the hairline
    if not (above_brow or temples or nape):
        return False
    if rel.z > 0.06 and depth > 0.03:   # crown behind the forehead: always hair (the unwrap's top notch samples background)
        return True
    votes = []
    for uv in vuv[vi]:
        tx, ty = min(int(uv.x * HW), HW - 1), min(int(uv.y * HH), HH - 1)
        c = HPo[ty, tx, :3]
        sat = (c.max() - c.min()) / max(c.max(), 1e-4)
        votes.append(lum[ty, tx] < dark_thr or (STYLE == 'adrian' and sat < 0.14 and lum[ty, tx] > 0.2))
    return bool(votes) and sum(votes) * 2 >= len(votes)


hair_v = {vi for vi in vuv if is_hair_vertex(vi)}
# close small holes / remove specks: two passes of neighbourhood majority over head vertices
adj = collections.defaultdict(set)
for e in me.edges:
    a, b = e.vertices
    if a in vuv and b in vuv:
        adj[a].add(b); adj[b].add(a)
for _ in range(2):
    nxt = set(hair_v)
    for vi in vuv:
        n = adj[vi]
        if not n:
            continue
        frac = sum(1 for x in n if x in hair_v) / len(n)
        if vi in hair_v and frac < 0.34:
            nxt.discard(vi)
        elif vi not in hair_v and frac > 0.66 and (mw @ me.vertices[vi].co - eye).z > -0.07:
            nxt.add(vi)
    hair_v = nxt
hair_f = [p.index for p in me.polygons if p.material_index == head_i and all(v in hair_v for v in p.vertices)]
log['hair_vertices'] = len(hair_v)
log['hair_faces'] = len(hair_f)

# topological distance from the hairline (0 = edge of the region) for blending and taper
dist = {vi: 99 for vi in hair_v}
frontier = [vi for vi in hair_v if any(x not in hair_v for x in adj[vi])]
for vi in frontier:
    dist[vi] = 0
d = 0
while frontier:
    nf = []
    for vi in frontier:
        for x in adj[vi]:
            if x in hair_v and dist[x] > d + 1:
                dist[x] = d + 1; nf.append(x)
    frontier = nf; d += 1

# coincident vertices (the head is split along its UV seams, e.g. the crown) must move and offset together
pos_group = collections.defaultdict(list)
for vi in hair_v:
    c = me.vertices[vi].co
    pos_group[(round(c.x, 3), round(c.y, 3), round(c.z, 3))].append(vi)

# --- reshape the hair volume onto the skull (+2 mm scalp), applied to every shape key
keys = me.shape_keys.key_blocks if me.shape_keys else []
inv = mw.inverted()
if CFG['reshape']:
    moved = 0
    for vi in hair_v:
        co = mw @ me.vertices[vi].co
        hit = skull_tree.find_nearest(co)
        if hit[0] is None:
            continue
        target = hit[0] + hit[1].normalized() * 0.002
        w = min(1.0, (dist[vi] + 0.5) / 2.5)          # ease in from the hairline
        if (target - headb).length > (co - headb).length:   # never push hair outward
            continue
        new = co.lerp(target, w)
        delta = inv.to_3x3() @ (new - co)
        me.vertices[vi].co += delta
        for k in keys:
            k.data[vi].co += delta
        moved += 1
    log['reshaped_vertices'] = moved
    # light Laplacian smoothing of the moved region (keys get the same delta)
    for _ in range(3):
        upd = {}
        for vi in hair_v:
            if dist[vi] == 0:
                continue
            n = [x for x in adj[vi]]
            avg = sum((me.vertices[x].co for x in n), Vector()) / len(n)
            upd[vi] = (avg - me.vertices[vi].co) * 0.35
        for vi, dlt in upd.items():
            me.vertices[vi].co += dlt
            for k in keys:
                k.data[vi].co += dlt
    # re-weld seam duplicates to their mean position (all keys by the same delta)
    for grp in pos_group.values():
        if len(grp) < 2:
            continue
        mean = sum((me.vertices[v].co for v in grp), Vector()) / len(grp)
        for v in grp:
            dlt = mean - me.vertices[v].co
            me.vertices[v].co += dlt
            for k in keys:
                k.data[v].co += dlt

# --- scalp base colour under the shells (hair texels of the head texture)
hair_tex_mask = np.zeros((HH, HW), dtype=bool)


def raster(mask, pts, w, h):
    for k in range(1, len(pts) - 1):
        a, b, c = pts[0], pts[k], pts[k + 1]
        xs = [a.x * w, b.x * w, c.x * w]; ys = [a.y * h, b.y * h, c.y * h]
        x0, x1 = max(int(min(xs)) - 2, 0), min(int(max(xs)) + 3, w)
        y0, y1 = max(int(min(ys)) - 2, 0), min(int(max(ys)) + 3, h)
        dd = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if x1 <= x0 or y1 <= y0 or abs(dd) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        l1 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / dd
        l2 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / dd
        mask[y0:y1, x0:x1] |= (l1 >= -0.05) & (l2 >= -0.05) & (1 - l1 - l2 >= -0.05)


for fi in hair_f:
    p = me.polygons[fi]
    raster(hair_tex_mask, [Vector(uvl[li].uv) for li in p.loop_indices], HW, HH)
# soft edge: blend factor from a blurred mask (box blur, numpy only)
soft = hair_tex_mask.astype(np.float32)
for _ in range(6):
    s2 = soft.copy()
    s2[1:] += soft[:-1]; s2[:-1] += soft[1:]; s2[:, 1:] += soft[:, :-1]; s2[:, :-1] += soft[:, 1:]
    soft = s2 / 5.0
base = np.array(CFG['base'], dtype=np.float32)
noise = rng.normal(1.0, 0.08, (HH, HW)).astype(np.float32)
HP[..., :3] = HP[..., :3] * (1 - soft[..., None] * 0.92) + (base[None, None] * noise[..., None]) * (soft[..., None] * 0.92)

# --- strand texture (RGB colour, A = strand height), in the head UV space
SW = SH = 2048
ST = np.zeros((SH, SW, 4), dtype=np.float32)
region = np.zeros((SH, SW), dtype=bool)
for fi in hair_f:
    p = me.polygons[fi]
    raster(region, [Vector(uvl[li].uv) for li in p.loop_indices], SW, SH)
ys, xs = np.nonzero(region)
n_strands = int(len(xs) * CFG['density'])
pick = rng.integers(0, len(xs), n_strands)
sx = xs[pick] + rng.random(n_strands); sy = ys[pick] + rng.random(n_strands)
hgt = rng.uniform(0.45, 1.0, n_strands)
col = np.tile(np.array(CFG['strand'], dtype=np.float32), (n_strands, 1)) * rng.lognormal(0.0, 0.35, (n_strands, 1)).astype(np.float32)
if CFG['grey'] is not None:
    # temples: in this unwrap the temple hair sits beside the face, just above the ear (both sides)
    u, v = sx / SW, sy / SH
    # soft radial falloff around each temple (above and in front of the ear), peak 38 % grey strands
    dt = np.sqrt(((np.abs(u - 0.5) - 0.225) / 0.055) ** 2 + ((v - 0.655) / 0.07) ** 2)
    greyness = rng.random(n_strands) < 0.5 * np.exp(-dt ** 2)
    col[greyness] = np.array(CFG['grey'], dtype=np.float32) * rng.normal(1.0, 0.07, (int(greyness.sum()), 1)).astype(np.float32)
    log['grey_strands'] = int(greyness.sum())
order = np.argsort(hgt)       # taller strands written last
sx, sy, hgt, col = sx[order], sy[order], hgt[order], col[order]
for dx, dy, f in ((0, 0, 1.0),):          # single-texel strands (2x2 dots merged into a helmet at grazing angles)
    xx = np.clip(sx.astype(int) + dx, 0, SW - 1); yy = np.clip(sy.astype(int) + dy, 0, SH - 1)
    m = region[yy, xx]
    ST[yy[m], xx[m], :3] = col[m]
    ST[yy[m], xx[m], 3] = np.maximum(ST[yy[m], xx[m], 3], hgt[m] * f)

# painted short strands on the scalp base under the shells (what the hair reads as at distance): each strand is a
# short line along the flow, darker at the root; Noah's curl as tight turning segments
fx = sx / SW - 0.5; fy = sy / SH - 0.64
nrm_ = np.sqrt(fx * fx + fy * fy) + 1e-6
ang = np.arctan2(fy / nrm_, fx / nrm_) + rng.normal(0, 0.18, n_strands)
if CFG['curl']:
    ang = rng.uniform(0, 2 * np.pi, n_strands)
turn = rng.normal(0, 0.45, n_strands) * CFG['curl']
length = CFG['line_px'] * hgt
px_, py_ = sx.copy(), sy.copy()
steps = int(np.ceil(length.max())) + 1
for st in range(steps):
    live = st <= length
    xx = np.clip(px_.astype(int), 0, HW - 1); yy = np.clip(py_.astype(int), 0, HH - 1)
    m = live & hair_tex_mask[yy, xx]
    t = st / np.maximum(length, 1.0)
    shade = (0.62 + 0.55 * t)[m, None]
    HP[yy[m], xx[m], :3] = HP[yy[m], xx[m], :3] * 0.25 + col[m] * shade * 0.75
    ang = ang + turn
    px_ = px_ + np.cos(ang); py_ = py_ + np.sin(ang)
head_img = bpy.data.images.new(f'{STYLE}_p05_head', HW, HH, alpha=True)
head_img.pixels.foreach_set(HP.ravel())
head_img.filepath_raw = str(EVID / f'{STYLE}_p05_head.png'); head_img.file_format = 'PNG'; head_img.save(); head_img.pack()
hnode.image = head_img
# matte hair: roughness map for the head (glTF metallicRoughness: G = roughness, B = metallic)
hb = ob.data.materials[head_i].node_tree.nodes.get('Principled BSDF')
r0 = float(hb.inputs['Roughness'].default_value) if not hb.inputs['Roughness'].is_linked else 0.55
log['head_roughness_was_linked'] = hb.inputs['Roughness'].is_linked
orm = np.zeros((HH, HW, 4), dtype=np.float32)
orm[..., 0] = 1.0; orm[..., 3] = 1.0
orm[..., 1] = r0 * (1 - soft) + 0.82 * soft
orm_img = bpy.data.images.new(f'{STYLE}_p05_head_rough', HW, HH, alpha=False)
orm_img.pixels.foreach_set(orm.ravel()); orm_img.colorspace_settings.name = 'Non-Color'
orm_img.filepath_raw = str(EVID / f'{STYLE}_p05_head_rough.png'); orm_img.file_format = 'PNG'; orm_img.save(); orm_img.pack()
if True:   # replace any previous roughness link (the Rocketbox spec map left the hair glossy)
    nt_h = ob.data.materials[head_i].node_tree
    for l in list(hb.inputs['Roughness'].links):
        nt_h.links.remove(l)
    on = nt_h.nodes.new('ShaderNodeTexImage'); on.image = orm_img
    sep = nt_h.nodes.new('ShaderNodeSeparateColor')
    nt_h.links.new(on.outputs['Color'], sep.inputs['Color'])
    nt_h.links.new(sep.outputs['Green'], hb.inputs['Roughness'])
log['head_roughness_base'] = r0
# colour bleed into empty texels (so filtering never pulls in black)
filled = ST[..., 3] > 0
rgb = ST[..., :3].copy()
for _ in range(3):
    acc = np.zeros_like(rgb); cnt = np.zeros(filled.shape, dtype=np.float32)
    for sh in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rs = np.roll(rgb, sh, (0, 1)); fs = np.roll(filled, sh, (0, 1))
        acc += rs * fs[..., None]; cnt += fs
    grow = (~filled) & (cnt > 0)
    rgb[grow] = acc[grow] / cnt[grow][:, None]
    filled = filled | grow
ST[..., :3] = rgb
log['strands'] = n_strands
strand_img = bpy.data.images.new(f'{STYLE}_p05_hair_strands', SW, SH, alpha=True)
strand_img.pixels.foreach_set(ST.ravel())
strand_img.filepath_raw = str(EVID / f'{STYLE}_p05_hair_strands.png'); strand_img.file_format = 'PNG'; strand_img.save(); strand_img.pack()

# --- shells
N = CFG['shells']
bm = bmesh.new(); bm.from_mesh(me)
bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table()
uvlay = bm.loops.layers.uv.active
shape_layers = list(bm.verts.layers.shape.values())
bm.normal_update()
src_faces = [bm.faces[i] for i in hair_f]
group_normal = {}
for grp in pos_group.values():
    n_ = sum((bm.verts[v].normal for v in grp), Vector())
    n_ = n_.normalized() if n_.length > 1e-9 else bm.verts[grp[0]].normal
    for v in grp:
        group_normal[v] = n_
# per-vertex thickness: full on the crown, tapering towards the hairline / over the ears and nape
top_z = max((mw @ bm.verts[v].co).z for v in hair_v)
thick = {}
for vi in hair_v:
    co = mw @ bm.verts[vi].co
    t = max(0.0, min(1.0, (co.z - (eye.z - 0.02)) / max(top_z - eye.z, 1e-3)))
    edge = min(1.0, (dist[vi] + 1) / 3.0)
    thick[vi] = (CFG['side'] + (CFG['top'] - CFG['side']) * t) * (0.55 + 0.45 * edge)
for grp in pos_group.values():
    tm = sum(thick[v] for v in grp) / len(grp)
    for v in grp:
        thick[v] = tm
scale = 1.0 / max(mw.to_scale().x, 1e-9)
face_uv_c = Vector((0.5, 0.64))
shell_mats = []
for k in range(1, N + 1):
    m = bpy.data.materials.new(f'hair_shell_{STYLE}_{k:02d}')
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = strand_img
    # texture straight into the BSDF (the glTF exporter drops textures behind Mix nodes); the root-to-tip tint
    # is applied per shell in Godot (CharacterVisual._setup_hair_shells)
    nt.links.new(tn.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(tn.outputs['Alpha'], bsdf.inputs['Alpha'])
    bsdf.inputs['Roughness'].default_value = 0.52
    m.blend_method = 'CLIP' if hasattr(m, 'blend_method') else m.blend_method
    try:
        m.surface_render_method = 'DITHERED'
    except Exception:
        pass
    m['gltf_alpha_cutoff'] = (k - 0.5) / N
    me.materials.append(m)
    shell_mats.append(len(me.materials) - 1)
    dup = bmesh.ops.duplicate(bm, geom=src_faces)
    nfaces = [g for g in dup['geom'] if isinstance(g, bmesh.types.BMFace)]
    vmap = dup['vert_map']
    for sv, nv in vmap.items():
        if not isinstance(sv, bmesh.types.BMVert) or sv.index not in thick:
            continue
        off = group_normal.get(sv.index, sv.normal) * (thick[sv.index] * k / N * scale)
        nv.co = sv.co + off
        for sl in shape_layers:
            nv[sl] = sv[sl] + off
    for f in nfaces:
        f.material_index = len(me.materials) - 1
        for l in f.loops:
            uv = l[uvlay].uv
            flow = (uv - face_uv_c)
            if flow.length > 1e-6:
                flow.normalize()
            if CFG['curl']:
                ang = math.sin(uv.x * 900.0) * 2.4 + math.cos(uv.y * 700.0) * 2.4
                flow = Vector((math.cos(ang), math.sin(ang)))
            l[uvlay].uv = uv + flow * (CFG['drift'] * k / N)
bm.to_mesh(me); bm.free()
log['shell_faces'] = len(hair_f) * N
log['final'] = {'verts': len(me.vertices), 'faces': len(me.polygons), 'materials': [m.name for m in me.materials],
                'shape_keys': len(me.shape_keys.key_blocks) if me.shape_keys else 0,
                'unweighted': sum(1 for v in me.vertices if not v.groups)}
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.ops.object.material_slot_remove_unused()
bpy.ops.export_scene.gltf(filepath=str(OUT), export_format='GLB', export_animations=False, export_skins=True)
log['sha256'] = hashlib.sha256(OUT.read_bytes()).hexdigest()
(EVID / 'hair_build.json').write_text(json.dumps(log, indent=1, default=str))
print('HAIR', STYLE, json.dumps(log['final']))

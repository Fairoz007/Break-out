"""Phase 05 (D05-004): Adrian Cross's wardrobe as real garment geometry.

ADRIAN_CROSS.md: "Faded grey prison shirt, orange overshirt, worn boots". The Rocketbox Male_Adult_02 derivative wore
a ribbed crew-neck sweater (recoloured orange in Phase 03, grey V painted in Phase 04 -- still a sweater). Every
Rocketbox adult male here shares one 80-joint Biped skeleton with identical rest transforms
(tests/phase05/rig_compare.gd, re-checked below), so garments transfer bone-for-bone:

  * Adrian keeps his own head (175 ARKit shapes + the Phase 05 hair shells), trousers and shoes.
  * Torso, sleeves and hands come from the Rocketbox m012 (Male_Adult_14) long-sleeve collared work shirt
    (sculpted collar, placket, cuffs) -- the sweater is removed, not recoloured.
  * The shirt texels become faded prison orange; donor hand skin is tone-matched to Adrian's own hands.
  * A separate grey cotton undershirt layer (own surface and material) fills the open collar.

Input is the shipped GLB (assets/characters/phase05/rb_adrian_cross_p05.glb, Phase 05 hair already in it); the
rest-pose output is re-animated by tools/phase05_copy_clips.py (glTF-level copy of the 37 clips by node name).
blender -b -P tools/phase05_adrian_garment.py -- <in.glb> <out_rest.glb>
"""
import bpy, bmesh, json, sys, hashlib, collections
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
argv = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = Path(argv[0]), Path(argv[1])
DONOR = R / 'asset_library/converted/phase15_characters/rocketbox/rb_prisoner_npc_rest.glb'
DONOR_TEX = R / 'asset_library/converted/phase15_characters/rocketbox/recolor/male_adult_14/m012_body_color_prison.png'
# the game renders Adrian's body through the Phase 03 hem fix (character_visual.gd TEXTURE_FIXES); his hand skin
# reference comes from that texture
ADRIAN_TEX = R / 'assets/characters/phase03/adrian_body_prison_p03.png'
EVID = R / 'tests/phase05/evidence/adrian_garment'
EVID.mkdir(parents=True, exist_ok=True)
log = {}

# Reuse the Noah garment helpers without running that build (its module body is the build).
_src = (R / 'tools/phase05_noah_garment.py').read_text()
_ns = {'__file__': str(R / 'tools/phase05_noah_garment.py')}
exec(compile(_src[:_src.index('bpy.ops.wm.read_factory_settings(use_empty=True)\nnoah')], 'phase05_noah_garment_helpers', 'exec'), _ns)
face_regions, uv_islands, image_of, pixels, face_texel_mask, rgb_to_hsv = (
    _ns[k] for k in ('face_regions', 'uv_islands', 'image_of', 'pixels', 'face_texel_mask', 'rgb_to_hsv'))


def load_any(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.type == 'MESH' and o.name.startswith('Icosphere'):
            bpy.data.objects.remove(o, do_unlink=True)
    new = [o for o in bpy.data.objects if o not in before]
    return next(o for o in new if o.type == 'MESH'), next(o for o in new if o.type == 'ARMATURE')


bpy.ops.wm.read_factory_settings(use_empty=True)
adrian, rig = load_any(SRC)
donor, drig = load_any(DONOR)
# identical rest skeletons (checked, not assumed): bone heads in armature space. Adrian's armature object carries a
# uniform 1.01 height scale (184 cm), so the donor is parented in armature space and inherits it.
dev = max((b.head_local - drig.data.bones[b.name].head_local).length * drig.matrix_world.to_scale().x
          for b in rig.data.bones if b.name in drig.data.bones)
log['height_scale'] = [round(rig.matrix_world.to_scale().x, 5), round(drig.matrix_world.to_scale().x, 5)]
donor_local = drig.matrix_world.inverted() @ donor.matrix_world
log['rest_skeleton_max_dev_m'] = round(dev, 6)
assert dev < 1e-3, 'rest skeletons differ: %f m' % dev
for m in donor.modifiers:
    if m.type == 'ARMATURE':
        m.object = rig
donor.parent = rig
donor.matrix_parent_inverse.identity()
donor.matrix_world = rig.matrix_world @ donor_local
for o in list(drig.children_recursive):
    if o != donor:
        bpy.data.objects.remove(o, do_unlink=True)
bpy.data.objects.remove(drig, do_unlink=True)
for a in list(bpy.data.actions):     # the input's 37 clips are copied back at glTF level afterwards
    bpy.data.actions.remove(a)

a_mats = [m.name for m in adrian.data.materials]
d_mats = [m.name for m in donor.data.materials]
a_body, d_body = a_mats.index('m003_body'), d_mats.index('m012_body')

# Adrian: drop the sweater (torso/arm/hand islands), keep trousers and shoes.
areg = face_regions(adrian)
drop_a = []
agn = {g.index: g.name for g in adrian.vertex_groups}


def waist_band(fi):
    # the donor shirt was tucked in at its belt and Adrian's trousers start lower: the bottom band of his own
    # sweater (torso-weighted, below 1.08 m) stays and reads as the overshirt hanging over the waistband;
    # where it lies under the shirt, the proximity pass below removes it
    p = adrian.data.polygons[fi]
    for vi in p.vertices:
        v = adrian.data.vertices[vi]
        if (adrian.matrix_world @ v.co).z > 1.08:
            return False
        best = max(v.groups, key=lambda g: g.weight, default=None)
        if best is None or not any(k in agn[best.group] for k in ('Spine', 'Pelvis')):
            return False
    return True


kept_band = 0
band_attr = adrian.data.attributes.new('p05_band', 'BOOLEAN', 'FACE')
for isl in uv_islands(adrian, a_body):
    c = collections.Counter(areg[f] for f in isl)
    if c['upper'] >= c['lower']:
        for f in isl:
            if waist_band(f):
                kept_band += 1
                band_attr.data[f].value = True
            else:
                drop_a.append(f)
log['sweater_waist_band_faces_kept'] = kept_band
# Donor: keep the shirt torso, sleeves, cuffs and hands; drop its trousers, belt, shoes and head.
dreg = face_regions(donor)
keep_d = []
d_islands = uv_islands(donor, d_body)
for isl in d_islands:
    c = collections.Counter(dreg[f] for f in isl)
    if c['upper'] > c['lower']:
        keep_d += isl
log['adrian_body_faces_removed'] = len(drop_a)
log['donor_faces_kept'] = len(keep_d)

# ---- donor texture: faded orange overshirt, Adrian-toned hands
img_d = bpy.data.images.load(str(DONOR_TEX))
W, H = img_d.size
P = pixels(img_d).copy()
P[..., 3] = 1.0
img_a = bpy.data.images.load(str(ADRIAN_TEX))
PA = pixels(img_a)
hand_faces_a = [i for i, p in enumerate(adrian.data.polygons) if p.material_index == a_body and areg[i] == 'upper'
                and any(('Hand' in adrian.vertex_groups[g.group].name or 'Finger' in adrian.vertex_groups[g.group].name) and g.weight > 0.6
                        for v in p.vertices for g in adrian.data.vertices[v].groups)]
mask_ah = face_texel_mask(adrian, hand_faces_a, *img_a.size)
a_skin = PA[..., :3][mask_ah]
sat_a, val_a = rgb_to_hsv(a_skin)
a_skin = a_skin[(val_a > 0.15) & (sat_a > 0.12)]

keep_mask = np.zeros((H, W), dtype=bool)
hand_mask = np.zeros((H, W), dtype=bool)
kd = set(keep_d)
for isl in d_islands:
    if not set(isl) & kd:
        continue
    m = face_texel_mask(donor, isl, W, H)
    keep_mask |= m
    hc = sum(1 for f in isl for vi in donor.data.polygons[f].vertices
             if any(('Hand' in donor.vertex_groups[g.group].name or 'Finger' in donor.vertex_groups[g.group].name) and g.weight > 0.5
                    for g in donor.data.vertices[vi].groups))
    nv = sum(len(donor.data.polygons[f].vertices) for f in isl)
    if hc > 0.6 * nv:
        hand_mask |= m
col = P[..., :3]
pink = (col[..., 0] > 0.3) & (col[..., 0] > col[..., 1] * 1.08) & (col[..., 0] > col[..., 2] * 1.15) & (col[..., 1] > 0.18)
skin_mask = hand_mask & pink
orange = (col[..., 0] > col[..., 1] * 1.6) & (col[..., 0] > 0.15)
shirt_core = keep_mask & ~hand_mask & orange
# dilate the shirt colour over the grey island padding (it bled through mipmaps as grey seams)
shirt_mask = shirt_core.copy()
for _ in range(8):
    g = shirt_mask.copy()
    g[1:] |= shirt_mask[:-1]; g[:-1] |= shirt_mask[1:]; g[:, 1:] |= shirt_mask[:, :-1]; g[:, :-1] |= shirt_mask[:, 1:]
    shirt_mask = g & ~hand_mask
log['texels'] = {'skin': int(skin_mask.sum()), 'shirt_core': int(shirt_core.sum()), 'shirt': int(shirt_mask.sum())}
# padding texels take the mean shirt colour; shirt texels are faded (less saturated, slightly lighter) keeping shading
lum = col @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
mean_rgb = col[shirt_core].mean(0)
pad = shirt_mask & ~shirt_core
P[..., :3][pad] = mean_rgb
faded = col[shirt_mask] * 0.78 + lum[shirt_mask][:, None] * 0.22 + 0.025
P[..., :3][shirt_mask] = np.clip(faded, 0, 1)
src = P[..., :3][skin_mask]
mu_s, mu_a = src.mean(0), a_skin.mean(0)
P[..., :3][skin_mask] = np.clip(src * (mu_a / mu_s)[None], 0, 1)
log['skin_transfer'] = {'donor_mean': mu_s.round(3).tolist(), 'adrian_mean': mu_a.round(3).tolist()}

new_img = bpy.data.images.new('adrian_p05_upper_color', W, H, alpha=True)
new_img.pixels.foreach_set(P.ravel())
new_img.filepath_raw = str(EVID / 'adrian_p05_upper_color.png')
new_img.file_format = 'PNG'
new_img.save()
new_img.pack()
up_mat = donor.data.materials[d_body].copy()
up_mat.name = 'adrian_p05_upper'
image_of(up_mat)[1].image = new_img
donor.data.materials[d_body] = up_mat

me = donor.data
bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index not in kd], context='FACES')
bm.to_mesh(me); bm.free()
bm = bmesh.new(); bm.from_mesh(adrian.data); bm.faces.ensure_lookup_table()
da = set(drop_a)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index in da], context='FACES')
bm.to_mesh(adrian.data); bm.free()

dmw = donor.matrix_world
amw = adrian.matrix_world
# trouser waistband under the shirt hem: body faces within 3 cm of the shirt surface are hidden by it; remove them
# so they cannot poke through while moving.
dmw = donor.matrix_world
tree = BVHTree.FromPolygons([dmw @ v.co for v in me.vertices], [tuple(p.vertices) for p in me.polygons])
amw = adrian.matrix_world
arot = amw.to_3x3().normalized()
covered = []
for p in adrian.data.polygons:
    if p.material_index != a_body:
        continue
    c = amw @ p.center
    nrm = (arot @ p.normal).normalized()
    if any(tree.ray_cast(c, d, 0.03)[0] is not None for d in (nrm, -nrm)):
        covered.append(p.index)
bm = bmesh.new(); bm.from_mesh(adrian.data); bm.faces.ensure_lookup_table()
cv = set(covered)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index in cv], context='FACES')
bm.to_mesh(adrian.data); bm.free()
log['trouser_faces_under_shirt_removed'] = len(covered)

# ---- separate grey undershirt from the Spine2/Neck faces of the head mesh (chest skin in the collar opening),
# pushed out 2.5 mm, crew neckline cut just above the neck joint
gname = {g.index: g.name for g in adrian.vertex_groups}
a_head = [m.name for m in adrian.data.materials].index('m003_head')
chest_ids = []
for p in adrian.data.polygons:
    if p.material_index != a_head:
        continue
    acc = collections.Counter()
    for vi in p.vertices:
        for g in adrian.data.vertices[vi].groups:
            acc[gname[g.group]] += g.weight
    if acc and acc.most_common(1)[0][0] in ('Bip01 Spine2', 'Bip01 Neck'):
        chest_ids.append(p.index)
bm = bmesh.new(); bm.from_mesh(adrian.data); bm.faces.ensure_lookup_table()
dup = bmesh.ops.duplicate(bm, geom=[bm.faces[i] for i in chest_ids])
nf = [g for g in dup['geom'] if isinstance(g, bmesh.types.BMFace)]
nv = [g for g in dup['geom'] if isinstance(g, bmesh.types.BMVert)]
under = bpy.data.materials.new('adrian_p05_undershirt')
under.use_nodes = True
bsdf = under.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value = (0.36, 0.37, 0.37, 1)     # faded grey cotton
bsdf.inputs['Roughness'].default_value = 0.93
adrian.data.materials.append(under)
u_idx = len(adrian.data.materials) - 1
for f in nf:
    f.material_index = u_idx
bm.normal_update()
shape_layers = list(bm.verts.layers.shape.values())
for v in nv:
    off = v.normal * 0.0025 / max(adrian.matrix_world.to_scale().x, 1e-6)
    v.co += off
    for sl in shape_layers:
        v[sl] += off
neck_z = (rig.matrix_world @ rig.data.bones['Bip01 Neck'].head_local).z
inv = adrian.matrix_world.inverted()
cut_co = inv @ Vector((0, 0, neck_z + float(argv[2]) if len(argv) > 2 else neck_z + 0.012))
cut_no = (inv.to_3x3() @ Vector((0, 0, 1))).normalized()
geom = nf + list({e for f in nf for e in f.edges}) + nv
bmesh.ops.bisect_plane(bm, geom=geom, plane_co=cut_co, plane_no=cut_no, clear_outer=True)
bm.to_mesh(adrian.data); bm.free()
# the kept sweater band is the grey undershirt hanging below the overshirt hem
ba = adrian.data.attributes['p05_band']
for p in adrian.data.polygons:
    if ba.data[p.index].value:
        p.material_index = u_idx
adrian.data.attributes.remove(ba)
log['undershirt_faces'] = sum(1 for p in adrian.data.polygons if p.material_index == u_idx)

# Adrian's mesh carries two white colour layers (exported as COLOR_0/1, which Godot multiplies into albedo); the
# donor must carry them too, or the join fills its vertices with black
for ca in adrian.data.color_attributes:
    if ca.name not in donor.data.color_attributes:
        nca = donor.data.color_attributes.new(ca.name, ca.data_type, ca.domain)
        nca.data.foreach_set('color', [1.0] * (4 * len(nca.data)))
log['colour_layers_filled'] = [ca.name for ca in adrian.data.color_attributes]

bpy.ops.object.select_all(action='DESELECT')
donor.select_set(True); adrian.select_set(True)
bpy.context.view_layer.objects.active = adrian
bpy.ops.object.join()
bpy.ops.object.material_slot_remove_unused()
log['final'] = {'verts': len(adrian.data.vertices), 'faces': len(adrian.data.polygons), 'materials': [m.name for m in adrian.data.materials],
                'shape_keys': len(adrian.data.shape_keys.key_blocks) if adrian.data.shape_keys else 0,
                'unweighted': sum(1 for v in adrian.data.vertices if not v.groups)}
bpy.ops.export_scene.gltf(filepath=str(OUT), export_format='GLB', export_animations=False, export_skins=True)
log['out'] = str(OUT)
log['sha256'] = hashlib.sha256(OUT.read_bytes()).hexdigest()
(EVID / 'adrian_garment_build.json').write_text(json.dumps(log, indent=1))
print('ADRIAN_GARMENT', json.dumps(log))

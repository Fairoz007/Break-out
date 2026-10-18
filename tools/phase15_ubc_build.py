"""Phase 01.5 replacement characters: Quaternius Universal Base Characters (CC0, native UAL skeleton)
plus original uniform shells generated from the body surface with copied skin weights.

Run: blender -b --factory-startup --python tools/phase15_ubc_build.py
Writes static (rest) GLBs to asset_library/converted/phase15_characters/ubc/; animations are injected
afterwards by tools/phase15_ubc_animate.py in glTF space. Source archives are never modified.
"""
import bpy, bmesh, json
from pathlib import Path
from mathutils import Vector

R = Path(__file__).resolve().parents[1]
UBC = R / 'asset_library/extracted_sources/phase15_characters/universal-base-characters/Universal Base Characters[Standard]'
BASE = UBC / 'Base Characters/Godot - UE'
TEX = UBC / 'Base Characters/Textures'
HAIR = UBC / 'Hairstyles/Rigged to Head Bone/glTF (Godot -Unreal)'
DENIM_N = R / 'assets/textures/phase15/denim_fabric/denim_fabric_nor_gl_1k.png'
OUT = R / 'asset_library/converted/phase15_characters/ubc'
OUT.mkdir(parents=True, exist_ok=True)

TOP = {'spine_01', 'spine_02', 'spine_03', 'clavicle_l', 'clavicle_r', 'upperarm_l', 'upperarm_r'}
SLEEVE = {'lowerarm_l', 'lowerarm_r'}
LEGS = {'pelvis', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r'}
FEET = {'foot_l', 'foot_r', 'ball_l', 'ball_r'}

# Story appearance (docs/characters): colours are linear-ish base colours.
CHARACTERS = {
    'adrian_cross': dict(height=1.84, skin='T_Superhero_Male_Ligh.png', hair=['Hair_Buzzed'],
                         top=(0.62, 0.20, 0.04), long_sleeve=True, legs=(0.23, 0.23, 0.22), boots=(0.10, 0.07, 0.05)),
    'noah_reyes': dict(height=1.78, skin='T_Superhero_Male_Dark.png', hair=['Hair_SimpleParted'],
                       top=(0.10, 0.17, 0.32), long_sleeve=False, legs=(0.62, 0.20, 0.04), boots=(0.13, 0.09, 0.06)),
    'prison_guard': dict(height=1.82, skin='T_Superhero_Male_Ligh.png', hair=['Hair_Buzzed'],
                         top=(0.22, 0.30, 0.42), long_sleeve=True, legs=(0.04, 0.05, 0.09), boots=(0.02, 0.02, 0.02)),
    'prisoner_npc': dict(height=1.80, skin='T_Superhero_Male_Dark.png', hair=['Hair_Buzzed', 'Hair_Beard'],
                         top=(0.62, 0.20, 0.04), long_sleeve=False, legs=(0.62, 0.20, 0.04), boots=(0.08, 0.08, 0.08)),
    'tomas_rusk': dict(height=1.83, skin='T_Superhero_Male_Ligh.png', hair=['Hair_Buzzed'],
                       top=(0.05, 0.08, 0.16), long_sleeve=True, legs=(0.04, 0.05, 0.09), boots=(0.02, 0.02, 0.02)),
    'silas_bell': dict(height=1.80, skin='T_Superhero_Male_Ligh.png', hair=[],
                       top=(0.55, 0.19, 0.05), long_sleeve=False, legs=(0.55, 0.19, 0.05), boots=(0.09, 0.08, 0.07)),
    'mara_sen': dict(base='Superhero_Female_FullBody.gltf', height=1.67, skin='T_Superhero_Female_Dark_BaseColor.png',
                     hair=['Hair_BuzzedFemale'], top=(0.10, 0.22, 0.24), long_sleeve=True, legs=(0.18, 0.40, 0.43), boots=(0.65, 0.65, 0.66)),
}
report = {}


def relink_images():
    for img in bpy.data.images:
        p = Path(bpy.path.abspath(img.filepath)) if img.filepath else None
        if p and not p.exists():
            for cand in (BASE / p.name.replace('_png.png', '.png'), TEX / p.name.replace('_png.png', '.png')):
                if cand.exists():
                    img.filepath = str(cand); img.reload(); break


def imp(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path), bone_heuristic='BLENDER')
    return [o for o in bpy.data.objects if o not in before]


def dominant(mesh_obj):
    names = {g.index: g.name for g in mesh_obj.vertex_groups}
    dom = []
    for v in mesh_obj.data.vertices:
        best = max(v.groups, key=lambda g: g.weight, default=None)
        dom.append(names[best.group] if best else None)
    return dom


def fabric_material(name, color, rough=0.88):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = rough
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(str(DENIM_N), check_existing=True)
    tex.image.colorspace_settings.name = 'Non-Color'
    nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.6
    nt.links.new(tex.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m


def build(stem, spec):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = imp(BASE / spec.get('base', 'Superhero_Male_FullBody.gltf'))
    rig = next(o for o in objs if o.type == 'ARMATURE')
    body = next(o for o in objs if o.type == 'MESH' and o.name.lower().startswith('superhero'))
    for o in objs:
        if o.type == 'MESH' and o.name.startswith('Icosphere'):
            bpy.data.objects.remove(o, do_unlink=True)
    for h in spec['hair']:
        new = imp(HAIR / (h + '.gltf'))
        for o in new:
            if o.type == 'MESH':
                o.parent = rig
                for mod in o.modifiers:
                    if mod.type == 'ARMATURE': mod.object = rig
        for o in new:
            if o.type == 'ARMATURE': bpy.data.objects.remove(o, do_unlink=True)
    for o in list(bpy.data.objects):
        if o.name.startswith('Icosphere'):
            bpy.data.objects.remove(o, do_unlink=True)  # importer bone-display helper, not character geometry
    relink_images()
    # Skin variant
    mat = body.data.materials[0]
    for n in mat.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image and 'Dark' in n.image.name or (n.type == 'TEX_IMAGE' and n.image and 'Ligh' in n.image.name):
            n.image = bpy.data.images.load(str(TEX / spec['skin']), check_existing=True)

    zs = [(body.matrix_world @ v.co).z for v in body.data.vertices]  # full body before hidden-face removal; hair adds ~1-2 cm
    # ---- uniform shell from body surface (shares skin weights exactly) ----
    dom = dominant(body)
    top = TOP | (SLEEVE if spec['long_sleeve'] else set())
    covered = top | LEGS | FEET
    bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); bpy.context.view_layer.objects.active = body
    bpy.ops.object.duplicate(); cloth = bpy.context.active_object; cloth.name = stem + '_uniform'
    cloth.data = cloth.data.copy(); cloth.data.name = cloth.name
    if cloth.data.shape_keys:
        cloth.shape_key_clear()
    # materials first: clearing slots afterwards would reset polygon material indices
    cloth.data.materials.clear()
    cloth.data.materials.append(fabric_material(stem + '_top', spec['top']))
    cloth.data.materials.append(fabric_material(stem + '_trousers', spec['legs']))
    cloth.data.materials.append(fabric_material(stem + '_boots', spec['boots'], 0.55))
    bm = bmesh.new(); bm.from_mesh(cloth.data)
    bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()

    def region(f):
        names = [dom[v.index] for v in f.verts]
        best = max(set(names), key=names.count)
        if best in FEET: return 'boots'
        if best in LEGS: return 'legs'
        if best in top: return 'top'
        return None
    fr = {f.index: region(f) for f in bm.faces}
    lay = bm.faces.layers.int.new('region')
    for f in bm.faces: f[lay] = {'top': 0, 'legs': 1, 'boots': 2, None: -1}[fr[f.index]]
    fr_of = lambda f: {0: 'top', 1: 'legs', 2: 'boots'}.get(f[lay])
    kill = [f for f in bm.faces if fr[f.index] is None]
    # offsets: boots thicker, transition vertices share the thinner offset so garments stay closed
    off = {}
    for v in bm.verts:
        regs = {fr[f.index] for f in v.link_faces}
        off[v.index] = 0.016 if regs == {'boots'} else 0.009
    for v in bm.verts:
        v.co += v.normal * off[v.index]
    uv = bm.loops.layers.uv.active
    for f in bm.faces:
        if fr[f.index] is None: continue
        f.material_index = {'top': 0, 'legs': 1, 'boots': 2}[fr[f.index]]
        for l in f.loops:
            l[uv].uv = l[uv].uv * 6.0
    bmesh.ops.delete(bm, geom=kill, context='FACES')
    # Boots: relax toe/arch detail away so the shell reads as footwear, then thicken slightly
    edge = {v for v in bm.verts if any(fr_of(f) != 'boots' for f in v.link_faces) or v.is_boundary}
    ring = {n for v in edge for e in v.link_edges for n in (e.other_vert(v),)} | edge
    boot_verts = [v for v in bm.verts if v.link_faces and v not in ring and all(fr_of(f) == 'boots' for f in v.link_faces)]
    for _ in range(4):  # gentle relax; garment edge rings stay pinned to the trouser hem
        bmesh.ops.smooth_vert(bm, verts=boot_verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.normal_update()
    for v in boot_verts:
        v.co += v.normal * 0.008
    bm.to_mesh(cloth.data); bm.free()

    # Remove body faces fully hidden under the shell (keep a one-face ring at garment edges)
    bm = bmesh.new(); bm.from_mesh(body.data); bm.faces.ensure_lookup_table()
    inside = {f.index for f in bm.faces if region(f) in ('top', 'legs')}
    hide = [f for f in bm.faces if f.index in inside and all(all(g.index in inside for g in v.link_faces) for v in f.verts)]
    hidden = len(hide)
    bmesh.ops.delete(bm, geom=hide, context='FACES'); bm.to_mesh(body.data); bm.free()

    # Height: uniform armature scale; evaluated bounding box incl. hair
    h0 = max(zs) - min(zs)
    s = spec['height'] / h0
    rig.scale = (s, s, s)
    bpy.ops.object.select_all(action='DESELECT')
    for o in [rig] + list(rig.children): o.select_set(True)
    bpy.context.view_layer.objects.active = rig
    out = OUT / (stem + '_rest.glb')
    bpy.ops.export_scene.gltf(filepath=str(out), export_format='GLB', use_selection=True, export_animations=False,
                              export_skins=True, export_image_format='AUTO')
    report[stem] = dict(file=str(out.relative_to(R)), source_height_m=round(h0, 4), scale=round(s, 4), target_height_m=spec['height'],
                        cloth_faces=len(cloth.data.polygons), body_faces_removed=hidden, body_faces_kept=len(body.data.polygons),
                        meshes=[o.name for o in rig.children if o.type == 'MESH'])
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / (stem + '.blend')))


for k, v in CHARACTERS.items():
    build(k, v)
(OUT / 'build_report.json').write_text(json.dumps(report, indent=2))
print('UBC_BUILD ' + json.dumps(report))

"""Dump UV triangles of each Rocketbox body mesh, labelled by dominant skin-weight region, for texture masks.
blender -b --factory-startup --python tools/phase15_rocketbox_uvdump.py -- <repo-relative avatar dir> <out.json>"""
import bpy, sys, json
from pathlib import Path
a = sys.argv[sys.argv.index('--') + 1:]; d = Path(a[0]); out = Path(a[1])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(d / 'Export' / (d.name + '.fbx')), use_anim=False)
REG = {'top': ['Spine', 'Clavicle', 'UpperArm', 'Neck'], 'forearm': ['Forearm'], 'legs': ['Pelvis', 'Thigh', 'Calf'], 'feet': ['Foot', 'Toe'], 'hands': ['Hand', 'Finger'], 'head': ['Head', 'Eye', 'Jaw', 'Lip', 'Mouth', 'Cheek', 'Brow', 'Nose', 'Masseter', 'Caninus', 'Tongue', 'Eyebrow']}
def region(name):
    for r, keys in REG.items():
        if any(k in name for k in keys): return r
    return 'other'
res = {}
for o in bpy.data.objects:
    if o.type != 'MESH' or not o.data.uv_layers: continue
    names = {g.index: g.name for g in o.vertex_groups}
    dom = []
    for v in o.data.vertices:
        g = max(v.groups, key=lambda g: g.weight, default=None); dom.append(region(names[g.group]) if g else 'other')
    uv = o.data.uv_layers.active.data
    tris = []
    for p in o.data.polygons:
        regs = [dom[i] for i in p.vertices]; r = max(set(regs), key=regs.count)
        img = None
        m = o.data.materials[p.material_index] if o.data.materials else None
        if m and m.use_nodes:
            b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            l = b.inputs['Base Color'].links if b else []
            t = l[0].from_node if l and l[0].from_node.type == 'TEX_IMAGE' else None
            img = (Path(bpy.path.abspath(t.image.filepath)).name if t and t.image.filepath else t.image.name) if t and t.image else 'MAT:' + m.name
        loops = list(p.loop_indices)
        for k in range(1, len(loops) - 1):
            tris.append([r, img, [list(uv[loops[0]].uv), list(uv[loops[k]].uv), list(uv[loops[k + 1]].uv)]])
    res[o.name] = tris
out.write_text(json.dumps(res)); print('UVDUMP', {k: len(v) for k, v in res.items()})

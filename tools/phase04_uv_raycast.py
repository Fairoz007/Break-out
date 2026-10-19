"""Raycast a rest-pose Rocketbox GLB and record the exact UV of each hit (Blender, headless). Used to place texture
edits on body landmarks (brow, temple, wrist) without touching geometry, rigs or blendshapes.
    blender -b --factory-startup --python tools/phase04_uv_raycast.py -- <glb> <rays.json> <out.json>
rays.json: [[name, origin[3], direction[3], material_name], ...]; out.json: {name: [u, v, [x, y, z]] | null}
"""
import bpy, bmesh, sys, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
args = sys.argv[sys.argv.index("--")+1:]
path, rays = args[0], json.load(open(args[1]))
results = {}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=path)
for o in bpy.context.scene.objects:
    if o.type == 'ARMATURE': o.data.pose_position = 'REST'
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
o = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.data.uv_layers][0]
me = o.evaluated_get(dg).to_mesh()
bm = bmesh.new(); bm.from_mesh(me); bm.transform(o.matrix_world); bmesh.ops.triangulate(bm, faces=bm.faces)
bm.faces.ensure_lookup_table(); uvl = bm.loops.layers.uv.active
mats = [m.name for m in o.data.materials]
tree = BVHTree.FromBMesh(bm)
for name, org, d, want in rays:
    org = Vector(org); d = Vector(d).normalized(); hit = None
    for _ in range(8):
        loc, n, idx, dist = tree.ray_cast(org, d, 5)
        if loc is None: break
        f = bm.faces[idx]
        if mats[f.material_index] == want:
            a, b, c = [l.vert.co for l in f.loops]; ua, ub, uc = [l[uvl].uv.to_3d() for l in f.loops]
            uv = barycentric_transform(loc, a, b, c, ua, ub, uc)
            hit = [round(uv.x, 4), round(uv.y, 4), [round(v, 3) for v in loc]]
            break
        org = loc + d * 0.0005
    results[name] = hit
json.dump(results, open(args[2], "w"), indent=1)
print("RAYS", len(results), "hits", sum(1 for v in results.values() if v))

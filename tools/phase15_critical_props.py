"""Original construction-grade assets for mission-critical gaps (M02 ball, M05 pump, M05/M06 lifting grille).
blender -b --factory-startup --python tools/phase15_critical_props.py
Metric, Z-up source -> glTF Y-up. Origins at floor level; moving parts are separate named nodes with their own pivot.
"""
import bpy, bmesh, math, json, hashlib
from pathlib import Path
R = Path(__file__).resolve().parents[1]
SRC = R / 'asset_library/extracted_sources/phase15_architecture/critical'
SRC.mkdir(parents=True, exist_ok=True)
out = {}

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, color, metal=0.0, rough=0.6):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    return m

def box(name, size, loc, m, parent=None, bevel=0.004):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = o.modifiers.new('bevel', 'BEVEL'); mod.width = bevel; mod.segments = 2
        bpy.ops.object.modifier_apply(modifier=mod.name)
    o.data.materials.append(m)
    if parent: o.parent = parent; o.matrix_parent_inverse = parent.matrix_world.inverted()
    return o

def cyl(name, r, depth, loc, m, rot=(0, 0, 0), parent=None, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m)
    if parent: o.parent = parent; o.matrix_parent_inverse = parent.matrix_world.inverted()
    return o

def empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None); e.location = loc; bpy.context.scene.collection.objects.link(e)
    if parent: e.parent = parent
    return e

def finish(stem, folder):
    for o in bpy.data.objects:
        if o.type == 'MESH':
            bpy.context.view_layer.objects.active = o; o.select_set(True)
            bpy.ops.object.shade_auto_smooth() if hasattr(bpy.ops.object, 'shade_auto_smooth') else None
            o.select_set(False)
            # cube-projected UVs for later texturing
            bpy.context.view_layer.objects.active = o; bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.cube_project(cube_size=1.0); bpy.ops.object.mode_set(mode='OBJECT')
    p = R / folder / (stem + '.glb')
    bpy.ops.export_scene.gltf(filepath=str(p), export_format='GLB', export_apply=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(SRC / (stem + '.blend')))
    tris = sum(sum(len(f.vertices) - 2 for f in o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    xs = [(o.matrix_world @ v.co) for o in bpy.data.objects if o.type == 'MESH' for v in o.data.vertices]
    dims = [round(max(v[i] for v in xs) - min(v[i] for v in xs), 3) for i in range(3)]
    out[stem] = {'runtime_file': str(p.relative_to(R)).replace('\\', '/'), 'source': str((SRC / (stem + '.blend')).relative_to(R)).replace('\\', '/'),
                 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'triangles': tris, 'dims_xyz_m_blender': dims,
                 'nodes': sorted(o.name for o in bpy.data.objects)}

# ---------- Basketball (FIBA size 7: 0.749 m circumference, ~0.239 m diameter) ----------
reset()
r = 0.749 / (2 * math.pi)
bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=48, ring_count=24, location=(0, 0, r)); ball = bpy.context.active_object; ball.name = 'basketball'
ball.data.materials.append(mat('ball_leather', (0.62, 0.20, 0.05), rough=0.75)); ball.data.materials.append(mat('ball_seam', (0.02, 0.02, 0.02), rough=0.6))
for f in ball.data.polygons:  # seam bands: equator + two meridians
    c = f.center
    if abs(c.z) < r * 0.1 or abs(c.x) < r * 0.1 or abs(c.y) < r * 0.1: f.material_index = 1
bpy.ops.object.shade_smooth()
finish('basketball', 'assets/props/phase15')

# ---------- Pump unit (M05 meeting point / ledger location) ----------
reset()
steel = mat('pump_paint', (0.12, 0.25, 0.18), 0.3, 0.55); dark = mat('pump_metal', (0.18, 0.18, 0.19), 0.9, 0.4); conc = mat('plinth', (0.45, 0.45, 0.44), 0, 0.9)
root = empty('pump_unit', (0, 0, 0))
box('plinth', (2.2, 1.0, 0.15), (0, 0, 0.075), conc, root)
box('skid', (2.0, 0.8, 0.12), (0, 0, 0.21), dark, root)
cyl('motor', 0.26, 0.9, (-0.45, 0, 0.55), steel, (0, math.pi / 2, 0), root)
box('motor_feet', (0.7, 0.5, 0.06), (-0.45, 0, 0.30), dark, root)
cyl('coupling_guard', 0.14, 0.3, (0.12, 0, 0.55), mat('guard_yellow', (0.75, 0.55, 0.05), 0.2, 0.5), (0, math.pi / 2, 0), root)
cyl('volute', 0.33, 0.28, (0.55, 0, 0.58), steel, (0, math.pi / 2, 0), root)
cyl('suction_pipe', 0.09, 0.7, (0.95, 0, 0.58), dark, (0, math.pi / 2, 0), root)
cyl('discharge_pipe', 0.08, 1.2, (0.55, 0, 1.35), dark, (0, 0, 0), root)
cyl('flange_a', 0.15, 0.03, (1.28, 0, 0.58), dark, (0, math.pi / 2, 0), root)
cyl('flange_b', 0.14, 0.03, (0.55, 0, 1.94), dark, (0, 0, 0), root)
box('nameplate', (0.18, 0.005, 0.1), (-0.45, -0.262, 0.62), mat('plate', (0.75, 0.75, 0.72), 0.8, 0.3), root, 0)
empty('ledger_inspect_marker', (-0.2, -0.75, 0.0), root)
finish('pump_unit', 'assets/props/phase15')

# ---------- Lifting security grille 4 m with drive (M05 grille, M06 rear grille closes) ----------
reset()
bar = mat('grille_steel', (0.22, 0.23, 0.24), 0.85, 0.45); frame_m = mat('grille_frame', (0.15, 0.15, 0.16), 0.8, 0.5)
haz = mat('hazard_yellow', (0.8, 0.6, 0.05), 0.1, 0.5); motor_m = mat('drive_paint', (0.10, 0.18, 0.30), 0.3, 0.5)
root = empty('security_grille_4m', (0, 0, 0))
# fixed frame: opening 4.0 m wide x 3.0 m clear height; guide channels outside opening
box('guide_left', (0.12, 0.2, 3.6), (-2.06, 0, 1.8), frame_m, root)
box('guide_right', (0.12, 0.2, 3.6), (2.06, 0, 1.8), frame_m, root)
box('header', (4.4, 0.35, 0.6), (0, 0, 3.3), frame_m, root)
box('threshold_plate', (4.0, 0.3, 0.02), (0, 0, 0.01), haz, root, 0)
# moving leaf: separate node, pivot at bottom centre; animate +Z up to 2.9 m
leaf = empty('grille_leaf', (0, 0, 0), root)
box('leaf_bottom_rail', (3.96, 0.08, 0.1), (0, 0, 0.05), haz, leaf)
box('leaf_top_rail', (3.96, 0.08, 0.08), (0, 0, 2.95), bar, leaf)
box('leaf_mid_rail', (3.96, 0.06, 0.06), (0, 0, 1.5), bar, leaf)
for i in range(21):
    x = -1.9 + i * 0.19
    box('bar_%02d' % i, (0.03, 0.03, 2.9), (x, 0, 1.5), bar, leaf, 0)
# drive assembly on header: motor, gearbox, chain sprocket, manual brake wheel
drive = empty('drive_housing', (1.4, 0.35, 3.3), root)
box('gearbox', (0.5, 0.35, 0.4), (1.4, 0.38, 3.3), motor_m, drive)
cyl('drive_motor', 0.15, 0.45, (0.95, 0.38, 3.3), motor_m, (0, math.pi / 2, 0), drive)
cyl('sprocket', 0.16, 0.04, (1.75, 0.38, 3.3), bar, (0, math.pi / 2, 0), drive)
box('limit_switch', (0.08, 0.06, 0.12), (2.0, 0.15, 3.0), haz, root)
empty('latch_point', (1.98, 0, 2.9), root)
finish('security_grille_4m', 'assets/environments/phase15')

(SRC / 'critical_props_report.json').write_text(json.dumps(out, indent=2))
print('CRITICAL_PROPS ' + json.dumps(out))

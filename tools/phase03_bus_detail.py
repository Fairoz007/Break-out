"""Phase 03 prison transport bus detail pass (Blender 5.1, headless).

Input : assets/props/phase025/blackridge_transport_bus.glb (CC0 OGA coach by ajanhallinta + Phase 02.5 interior).
Output: assets/props/phase03/blackridge_transport_bus_p03.glb (+ render previews).

1. Coach proportions: x1.10 / y1.06 / z1.12 -> ~12.1 x 2.5 x 3.1 m (Godot rescales uniformly to 12 m).
2. The 0.82 m single-piece tyres are removed and replaced with 1.0 m tyres (tread blocks, sidewall, steel rim,
   hub, ten lug nuts), dual rear wheels, black arch flares and mud flaps. Each wheel is its own object
   (Wheel_FL/FR/RL/RR, origin at the hub) so Godot can spin them during the arrival shot.
3. Exterior detail placed on raycast surface hits: headlamp clusters, grille, wipers, destination sign, plates,
   luggage-bay doors (kerb-opposite side), marker lamps, tail clusters, engine louvres, roof A/C, antennas,
   unit numbers and rear caution plate. Body paint becomes P3_BusPaint (clear-coat in Godot).

    blender -b --factory-startup --python tools/phase03_bus_detail.py -- <repo_root> [--render <dir>]
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ARGS = sys.argv[sys.argv.index("--") + 1:]
ROOT = os.path.abspath(ARGS[0])
RENDER = os.path.abspath(ARGS[ARGS.index("--render") + 1]) if "--render" in ARGS else ""
sys.path.insert(0, os.path.join(ROOT, "tools"))
import phase03_props_build as pb   # shared primitives + P3 material table

pb.MATS.update({
    "P3_BusPaint": ((0.80, 0.82, 0.81), 0.0, 0.32, {}),
    "P3_LensClear": ((0.85, 0.88, 0.9), 0.0, 0.05, {"alpha": 0.35}),
    "P3_LensRed": ((0.6, 0.02, 0.02), 0.0, 0.1, {"emit": (0.5, 0.0, 0.0), "strength": 0.3}),
    "P3_LensAmber": ((0.85, 0.42, 0.02), 0.0, 0.1, {"emit": (0.6, 0.25, 0.0), "strength": 0.2}),
    "P3_Navy": ((0.03, 0.06, 0.13), 0.0, 0.4, {}),
    "P3_SignLED": ((0.02, 0.02, 0.02), 0.0, 0.3, {"emit": (1.0, 0.55, 0.08), "strength": 2.5}),
})
SX, SY, SZ = 1.10, 1.06, 1.12

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/props/phase025/blackridge_transport_bus.glb"))
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
body = [o for o in meshes if "assembly" in o.name][0]

# ---- 1. bake transforms + proportional scale
for o in meshes:
    o.data.transform(o.matrix_world)
    o.matrix_world = Matrix.Identity(4)
    o.data.transform(Matrix.Diagonal((SX, SY, SZ, 1.0)))
    o.parent = None

# side lettering was authored 5 cm proud of the old panel; after the y scale seat it on the paint
for o in meshes:
    if "identification" in o.name:
        ys = [v.co.y for v in o.data.vertices]
        side = 1 if sum(ys) > 0 else -1
        shift = side * 1.257 - (max(ys) if side < 0 else min(ys))
        for v in o.data.vertices:
            v.co.y += shift

# ---- 2. strip old tyres/rims/lug nuts around the four wheel stations
FRONT_X, REAR_X, WHEEL_Z, R_TYRE = 2.935 * SX, -2.65 * SX, 0.52, 0.52
bm = bmesh.new(); bm.from_mesh(body.data)
mats = [m.name for m in body.data.materials]
kill = []
for f in bm.faces:
    c = f.calc_center_median()
    name = mats[f.material_index]
    near = any(abs(c.x - wx) < 0.62 and abs(c.z - 0.46) < 0.6 and abs(c.y) > 0.72 for wx in (FRONT_X, REAR_X))
    if name in ("Tire", "Bolt") or (name == "Metal" and near):
        kill.append(f)
bmesh.ops.delete(bm, geom=kill, context="FACES")
bm.to_mesh(body.data); bm.free()
for m in body.data.materials:
    if m.name == "Body":
        m.name = "P3_BusPaint"
        p = m.node_tree.nodes.get("Principled BSDF") or next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        p.inputs["Base Color"].default_value = (0.80, 0.82, 0.81, 1)
        p.inputs["Roughness"].default_value = 0.32
print("STRIPPED", len(kill))

# BVH for surface placement (after stripping)
bmb = bmesh.new(); bmb.from_mesh(body.data); bmb.faces.ensure_lookup_table()
TREE = BVHTree.FromBMesh(bmb)


def hit(origin, direction):
    h = TREE.ray_cast(Vector(origin), Vector(direction).normalized(), 40)
    return h[0], h[1]


def on_surface(origin, direction, offset=0.004):
    loc, n = hit(origin, direction)
    if loc is None:
        return None, None
    return loc + n * offset, n


# ---- 3. wheels
def wheel(name, x, y, dual, outward):
    pb.PARTS.clear()
    tyres = [y] if not dual else [y, y - outward * 0.31]
    for ty in tyres:
        pb.cyl(R_TYRE, 0.28, (x, ty, WHEEL_Z), "P3_Rubber", rot=(90, 0, 0), verts=48, bevel=0.06, segs=4)
        for i in range(36):                                                    # tread blocks
            a = 2 * math.pi * i / 36
            pb.box((0.07, 0.26, 0.025), (x + math.cos(a) * (R_TYRE + 0.006), ty, WHEEL_Z + math.sin(a) * (R_TYRE + 0.006)), "P3_Rubber",
                   rot=(0, -math.degrees(a) + 90, 0), bevel=0.006, segs=1)
    face_y = y + outward * 0.141
    pb.cyl(0.30, 0.02, (x, face_y, WHEEL_Z), "P3_PaintSteelGrey", rot=(90, 0, 0), verts=40, bevel=0.008)          # steel rim
    pb.torus(0.29, 0.018, (x, face_y + outward * 0.006, WHEEL_Z), "P3_PaintSteelGrey", rot=(90, 0, 0), maj=40, mino=8)
    for i in range(8):                                                         # rim hand holes
        a = 2 * math.pi * i / 8 + 0.2
        pb.cyl(0.035, 0.03, (x + math.cos(a) * 0.2, face_y, WHEEL_Z + math.sin(a) * 0.2), "P3_PaintSteelDark", rot=(90, 0, 0), verts=12, bevel=0)
    pb.cyl(0.11, 0.06, (x, face_y + outward * 0.02, WHEEL_Z), "P3_Chrome" if not dual else "P3_PaintSteelDark", rot=(90, 0, 0), verts=24, bevel=0.01)
    for i in range(10):                                                        # lug nuts
        a = 2 * math.pi * i / 10
        pb.cyl(0.014, 0.03, (x + math.cos(a) * 0.14, face_y + outward * 0.03, WHEEL_Z + math.sin(a) * 0.14), "P3_Chrome", rot=(90, 0, 0), verts=6, bevel=0.002)
    # join into one object with origin at the hub
    bpy.ops.object.select_all(action="DESELECT")
    for o in pb.PARTS:
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        for mod in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.context.view_layer.objects.active = pb.PARTS[0]
    bpy.ops.object.join()
    w = bpy.context.active_object
    w.name = name
    bpy.context.scene.cursor.location = (x, (y + (tyres[-1])) / 2.0, WHEEL_Z)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    except Exception:
        pass
    return w


BODY_HALF = 1.19 * SY
wheels = [wheel("Wheel_FL", FRONT_X, BODY_HALF - 0.17, False, 1), wheel("Wheel_FR", FRONT_X, -(BODY_HALF - 0.17), False, -1),
          wheel("Wheel_RL", REAR_X, BODY_HALF - 0.17, True, 1), wheel("Wheel_RR", REAR_X, -(BODY_HALF - 0.17), True, -1)]

# ---- 4. exterior detail (one joined "Blackridge exterior detail" object)
pb.PARTS.clear()
for wx in (FRONT_X, REAR_X):
    for side in (1, -1):
        y = side * (BODY_HALF + 0.005)
        for i in range(27):                                                    # arch flare (overlapping arc segments)
            a = math.pi * (0.06 + 0.88 * i / 26)
            pb.box((0.12, 0.05, 0.05), (wx + math.cos(a) * 0.62, y, WHEEL_Z + math.sin(a) * 0.62), "P3_Rubber", rot=(0, -math.degrees(a) + 90, 0), bevel=0.01, segs=1)
        pb.box((0.42, 0.012, 0.34), (wx - 0.82, side * (BODY_HALF - 0.12), 0.32), "P3_Rubber", bevel=0.004)   # mud flap

FX = 5.416 * SX
# headlamp clusters + indicators
for side in (1, -1):
    yc = side * 0.80
    loc, n = on_surface((FX + 3, yc, 0.98), (-1, 0, 0), 0.006)
    if loc is not None:
        pb.box((0.012, 0.46, 0.20), (loc.x, yc, 0.98), "P3_Chrome", bevel=0.01, segs=2)
        for dy in (-0.11, 0.11):
            pb.cyl(0.075, 0.02, (loc.x + 0.012, yc + dy, 0.98), "P3_Chrome", rot=(0, 90, 0), verts=32, bevel=0.004)
            pb.sphere(0.066, (loc.x + 0.02, yc + dy, 0.98), "P3_LensClear", scale=(0.35, 1, 1), segs=24)
        pb.box((0.012, 0.12, 0.06), (loc.x + 0.008, side * 1.10, 0.98), "P3_LensAmber", bevel=0.004)
# grille
loc, n = on_surface((FX + 3, 0, 1.0), (-1, 0, 0), 0.006)
if loc is not None:
    pb.box((0.012, 0.86, 0.26), (loc.x, 0, 1.0), "P3_PaintSteelDark", bevel=0.01)
    for i in range(7):
        pb.box((0.02, 0.82, 0.014), (loc.x + 0.01, 0, 0.89 + i * 0.036), "P3_Chrome", bevel=0.002, segs=1)
    pb.box((0.01, 0.30, 0.06), (loc.x + 0.012, 0, 1.24), "P3_Navy", bevel=0.002)
# number plate front/rear
for x_dir, z in ((1, 0.66), (-1, 0.62)):
    loc, n = on_surface((x_dir * 9, 0, z), (-x_dir, 0, 0), 0.008)
    if loc is not None:
        pb.box((0.008, 0.52, 0.12), (loc.x, 0, z), "P3_LabelWhite", bevel=0.004)
        pb.box((0.006, 0.46, 0.006), (loc.x + x_dir * 0.004, 0, z + 0.045), "P3_Navy", bevel=0)
# wipers
for side in (1, -1):
    loc, n = on_surface((FX + 3, side * 0.45, 1.66), (-1, 0, 0), 0.012)
    if loc is not None:
        pb.box((0.012, 0.9, 0.018), (loc.x, side * 0.45, 1.66 + 0.18), "P3_PaintSteelDark", rot=(side * 22, 0, 0), bevel=0.003)
        pb.cyl(0.02, 0.04, (loc.x, side * 0.05, 1.63), "P3_PaintSteelDark", rot=(0, 90, 0), verts=12)
# destination sign behind the upper windscreen
loc, n = on_surface((FX + 3, 0, 2.62), (-1, 0, 0), -0.10)
if loc is not None:
    pb.box((0.05, 1.9, 0.20), (loc.x, 0, 2.62), "P3_PlasticDark", bevel=0.004)
    bpy.ops.object.text_add(location=(loc.x + 0.03, 0, 2.58))
    t = bpy.context.active_object
    t.data.body = "CORRECTIONS"
    t.data.size = 0.14
    t.data.align_x = "CENTER"
    t.rotation_euler = (math.radians(90), 0, math.radians(90))
    t.data.extrude = 0.002
    bpy.ops.object.convert(target="MESH")
    pb._finish(bpy.context.active_object, "P3_SignLED", 0, 0)
# luggage-bay doors on the +Y side (kerb side faces the intake building)
for i, (x0, x1) in enumerate(((-1.95, -0.55), (-0.45, 0.95), (1.05, 2.35))):
    yv = BODY_HALF
    loc, n = on_surface(((x0 + x1) / 2, 6, 0.7 * SZ), (0, -1, 0), 0.002)
    if loc is None:
        continue
    for x in (x0, x1):
        pb.box((0.012, 0.006, 0.66), (x, loc.y, 0.72), "P3_PaintSteelDark", bevel=0)
    for z in (0.39, 1.05):
        pb.box((x1 - x0, 0.006, 0.012), ((x0 + x1) / 2, loc.y, z), "P3_PaintSteelDark", bevel=0)
    pb.box((0.16, 0.02, 0.04), ((x0 + x1) / 2, loc.y + 0.008, 0.95), "P3_Chrome", bevel=0.008, segs=2)
    pb.cyl(0.012, 0.012, ((x0 + x1) / 2 + 0.12, loc.y + 0.01, 0.95), "P3_Chrome", rot=(90, 0, 0), verts=12)
# marker lamps along both skirts
for side in (1, -1):
    for x in (-4.6, -1.5, 1.2, 4.6):
        loc, n = on_surface((x, side * 6, 0.46), (0, -side, 0), 0.006)
        if loc is not None:
            pb.box((0.08, 0.016, 0.04), (x, loc.y, 0.46), "P3_LensAmber", bevel=0.006)
    loc, n = on_surface((3.25, side * 6, 1.45), (0, -side, 0), 0.003)
    if loc is not None:                                                         # unit numbers by the cab
        bpy.ops.object.text_add(location=(3.25, loc.y + side * 0.002, 1.32))
        t = bpy.context.active_object
        t.data.body = "BCF 07"
        t.data.size = 0.2
        t.data.extrude = 0.002
        t.data.align_x = "CENTER"
        t.rotation_euler = (math.radians(90), 0, 0 if side < 0 else math.radians(180))
        bpy.ops.object.convert(target="MESH")
        pb._finish(bpy.context.active_object, "P3_Navy", 0, 0)
# rear: tail clusters, louvres, caution plate
RX = -5.47 * SX
for side in (1, -1):
    loc, n = on_surface((RX - 3, side * 0.92, 0.95), (1, 0, 0), 0.006)
    if loc is not None:
        pb.box((0.012, 0.22, 0.52), (loc.x, side * 0.92, 1.0), "P3_Chrome", bevel=0.01)
        for j, (mat, z) in enumerate((("P3_LensRed", 1.17), ("P3_LensAmber", 1.0), ("P3_LensRed", 0.83))):
            pb.cyl(0.07, 0.02, (loc.x - 0.012, side * 0.92, z), mat, rot=(0, 90, 0), verts=32, bevel=0.01)
loc, n = on_surface((RX - 3, 0, 0.95), (1, 0, 0), 0.006)
if loc is not None:
    pb.box((0.012, 1.1, 0.46), (loc.x, 0, 0.95), "P3_PaintSteelDark", bevel=0.008)
    for i in range(9):
        pb.box((0.02, 1.04, 0.022), (loc.x - 0.012, 0, 0.75 + i * 0.05), "P3_PaintSteelGrey", rot=(0, 20, 0), bevel=0.002, segs=1)
loc, n = on_surface((RX - 3, 0, 1.45), (1, 0, 0), 0.004)
if loc is not None:
    pb.box((0.006, 1.2, 0.14), (loc.x, 0, 1.45), "P3_PaintYellow", bevel=0.003)
    bpy.ops.object.text_add(location=(loc.x - 0.005, 0, 1.415))
    t = bpy.context.active_object
    t.data.body = "CORRECTIONS VEHICLE  -  DO NOT FOLLOW"
    t.data.size = 0.075
    t.data.align_x = "CENTER"
    t.data.extrude = 0.001
    t.rotation_euler = (math.radians(90), 0, math.radians(-90))
    bpy.ops.object.convert(target="MESH")
    pb._finish(bpy.context.active_object, "P3_PaintSteelDark", 0, 0)
# prisoner cage partition behind the driver: steel frame, vertical bars, barred aisle door (security transport)
CX = 3.95
floor_hit, _ = hit((CX, 0, 2.2), (0, 0, -1))
ceil_hit, _ = hit((CX, 0, 1.6), (0, 0, 1))
wall_l, _ = hit((CX, 0, 1.8), (0, 1, 0))
wall_r, _ = hit((CX, 0, 1.8), (0, -1, 0))
if floor_hit is not None and ceil_hit is not None and wall_l is not None and wall_r is not None:
    fz, cz, yl, yr = floor_hit.z, ceil_hit.z, wall_l.y - 0.02, wall_r.y + 0.02
    h = cz - fz
    for y in (yl, yr, 0.42, -0.42):
        pb.box((0.05, 0.05, h), (CX, y, fz + h / 2), "P3_PaintSteelDark", bevel=0.006)
    for z in (fz + 0.08, fz + h * 0.5, cz - 0.06):
        pb.box((0.05, yl - yr, 0.05), (CX, (yl + yr) / 2, z), "P3_PaintSteelDark", bevel=0.006)
    y = yr + 0.09
    while y < yl - 0.05:
        if abs(y) > 0.44:
            pb.cyl(0.011, h - 0.1, (CX, y, fz + h / 2), "P3_PaintSteelDark", verts=8, bevel=0)
        y += 0.1
    for i in range(7):                                                       # aisle door bars (closed)
        pb.cyl(0.011, h - 0.24, (CX - 0.03, -0.36 + i * 0.12, fz + h / 2 - 0.02), "P3_PaintSteelDark", verts=8, bevel=0)
    pb.box((0.04, 0.10, 0.16), (CX - 0.06, 0.36, fz + 1.05), "P3_Chrome", bevel=0.01)   # lock box
    print("CAGE", round(fz, 2), round(cz, 2), round(yl, 2), round(yr, 2))

# roof: A/C unit with fan grilles, hatches, antennas, unit number for aerial identification
ROOF = 2.708 * SZ
pb.box((2.4, 1.5, 0.24), (0.6, 0, ROOF + 0.12), "P3_BusPaint", bevel=0.05, segs=3)
for x in (0.0, 1.2):
    pb.cyl(0.26, 0.02, (x, 0, ROOF + 0.245), "P3_PaintSteelDark", verts=32)
    for i in range(6):
        pb.box((0.5, 0.012, 0.012), (x, 0, ROOF + 0.258), "P3_PaintSteelGrey", rot=(0, 0, i * 30), bevel=0)
for x in (-3.4, 3.2):
    pb.box((0.7, 0.7, 0.06), (x, 0, ROOF + 0.03), "P3_PlasticGrey", bevel=0.02, segs=2)
for x, y in ((4.6, 0.6), (-4.8, -0.5)):
    pb.cyl(0.03, 0.03, (x, y, ROOF + 0.015), "P3_PaintSteelDark", verts=12)
    pb.cyl(0.005, 0.5, (x, y, ROOF + 0.27), "P3_PaintSteelDark", verts=6)
# (roof unit number removed: the flat lettering showed through the cabin ceiling from inside)

bpy.ops.object.select_all(action="DESELECT")
for o in pb.PARTS:
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for mod in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.context.view_layer.objects.active = pb.PARTS[0]
bpy.ops.object.join()
detail = bpy.context.active_object
detail.name = "Blackridge exterior detail"
try:
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35), keep_sharp_edges=True)
except Exception:
    pass

out = os.path.join(ROOT, "assets/props/phase03/blackridge_transport_bus_p03.glb")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_apply=True, export_yup=True, use_selection=True)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in objs)
print("BUS_OUT", out, "size", tuple(round(v, 2) for v in hi - lo), "tris", tris, "objects", [o.name for o in objs])

if RENDER:
    scn = bpy.context.scene
    scn.render.engine = "BLENDER_EEVEE"
    scn.render.resolution_x, scn.render.resolution_y = 1100, 620
    w = bpy.data.worlds.new("w"); scn.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.62, 0.7, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.8
    bpy.ops.object.light_add(type="SUN"); s = bpy.context.active_object; s.rotation_euler = (0.9, 0.2, 2.2); s.data.energy = 4
    ctr = (lo + hi) / 2
    for nm, p in {"front34": Vector((hi.x + 5, lo.y - 5, 2.2)), "rear34": Vector((lo.x - 5, hi.y + 5, 2.4)),
                  "kerb": Vector((ctr.x, hi.y + 11, 1.8)), "wheel": Vector((FRONT_X + 1.2, hi.y + 2.2, 0.9))}.items():
        bpy.ops.object.camera_add(location=p); c = bpy.context.active_object
        tgt = ctr if nm != "wheel" else Vector((FRONT_X, BODY_HALF, WHEEL_Z))
        c.rotation_euler = (tgt - p).to_track_quat("-Z", "Y").to_euler(); scn.camera = c
        c.data.lens = 35
        scn.render.filepath = os.path.join(RENDER, f"bus_p03_{nm}.png")
        bpy.ops.render.render(write_still=True)

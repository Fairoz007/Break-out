"""Phase 03 hard-surface prop rebuild (Blender 5.1, run headless).

Replaces the Phase 01.5 primitive machinery with detailed, bevelled, real-scale geometry while keeping each
asset's file name, origin (floor centre) and Godot footprint, so mission colliders, anchors and navigation stay
valid. Surfaces carry P3_* material slots; Godot binds them to the curated PBR set in EnvBuilder.p3_material().

    blender -b --factory-startup --python tools/phase03_props_build.py -- <out_dir> [name,name,...] [--render <dir>]

Axis note: Blender -Y is the Godot +Z ("front") side after glTF export.
"""
import bpy, bmesh, math, os, sys, json
from mathutils import Vector, Matrix

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(ARGS[0] if ARGS else ".")
ONLY = ARGS[1].split(",") if len(ARGS) > 1 and not ARGS[1].startswith("--") else []
RENDER = os.path.abspath(ARGS[ARGS.index("--render") + 1]) if "--render" in ARGS else ""

# name: (base colour, metallic, roughness, extra)
MATS = {
    "P3_Stainless": ((0.62, 0.63, 0.64), 1.0, 0.32, {}),
    "P3_PaintSteelGrey": ((0.42, 0.44, 0.45), 0.0, 0.48, {}),
    "P3_PaintSteelDark": ((0.10, 0.11, 0.12), 0.0, 0.55, {}),
    "P3_PaintSage": ((0.38, 0.45, 0.41), 0.0, 0.5, {}),
    "P3_PaintBlue": ((0.07, 0.20, 0.36), 0.0, 0.45, {}),
    "P3_PaintGreen": ((0.10, 0.27, 0.20), 0.0, 0.45, {}),
    "P3_PaintYellow": ((0.78, 0.55, 0.04), 0.0, 0.5, {}),
    "P3_PaintRed": ((0.55, 0.05, 0.04), 0.0, 0.45, {}),
    "P3_PaintBeige": ((0.58, 0.55, 0.47), 0.0, 0.5, {}),
    "P3_CastIron": ((0.16, 0.17, 0.18), 0.8, 0.62, {}),
    "P3_Chrome": ((0.8, 0.8, 0.8), 1.0, 0.12, {}),
    "P3_Brass": ((0.72, 0.52, 0.22), 1.0, 0.35, {}),
    "P3_Rubber": ((0.025, 0.025, 0.025), 0.0, 0.85, {}),
    "P3_PlasticDark": ((0.04, 0.045, 0.05), 0.0, 0.42, {}),
    "P3_PlasticGrey": ((0.32, 0.33, 0.34), 0.0, 0.4, {}),
    "P3_Glass": ((0.55, 0.62, 0.62), 0.0, 0.05, {"alpha": 0.28}),
    "P3_Screen": ((0.02, 0.05, 0.03), 0.0, 0.2, {"emit": (0.2, 0.75, 0.35), "strength": 2.0}),
    "P3_ScreenBlue": ((0.02, 0.03, 0.06), 0.0, 0.2, {"emit": (0.35, 0.55, 0.9), "strength": 1.5}),
    "P3_LampAmber": ((0.6, 0.35, 0.05), 0.0, 0.3, {"emit": (1.0, 0.55, 0.1), "strength": 1.2}),
    "P3_LampGreen": ((0.05, 0.4, 0.1), 0.0, 0.3, {"emit": (0.2, 1.0, 0.3), "strength": 1.2}),
    "P3_Laminate": ((0.55, 0.56, 0.55), 0.0, 0.38, {}),
    "P3_LaminateWood": ((0.42, 0.30, 0.20), 0.0, 0.45, {}),
    "P3_Concrete": ((0.48, 0.47, 0.45), 0.0, 0.9, {}),
    "P3_LabelWhite": ((0.82, 0.82, 0.78), 0.0, 0.5, {}),
    "P3_Fabric": ((0.62, 0.62, 0.58), 0.0, 0.95, {}),
    "P3_Paper": ((0.85, 0.84, 0.80), 0.0, 0.9, {}),
}


def material(name):
    m = bpy.data.materials.get(name)
    if m:
        return m
    col, met, rough, extra = MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*col, 1.0)
    p.inputs["Metallic"].default_value = met
    p.inputs["Roughness"].default_value = rough
    if "alpha" in extra:
        p.inputs["Alpha"].default_value = extra["alpha"]
        m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    if "emit" in extra:
        p.inputs["Emission Color"].default_value = (*extra["emit"], 1.0)
        p.inputs["Emission Strength"].default_value = extra["strength"]
    return m


PARTS = []


def _finish(obj, mat, bevel, segs):
    obj.data.materials.clear()
    obj.data.materials.append(material(mat))
    if bevel > 0:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = segs
        mod.limit_method = "ANGLE"
        mod.angle_limit = math.radians(40)
        mod.harden_normals = True
    PARTS.append(obj)
    return obj


def _place(obj, loc, rot):
    obj.location = Vector(loc)
    obj.rotation_euler = [math.radians(a) for a in rot]


def box(size, loc, mat, rot=(0, 0, 0), bevel=0.004, segs=2):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.active_object
    o.scale = size
    _place(o, loc, rot)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, mat, bevel, segs)


def cyl(r, depth, loc, mat, rot=(0, 0, 0), verts=32, bevel=0.003, segs=2, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=depth, vertices=verts)
    o = bpy.context.active_object
    _place(o, loc, rot)
    return _finish(o, mat, bevel, segs)


def torus(R, r, loc, mat, rot=(0, 0, 0), maj=48, mino=12):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=maj, minor_segments=mino)
    o = bpy.context.active_object
    _place(o, loc, rot)
    return _finish(o, mat, 0, 0)


def sphere(r, loc, mat, scale=(1, 1, 1), segs=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=segs, ring_count=segs // 2)
    o = bpy.context.active_object
    o.location = Vector(loc)
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, mat, 0, 0)


def tube(points, r, mat, verts=16):
    """Pipe through 3D points with straight runs (elbows are small spheres)."""
    for a, b in zip(points[:-1], points[1:]):
        a, b = Vector(a), Vector(b)
        d = b - a
        o_len = d.length
        mid = (a + b) / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=o_len, vertices=verts)
        o = bpy.context.active_object
        o.location = mid
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
        _finish(o, mat, 0, 0)
    for p in points[1:-1]:
        sphere(r * 1.02, p, mat, segs=16)


def flange(r, thick, loc, axis_rot, mat_f, bolts=8, bolt_r=0.008):
    cyl(r, thick, loc, mat_f, rot=axis_rot, verts=40, bevel=0.002)
    # bolt heads on the flange face, built in local space then rotated
    rx, ry, rz = [math.radians(a) for a in axis_rot]
    m = Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y") @ Matrix.Rotation(rx, 4, "X")
    for i in range(bolts):
        ang = 2 * math.pi * i / bolts
        local = Vector((math.cos(ang) * r * 0.78, math.sin(ang) * r * 0.78, thick / 2 + 0.006))
        cyl(bolt_r * 1.6, 0.012, Vector(loc) + m @ local, "P3_Chrome", rot=axis_rot, verts=6, bevel=0.001)


def screws(points, mat="P3_Chrome", r=0.006, rot=(90, 0, 0)):
    for p in points:
        cyl(r, 0.006, p, mat, rot=rot, verts=10, bevel=0.0015, segs=1)


def louvres(x0, x1, z0, z1, y, n, mat, depth=0.012):
    step = (z1 - z0) / n
    for i in range(n):
        z = z0 + step * (i + 0.5)
        box(((x1 - x0), depth, step * 0.35), (0.5 * (x0 + x1), y, z), mat, rot=(25, 0, 0), bevel=0.001, segs=1)


def finalize(name):
    """Apply modifiers, smooth by angle, join to one multi-material object and export."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in PARTS:
        o.select_set(True)
    bpy.context.view_layer.objects.active = PARTS[0]
    for o in PARTS:
        bpy.context.view_layer.objects.active = o
        for m in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.context.view_layer.objects.active = PARTS[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35), keep_sharp_edges=True)
    except Exception:
        bpy.ops.object.shade_smooth()
    # UVs for any authored texture usage downstream (Godot uses object triplanar on P3 materials)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.cube_project(cube_size=1.0)
    bpy.ops.object.mode_set(mode="OBJECT")
    tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    path = os.path.join(OUT, name + ".glb")
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_apply=True, export_yup=True,
                              use_selection=True, export_materials="EXPORT")
    bb = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mn = Vector(map(min, *bb)); mx = Vector(map(max, *bb))
    info = {"name": name, "tris": tris, "materials": [m.name for m in obj.data.materials],
            "godot_bounds": {"x": [round(mn.x, 3), round(mx.x, 3)], "y": [round(mn.z, 3), round(mx.z, 3)],
                             "z": [round(-mx.y, 3), round(-mn.y, 3)]}, "path": path}
    print("PROP " + json.dumps(info))
    return obj, info


# ----------------------------------------------------------------------------------------------- models

def washer():
    """Front-loading industrial washer-extractor (approx. 25 kg class), 1.0 W x 1.2 H x 0.94 D."""
    W, D = 0.96, 0.86
    yF = -D / 2
    # base frame and anchor feet
    box((W + 0.02, D + 0.02, 0.10), (0, 0, 0.05), "P3_PaintSteelDark", bevel=0.006)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(0.035, 0.02, (sx * 0.43, sy * 0.38, 0.01), "P3_PaintSteelDark", verts=16)
            cyl(0.012, 0.03, (sx * 0.43, sy * 0.38, 0.03), "P3_Chrome", verts=6)
    # cabinet: brushed stainless shell with separate front/side panels and seams
    box((W, D - 0.02, 0.95), (0, 0.01, 0.575), "P3_Stainless", bevel=0.008, segs=3)
    box((W + 0.012, 0.02, 0.62), (0, yF - 0.004, 0.43), "P3_Stainless", bevel=0.004)          # front lower panel
    box((W - 0.04, 0.006, 0.004), (0, yF - 0.016, 0.745), "P3_PaintSteelDark", bevel=0)       # panel seam
    for sx in (-1, 1):
        box((0.004, D - 0.08, 0.004), (sx * (W / 2 + 0.001), 0.0, 0.5), "P3_PaintSteelDark", bevel=0)
    # top cover, slightly overhanging, painted
    box((W + 0.03, D + 0.01, 0.05), (0, 0.0, 1.075), "P3_PaintSteelGrey", bevel=0.01, segs=3)
    # control console: angled facia across the upper front
    box((W, 0.16, 0.20), (0, yF + 0.03, 0.95), "P3_PaintSteelGrey", rot=(-12, 0, 0), bevel=0.008, segs=3)
    box((0.36, 0.01, 0.12), (-0.22, yF - 0.035, 0.955), "P3_PlasticDark", rot=(-12, 0, 0), bevel=0.003)
    box((0.14, 0.006, 0.06), (-0.26, yF - 0.042, 0.965), "P3_Screen", rot=(-12, 0, 0), bevel=0)
    for i in range(4):
        cyl(0.012, 0.012, (-0.12 + i * 0.0, yF - 0.044, 0.93 + 0.0), "P3_PlasticGrey", rot=(78, 0, 0), verts=16) if False else None
    for i, mat in enumerate(["P3_PlasticGrey", "P3_PlasticGrey", "P3_LampGreen", "P3_PlasticGrey", "P3_LampAmber"]):
        cyl(0.013, 0.014, (-0.12 + i * 0.045, yF - 0.042, 0.94), mat, rot=(78, 0, 0), verts=20)
    # emergency stop: yellow collar + red mushroom
    cyl(0.04, 0.012, (0.36, yF - 0.04, 0.955), "P3_PaintYellow", rot=(78, 0, 0), verts=32)
    cyl(0.027, 0.03, (0.36, yF - 0.058, 0.957), "P3_PaintRed", rot=(78, 0, 0), verts=32, bevel=0.008, segs=3)
    cyl(0.012, 0.02, (0.25, yF - 0.045, 0.955), "P3_Chrome", rot=(78, 0, 0), verts=16)      # key switch
    box((0.11, 0.004, 0.035), (0.11, yF - 0.044, 0.985), "P3_LabelWhite", rot=(-12, 0, 0), bevel=0)
    # door: bezel, chrome ring, rubber gasket, domed glass and visible drum
    dz, dr = 0.52, 0.215
    cyl(dr + 0.06, 0.03, (0, yF - 0.02, dz), "P3_Stainless", rot=(90, 0, 0), verts=64, bevel=0.01, segs=3)
    torus(dr + 0.035, 0.022, (0, yF - 0.045, dz), "P3_Chrome", rot=(90, 0, 0), maj=64, mino=16)
    torus(dr - 0.005, 0.016, (0, yF - 0.04, dz), "P3_Rubber", rot=(90, 0, 0), maj=64, mino=12)
    sphere(dr, (0, yF + 0.04, dz), "P3_Glass", scale=(1, 0.28, 1), segs=48)
    cyl(dr - 0.01, 0.30, (0, yF + 0.17, dz), "P3_Stainless", rot=(90, 0, 0), verts=48, bevel=0)
    cyl(dr - 0.03, 0.01, (0, yF + 0.32, dz), "P3_PaintSteelDark", rot=(90, 0, 0), verts=48, bevel=0)
    for i in range(3):                                                                      # drum lifters
        a = 2 * math.pi * i / 3
        box((0.03, 0.26, 0.03), (math.cos(a) * 0.17, yF + 0.17, dz + math.sin(a) * 0.17), "P3_Stainless", rot=(0, -math.degrees(a), 0))
    # hinge block (left) and latch handle (right)
    box((0.06, 0.06, 0.22), (-dr - 0.07, yF - 0.04, dz), "P3_Chrome", bevel=0.01, segs=3)
    for z in (dz - 0.07, dz + 0.07):
        cyl(0.018, 0.07, (-dr - 0.07, yF - 0.04, z), "P3_Chrome", verts=20)
    box((0.05, 0.05, 0.14), (dr + 0.075, yF - 0.06, dz), "P3_PlasticDark", bevel=0.012, segs=3)
    # lower service panel with screws and louvres
    box((0.74, 0.008, 0.16), (0, yF - 0.016, 0.20), "P3_Stainless", bevel=0.003)
    louvres(-0.30, 0.30, 0.14, 0.26, yF - 0.024, 6, "P3_PaintSteelDark")
    screws([(sx * 0.35, yF - 0.022, z) for sx in (-1, 1) for z in (0.14, 0.26)])
    box((0.10, 0.004, 0.06), (0.30, yF - 0.016, 0.72), "P3_LabelWhite", bevel=0)              # data plate
    # chemical inlet box on top and rear services
    box((0.24, 0.16, 0.08), (-0.30, 0.22, 1.14), "P3_PlasticGrey", bevel=0.01, segs=3)
    box((0.22, 0.14, 0.012), (-0.30, 0.22, 1.186), "P3_PlasticDark", bevel=0.004)
    for i, mat in enumerate(["P3_PaintBlue", "P3_PaintRed"]):
        x = 0.20 + i * 0.14
        tube([(x, D / 2 - 0.02, 0.95), (x, D / 2 + 0.06, 0.95), (x, D / 2 + 0.06, 1.18)], 0.016, "P3_Chrome")
        cyl(0.03, 0.04, (x, D / 2 + 0.06, 1.05), "P3_Brass", verts=16)
        cyl(0.035, 0.008, (x, D / 2 + 0.06, 1.09), mat, verts=24)                             # valve handwheel
    tube([(-0.25, D / 2 - 0.02, 0.18), (-0.25, D / 2 + 0.08, 0.18), (-0.25, D / 2 + 0.08, 0.0)], 0.04, "P3_PlasticGrey")
    return finalize("laundry_washer")


def press():
    """Steam utility garment press (scissor-head type), operator side facing Godot -Z (Blender +Y)."""
    yO = 0.42           # operator side (Blender +Y)
    # cabinet base with access door, kick recess and side panels
    box((1.50, 0.80, 0.82), (0, 0, 0.47), "P3_PaintSage", bevel=0.012, segs=3)
    box((1.46, 0.74, 0.06), (0, 0, 0.03), "P3_PaintSteelDark", bevel=0.004)
    box((1.36, 0.02, 0.10), (0, yO - 0.035, 0.11), "P3_PaintSteelDark", bevel=0.003)        # kick recess shadow
    box((0.62, 0.012, 0.50), (-0.38, yO - 0.012, 0.50), "P3_PaintSage", bevel=0.006)          # access doors
    box((0.62, 0.012, 0.50), (0.38, yO - 0.012, 0.50), "P3_PaintSage", bevel=0.006)
    for x in (-0.12, 0.12):
        box((0.018, 0.03, 0.12), (x, yO + 0.0, 0.55), "P3_Chrome", bevel=0.006)
    louvres(-0.62, -0.14, 0.32, 0.46, yO - 0.002, 5, "P3_PaintSteelDark")
    box((0.18, 0.004, 0.08), (0.45, yO - 0.004, 0.70), "P3_LabelWhite", bevel=0)
    # buck (lower padded board) on support pedestal
    box((0.30, 0.30, 0.18), (0, 0.05, 0.97), "P3_CastIron", bevel=0.02, segs=3)
    box((1.32, 0.50, 0.06), (0, 0.12, 1.09), "P3_Stainless", bevel=0.02, segs=4)
    box((1.30, 0.48, 0.05), (0, 0.12, 1.135), "P3_Fabric", bevel=0.022, segs=4)              # padded cover
    # head (upper heated plate) on scissor arms, open position
    hz = 1.48
    box((1.30, 0.46, 0.08), (0, 0.10, hz), "P3_Stainless", rot=(-14, 0, 0), bevel=0.02, segs=4)
    box((1.20, 0.30, 0.10), (0, 0.06, hz + 0.08), "P3_PaintSage", rot=(-14, 0, 0), bevel=0.02, segs=3)
    for x in (-0.48, 0.48):
        box((0.06, 0.06, 0.70), (x, -0.22, 1.25), "P3_CastIron", rot=(18, 0, 0), bevel=0.01)
        cyl(0.045, 0.08, (x, -0.33, 0.93), "P3_Chrome", rot=(0, 90, 0), verts=24)
        cyl(0.04, 0.08, (x, -0.10, 1.55), "P3_Chrome", rot=(0, 90, 0), verts=24)
    # operating handle bar across the head front + twin palm buttons
    tube([(-0.55, yO - 0.05, hz - 0.02), (-0.55, yO + 0.03, hz - 0.02), (0.55, yO + 0.03, hz - 0.02), (0.55, yO - 0.05, hz - 0.02)], 0.016, "P3_Chrome")
    for x in (-0.72, 0.72):
        box((0.12, 0.12, 0.10), (x, yO - 0.10, 0.92), "P3_PaintYellow", bevel=0.012, segs=3)
        cyl(0.035, 0.03, (x, yO - 0.10, 0.985), "P3_PaintGreen" if x < 0 else "P3_PaintRed", verts=24, bevel=0.008)
    # foot pedal
    box((0.36, 0.20, 0.03), (0, yO + 0.10, 0.06), "P3_CastIron", rot=(10, 0, 0), bevel=0.006)
    box((0.03, 0.12, 0.12), (0, yO + 0.0, 0.11), "P3_CastIron", bevel=0.004)
    # steam supply: riser pipes with valve handwheel, pressure gauge and trap at the rear
    tube([(0.55, -0.40, 0.70), (0.55, -0.50, 0.70), (0.55, -0.50, 2.05)], 0.022, "P3_PaintSteelGrey")
    tube([(-0.55, -0.40, 0.25), (-0.55, -0.50, 0.25), (-0.55, -0.50, 2.05)], 0.018, "P3_PaintSteelGrey")
    tube([(-0.55, -0.50, 2.05), (0.55, -0.50, 2.05)], 0.026, "P3_PaintSteelGrey")
    tube([(0.0, -0.50, 2.05), (0.0, -0.62, 2.05)], 0.03, "P3_PaintSteelGrey")
    for x in (-0.55, 0.0, 0.55):
        sphere(0.034, (x, -0.50, 2.05), "P3_PaintSteelGrey", segs=16)
    cyl(0.04, 0.10, (0.55, -0.50, 1.35), "P3_Brass", verts=20)
    torus(0.07, 0.009, (0.55, -0.50, 1.43), "P3_PaintRed", maj=32, mino=8)
    for a in range(0, 360, 90):
        box((0.13, 0.008, 0.008), (0.55, -0.50, 1.43), "P3_PaintRed", rot=(0, 0, a / 2.0), bevel=0)
    cyl(0.055, 0.03, (0.55, -0.44, 1.75), "P3_Chrome", rot=(90, 0, 0), verts=32)
    cyl(0.047, 0.004, (0.55, -0.424, 1.75), "P3_LabelWhite", rot=(90, 0, 0), verts=32, bevel=0)
    box((0.004, 0.002, 0.035), (0.55, -0.42, 1.76), "P3_PaintSteelDark", rot=(0, 35, 0), bevel=0)
    cyl(0.06, 0.12, (-0.55, -0.50, 0.40), "P3_CastIron", verts=20)                             # steam trap
    # control box with indicator lamps on the right side
    box((0.18, 0.12, 0.26), (0.84, 0.02, 1.0), "P3_PaintSteelGrey", bevel=0.01, segs=3)
    for i, mat in enumerate(["P3_LampGreen", "P3_LampAmber"]):
        cyl(0.012, 0.014, (0.935, -0.02 + i * 0.06, 1.05), mat, rot=(0, 90, 0), verts=16)
    cyl(0.025, 0.02, (0.935, 0.02, 0.94), "P3_PlasticDark", rot=(0, 90, 0), verts=20)
    tube([(0.84, 0.02, 0.87), (0.84, 0.02, 0.80), (0.75, 0.02, 0.80)], 0.012, "P3_PlasticDark")
    return finalize("laundry_press")


def pump():
    """End-suction centrifugal pump set: motor, coupling guard, volute, valves, on a steel skid and plinth."""
    # concrete plinth and fabricated base frame
    box((2.30, 0.92, 0.14), (0.10, 0, 0.07), "P3_Concrete", bevel=0.02, segs=2)
    box((2.10, 0.70, 0.12), (0.10, 0, 0.20), "P3_PaintBlue", bevel=0.006)
    box((2.06, 0.66, 0.02), (0.10, 0, 0.265), "P3_PaintSteelDark", bevel=0.002)
    screws([(x, y, 0.278) for x in (-0.85, -0.25, 0.45, 1.05) for y in (-0.28, 0.28)], r=0.014, rot=(0, 0, 0))
    # motor (+X side): finned frame, feet, fan cowl, terminal box
    mx0, mx1, mz, mr = 0.20, 1.10, 0.56, 0.21
    cyl(mr, mx1 - mx0, ((mx0 + mx1) / 2, 0, mz), "P3_PaintSteelGrey", rot=(0, 90, 0), verts=48, bevel=0.01)
    for i in range(14):
        a = 2 * math.pi * i / 14
        if abs(math.sin(a)) > 0.92 and math.cos(a) < 0:
            continue
        box((mx1 - mx0 - 0.10, 0.012, 0.035), ((mx0 + mx1) / 2, math.cos(a) * (mr + 0.012), mz + math.sin(a) * (mr + 0.012)),
            "P3_PaintSteelGrey", rot=(math.degrees(a) + 90, 0, 0), bevel=0.002)
    for x in (mx0 + 0.15, mx1 - 0.15):
        box((0.10, 0.44, 0.08), (x, 0, 0.32), "P3_PaintSteelGrey", bevel=0.006)
    cyl(mr + 0.02, 0.06, (mx0 + 0.02, 0, mz), "P3_PaintSteelGrey", rot=(0, 90, 0), verts=48, bevel=0.008)
    cyl(mr + 0.025, 0.20, (mx1 + 0.08, 0, mz), "P3_PaintSteelGrey", rot=(0, 90, 0), verts=48, bevel=0.01, r2=None)
    for i in range(7):
        torus(0.04 + i * 0.028, 0.004, (mx1 + 0.185, 0, mz), "P3_PaintSteelDark", rot=(0, 90, 0), maj=40, mino=6)
    box((0.20, 0.18, 0.12), ((mx0 + mx1) / 2, 0, mz + mr + 0.06), "P3_PaintSteelGrey", bevel=0.01, segs=3)
    cyl(0.025, 0.05, ((mx0 + mx1) / 2 + 0.12, 0, mz + mr + 0.06), "P3_Brass", rot=(0, 90, 0), verts=12)
    tube([((mx0 + mx1) / 2 + 0.15, 0, mz + mr + 0.06), ((mx0 + mx1) / 2 + 0.15, 0.30, mz + mr + 0.06), ((mx0 + mx1) / 2 + 0.15, 0.30, 0.27)], 0.014, "P3_PaintSteelDark")
    box((0.12, 0.004, 0.06), ((mx0 + mx1) / 2, -mr - 0.03, mz + 0.05), "P3_LabelWhite", bevel=0)
    # coupling guard (yellow safety cover)
    box((0.36, 0.30, 0.26), (0.0, 0, mz), "P3_PaintYellow", bevel=0.05, segs=4)
    box((0.30, 0.31, 0.02), (0.0, 0, mz + 0.03), "P3_PaintSteelDark", bevel=0)
    # pump bearing frame, volute casing and nozzles (-X side)
    cyl(0.10, 0.30, (-0.35, 0, mz), "P3_CastIron", rot=(0, 90, 0), verts=32, bevel=0.01)
    box((0.12, 0.30, 0.26), (-0.35, 0, 0.36), "P3_CastIron", bevel=0.01)
    cyl(0.30, 0.22, (-0.66, 0, mz + 0.04), "P3_PaintGreen", rot=(0, 90, 0), verts=56, bevel=0.03, segs=3)
    cyl(0.25, 0.10, (-0.80, 0, mz + 0.02), "P3_PaintGreen", rot=(0, 90, 0), verts=48, bevel=0.02)
    for i in range(10):                                                                     # casing bolts
        a = 2 * math.pi * i / 10
        cyl(0.012, 0.03, (-0.545, math.cos(a) * 0.27, mz + 0.04 + math.sin(a) * 0.27), "P3_Chrome", rot=(0, 90, 0), verts=6)
    # suction (axial, -X) with flange to a horizontal pipe leaving the skid
    cyl(0.10, 0.20, (-0.95, 0, mz), "P3_PaintGreen", rot=(0, 90, 0), verts=32)
    flange(0.16, 0.03, (-1.05, 0, mz), (0, 90, 0), "P3_PaintGreen")
    cyl(0.10, 0.06, (-1.09, 0, mz), "P3_PaintSteelGrey", rot=(0, 90, 0), verts=32)
    # discharge (vertical) with gate valve, handwheel and gauge up to the ceiling header
    cyl(0.075, 0.20, (-0.66, 0, mz + 0.40), "P3_PaintGreen", verts=32)
    flange(0.13, 0.03, (-0.66, 0, mz + 0.51), (0, 0, 0), "P3_PaintGreen")
    cyl(0.12, 0.18, (-0.66, 0, mz + 0.64), "P3_CastIron", verts=8, bevel=0.01)                 # valve body
    flange(0.13, 0.03, (-0.66, 0, mz + 0.75), (0, 0, 0), "P3_PaintGreen")
    cyl(0.03, 0.18, (-0.66, 0.16, mz + 0.64), "P3_Chrome", rot=(90, 0, 0), verts=16)          # stem
    torus(0.10, 0.012, (-0.66, 0.26, mz + 0.64), "P3_PaintRed", rot=(90, 0, 0), maj=40, mino=8)
    for a in (0, 60, 120):
        box((0.20, 0.012, 0.012), (-0.66, 0.26, mz + 0.64), "P3_PaintRed", rot=(0, a, 0), bevel=0)
    cyl(0.075, 1.96 - (mz + 0.77), (-0.66, 0, (mz + 0.77 + 1.96) / 2), "P3_PaintSteelGrey", verts=32)
    tube([(-0.66, -0.07, mz + 0.86), (-0.66, -0.16, mz + 0.86)], 0.008, "P3_Brass")
    cyl(0.05, 0.03, (-0.66, -0.18, mz + 0.86), "P3_Chrome", rot=(90, 0, 0), verts=32)
    cyl(0.043, 0.004, (-0.66, -0.196, mz + 0.86), "P3_LabelWhite", rot=(90, 0, 0), verts=32, bevel=0)
    return finalize("pump_unit")


def counter():
    """Intake processing counter: officer side -Y? Model front (inmate side) is Blender -Y (Godot +Z)."""
    L, D = 2.40, 0.72
    # plinth / kick plate
    box((L - 0.04, D - 0.08, 0.10), (0, 0.02, 0.05), "P3_PaintSteelDark", bevel=0.004)
    box((L, 0.012, 0.10), (0, -D / 2 + 0.03, 0.05), "P3_Stainless", bevel=0.002)
    # carcass and front facade panels with shadow gaps
    box((L, D, 0.86), (0, 0, 0.53), "P3_PaintSage", bevel=0.006)
    for i in range(4):
        x = -L / 2 + L / 8 + i * L / 4
        box((L / 4 - 0.012, 0.016, 0.80), (x, -D / 2 - 0.006, 0.53), "P3_LaminateWood" if False else "P3_PaintBeige", bevel=0.004)
    # raised transaction ledge with stainless edge, worktop behind
    box((L + 0.04, 0.34, 0.035), (0, -D / 2 + 0.13, 1.08), "P3_Laminate", bevel=0.008, segs=3)
    box((L + 0.04, 0.012, 0.04), (0, -D / 2 - 0.035, 1.08), "P3_Stainless", bevel=0.003)
    box((0.04, 0.30, 0.13), (-L / 2 + 0.02, -D / 2 + 0.13, 1.0), "P3_PaintSage", bevel=0.004)
    box((0.04, 0.30, 0.13), (L / 2 - 0.02, -D / 2 + 0.13, 1.0), "P3_PaintSage", bevel=0.004)
    box((L, 0.40, 0.03), (0, 0.16, 0.975), "P3_Laminate", bevel=0.005)
    # pass-through tray slot and property tray recess in the ledge
    box((0.46, 0.30, 0.012), (0.0, -D / 2 + 0.13, 1.1), "P3_Stainless", bevel=0.002)
    # acrylic screen on stainless posts across the ledge
    for x in (-1.05, -0.36, 0.36, 1.05):
        cyl(0.012, 0.42, (x, -D / 2 + 0.24, 1.31), "P3_Stainless", verts=16)
    for x in (-0.705, 0.705):                                                                  # panes either side of the tray
        box((0.68, 0.008, 0.36), (x, -D / 2 + 0.24, 1.33), "P3_Glass", bevel=0.002)
    box((0.72, 0.03, 0.03), (0, -D / 2 + 0.24, 1.505), "P3_Stainless", bevel=0.004)            # header over pass-through
    # officer side: monitor, keyboard, mouse, document trays, desk phone
    mx = -0.55
    box((0.22, 0.16, 0.012), (mx, 0.20, 0.995), "P3_PlasticDark", bevel=0.004)
    box((0.04, 0.03, 0.30), (mx, 0.17, 1.14), "P3_PlasticDark", bevel=0.006)
    box((0.56, 0.035, 0.34), (mx, 0.20, 1.30), "P3_PlasticDark", rot=(8, 0, 0), bevel=0.01, segs=3)
    box((0.52, 0.004, 0.30), (mx, 0.219, 1.30), "P3_ScreenBlue", rot=(8, 0, 0), bevel=0)
    box((0.44, 0.15, 0.022), (mx, 0.33, 1.0), "P3_PlasticDark", rot=(-5, 0, 0), bevel=0.004)
    for r in range(4):
        for c in range(14):
            box((0.024, 0.024, 0.008), (mx - 0.19 + c * 0.029, 0.38 - r * 0.03, 1.013 + r * 0.0026), "P3_PlasticGrey", bevel=0.002, segs=1)
    box((0.06, 0.10, 0.03), (mx + 0.32, 0.32, 0.995), "P3_PlasticDark", bevel=0.012, segs=3)
    for i in range(3):
        box((0.26, 0.34, 0.008), (0.62, 0.17, 0.995 + i * 0.07), "P3_PlasticGrey", bevel=0.002)
        box((0.008, 0.34, 0.07), (0.49, 0.17, 1.03 + i * 0.07), "P3_PlasticGrey", bevel=0.001)
        box((0.008, 0.34, 0.07), (0.75, 0.17, 1.03 + i * 0.07), "P3_PlasticGrey", bevel=0.001)
        box((0.21, 0.29, 0.012), (0.62, 0.17, 1.005 + i * 0.07), "P3_Paper", bevel=0.001)
    box((0.18, 0.20, 0.06), (0.98, 0.15, 1.02), "P3_PlasticDark", rot=(10, 0, 0), bevel=0.012, segs=3)
    box((0.20, 0.05, 0.04), (0.98, 0.10, 1.07), "P3_PlasticDark", bevel=0.015, segs=3)
    # cable grommet and conduit drop at the rear
    cyl(0.03, 0.01, (mx, 0.10, 0.993), "P3_PlasticDark", verts=20)
    # Built with the ledge on -Y; the inmate side of the placed counter is Blender +Y, so turn it about Z.
    for o in PARTS:
        o.location = Matrix.Rotation(math.pi, 4, "Z") @ o.location
        o.rotation_euler.z += math.pi
    return finalize("intake_counter")


def locker():
    """Single steel locker 0.48 W x 1.80 H, louvred door, recessed handle, hasp, number plate."""
    W, D, H = 0.48, 0.50, 1.80
    yF = -D / 2
    box((W, D, 0.10), (0, 0.04, 0.05), "P3_PaintSteelDark", bevel=0.003)                      # plinth
    box((W, D, H - 0.10), (0, 0.04, 0.95), "P3_PaintBeige", bevel=0.004)                       # body
    box((W - 0.03, 0.02, H - 0.15), (0, yF + 0.025, 0.97), "P3_PaintBeige", bevel=0.006, segs=3)  # door
    box((W - 0.034, 0.004, 0.004), (0, yF + 0.012, 1.80), "P3_PaintSteelDark", bevel=0)
    for z0 in (1.42, 0.30):
        for i in range(6):
            box((0.26, 0.012, 0.010), (0, yF + 0.012, z0 + i * 0.03), "P3_PaintSteelDark", rot=(30, 0, 0), bevel=0.001, segs=1)
            box((0.27, 0.006, 0.006), (0, yF + 0.010, z0 + i * 0.03 + 0.008), "P3_PaintBeige", bevel=0.001, segs=1)
    box((0.05, 0.03, 0.14), (0.17, yF + 0.012, 1.05), "P3_PaintSteelDark", bevel=0.008, segs=2)  # handle recess
    box((0.03, 0.02, 0.10), (0.17, yF + 0.0, 1.05), "P3_Chrome", bevel=0.008, segs=2)
    box((0.025, 0.035, 0.015), (0.17, yF - 0.008, 0.98), "P3_Chrome", bevel=0.003)             # hasp
    torus(0.018, 0.004, (0.17, yF - 0.028, 0.965), "P3_Chrome", rot=(0, 90, 0), maj=20, mino=6)
    box((0.032, 0.014, 0.036), (0.17, yF - 0.028, 0.94), "P3_Brass", bevel=0.004)
    box((0.08, 0.004, 0.035), (0, yF + 0.012, 1.64), "P3_LabelWhite", bevel=0.0005)
    for z in (0.35, 0.95, 1.55):                                                               # hinge knuckles
        cyl(0.008, 0.06, (-W / 2 + 0.018, yF + 0.012, z), "P3_PaintBeige", verts=12)
    box((W, D + 0.02, 0.012), (0, 0.04, H + 0.006), "P3_PaintBeige", bevel=0.003)              # top lip
    return finalize("locker")


def razor_wire():
    """Concertina razor-wire coil, 2 m module along +X (Godot), 0.75 m diameter, galvanised, with barbs."""
    R, L, loops = 0.36, 2.0, 16
    segs = 20
    pts = []
    for i in range(loops * segs + 1):
        t = i / segs
        a = 2 * math.pi * t
        x = -L / 2 + L * i / (loops * segs)
        pts.append((x, math.cos(a) * R, R + 0.02 + math.sin(a) * R))
    # wire as a chain of short cylinders (one mesh, low radius); barbs every quarter turn
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = Vector(a), Vector(b)
        d = b - a
        bpy.ops.mesh.primitive_cylinder_add(radius=0.004, depth=d.length * 1.02, vertices=5)
        o = bpy.context.active_object
        o.location = (a + b) / 2
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
        _finish(o, "P3_Chrome", 0, 0)
    for i in range(0, len(pts), 5):
        p = Vector(pts[i])
        box((0.03, 0.004, 0.012), p, "P3_Chrome", rot=(0, 0, 35), bevel=0)
    # support stakes clamping the coil to the wall coping
    for x in (-0.9, 0.0, 0.9):
        box((0.02, 0.02, 0.10), (x, 0, 0.05), "P3_PaintSteelDark", bevel=0.002)
    return finalize("razor_wire_2m")


def floodlight_pole():
    """Galvanised 8 m yard lighting column on a concrete base, double arm, two LED floodlights."""
    cyl(0.25, 0.5, (0, 0, 0.25), "P3_Concrete", verts=24, bevel=0.02)
    box((0.36, 0.36, 0.02), (0, 0, 0.51), "P3_Stainless", bevel=0.004)
    screws([(sx * 0.14, sy * 0.14, 0.53) for sx in (-1, 1) for sy in (-1, 1)], r=0.016, rot=(0, 0, 0))
    cyl(0.09, 7.6, (0, 0, 0.52 + 3.8), "P3_Stainless", verts=24, r2=0.06)
    box((0.10, 0.06, 0.30), (0, -0.09, 1.4), "P3_Stainless", bevel=0.01)               # access door
    for side in (-1, 1):
        tube([(0, 0, 7.7), (side * 0.55, 0, 7.95)], 0.035, "P3_Stainless")
        box((0.42, 0.30, 0.08), (side * 0.75, -0.05, 7.92), "P3_PaintSteelDark", rot=(-25, 0, 0), bevel=0.012, segs=2)
        box((0.36, 0.005, 0.24), (side * 0.75, -0.21, 7.86), "P3_LabelWhite", rot=(-25 + 90, 0, 0), bevel=0)
        for i in range(6):
            box((0.40, 0.008, 0.06), (side * 0.75, 0.10 - i * 0.0, 7.98 + 0.0), "P3_PaintSteelDark", rot=(-25, 0, 0), bevel=0) if False else None
    tube([(0, 0.07, 1.0), (0, 0.07, 7.6)], 0.012, "P3_PaintSteelDark")                     # cable conduit
    return finalize("floodlight_pole")


def lint_screen():
    """Removable lint screen in its stainless frame (M03 W2), 0.70 x 0.55 m, 40 mm deep."""
    W, H = 0.70, 0.55
    for x in (-W / 2 + 0.02, W / 2 - 0.02):
        box((0.04, 0.04, H), (x, 0, 0), "P3_Stainless", bevel=0.004)
    for z in (-H / 2 + 0.02, H / 2 - 0.02):
        box((W, 0.04, 0.04), (0, 0, z), "P3_Stainless", bevel=0.004)
    n = 34
    for i in range(1, n):
        x = -W / 2 + W * i / n
        box((0.003, 0.006, H - 0.06), (x, 0, 0), "P3_PaintSteelGrey", bevel=0)
    for i in range(1, 24):
        z = -H / 2 + H * i / 24
        box((W - 0.06, 0.006, 0.003), (0, 0.004, z), "P3_PaintSteelGrey", bevel=0)
    for x in (-0.18, 0.18):
        tube([(x, 0, H / 2), (x, -0.05, H / 2 + 0.03), (x, -0.05, H / 2 + 0.06)], 0.008, "P3_PlasticDark")
    box((0.10, 0.004, 0.04), (0.25, -0.022, -0.2), "P3_LabelWhite", bevel=0)
    return finalize("lint_screen")


def isolator():
    """Press isolation switch (M03 lever W1): grey enclosure, yellow front plate, red rotary handle, ON/OFF marks,
    lock-off hasp and conduit. Origin at the floor; front faces Godot -Z (Blender +Y), like laundry_press."""
    yF = 0.12
    box((0.06, 0.06, 0.9), (0, -0.02, 0.45), "P3_PaintSteelGrey", bevel=0.006)             # mounting post
    box((0.36, 0.20, 0.46), (0, 0.02, 1.02), "P3_PaintSteelGrey", bevel=0.012, segs=3)     # enclosure
    box((0.30, 0.012, 0.36), (0, yF + 0.006, 1.03), "P3_PaintYellow", bevel=0.004)          # front plate
    screws([(sx * 0.13, yF + 0.014, 1.03 + sz * 0.16) for sx in (-1, 1) for sz in (-1, 1)], rot=(90, 0, 0))
    cyl(0.07, 0.03, (0, yF + 0.025, 1.06), "P3_PaintRed", rot=(90, 0, 0), verts=32, bevel=0.008)   # rotary boss
    box((0.05, 0.05, 0.22), (0, yF + 0.055, 1.06), "P3_PaintRed", rot=(0, 30, 0), bevel=0.015, segs=3)   # handle
    for txt, x in (("OFF", 0.09), ("ON", -0.09)):              # read from the front (+Y), OFF on the viewer's left
        bpy.ops.object.text_add(location=(x, yF + 0.013, 1.165))
        t = bpy.context.active_object
        t.data.body = txt
        t.data.size = 0.035
        t.data.align_x = "CENTER"
        t.data.extrude = 0.0006
        t.rotation_euler = (math.radians(90), 0, math.radians(180))
        bpy.ops.object.convert(target="MESH")
        _finish(bpy.context.active_object, "P3_PaintSteelDark", 0, 0)
    box((0.22, 0.004, 0.05), (0, yF + 0.013, 0.89), "P3_LabelWhite", bevel=0)
    box((0.03, 0.04, 0.012), (0.1, yF + 0.04, 0.95), "P3_Chrome", bevel=0.003)             # lock-off hasp
    torus(0.016, 0.004, (0.1, yF + 0.06, 0.93), "P3_Chrome", rot=(0, 90, 0), maj=20, mino=6)
    tube([(0, -0.08, 1.25), (0, -0.08, 1.55), (0, -0.3, 1.55)], 0.016, "P3_PaintSteelDark")    # conduit to the press
    return finalize("isolation_switch")


def hoop():
    """Outdoor prison-yard basketball unit (Phase 04). Origin = post base centre on the ground; Blender +X points from
    the post to the court (board face at x=2.73, rim centre at x=3.105, rim height 3.05 m, board 1.80 x 1.05 m
    centred at 3.40 m) — the same metric layout as prison_court.gd."""
    # concrete footing, base plate, anchor bolts
    box((0.62, 0.62, 0.10), (0, 0, 0.03), "P3_Concrete", bevel=0.03, segs=2)
    box((0.40, 0.40, 0.025), (0, 0, 0.09), "P3_PaintSteelDark", bevel=0.004)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(0.016, 0.06, (sx * 0.15, sy * 0.15, 0.13), "P3_Chrome", verts=8)
            cyl(0.028, 0.025, (sx * 0.15, sy * 0.15, 0.115), "P3_Chrome", verts=6, bevel=0.002)
    # square steel post with weld collar and gooseneck
    box((0.115, 0.115, 3.05), (0, 0, 0.1 + 1.525), "P3_PaintSteelDark", bevel=0.008)
    box((0.15, 0.15, 0.03), (0, 0, 0.12), "P3_PaintSteelDark", bevel=0.004)
    pts = []
    for i in range(9):                                   # quarter bend from vertical to horizontal, radius 0.55
        a = math.radians(90 * i / 8)
        pts.append((0.55 - math.cos(a) * 0.55, 0, 3.15 + math.sin(a) * 0.55))
    pts.append((1.9, 0, 3.70))
    for a_, b_ in zip(pts[:-1], pts[1:]):
        av, bv = Vector(a_), Vector(b_)
        d = bv - av
        bpy.ops.mesh.primitive_cube_add(size=1)
        o = bpy.context.active_object
        o.scale = (d.length + 0.02, 0.115, 0.115)
        o.location = (av + bv) / 2
        o.rotation_euler = (0, -math.atan2(d.z, d.x), 0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        _finish(o, "P3_PaintSteelDark", 0.006, 2)
    # board bracket: two braces from the arm to the board corners, gusset plate
    for y in (-0.42, 0.42):
        tube([(1.75, 0, 3.66), (2.70, y, 3.80)], 0.025, "P3_PaintSteelDark")
        tube([(1.90, 0, 3.70), (2.70, y, 3.02)], 0.022, "P3_PaintSteelDark")
    # perforated steel backboard: frame, face sheet with hole pattern, painted border and shooter's square
    BX = 2.72
    box((0.035, 1.80, 1.05), (BX, 0, 3.40), "P3_PaintSteelGrey", bevel=0.008, segs=2)
    box((0.06, 1.84, 0.05), (BX - 0.01, 0, 3.40 + 0.535), "P3_PaintSteelDark", bevel=0.006)
    box((0.06, 1.84, 0.05), (BX - 0.01, 0, 3.40 - 0.535), "P3_PaintSteelDark", bevel=0.006)
    for y in (-0.92, 0.92):
        box((0.06, 0.05, 1.10), (BX - 0.01, y, 3.40), "P3_PaintSteelDark", bevel=0.006)
    for iy in range(-16, 17):
        for iz in range(-9, 10):
            if abs(iy) % 2 == abs(iz) % 2:
                box((0.004, 0.022, 0.022), (BX + 0.018, iy * 0.05, 3.40 + iz * 0.05), "P3_PaintSteelDark", bevel=0)
    for y0, y1, z0, z1 in ((-0.875, 0.875, 3.90, 3.93), (-0.875, 0.875, 2.87, 2.90)):
        box((0.004, y1 - y0, z1 - z0), (BX + 0.02, (y0 + y1) / 2, (z0 + z1) / 2), "P3_LabelWhite", bevel=0)
    for y in (-0.875, 0.875):
        box((0.004, 0.03, 1.03), (BX + 0.02, y, 3.40), "P3_LabelWhite", bevel=0)
    for y in (-0.295, 0.295):
        box((0.005, 0.05, 0.45), (BX + 0.021, y, 3.275), "P3_LabelWhite", bevel=0)
    for z in (3.05, 3.50):
        box((0.005, 0.59, 0.05), (BX + 0.021, 0, z), "P3_LabelWhite", bevel=0)
    # spring-loaded rim mount and heavy-duty double rim
    box((0.03, 0.22, 0.16), (BX + 0.035, 0, 3.10), "P3_PaintRed", bevel=0.006)
    box((0.16, 0.12, 0.05), (BX + 0.13, 0, 3.035), "P3_PaintRed", bevel=0.006)
    cyl(0.03, 0.08, (BX + 0.10, 0, 3.09), "P3_Chrome", rot=(0, 90, 0), verts=16)
    RX = BX + 0.385
    torus(0.233, 0.009, (RX, 0, 3.05), "P3_PaintRed", maj=64, mino=10)
    torus(0.233, 0.009, (RX, 0, 3.03), "P3_PaintRed", maj=64, mino=10)
    for i in range(12):                                   # net hooks between the two rings
        a = 2 * math.pi * i / 12
        cyl(0.006, 0.03, (RX + math.cos(a) * 0.233, math.sin(a) * 0.233, 3.04), "P3_PaintRed", verts=6, bevel=0)
    # steel chain net: 12 chains of oval links tapering toward the bottom
    for i in range(12):
        a0 = 2 * math.pi * i / 12
        for k in range(10):
            t = k / 10
            r = 0.233 - 0.09 * t
            ang = a0 + (math.pi / 12) * t * (1 if i % 2 else -1)
            z = 3.02 - 0.042 * k
            bpy.ops.mesh.primitive_torus_add(major_radius=0.016, minor_radius=0.0035, major_segments=10, minor_segments=5)
            o = bpy.context.active_object
            o.location = (RX + math.cos(ang) * r, math.sin(ang) * r, z)
            o.scale = (1, 1, 1.7)
            o.rotation_euler = (math.radians(90), 0, ang + (math.pi / 2 if k % 2 else 0))
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            _finish(o, "P3_Chrome", 0, 0)
    return finalize("hoop_gooseneck")


BUILDERS = {"laundry_washer": washer, "laundry_press": press, "pump_unit": pump, "intake_counter": counter, "locker": locker,
            "razor_wire_2m": razor_wire, "floodlight_pole": floodlight_pole, "lint_screen": lint_screen, "isolation_switch": isolator, "hoop_gooseneck": hoop}


def render_preview(obj, path):
    scn = bpy.context.scene
    scn.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
    scn.render.resolution_x, scn.render.resolution_y = 900, 700
    world = bpy.data.worlds.new("w"); scn.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.52, 0.55, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    bb = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    ctr = sum(bb, Vector()) / 8
    size = max((max(v[i] for v in bb) - min(v[i] for v in bb)) for i in range(3))
    bpy.ops.object.camera_add(location=ctr + Vector((size * 1.2, -size * 1.6, size * 0.8)))
    cam = bpy.context.active_object
    cam.rotation_euler = (ctr - cam.location).to_track_quat("-Z", "Y").to_euler()
    scn.camera = cam
    bpy.ops.object.light_add(type="AREA", location=ctr + Vector((-size, -size, size * 2)))
    bpy.context.active_object.data.energy = 400 * size * size
    bpy.context.active_object.data.size = size * 2
    bpy.ops.object.light_add(type="SUN", location=ctr + Vector((size, size, size)))
    bpy.context.active_object.data.energy = 2.0
    bpy.context.active_object.rotation_euler = (math.radians(50), 0, math.radians(140))
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    results = []
    for name, fn in BUILDERS.items():
        if ONLY and name not in ONLY:
            continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        PARTS.clear()
        obj, info = fn()
        results.append(info)
        if RENDER:
            os.makedirs(RENDER, exist_ok=True)
            render_preview(obj, os.path.join(RENDER, name + ".png"))
    with open(os.path.join(OUT, "phase03_props_build.json"), "w") as f:
        json.dump(results, f, indent=1)

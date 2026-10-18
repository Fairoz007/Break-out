"""Re-import GLBs into a fresh scene and render a 3/4 preview each.
blender -b --factory-startup --python tools/phase15_glb_preview.py -- OUT_DIR file1.glb file2.glb ..."""
import bpy, sys, math
from pathlib import Path
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; out = Path(a[0]); out.mkdir(parents=True, exist_ok=True)
for f in a[1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=f)
    pts = [o.matrix_world @ Vector(c) for o in bpy.data.objects if o.type == 'MESH' for c in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
    c = (lo + hi) / 2; rad = max((hi - lo).length / 2, 0.1)
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x = 640; sc.render.resolution_y = 480
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.35, 0.37, 0.4, 1)
    L = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); L.data.energy = 3; L.rotation_euler = (math.radians(50), 0, math.radians(30)); sc.collection.objects.link(L)
    bpy.ops.mesh.primitive_plane_add(size=rad * 8, location=(c.x, c.y, lo.z - 0.001))
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = c + Vector((rad * 1.6, -rad * 2.2, rad * 1.1)); cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = str(out / (Path(f).stem + '.png')); bpy.ops.render.render(write_still=True)

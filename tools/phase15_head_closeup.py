"""Close-up head renders of exported character GLBs (rest pose). blender -b --python tools/phase15_head_closeup.py -- OUT_DIR a.glb b.glb"""
import bpy, sys, math
from pathlib import Path
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; out = Path(a[0]); out.mkdir(parents=True, exist_ok=True)
for f in a[1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=f)
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    hb = next(b for b in rig.pose.bones if b.name.lower() in ('head', 'bip01 head'))
    h = rig.matrix_world @ hb.head
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x = 480; sc.render.resolution_y = 480
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.4, 0.4, 0.42, 1)
    L = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); L.data.energy = 3; L.rotation_euler = (math.radians(60), 0, math.radians(20)); sc.collection.objects.link(L)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); cam.data.lens = 85; sc.collection.objects.link(cam); sc.camera = cam
    for tag, off in (('front', Vector((0, -1.1, 0.08))), ('three_quarter', Vector((0.75, -0.8, 0.08)))):
        tgt = h + Vector((0, 0, 0.09)); cam.location = tgt + off; cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = str(out / (Path(f).stem + '_head_' + tag + '.png')); bpy.ops.render.render(write_still=True)

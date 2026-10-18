"""Render every action of a character GLB at mid-clip (3/4 view) for full-library visual QA.
blender -b --factory-startup --python tools/phase15_clip_sheet.py -- OUT_DIR file.glb"""
import bpy, sys, math
from pathlib import Path
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; out = Path(a[0]); out.mkdir(parents=True, exist_ok=True); f = a[1]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=f)
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x = 300; sc.render.resolution_y = 400
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.33, 0.34, 0.36, 1)
L = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); L.data.energy = 3; L.rotation_euler = (math.radians(50), 0, math.radians(30)); sc.collection.objects.link(L)
bpy.ops.mesh.primitive_plane_add(size=8)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 35
cam.location = (3.6, -4.6, 1.5); cam.rotation_euler = (Vector((0, 0, 0.85)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
ad = rig.animation_data or rig.animation_data_create()
for act in sorted(bpy.data.actions, key=lambda x: x.name):
    ad.action = act
    if hasattr(ad, 'action_slot') and act.slots: ad.action_slot = act.slots[0]
    f0, f1 = act.frame_range; sc.frame_set(int((f0 + f1) / 2))
    sc.render.filepath = str(out / (Path(f).stem + '__' + act.name.split('|')[-1] + '.png')); bpy.ops.render.render(write_still=True)

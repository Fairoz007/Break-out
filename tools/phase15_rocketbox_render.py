"""Render Rocketbox evaluation GLBs (re-imported) at rest + clip poses. Derived from phase15_ubc_render.py.
blender -b --factory-startup --python tools/phase15_rocketbox_render.py -- [stem ...]"""
import bpy, sys, json, math
from pathlib import Path
from mathutils import Vector
R = Path(__file__).resolve().parents[1]
SRC = R / 'asset_library/converted/phase15_characters/rocketbox/animated'
OUT = R / 'asset_library/manifests/phase15_characters_previews/rocketbox_eval'
OUT.mkdir(parents=True, exist_ok=True)
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
STEMS = args or ['male_adult_01', 'security_male_01', 'medical_female_01']
POSES = [('REST', None, 0.0), ('Idle_Loop', 'Idle_Loop', 0.5), ('Walk_Loop', 'Walk_Loop', 0.0), ('Walk_Loop', 'Walk_Loop', 0.5),
         ('Jog_Fwd_Loop', 'Jog_Fwd_Loop', 0.25), ('Sprint_Loop', 'Sprint_Loop', 0.25), ('Crouch_Idle_Loop', 'Crouch_Idle_Loop', 0.5),
         ('Crouch_Fwd_Loop', 'Crouch_Fwd_Loop', 0.25), ('Jump_Loop', 'Jump_Loop', 0.5), ('Interact', 'Interact', 0.5),
         ('Push_Loop', 'Push_Loop', 0.5), ('ClimbUp_1m', 'ClimbUp_1m', 0.5)]
log = {}
for stem in STEMS:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(SRC / (stem + '.glb')))
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x = 520; sc.render.resolution_y = 720
    sc.render.film_transparent = False
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.32, 0.33, 0.35, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.6
    for rot, e in (((50, 0, 30), 3.0), ((60, 0, -140), 1.5)):
        L = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); L.data.energy = e; L.rotation_euler = [math.radians(a) for a in rot]; sc.collection.objects.link(L)
    bpy.ops.mesh.primitive_plane_add(size=6); floor = bpy.context.active_object
    fm = bpy.data.materials.new('floor'); fm.use_nodes = True; fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1); floor.data.materials.append(fm)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 50
    acts = {a.name: a for a in bpy.data.actions}
    shots = []
    for label, act, phase in POSES:
        ad = rig.animation_data or rig.animation_data_create()
        if act is None:
            ad.action = None
            for pb in rig.pose.bones: pb.matrix_basis.identity()
            frame = 0
        else:
            a = acts.get(act) or next((v for k, v in acts.items() if k.split('|')[-1] == act), None)
            if a is None: shots.append((label, 'MISSING')); continue
            ad.action = a
            if hasattr(ad, 'action_slot') and a.slots: ad.action_slot = a.slots[0]
            f0, f1 = a.frame_range; frame = int(round(f0 + (f1 - f0) * phase))
        sc.frame_set(frame); bpy.context.view_layer.update()
        for view, loc in (('front', (0, -5.2, 1.0)), ('side', (5.2, 0, 1.0))):
            cam.location = loc; d = Vector((0, 0, 0.92)) - Vector(loc); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
            p = OUT / f'{stem}__{label}_{int(phase*100):02d}_{view}.png'
            sc.render.filepath = str(p); bpy.ops.render.render(write_still=True); shots.append((label, str(p.relative_to(R))))
    log[stem] = {'actions': sorted(acts), 'shots': shots}
(OUT / ('render_log_' + '_'.join(STEMS) + '.json')).write_text(json.dumps(log, indent=2))
print('UBC_RENDER_DONE')

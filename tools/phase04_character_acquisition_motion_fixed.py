import bpy, math, json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
O=R/'assets/characters/phase04_realistic/inspection_fixed';O.mkdir(parents=True,exist_ok=True)
report={}
for stem in ['rb_adrian_cross','rb_noah_reyes']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str(R/f'assets/characters/phase04_realistic/evaluation/{stem}_mixamo_evaluation.glb'))
 rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
 sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=500;sc.render.resolution_y=650;sc.render.resolution_percentage=100
 sc.world=bpy.data.worlds.new('Studio');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.15,.15,.15,1)
 for name,loc,power in [('Key',(2,-3,4),700),('Fill',(-3,-1,2),500)]:
  l=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(l);l.location=loc;l.data.energy=power;l.data.size=4;l.rotation_euler=(Vector((0,0,1))-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.mesh.primitive_plane_add(size=6)
 cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=(2,-4,1.8);cam.rotation_euler=(Vector((0,0,.9))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=45
 records=[]
 for clip in ['pull_heavy_object','opening_door_inwards']:
  action=next(a for a in bpy.data.actions if a.name.split('|')[-1]==clip or a.name==clip)
  rig.animation_data_create();rig.animation_data.action=action
  if action.slots:rig.animation_data.action_slot=action.slots[0]
  for phase in [.1,.5,.9]:
   sc.frame_set(round(action.frame_range[0]+phase*(action.frame_range[1]-action.frame_range[0])))
   sc.render.filepath=str(O/f'{stem}_{clip}_{int(phase*100)}.png');bpy.ops.render.render(write_still=True)
   records.append({'clip':clip,'phase':phase,'frame':sc.frame_current,'image':sc.render.filepath})
 report[stem]=records
(O/'motion_review.json').write_text(json.dumps(report,indent=2))

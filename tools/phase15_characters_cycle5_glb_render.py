import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(R/'asset_library/converted/phase15_characters/cycle5/native_walk_proxy.glb'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
rig.animation_data.action=None
print('TRACKS',[(t.name,[(s.action.name,s.frame_start,s.frame_end) for s in t.strips]) for t in rig.animation_data.nla_tracks])
for t in rig.animation_data.nla_tracks:t.mute=True
bpy.ops.mesh.primitive_plane_add(size=200);bpy.context.object.location.z=-.02
bpy.ops.object.camera_add(location=(3,-5,2.0));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=2.3
for loc,power,size in [((2,-3,4),650,4),((-2,1,3),500,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(-l.location).to_track_quat('-Z','Y').to_euler()
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=16;sc.render.resolution_x=600;sc.render.resolution_y=700;sc.render.resolution_percentage=100;sc.world.color=(.2,.2,.2)
out=R/'asset_library/manifests/phase15_characters_previews';out.mkdir(exist_ok=True)
for name,frame in [('Original_Walk_Prototype',8)]:
 for t in rig.animation_data.nla_tracks:t.mute=name not in t.name
 sc.frame_set(frame);sc.render.filepath=str(out/(name+'_'+str(frame)+'.png'));bpy.ops.render.render(write_still=True)


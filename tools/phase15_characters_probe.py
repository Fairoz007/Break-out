import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/prison_humanoid_source.blend'))
r=bpy.data.objects['Human.rig'];print('ACTIONS',[(a.name,len(a.layers)) for a in bpy.data.actions][:5])
for t in r.animation_data.nla_tracks:t.mute=True
for t in r.animation_data.nla_tracks:
 if t.name=='Walk_Loop':t.mute=False
for f in [0,8,16]:
 bpy.context.scene.frame_set(f);print(f,list(r.pose.bones['thigh_l'].rotation_quaternion),list(r.pose.bones['thigh_l'].matrix.translation))
for o in bpy.data.objects:
 if o.type=='MESH':print(o.name,len(o.data.vertices),list(o.data.materials),set(p.material_index for p in o.data.polygons))

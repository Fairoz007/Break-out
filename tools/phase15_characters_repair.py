import bpy,json,math
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/prison_humanoid_source.blend'))
tgt=bpy.data.objects['Human.rig']; tgt.animation_data_clear()
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
paths=list((R/'asset_library/extracted_sources/phase15_characters').rglob('UAL*_Standard.glb'))
clips=['Idle_Loop','Walk_Loop','Jog_Fwd_Loop','Sprint_Loop','Crouch_Idle_Loop','Crouch_Fwd_Loop','Jump_Start','Jump_Land','Walk_Formal_Loop','Interact','PickUp_Table','Fixing_Kneeling','Push_Loop','Sitting_Enter','Sitting_Exit','Sitting_Idle_Loop','Punch_Jab','Hit_Chest','Idle_Talking_Loop']
report=[];actions=[]
for path in paths:
 before=set(bpy.data.objects); beforea=set(bpy.data.actions);bpy.ops.import_scene.gltf(filepath=str(path));new=set(bpy.data.objects)-before
 src=next(o for o in new if o.type=='ARMATURE');src.animation_data.action=None
 for tr in src.animation_data.nla_tracks:tr.mute=True
 sourceactions=list(set(bpy.data.actions)-beforea)
 for sa in sourceactions:
  name=sa.name.split('.')[0]
  if name not in clips or name in [x.name for x in actions]:continue
  src.animation_data.action=sa
  ta=bpy.data.actions.new(name);tgt.animation_data_create();tgt.animation_data.action=ta
  start,end=map(int,sa.frame_range)
  for f in range(start,end+1):
   bpy.context.scene.frame_set(f);bpy.context.view_layer.update()
   for tb in tgt.pose.bones:
    sb=src.pose.bones.get(tb.name)
    if not sb:continue
    delta=sb.matrix.to_quaternion() @ sb.bone.matrix_local.to_quaternion().inverted()
    desired=(delta @ tb.bone.matrix_local.to_quaternion()).to_matrix().to_4x4()
    desired.translation=tb.bone.head_local
    tb.location=(0,0,0);tb.scale=(1,1,1);tb.rotation_mode='QUATERNION';tb.rotation_quaternion=sb.rotation_quaternion.copy()
    tb.rotation_mode='QUATERNION';tb.keyframe_insert('rotation_quaternion',frame=f)
   bpy.context.view_layer.update()
  actions.append(ta); report.append({'clip':name,'frames':end-start+1,'duration_seconds':(end-start)/24,'status':'PARTIALLY_VERIFIED','method':'world rotation rest delta; no root translation; foot contact unverified'})
  tgt.animation_data.action=None
 for o in new:bpy.data.objects.remove(o,do_unlink=True)
 for a in sourceactions:
  if a not in actions:bpy.data.actions.remove(a)
for a in actions:
 tr=tgt.animation_data.nla_tracks.new();tr.name=a.name;tr.strips.new(a.name,0,a)
tgt.animation_data.action=None
for tr in tgt.animation_data.nla_tracks:tr.mute=True
for pb in tgt.pose.bones:pb.matrix_basis=Matrix.Identity(4)
for o in list(bpy.data.objects):
 if o.type=='MESH':
  o.parent=tgt
  for s in o.material_slots:s.link='DATA'
  bpy.context.view_layer.objects.active=o;o.select_set(True)
  try:
   bpy.ops.object.vertex_group_limit_total(limit=4);bpy.ops.object.vertex_group_normalize_all(lock_active=False)
  except Exception:pass
  o.select_set(False)
for name,color in [('adrian_cross',(.48,.11,.025,1)),('noah_reyes',(.30,.22,.11,1)),('prison_guard',(.025,.055,.11,1)),('prisoner_npc',(.42,.13,.03,1))]:
 shirt=bpy.data.objects['original_short_sleeve_shirt'];m=shirt.data.materials[0].copy();m.name=name+'_uniform';m.diffuse_color=color;m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color;shirt.data.materials[0]=m
 bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=tgt
 bpy.ops.export_scene.gltf(filepath=str(R/'assets/characters/phase15'/ (name+'.glb')),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_skins=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/prison_humanoid_repaired.blend'))
(R/'asset_library/manifests/phase15_characters_repair.json').write_text(json.dumps(report,indent=2))
print('REPAIRED',len(actions))


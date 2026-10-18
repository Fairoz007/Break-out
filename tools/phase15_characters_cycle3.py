import bpy,json
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/prison_humanoid_source.blend'))
tgt=bpy.data.objects['Human.rig'];tgt.animation_data_clear()
for p in tgt.pose.bones:p.matrix_basis=Matrix.Identity(4)
bpy.context.view_layer.update()
for o in bpy.data.objects:
 if o.type=='MESH':print('MESH',o.name,'bounds',list(o.dimensions),'loc',list(o.location),'mat',[(s.name,s.link) for s in o.material_slots])
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
path=next((R/'asset_library/extracted_sources/phase15_characters').rglob('UAL1_Standard.glb'))
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));new=set(bpy.data.objects)-before;src=next(o for o in new if o.type=='ARMATURE');src.animation_data.action=None
for tr in src.animation_data.nla_tracks:tr.mute=True
sa=next(a for a in bpy.data.actions if a.name.split('.')[0]=='Walk_Loop');src.animation_data.action=sa
print('REST',tgt.data.bones['pelvis'].matrix_local,src.data.bones['pelvis'].matrix_local)
act=bpy.data.actions.new('Walk_Loop');tgt.animation_data_create();tgt.animation_data.action=act
for f in range(33):
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update()
 for tb in tgt.pose.bones:
  sb=src.pose.bones.get(tb.name)
  if sb is None:continue
  delta=sb.matrix.to_quaternion() @ sb.bone.matrix_local.to_quaternion().inverted()
  desired=(delta @ tb.bone.matrix_local.to_quaternion()).to_matrix().to_4x4()
  if tb.parent:desired.translation=tb.parent.matrix @ tb.parent.bone.matrix_local.inverted() @ tb.bone.head_local
  else:desired.translation=tb.bone.head_local
  tb.matrix=desired;bpy.context.view_layer.update()
  tb.rotation_mode='QUATERNION';tb.keyframe_insert('rotation_quaternion',frame=f);tb.keyframe_insert('location',frame=f)
for o in new:bpy.data.objects.remove(o,do_unlink=True)
for o in bpy.data.objects:
 if o.type=='MESH':
  for s in o.material_slots:s.link='DATA'
# Remove mesh material ambiguity with fresh object/data assignments.
for nm,col in [('original_short_sleeve_shirt',(.55,.13,.02,1)),('original_prison_trousers',(.08,.075,.07,1)),('original_work_boots',(.02,.02,.02,1)),('original_close_crop_scalp',(.04,.025,.015,1))]:
 o=bpy.data.objects[nm];o.data=o.data.copy();m=bpy.data.materials.new(nm+'_v3');m.diffuse_color=col;m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=col;o.data.materials.clear();o.data.materials.append(m)
 for p in o.data.polygons:p.material_index=0
bpy.context.scene.frame_set(8);bpy.context.view_layer.update()
bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=tgt
out=R/'asset_library/converted/phase15_characters/cycle3';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'test.blend'))
bpy.ops.export_scene.gltf(filepath=str(out/'test.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='ACTIONS')

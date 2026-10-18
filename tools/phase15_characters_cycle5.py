import bpy,math
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/prison_humanoid_source.blend'))
rig=bpy.data.objects['Human.rig'];rig.animation_data_clear()
for p in rig.pose.bones:p.matrix_basis=Matrix.Identity(4)
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
# Original native rig locomotion experiment, not UAL animation.
a=bpy.data.actions.new('Original_Walk_Prototype');rig.animation_data_create();rig.animation_data.action=a
for f in range(33):
 phase=f*2*math.pi/32
 for p in rig.pose.bones:
  p.rotation_mode='XYZ';p.rotation_euler=(0,0,0)
 for side,sgn in [('l',1),('r',-1)]:
  rig.pose.bones['thigh_'+side].rotation_euler.x=.35*math.sin(phase)*sgn
  rig.pose.bones['calf_'+side].rotation_euler.x=-.6*max(0,-math.sin(phase)*sgn)
  rig.pose.bones['upperarm_'+side].rotation_euler.x=-.22*math.sin(phase)*sgn
  rig.pose.bones['lowerarm_'+side].rotation_euler.x=-.15
 for p in rig.pose.bones:p.keyframe_insert('rotation_euler',frame=f)
# Uniform surface substitute on body prevents duplicate shell z fighting.
h=bpy.data.objects['Human'];h.data=h.data.copy()
for name,c in [('prison_shirt',(.5,.12,.025,1)),('prison_trouser',(.07,.065,.06,1)),('boot',(.02,.02,.02,1))]:
 m=bpy.data.materials.new(name);m.diffuse_color=c;m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=c;h.data.materials.append(m)
for p in h.data.polygons:
 c=p.center
 if c.z<.14:p.material_index=3
 elif c.z<.96 and abs(c.x)<.32:p.material_index=2
 elif .96<c.z<1.43 and abs(c.x)<.30:p.material_index=1
for n in ['original_short_sleeve_shirt','original_prison_trousers','original_work_boots']:bpy.data.objects[n].hide_render=True
out=R/'asset_library/converted/phase15_characters/cycle5';out.mkdir(exist_ok=True)
bpy.context.scene.frame_set(8);bpy.ops.wm.save_as_mainfile(filepath=str(out/'test.blend'))

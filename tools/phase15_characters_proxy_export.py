import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/converted/phase15_characters/cycle5/test.blend'))
rig=bpy.data.objects['Human.rig'];a=rig.animation_data.action
for n in ['original_short_sleeve_shirt','original_prison_trousers','original_work_boots']:
 bpy.data.objects.remove(bpy.data.objects[n],do_unlink=True)
for m in bpy.data.materials:
 if m.use_nodes and m.node_tree.nodes.get('Principled BSDF'):m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.85
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:o.select_set(True)
bpy.context.view_layer.objects.active=rig

for stem,color in [('adrian_native_proxy',(.5,.12,.025,1)),('noah_native_proxy',(.35,.20,.07,1))]:
 m=bpy.data.objects['Human'].data.materials[1];m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color
 bpy.ops.export_scene.gltf(filepath=str(R/'assets/characters/phase15'/(stem+'.glb')),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='ACTIONS')


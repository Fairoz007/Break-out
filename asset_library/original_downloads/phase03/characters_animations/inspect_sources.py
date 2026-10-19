import bpy,json
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parent;records=json.loads((r/'new_acquisition_inventory.json').read_text());out=[]
for x in records:
 p=Path(x['local_path']).resolve()
 if p.suffix.lower()!='.fbx':continue
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(p))
 rigs=[o for o in bpy.data.objects if o.type=='ARMATURE'];meshes=[o for o in bpy.data.objects if o.type=='MESH'];points=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
 bounds=([min(v[i] for v in points) for i in range(3)],[max(v[i] for v in points) for i in range(3)]) if points else None
 out.append({'source':str(p),'rigs':len(rigs),'bone_counts':[len(o.data.bones) for o in rigs],'bone_names':[b.name for b in rigs[0].data.bones] if rigs else [],'mesh_count':len(meshes),'polygons':sum(len(o.data.polygons) for o in meshes),'max_shape_keys':max([len(o.data.shape_keys.key_blocks)-1 if o.data.shape_keys else 0 for o in meshes],default=0),'actions':[{'name':a.name,'frame_range':list(a.frame_range)} for a in bpy.data.actions],'blender_world_bounds':bounds,'source_units_scale':bpy.context.scene.unit_settings.scale_length,'import':'PASS','visual':'NOT TESTED'})
(r/'new_blender_source_validation.json').write_text(json.dumps(out,indent=2));print('VALIDATED',len(out))

import bpy,json,sys,hashlib,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]; SRC=R/'asset_library/original_downloads/animations/mixamo_20261019'; OUT=R/'asset_library/converted/mixamo_20261019'; M=R/'asset_library/manifests/mixamo_20261019'
OUT.mkdir(parents=True,exist_ok=True);M.mkdir(parents=True,exist_ok=True)
reports=[]
for p in sorted(SRC.glob('*.fbx')):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_anim=True)
 arms=[o for o in bpy.data.objects if o.type=='ARMATURE']; meshes=[o for o in bpy.data.objects if o.type=='MESH']; pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
 name=p.stem.lower().replace(' ','_'); dest=OUT/(name+'.glb')
 actions=[{'name':a.name,'frames':list(a.frame_range)} for a in bpy.data.actions]
 bpy.ops.export_scene.gltf(filepath=str(dest),export_format='GLB',export_animations=True,export_animation_mode='ACTIONS',export_force_sampling=True,export_yup=True)
 reports.append(dict(source=str(p.relative_to(R)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),converted=str(dest.relative_to(R)),converted_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),blender_version=bpy.app.version_string,armatures=[{'name':a.name,'bones':[b.name for b in a.data.bones]} for a in arms],meshes=len(meshes),triangles=sum(sum(len(f.vertices)-2 for f in o.data.polygons) for o in meshes),materials=len(bpy.data.materials),images=[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file),'has_data':i.has_data} for i in bpy.data.images],dimensions_m=[max(p[i] for p in pts)-min(p[i] for p in pts) for i in range(3)] if pts else None,actions=actions,weighted_meshes=[o.name for o in meshes if o.vertex_groups],godot_import='NOT TESTED',retargeting='REQUIRED for Rocketbox Bip01 / UBC skeletons',identity='Mixamo default animation reference only, not protagonist',visual_inspection='NOT TESTED'))
 (M/'blender_validation.json').write_text(json.dumps(reports,indent=2))
 print(name,len(arms),len(actions),flush=True)

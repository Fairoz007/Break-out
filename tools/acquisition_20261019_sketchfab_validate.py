import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];D=R/'asset_library/converted/acquisition_20261019/sketchfab_props';D.mkdir(parents=True,exist_ok=True);M=R/'asset_library/manifests/acquisition_20261019';rep={}
items=[('simple_handcuffs',R/'asset_library/extracted_sources/acquisition_20261019/sketchfab/simple_handcuffs/source/simple_handcuffs.glb'),('industrial_dryer_ironing',R/'asset_library/original_downloads/props/acquisition_20261019/industrial_dryer_ironing/industrial_dryer_machine__ironing.glb')]
items.append(('guard_tower',R/'asset_library/original_downloads/architecture/acquisition_20261019/guard_tower/guard_tower_free_asset.glb'))
for slug,p in items:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(p));meshes=[o for o in bpy.data.objects if o.type=='MESH'];
 if slug=='industrial_dryer_ironing':
  for ob in list(meshes):
   if max(ob.dimensions)>50:bpy.data.objects.remove(ob,do_unlink=True)
 factor=0.05 if slug=='simple_handcuffs' else (0.45 if slug=='industrial_dryer_ironing' else 1.0)
 for ob in bpy.context.scene.objects:
  if ob.parent is None:ob.scale*=factor
 bpy.context.view_layer.update();meshes=[o for o in bpy.data.objects if o.type=='MESH'];pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)*.5;extent=max(hi-lo)
 info={'source':str(p.relative_to(R)),'scale_adjustment':factor,'scale_status':'Proposed gameplay scale; physical reference calibration NOT TESTED','removed_backdrop':slug=='industrial_dryer_ironing','mesh_count':len(meshes),'meshes':[{'name':o.name,'polygons':len(o.data.polygons),'vertices':len(o.data.vertices),'dimensions':list(o.dimensions),'materials':[m.name if m else None for m in o.data.materials]} for o in meshes],'bounds_m':list(hi-lo),'separate_parts':[o.name for o in meshes],'actions':[a.name for a in bpy.data.actions],'textures':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images],'missing_images':[i.filepath for i in bpy.data.images if not i.packed_file and i.source=='FILE' and not Path(bpy.path.abspath(i.filepath)).exists()]}
 dest=D/(slug+'.glb');bpy.ops.export_scene.gltf(filepath=str(dest),export_format='GLB',export_animations=True);info['converted_file']=dest.relative_to(R).as_posix();info['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();info['size']=dest.stat().st_size
 sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=800;sc.render.resolution_y=700;sc.render.resolution_percentage=100;sc.world=bpy.data.worlds.new('w');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.18,.18,1)
 for rot,e in [((30,0,30),3),((60,0,-140),2)]:
  ob=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN'));ob.data.energy=e;ob.rotation_euler=[math.radians(a) for a in rot];sc.collection.objects.link(ob)
 cam=bpy.data.objects.new('camera',bpy.data.cameras.new('camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=extent*1.65;cam.location=center+Vector((1,-1,.7))*extent*2;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(M/(slug+'_actual.png'));bpy.ops.render.render(write_still=True);rep[slug]=info
# Inspect source blend without executing embedded scripts.
bpy.ops.wm.open_mainfile(filepath=str(R/'asset_library/extracted_sources/acquisition_20261019/sketchfab/industrial_dryer_ironing/source/washing.blend'),use_scripts=False)
rep['laundry_blend_source']={'objects':[{'name':o.name,'type':o.type} for o in bpy.data.objects],'images':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file),'filepath':i.filepath} for i in bpy.data.images],'actions':[a.name for a in bpy.data.actions]}
(M/'sketchfab_blender_validation.json').write_text(json.dumps(rep,indent=2))

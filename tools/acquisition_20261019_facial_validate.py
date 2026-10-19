import bpy,json,sys,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];D=R/'asset_library/converted/acquisition_20261019/rocketbox_facial';OUT=D/'validation';OUT.mkdir(exist_ok=True)
rep={}
for p in sorted((D/'animated').glob('*.glb')):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(p));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');meshes=[o for o in bpy.data.objects if o.type=='MESH'];shapes={o.name:[k.name for k in o.data.shape_keys.key_blocks][1:] for o in meshes if o.data.shape_keys};imgs=[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images];zs=[(o.matrix_world@v.co).z for o in meshes for v in o.data.vertices]
 rep[p.stem]={'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'bones':len(rig.data.bones),'polygons':sum(len(o.data.polygons) for o in meshes),'shape_keys':shapes,'unweighted_vertices':{o.name:sum(not v.groups for v in o.data.vertices) for o in meshes},'actions':len(bpy.data.actions),'height_m':max(zs)-min(zs),'images':imgs}
 if p.stem not in ['rb_adrian_cross','rb_noah_reyes']:continue
 sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=640;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.world=bpy.data.worlds.new('world');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(0.3,0.3,0.3,1)
 for rot,e in [((50,0,30),3),((60,0,-140),2)]:
  ob=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN'));ob.data.energy=e;ob.rotation_euler=[math.radians(a) for a in rot];sc.collection.objects.link(ob)
 cam=bpy.data.objects.new('camera',bpy.data.cameras.new('camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.lens=70;cam.location=(0,-1.25,1.68);cam.rotation_euler=(Vector((0,0,1.62))-cam.location).to_track_quat('-Z','Y').to_euler()
 for pose in ['neutral','jaw_test']:
  if pose=='jaw_test':
   for o in meshes:
    if o.data.shape_keys:
     keys=o.data.shape_keys.key_blocks;key=next((k for k in keys if 'jaw' in k.name.lower() and ('open' in k.name.lower() or 'drop' in k.name.lower())),None)
     if key:key.value=0.7;rep[p.stem]['tested_morph']=key.name
  sc.render.filepath=str(OUT/(p.stem+'_'+pose+'.png'));bpy.ops.render.render(write_still=True)
(OUT/'blender_reload_report.json').write_text(json.dumps(rep,indent=2))

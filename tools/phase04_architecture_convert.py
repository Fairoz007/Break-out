import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector, Matrix
R=Path.cwd();out=R/'assets/props/phase04_architecture';src=R/'assets/props/acquisition_20261019/industrial_dryer_ironing.glb'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(src));meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];report={}
for name,group,height in [('industrial_dryer',[o for o in meshes if o.name=='Object_4'],1.9),('ironing_station',[o for o in meshes if o.name!='Object_4'],1.25)]:
 pts=[o.matrix_world@Vector(v) for o in group for v in o.bound_box];lo=Vector(tuple(min(p[i] for p in pts) for i in range(3)));hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)));factor=height/(hi.z-lo.z);center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
 copies=[]
 for o in group:
  n=o.copy();n.data=o.data.copy();bpy.context.collection.objects.link(n);n.matrix_world=o.matrix_world.copy();bpy.ops.object.select_all(action='DESELECT');n.select_set(True);bpy.context.view_layer.objects.active=n;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
  # Bake world transforms and center to floor in Blender Z-up; exporter converts to Godot Y-up.
  xf=n.matrix_world.copy()
  for v in n.data.vertices:v.co=(xf@v.co-center)*factor
  n.parent=None;n.matrix_world=Matrix.Identity(4);copies.append(n)
  if len(n.data.polygons)>8000:
   mod=n.modifiers.new('Runtime reduction','DECIMATE');mod.ratio=.25;bpy.ops.object.modifier_apply(modifier=mod.name)
 bpy.ops.object.select_all(action='DESELECT')
 for n in copies:n.select_set(True)
 dest=out/(name+'.glb');bpy.ops.export_scene.gltf(filepath=str(dest),use_selection=True,export_format='GLB')
 report[name]={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'runtime_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'height_m':height,'width_m':(hi.x-lo.x)*factor,'depth_m':(hi.y-lo.y)*factor,'triangles':sum(sum(len(p.vertices)-2 for p in n.data.polygons) for n in copies),'modifications':'Separate assembly; center floor origin; metric scale; reduce dense ironing components to 25%; original materials preserved'}
 for n in copies:bpy.data.objects.remove(n,do_unlink=True)
(out/'conversion.json').write_text(json.dumps(report,indent=2))


import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
src=R/'extracted/OGA_industrial_a52_version/industrial_final_cycles.blend'
bpy.ops.wm.open_mainfile(filepath=str(src))
meshes=[]
for o in bpy.data.objects:
 if o.type=='MESH':meshes.append({'name':o.name,'dimensions':list(o.dimensions),'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'materials':[m.name for m in o.data.materials if m]})
images=[{'name':i.name,'path':i.filepath,'packed':bool(i.packed_file),'exists':Path(bpy.path.abspath(i.filepath)).exists(),'users':i.users} for i in bpy.data.images if i.source=='FILE']
(R/'geometry_inspection.json').write_text(json.dumps({'source':str(src),'mesh_objects':meshes,'images':images},indent=2))
print('SOURCE_INSPECTED',len(meshes),'meshes',len(images),'images')

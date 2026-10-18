import bpy,pathlib,json,hashlib,math
from mathutils import Vector
R=pathlib.Path(__file__).resolve().parents[1]; S=R/'asset_library/extracted_sources/phase15_architecture'; M=R/'asset_library/manifests/phase15_architecture.json'
records=json.loads(M.read_text())
# Replace the empty sleeve with the separately generated and visually inspected original portrait.
p=S/'photo_sleeve_empty.blend'; bpy.ops.wm.open_mainfile(filepath=str(p))
mat=bpy.data.materials.new('Elena_original_portrait'); mat.use_nodes=True; tex=mat.node_tree.nodes.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(str(R/'assets/textures/phase15_story/elena_harbor_photo.png')); tex.image.pack(); mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
bpy.ops.mesh.primitive_plane_add(size=1,location=(0,-.002,0),rotation=(math.pi/2,0,0)); ob=bpy.context.object; ob.name='Elena_portrait'; ob.scale=(.094,.0627,1); ob.data.materials.append(mat)
bpy.ops.wm.save_as_mainfile(filepath=str(p)); out=R/'assets/props/phase15/photo_sleeve_empty.glb'; bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_yup=True,export_apply=True)
rec=next(x for x in records if x['asset_name']=='photo_sleeve_empty'); rec['asset_name']='photo_sleeve_with_elena'; rec['notes']+=' Contains original generated Elena portrait supplied and visually inspected by coordinator; portrait front -Y source, sleeve retains identifier for stable references.'; rec['original_checksum']=hashlib.sha256(p.read_bytes()).hexdigest(); rec['runtime_checksum']=hashlib.sha256(out.read_bytes()).hexdigest()
# Original fictional diagram, vertical readable labels and strokes; not a working electrical schematic.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def cube(n,loc,dim):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=dim; o.data.materials.append(matpaper)
matpaper=bpy.data.materials.new('Diagram_paper'); matpaper.diffuse_color=(.7,.67,.53,1)
ink=bpy.data.materials.new('Diagram_ink'); ink.diffuse_color=(.015,.025,.03,1)
cube('Paper',(0,0,.3),(.6,.004,.6))
for text,x,z,size in [('BLACKRIDGE / SERVICE',-.27,.54,.035),('NORTH CHASE > CATWALK',-.27,.43,.027),('P1: SELECTOR B',-.27,.3,.034),('P2: HOLD BRAKE',-.27,.2,.034),('CLEAR > B > POWER',-.27,.1,.03),('REFERENCE ONLY / 17',-.27,.035,.022)]:
 bpy.ops.object.text_add(location=(x,-.003,z),rotation=(math.pi/2,0,0)); o=bpy.context.object; o.data.body=text; o.data.size=size; o.data.materials.append(ink); bpy.ops.object.convert(target='MESH')
p=S/'maintenance_diagram.blend'; bpy.ops.wm.save_as_mainfile(filepath=str(p)); out=R/'assets/props/phase15/maintenance_diagram.glb'; bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_yup=True,export_apply=True)
rec=dict(records[-1]); rec.update(asset_id='P15_MAINTENANCE_DIAGRAM',asset_name='maintenance_diagram',requirement_bundle='PROP_DIAGRAM',original_file=str(p.relative_to(R)).replace('\\','/'),runtime_file=str(out.relative_to(R)).replace('\\','/'),original_checksum=hashlib.sha256(p.read_bytes()).hexdigest(),runtime_checksum=hashlib.sha256(out.read_bytes()).hexdigest(),required_by_scene=['CH01_M03_SC01'],dimensions_blender_xyz_m=[.6,.005,.6],polygon_count_if_known=None,notes='Original fictional scene diagram with actual P1 selector B / P2 hold brake order. Split-screen legibility still requires Godot shot validation.'); records.append(rec)
M.write_text(json.dumps(records,indent=2))
# Re-import selected actual exported GLBs and normalize only in QA gallery, never in source/runtime assets.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
names=['wall_4m','cell_bars_3m','stairs_10_risers','fence_2x5','cell_bed','laundry_washer','laundry_press','electrical_panel','toilet','wired_handset','maintenance_diagram','photo_sleeve_empty']
for idx,name in enumerate(names):
 path=R/('assets/environments/phase15' if (R/f'assets/environments/phase15/{name}.glb').exists() else 'assets/props/phase15')/(name+'.glb'); before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(path)); obs=[o for o in bpy.data.objects if o not in before]; meshes=[o for o in obs if o.type=='MESH']; vertices=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]; low=Vector([min(v[i] for v in vertices) for i in range(3)]); high=Vector([max(v[i] for v in vertices) for i in range(3)]); center=(low+high)/2; scale=1.6/max(high-low)
 for o in obs:
  if o.parent is None:o.location=(o.location-center)*scale+Vector(((idx%4)*2.25,(idx//4)*2.4,1)); o.scale*=scale
 bpy.ops.object.text_add(location=((idx%4)*2.25-.85,(idx//4)*2.4-1.03,.08)); txt=bpy.context.object; txt.data.body=name; txt.data.size=.11
bpy.ops.mesh.primitive_plane_add(size=200); floor=bpy.context.object; floor.location.z=-.05
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=12; scene.render.resolution_x=1500; scene.render.resolution_y=1100; scene.render.resolution_percentage=100
scene.world.color=(.3,.3,.3)
for loc in [(2,-4,10),(8,5,10)]:
 bpy.ops.object.light_add(type='AREA',location=loc); bpy.context.object.data.energy=1500; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=7
bpy.ops.object.camera_add(location=(8,-12,13)); cam=bpy.context.object; direction=Vector((3.2,2.4,.6))-cam.location; cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=11; scene.camera=cam
scene.render.filepath=str(S/'qa_contact_sheet.png'); bpy.ops.render.render(write_still=True)

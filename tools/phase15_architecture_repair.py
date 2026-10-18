import bpy,json,pathlib,hashlib,math
from mathutils import Vector
R=pathlib.Path(__file__).resolve().parents[1]; P=R/'asset_library/manifests/phase15_architecture.json'; rows=json.loads(P.read_text())
for name in ['laundry_press','transfer_ledger','electrical_panel','brake_station','double_spillway_door','maintenance_diagram']:
 r=next(x for x in rows if x['asset_name']==name); source=R/r['original_file']; bpy.ops.wm.open_mainfile(filepath=str(source))
 if name=='laundry_press':
  # Move welded mesh guard from construction origin to front of the platen.
  for o in bpy.context.scene.objects:
   if o.name.startswith(('Frame','Vertical_bar')):o.location.y-=.62; o.location.z+=.95
 if name=='transfer_ledger':
  for o in bpy.context.scene.objects:
   if o.name.startswith('Label_'):o.rotation_euler=(0,0,0); o.location=(-.12,-.1,.025)
 if name=='maintenance_diagram':
  for material in bpy.data.materials:
   if material.name in ['Diagram_ink','Diagram_paper']:
    color=material.diffuse_color[:]; material.use_nodes=True; material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color
 markers={'electrical_panel':[('GRIP_P1_SELECTOR',(0,-.22,.46)),('LOOK_SELECTOR_LABEL',(0,-.16,.68))],'brake_station':[('GRIP_P2_BRAKE',(0,-.28,.4))],'double_spillway_door':[('GRIP_LEFT',(-.7,-.1,1.05)),('GRIP_RIGHT',(.88,-.1,1.05))],'laundry_press':[('GRIP_ISOLATION',(.8,-.65,1.1))]}.get(name,[])
 for label,loc in markers:bpy.ops.object.empty_add(type='PLAIN_AXES',location=loc); bpy.context.object.name=label
 bpy.ops.wm.save_as_mainfile(filepath=str(source)); out=R/r['runtime_file']; bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_yup=True,export_apply=True,export_extras=True)
 r['original_checksum']=hashlib.sha256(source.read_bytes()).hexdigest(); r['runtime_checksum']=hashlib.sha256(out.read_bytes()).hexdigest()
 if markers:r['notes']+=' Named grip/look empties are authored alignment proposals; validate against actual rigs.'
P.write_text(json.dumps(rows,indent=2))
# Close-up actual exported diagram front view for legibility check.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); bpy.ops.import_scene.gltf(filepath=str(R/'assets/props/phase15/maintenance_diagram.glb'))
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=8; scene.render.resolution_x=900; scene.render.resolution_y=900; scene.render.resolution_percentage=100; scene.world.color=(.2,.2,.2)
bpy.ops.object.light_add(type='AREA',location=(0,-2,2)); bpy.context.object.data.energy=70; bpy.context.object.data.size=3
bpy.ops.object.camera_add(location=(0,-2,.3)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,0,.3))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=.7; scene.camera=cam; scene.render.filepath=str(R/'asset_library/extracted_sources/phase15_architecture/qa_diagram_front.png'); bpy.ops.render.render(write_still=True)

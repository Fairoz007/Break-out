import bpy,json,math,re,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];M=R/'asset_library/manifests/acquisition_20261019';out=R/'asset_library/converted/acquisition_20261019/radio_yaesu';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);src=R/'asset_library/original_downloads/props/acquisition_20261019/radio_yaesu/radio_yaesu_vx-8.glb';bpy.ops.import_scene.gltf(filepath=str(src));bpy.context.view_layer.update()
meshes=[o for o in bpy.data.objects if o.type=='MESH'];source_report=[dict(name=o.name,triangles=sum(len(p.vertices)-2 for p in o.data.polygons),dimensions=list(o.dimensions)) for o in meshes];removed=[]
# Author's presentation includes three radio copies; retain the unnumbered canonical copy only.
for o in list(meshes):
 if re.search(r'\.00[12]',o.name):removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
meshes=[o for o in bpy.data.objects if o.type=='MESH'];base=next(o for o in meshes if o.name.startswith('Radio_base_low_'))
# Bake source presentation transforms before metric calibration.
for o in meshes:
 matrix=o.matrix_world.copy();o.parent=None;o.matrix_world=matrix
bpy.context.view_layer.update();body_pts=[base.matrix_world@Vector(c) for c in base.bound_box];body_height=max(v.z for v in body_pts)-min(v.z for v in body_pts);factor=.095/body_height
pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box];lo=Vector([min(v[i] for v in pts) for i in range(3)]);hi=Vector([max(v[i] for v in pts) for i in range(3)]);origin=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
for o in meshes:
 for v in o.data.vertices:v.co=(o.matrix_world@v.co-origin)*factor
 o.matrix_world.identity()
bpy.context.view_layer.update();pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box];lo=Vector([min(v[i] for v in pts) for i in range(3)]);hi=Vector([max(v[i] for v in pts) for i in range(3)]);center=(lo+hi)/2;extent=max(hi-lo)
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:o.select_set(True)
glb=out/'radio_yaesu_single_metric.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_animations=False)
report=dict(blender_version=bpy.app.version_string,source_meshes=len(source_report),source_mesh_report=source_report,removed_presentation_meshes=removed,gameplay_meshes=len(meshes),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),bounds_m=list(hi-lo),scale_factor=factor,scale_method='Case body height calibrated to 0.095m from manufacturer VX-8R brochure; source presentation orientation baked, bottom pivot centered.',scale_reference='https://www.yaesu.com/jp/en/products/pdf/AMR/VX-8R.pdf',materials=[m.name for m in bpy.data.materials],images=[dict(name=im.name,size=list(im.size),packed=bool(im.packed_file)) for im in bpy.data.images],armatures=0,actions=len(bpy.data.actions),converted_file=glb.relative_to(R).as_posix(),converted_sha256=hashlib.sha256(glb.read_bytes()).hexdigest(),converted_size=glb.stat().st_size,visual_status='Render pending review',godot_status='NOT TESTED')
(M/'yaesu_blender_validation.json').write_text(json.dumps(report,indent=2))
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=800;sc.render.resolution_y=800;sc.render.resolution_percentage=100;world=bpy.data.worlds.new('Studio');sc.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1)
for loc,power in [((2,-3,4),600),((-3,-1,1),250)]:
 l=bpy.data.objects.new('Area',bpy.data.lights.new('Area','AREA'));sc.collection.objects.link(l);l.location=center+Vector(loc)*extent;l.data.energy=power*extent*extent;l.data.size=3*extent;l.rotation_euler=(center-l.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=extent*1.3
for label,offset in [('front',(2,-2,1)),('rear',(-2,2,1))]:
 cam.location=center+Vector(offset)*extent*2;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(M/('yaesu_actual_'+label+'.png'));bpy.ops.render.render(write_still=True)

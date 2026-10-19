import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];tag='acquisition_20261019';M=R/'asset_library/manifests'/tag;out=R/'asset_library/converted'/tag;out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
p=R/'asset_library/original_downloads/props'/tag/'signal_flashlight/signal_flashlight_2k.gltf';bpy.ops.import_scene.gltf(filepath=str(p))
meshes=[o for o in bpy.data.objects if o.type=='MESH'];pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)])
report=dict(blender_version=bpy.app.version_string,meshes=len(meshes),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes),dimensions_m=list(hi-lo),materials=len(bpy.data.materials),missing_images=[im.filepath for im in bpy.data.images if im.source=='FILE' and not im.has_data],armatures=len([o for o in bpy.data.objects if o.type=='ARMATURE']),animation_actions=len(bpy.data.actions),skin_weights='N/A static prop',visual_defects='Pending render review',godot_import_status='NOT TESTED')
glb=out/'signal_flashlight_2k.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=False);runtime=R/'assets/props'/tag/'signal_flashlight_2k.glb';runtime.write_bytes(glb.read_bytes());(M/'props_blender_validation.json').write_text(json.dumps(report,indent=2))
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=640;sc.render.resolution_y=640;sc.render.resolution_percentage=100
w=bpy.data.worlds.new('Studio');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1)
c=(lo+hi)/2;rad=(hi-lo).length/2
for name,loc,power,size in [('Key',(2,-3,4),400,3),('Fill',(-3,-1,1),150,3)]:
 l=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(l);l.location=c+Vector(loc)*rad;l.data.energy=power*rad*rad;l.data.shape='DISK';l.data.size=size*rad;l.rotation_euler=(c-l.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=c+Vector((rad*1.6,-rad*3,rad*1.4));cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48
sc.render.filepath=str(M/'signal_flashlight_actual.png');bpy.ops.render.render(write_still=True)

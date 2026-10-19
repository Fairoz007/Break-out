import bpy,sys,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];S=R/'asset_library/converted/mixamo_20261019/retarget_trials/poses';O=R/'asset_library/manifests/mixamo_20261019'
for p in S.glob('*.glb'):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(p))
 bpy.context.view_layer.update();meshes=[o for o in bpy.data.objects if o.type=='MESH'];deps=bpy.context.evaluated_depsgraph_get();pts=[o.evaluated_get(deps).matrix_world@v.co for o in meshes for v in o.evaluated_get(deps).data.vertices];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);c=(lo+hi)/2;rad=max((hi-lo).length/2,.001);print(p.name,list(lo),list(hi),flush=True)
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=8;sc.render.resolution_x=400;sc.render.resolution_y=512;sc.render.resolution_percentage=100;sc.world=bpy.data.worlds.new('Studio');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.2,.2,.2,1)
 for name,loc,power in [('Key',(2,-3,4),800),('Fill',(-3,-1,2),500)]:
  l=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(l);l.location=c+Vector(loc)*rad;l.data.energy=power*rad*rad;l.data.size=4*rad;l.rotation_euler=(c-l.location).to_track_quat('-Z','Y').to_euler()
 cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=c+Vector((rad*1.7,-rad*3.2,rad*.7));cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48;sc.render.filepath=str(O/(p.stem+'.png'));bpy.ops.render.render(write_still=True)


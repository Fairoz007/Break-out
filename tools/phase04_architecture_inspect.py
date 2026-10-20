import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path.cwd(); out=R/'assets/props/phase04_architecture';out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(R/'assets/props/acquisition_20261019/industrial_dryer_ironing.glb'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
pts=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box];lo=Vector(tuple(min(p[i] for p in pts) for i in range(3)));hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
report={'bounds':[list(lo),list(hi)],'objects':[{'name':o.name,'verts':len(o.data.vertices),'bounds':[list(o.matrix_world@Vector(o.bound_box[0])),list(o.matrix_world@Vector(o.bound_box[6]))]} for o in meshes]}
(out/'source_inspection.json').write_text(json.dumps(report,indent=2))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=1000;s.render.resolution_y=750;s.render.resolution_percentage=100
s.world.color=(.2,.2,.2);c=(lo+hi)/2;r=(hi-lo).length/2
for name,p,e in [('Key',(2,-3,4),1000),('Fill',(-3,-1,2),600)]:
 l=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));s.collection.objects.link(l);l.location=c+Vector(p)*r;l.data.energy=e*r*r;l.data.size=3*r;l.rotation_euler=(c-l.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));s.collection.objects.link(cam);s.camera=cam;cam.location=c+Vector((r*1.6,-r*2.8,r*1.1));cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=45
s.render.filepath=str(out/'source_inspection.png');bpy.ops.render.render(write_still=True)

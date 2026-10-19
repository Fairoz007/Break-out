import bpy, json, math
from pathlib import Path
from mathutils import Vector
R = Path(__file__).resolve().parents[1]
O = R / 'tests/phase025/evidence/integration'
O.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(R/'asset_library/original_downloads/phase025_integration/city_bus.glb'))
meshes=[o for o in bpy.data.objects if o.type=='MESH']
pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
lo=Vector([min(p[i] for p in pts) for i in range(3)])
hi=Vector([max(p[i] for p in pts) for i in range(3)])
(O/'bus_geometry.json').write_text(json.dumps({'bounds_min':list(lo),'bounds_max':list(hi),'dimensions':list(hi-lo),'meshes':len(meshes),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)},indent=2))
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100
w=bpy.data.worlds.new('Studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.25,.3,.35,1);sc.world=w
c=(lo+hi)/2;rad=(hi-lo).length/2
for name,loc,power in [('Key',(1,-2,3),2200),('Fill',(-2,1,2),1500)]:
    light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(light);light.location=c+Vector(loc)*rad;light.data.energy=power;light.data.size=12;light.rotation_euler=(c-light.location).to_track_quat('-Z','Y').to_euler()
camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(camera);sc.camera=camera;camera.location=c+Vector((1.7,-2.2,1.0))*rad;camera.rotation_euler=(c-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=46
sc.render.filepath=str(O/'bus_candidate.png');bpy.ops.render.render(write_still=True)

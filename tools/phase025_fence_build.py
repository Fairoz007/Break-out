"""Original metric galvanized chain-link fabrication; no third-party geometry."""
from pathlib import Path
import bpy, math, json
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
verts=[];faces=[]
def tube(points,radius,sides=6):
    start=len(verts)
    for i,p in enumerate(points):
        p=Vector(p);direction=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
        direction.normalize();u=direction.cross(Vector((0,1,0))).normalized()
        if u.length<.1:u=direction.cross(Vector((1,0,0))).normalized()
        v=direction.cross(u).normalized()
        for j in range(sides):verts.append(tuple(p+radius*(u*math.cos(j*math.tau/sides)+v*math.sin(j*math.tau/sides))))
    for i in range(len(points)-1):
        for j in range(sides):a=start+i*sides+j;b=start+i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces.append(tuple(start+j for j in reversed(range(sides))))
    faces.append(tuple(start+(len(points)-1)*sides+j for j in range(sides)))
def line(a,b,r,sides=12):tube([a,b],r,sides)
# Woven 65mm diamonds, 2.8mm diameter wire, open geometry rather than alpha cloth.
pitch=.065;xmin=-.984;xmax=.984;bottom=.12;top=4.68
for family in [1,-1]:
    for k in range(-40,100):
        c=k*pitch
        lo=max(xmin,(bottom-c)/family) if family==1 else max(xmin,c-top)
        hi=min(xmax,(top-c)/family) if family==1 else min(xmax,c-bottom)
        if hi<=lo:continue
        steps=max(2,math.ceil((hi-lo)/(.5*pitch)))
        pts=[]
        for j in range(steps+1):
            x=lo+(hi-lo)*j/steps;z=family*x+c
            y=family*.0024*math.cos(2*x*math.pi/pitch)
            pts.append((x,y,z))
        tube(pts,.0014,4)
# Tubular posts, rounded caps, three tension rails, tie wires and wall fixing plates.
for x in [xmin,xmax]:
    line((x,0,.0),(x,0,4.8),.038,16)
    for z in [.18,1.5,3.0,4.64]:
        line((x,-.044,z),(x,.044,z),.006,8)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.041,location=(x,0,4.8));obj=bpy.context.object
    # Add temporary sphere geometry into main buffers.
    off=len(verts);verts.extend([tuple(obj.matrix_world@v.co) for v in obj.data.vertices]);faces.extend([tuple(off+i for i in p.vertices) for p in obj.data.polygons]);bpy.data.objects.remove(obj,do_unlink=True)
for z in [.1,2.4,4.7]:line((xmin,0,z),(xmax,0,z),.018,12)
# Three taut security wires above mesh, within the five-metre module envelope.
for z in [4.79,4.89,4.98]:
    line((xmin,0,z),(xmax,0,z),.0017,6)
    for i in range(12):
        x=xmin+(i+.5)*(xmax-xmin)/12
        line((x-.018,-.012,z-.012),(x+.018,.012,z+.012),.0012,4)
        line((x-.018,.012,z+.012),(x+.018,-.012,z-.012),.0012,4)
for x in [xmin,xmax]:line((x,0,4.7),(x,0,4.99),.009,8)
mesh=bpy.data.meshes.new('Woven galvanized steel mesh');mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new('ChainLink 2.05m x5m fabricated wire',mesh);bpy.context.collection.objects.link(obj)
mat=bpy.data.materials.new('Galvanized zinc steel');mat.diffuse_color=(.38,.43,.46,1);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.38,.43,.46,1);bs.inputs['Metallic'].default_value=.78;bs.inputs['Roughness'].default_value=.48;obj.data.materials.append(mat)
for p in mesh.polygons:p.use_smooth=True
bpy.context.view_layer.objects.active=obj;obj.select_set(True)
out=R/'assets/environments/phase025/chain_link_fence_2x5.glb';out.parent.mkdir(parents=True,exist_ok=True);bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_apply=True)
source=R/'asset_library/converted/phase025_integration/chain_link_fence_2x5.blend';source.parent.mkdir(parents=True,exist_ok=True)
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=1000;sc.render.resolution_y=1000;sc.render.resolution_percentage=100
world=bpy.data.worlds.new('Neutral inspection');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.13,.16,.19,1);sc.world=world
for name,loc,power in [('Key',(2,-4,7),1700),('Rim',(-3,2,6),2200)]:
 light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(light);light.location=loc;light.data.energy=power;light.data.size=4;light.rotation_euler=(Vector((0,0,2.5))-light.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=(4,-8,4);cam.rotation_euler=(Vector((0,0,2.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
sc.render.filepath=str(R/'tests/phase025/evidence/integration/fence_preview.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(source))
(R/'tests/phase025/evidence/integration/fence_geometry.json').write_text(json.dumps({'author':'Original engineering geometry created for BREAKOUT Phase02.5','license':'CC0-1.0','module_metres':[2.05,5,.15],'wire_diameter_metres':.0028,'diamond_pitch_metres':pitch,'vertices':len(verts),'faces':len(faces),'render':sc.render.filepath},indent=2))


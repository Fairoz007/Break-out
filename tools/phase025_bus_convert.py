import bpy,json,math
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(R/'asset_library/original_downloads/phase025_integration/oga_bus/FBX/BUS.fbx'))
meshes=[o for o in bpy.data.objects if o.type=='MESH']
def bounds():
    pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    return Vector([min(p[i] for p in pts) for i in range(3)]),Vector([max(p[i] for p in pts) for i in range(3)])
lo,hi=bounds()
report={'original_bounds':[list(lo),list(hi)],'materials':[(m.name,list(m.diffuse_color)) for m in bpy.data.materials]}
(R/'tests/phase025/evidence/integration/oga_bus_inspect.json').write_text(json.dumps(report,indent=2))
print('BUS_INSPECT',json.dumps(report))
# Bake source transforms into a metric exterior, centered at the ground contact.
center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));scale=11.0/(hi.x-lo.x)
records=[(obj,obj.matrix_world.copy(),obj.data.copy()) for obj in meshes]
for obj,world,data in records:
    obj.animation_data_clear()
    obj.data=data
    for vertex in data.vertices:vertex.co=(world@vertex.co-center)*scale
    obj.parent=None;obj.matrix_world=Matrix.Identity(4);obj.hide_render=False;obj.hide_viewport=False;obj.hide_set(False)
    print('NORMALIZED',obj.name,len(obj.data.vertices),list(obj.dimensions),list(obj.location),obj.hide_render)
    if 'Body' in obj.name:
        bevel=obj.modifiers.new('Panel edge radii','BEVEL');bevel.width=.012;bevel.segments=3
    else:
        for poly in obj.data.polygons:poly.use_smooth=True
colors={'Body':(.24,.29,.27,1),'Windows':(.016,.045,.055,1),'Tire':(.012,.014,.015,1),'Metal':(.32,.36,.39,1),'karmi':(.025,.03,.033,1)}
for mat in bpy.data.materials:
    mat.use_nodes=True
    shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    shader.inputs['Alpha'].default_value=1.0
    for inp in shader.inputs:
        for link in list(inp.links):mat.node_tree.links.remove(link)
    shader.inputs['Base Color'].default_value=colors.get(mat.name,tuple(mat.diffuse_color))
    shader.inputs['Roughness'].default_value=.82 if mat.name=='Tire' else (.18 if mat.name=='Windows' else .42)
    if mat.name=='Windows':
        shader.inputs['Alpha'].default_value=.42;shader.inputs['Transmission Weight'].default_value=.12;mat.surface_render_method='DITHERED'
    shader.inputs['Metallic'].default_value=.75 if mat.name in ['Metal','Bolt'] else (.25 if mat.name=='Windows' else 0)
def material(name,color,metallic=0,roughness=.6):
    m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Metallic'].default_value=metallic;p.inputs['Roughness'].default_value=roughness;return m
navy=material('Correctional transport navy',(.018,.045,.065,1),0,.45)
steel=material('Security window steel',(.03,.04,.045,1),.6,.5)
def box(name,loc,size,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    mod=o.modifiers.new('Manufactured edges','BEVEL');mod.width=min(.035,min(size)*.2);mod.segments=4
    return o
# Existing CC0 weathered painted steel roughness controls broad panel wear.
for mat in bpy.data.materials:
    if mat.name=='Body':
        tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'asset_library/original_downloads/materials/acquisition_20261019/rusty_painted_metal/rusty_painted_metal_rough_2k.jpg'));tex.image.colorspace_settings.name='Non-Color';mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'])
# Detailed authored transport conversion over the sourced coach body.
fabric=material('CC0 worn leather upholstered seats',(.055,.075,.08,1),0,.9)
nt=fabric.node_tree;bs=nt.nodes.get('Principled BSDF')
base=R/'asset_library/original_downloads/phase025_bulk_20261019/materials/fabric_leather_02'
for suffix,socket in [('diff','Base Color'),('rough','Roughness'),('nor_gl','Normal')]:
    path=base/f'fabric_leather_02_{suffix}_2k.jpg'
    if path.exists():
        tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path))
        if suffix!='diff':tex.image.colorspace_settings.name='Non-Color'
        if suffix=='nor_gl':
            norm=nt.nodes.new('ShaderNodeNormalMap');norm.inputs['Strength'].default_value=.35;nt.links.new(tex.outputs['Color'],norm.inputs['Color']);nt.links.new(norm.outputs[0],bs.inputs[socket])
        else:nt.links.new(tex.outputs['Color'],bs.inputs[socket])
rubber=material('Anti slip interior rubber',(.025,.031,.035,1),0,.95)
alloy=material('Satin hardware',(.35,.39,.4,1),.8,.3)
box('Passenger aisle floor',(-.25,0,.84),(9.6,2.17,.1),rubber)
for row in range(8):
    x=-4.1+row*.87
    for side in [-1,1]:
        for lane in range(2):
            y=side*(.53+lane*.42)
            seat=box('Upholstered contoured seat cushion',(x,y,1.10),(.57,.39,.16),fabric)
            back=box('Upholstered high back',(x-.25,y,1.48),(.14,.4,.69),fabric);back.rotation_euler.y=-.11
            box('Seat headrest',(x-.28,y,1.87),(.16,.32,.15),fabric)
            box('Tubular seat pedestal',(x,y,.95),(.06,.065,.22),steel)
            box('Seat belt buckle',(x+.06,y+.15,1.20),(.06,.035,.025),steel)
        box('Seat row handhold',(x-.3,side*.72,1.98),(.045,.7,.04),alloy)
# Driver cockpit, molded instrument panel, steering wheel and seat.
box('Driver dashboard',(4.55,-.54,1.25),(.64,.9,.32),steel)
box('Driver console',(4.3,-.85,1.05),(.5,.32,.55),steel)
box('Driver seat cushion',(3.76,-.55,1.12),(.58,.58,.17),fabric)
box('Driver seat back',(3.48,-.55,1.5),(.15,.58,.77),fabric)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=12,location=(4.12,-.55,1.46),major_radius=.21,minor_radius=.017,rotation=(0,.55,0));bpy.context.object.name='Steering wheel';bpy.context.object.data.materials.append(rubber)
for offset in [-.15,0,.15]:box('Dashboard instrument',(4.38,-.55+offset,1.42),(.09,.09,.035),alloy)
# Mirror housings and curved supports, front destination plate and roof vents.
for side in [-1,1]:
    box('Mirror support',(4.68,side*1.34,1.95),(.06,.34,.045),steel)
    mirror=box('Exterior rear view mirror',(4.64,side*1.49,1.9),(.13,.075,.3),steel)
    box('Mirror glass',(4.565,side*1.49,1.9),(.008,.06,.25),alloy)
for x in [-2.7,.1,2.7]:
    box('Raised roof ventilator',(x,0,2.71),(.7,.65,.07),alloy)
    for j in range(7):box('Vent louver',(x-.25+j*.08,0,2.755),(.02,.5,.012),steel)

for side in [-1,1]:
    y=side*1.225
    box('Transport livery',(0,y,.95),(9.6,.018,.22),navy)
    for x in [i*.3 for i in range(-14,10)]:
        box('Window security upright',(x,y,2.0),(.018,.022,.82),steel)
    for z in [1.65,2.35]:box('Window security rail',(-.75,y,z),(7.0,.024,.018),steel)
    bpy.ops.object.text_add(location=(-2.8,side*1.24,1.15));text=bpy.context.object;text.name='Blackridge transport identification';text.data.body='BLACKRIDGE  /  CORRECTIONS';text.data.size=.17;text.data.extrude=.0008;text.rotation_euler=(math.pi/2,0,0) if side<0 else (math.pi/2,0,math.pi);text.data.materials.append(navy)
# Apply fabrication bevels, consolidate static geometry by material for runtime draw calls.
bpy.ops.object.select_all(action='DESELECT')
for obj in list(bpy.data.objects):
    if obj.type=='MESH':
        bpy.context.view_layer.objects.active=obj
        for modifier in list(obj.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
for obj in bpy.data.objects:obj.select_set(obj.type=='MESH')
bpy.context.view_layer.objects.active=next(o for o in bpy.data.objects if o.type=='MESH')
bpy.ops.object.join();bpy.context.object.name='Blackridge static coach assembly'
bpy.context.view_layer.update()
out=R/'assets/props/phase025/blackridge_transport_bus.glb';out.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_apply=True)
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100
w=bpy.data.worlds.new('Studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.3,.32,.35,1);sc.world=w
for name,loc,power in [('Key',(2,-5,8),2500),('Fill',(-4,3,6),1800)]:
    light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(light);light.location=loc;light.data.energy=power;light.data.size=8;light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=(10,-13,6);cam.rotation_euler=(Vector((0,0,1.3))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48
sc.render.filepath=str(R/'tests/phase025/evidence/integration/bus_converted.png');bpy.ops.render.render(write_still=True)

sc.render.filepath=str(R/'tests/phase025/evidence/integration/bus_interior.png');cam.location=(5.0,-.05,2.13);cam.rotation_euler=(Vector((-3,0,1.45))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=24;bpy.ops.render.render(write_still=True)
source=R/'asset_library/converted/phase025_integration/blackridge_transport_bus.blend';source.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(source))

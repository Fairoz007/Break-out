import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(R/'assets/props/phase15/cell_bed.glb'))
def mat(name,color,rough=.8,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
steel=mat('Institutional painted steel',(.11,.15,.14),.58,.35)
linen=mat('Unbleached mattress ticking',(.52,.5,.41),.95)
blanket=mat('CC0 Fabric030 institutional wool',(.18,.22,.21),.96)
nt=blanket.node_tree;p=nt.nodes.get('Principled BSDF')
for suffix,socket in [('Color','Base Color'),('Roughness','Roughness'),('NormalGL','Normal')]:
 tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/f'asset_library/extracted_sources/acquisition_20261019/Fabric030/Fabric030_2K-JPG_{suffix}.jpg'))
 if suffix!='Color':tex.image.colorspace_settings.name='Non-Color'
 if suffix=='NormalGL':
  n=nt.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;nt.links.new(tex.outputs['Color'],n.inputs['Color']);nt.links.new(n.outputs[0],p.inputs[socket])
 else:nt.links.new(tex.outputs['Color'],p.inputs[socket])
for o in list(bpy.data.objects):
 if o.type=='MESH':
  o.data.materials.clear();o.data.materials.append(steel);m=o.modifiers.new('Safe steel edge radii','BEVEL');m.width=.007;m.segments=3

def upholstered(name,loc,size,material,radius):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 m=o.modifiers.new('Rounded upholstered construction','BEVEL');m.width=radius;m.segments=6
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=m.name)
 m=o.modifiers.new('Soft cloth support','SUBSURF');m.levels=2;bpy.ops.object.modifier_apply(modifier=m.name)
 for v in o.data.vertices:
  x,y,z=v.co
  v.co.z+=.0025*math.sin(24*x+3*y)*math.cos(13*y)*max(0,(z/size[2]+.5))
 for f in o.data.polygons:f.use_smooth=True
 return o
upholstered('Rounded institutional mattress',(0,0,.515),(.80,1.93,.15),linen,.06)
upholstered('Soft pillow',(0,.68,.635),(.61,.36,.11),linen,.048)
# Dense cloth surface with gentle folds and draped edges, within existing frame footprint.
v=[];faces=[];nx=44;ny=76
for j in range(ny+1):
 y=-.94+j/ny*1.38
 for i in range(nx+1):
  x=-.417+i/nx*.834;edge=max(0,(abs(x)-.33)/.087)
  z=.625-.145*edge**2+.008*math.sin(y*31+x*5)*math.exp(-abs(x)*2)+.005*math.sin(x*42+y*7)
  v.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
mesh=bpy.data.meshes.new('Cloth folds mesh');mesh.from_pydata(v,[],faces);mesh.update();o=bpy.data.objects.new('Draped woven blanket',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(blanket)
uv=mesh.uv_layers.new()
for f in mesh.polygons:
 f.use_smooth=True
 for loop in f.loop_indices:
  co=mesh.vertices[mesh.loops[loop].vertex_index].co;uv.data[loop].uv=(co.x*1.5,co.y*1.5)
m=o.modifiers.new('Blanket thickness','SOLIDIFY');m.thickness=.004
# Piped mattress seams as continuous soft cords.
for z in [.465,.565]:
 curve=bpy.data.curves.new('Mattress stitched piping','CURVE');curve.dimensions='3D';curve.bevel_depth=.003;curve.bevel_resolution=3
 points=[]
 for cx,cy,start in [(.34,.905,0),(-.34,.905,90),(-.34,-.905,180),(.34,-.905,270)]:
  for k in range(9):
   t=math.radians(start+k*90/8);points.append((cx+.055*math.cos(t),cy+.055*math.sin(t),z))
 sp=curve.splines.new('POLY');sp.points.add(len(points)-1)
 for a,b in zip(sp.points,points):a.co=(*b,1)
 sp.use_cyclic_u=True;o=bpy.data.objects.new('Mattress edge piping',curve);bpy.context.collection.objects.link(o);o.data.materials.append(linen)
# Convert details and consolidate static surfaces.
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if o.type in ['MESH','CURVE']:o.select_set(True)
bpy.context.view_layer.objects.active=next(o for o in bpy.data.objects if o.type=='MESH');bpy.ops.object.convert(target='MESH');bpy.ops.object.join();bpy.context.object.name='Prison bed complete'
pts=[bpy.context.object.matrix_world@Vector(c) for c in bpy.context.object.bound_box];lo=[min(v[i] for v in pts) for i in range(3)];hi=[max(v[i] for v in pts) for i in range(3)]
out=R/'assets/props/phase025/prison_bed.glb';bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_apply=True)
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=1200;sc.render.resolution_y=900;sc.render.resolution_percentage=100
w=bpy.data.worlds.new('Studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.25,.27,.3,1);sc.world=w
for name,loc,power in [('Key',(2,-3,4),500),('Fill',(-2,1,3),300)]:
 l=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(l);l.location=loc;l.data.energy=power;l.data.size=3;l.rotation_euler=(Vector((0,0,.4))-l.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=(2,-2.8,2);cam.rotation_euler=(Vector((0,0,.4))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=49
sc.render.filepath=str(R/'tests/phase025/evidence/integration/prison_bed_preview.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'asset_library/converted/phase025_integration/prison_bed.blend'))
(R/'tests/phase025/evidence/integration/prison_bed_asset.json').write_text(json.dumps({'source_frame':'assets/props/phase15/cell_bed.glb','fabric':'ambientCG Fabric030 CC0 existing acquisition','additions':['rounded mattress with stitched piping','soft pillow','draped cloth blanket with geometric wrinkles'],'bounds_blender':[lo,hi],'dimensions_godot_xyz':[hi[0]-lo[0],hi[2]-lo[2],hi[1]-lo[1]],'origin':'source unchanged','verification':'Blender render; Godot runtime pending'},indent=2))


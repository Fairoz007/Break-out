import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path.cwd();O=R/'assets/props/phase04_architecture';bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0,rough=.6):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
steel=mat('Welded institutional steel',(.19,.23,.21),.55,.48);bolt=mat('Zinc fasteners',(.36,.38,.36),.8,.4);linen=mat('Undyed mattress ticking',(.62,.60,.51),0,.9);blanket=mat('Olive prison blanket',(.20,.23,.17),0,.95);seam=mat('Cotton seam piping',(.44,.42,.34),0,.85)
import numpy as np
for m in [linen,blanket]:
 n=m.node_tree.nodes;p=n.get('Principled BSDF')
 for suffix,socket in [('Color','Base Color'),('Roughness','Roughness'),('NormalGL','Normal')]:
  im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(R/f'assets/materials/acquisition_20261019/Fabric030/Fabric030_2K-JPG_{suffix}.jpg'),check_existing=False);im.image.colorspace_settings.name=('sRGB' if suffix=='Color' else 'Non-Color');im.image.scale(1024,1024)
  if suffix=='Color':
   pixels=np.empty(1024*1024*4,dtype=np.float32);im.image.pixels.foreach_get(pixels);pixels=pixels.reshape(-1,4);pixels[:,:3]*=np.array(m.diffuse_color[:3]);im.image.pixels.foreach_set(pixels.ravel());im.image.update()

  im.image.filepath_raw=str(O/f'prison_bunk_{m.name.split()[0]}_{suffix}.jpg');im.image.file_format='JPEG';im.image.save()
  if suffix=='NormalGL':
   normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.18;m.node_tree.links.new(im.outputs[0],normal.inputs['Color']);m.node_tree.links.new(normal.outputs[0],p.inputs['Normal'])
  else:m.node_tree.links.new(im.outputs[0],p.inputs[socket])
def box(name,loc,size,m,bevel=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:
  q=o.modifiers.new('Rolled softened edges','BEVEL');q.width=bevel;q.segments=6;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=q.name)
 for p in o.data.polygons:p.use_smooth=True
 return o
def tube(name,a,b,r,m,verts=20):
 a=Vector(a);b=Vector(b);d=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=d.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 return o
# Tubular welded chassis: within .85 x 2.005m source footprint, floor origin retained.
for x in [-.389,.389]:
 for y,h in [(-.965,.68),(.965,.92)]:
  tube('Tubular leg',(x,y,.018),(x,y,h),.024,steel);box('Welded foot pad',(x,y,.014),(.066,.066,.028),steel,.007);tube('End cap',(x,y,h),(x,y,h+.012),.026,bolt)
 tube('Mattress side rail',(x,-.965,.365),(x,.965,.365),.023,steel)
 tube('Lower longitudinal brace',(x,-.94,.17),(x,.94,.17),.014,steel)
 for y in [-.94,.94]:
  for z in [.17,.365]:tube('Bracket bolt',(x-.012,y,z),(x+.012,y,z),.014,bolt,12)
for y,h in [(-.965,.68),(.965,.92)]:
 for z in [.365,h-.035]:tube('End frame rail',(-.389,y,z),(.389,y,z),.023,steel)
 for x in [-.21,0,.21]:tube('End vertical spindle',(x,y,.39),(x,y,h-.04),.012,steel)
for y in [-.83,-.59,-.35,-.11,.13,.37,.61,.85]:box('Steel mattress support slat',(0,y,.37),(.76,.04,.018),steel,.006)
for x in [-.36,.36]:
 for y in [-.9,.9]:tube('Corner diagonal brace',(x,y,.22),(x,y+(.19 if y<0 else -.19),.36),.012,steel)
box('Rounded ticking mattress',(0,0,.47),(.765,1.89,.19),linen,.065)
# Raised seam piping around the rounded mattress edge.
for z in [.42,.525]:
 for x in [-.365,.365]:tube('Longitudinal stitched piping',(x,-.86,z),(x,.86,z),.003,seam,10)
 for y in [-.91,.91]:tube('End stitched piping',(-.31,y,z),(.31,y,z),.003,seam,10)
 for y in [i*.055-.85 for i in range(32)]:
  for x in [-.369,.369]:tube('Short visible mattress stitches',(x,y,z),(x,y+.022,z),.0009,seam,6)
box('Soft rounded pillow',(0,.66,.625),(.57,.40,.15),linen,.065)
for x in [-.272,.272]:tube('Pillow case stitched edge',(x,.52,.625),(x,.79,.625),.002,seam,8)
# Woven blanket sheet: real folded and draped geometry, irregular wrinkles and rolled foot edge.
verts=[];faces=[];nx=40;ny=58
for j in range(ny+1):
 y=-.95+j/ny*1.25
 for i in range(nx+1):
  x=-.416+i/nx*.832;drop=max(0,abs(x)-.337)/.079*.18
  z=.582-drop+.009*math.sin(y*24+x*13)+.005*math.sin(x*52-y*9)
  z+=.035*math.exp(-((y-.27)/.045)**2)+.018*math.exp(-((y+.91)/.04)**2)
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  k=j*(nx+1)+i;faces.append((k,k+1,k+nx+2,k+nx+1))
mesh=bpy.data.meshes.new('Draped blanket woven topology');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Draped wrinkled blanket with folded hem',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(blanket)
for p in mesh.polygons:p.use_smooth=True
q=o.modifiers.new('Cloth thickness','SOLIDIFY');q.thickness=.004;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=q.name)
# Metric box UVs maintain small fabric weave across rounded mattress and blanket.
for o in list(bpy.context.scene.objects):
 if o.type=='MESH':
  uv=o.data.uv_layers.new(name='Metric fabric UV')
  for polygon in o.data.polygons:
   normal=polygon.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
   for li in polygon.loop_indices:
    v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]*5,v[axes[1]]*5)
objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box]
report={'name':'Original authored tubular prison single bed','license':'Project-authored geometry; Fabric030 ambientCG CC0 texture','texture_source':'https://ambientcg.com/view?id=Fabric030','bounds_blender_z_up':[(min(p[i] for p in pts),max(p[i] for p in pts)) for i in range(3)],'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objects),'status':'CONVERTED; final game visual review and regression pending'}
bpy.ops.object.select_all(action='SELECT');dest=O/'prison_bunk.glb';bpy.ops.export_scene.gltf(filepath=str(dest),export_format='GLB',use_selection=True);report['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();(O/'prison_bunk.json').write_text(json.dumps(report,indent=2))
source_dir=R/'asset_library/original_created/phase04';source_dir.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(source_dir/'prison_bunk.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.render.resolution_x=1100;s.render.resolution_y=850;s.render.resolution_percentage=100;s.world.color=(.24,.24,.24)
for loc,power in [((2,-2,4),650),((-2,1,3),450)]:
 l=bpy.data.objects.new('Preview area light',bpy.data.lights.new('Preview light','AREA'));s.collection.objects.link(l);l.location=loc;l.data.energy=power;l.data.size=3;l.rotation_euler=(Vector((0,0,.4))-l.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.objects.new('Preview camera',bpy.data.cameras.new('Preview camera'));s.collection.objects.link(cam);s.camera=cam;cam.location=(2.2,-2.8,1.9);cam.rotation_euler=(Vector((0,0,.4))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=45;s.render.filepath=str(O/'prison_bunk_preview.png');bpy.ops.render.render(write_still=True)


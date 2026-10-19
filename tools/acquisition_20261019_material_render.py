import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];M=R/'asset_library/manifests/acquisition_20261019';base=R/'assets/materials/acquisition_20261019';slugs=['Fabric030','concrete_wall_001','concrete_floor_worn_001','rusty_painted_metal','painted_concrete','denim_fabric'];results=[]
for slug in slugs:
 bpy.ops.wm.read_factory_settings(use_empty=True);p=base/slug
 if slug=='Fabric030':maps=dict(color=p/'Fabric030_2K-JPG_Color.jpg',normal=p/'Fabric030_2K-JPG_NormalGL.jpg',rough=p/'Fabric030_2K-JPG_Roughness.jpg')
 else:maps=dict(color=p/(slug+'_diff_2k.jpg'),normal=p/(slug+'_nor_gl_2k.jpg'),rough=p/(slug+'_rough_2k.jpg'),arm=p/(slug+'_arm_2k.jpg'))
 if not all(x.exists() for x in maps.values()):continue
 mat=bpy.data.materials.new(slug);mat.use_nodes=True;n=mat.node_tree.nodes;links=mat.node_tree.links;bs=n.get('Principled BSDF')
 for kind,path in maps.items():
  tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path));
  if kind!='color':tex.image.colorspace_settings.name='Non-Color'
  if kind=='color':links.new(tex.outputs['Color'],bs.inputs['Base Color'])
  elif kind=='rough':links.new(tex.outputs['Color'],bs.inputs['Roughness'])
  elif kind=='normal':
   normal=n.new('ShaderNodeNormalMap');links.new(tex.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],bs.inputs['Normal'])
  elif kind=='arm':
   sep=n.new('ShaderNodeSeparateColor');links.new(tex.outputs['Color'],sep.inputs['Color']);links.new(sep.outputs['Blue'],bs.inputs['Metallic'])
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32);obj=bpy.context.object;obj.data.materials.append(mat);bpy.ops.object.shade_smooth()
 sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=400;sc.render.resolution_y=400;sc.render.resolution_percentage=100;w=bpy.data.worlds.new('Studio');sc.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.4,.4,.4,1)
 for name,loc,power in [('Key',(2,-3,4),600),('Fill',(-3,-1,1),250)]:
  l=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));sc.collection.objects.link(l);l.location=loc;l.data.energy=power;l.data.size=3;l.rotation_euler=(-l.location).to_track_quat('-Z','Y').to_euler()
 cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.location=(0,-4,1.4);cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(M/(slug+'_actual_material.png'));bpy.ops.render.render(write_still=True);results.append(dict(asset=slug,image_count=len(maps),render=str(M/(slug+'_actual_material.png')),status='RENDERED; visual review pending'))
(M/'materials_blender_validation.json').write_text(json.dumps(dict(blender_version=bpy.app.version_string,results=results,godot_status='NOT TESTED'),indent=2))

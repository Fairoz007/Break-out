from pathlib import Path
p=Path('tools/phase04_architecture_bunk.py');s=p.read_text();start=s.index('for m in [linen,blanket]:');end=s.index('def box',start)
s=s[:start]+'''import numpy as np
for m in [linen,blanket]:
 n=m.node_tree.nodes;p=n.get('Principled BSDF')
 for suffix,socket in [('Color','Base Color'),('Roughness','Roughness'),('NormalGL','Normal')]:
  im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(R/f'assets/materials/acquisition_20261019/Fabric030/Fabric030_2K-JPG_{suffix}.jpg'),check_existing=False);im.image.scale(1024,1024)
  if suffix=='Color':
   pixels=np.empty(1024*1024*4,dtype=np.float32);im.image.pixels.foreach_get(pixels);pixels=pixels.reshape(-1,4);pixels[:,:3]*=np.array(m.diffuse_color[:3]);im.image.pixels.foreach_set(pixels.ravel());im.image.update()
  else:im.image.colorspace_settings.name='Non-Color'
  im.image.filepath_raw=str(O/f'prison_bunk_{m.name.split()[0]}_{suffix}.jpg');im.image.file_format='JPEG';im.image.save()
  if suffix=='NormalGL':
   normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.18;m.node_tree.links.new(im.outputs[0],normal.inputs['Color']);m.node_tree.links.new(normal.outputs[0],p.inputs['Normal'])
  else:m.node_tree.links.new(im.outputs[0],p.inputs[socket])
''' +s[end:]
a=s.index('# Bake generated fabric');b=s.index('objects=[',a)
s=s[:a]+'''# Metric box UVs maintain small fabric weave across rounded mattress and blanket.
for o in list(bpy.context.scene.objects):
 if o.type=='MESH':
  uv=o.data.uv_layers.new(name='Metric fabric UV')
  for polygon in o.data.polygons:
   normal=polygon.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
   for li in polygon.loop_indices:
    v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]*5,v[axes[1]]*5)
''' +s[b:];p.write_text(s)

import bpy, math, json, hashlib, pathlib
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'asset_library/extracted_sources/phase15_architecture'; SRC.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'assets/environments/phase15'; OUT.mkdir(parents=True,exist_ok=True)
PROP=ROOT/'assets/props/phase15'; PROP.mkdir(parents=True,exist_ok=True)
LIC=ROOT/'asset_library/licenses/phase15_architecture'; LIC.mkdir(parents=True,exist_ok=True)
(LIC/'LICENSE.md').write_text('Original procedural meshes authored for BREAKOUT: NO WAY BACK by Codex, 2026-10-18. Project owner may use, modify, distribute and commercially exploit these original meshes without attribution. Embedded Poly Haven textures concrete_wall_001 and rusty_metal_02 are CC0-1.0; original source/license evidence remains in project licenses. No third-party human likeness, trademarks or photographed portraits included. Procedural materials are original.\n')
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def material(name,color,metal=0,rough=.65,texture=None):
 m=bpy.data.materials.new(name); m.use_nodes=True; n=m.node_tree.nodes; bs=n.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=rough
 if texture:
  uv=n.new('ShaderNodeTexCoord'); mapping=n.new('ShaderNodeMapping'); m.node_tree.links.new(uv.outputs['Generated'],mapping.inputs['Vector']); mapping.inputs['Scale'].default_value=(2,2,2)
  for suffix,channel in [('diff','Base Color'),('rough','Roughness'),('nor_gl',None)]:
   p=ROOT/f'assets/materials/{texture}/{texture}_{suffix}_1k.png'
   if not p.exists(): continue
   im=n.new('ShaderNodeTexImage'); im.image=bpy.data.images.load(str(p),check_existing=True); im.projection='BOX'; im.projection_blend=.15
   m.node_tree.links.new(mapping.outputs['Vector'],im.inputs['Vector'])
   if channel: m.node_tree.links.new(im.outputs['Color'],bs.inputs[channel])
   else:
    im.image.colorspace_settings.name='Non-Color'; normal=n.new('ShaderNodeNormalMap'); normal.inputs['Strength'].default_value=.28; m.node_tree.links.new(im.outputs['Color'],normal.inputs['Color']); m.node_tree.links.new(normal.outputs['Normal'],bs.inputs['Normal'])
   if suffix=='rough': im.image.colorspace_settings.name='Non-Color'
 else:
  noise=n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=65; bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.14; bump.inputs['Distance'].default_value=.012; m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']); m.node_tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
 return m
con=material('Concrete_CC0',(.36,.37,.35),texture='concrete_wall_001'); steel=material('AgedSteel_CC0',(.25,.27,.25),.85,texture='rusty_metal_02')
paint=material('Institutional_Sage',(.18,.25,.23),.4); dark=material('BlackRubber',(.025,.03,.032),0,.9); white=material('Enamel',(.7,.72,.67),.15,.3); cloth=material('CoarseCanvas',(.34,.39,.37)); paper=material('AgedPaper',(.68,.65,.5)); red=material('SafetyRed',(.45,.04,.025),.2); glass=material('DarkGlass',(.025,.05,.06),.25,.15)
def box(name,loc,dim,mat=steel,bev=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=dim; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(mat)
 if bev:
  mod=o.modifiers.new('Manufactured_edge_radius','BEVEL'); mod.width=bev; mod.segments=2; o.modifiers.new('Weighted_normals','WEIGHTED_NORMAL')
 return o
def cyl(name,loc,r,depth,mat=steel,axis='Z'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=depth,location=loc); o=bpy.context.object; o.name=name
 if axis=='X': o.rotation_euler[1]=math.pi/2
 if axis=='Y': o.rotation_euler[0]=math.pi/2
 o.data.materials.append(mat); mod=o.modifiers.new('Edge_radius','BEVEL'); mod.width=.004; mod.segments=2; return o
def label(txt,loc,size=.08):
 bpy.ops.object.text_add(location=loc,rotation=(math.pi/2,0,0)); o=bpy.context.object; o.name='Label_'+txt; o.data.body=txt; o.data.size=size; o.data.extrude=.0003; o.data.materials.append(paper); bpy.ops.object.convert(target='MESH')
def legs(w,d,h):
 for x in [-w/2+.06,w/2-.06]:
  for y in [-d/2+.06,d/2-.06]:box('Welded_leg',(x,y,h/2),(.045,.045,h))
def panel(w=1,h=2.2):
 box('Door_leaf',(0,0,h/2),(w,.07,h),paint); box('Kickplate',(0,-.043,.2),(w-.08,.015,.3)); box('Lock',(w/2-.12,-.055,1.05),(.08,.04,.13)); cyl('Handle',(w/2-.12,-.085,1.05),.025,.16,axis='X')
 for z in [.25,h-.25]:cyl('Hinge',(-w/2+.02,0,z),.025,.15)
def bars(w,h):
 for x in [-w/2,w/2]:box('Frame',(x,0,h/2),(.06,.08,h))
 for z in [.04,h-.04]:box('Frame',(0,0,z),(w,.08,.08))
 for i in range(1,int(w/.13)):cyl('Vertical_bar',(-w/2+i*.13,0,h/2),.012,h-.12)
def controls(mode):
 box('Enclosed_switchgear',(0,0,.45),(.65,.25,.9),paint); box('Inset_face',(0,-.135,.47),(.56,.025,.72),dark)
 label(mode,( -.24,-.155,.68),.055)
 if mode=='A   B   C':
  cyl('Selector',(0,-.18,.46),.08,.05,axis='Y'); box('Pointer',(0,-.215,.49),(.025,.035,.11),white); label('OFF / ENERGIZE',(-.23,-.16,.2),.037)
 else:box('Brake_handle',(0,-.25,.4),(.3,.06,.05),red); label('HOLD / CLEAR',(-.22,-.16,.2),.04)
 for x in [-.25,.25]:
  for z in [.12,.8]:cyl('Fastener',(x,-.16,z),.012,.01,axis='Y')
records=[]
def export(name,bundle,mission,fn,prop=False):
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); fn(); objects=list(bpy.context.scene.objects)
 for o in objects:
  if o.type=='MESH':
   bpy.context.view_layer.objects.active=o; o.select_set(True)
   for mod in list(o.modifiers):
    try:bpy.ops.object.modifier_apply(modifier=mod.name)
    except:pass
   bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
   # Exporter requires UV for embedded PBR textures; cubic UV on each static component.
   bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.cube_project(cube_size=1); bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)
 for im in bpy.data.images:
  if im.filepath:
   try:im.pack()
   except:pass
 bpy.ops.object.select_all(action='SELECT')
 verts=[o.matrix_world@v.co for o in objects if o.type=='MESH' for v in o.data.vertices]; dims=[round(max(v[i] for v in verts)-min(v[i] for v in verts),4) for i in range(3)]
 blend=SRC/(name+'.blend'); bpy.ops.wm.save_as_mainfile(filepath=str(blend)); target=(PROP if prop else OUT)/(name+'.glb')
 bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
 r={'asset_id':'P15_'+name.upper(),'asset_name':name,'category':'prop' if prop else 'environment','source_url':None,'creator':'Original project procedural modeling by Codex','license':'Project-owned original meshes; embedded texture maps CC0-1.0','license_file':str((LIC/'LICENSE.md').relative_to(ROOT)).replace('\\','/'),'attribution_required':False,'original_file':str(blend.relative_to(ROOT)).replace('\\','/'),'original_checksum':hashlib.sha256(blend.read_bytes()).hexdigest(),'runtime_file':str(target.relative_to(ROOT)).replace('\\','/'),'runtime_checksum':hashlib.sha256(target.read_bytes()).hexdigest(),'format':'GLB','polygon_count_if_known':sum(len(o.data.polygons) for o in objects if o.type=='MESH'),'texture_resolution_if_known':'1024 where textured','skeleton_type_if_applicable':None,'animation_compatibility':'Static components separated and named; no animation clips','required_by_scene':[f'CH01_M{i:02}_SC01' for i in mission],'requirement_bundle':bundle,'download_status':'CREATED','import_status':'NOT TESTED','validation_status':'PARTIALLY_VERIFIED','dimensions_blender_xyz_m':dims,'notes':'Blender geometry/export validated. Godot import, collision, navigation, interaction hand alignment and visual approval pending. Metric Z-up source exported glTF Y-up. Detailed authored substitute, not final photoreal art.'}; records.append(r)
 print('ASSET_DONE',name,flush=True)
def make_wall():
 box('Concrete',(0,0,1.5),(4,.25,3),con); box('Painted_lower_band',(0,-.133,.65),(4,.018,1.3),paint); box('Skirting',(0,-.15,.08),(4,.05,.16));
 for x in [-1.96,1.96]:box('Expansion_joint',(x,-.14,1.5),(.018,.012,3),dark,.001)
export('wall_4m','ENV_CELLBLOCK',[1,4,6],make_wall)
export('floor_4m','ENV_CELLBLOCK',[1,2,3,4,5,6],lambda:box('Concrete_slab',(0,0,-.1),(4,4,.2),con))
export('ceiling_4m','ENV_CELLBLOCK',[1,3,4,5],lambda:[box('Ceiling',(0,0,0),(4,4,.16),con),box('Beam',(0,0,-.2),(.25,4,.4),con)])
export('corner_pier','ENV_CELLBLOCK',[1,4],lambda:[box('Pier',(0,0,1.5),(.6,.6,3),con),box('Impact_band',(0,-.31,.65),(.65,.05,1.3),paint)])
export('cell_bars_3m','ENV_CELLBLOCK',[1,4,6],lambda:bars(3,3))
export('cell_door_1m','ENV_CELLBLOCK',[1,4,6],lambda:[bars(1,2.2),box('Lockcase',(.35,-.06,1),(.18,.12,.25))])
export('security_door_12','ENV_CELLBLOCK',[1,4,6],lambda:panel(1.2))
export('double_spillway_door','ENV_MAINTENANCE',[5,6],lambda:[panel(2,2.5),cyl('Second_handle',(-.7,-.085,1.05),.025,.16,axis='X')])
export('service_hatch_11','ENV_CELLBLOCK',[4],lambda:panel(1.1,1.1))
def railing():
 for x in [-.95,0,.95]:box('Post',(x,0,.55),(.05,.05,1.1))
 for z in [.1,.55,1.08]:box('Rail',(0,0,z),(2,.05,.045))
export('railing_2m','ENV_MAINTENANCE',[5],railing)
export('catwalk_2m','ENV_MAINTENANCE',[5],lambda:[box('Deck',(0,0,-.06),(2,1.6,.12)),*[box('Anti_slip_rib',(x/10,0,.007),(.015,1.5,.014)) for x in range(-9,10)]])
def stair():
 for i in range(10):box('Tread',(0,i*.26,i*.18+.09),(1.6,.26,.18))
 for x in [-.75,.75]:
  beam=box('Stringer',(x,1.17,.8),(.06,3,.15)); beam.rotation_euler[0]=math.radians(35)
export('stairs_10_risers','ENV_MAINTENANCE',[5],stair)
def ladder():
 for x in [-.25,.25]:cyl('Stile',(x,0,1.4),.03,2.8)
 for i in range(10):cyl('Rung',(0,0,.15+i*.28),.018,.5,axis='X')
export('ladder_28','ENV_MAINTENANCE',[5],ladder)
def fence():
 for x in [-1,1]:cyl('Fence_post',(x,0,2.5),.05,5)
 for z in [.1,4.9]:cyl('Rail',(0,0,z),.025,2,axis='X')
 for x in range(-9,10):cyl('Welded_wire',(x*.1,0,2.5),.004,4.8)
 for z in range(1,50):cyl('Welded_wire',(0,0,z*.1),.004,2,axis='X')
export('fence_2x5','ENV_YARD',[2],fence)
export('yard_gate_2m','ENV_YARD',[2],lambda:[bars(2,3),box('Latch',(.8,-.06,1.1),(.25,.12,.1))])
export('barred_window','ENV_CELLBLOCK',[1,4],lambda:[bars(1.2,.8),box('Sill',(0,0,-.05),(1.4,.4,.1),con)])
def table(w=1.4,d=.7,h=.75):box('Top',(0,0,h),(w,d,.07),paint); legs(w,d,h)
export('intake_counter','ENV_INTAKE',[1],lambda:[box('Counter',(0,0,.5),(2.4,.7,1),paint),box('Steel_top',(0,0,1.03),(2.5,.8,.06)),box('Document_tray',(.6,0,1.08),(.35,.27,.03))],True)
export('steel_table','ENV_WORKSHOP',[2,3],table,True)
export('steel_chair','ENV_WORKSHOP',[1,3],lambda:[box('Seat',(0,0,.45),(.43,.43,.05),paint),legs(.43,.43,.45),box('Back',(0,.2,.72),(.43,.045,.5),paint)],True)
export('yard_bench','ENV_YARD',[2],lambda:table(2,.45,.45),True)
export('cell_bed','ENV_CELLBLOCK',[1,4,6],lambda:[box('Bed_pan',(0,0,.4),(.85,2,.08)),legs(.85,2,.4),box('Headboard',(0,.98,.65),(.85,.05,.6),paint)],True)
export('mattress','ENV_CELLBLOCK',[1,4],lambda:[box('Mattress',(0,0,.09),(.8,1.9,.18),cloth,.065),box('Pillow',(0,.65,.2),(.55,.35,.12),cloth,.05)],True)
export('locker','ENV_CELLBLOCK',[1,3],lambda:[box('Locker_shell',(0,0,.9),(.5,.5,1.8),paint),box('Door',(0,-.26,.9),(.46,.025,1.75),paint),*[box('Vent',(0,-.28,1.5+i*.04),(.3,.01,.012),dark,.001) for i in range(4)],box('Handle',(.15,-.3,.9),(.025,.05,.15))],True)
def basin():
 box('Pedestal',(0,.05,.4),(.25,.25,.8),white); box('Bowl',(0,0,.82),(.58,.45,.12),white,.06); box('Recess',(0,-.02,.884),(.42,.3,.012),dark,.04); cyl('Faucet',(0,.16,.97),.018,.2)
export('sink','ENV_CELLBLOCK',[1,4],basin,True)
export('toilet','ENV_CELLBLOCK',[1,4,6],lambda:[box('Pedestal',(0,0,.2),(.3,.4,.4),white,.07),box('Bowl',(0,-.12,.43),(.42,.62,.16),white,.1),box('Seat_opening',(0,-.15,.518),(.25,.36,.012),dark,.09),box('Cistern',(0,.24,.65),(.4,.17,.45),white,.04)],True)
def washer():
 box('Body',(0,0,.6),(1,.85,1.2),paint); cyl('Door_rim',(0,-.45,.55),.36,.08,axis='Y'); cyl('Window',(0,-.5,.55),.29,.02,glass,'Y'); box('Control_strip',(0,-.44,1.05),(.85,.03,.15),dark); label('INDUSTRIAL 08',(-.36,-.465,1.02),.055)
export('laundry_washer','ENV_WORKSHOP',[3],washer,True)
def press():
 box('Base',(0,0,.2),(1.8,1.1,.4),paint); box('Platen',(0,0,1.05),(1.8,1.1,.15));
 for x in [-.7,.7]:box('Column',(x,.35,1.1),(.15,.15,1.8),paint)
 box('Crosshead',(0,.35,1.95),(1.8,.3,.25),paint); cyl('Ram',(0,.35,1.5),.1,.65); box('Isolation_handle',(.8,-.65,1.1),(.3,.05,.05),red); bars(1.5,.65)
export('laundry_press','ENV_WORKSHOP',[3],press,True)
export('electrical_panel','PROP_RELAY',[5],lambda:controls('A   B   C'),True)
export('brake_station','PROP_RELAY',[5],lambda:controls('BRAKE'),True)
export('service_panel','ENV_CELLBLOCK',[4],lambda:[box('Removable_panel',(0,0,.55),(.8,.04,1.1),paint),*[cyl('Captive_bolt',(x,-.028,z),.012,.012,axis='Y') for x in [-.35,.35] for z in [.08,1.02]]],True)
export('pipe_straight_2m','ENV_MAINTENANCE',[5],lambda:[cyl('Pipe',(0,0,1),.08,2),*[cyl('Flange',(0,0,z),.12,.045) for z in [.05,1.95]]],True)
export('cctv_camera','ENV_INTAKE',[1,4],lambda:[box('Camera_body',(0,0,0),(.18,.35,.15),white),cyl('Lens',(0,-.19,0),.045,.05,glass,'Y'),box('Mount',(0,.17,-.1),(.05,.18,.2))],True)
export('floodlight','ENV_YARD',[2],lambda:[box('Housing',(0,0,0),(.6,.16,.4)),box('Reflector',(0,-.09,0),(.53,.015,.33),white),box('Bracket',(0,.12,-.2),(.04,.3,.3))],True)
export('fluorescent_fixture','ENV_CELLBLOCK',[1,3,4],lambda:[box('Housing',(0,0,0),(1.2,.22,.1),paint),*[cyl('Tube',(0,y,-.08),.022,1.05,white,'X') for y in [-.055,.055]],*[box('Cage',(x,0,-.12),(.015,.23,.02)) for x in [-.5,-.25,0,.25,.5]]],True)
export('guard_radio','ENV_INTAKE',[1,4,6],lambda:[box('Body',(0,0,.075),(.065,.035,.15),dark),cyl('Antenna',(.02,0,.2),.004,.15,dark),*[box('Speaker_slot',(0,-.02,.09+i*.008),(.04,.004,.003)) for i in range(5)]],True)
export('wired_handset','PROP_RELAY',[5],lambda:[box('Receiver',(0,0,.1),(.04,.045,.2),dark),*[box('Earpiece',(0,-.01,z),(.065,.06,.045),dark) for z in [.02,.18]],*[cyl('Coiled_cable',(0,.012,-.025-i*.009),.016,.004,dark) for i in range(20)]],True)
export('spring_shim','PROP_SHIM',[3,4,6],lambda:box('Spring_strip',(0,0,.001),(.018,.14,.002),steel,.0005),True)
export('photo_sleeve_empty','PROP_PHOTO',[1,2],lambda:[box('Backing',(0,0,0),(.1,.001,.14),paper,.001),*[box('Sleeve_edge',(x,-.002,0),(.004,.002,.14),dark,.001) for x in [-.05,.05]]],True)
export('vantage_badge','PROP_VANTAGE_BADGE',[1],lambda:[box('Seal',(0,0,.04),(.065,.006,.08),paint,.005),label('V',(-.023,-.004,.025),.05)],True)
export('transfer_ledger','PROP_LEDGER',[5,6],lambda:[box('Folder',(0,0,.01),(.3,.4,.02),paint),box('Paper',(0,0,.022),(.27,.37,.004),paper),label('TRANSFER / 17',(-.12,-.002,.025),.025)],True)
export('inspection_lamp','ENV_WORKSHOP',[3],lambda:[cyl('Grip',(0,0,.08),.025,.16,dark),cyl('Lamp',(0,0,.24),.045,.17,white),*[cyl('Cage',(x,0,.24),.004,.2) for x in [-.05,.05]]],True)
export('scrap_bin','ENV_WORKSHOP',[3],lambda:[box('Bin',(0,0,.35),(.5,.45,.7),paint),box('Dark_opening',(0,0,.705),(.42,.37,.01),dark)],True)
export('linen_trolley','ENV_WORKSHOP',[3],lambda:[box('Basket',(0,0,.65),(.8,.6,.65),cloth),box('Frame',(0,0,.25),(.85,.65,.08)),*[cyl('Wheel',(x,y,.12),.1,.05,dark,'X') for x in [-.35,.35] for y in [-.25,.25]]],True)
export('water_tap','ENV_YARD',[2],lambda:[cyl('Pipe',(0,0,.6),.025,1.2),cyl('Spout',(0,-.1,1.17),.02,.2,axis='Y'),box('Valve',(0,0,1.27),(.15,.025,.025),red)],True)
export('drain_grate','ENV_YARD',[2],lambda:[box('Frame',(0,0,-.025),(.6,.4,.05)),*[box('Slot',(x*.05,0,.002),(.023,.32,.008),dark,.002) for x in range(-5,6)]],True)
export('mechanical_latch','ENV_MAINTENANCE',[5],lambda:[box('Housing',(0,0,.15),(.35,.2,.3),paint),box('Bolt',(.23,0,.15),(.3,.08,.08)),cyl('Pin',(.3,0,.2),.025,.2)],True)
export('dual_door_handle','ENV_MAINTENANCE',[5,6],lambda:[*[cyl('Pull',(x,-.05,.2),.02,.4) for x in [-.7,.7]],*[box('Mount',(x,0,z),(.06,.12,.04)) for x in [-.7,.7] for z in [.02,.38]]],True)
(ROOT/'asset_library/manifests/phase15_architecture.json').write_text(json.dumps(records,indent=2))
print('COMPLETE',len(records),flush=True)

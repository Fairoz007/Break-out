"""Original metric security door assembly. Blender 5.1; no third-party geometry.
Reuses Phase03 bevel/export utilities and runtime P3 material slots.
Run: blender -b --python tools/phase04_cell_hardware.py -- assets/props/phase04_cellblock
"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import phase03_props_build as p
import bpy

out = os.path.abspath(sys.argv[sys.argv.index('--')+1])
os.makedirs(out, exist_ok=True)
p.OUT = out
bpy.ops.wm.read_factory_settings(use_empty=True)
p.PARTS.clear()
# 920 x 2100 mm leaf; welded 55 mm frame. Front is Blender -Y / Godot +Z.
for x in [-.49,.49]: p.box((.055,.115,2.20),(x,0,1.10),'P3_PaintSteelDark')
p.box((1.035,.115,.055),(0,0,2.175),'P3_PaintSteelDark')
p.box((.91,.045,2.08),(0,0,1.05),'P3_PaintSteelGrey',bevel=.006,segs=3)
# Vision panel has a recessed dark gasket, protective grille, separate steel surround.
p.box((.235,.012,.50),(0,-.028,1.58),'P3_Rubber',bevel=.008,segs=3)
p.box((.185,.012,.45),(0,-.036,1.58),'P3_Glass',bevel=.004)
for x in [-.126,.126]: p.box((.026,.028,.55),(x,-.048,1.58),'P3_Stainless')
for z in [1.318,1.842]: p.box((.278,.028,.026),(0,-.048,z),'P3_Stainless')
for x in [-.058,0,.058]: p.cyl(.008,.46,(x,-.063,1.58),'P3_PaintSteelDark',bevel=.001)
for z in [1.43,1.58,1.73]: p.box((.185,.016,.012),(0,-.065,z),'P3_PaintSteelDark',bevel=.002)
# Food pass: recessed frame, bevelled shut flap, continuous pin hinge and latch.
p.box((.39,.015,.20),(0,-.030,1.02),'P3_Rubber')
p.box((.35,.018,.16),(0,-.044,1.02),'P3_Stainless',bevel=.004)
p.cyl(.012,.37,(0,-.062,.932),'P3_Chrome',rot=(0,90,0),bevel=.001)
p.box((.055,.028,.030),(.14,-.068,1.095),'P3_PaintSteelDark',bevel=.003)
# Lock escutcheon, key cylinder, offset pull and three welded hinge barrels.
p.box((.085,.018,.225),(.34,-.037,1.12),'P3_Stainless')
p.cyl(.017,.022,(.34,-.056,1.18),'P3_Brass',rot=(90,0,0),bevel=.002)
p.box((.003,.003,.014),(.34,-.069,1.18),'P3_Rubber',bevel=0)
p.tube([(.34,-.053,1.04),(.34,-.095,1.04),(.34,-.095,1.125),(.34,-.053,1.125)],.011,'P3_Stainless')
for z in [.30,1.06,1.83]:
    p.box((.09,.018,.13),(-.425,-.036,z),'P3_PaintSteelDark')
    p.cyl(.021,.15,(-.466,-.057,z),'P3_Stainless',bevel=.002)
    for zz in [z-.052,z+.052]: p.torus(.022,.002,(-.466,-.057,zz),'P3_Chrome',maj=20,mino=6)
# Recessed vent at the base, individually angled louvres, kick plate and fixing heads.
p.box((.48,.012,.24),(0,-.03,.42),'P3_Rubber')
for i in range(7): p.box((.46,.026,.018),(0,-.045,.325+i*.031),'P3_PaintSteelGrey',rot=(22,0,0),bevel=.002)
p.box((.82,.012,.16),(0,-.034,.12),'P3_Stainless',bevel=.003)
p.screws([(x,-.066,z) for x in [-.125,.125] for z in [1.32,1.84]])
p.screws([(x,-.044,z) for x in [-.38,.38] for z in [.07,.17]])
obj, info = p.finalize('tier_security_door')
info['license']='Original project geometry; project-owned'
info['source']='tools/phase04_cell_hardware.py'
info['sha256']=hashlib.sha256(open(os.path.join(out,'tier_security_door.glb'),'rb').read()).hexdigest()
with open(os.path.join(out,'asset_record.json'),'w') as f: json.dump(info,f,indent=2)
p.render_preview(obj,os.path.join(out,'inspection.png'))

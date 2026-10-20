"""Repair rejected pole-stepped basketball using smooth independent rubber channel meshes."""
import bpy,sys,math,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import phase03_props_build as p
OUT=ROOT/'assets/props/phase04_realistic';p.OUT=str(OUT)
bpy.ops.wm.read_factory_settings(use_empty=True);p.PARTS.clear()
p.MATS['P4_BallLeather']=((.48,.135,.028),0,.8,{})
p.MATS['P4_BallChannel']=((.018,.012,.008),0,.85,{})
r=.749/(2*math.pi)
bpy.ops.mesh.primitive_uv_sphere_add(segments=192,ring_count=96,radius=r,location=(0,0,r))
ball=bpy.context.object;ball.name='Size7 continuous recessed channel leather shell'
ball.data.materials.append(p.material('P4_BallLeather'))
for v in ball.data.vertices:
    direction=v.co.normalized()
    d=min(abs(direction.x),abs(direction.y),abs(direction.z))
    channel=max(0,1-d/.021)
    v.co=direction*(r-.0012*channel)
for f in ball.data.polygons:f.use_smooth=True
p.PARTS.append(ball)
# Analytic great-circle rubber inserts; no material boundaries following latitude faces.
for rotation in [(0,0,0),(90,0,0),(0,90,0)]:
    p.torus(r-.00095,.00115,(0,0,r),'P4_BallChannel',rot=rotation,maj=256,mino=12)
ball,info=p.finalize('basketball_recessed_channels')
path=OUT/'basketball_recessed_channels.glb'
info.update({'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':'Original project-authored geometry','license':'Original project-authored geometry','status':'CONVERTED','diameter_m':r*2,'revision':'Replaced rejected face-classified seams with smooth independent analytic circular rubber inserts in recessed shell; no pole stepping. Eight spherical panels.','integration':'scripts/missions/mission_02.gd asset path change only; same floor origin and size; gameplay regression required.'})
(OUT/'basketball_recessed_channels.asset_record.json').write_text(json.dumps(info,indent=2))
p.render_preview(ball,str(OUT/'basketball_recessed_channels_preview.png'))

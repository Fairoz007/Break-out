"""Preserve completed Mixamo UI downloads and create incremental accurate inventory."""
from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parents[1];S=Path.home()/'Downloads';O=R/'asset_library/original_downloads/animations/mixamo_20261019';M=R/'asset_library/manifests/mixamo_20261019';O.mkdir(parents=True,exist_ok=True);M.mkdir(parents=True,exist_ok=True)
known=['Unarmed Turn Right 90','Kneeling Down','Kneeling Inspecting','Talking','Standing Arguing','Pointing Forward','Open Door Outwards','Closing','Opening Door Inwards','Unarmed Turn Left 90','Pull Heavy Object','Pull Heavy Object Start','Pull Heavy Object Stop','Pulling Lever','Closing Door','Open Door','Jumping','Climbing','Climb','Vault','Picking Up','Sitting Down','Getting Up','Standing Up','Punching','Talking','Looking Around','Helping','Assisted Climb']
for p in S.glob('*.fbx'):
 if p.stem not in known:continue
 dst=O/p.name
 if not dst.exists():shutil.copy2(p,dst)
 assert hashlib.sha256(dst.read_bytes()).digest()==hashlib.sha256(p.read_bytes()).digest()
rows=[]
for p in sorted(O.glob('*.fbx')):
 b=p.read_bytes(); assert b.startswith(b'Kaydara FBX Binary')
 rows.append(dict(asset_id='MIXAMO_'+p.stem.upper().replace(' ','_'),name=p.stem,category='animations',source_website='Adobe Mixamo',source_url='https://www.mixamo.com/#/?query='+p.stem.replace(' ','+'),source_url_note='Search URL derived from UI clip title, not a permanent item identifier',creator='Adobe Mixamo',license='Adobe Mixamo royalty-free commercial video-game usage; official FAQ evidence saved',license_url='https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html',commercial_use=True,download_date='2026-10-19',original_filename=p.name,local_path=str(p.relative_to(R)),size_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),model_format='FBX Binary',texture_resolution='NOT TESTED',rigged_status='NOT TESTED',animation_status='FBX header verified; Blender actions NOT TESTED',godot_import_status='NOT TESTED',visual_inspection_status='NOT TESTED',related_missions=['Chapter 1 interaction/locomotion candidates; exact contacts require staging'],remaining_issues='Retarget and choreography review required. Default character reference does not satisfy final protagonist identity. Raw files internal project dependency only.'))
(M/'inventory.json').write_text(json.dumps(rows,indent=2));print(len(rows),'verified FBX originals')



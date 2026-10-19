"""Create a current inventory without overwriting the Phase 01.5 authority."""
from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parents[1];D=R/'asset_library/manifests/acquisition_20261019'
old=json.loads((R/'asset_library/manifests/assets.json').read_text(encoding='utf-8-sig'))
audit=json.loads((D/'baseline_audit.json').read_text());checked={a['asset_id']:a for a in audit['assets']}
new=[]
for name in ['props_materials_inventory.json','materials_2k_inventory.json','radio_inventory.json','sketchfab_inventory.json','yaesu_inventory.json']:
 p=D/name
 if p.exists():new+=json.loads(p.read_text(encoding='utf-8-sig'))
mix=R/'asset_library/manifests/mixamo_20261019/inventory.json'
if mix.exists():
 for a in json.loads(mix.read_text(encoding='utf-8-sig')):
  new.append({**a,'asset_name':a.get('name',a['asset_id']),'asset_category':'animations',
   'commercial_use_status':'PERMITTED for commercial game; raw source redistribution restricted',
   'local_file_path':a.get('local_path'),'file_size':a.get('size_bytes'),
   'converted_file':a.get('converted_path'),
   'license_record':'asset_library/licenses/mixamo_20261019/LICENSE_RECORD.md',
   'related_mission':a.get('related_missions'),'files':[{'local_file_path':a['local_path'],'file_size':a['size_bytes'],'sha256':a['sha256']}]})
rows=[]
for a in old:
 aid=a['asset_id'];v=checked[aid]
 rows.append({'asset_id':aid,'asset_name':a.get('asset_name',aid),'asset_category':a.get('category'),
 'source_website':a.get('source_website'),'source_url':a.get('source_url'),'creator':a.get('creator'),'license':a.get('license'),
 'commercial_use_status':'SEE LICENSE RECORD; NOT RE-EVALUATED' if a.get('license') else 'NOT RECORDED',
 'download_date':a.get('download_date','NOT RECORDED'),'original_filename':a.get('original_file'),
 'local_file_path':a.get('runtime_file'),'file_size':sum(f.get('bytes',0) for f in v['runtime_files']),
 'sha256':{f['path']:f.get('sha256') for f in v['runtime_files']},'model_format':a.get('format'),
 'texture_resolution':a.get('texture_resolution_if_known'),'rigged_status':a.get('skeleton_type_if_applicable'),
 'animation_status':a.get('animation_compatibility'),'godot_import_status':a.get('import_status'),
 'visual_inspection_status':a.get('validation_status'),'related_mission':a.get('required_by_scene'),
 'remaining_issues':a.get('production_gap',a.get('notes')),'license_record':v.get('license_record'),
 'record_scope':'EXISTING; import/visual statuses historical; current files rehashed 2026-10-19',
 'current_file_checks':v['runtime_files'],'original_manifest_record':a})
facial=R/'asset_library/converted/acquisition_20261019/rocketbox_facial/conversion_inventory.json'
if facial.exists():
 for name,a in json.loads(facial.read_text()).items():
  new.append({**a,'asset_name':name+' facial derivative','asset_category':'characters','source_website':'Microsoft GitHub',
   'commercial_use_status':a['commercial_use'],'download_date':'EXISTING SOURCE; converted 2026-10-19',
   'original_filename':a['source_file'],'local_file_path':a['file'],'file_size':a['bytes'],
   'model_format':'GLB','texture_resolution':'Existing embedded character textures; see source record',
   'rigged_status':f"{a['bones']} bones; 175 facial targets",'animation_status':f"{a['actions']} body actions; facial performance missing",
   'related_mission':['CH01_M01','CH01_M02','CH01_M03','CH01_M04','CH01_M05','CH01_M06']})
for a in new:
 a['asset_category']=a.get('asset_category',a.get('category','NOT RECORDED'))
 a['license_record']=a.get('license_record',a.get('official_metadata','NOT RECORDED'))
 a.setdefault('godot_import_status','NOT TESTED')
 a.setdefault('model_format','NOT RECORDED')
 staged=D/'runtime_staging.json'
 if staged.exists():
  hit=next((s for s in json.loads(staged.read_text()) if s['asset_id']==a['asset_id']),None)
  if hit:a['runtime_staging']=hit
 if a['asset_id']=='ACQ26_YAESU_RADIO':
  probe=json.loads((D/'yaesu_blender_validation.json').read_text())
  a.update({'converted_file':probe['converted_file'],'converted_sha256':probe['converted_sha256'],'converted_size':probe['converted_size'],
   'visual_inspection_status':'Actual Blender front render inspected by acquisition and independent QA; rear view NOT TESTED',
   'remaining_issues':'Single radio derivative extracted from presentation; body height 95mm per manufacturer reference. Holster/hand attachment, branding, LOD and scene tests pending.'})
  ev=R/'asset_library/converted/acquisition_20261019/material_validation/godot_report.json'
  if ev.exists():
   match=next((r for r in json.loads(ev.read_text())['resources'] if 'radio_yaesu_single' in r['path']),None)
   if match and match.get('loaded'):a['godot_import_status']='PASS isolated Godot 4.7.2 load/instantiate; rendered gameplay NOT TESTED'
 if a['asset_id'].startswith('ACQ26_2K_') or a['asset_id'] in ['ACQ26_SIGNAL_FLASHLIGHT','ACQ26_FABRIC030']:
  ev=R/'asset_library/converted/acquisition_20261019/material_validation/godot_report.json'
  if ev.exists():
   report=json.loads(ev.read_text())
   if not report['failed']:a['godot_import_status']='PASS isolated Godot 4.7.2 bound texture/resource validation; gameplay NOT TESTED'
 if a['asset_id']=='ACQ26_RADIO_EVALUATION':
  a.update({'visual_inspection_status':'REJECTED FOR REQUESTED REALISTIC TEXTURED ART','texture_resolution':'NONE; archive contains OBJ and flat Phong MTL only',
   'commercial_use_status':'AMBIGUOUS creator terms vs CC0 update; NOT CLEARED',
   'remaining_issues':'No texture maps; art unsuitable. Conflicting creator redistribution/credit terms preserved. Evaluation archive only; not installed in runtime assets.'})
 rows.append({**a,'record_scope':'2026-10-19 session; see scoped validation reports'})
assert len({r['asset_id'] for r in rows})==len(rows),'Duplicate IDs'
(D/'inventory.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
fields=['asset_id','asset_name','asset_category','source_website','source_url','creator','license','commercial_use_status','download_date','original_filename','local_file_path','file_size','sha256','model_format','texture_resolution','rigged_status','animation_status','godot_import_status','visual_inspection_status','related_mission','remaining_issues','license_record','record_scope']
with (D/'inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
 for a in rows:w.writerow({k:json.dumps(a.get(k),ensure_ascii=False) if isinstance(a.get(k),(list,dict)) else a.get(k) for k in fields})
print(json.dumps({'existing':len(old),'session_records':len(new),'consolidated':len(rows)}))


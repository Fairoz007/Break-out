from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1];M=R/'asset_library/manifests';D=M/'phase15'
D.mkdir(exist_ok=True);(D/'previews').mkdir(exist_ok=True)
sources=['phase15_architecture.json','phase15_bulk_assets.json','phase15_bulk_oga_assets.json','phase15_props_records.json','phase15_ui_records.json','phase15_original_audio.json','phase15_characters_records.json','phase15_critical_records.json','phase15_discovery_records.json']
records=[]
for source in sources:
    p=M/source
    if p.exists():
        fragment=json.loads(p.read_text(encoding='utf-8-sig'))
        records.extend(fragment)
ids=[x['asset_id'] for x in records]
if len(ids)!=len(set(ids)):raise RuntimeError('Duplicate new asset IDs')
jobs=[];seen=set();errors=[]
for record in records:
    if '--no-characters' in sys.argv and ('characters/phase15/' in str(record.get('runtime_file')) or 'animations/phase15/' in str(record.get('runtime_file'))):continue
    paths=record.get('runtime_file') or [];paths=[paths] if isinstance(paths,str) else paths
    for i,path in enumerate(paths):
        p=R/path
        if not p.exists():errors.append(record['asset_id']+' missing '+path);continue
        if p.suffix.lower() not in ['.glb','.gltf','.ogg','.wav','.mp3','.png','.jpg','.jpeg','.svg','.tres','.ttf']:continue
        if path in seen:continue
        seen.add(path)
        jobs.append({'asset_id':record['asset_id'] if len(paths)==1 else record['asset_id']+'_DEP'+str(i),'owner_asset_id':record['asset_id'],'path':'res://'+path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'validation_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'fragment_snapshot.json').write_text(json.dumps(records,indent=2))
print(len(records),'new records',len(jobs),'resource jobs',errors)
if errors:raise RuntimeError('Missing paths')

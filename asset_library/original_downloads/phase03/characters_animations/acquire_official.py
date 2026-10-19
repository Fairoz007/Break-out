import urllib.request,urllib.parse,json,hashlib,concurrent.futures
from pathlib import Path
r=Path('asset_library/original_downloads/phase03/characters_animations');d=json.loads((r/'official_tree.json').read_text());sha=d['sha']
names={'m_knock_door.max.fbx','m_listen_door.max.fbx','m_documents_check.max.fbx','m_documents_take.max.fbx','m_documents_note.max.fbx','m_sit_chair_idle_nervous_01.max.fbx','m_sit_chair_idle_look_around.max.fbx','m_sit_down_chair_01.max.fbx','m_sit_stand_up_chair_01.max.fbx','m_gestic_talk_sad_01.max.fbx'}
selected=[x for x in d['tree'] if x['type']=='blob' and (('/Animations/' in x['path'] and Path(x['path']).name in names) or 'Assets/Avatars/Professions/Security_Female_01/' in x['path'] or x['path']=='LICENSE.md')]
def get(x):
 path=x['path'];local=r/'microsoft_rocketbox'/path;p=local;p.parent.mkdir(parents=True,exist_ok=True);url='https://raw.githubusercontent.com/microsoft/Microsoft-Rocketbox/'+sha+'/'+urllib.parse.quote(path)
 if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=120).read())
 b=p.read_bytes();git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();ok=git==x['sha'] and len(b)==x['size'];return {'source_path':path,'local_path':str(local),'source_url':url,'license':'MIT','license_path':str(r/'microsoft_rocketbox/LICENSE.md'),'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'official_git_blob':x['sha'],'git_blob_verified':ok,'status':'SOURCE VERIFIED; Blender/Godot/visual NOT TESTED'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: records=list(ex.map(get,selected))
(r/'new_acquisition_inventory.json').write_text(json.dumps(records,indent=2));print('FILES',len(records),'BYTES',sum(x['size_bytes'] for x in records),'ALL_VERIFIED',all(x['git_blob_verified'] for x in records))

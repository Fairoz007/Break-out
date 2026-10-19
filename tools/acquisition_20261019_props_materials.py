from pathlib import Path
import urllib.request,json,time,hashlib,zipfile,shutil
from PIL import Image
R=Path.cwd(); tag='acquisition_20261019'; M=R/'asset_library/manifests'/tag; L=R/'asset_library/licenses'/tag;M.mkdir(parents=True,exist_ok=True);L.mkdir(parents=True,exist_ok=True)
def fetch(u):
 q=urllib.request.Request(u,headers={'User-Agent':'Breakout-No-Way-Back/20261019 (Powered by Poly Haven)'});return urllib.request.urlopen(q,timeout=120).read()
def save(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=d:raise ValueError('would overwrite '+str(p))
 p.write_bytes(d)
def file_record(p,u):return dict(local_file_path=p.relative_to(R).as_posix(),source_url=u,file_size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
records=[];errors=[]
def checkpoint():
 (M/'props_materials_inventory.json').write_text(json.dumps(records,indent=2),encoding='utf8');(M/'props_materials_checkpoint.json').write_text(json.dumps(dict(completed=[x['asset_id'] for x in records],failed=errors,pending_conversions=[x['asset_id'] for x in records],godot_validation='NOT TESTED',next_action='Blender conversion and Godot import; acquire exact guard handheld radio, keys and restraints'),indent=2),encoding='utf8')
for provider,url in [('polyhaven','https://polyhaven.com/license'),('ambientcg','https://docs.ambientcg.com/license/')]:
 try:save(L/(provider+'_license.html'),fetch(url))
 except Exception as e:errors.append(dict(stage='license',source=url,error=str(e)))
try:
 slug='signal_flashlight';meta=json.loads(fetch('https://api.polyhaven.com/files/'+slug));time.sleep(1.2);info=json.loads(fetch('https://api.polyhaven.com/info/'+slug));save(L/(slug+'_info.json'),json.dumps(info,indent=2).encode());save(M/(slug+'_files.json'),json.dumps(meta,indent=2).encode()); f=meta['gltf']['2k']['gltf'];entries={Path(f['url']).name:f,**f['include']}; files=[];dest=R/'asset_library/original_downloads/props'/tag/slug
 for rel,v in entries.items():
  p=dest/rel;d=p.read_bytes() if p.exists() else fetch(v['url']);assert hashlib.md5(d).hexdigest()==v['md5'];save(p,d);files.append(file_record(p,v['url']))
 g=json.loads((dest/Path(f['url']).name).read_text());uris=[x['uri'] for x in g.get('buffers',[])]+[x['uri'] for x in g.get('images',[])];assert all((dest/u).is_file() for u in uris)
 for im in g.get('images',[]):
  with Image.open(dest/im['uri']) as image:image.verify()
 runtime=R/'assets/props'/tag/slug;shutil.copytree(dest,runtime,dirs_exist_ok=True)
 records.append(dict(asset_id='ACQ26_SIGNAL_FLASHLIGHT',asset_name='Signal Flashlight',asset_category='props',source_website='Poly Haven',source_url='https://polyhaven.com/a/'+slug,creator=info.get('authors'),license='CC0-1.0',commercial_use_status='PERMITTED',license_record=str((L/'polyhaven_license.html').relative_to(R)),download_date='2026-10-19',original_filename=Path(f['url']).name,local_file_path=str(dest.relative_to(R)),file_size=sum(x['file_size'] for x in files),sha256=files[0]['sha256'],model_format='glTF 2.0 + BIN',texture_resolution='2048x2048',rigged_status='static',animation_status='none',godot_import_status='NOT TESTED',visual_inspection_status='Official realistic preview inspected; actual render pending',related_mission=['CH01_M03','CH01_M04','CH01_M05'],remaining_issues='Vintage signal device; practical inspection/emergency lamp candidate. Not a modern tactical torch. Grip, scale and light emitter need validation. Branding review.',archive_integrity='N/A individual files; every provider MD5 matched',dependency_verification='All glTF image and buffer paths exist; image decoding PASS',files=files,runtime_path=str(runtime.relative_to(R))))
 print('DOWNLOADED signal flashlight',flush=True)
except Exception as e:errors.append(dict(asset='signal_flashlight',error=str(e)))
checkpoint()
try:
 slug='Fabric030';url='https://ambientcg.com/get?file=Fabric030_2K-JPG.zip';p=R/'asset_library/original_downloads/materials'/tag/'Fabric030_2K-JPG.zip';d=p.read_bytes() if p.exists() else fetch(url);save(p,d);dest=R/'asset_library/extracted_sources'/tag/slug;dest.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  for n in z.namelist():
   target=(dest/n).resolve();assert target.is_relative_to(dest.resolve())
  z.extractall(dest)
 files=[file_record(p,url)]
 for f in dest.rglob('*'):
  if f.is_file():
   files.append(file_record(f,url))
   if f.suffix.lower() in ['.png','.jpg']:
    with Image.open(f) as im:im.verify()
 runtime=R/'assets/materials'/tag/slug;shutil.copytree(dest,runtime,dirs_exist_ok=True)
 records.append(dict(asset_id='ACQ26_FABRIC030',asset_name='Grey woven cloth PBR',asset_category='materials',source_website='ambientCG',source_url='https://ambientcg.com/view?id=Fabric030',creator='Lennart Demes / ambientCG',license='CC0-1.0',commercial_use_status='PERMITTED',license_record=str((L/'ambientcg_license.html').relative_to(R)),download_date='2026-10-19',original_filename=p.name,local_file_path=str(p.relative_to(R)),file_size=p.stat().st_size,sha256=files[0]['sha256'],model_format='PBR texture set (JPG)',texture_resolution='2048x2048',rigged_status='N/A',animation_status='N/A',godot_import_status='NOT TESTED',visual_inspection_status='Official preview inspected; realistic coarse weave. Actual shader rendering pending.',related_mission=['CH01_M01','CH01_M03','CH01_M04','CH01_M06'],remaining_issues='Bind to blanket/linen meshes, calibrate UV weave scale. Not a complete linen stack model.',archive_integrity='ZIP CRC PASS and paths safe',dependency_verification='Image decoding PASS',files=files,runtime_path=str(runtime.relative_to(R))))
 print('DOWNLOADED grey woven fabric',flush=True)
except Exception as e:errors.append(dict(asset='Fabric030',error=str(e)))
checkpoint();print(json.dumps(dict(assets=len(records),errors=errors)))

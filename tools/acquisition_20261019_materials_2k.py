from pathlib import Path
import urllib.request,json,time,hashlib,shutil
from PIL import Image,ImageOps,ImageDraw
R=Path.cwd();tag='acquisition_20261019';M=R/'asset_library/manifests'/tag;L=R/'asset_library/licenses'/tag
slugs=['concrete_wall_001','concrete_floor_worn_001','rusty_painted_metal','painted_concrete','denim_fabric'];records=[];errors=[]
def fetch(u):return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Breakout-No-Way-Back/20261019 (Powered by Poly Haven)'}),timeout=120).read()
for slug in slugs:
 try:
  meta=json.loads(fetch('https://api.polyhaven.com/files/'+slug));time.sleep(1.1);info=json.loads(fetch('https://api.polyhaven.com/info/'+slug));time.sleep(1.1);(M/(slug+'_files.json')).write_text(json.dumps(meta,indent=2));(L/(slug+'_info.json')).write_text(json.dumps(info,indent=2))
  orig=R/'asset_library/original_downloads/materials'/tag/slug;runtime=R/'assets/materials'/tag/slug;orig.mkdir(parents=True,exist_ok=True);runtime.mkdir(parents=True,exist_ok=True);files=[];paths={}
  for channel in ['Diffuse','nor_gl','Rough','arm']:
   if channel not in meta:continue
   entry=meta[channel]['2k']['jpg'];p=orig/Path(entry['url']).name;d=p.read_bytes() if p.exists() else fetch(entry['url']);assert hashlib.md5(d).hexdigest()==entry['md5'];p.write_bytes(d)
   with Image.open(p) as im:assert im.size==(2048,2048);im.verify()
   target=runtime/p.name;target.write_bytes(d);paths[channel]=target.relative_to(R).as_posix();files.append(dict(local_file_path=p.relative_to(R).as_posix(),source_url=entry['url'],file_size=len(d),sha256=hashlib.sha256(d).hexdigest(),provider_md5=entry['md5']))
  text='[gd_resource type="StandardMaterial3D" load_steps=5 format=3]\n\n'
  for i,k in enumerate(['Diffuse','nor_gl','Rough','arm'],1):text+=f'[ext_resource type="Texture2D" path="res://{paths[k]}" id="{i}"]\n'
  text+='\n[resource]\nresource_name = "'+slug+' 2k"\nalbedo_texture = ExtResource("1")\nnormal_enabled = true\nnormal_texture = ExtResource("2")\nroughness_texture = ExtResource("3")\nroughness_texture_channel = 0\nao_enabled = true\nao_texture = ExtResource("4")\nao_texture_channel = 0\nmetallic = 1.0\nmetallic_texture = ExtResource("4")\nmetallic_texture_channel = 2\n'
  mat=runtime/(slug+'_2k.tres');mat.write_text(text)
  records.append(dict(asset_id='ACQ26_2K_'+slug.upper(),asset_name=info.get('name',slug),asset_category='materials',source_website='Poly Haven',source_url='https://polyhaven.com/a/'+slug,creator=info.get('authors'),license='CC0-1.0',commercial_use_status='PERMITTED',license_record='asset_library/licenses/'+tag+'/polyhaven_license.html',download_date='2026-10-19',original_filename=[Path(x['local_file_path']).name for x in files],local_file_path=orig.relative_to(R).as_posix(),file_size=sum(x['file_size'] for x in files),sha256={x['local_file_path']:x['sha256'] for x in files},model_format='2k JPG PBR',texture_resolution='2048x2048',rigged_status='N/A',animation_status='N/A',godot_import_status='NOT TESTED',visual_inspection_status='Image decode PASS; contact sheet pending review',related_mission=['CH01_M%02d'%i for i in range(1,7)],remaining_issues='UV physical scale and scene lighting calibration; no AAA readiness claim. Existing 1k preserved. Provider ARM blue metal channel used; optional AO enabled.',archive_integrity='N/A individual files; provider MD5 PASS',files=files,runtime_material=mat.relative_to(R).as_posix()))
  print('DOWNLOADED',slug,flush=True)
 except Exception as e:errors.append(dict(asset=slug,error=str(e)));print('FAILED',slug,str(e),flush=True)
 (M/'materials_2k_inventory.json').write_text(json.dumps(records,indent=2));(M/'materials_2k_checkpoint.json').write_text(json.dumps(dict(completed=[r['asset_id'] for r in records],failed=errors,pending_conversions=[],godot_validation='NOT TESTED',next_action='Visual material rendering, UV scale calibration and Godot import'),indent=2))
canvas=Image.new('RGB',(1250,280*len(records)),'#242424');draw=ImageDraw.Draw(canvas)
for row,rec in enumerate(records):
 for col,f in enumerate(rec['files']):
  im=Image.open(R/f['local_file_path']);im.thumbnail((255,255));canvas.paste(im,(col*310,row*280+25));draw.text((col*310,row*280+5),Path(f['local_file_path']).name,fill='white')
canvas.save(M/'materials_2k_actual_contact_sheet.jpg');print('COMPLETE',len(records),errors)

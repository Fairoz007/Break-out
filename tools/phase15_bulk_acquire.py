from pathlib import Path
import urllib.request,json,re,zipfile,hashlib,time,shutil,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1]; records=[];errors=[]
def rel(p):return p.relative_to(R).as_posix()
def fetch(u):
 d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Breakout-Preproduction/1.0 (Powered by Poly Haven)'}),timeout=90).read();time.sleep(1.05);return d
def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d)
def sha(d):return hashlib.sha256(d).hexdigest()
def checkpoint():put(R/'asset_library/manifests/phase15_bulk_assets.json',json.dumps(records,indent=2).encode());put(R/'asset_library/manifests/phase15_bulk_errors.json',json.dumps(errors,indent=2).encode())
existing={sha(p.read_bytes()) for p in (R/'assets/audio').rglob('*.ogg')}
for slug in ['impact-sounds','interface-sounds','ui-audio','rpg-audio']:
 try:
  page='https://kenney.nl/assets/'+slug;html=fetch(page);put(R/f'asset_library/licenses/phase15_bulk/{slug}_page.html',html)
  assert b'CC0' in html
  if slug=='impact-sounds':archive=R/'asset_library/original_downloads/kenney_impact-sounds.zip';data=archive.read_bytes()
  else:
   url=re.findall(r'https?[^\" ]+\.zip',html.decode())[0];data=fetch(url);archive=R/f'asset_library/original_downloads/phase15_bulk/kenney_{slug}.zip';put(archive,data)
  z=zipfile.ZipFile(archive);assert z.testzip() is None
  license_names=[n for n in z.namelist() if 'license' in n.lower() and n.lower().endswith('.txt')];assert license_names
  licensepath=R/f'asset_library/licenses/phase15_bulk/{slug}_License.txt';put(licensepath,z.read(license_names[0]));assert b'CC0' in licensepath.read_bytes()
  for n in z.namelist():
   if not n.lower().endswith(('.ogg','.wav')):continue
   d=z.read(n);digest=sha(d)
   if digest in existing:continue
   # RPG weapons not required; preserve archive but avoid promoting fantasy blade/bow assets.
   if slug=='rpg-audio' and any(t in n.lower() for t in ['sword','bow','arrow','spell']):continue
   existing.add(digest);name=re.sub('[^a-z0-9_]+','_',Path(n).stem.lower());p=R/f'assets/audio/phase15/{slug}/{name}{Path(n).suffix.lower()}';put(p,d)
   aid='AUDIO_P15_'+slug.replace('-','_').upper()+'_'+name.upper()
   records.append(dict(asset_id=aid,asset_name=Path(n).stem,category='audio',source_url=page,creator='Kenney',license='CC0-1.0',license_record=rel(licensepath),attribution_required=False,original_file=rel(archive),archive_member=n,original_checksum=sha(data),runtime_checksum=digest,runtime_file=rel(p),format=p.suffix[1:],polygon_count_if_known=None,texture_resolution_if_known=None,skeleton_type_if_applicable=None,animation_compatibility='not applicable',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='DOWNLOADED',import_status='NOT TESTED',validation_status='PARTIALLY_VERIFIED',priority='OPTIONAL' if slug in ['interface-sounds','ui-audio'] else 'IMPORTANT',notes='ZIP CRC and SHA256 verified. Candidate sound; audition and scene mix outstanding. Archive contains original source; no redundant extracted copy.'))
  checkpoint();print(slug,len(records),flush=True)
 except Exception as e:errors.append(dict(bundle=slug,error=str(e)));checkpoint()
slugs=['concrete_block_wall','concrete_floor_painted','concrete_floor_worn_001','painted_concrete','painted_concrete_02','concrete_wall_004','concrete_slab_wall','hangar_concrete_floor','smooth_concrete_floor','dirty_concrete','blue_metal_plate','metal_plate','metal_plate_02','rusty_painted_metal','corrugated_iron','rubber_tiles','denim_fabric','denim_fabric_03','fabric_leather_01','dirty_tiles','asphalt_01','anti_slip_concrete','worn_corrugated_iron','rusty_corrugated_iron']
for slug in slugs:
 try:
  meta=json.loads(fetch('https://api.polyhaven.com/files/'+slug));info=json.loads(fetch('https://api.polyhaven.com/info/'+slug))
  source=R/f'asset_library/licenses/phase15_bulk/{slug}_source.json';put(source,json.dumps(info,indent=2).encode());put(R/f'asset_library/manifests/phase15_bulk_{slug}.json',json.dumps(meta,indent=2).encode())
  files=[];hashes={};textures={}
  for channel in ['Diffuse','nor_gl','Rough','Metal']:
   if channel not in meta:continue
   f=meta[channel].get('1k',{});f=f.get('png',f.get('jpg'))
   if not f:continue
   d=fetch(f['url']);assert hashlib.md5(d).hexdigest()==f['md5'];name=Path(f['url']).name;p=R/f'asset_library/original_downloads/phase15_bulk/{slug}/{name}';put(p,d)
   runtime=R/f'assets/textures/phase15/{slug}/{name}';put(runtime,d)
   with Image.open(runtime) as im:im.verify()
   files.append(rel(runtime));hashes[rel(p)]=sha(d);textures[channel]=runtime
  assert all(k in textures for k in ['Diffuse','nor_gl','Rough'])
  p=R/f'assets/materials/phase15/{slug}.tres';lines=['[gd_resource type="StandardMaterial3D" load_steps=%d format=3]'%(len(textures)+1)]
  for i,(k,t) in enumerate(textures.items()):lines.append('[ext_resource type="Texture2D" path="res://%s" id="%s"]'%(rel(t),k))
  lines+=['[resource]','resource_name = "%s"'%slug,'albedo_texture = ExtResource("Diffuse")','roughness_texture = ExtResource("Rough")','roughness_texture_channel = 0','normal_enabled = true','normal_texture = ExtResource("nor_gl")']
  if 'Metal'in textures:lines+=['metallic = 1.0','metallic_texture = ExtResource("Metal")','metallic_texture_channel = 0']
  put(p,('\n'.join(lines)+'\n').encode())
  records.append(dict(asset_id='MAT_P15_'+slug.upper(),asset_name=slug,category='material',source_url='https://polyhaven.com/a/'+slug,creator=info.get('authors',{}),license='CC0-1.0',license_record=rel(source),attribution_required=False,original_file=list(hashes),original_checksum=hashes,runtime_file=rel(p),dependencies=files,format='Godot StandardMaterial3D + PNG/JPEG',polygon_count_if_known=None,texture_resolution_if_known='1k',skeleton_type_if_applicable=None,animation_compatibility='static',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='DOWNLOADED',import_status='NOT TESTED',validation_status='PARTIALLY_VERIFIED',priority='IMPORTANT',notes='Provider MD5 matched; SHA256 and image decode passed. OpenGL normal; diffuse uses source color, scalar rough/metal use red linear channels. Visual review and physical UV scale outstanding. Powered by Poly Haven.'))
  checkpoint();print(slug,len(files),flush=True)
 except Exception as e:errors.append(dict(bundle=slug,error=str(e)));checkpoint();print(slug,e,flush=True)
print('DONE',len(records),'errors',len(errors),flush=True)

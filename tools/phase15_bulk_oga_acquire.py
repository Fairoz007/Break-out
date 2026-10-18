from pathlib import Path
import urllib.request,re,zipfile,hashlib,json,time
R=Path(__file__).resolve().parents[1];records=[];errors=[]
def rel(p):return p.relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d)
def fetch(u):d=urllib.request.urlopen(u,timeout=90).read();time.sleep(1);return d
existing={sha(p.read_bytes()) for p in (R/'assets/audio').rglob('*') if p.is_file() and p.suffix in ['.ogg','.wav']}
for slug in ['100-cc0-sfx-2','75-cc0-breaking-falling-hit-sfx','100-cc0-metal-and-wood-sfx','electronic-device-loop']:
 try:
  page='https://opengameart.org/content/'+slug;h=fetch(page);assert re.search(rb'publicdomain/zero',h)
  licensepath=R/f'asset_library/licenses/phase15_bulk/{slug}_page.html';put(licensepath,h)
  urls=sorted(set(re.findall(r'href="([^"]+(?:\.zip|\.flac))"',h.decode())));assert urls
  for url in urls:
   d=fetch(url);archive=R/f'asset_library/original_downloads/phase15_bulk/{Path(url).name}';put(archive,d)
   if url.endswith('.zip'):
    z=zipfile.ZipFile(archive);assert z.testzip() is None;members=[(n,z.read(n)) for n in z.namelist() if n.lower().endswith(('.wav','.ogg','.flac'))]
   else:members=[(Path(url).name,d)]
   for n,b in members:
    if n.lower().endswith('.flac'):
     # keep archival FLAC; lossless convert to supported WAV in next script
     ext='.wav'
    else:ext=Path(n).suffix.lower()
    if sha(b) in existing:continue
    existing.add(sha(b));name=re.sub('[^a-z0-9_]+','_',Path(n).stem.lower());p=R/f'assets/audio/phase15/{slug}/{name}{ext}'
    if ext=='.wav' and n.endswith('.flac'):
     import subprocess
     p.parent.mkdir(parents=True,exist_ok=True);subprocess.run(['ffmpeg','-v','error','-y','-i',str(archive),str(p)],check=True)
    else:put(p,b)
    records.append(dict(asset_id='AUDIO_P15_OGA_'+slug.replace('-','_').upper()+'_'+name.upper(),asset_name=Path(n).stem,category='audio',source_url=page,creator='qubodup' if slug=='electronic-device-loop' else 'rubberduck',license='CC0-1.0',license_record=rel(licensepath),attribution_required=False,original_file=rel(archive),archive_member=n,original_checksum=sha(d),runtime_checksum=sha(p.read_bytes()),runtime_file=rel(p),format=ext[1:],polygon_count_if_known=None,texture_resolution_if_known=None,skeleton_type_if_applicable=None,animation_compatibility='not applicable',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='DOWNLOADED',import_status='NOT TESTED',validation_status='PARTIALLY_VERIFIED',priority='IMPORTANT',notes='Official page CC0 record saved. ZIP CRC/SHA256 verified. Candidate sound; listening and scene mix NOT TESTED. Scene list indicates eligible pool, not approved final placement.'))
  put(R/'asset_library/manifests/phase15_bulk_oga_assets.json',json.dumps(records,indent=2).encode());print(slug,len(records),flush=True)
 except Exception as e:errors.append(dict(bundle=slug,error=str(e)));print(slug,e,flush=True)
put(R/'asset_library/manifests/phase15_bulk_oga_errors.json',json.dumps(errors,indent=2).encode())

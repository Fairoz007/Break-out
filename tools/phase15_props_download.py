"""Curated official Poly Haven industrial props; run after coordinated API window."""
from pathlib import Path
import urllib.request,json,time,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[1]
M=R/'asset_library/manifests/phase15';M.mkdir(exist_ok=True)
slugs=['modular_chainlink_fence','modular_airduct_rectangular_01','modular_airduct_circular_01','security_light','portable_searchlight','mounted_fluorescent_lights','fire_alarm','wall_clock','pipe_wrench','adjustable_wrench','bench_vice_01','metal_tool_chest','steel_frame_shelves_01','plastic_crate_01','vintage_radio_transceiver','concrete_road_barrier_02','rollershutter_door','modular_fire_escape','ladder_sectioned_01','metal_stool_01']
def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Breakout-No-Way-Back-preproduction/1.5'})
    with urllib.request.urlopen(request,timeout=120) as response:return response.read()
def save(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
todo=[];errors=[]
for slug in slugs:
    try:
        meta=json.loads(fetch('https://api.polyhaven.com/files/'+slug));time.sleep(1.2)
        info=json.loads(fetch('https://api.polyhaven.com/info/'+slug));time.sleep(1.2)
        save(M/f'props_{slug}_files.json',json.dumps(meta,indent=2).encode())
        save(R/f'asset_library/licenses/phase15_props/{slug}_info.json',json.dumps(info,indent=2).encode())
        f=meta['gltf']['1k']['gltf'];entries={Path(f['url']).name:f};entries.update(f.get('include',{}))
        todo.append((slug,info,entries));print('METADATA',slug,flush=True)
    except Exception as e:errors.append({'slug':slug,'stage':'metadata','error':str(e)})
print('API_METADATA_COMPLETE',flush=True)
def acquire(job):
    slug,info,entries=job;originals=[];runtime=[];hashes={};filechecks=[]
    for rel,f in entries.items():
        orig=R/'asset_library/original_downloads/phase15_props'/slug/rel
        data=orig.read_bytes() if orig.exists() else fetch(f['url'])
        if hashlib.md5(data).hexdigest()!=f['md5']:raise ValueError('Provider checksum mismatch '+slug+'/'+rel)
        if not orig.exists():save(orig,data)
        dest=R/'assets/props/phase15_polyhaven'/slug/rel
        if not dest.exists():save(dest,data)
        p=orig.relative_to(R).as_posix();originals.append(p);runtime.append(dest.relative_to(R).as_posix());hashes[p]=hashlib.sha256(data).hexdigest()
        filechecks.append({'path':p,'source_url':f['url'],'sha256':hashes[p],'provider_md5':f['md5'],'bytes':len(data)})
    return dict(asset_id='PH15_'+slug.upper(),asset_name=slug,category='prop',source_url='https://polyhaven.com/a/'+slug,creator=info.get('authors',{}),license='CC0-1.0',license_file='asset_library/licenses/PolyHaven_license_policy.html',attribution_required=False,original_file=originals,original_checksum=hashes,runtime_file=runtime,format='glTF 2.0 + dependency files',polygon_count_if_known=None,texture_resolution_if_known='1k',skeleton_type_if_applicable=None,animation_compatibility='static',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='DOWNLOADED',import_status='NOT TESTED',validation_status='PARTIALLY_VERIFIED',notes='Authorized official CC0 file delivery; provider MD5 matched. Powered by Poly Haven. Mission scope reviewed at integration; no generic whole-room readiness claim.',priority='IMPORTANT',file_checks=filechecks)
records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures={pool.submit(acquire,job):job[0] for job in todo}
    for future in concurrent.futures.as_completed(futures):
        slug=futures[future]
        try:records.append(future.result());print('DOWNLOADED',slug,flush=True)
        except Exception as e:errors.append({'slug':slug,'stage':'download','error':str(e)});print('FAILED',slug,str(e),flush=True)
        save(R/'asset_library/manifests/phase15_props_records.json',json.dumps(records,indent=2).encode())
save(M/'props_errors.json',json.dumps(errors,indent=2).encode())
print('COMPLETE',len(records),'props',len(errors),'errors',flush=True)

"""Phase 01 reproducible public CC0 download; never supplies credentials."""
from pathlib import Path
import json, urllib.request, hashlib, shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Breakout-Preproduction/1.0'}),timeout=60).read()
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
records=[]; checks=[]
for aid,slug,kind in [('MAT_CONCRETE','concrete_wall_001','texture'),('MAT_METAL','rusty_metal_02','texture'),('PROP_SCONCE','industrial_caged_sconce','model'),('PROP_CART','industrial_storage_cart','model'),('PROP_PIPES','modular_industrial_pipes_01','model')]:
    meta=json.loads(fetch('https://api.polyhaven.com/files/'+slug))
    save(ROOT/f'asset_library/manifests/polyhaven_{slug}.json',json.dumps(meta,indent=2).encode())
    info=json.loads(fetch('https://api.polyhaven.com/info/'+slug))
    save(ROOT/f'asset_library/licenses/{slug}_source.json',json.dumps(info,indent=2).encode())
    entries={}
    if kind=='texture':
        for channel in ['Diffuse','nor_gl','Rough']:
            if channel not in meta: channel={'nor_gl':'Normal','Rough':'Roughness'}.get(channel,channel)
            f=meta[channel]['1k']; f=f.get('png',f.get('jpg'));entries[Path(f['url']).name]=f
    else:
        f=meta['gltf']['1k']['gltf'];entries[Path(f['url']).name]=f
        entries.update(f.get('include',{}))
    originals=[]; runtimes=[]
    for rel,f in entries.items():
        data=fetch(f['url']);md5=hashlib.md5(data).hexdigest()
        if md5!=f['md5']:raise ValueError('Checksum mismatch '+rel)
        orig=ROOT/'asset_library/original_downloads'/slug/rel
        dest=ROOT/('assets/materials' if kind=='texture' else 'assets/props')/slug/rel
        save(orig,data);save(dest,data)
        extracted=ROOT/'asset_library/extracted_sources'/slug/rel;save(extracted,data)
        if dest.suffix.lower() in ['.png','.jpg']:
            with Image.open(dest) as im: im.verify()
        checks.append(dict(path=str(orig.relative_to(ROOT)).replace('\\','/'),source_url=f['url'],md5=md5,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),provider_checksum_match=True))
        originals.append(str(orig.relative_to(ROOT)).replace('\\','/'));runtimes.append(str(dest.relative_to(ROOT)).replace('\\','/'))
    records.append(dict(asset_id=aid,asset_name=slug,category=kind,source_url='https://polyhaven.com/a/'+slug,creator=info.get('authors',{}),license='CC0-1.0',attribution_required=False,original_file=originals,original_checksum={c['path']:c['sha256'] for c in checks if '/'+slug+'/' in c['path']},runtime_file=runtimes,format='glTF 2.0 + bin + JPEG' if kind=='model' else 'PNG/JPEG',polygon_count_if_known=None,texture_resolution_if_known='1k',skeleton_type_if_applicable=None,animation_compatibility='static',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='DOWNLOADED',import_status='NOT TESTED',validation_status='NOT TESTED',notes='Byte checks and image decoding passed; visual/engine tests separate. Source files delivered individually, no archive. Runtime copies unoptimized. Powered by Poly Haven.'))
    print(aid,len(entries),'files',flush=True)
save(ROOT/'asset_library/manifests/download_checks.json',json.dumps(checks,indent=2).encode())
save(ROOT/'asset_library/manifests/acquired.json',json.dumps(records,indent=2).encode())

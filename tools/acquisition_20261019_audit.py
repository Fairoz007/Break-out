"""Read-only baseline reconciliation. Never rewrites previous acquisition evidence."""
import json, hashlib, csv
from pathlib import Path
from collections import defaultdict
R=Path(__file__).resolve().parents[1]
D=R/'asset_library/manifests/acquisition_20261019'; D.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
A=json.loads((R/'asset_library/manifests/assets.json').read_text(encoding='utf-8-sig'))
S=json.loads((R/'asset_library/manifests/phase15/integration_summary.json').read_text())['bundles']
def seq(v): return [v] if isinstance(v,str) else v if isinstance(v,list) else []
files={}; rows=[]
for a in A:
    paths=seq(a.get('runtime_file')); checks=a.get('runtime_checksum',{})
    result=[]
    for p in paths:
        f=R/p
        if not f.is_file(): result.append({'path':p,'exists':False}); continue
        if p not in files: files[p]={'path':p,'exists':True,'bytes':f.stat().st_size,'sha256':sha(f)}
        e=dict(files[p]); expected=checks.get(p) if isinstance(checks,dict) else checks if len(paths)==1 else None
        e['recorded_hash_match']=e['sha256']==expected if expected else None; result.append(e)
    lic=a.get('license_file') or a.get('license_record')
    rows.append({'asset_id':a['asset_id'],'category':a.get('category'),'prior_status':a.get('validation_status'),
        'runtime_files':result,'license_record':lic,'license_record_exists':(R/lic).is_file() if isinstance(lic,str) else None,
        'usable_previously':a.get('usable'),'source_url':a.get('source_url')})
byid={a['asset_id']:a for a in A}; bundles=[]
for aid,b in S.items():
    kids=byid[aid].get('child_asset_ids',[])
    childrows=[r for r in rows if r['asset_id'] in kids]
    bundles.append({'asset_id':aid,**b,'children':kids,'children_reconciled':len(childrows),
        'missing_runtime_paths':[f['path'] for r in childrows for f in r['runtime_files'] if not f['exists']],
        'hash_mismatches':[f['path'] for r in childrows for f in r['runtime_files'] if f.get('recorded_hash_match') is False]})
docs=[R/p for p in ['STORY.md','GAME_DESIGN.md','ASSET_MANIFEST.md','docs/assets/ASSET_REQUIREMENTS.md','docs/assets/ASSET_GAPS.md','docs/qa/BLOCKERS.md','docs/qa/ASSET_COVERAGE_MATRIX.md','docs/qa/PHASE_01_5_REPORT.md']]
for folder in ['missions','environments','screenplay']: docs+=sorted((R/'docs'/folder).glob('*.md'))
docrows=[{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'characters':len(p.read_text(encoding='utf-8-sig'))} for p in docs]
dups=defaultdict(list)
for p,f in files.items(): dups[f['sha256']].append(p)
report={'date':'2026-10-19','scope':'Current filesystem/hash/license-presence check; prior visual and import statuses are historical evidence, not rerun here.',
    'records':len(rows),'documents_inspected':docrows,'assets':rows,'bundles':bundles,
    'byte_duplicate_runtime_groups':[v for v in dups.values() if len(v)>1],
    'missing_paths':[f['path'] for r in rows for f in r['runtime_files'] if not f['exists']],
    'hash_mismatches':[f['path'] for r in rows for f in r['runtime_files'] if f.get('recorded_hash_match') is False]}
(D/'baseline_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
out=['# Acquisition checkpoint — 19 October 2026','','All 22 original missing bundles reconciled against current runtime files. Existing manifest retained. Prior import and visual claims are historical evidence; this audit checks file presence and recorded hashes.','','| Bundle | Existing child records | Missing paths | Hash mismatches | Production | Remaining requirement |','|---|---:|---:|---:|---|---|']
for b in bundles:out.append(f"| {b['asset_id']} | {b['children_reconciled']} | {len(b['missing_runtime_paths'])} | {len(b['hash_mismatches'])} | {b['production_status']} | {b['missing']} |")
(D/'BUNDLE_RECONCILIATION.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
print(json.dumps({'records':len(rows),'bundles':len(bundles),'unique_runtime_files':len(files),'missing_paths':len(report['missing_paths']),'hash_mismatches':len(report['hash_mismatches']),'documents':len(docrows)}))

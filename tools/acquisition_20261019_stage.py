"""Stage new embedded static GLBs; never replace an existing different payload."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'asset_library/manifests/acquisition_20261019'
items=[]
for a in json.loads((D/'sketchfab_inventory.json').read_text()):
 cat='environments' if a['asset_id']=='SF_GUARD_TOWER' else 'props'
 items.append((a['asset_id'],R/a['conversion']['converted_file'],R/'assets'/cat/'acquisition_20261019'/(a['asset_name']+'.glb')))
items.append(('ACQ26_YAESU_RADIO',R/'asset_library/converted/acquisition_20261019/radio_yaesu/radio_yaesu_single_metric.glb',R/'assets/props/acquisition_20261019/radio_yaesu_single_metric.glb'))
out=[]
for aid,src,dst in items:
 dst.parent.mkdir(parents=True,exist_ok=True)
 h=hashlib.sha256(src.read_bytes()).hexdigest()
 if dst.exists():assert hashlib.sha256(dst.read_bytes()).hexdigest()==h,'Refuse overwrite '+str(dst)
 else:shutil.copyfile(src,dst)
 out.append({'asset_id':aid,'candidate_runtime_path':dst.relative_to(R).as_posix(),'source':src.relative_to(R).as_posix(),'sha256':h,'size':dst.stat().st_size,'status':'Static placement candidate; main game scene integration NOT TESTED'})
(D/'runtime_staging.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'staged':len(out)}))

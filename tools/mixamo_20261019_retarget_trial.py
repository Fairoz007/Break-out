"""Isolated Mixamo -> Rocketbox rest-relative retarget evaluation, never canonical replacement."""
import sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from phase15_gltf_util import read_glb,write_glb
import phase15_rocketbox_animate as rocket
import inspect
transfer_code=inspect.getsource(rocket.transfer).replace("wu[n] = qmul(pw, local);", "loct=tuple(x*rocket.world_rest_full(ujs,up,par)[1] for x in loct) if par is not None else loct; wu[n] = qmul(pw, local);")
namespace=dict(rocket.__dict__);namespace["rocket"]=rocket;exec(transfer_code,namespace);transfer=namespace["transfer"]
SRC=R/'asset_library/converted/mixamo_20261019';OUT=SRC/'retarget_trials';OUT.mkdir(parents=True,exist_ok=True)
M=R/'asset_library/manifests/mixamo_20261019'
mp={'Hips':'pelvis','Spine':'spine_01','Spine1':'spine_02','Spine2':'spine_03','Neck':'neck_01','Head':'Head'}
for s,S in [('Left','l'),('Right','r')]:
 for a,b in [('Shoulder','clavicle'),('Arm','upperarm'),('ForeArm','lowerarm'),('Hand','hand'),('UpLeg','thigh'),('Leg','calf'),('Foot','foot'),('ToeBase','ball')]:mp[s+a]=b+'_'+S
 for f,g in [('Thumb','thumb'),('Index','index'),('Middle','middle'),('Ring','ring'),('Pinky','pinky')]:
  for i in range(1,4):mp[s+'Hand'+f+str(i)]=f'{g}_0{i}_{S}'
allreports={}
for stem in ['rb_adrian_cross','rb_noah_reyes']:
 target=R/('asset_library/converted/acquisition_20261019/rocketbox_facial/'+stem+'_rest.glb')
 if not target.exists(): target=R/('asset_library/converted/phase15_characters/rocketbox/'+stem+'_rest.glb')
 tjs,tbin=read_glb(target);report=[]
 for p in sorted(SRC.glob('*.glb')):
  ujs,ubin=read_glb(p)
  for n in ujs['nodes']:
   raw=n.get('name','').split(':')[-1];n['name']=mp.get(raw,n.get('name',''))
  for a in ujs.get('animations',[]):
   a['name']=p.stem
   try:report.append(dict(source=p.name,**transfer(tjs,tbin,ujs,ubin,p.stem)))
   except Exception as e:report.append(dict(source=p.name,error=repr(e)))
 p=OUT/(stem+'_mixamo_evaluation.glb');tjs['buffers'][0]['byteLength']=len(tbin)+((4-len(tbin)%4)%4);write_glb(p,tjs,tbin)
 allreports[stem]=dict(target=str(target.relative_to(R)),trial=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),clips=report,status='STRUCTURAL TRIAL ONLY; rendered contact and locomotion review required',method='Rest-relative world quaternion transfer with bone direction swing and hip-scaled pelvis displacement',limitations='Does not solve foot locking, hand contacts, paired choreography, facial performance or root motion policy')
(M/'retarget_trial.json').write_text(json.dumps(allreports,indent=2));print(allreports)


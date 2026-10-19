from pathlib import Path
import sys,copy
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from phase15_gltf_util import read_glb,write_glb
from phase15_ubc_animate import accessor,sample
S=R/'asset_library/converted/mixamo_20261019/retarget_trials';O=S/'poses';O.mkdir(exist_ok=True)
for stem in ['rb_adrian_cross','rb_noah_reyes']:
 js,b=read_glb(S/(stem+'_mixamo_evaluation.glb'))
 for clip,fraction in [('opening_door_inwards',.5),('pull_heavy_object',.5),('unarmed_turn_left_90',.7)]:
  out=copy.deepcopy(js);a=next(a for a in js['animations'] if a['name']==clip)
  for ch in a['channels']:
   sm=a['samplers'][ch['sampler']];ts=[r[0] for r in accessor(js,b,sm['input'])];vs=accessor(js,b,sm['output']);path=ch['target']['path'];out['nodes'][ch['target']['node']][path]=sample(ts,vs,ts[-1]*fraction,path=='rotation')
  out.pop('animations',None);write_glb(O/(stem+'_'+clip+'.glb'),out,b)

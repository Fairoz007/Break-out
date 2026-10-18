from pathlib import Path
import json,zipfile,subprocess,array
R=Path(__file__).resolve().parents[1];corrpath=R/'asset_library/manifests/phase15_bulk_audio_corrections.json';corr=json.loads(corrpath.read_text());byid={x['asset_id']:x for x in corr}
for f in ['phase15_bulk_assets.json','phase15_bulk_oga_assets.json']:
 p=R/'asset_library/manifests'/f;out=[]
 for r in json.loads(p.read_text()):
  c=byid.get(r['asset_id'])
  if c and c.get('exclude'):continue
  if c:
   original=zipfile.ZipFile(R/r['original_file']).read(r['archive_member']);raw=subprocess.run(['ffmpeg','-v','error','-i','pipe:0','-f','f32le','-acodec','pcm_f32le','pipe:1'],input=original,capture_output=True,check=True).stdout;a=array.array('f');a.frombytes(raw)
   c['source_decoded_peak_linear']=max(map(abs,a));c['source_samples_at_or_above_full_scale']=sum(abs(x)>=1 for x in a)
   r['notes']+=' '+c['notes_add'];r.update({k:v for k,v in c.items() if k not in ['asset_id','notes_add']});r['source_audition_required']=True
  if r['category']=='audio':r['notes']+=' Required scenes are eligibility pool, not final approved placement; listening remains NOT TESTED.'
  assert (R/r['runtime_file']).exists();out.append(r)
 p.write_text(json.dumps(out,indent=2))
corrpath.write_text(json.dumps(corr,indent=2));print('applied',len(corr))

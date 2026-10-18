from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1]; count=0
for fname in ['phase15_bulk_assets.json','phase15_bulk_oga_assets.json']:
 p=R/'asset_library/manifests'/fname;b=p.read_bytes();assert b'\0' not in b;a=json.loads(b)
 for r in a:
  if r['category']!='audio' or not r['runtime_file'].endswith('.wav'):continue
  f=R/r['runtime_file'];assert '/phase15/' in r['runtime_file'];tmp=f.with_name(f.stem+'_pcm16_temp.wav')
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-c:a','pcm_s16le','-write_bext','0',str(tmp)],check=True)
  tmp.replace(f);r['runtime_checksum']=hashlib.sha256(f.read_bytes()).hexdigest();r['format']='wav';r['notes']+=' Godot import repair: standard PCM16 RIFF/WAVE runtime; source archive retained unchanged.';count+=1
 p.write_text(json.dumps(a,indent=2),encoding='utf-8')
print('PCM16 repaired',count,flush=True)

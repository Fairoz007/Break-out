from pathlib import Path
import subprocess,array,json,math
R=Path(__file__).resolve().parents[1]
out=[]
for p in sorted((R/'assets/audio').glob('*.ogg')):
    proc=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-acodec','pcm_f32le','-'],capture_output=True,check=True)
    values=array.array('f');values.frombytes(proc.stdout)
    peak=max(map(abs,values),default=0)
    out.append(dict(path=p.relative_to(R).as_posix(),decoded_samples=len(values),peak_linear=peak,peak_dbfs=20*math.log10(peak) if peak else None,samples_at_or_above_full_scale=sum(abs(v)>=1 for v in values),decode='PASS',listening='NOT TESTED'))
(R/'asset_library/manifests/audio_waveform_validation.json').write_text(json.dumps(out,indent=2))
print(len(out),'files decoded; maximum peak',max(x['peak_linear'] for x in out),'full-scale samples',sum(x['samples_at_or_above_full_scale'] for x in out))

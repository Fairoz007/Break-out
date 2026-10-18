from pathlib import Path
import subprocess,array,json,math,concurrent.futures
R=Path(__file__).resolve().parents[1]
def inspect(p):
 try:
  info=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],capture_output=True,check=True).stdout);stream=info['streams'][0]
  raw=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-acodec','pcm_f32le','-'],capture_output=True,check=True).stdout
  a=array.array('f');a.frombytes(raw);peak=max(map(abs,a),default=0)
  return dict(path=p.relative_to(R).as_posix(),sample_rate=int(stream['sample_rate']),channels=stream['channels'],duration_seconds=float(info['format']['duration']),decoded_samples=len(a),peak_linear=peak,peak_dbfs=20*math.log10(peak) if peak else None,samples_at_or_above_full_scale=sum(abs(x)>=1 for x in a),decode='PASS',listening='NOT TESTED')
 except Exception as e:return dict(path=p.relative_to(R).as_posix(),decode='FAIL',error=str(e))
paths=[p for p in (R/'assets/audio').rglob('*') if p.suffix in ['.ogg','.wav']]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:results=list(e.map(inspect,paths))
p=R/'asset_library/manifests/phase15_bulk_audio_validation.json';p.write_text(json.dumps(results,indent=2));print('files',len(results),'failed',sum(x['decode']!='PASS' for x in results),'fullscale_samples',sum(x.get('samples_at_or_above_full_scale',0) for x in results))

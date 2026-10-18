from pathlib import Path
import json,subprocess,hashlib,math
R=Path(__file__).resolve().parents[1];corrections=[]
reports={x['path']:x for x in json.loads((R/'asset_library/manifests/phase15_bulk_audio_validation.json').read_text())}
for file in ['phase15_bulk_assets.json','phase15_bulk_oga_assets.json']:
 for r in json.loads((R/'asset_library/manifests'/file).read_text()):
  if r['category']!='audio':continue
  p=R/r['runtime_file']
  if 'preview' in p.stem:
   # These are provider demonstration montages, not individual production cues.
   if p.exists():p.unlink()
   corrections.append(dict(asset_id=r['asset_id'],exclude=True,reason='Pack demonstration montage excluded; original retained in archive.'));continue
  test=reports.get(r['runtime_file'])
  if test and test['peak_linear']>=1:
   q=p.with_suffix('.wav');gain=0.5/test['peak_linear'];subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-af',f'volume={gain:.10f}','-c:a','pcm_s24le',str(q)],check=True)
   p.unlink();corrections.append(dict(asset_id=r['asset_id'],runtime_file=q.relative_to(R).as_posix(),runtime_checksum=hashlib.sha256(q.read_bytes()).hexdigest(),format='wav',notes_add=f'Runtime repaired: lossless24-bit WAV decoded and attenuated {20*math.log10(gain):.2f}dB to peak0.5; source OGG/FLAC archived unchanged. Clipping in source waveform cannot be undone; audition required.'))
(R/'asset_library/manifests/phase15_bulk_audio_corrections.json').write_text(json.dumps(corrections,indent=2));print('corrections',len(corrections),'montages',sum(x.get('exclude',False) for x in corrections))

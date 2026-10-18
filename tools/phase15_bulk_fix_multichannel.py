from pathlib import Path
import json,subprocess,wave,io,hashlib
R=Path(__file__).resolve().parents[1];p=R/'assets/audio/phase15/electronic-device-loop/qubodup_edev.wav'
# Runtime ambience downmixed stereo deliberately; archived original FLAC unchanged.
b=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-ac','2','-f','s16le','-c:a','pcm_s16le','-'],capture_output=True,check=True).stdout
rate=int(json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(p)],capture_output=True,check=True).stdout)['streams'][0]['sample_rate'])
with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b)
f=R/'asset_library/manifests/phase15_bulk_oga_assets.json';a=json.loads(f.read_text())
for r in a:
 if r['runtime_file']==p.relative_to(R).as_posix():r['runtime_checksum']=hashlib.sha256(p.read_bytes()).hexdigest();r['notes']+=' Multichannel electronic-device recording downmixed to stereo PCM16 with standard format1 WAV header for Godot compatibility.'
f.write_text(json.dumps(a,indent=2));print('electronicdevice stereo PCM16 fixed')

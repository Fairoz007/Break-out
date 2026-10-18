"""Original functional sound candidates, explicitly synthetic, not field recordings."""
from pathlib import Path
import math,random,wave,array,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/audio/phase15_original';D.mkdir(exist_ok=True)
rate=48000;rng=random.Random(15018)
spec=[('ALARM_SIREN',6.0),('ALERT_DOUBLE',1.0),('RADIO_STATIC',3.0),('FAN_LOOP',6.0),('FLUORESCENT_BUZZ',4.0),('PA_CHIME',1.6),('RELAY_CLICK',0.2)]
records=[]
for name,duration in spec:
    n=int(rate*duration);values=[];smooth=0;phase=0
    for i in range(n):
        t=i/rate;noise=rng.uniform(-1,1);smooth=0.94*smooth+0.06*noise
        if name=='ALARM_SIREN':
            frequency=560+240*(0.5+0.5*math.sin(2*math.pi*t/2));phase+=2*math.pi*frequency/rate
            value=0.3*math.sin(phase)+0.1*math.sin(phase*2)
        elif name=='ALERT_DOUBLE':value=0.35*math.sin(2*math.pi*880*t)*(1 if t<0.18 or 0.3<t<0.48 else 0)
        elif name=='RADIO_STATIC':value=noise*0.16+smooth*0.1
        elif name=='FAN_LOOP':value=0.18*smooth+0.09*math.sin(2*math.pi*60*t)+0.035*math.sin(2*math.pi*120*t)
        elif name=='FLUORESCENT_BUZZ':value=0.08*math.sin(2*math.pi*100*t)+0.025*math.sin(2*math.pi*200*t)+smooth*0.06
        elif name=='PA_CHIME':value=0.3*math.sin(2*math.pi*(660 if t<0.6 else 440)*t)*math.exp(-2*(t if t<0.6 else t-0.6))
        else:value=(noise*0.4+0.3*math.sin(2*math.pi*2200*t))*math.exp(-80*t)
        envelope=min(1,i/(rate*0.012),(n-1-i)/(rate*0.025))
        values.append(value*max(0,envelope))
    data=array.array('h',[round(v*32767) for v in values]);p=D/(name.lower()+'.wav')
    with wave.open(str(p),'wb') as out:out.setparams((1,2,rate,0,'NONE','not compressed'));out.writeframes(data.tobytes())
    path=p.relative_to(R).as_posix()
    records.append(dict(asset_id='AUDIO15_'+name,asset_name=name.lower()+' (original synthetic candidate)',category='audio',source_url=None,creator='Project original procedural synthesis',license='Project original',license_file='asset_library/licenses/phase15_original_audio.md',attribution_required=False,original_file='tools/phase15_synthetic_audio.py',original_checksum=None,runtime_file=path,runtime_checksum=hashlib.sha256(p.read_bytes()).hexdigest(),format='WAV PCM16 mono 48000Hz',polygon_count_if_known=None,texture_resolution_if_known=None,skeleton_type_if_applicable=None,animation_compatibility='audio event/loop candidate',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='CREATED',import_status='NOT TESTED',validation_status='PARTIALLY_VERIFIED',priority='IMPORTANT',duration_seconds=duration,sample_rate=rate,peak_linear=max(map(abs,values)),synthetic=True,notes='Deterministic original synthesis; faded edges and peak below full scale. Not an authentic prison field recording. Listening/mix pending. Loop names have edge fades, continuous crossfade test still required.'))
script_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
for record in records:record['original_checksum']=script_hash
(R/'asset_library/manifests/phase15_original_audio.json').write_text(json.dumps(records,indent=2))
(R/'asset_library/licenses/phase15_original_audio.md').write_text('# Original synthetic audio\n\nSeven mathematical sound candidates created for BREAKOUT: NO WAY BACK with tools/phase15_synthetic_audio.py. Project owner may use, modify and distribute these original sounds. No samples or third-party recordings used. They are functional synthetic placeholders for art audition, not claimed authentic prison recordings. WAV PCM16 mono 48kHz, source script and checksums retained. No voice or music generated.\n')
print(len(records),'original PCM16 sound candidates')

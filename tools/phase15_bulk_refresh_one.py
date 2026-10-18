from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'tools/phase15_bulk_validate_audio.py')};exec(compile((R/'tools/phase15_bulk_validate_audio.py').read_text().split('paths=')[0],str(R/'tools/phase15_bulk_validate_audio.py'),'exec'),ns)
p=R/'asset_library/manifests/phase15_bulk_audio_validation.json';a=json.loads(p.read_text());key='assets/audio/phase15/electronic-device-loop/qubodup_edev.wav';a=[x for x in a if x['path']!=key];a.append(ns['inspect'](R/key));p.write_text(json.dumps(a,indent=2));print('final',len(a),'fails',sum(x['decode']!='PASS' for x in a),'fullscale',sum(x.get('samples_at_or_above_full_scale',0) for x in a),'electronicchannels',a[-1]['channels'])


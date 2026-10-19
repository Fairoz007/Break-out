"""Export canonical Chapter 1 dialogue, camera shots and mission metadata to runtime JSON under data/ch01/.
The game only reads these files; they are regenerated from the docs and checked for drift.
python -I tools/phase02_export_data.py          (write)
python -I tools/phase02_export_data.py --check  (exit 1 if data/ch01 differs from the docs)"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
DOC = R / 'docs'; OUT = R / 'data/ch01'
dlg_md = (DOC / 'screenplay/CH01_DIALOGUE.md').read_text(encoding='utf-8')
lines = []
for m in re.finditer(r'^\| (CH01_M0(\d)_DLG(\d{3})) \| ([A-Z]+) \| ([\d.]+)–([\d.]+)s \| ([^|]+) \| (.+?) \|\s*$', dlg_md, re.M):
    delivery, _, cond = m[7].strip().partition('; ')
    lines.append(dict(id=m[1], mission=int(m[2]), speaker=m[4], start=float(m[5]), end=float(m[6]),
                      duration=round(float(m[6]) - float(m[5]), 2), delivery=delivery, condition=cond, main=cond == 'main sequence', text=m[8].strip()))
shots_md = (DOC / 'screenplay/CH01_CAMERA_SHOTS.md').read_text(encoding='utf-8')
shots = []
for m in re.finditer(r'^\| (CH01_M0(\d)_CS01_SH(\d\d)) \| (\d+)–(\d+)s \| ([^|]+) \| (.+?) \|\s*$', shots_md, re.M):
    lens = re.match(r'(\d+)mm', m[6].strip())
    shots.append(dict(id=m[1], mission=int(m[2]), index=int(m[3]), reel_start=int(m[4]), reel_end=int(m[5]), duration=int(m[5]) - int(m[4]),
                      camera=m[6].strip(), lens_mm=int(lens[1]) if lens else 50, direction=m[7].strip()))
missions = []
for i in range(1, 7):
    md = (DOC / f'missions/CH01_MISSION_0{i}.md').read_text(encoding='utf-8')
    title = re.match(r'# Mission 0\d — (.+)', md)[1]
    trig = re.search(r'## Objective and cinematic triggers\s+(.+?)\n', md)[1]
    objs = [dict(id=f'CH01_M0{i}_OBJ{n}', text=t.strip(' ;.')) for n, t in re.findall(r'OBJ(\d{3}) (.+?)(?=; OBJ\d{3}|\. |; CS01| CS01|\.$)', trig.split('IDs are')[0])]
    time = re.search(r'Time: (.+?)\.', md)[1]
    missions.append(dict(id=f'CH01_M0{i}', index=i, title=title.upper(), time=time, scene=f'CH01_M0{i}_SC01', cinematic=f'CH01_M0{i}_CS01',
                         objectives=objs, checkpoints=[f'CP0{i}_A', f'CP0{i}_B']))
files = {'dialogue.json': dict(source='docs/screenplay/CH01_DIALOGUE.md', lines=lines),
         'shots.json': dict(source='docs/screenplay/CH01_CAMERA_SHOTS.md', shots=shots),
         'missions.json': dict(source='docs/missions/CH01_MISSION_0*.md', missions=missions)}
assert len(lines) == 145 and len(shots) == 36 and len(missions) == 6, (len(lines), len(shots), len(missions))
drift = []
for name, data in files.items():
    text = json.dumps(data, indent=1, ensure_ascii=False) + '\n'
    p = OUT / name
    if '--check' in sys.argv:
        if not p.is_file() or p.read_text(encoding='utf-8') != text: drift.append(name)
    else:
        OUT.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8', newline='\n')
print(json.dumps(dict(lines=len(lines), shots=len(shots), missions=len(missions), objectives=sum(len(m['objectives']) for m in missions), drift=drift)))
sys.exit(1 if drift else 0)

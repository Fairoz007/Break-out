"""Phase 06: build docs/phase06/DIALOGUE_AUDIO_MANIFEST.csv and SFX_MANIFEST.csv from the screenplay data, the
generation manifests, the game code (where each line/cue is triggered) and runtime evidence.

QA status values (automated only; listening quality is never claimed here):
  RUNTIME_VOICED  - the line was shown in a chapter run with its take playing (tests/phase06/evidence/chapter_*.json)
  NOT_TRIGGERED   - file exists but no run reached the line
  MISSING_AUDIO   - no take
Human column is always HUMAN_AUDIO_REVIEW_PENDING until a listener fills docs/phase06/AUDIO_QA_REPORT.md.
python3 -I tools/phase06_audio_manifests.py
"""
import csv, json, re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from elevenlabs_client import probe_seconds

R = Path(__file__).resolve().parents[1]
D = R / 'docs/phase06'
EV = R / 'tests/phase06/evidence'


def code_refs():
    """mission -> {line number n: 'file:line kind'} from line_id(n) / bark(n / say(n uses."""
    refs = {}
    for m in range(1, 7):
        p = R / ('scripts/missions/mission_%02d.gd' % m)
        for i, text in enumerate(p.read_text().splitlines(), 1):
            for kind, n in re.findall(r'\b(line_id|bark|say)\((\d+)', text):
                refs.setdefault(m, {}).setdefault(int(n), '%s:%d %s' % (p.relative_to(R), i, kind))
    return refs


def runtime():
    seen = {}
    for f in sorted(EV.glob('chapter_*.json')):
        d = json.loads(f.read_text())
        for e in d['events']:
            if e['kind'] == 'dialogue_shown' and e.get('voice'):
                seen.setdefault(e['id'], set()).add(f.stem.replace('chapter_', ''))
    return seen


def main():
    lines = json.loads((R / 'data/ch01/dialogue.json').read_text())['lines']
    vm = json.loads((R / 'assets/audio/voice/ch01/voice_manifest.json').read_text())
    cast = vm['cast']
    refs, seen = code_refs(), runtime()
    D.mkdir(parents=True, exist_ok=True)
    rows = []
    for l in lines:
        n = int(l['id'][-3:])
        take = R / 'assets/audio/voice/ch01' / (l['id'] + '.ogg')
        g = vm['lines'].get(l['id'], {})
        secs = probe_seconds(take) if take.exists() else None
        qa = 'MISSING_AUDIO' if not take.exists() else ('RUNTIME_VOICED' if l['id'] in seen else 'NOT_TRIGGERED')
        rows.append({
            'dialogue_id': l['id'], 'mission': l['mission'], 'character': l['speaker'], 'dialogue': l['text'],
            'emotional_direction': l['delivery'], 'voice': cast[l['speaker']]['voice'], 'voice_id': cast[l['speaker']]['voice_id'],
            'model': vm['model'], 'generation_status': 'GENERATED' if g else 'NOT_GENERATED',
            'audio_file': str(take.relative_to(R)) if take.exists() else '', 'duration_s': secs or '',
            'subtitle_s': l['duration'], 'subtitle_text': l['text'], 'main': l['main'], 'trigger_condition': l['condition'],
            'trigger_code': refs.get(l['mission'], {}).get(n, ''), 'runtime_runs': ' '.join(sorted(seen.get(l['id'], []))),
            'qa_status': qa, 'human_review': 'HUMAN_AUDIO_REVIEW_PENDING', 'sha256': g.get('sha256', ''),
        })
    with (D / 'DIALOGUE_AUDIO_MANIFEST.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # SFX: every cue in audio_director.gd (+ footsteps), with source, generator record and where the game uses it
    ad = (R / 'scripts/core/audio_director.gd').read_text()
    cues = dict(re.findall(r'\t"([a-z_]+)": ((?:A|E|P6) \+ "[^"]+")', ad))
    sm = json.loads((R / 'assets/audio/phase05_elevenlabs/sfx_manifest.json').read_text())['items']
    for extra in sorted((R / 'assets/audio/phase06_elevenlabs').glob('sfx_manifest.json')) if (R / 'assets/audio/phase06_elevenlabs').exists() else []:
        sm.update(json.loads(extra.read_text())['items'])
    uses = {}
    for p in list((R / 'scripts').rglob('*.gd')):
        for i, text in enumerate(p.read_text().splitlines(), 1):
            for name in re.findall(r'(?:cue|start_bed|play_music)\("([a-z_]+)"', text):
                uses.setdefault(name, []).append('%s:%d' % (p.relative_to(R), i))
    door = (R / 'scripts/world/door.gd').read_text()
    sounds = door[door.index('const SOUNDS'):door.index('\n\n', door.index('const SOUNDS'))]
    for a, b in re.findall(r'\["(\w+)", "(\w+)"\]', sounds):
        for name in (a, b):
            uses.setdefault(name, []).append('scripts/world/door.gd SOUNDS (door motion)')
    for name in re.findall(r'"(ui_\w+)" if|else "(ui_\w+)", null', '\n'.join(p.read_text() for p in (R / 'scripts/ui').glob('*.gd'))):
        pass
    uses.setdefault('ui_confirm', []).append('scripts/ui/main_menu.gd _button')
    for spot in re.findall(r'\["([a-z_]+)", [0-9.]+, [0-9.]+, -?[0-9.]+\]', ad):
        uses.setdefault(spot, []).append('SCENE_SPOTS')
    for m in re.findall(r'\{\d+: "([a-z_]+)"\}', ad):
        uses.setdefault(m, []).append('SCENE_MUSIC')
    amb = re.findall(r'\["([a-z_]+)", -?[0-9.]+\]', ad)
    srows = []
    for name, expr in sorted(cues.items()):
        rel = expr.split('"')[1]
        path = {'A': 'assets/audio/', 'E': 'assets/audio/phase05_elevenlabs/', 'P6': 'assets/audio/phase06_elevenlabs/'}[expr.split(' ')[0]] + rel
        if expr.startswith('E') and 'phase06' in ad and False:
            pass
        rec = sm.get(name, {})
        source = 'ElevenLabs sound generation' if rec else ('ElevenLabs sound generation (PENDING approval)' if 'phase06' in path else 'licensed library (asset_library/licenses, ASSET_MANIFEST.md)')
        srows.append({'cue': name, 'file': path, 'exists': (R / path).exists(), 'duration_s': probe_seconds(R / path) if (R / path).exists() else '',
                      'source': source, 'prompt': rec.get('prompt', ''), 'kind': rec.get('kind', ''),
                      'used_by': ' '.join(uses.get(name, []) + (['SCENE_AMBIENCE'] if name in amb else [])),
                      'human_review': 'HUMAN_AUDIO_REVIEW_PENDING'})
    for surf in ('concrete', 'metal', 'asphalt', 'tile'):
        files = sorted((R / 'assets/audio/phase05_elevenlabs/footsteps').glob(surf + '_*.ogg'))
        srows.append({'cue': 'footstep_' + surf, 'file': 'assets/audio/phase05_elevenlabs/footsteps/%s_NN.ogg (%d takes)' % (surf, len(files)),
                      'exists': bool(files), 'duration_s': '', 'source': 'ElevenLabs sound generation, sliced',
                      'prompt': sm.get('steps_' + surf, {}).get('prompt', ''), 'kind': 'steps',
                      'used_by': 'scripts/player/character_visual.gd _footsteps', 'human_review': 'HUMAN_AUDIO_REVIEW_PENDING'})
    with (D / 'SFX_MANIFEST.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(srows[0]))
        w.writeheader()
        w.writerows(srows)
    print('DIALOGUE', len(rows), {s: sum(r['qa_status'] == s for r in rows) for s in ('RUNTIME_VOICED', 'NOT_TRIGGERED', 'MISSING_AUDIO')})
    print('SFX', len(srows), 'unused:', [r['cue'] for r in srows if not r['used_by']])


if __name__ == '__main__':
    main()

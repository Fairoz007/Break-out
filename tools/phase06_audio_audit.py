"""Phase 06 automated audio audit. It checks files, mappings, references, licences and secrets; it does NOT and
cannot judge voice acting or audio quality (that is the human listening review, HUMAN_AUDIO_REVIEW_PENDING).

Checks: every dialogue ID has a take; takes decode with a valid duration; no zero-length audio files; subtitle text
matches the screenplay; one voice per character; every cue the code calls is defined and its file exists (or is
listed as pending generation); every generated file is referenced by the game; licences/attribution recorded;
no API keys in tracked files (and whether any appear in git history); runtime evidence of voiced lines.
python3 -I tools/phase06_audio_audit.py   -> tests/phase06/evidence/audio_audit.json, exit 1 on any FAIL
"""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from elevenlabs_client import probe_seconds, decodes

R = Path(__file__).resolve().parents[1]
OUT = R / 'tests/phase06/evidence/audio_audit.json'
KEY_RE = r'sk_[0-9a-f]{40,}'
checks = []


def check(name, ok, detail='', status=None):
    checks.append({'check': name, 'status': status or ('PASS' if ok else 'FAIL'), 'detail': detail})


def main():
    lines = json.loads((R / 'data/ch01/dialogue.json').read_text())['lines']
    vdir = R / 'assets/audio/voice/ch01'
    vm = json.loads((vdir / 'voice_manifest.json').read_text())
    missing = [l['id'] for l in lines if not (vdir / (l['id'] + '.ogg')).exists()]
    check('every dialogue ID has a take', not missing, '%d lines, missing %s' % (len(lines), missing))
    bad = []
    for l in lines:
        f = vdir / (l['id'] + '.ogg')
        if f.exists():
            s = probe_seconds(f)
            if not s or s < 0.2 or s > 20 or not decodes(f):
                bad.append((l['id'], s))
    check('takes decode with a valid duration (0.2-20 s)', not bad, str(bad))
    zero = [str(p.relative_to(R)) for p in (R / 'assets/audio').rglob('*') if p.suffix in ('.ogg', '.wav', '.mp3') and p.stat().st_size == 0]
    check('no zero-length audio files under assets/audio', not zero, str(zero))
    mism = [l['id'] for l in lines if vm['lines'].get(l['id'], {}).get('text') != l['text']]
    check('subtitle text == recorded text == screenplay', not mism, str(mism))
    voices = {}
    for lid, g in vm['lines'].items():
        voices.setdefault(g['speaker'], set()).add(g['voice_id'])
    multi = {k: sorted(v) for k, v in voices.items() if len(v) > 1}
    check('one voice per character across the chapter', not multi, json.dumps({k: sorted(v) for k, v in voices.items()}))

    ad = (R / 'scripts/core/audio_director.gd').read_text()
    consts = dict(re.findall(r'const (A|E|P6) := "([^"]+)"', ad))
    cues = {}
    for name, base, rel in re.findall(r'\t"([a-z_]+)": (A|E|P6) \+ "([^"]+)"', ad):
        cues[name] = consts[base].replace('res://', '') + rel
    code = '\n'.join(p.read_text() for p in (R / 'scripts').rglob('*.gd'))
    called = set(re.findall(r'(?:cue|start_bed|play_music)\("([a-z_]+)"', code)) | set(re.findall(r'\["([a-z_]+)", -?[0-9.]+\]', ad))
    called |= set(re.findall(r'\["([a-z_]+)", [0-9.]+, [0-9.]+, -?[0-9.]+\]', ad)) | set(re.findall(r'\{\d+: "([a-z_]+)"\}', ad))
    door = (R / 'scripts/world/door.gd').read_text()
    sounds = door[door.index('const SOUNDS'):door.index('\n\n', door.index('const SOUNDS'))]
    called |= {x for pair in re.findall(r'\["(\w+)", "(\w+)"\]', sounds) for x in pair}
    called |= set(re.findall(r'cue\("(\w+)" if', code)) | set(re.findall(r'else "(\w+)", null', code))
    called.discard('')
    undefined = sorted(c for c in called if c not in cues)
    check('every cue the code calls is defined', not undefined, str(undefined))
    p6_spec = re.findall(r"^    '([a-z_]+)': \(", (R / 'tools/phase06_elevenlabs_sfx.py').read_text(), re.M)
    absent = sorted(c for c, f in cues.items() if not (R / f).exists())
    pending = [c for c in absent if c in p6_spec]
    hard = [c for c in absent if c not in p6_spec]
    check('every defined cue has its file', not hard, 'missing (not pending): %s' % hard)
    check('cues pending billable generation (approval required)', True, str(pending), status='PENDING' if pending else 'PASS')

    gen = [p for p in (R / 'assets/audio/phase05_elevenlabs').rglob('*.ogg')] + [p for p in (R / 'assets/audio/phase06_elevenlabs').rglob('*.ogg')] if (R / 'assets/audio/phase06_elevenlabs').exists() else list((R / 'assets/audio/phase05_elevenlabs').rglob('*.ogg'))
    referenced = set(cues.values())
    unref = [str(p.relative_to(R)) for p in gen if str(p.relative_to(R)) not in referenced and '/footsteps/' not in str(p)]
    check('every generated effect is referenced by the game', not unref, str(unref))
    unused_cues = sorted(c for c in cues if c not in called)
    check('defined cues that nothing triggers (informational)', True, str(unused_cues), status='INFO')

    credits = (R / 'data/credits.txt').read_text()
    lic_ok = 'ElevenLabs' in credits and (R / 'assets/audio/phase05_elevenlabs/sfx_manifest.json').exists() and (vdir / 'voice_manifest.json').exists()
    check('ElevenLabs attribution in credits and generation manifests present', lic_ok)
    check('ElevenLabs free-plan commercial licence', True, 'free plan: attribution required, no commercial licence; regenerate on a paid plan before commercial release', status='WARN')

    tracked = subprocess.run(['git', 'grep', '-l', '-E', KEY_RE], cwd=R, capture_output=True, text=True).stdout.split()
    check('no API keys in tracked files', not tracked, str(tracked))
    hist = subprocess.run(['git', 'log', '--all', '-G', KEY_RE, '--format=%h'], cwd=R, capture_output=True, text=True).stdout.split()
    check('no API keys anywhere in git history', not hist, 'commits: %s (keys must be rotated)' % hist, status='PASS' if not hist else 'WARN')
    ign = subprocess.run(['git', 'check-ignore', '.secrets/elevenlabs.env'], cwd=R, capture_output=True, text=True).returncode == 0
    exp = '.secrets/*' in (R / 'export_presets.cfg').read_text()
    check('local secrets file git-ignored and excluded from exports', ign and exp)

    seen = set()
    for f in (R / 'tests/phase06/evidence').glob('chapter_*.json'):
        for e in json.loads(f.read_text())['events']:
            if e['kind'] == 'dialogue_shown' and e.get('voice'):
                seen.add(e['id'])
    check('runtime: every line shown with its take loaded and its player started (union of chapter runs; dummy audio driver)', len(seen) == len(lines), '%d/%d' % (len(seen), len(lines)))
    check('human listening review', True, 'HUMAN_AUDIO_REVIEW_PENDING', status='PENDING')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({'checks': checks}, indent=1))
    for c in checks:
        print('%-8s %s  %s' % (c['status'], c['check'], c['detail'][:150]))
    sys.exit(1 if any(c['status'] == 'FAIL' for c in checks) else 0)


if __name__ == '__main__':
    main()

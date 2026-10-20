"""Phase 06: missing mission sounds and tension beds via ElevenLabs text-to-sound-effects.

The ElevenLabs Music API is refused on the free plan (HTTP 402 paid_plan_required, 20 Oct 2026), so the tension
underscore is generated as sound-effect beds (drones/pulses, <= 22 s, crossfade-looped), not composed music.
Credentials: tools/elevenlabs_client.py (ELEVENLABS_API_KEY / .secrets/elevenlabs.env); the last key is used first.
Cache: each item is keyed by sha256(prompt, seconds, influence); a downloaded take is never requested twice.
Usage before/after the batch goes to build/elevenlabs_usage.jsonl and the manifest.
python3 -I tools/phase06_elevenlabs_sfx.py [--only a,b] [--estimate]
"""
import json, sys, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import elevenlabs_client as el
from phase05_elevenlabs_sfx import ff, dur, cap_peak

R = Path(__file__).resolve().parents[1]
OUT = R / 'assets/audio/phase06_elevenlabs'
TMP = R / 'build/sfx_tmp_p06'
CREDITS_PER_SECOND = 10.0   # measured on this account in Phase 05 (1,765 credits for ~185 s generated)
SPEC = {
    'music_tension': ('Minimal tense cinematic underscore for a night-time prison stealth sequence: low pulsing sub bass, '
                      'soft ticking percussion, faint metallic textures, no melody, steady and loopable', 20, 'loop'),
    'music_chase': ('Driving tense cinematic chase underscore: urgent low percussion, pulsing bass ostinato, rising '
                    'metallic hits, no melody, steady tempo, loopable', 15, 'loop'),
    'music_betrayal': ('Somber cinematic underscore for a betrayal scene: slow low string drone, distant piano notes, '
                       'heavy and quiet, loopable', 20, 'loop'),
    'sting_capture': ('Short dark cinematic stinger: deep orchestral hit with a low boom fading into silence', 4, 'one'),
    'dryer': ('Industrial laundry tumble dryers running, steady rumble and soft fabric tumbling, inside a workshop', 12, 'loop'),
    'cart': ('Metal laundry cart pushed across a concrete floor, rattling wheels', 3, 'one'),
    'tools': ('Metal hand tools set down on a steel workbench, wrench clank', 2, 'one'),
    'switch': ('Heavy industrial electrical switch thrown, loud mechanical clack', 1, 'one'),
    'pipe_groan': ('Old metal water pipe groaning and vibrating as pressure changes, deep resonant creak', 4, 'one'),
    'drips': ('Water dripping into puddles in a long concrete maintenance tunnel, sparse drips, faint echo', 12, 'loop'),
    'electric_hum': ('Electrical transformer and conduit hum in a maintenance tunnel, steady low buzz', 10, 'loop'),
    'bus_arrive': ('Old prison transport bus driving in slowly and stopping: diesel engine, squealing brakes, air brake hiss', 7, 'one'),
    'bus_engine_off': ('Diesel bus engine shutting down, rattle and a final shudder, then silence', 3, 'one'),
    'cellblock_day': ('Prison cell block daytime ambience: distant inmates talking, echoing voices, a far metal door, no music', 15, 'loop'),
}


def main():
    only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else set()
    items = {k: v for k, v in SPEC.items() if not only or k in only}
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    man_p = OUT / 'sfx_manifest.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {'generator': 'ElevenLabs text-to-sound-effects', 'items': {}}
    todo = {k: v for k, v in items.items() if man['items'].get(k, {}).get('cache') != el.cache_key(p=v[0], s=v[1], i=0.55)}
    est = sum(v[1] for v in todo.values()) * CREDITS_PER_SECOND
    print('ESTIMATE items=%d seconds=%d credits~%d' % (len(todo), sum(v[1] for v in todo.values()), est))
    if '--estimate' in sys.argv or not todo:
        return
    c = el.Client(prefer_last=True)
    before = c.usage_all()
    for name, (prompt, secs, kind) in todo.items():
        ck = el.cache_key(p=prompt, s=secs, i=0.55)
        raw = TMP / ('%s_%s.mp3' % (name, ck))
        if not raw.exists():
            raw.write_bytes(c.sfx(prompt, secs))
        out = OUT / (name + '.ogg')
        if kind == 'one':
            ff('-i', str(raw), '-af', 'silenceremove=start_periods=1:start_threshold=-50dB,loudnorm=I=-16:TP=-1.5',
               '-ac', '2' if name.startswith('sting') else '1', '-ar', '44100', '-c:a', 'libvorbis', '-q:a', '6', str(out))
        else:
            L = dur(raw)
            X = min(1.5, L / 4)
            lufs = -22 if name.startswith('music') else -20
            ff('-i', str(raw), '-i', str(raw), '-filter_complex',
               '[0]atrim=%f:%f,asetpts=PTS-STARTPTS[a];[1]atrim=0:%f,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=%f:c1=tri:c2=tri,loudnorm=I=%d:TP=-2' % (X, L, X, X, lufs),
               '-ac', '2', '-ar', '44100', '-c:a', 'libvorbis', '-q:a', '6', str(out))
        cap_peak(out)
        secs_out = el.probe_seconds(out)
        if not (secs_out and secs_out > 0.2 and el.decodes(out)):
            raise SystemExit('validation failed: ' + name)
        man['items'][name] = {'prompt': prompt, 'requested_seconds': secs, 'kind': kind, 'cache': ck, 'key': c.key_no,
                              'files': [{'path': str(out.relative_to(R)), 'seconds': secs_out, 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}]}
        man_p.write_text(json.dumps(man, indent=1))
        print(name, kind, secs_out, flush=True)
    after = c.usage_all()
    rec = el.log_usage('phase06_sfx', before, after, len(todo))
    man.setdefault('usage', []).append(rec)
    man_p.write_text(json.dumps(man, indent=1))
    print('USAGE', rec['credits_used'])


if __name__ == '__main__':
    main()

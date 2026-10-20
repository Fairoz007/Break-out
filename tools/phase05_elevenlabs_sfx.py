"""Phase 05 audio: sound effects and ambience beds generated with ElevenLabs text-to-sound-effects.

Replaces the synthetic placeholders and mismatched stand-ins in scripts/core/audio_director.gd (alarm, whistle,
breaker, relay, PA chime, fluorescent and fan loops, handcuffs, basketball, handset, steel doors ...), adds the
missing beds (yard crowd, cell block at night, radio chatter, bus idle) and surface footsteps (none were played).

Keys are never stored in the repository: pass a file with one API key per line; the LAST key is tried first
(the first key is reserved for voice-over).
python3 -I tools/phase05_elevenlabs_sfx.py <keys_file> [--only name,name] [--redo]
Outputs: assets/audio/phase05_elevenlabs/<name>.ogg, footsteps/<surface>_NN.ogg, sfx_manifest.json
"""
import json, sys, subprocess, hashlib, time, urllib.request, urllib.error, re
from pathlib import Path

R = Path(__file__).resolve().parents[1]
OUT = R / 'assets/audio/phase05_elevenlabs'
TMP = R / 'build/sfx_tmp'
# name: (prompt, seconds, kind) kind: one = one-shot, loop = seamless bed, steps = slice into single footsteps
SPEC = {
    'alarm': ('Prison facility lockdown alarm, repeating two-tone electronic klaxon siren echoing down concrete corridors, continuous', 10, 'loop'),
    'whistle': ('A single sharp blast of a guard whistle in a concrete prison corridor, short natural reverb', 2, 'one'),
    'breaker_trip': ('Heavy industrial circuit breaker tripping: loud mechanical clunk, then an electrical hum winding down to silence', 3, 'one'),
    'detect_warn': ('Short tense low brass and string stinger, someone has been spotted, cinematic suspense hit', 1.5, 'one'),
    'relay_click': ('Electrical relay contactor clicking on inside a metal control cabinet, close up', 1, 'one'),
    'pa_chime': ('Old institutional public address two-tone chime through worn ceiling speakers, slight distortion', 3, 'one'),
    'fluorescent': ('Fluorescent tube lights buzzing and humming steadily in a quiet concrete room, room tone', 12, 'loop'),
    'ventilation': ('Industrial ventilation duct air handler, steady low drone with moving air, inside a building', 15, 'loop'),
    'cuffs': ('Steel handcuffs ratcheting closed around two wrists, quick metallic clicks', 2, 'one'),
    'ball_bounce': ('One basketball bounce on an outdoor concrete court', 1, 'one'),
    'handset': ('Lifting an old heavy wall telephone handset off its metal hook switch, plastic and metal click', 1.5, 'one'),
    'pipe_knock': ('A single knuckle knock on a thick metal water pipe, resonant ring', 1, 'one'),
    'pipe_reply': ('A single faint muffled knock on a metal pipe heard through a thick concrete wall', 1, 'one'),
    'grille': ('Heavy steel barred security gate sliding open on rails, motor whine and rattling bars, prison', 3, 'one'),
    'cell_slam': ('Prison cell door of steel bars slamming shut, heavy metal impact with long concrete echo', 2.5, 'one'),
    'door_open': ('Heavy steel security door unlatching and swinging open, latch clack and low hinge creak', 2, 'one'),
    'door_close': ('Heavy steel security door swinging shut and latching with a solid clunk', 2, 'one'),
    'lever': ('Heavy industrial lever pulled down hard, grinding metal clunk', 1.5, 'one'),
    'panel': ('Metal electrical access panel pried open, scraping sheet metal and a screw rattling', 1.5, 'one'),
    'count_bell': ('Old electric institutional bell ringing for headcount in a prison block, then stopping', 3, 'one'),
    'bus_doors': ('Bus pneumatic folding door opening with a sharp air hiss', 2, 'one'),
    'bus_diesel': ('Idling diesel engine of an old transport bus, steady rumble from outside', 12, 'loop'),
    'crowd': ('Outdoor prison yard ambience, many inmates talking and murmuring at a distance, occasional shout, no music', 15, 'loop'),
    'cellblock_night': ('Prison cell block at night ambience, distant echoing footsteps, faint coughing, far metal door, quiet hum', 15, 'loop'),
    'radio': ('Distant security radio chatter, garbled dispatcher voice, squelch and static bursts, walkie talkie', 10, 'loop'),
    'steps_concrete': ('Footsteps of one man in work boots walking slowly on a concrete floor indoors, eight separate steps, no other sounds', 5, 'steps'),
    'steps_metal': ('Footsteps of one man in work boots walking slowly on a metal grating catwalk, eight separate clanging steps, no other sounds', 5, 'steps'),
    'steps_asphalt': ('Footsteps of one man in work boots walking slowly on gritty outdoor asphalt, eight separate steps, no other sounds', 5, 'steps'),
    'steps_tile': ('Footsteps of one man in hard shoes walking slowly on a tiled floor in an echoing room, eight separate steps', 5, 'steps'),
}


def gen(key, prompt, secs):
    body = {'text': prompt, 'duration_seconds': secs, 'prompt_influence': 0.55}
    req = urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation', data=json.dumps(body).encode(),
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def dur(p):
    for entry in ('format=duration', 'stream=duration'):
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', entry, '-of', 'csv=p=0', str(p)],
                             capture_output=True, text=True).stdout.strip().splitlines()
        vals = [v for v in out if v and v != 'N/A']
        if vals:
            return float(vals[0])
    raise RuntimeError('no duration for %s' % p)


def ff(*a):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *a], check=True)


def peak_db(p):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(p), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.search(r'max_volume: ([-0-9.]+) dB', e)
    return float(m.group(1)) if m else 0.0


def cap_peak(p, ceiling=-1.5):
    """loudnorm resamples internally and short transients slip past the limiter: measure and pull the peak down."""
    pk = peak_db(p)
    if pk > ceiling:
        tmp = p.with_suffix('.cap.ogg')
        ff('-i', str(p), '-af', 'volume=%.2fdB' % (ceiling - 0.3 - pk), '-c:a', 'libvorbis', '-q:a', '6', str(tmp))
        tmp.replace(p)


def main():
    keys = [k.strip() for k in Path(sys.argv[1]).read_text().splitlines() if k.strip()][::-1]
    only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else set()
    redo = '--redo' in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'footsteps').mkdir(exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    man_p = OUT / 'sfx_manifest.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {'generator': 'ElevenLabs text-to-sound-effects', 'items': {}}
    ki = 0
    for name, (prompt, secs, kind) in SPEC.items():
        if only and name not in only:
            continue
        if name in man['items'] and not redo:
            continue
        raw = TMP / (name + '.mp3')
        while not (raw.exists() and (not redo or '--reencode' in sys.argv)):   # a downloaded take is reused, never paid for twice
            try:
                raw.write_bytes(gen(keys[ki], prompt, secs))
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors='replace')
                if e.code in (401, 402, 403) and ki + 1 < len(keys):
                    print('key exhausted/refused (%d), switching: %s' % (e.code, msg[:120]), flush=True)
                    ki += 1
                    continue
                if e.code == 429:
                    time.sleep(5)
                    continue
                raise SystemExit('%s HTTP %d %s' % (name, e.code, msg[:300]))
        files = []
        if kind == 'one':
            out = OUT / (name + '.ogg')
            ff('-i', str(raw), '-af', 'silenceremove=start_periods=1:start_threshold=-50dB,loudnorm=I=-16:TP=-1.5,alimiter=limit=0.85:level=false',
               '-ac', '1', '-ar', '44100', '-c:a', 'libvorbis', '-q:a', '6', str(out))
            files.append(out)
        elif kind == 'loop':
            # seamless: the last X seconds crossfade into the first X, so the end flows into the start
            L = dur(raw)
            X = min(1.5, L / 4)
            out = OUT / (name + '.ogg')
            ff('-i', str(raw), '-i', str(raw), '-filter_complex',
               '[0]atrim=%f:%f,asetpts=PTS-STARTPTS[a];[1]atrim=0:%f,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=%f:c1=tri:c2=tri,loudnorm=I=-20:TP=-2,alimiter=limit=0.8:level=false' % (X, L, X, X),
               '-ac', '2', '-ar', '44100', '-c:a', 'libvorbis', '-q:a', '6', str(out))
            files.append(out)
        else:
            # slice single steps at the silences between them
            sd = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(raw), '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'],
                                capture_output=True, text=True).stderr
            starts = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', sd)]
            ends = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', sd)]
            L = dur(raw)
            onsets = ([0.0] if not ends or (starts and starts[0] > ends[0]) else []) + starts
            surface = name.split('_', 1)[1]
            n = 0
            for o in onsets:
                nxt = min([e for e in ends if e > o + 0.05] + [L])
                seg = min(nxt - o + 0.08, 0.7)
                if seg < 0.08:
                    continue
                out = OUT / 'footsteps' / ('%s_%02d.ogg' % (surface, n))
                ff('-ss', '%f' % max(o - 0.01, 0), '-t', '%f' % seg, '-i', str(raw), '-af',
                   'afade=t=out:st=%f:d=0.06,loudnorm=I=-18:TP=-2,alimiter=limit=0.8:level=false' % max(seg - 0.06, 0), '-ac', '1', '-ar', '44100',
                   '-c:a', 'libvorbis', '-q:a', '6', str(out))
                if dur(out) < 0.1:   # the recording ended inside this slice
                    out.unlink()
                    continue
                files.append(out)
                n += 1
        for f in files:
            cap_peak(f)
        man['items'][name] = {'prompt': prompt, 'requested_seconds': secs, 'kind': kind,
                              'files': [{'path': str(f.relative_to(R)), 'seconds': round(dur(f), 3), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]}
        man_p.write_text(json.dumps(man, indent=1))
        print(name, kind, [round(dur(f), 2) for f in files], flush=True)
    print('SFX', len(man['items']), 'of', len(SPEC))


if __name__ == '__main__':
    main()

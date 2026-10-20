"""Phase 05 audio: voice-over for the 145 canonical Chapter 1 lines (data/ch01/dialogue.json) with ElevenLabs TTS.

Keys: the KEYS list below, or a file with one API key per line given as the first argument.
Resumable: lines whose .ogg already exists are skipped. When a key runs out of credits the next key is used.

python3 -I tools/phase05_elevenlabs_voices.py [keys_file] [--only ID,ID] [--redo]
Outputs: assets/audio/voice/ch01/<LINE_ID>.ogg (mono 44.1 kHz Vorbis), manifest assets/audio/voice/ch01/voice_manifest.json
"""
import json, sys, subprocess, hashlib, time, urllib.request, urllib.error
from pathlib import Path

# ElevenLabs free-plan keys, committed in the open at the owner's request (20 Oct 2026). Pass a key file as the first
# argument to use other keys instead.
KEYS = ['sk_393420e01fb87239b13f65e16639948c75ffb896ac014385', 'sk_093bb936fc0ed41670db9145795e552032a0be05a66ba07a']

R = Path(__file__).resolve().parents[1]
OUT = R / 'assets/audio/voice/ch01'
TMP = R / 'build/voice_tmp'
MODEL = 'eleven_multilingual_v2'
# Casting (premade ElevenLabs voices, American unless noted), from docs/characters/*.md ages and delivery notes.
CAST = {
    'ADRIAN': ('nPczCjzI2devNBz1zQrb', 'Brian', 'Adrian Cross, 34: tired ex-investigator; low, controlled'),
    'NOAH': ('TX3LPaxmHKxFdv7VOQHJ', 'Liam', 'Noah Reyes, 29: warm, quick; intimate, tense'),
    'RUSK': ('pNInz6obpgDQGcFmaJgB', 'Adam', 'Tomas Rusk, 41: guard officer; clipped, guarded'),
    'GUARD': ('SOYHLrjzK2X1ezoPC6cr', 'Harry', 'shift guards; clipped, rough'),
    'SILAS': ('N2lVS1w4EtoT3dr4eOWO', 'Callum', 'Silas Bell, 38: favour broker; husky'),
    'MARA': ('XrExE9yKIg1WjnnlVkGX', 'Matilda', 'Dr Mara Sen, 46: clinic doctor; natural, understated'),
    'RECORDING': ('onwK4e9ZLuTAKqWW03F9', 'Daniel (British)', 'calibration-log recording; band-limited after synthesis'),
}
# delivery note -> voice settings (stability lower = more expressive)
DELIVERY = {
    'low, controlled': {'stability': 0.55, 'similarity_boost': 0.8, 'style': 0.15},
    'intimate, tense': {'stability': 0.38, 'similarity_boost': 0.8, 'style': 0.35},
    'clipped, guarded': {'stability': 0.5, 'similarity_boost': 0.8, 'style': 0.25},
    'natural, understated': {'stability': 0.6, 'similarity_boost': 0.75, 'style': 0.1},
}


def lines():
    d = json.loads((R / 'data/ch01/dialogue.json').read_text())
    return next(v for v in d.values() if isinstance(v, list)) if isinstance(d, dict) else d


def tts(key, voice, text, settings, prev_text, next_text):
    body = {'text': text, 'model_id': MODEL, 'voice_settings': dict(settings, use_speaker_boost=True)}
    if prev_text:
        body['previous_text'] = prev_text
    if next_text:
        body['next_text'] = next_text
    req = urllib.request.Request(
        'https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % voice,
        data=json.dumps(body).encode(), headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.headers.get('request-id') or r.headers.get('x-request-id')


def probe_seconds(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                         capture_output=True, text=True).stdout.strip()
    return round(float(out), 3) if out else None


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else None
    keys = [k.strip() for k in Path(arg).read_text().splitlines() if k.strip()] if arg else KEYS
    only = set()
    if '--only' in sys.argv:
        only = set(sys.argv[sys.argv.index('--only') + 1].split(','))
    redo = '--redo' in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    man_p = OUT / 'voice_manifest.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {'generator': 'ElevenLabs text-to-speech', 'model': MODEL,
                                                                   'cast': {k: {'voice_id': v[0], 'voice': v[1], 'note': v[2]} for k, v in CAST.items()},
                                                                   'lines': {}}
    L = lines()
    by_mission = {}
    for l in L:
        by_mission.setdefault(l['mission'], []).append(l)
    ki = 0
    for i, l in enumerate(L):
        lid = l['id']
        if only and lid not in only:
            continue
        ogg = OUT / (lid + '.ogg')
        if ogg.exists() and not redo:
            continue
        ml = by_mission[l['mission']]
        j = ml.index(l)
        prev_text = ml[j - 1]['text'] if j > 0 else ''
        next_text = ml[j + 1]['text'] if j + 1 < len(ml) else ''
        voice, vname, _ = CAST[l['speaker']]
        settings = DELIVERY.get(l['delivery'], DELIVERY['natural, understated'])
        mp3 = TMP / (lid + '.mp3')
        rid = man['lines'].get(lid, {}).get('request_id')
        while not (mp3.exists() and '--reencode' in sys.argv):   # --reencode: reuse the downloaded take
            try:
                audio, rid = tts(keys[ki], voice, l['text'], settings, prev_text, next_text)
                mp3.write_bytes(audio)
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors='replace')
                if e.code in (401, 402, 403) and ('quota' in msg or 'credits' in msg or 'limit' in msg) and ki + 1 < len(keys):
                    print('key %d exhausted, switching' % (ki + 1), flush=True)
                    ki += 1
                    continue
                if e.code == 429:
                    time.sleep(5)
                    continue
                raise SystemExit('%s HTTP %d %s' % (lid, e.code, msg[:300]))
        # trim the take's leading/trailing silence (keeps ~60 ms of air), then normalise
        trim = ['silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06', 'areverse',
                'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06', 'areverse']
        af = trim + ['loudnorm=I=-18:TP=-2:LRA=9']
        if l['speaker'] == 'RECORDING':   # tape/channel recording played through a speaker
            af = trim + ['highpass=f=320', 'lowpass=f=3400', 'acompressor=threshold=-20dB:ratio=4', 'loudnorm=I=-20:TP=-2']
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(mp3), '-af', ','.join(af), '-ac', '1', '-ar', '44100',
                        '-c:a', 'libvorbis', '-q:a', '5', str(ogg)], check=True)
        secs = probe_seconds(ogg)
        man['lines'][lid] = {'speaker': l['speaker'], 'voice': vname, 'voice_id': voice, 'text': l['text'], 'delivery': l['delivery'],
                             'settings': settings, 'characters': len(l['text']), 'seconds': secs, 'subtitle_seconds': l['duration'],
                             'over_subtitle': bool(secs and secs > l['duration']), 'key_index': ki + 1, 'request_id': rid,
                             'sha256': hashlib.sha256(ogg.read_bytes()).hexdigest()}
        man_p.write_text(json.dumps(man, indent=1))
        print('%s %s %.2fs (subtitle %.1fs) key%d' % (lid, l['speaker'], secs or 0, l['duration'], ki + 1), flush=True)
    done = len(man['lines'])
    print('VOICES', done, 'of', len(L), 'chars', sum(v['characters'] for v in man['lines'].values()))


if __name__ == '__main__':
    main()

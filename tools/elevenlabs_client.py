"""Shared ElevenLabs client for the offline audio pipeline (Phase 06).

Credentials: ELEVENLABS_API_KEY (one key, or several separated by commas) from the environment, else from the
git-ignored file .secrets/elevenlabs.env (KEY=VALUE lines). Keys are never printed: logs show key #n only.
The game never calls ElevenLabs; it plays the bundled files this pipeline writes.

Provides: retry with backoff (429/5xx/network), key rotation when a key is out of credits, usage tracking
(subscription character_count before/after each batch, appended to build/elevenlabs_usage.jsonl and the manifests),
output validation (decodes with ffprobe, non-zero duration) and stable cache hashes of (text/prompt, voice, model,
settings) so unchanged requests are never paid for twice.
"""
import hashlib, json, os, time, subprocess, urllib.request, urllib.error
from pathlib import Path

R = Path(__file__).resolve().parents[1]
API = 'https://api.elevenlabs.io'
USAGE_LOG = R / 'build/elevenlabs_usage.jsonl'


def load_keys():
    raw = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not raw:
        f = R / '.secrets/elevenlabs.env'
        if f.exists():
            for line in f.read_text().splitlines():
                if line.strip().startswith('ELEVENLABS_API_KEY='):
                    raw = line.split('=', 1)[1].strip()
    keys = [k.strip() for k in raw.split(',') if k.strip()]
    if not keys:
        raise SystemExit('No ElevenLabs key: set ELEVENLABS_API_KEY or create .secrets/elevenlabs.env')
    return keys


def cache_key(**parts):
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:16]


def _request(key, method, path, body=None, accept='application/json', timeout=180):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': accept})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), dict(r.headers)


class Client:
    def __init__(self, keys=None, prefer_last=False):
        self.keys = keys or load_keys()
        self.order = list(range(len(self.keys)))[::-1] if prefer_last else list(range(len(self.keys)))
        self.ki = 0

    @property
    def key_no(self):
        return self.order[self.ki] + 1

    def subscription(self, i=None):
        k = self.keys[self.order[self.ki] if i is None else i]
        b, _ = _request(k, 'GET', '/v1/user/subscription')
        d = json.loads(b)
        return {'tier': d.get('tier'), 'used': d.get('character_count'), 'limit': d.get('character_limit')}

    def usage_all(self):
        return {'key%d' % (i + 1): self.subscription(i) for i in range(len(self.keys))}

    def call(self, path, body, accept='audio/mpeg'):
        """POST with retries; rotates to the next key when one is out of credits or refused."""
        delay = 2
        for attempt in range(8):
            try:
                return _request(self.keys[self.order[self.ki]], 'POST', path, body, accept)
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors='replace')
                if e.code in (401, 402, 403) and self.ki + 1 < len(self.keys):
                    print('key #%d refused (%d: %s); rotating' % (self.key_no, e.code, msg[:120]), flush=True)
                    self.ki += 1
                    continue
                if e.code == 429 or e.code >= 500:
                    time.sleep(delay)
                    delay = min(delay * 2, 30)
                    continue
                raise RuntimeError('HTTP %d %s' % (e.code, msg[:300]))
            except (urllib.error.URLError, TimeoutError) as e:
                time.sleep(delay)
                delay = min(delay * 2, 30)
        raise RuntimeError('ElevenLabs request failed after retries: ' + path)

    def tts(self, voice_id, text, model, settings, previous_text='', next_text='', fmt='mp3_44100_128'):
        body = {'text': text, 'model_id': model, 'voice_settings': settings}
        if previous_text:
            body['previous_text'] = previous_text
        if next_text:
            body['next_text'] = next_text
        audio, h = self.call('/v1/text-to-speech/%s?output_format=%s' % (voice_id, fmt), body)
        return audio, h.get('request-id') or h.get('x-request-id')

    def sfx(self, prompt, seconds, influence=0.55, loop=False):
        body = {'text': prompt, 'duration_seconds': seconds, 'prompt_influence': influence}
        if loop:
            body['loop'] = True
        audio, h = self.call('/v1/sound-generation', body)
        return audio


def log_usage(batch, before, after, items):
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    rec = {'time': time.strftime('%Y-%m-%dT%H:%M:%S'), 'batch': batch, 'items': items, 'before': before, 'after': after,
           'credits_used': {k: (after[k]['used'] or 0) - (before[k]['used'] or 0) for k in before}}
    with USAGE_LOG.open('a') as f:
        f.write(json.dumps(rec) + '\n')
    return rec


def probe_seconds(path):
    """Decode check: returns the duration in seconds, or None when the file does not decode."""
    for entry in ('format=duration', 'stream=duration'):
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', entry, '-of', 'csv=p=0', str(path)],
                             capture_output=True, text=True).stdout.strip().splitlines()
        vals = [v for v in out if v and v != 'N/A']
        if vals:
            return round(float(vals[0]), 3)
    return None


def decodes(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True, text=True)
    return r.returncode == 0 and not r.stderr.strip()

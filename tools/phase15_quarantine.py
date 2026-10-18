"""Move REJECTED / FAILED / SUPERSEDED runtime files out of the shippable assets/ tree (QA finding QAF-04/18).
Files are moved (never deleted) to asset_library/rejected/<area>/ with their relative path kept; fragment records get
runtime_file = None, rejected_file = <new path>, and keep their status. Idempotent. python -I tools/phase15_quarantine.py"""
import json, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[1]; M = R / 'asset_library/manifests'
audit = json.loads((M / 'phase15/audio_materials_audit.json').read_text(encoding='utf-8'))
REJ_AUDIO = {x['runtime_file']: x['reasons'] for x in audit['rejected_audio']}
RULES = {  # asset_id -> (status, reason)
    'P15_CHAR_ADRIAN': ('FAILED', 'MPFB retarget failed visual deformation (5 cycles)'), 'P15_CHAR_NOAH': ('FAILED', 'MPFB retarget failed visual deformation (5 cycles)'),
    'P15_CHAR_GUARD': ('FAILED', 'MPFB retarget failed visual deformation (5 cycles)'), 'P15_CHAR_INMATE': ('FAILED', 'MPFB retarget failed visual deformation (5 cycles)'),
    'P15_PROXY_ADRIAN': ('SUPERSEDED', 'diagnostic sine-walk proxy superseded by P15_RB_ADRIAN / P15_UBC_ADRIAN'),
    'P15_PROXY_NOAH': ('SUPERSEDED', 'diagnostic sine-walk proxy superseded by P15_RB_NOAH / P15_UBC_NOAH'),
    'DISC15_OGA_GUARD_TOWER': ('REJECTED', 'medieval arrow-turret style; record notes say not for shipping scenes')}
log = []
def move(rel, area, a):
    src = R / rel
    dst = R / 'asset_library/rejected' / area / Path(rel).relative_to('assets')
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.move(str(src), str(dst))
        for side in (src.with_name(src.name + '.import'),):
            if side.exists(): side.unlink()  # Godot import sidecar is regenerated data, not a payload
        log.append({'asset_id': a['asset_id'], 'from': rel, 'to': dst.relative_to(R).as_posix()})
    return dst.relative_to(R).as_posix()
for frag in ['phase15_characters_records.json', 'phase15_bulk_assets.json', 'phase15_bulk_oga_assets.json', 'phase15_discovery_records.json']:
    p = M / frag; recs = json.loads(p.read_text(encoding='utf-8-sig')); changed = False
    for a in recs:
        rf = a.get('runtime_file'); paths = [rf] if isinstance(rf, str) else (rf or [])
        if a['asset_id'] in RULES:
            st, why = RULES[a['asset_id']]
        elif any(x in REJ_AUDIO for x in paths):
            st, why = 'REJECTED', '; '.join(r for x in paths for r in REJ_AUDIO.get(x, []))
        else:
            continue
        if not paths: continue
        area = 'phase15_characters' if 'characters' in paths[0] else 'phase15_audio' if 'audio' in paths[0] else 'phase15_props'
        moved = [move(x, area, a) for x in paths if not x.endswith('.import')]
        a['rejected_file'] = moved[0] if len(moved) == 1 else moved; a['runtime_file'] = None
        a['validation_status'] = st; a['rejection_reasons'] = [why]; a['import_status'] = 'NOT_APPLICABLE'; changed = True
    if changed: p.write_text(json.dumps(recs, indent=2), encoding='utf-8')
# directories left empty by the moves (e.g. guard tower folder) are removed only if empty
for d in sorted({(R / x['from']).parent for x in log}, reverse=True):
    if d.exists() and not any(d.iterdir()): d.rmdir()
out = M / 'phase15/quarantine_log.json'
prev = json.loads(out.read_text()) if out.exists() else []
out.write_text(json.dumps(prev + log, indent=2)); print('moved', len(log))

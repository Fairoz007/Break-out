"""Fold automated test evidence into docs/PHASE_02_REQUIREMENTS.json.

Rules (Phase 02 protocol section 5): this tool never sets VERIFIED. It records automated evidence per requirement
and sets IMPLEMENTED_UNTESTED when the implementation exists, or TEST_FAILED when an automated check failed.
Graphical/manual criteria are listed under "pending_checks" until the independent QA reviewer inspects them.
QA verdicts live in docs/qa/PHASE_02_QA_VERDICTS.json and are applied last (the only route to VERIFIED).
python -I tools/phase02_update_status.py
"""
import json, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REG = R / 'docs/PHASE_02_REQUIREMENTS.json'
EV = R / 'tests/phase02/evidence'
VERDICTS = R / 'docs/qa/PHASE_02_QA_VERDICTS.json'


def load(name):
    p = EV / name
    return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else None


runs = {p.stem: load(p.name) for p in sorted(EV.glob('*.json')) if p.stem != 'system_tests'}
runs = {k: v for k, v in runs.items() if v}
systests = load('system_tests.json') or {'results': []}
sys_ok = {t['test']: t['pass'] for t in systests['results']}


def events(run, kind):
    return [e for e in runs[run]['events'] if e['kind'] == kind] if run in runs else []


def seen(kind, key, value):
    hits = []
    for name in runs:
        if any(e.get(key) == value for e in events(name, kind)):
            hits.append(f'tests/phase02/evidence/{name}.json')
    return hits


def run_ok(name):
    return name in runs and runs[name]['reason'] in ('chapter_complete', 'until_reached')


# requirement -> system tests that exercise it
SYS_MAP = {
    'REQ-ARCH-001': ['split_screen_world'], 'REQ-ARCH-002': ['commit_idempotent'], 'REQ-ARCH-003': ['data_integrity'],
    'REQ-ARCH-005': [], 'REQ-CHAR-001': [], 'REQ-MOVE-001': ['movement_speeds', 'wall_collision'], 'REQ-CAM-001': ['camera_min_distance'],
    'REQ-SPLIT-001': ['split_screen_world'], 'REQ-INPUT-001': ['device_exclusive'], 'REQ-INPUT-002': ['device_disconnect_pause'],
    'REQ-COOP-001': ['simultaneous_movement'], 'REQ-COOP-002': ['interaction_leases'], 'REQ-COOP-003': ['solo_gate_m02', 'solo_gate_m03', 'solo_gate_m06'],
    'REQ-ENV-007': ['wall_collision'], 'REQ-GUARD-002': ['guard_detection_and_cover'], 'REQ-DLG-002': ['subtitle_wrap'],
    'REQ-CINE-002': ['mutual_skip'], 'REQ-SAVE-001': ['snapshot_roundtrip'], 'REQ-SAVE-002': ['save_rejected_in_cinematic', 'checkpoint_reload'],
    'REQ-SAVE-003': ['save_file'], 'REQ-SAVE-004': ['canon_entry_states'], 'REQ-UI-004': ['settings_roundtrip'], 'REQ-INPUT-003': ['settings_roundtrip'],
}
# criteria that need eyes (graphical) or a human; listed until QA inspects them
GRAPHICAL = {'REQ-CHAR-001', 'REQ-CHAR-002', 'REQ-ANIM-001', 'REQ-ANIM-002', 'REQ-CAM-001', 'REQ-SPLIT-001', 'REQ-ENV-001', 'REQ-ENV-002',
             'REQ-ENV-003', 'REQ-ENV-004', 'REQ-ENV-005', 'REQ-ENV-006', 'REQ-ENV-009', 'REQ-CINE-001', 'REQ-DLG-002', 'REQ-UI-001',
             'REQ-UI-002', 'REQ-UI-003', 'REQ-UI-005', 'REQ-TEST-002', 'REQ-PERF-001', 'REQ-EXPORT-002'}

reg = json.loads(REG.read_text(encoding='utf-8'))
full_events = {k: [e for e in runs.get('full_headless', {}).get('events', [])] for k in ['x']}
for r in reg['requirements']:
    if r['status'] == 'VERIFIED':
        continue
    ev, fails = [], []
    rid = r['id']
    if r['category'] == 'dialogue-line':
        ev = seen('dialogue_shown', 'id', r['dialogue_id'])
        if not ev: fails.append('line never shown in any automated run')
    elif r['category'] == 'camera-shot':
        ev = seen('shot_activated', 'id', r['shot_id'])
        if not ev: fails.append('shot camera never activated')
    elif r['category'] == 'objective':
        ev = seen('objective_completed', 'id', r['objective_id'])
        if not ev: fails.append('objective never completed')
    elif 'checkpoint_id' in r:
        ev = seen('checkpoint', 'checkpoint', r['checkpoint_id'])
        if not ev: fails.append('checkpoint never committed')
        if sys_ok.get('checkpoint_reload') is False: fails.append('system test checkpoint_reload failed')
    elif r['category'] in ('mission', 'scene') or rid.startswith('REQ-MIS-'):
        n = int(rid.split('-')[2][:2])
        ev = seen('mission_complete', 'mission', n)
        if not ev: fails.append('mission never completed')
    if rid in SYS_MAP:
        for t in SYS_MAP[rid]:
            if t in sys_ok:
                ev.append(f'tests/phase02/evidence/system_tests.json#{t}')
                if not sys_ok[t]: fails.append(f'system test {t} failed')
    if rid == 'REQ-DLG-001':
        shown = set()
        for name in runs:
            shown |= {e['id'] for e in events(name, 'dialogue_shown')}
        ev.append(f'{len(shown)}/145 lines shown across automated runs')
        if len(shown) < 145: fails.append(f'{145 - len(shown)} lines never shown')
    if rid == 'REQ-TEST-001':
        ev.append('tests/phase02/evidence/system_tests.json')
        if systests.get('failed', 1) != 0: fails.append('system tests failing')
    if rid == 'REQ-GUARD-001' or rid == 'REQ-GUARD-002':
        if seen('detected_fail', 'kind', 'detected_fail'): ev.append('full_mistakes: detection -> CP04_A reload')
    if rid == 'REQ-EXPORT-001' and (R / 'build/windows/BreakoutNoWayBack.exe').is_file():
        ev.append('build/windows/BreakoutNoWayBack.exe')
    r['evidence'] = sorted(set(ev))
    implemented = all((R / f).exists() for f in r['implementation_files']) and r['implementation_files']
    if r['status'] == 'BLOCKED':
        continue
    if fails and (ev or implemented):
        r['status'] = 'TEST_FAILED' if any('failed' in f or 'never' in f for f in fails) else 'IMPLEMENTED_UNTESTED'
        r['blocking_issues'] = fails
    elif implemented or ev:
        r['status'] = 'IMPLEMENTED_UNTESTED'
        r['blocking_issues'] = []
    else:
        r['status'] = 'NOT_STARTED'
    r['pending_checks'] = (['graphical inspection by independent QA'] if rid in GRAPHICAL else []) + ['independent QA review']

# QA verdicts are the only route to VERIFIED
if VERDICTS.is_file():
    v = json.loads(VERDICTS.read_text(encoding='utf-8'))
    for r in reg['requirements']:
        q = v.get('verdicts', {}).get(r['id'])
        if q:
            r['qa'] = q
            if q['verdict'] == 'VERIFIED' and r['status'] in ('IMPLEMENTED_UNTESTED', 'VERIFIED'):
                r['status'] = 'VERIFIED'
                r['pending_checks'] = []
            elif q['verdict'] in ('TEST_FAILED', 'BLOCKED'):
                r['status'] = q['verdict']
                r['blocking_issues'] = sorted(set(r.get('blocking_issues', []) + [q.get('reason', 'QA')]))
REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
subprocess.run([sys.executable, '-I', str(R / 'tools/phase02_build_registry.py')], check=True, stdout=subprocess.DEVNULL)
from collections import Counter
print(dict(Counter(r['status'] for r in json.loads(REG.read_text(encoding='utf-8'))['requirements'])))

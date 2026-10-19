"""Generate docs/qa/ASSET_COVERAGE_MATRIX.md from assets.json + integration_summary.json + mission specs.
python -I tools/phase15_coverage.py   (run after tools/phase15_finalize.py)"""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
A = {a['asset_id']: a for a in json.loads((R / 'asset_library/manifests/assets.json').read_text(encoding='utf-8'))}
S = json.loads((R / 'asset_library/manifests/phase15/integration_summary.json').read_text())['bundles']
NAMES = {1: 'New Blood', 2: 'Trouble in the Yard', 3: 'The Workshop', 4: 'Lights Out', 5: 'Behind the Walls', 6: 'The Betrayal'}
ENVS = {1: ['ENV_INTAKE', 'ENV_CELLBLOCK'], 2: ['ENV_YARD'], 3: ['ENV_WORKSHOP'], 4: ['ENV_CELLBLOCK', 'ENV_MAINTENANCE'], 5: ['ENV_MAINTENANCE'], 6: ['ENV_MAINTENANCE', 'ENV_CELLBLOCK']}
OBJECTIVE_PROPS = {1: ['PROP_PHOTO', 'PROP_VANTAGE_BADGE'], 3: ['PROP_DIAGRAM', 'PROP_SHIM'], 4: ['PROP_SHIM'], 5: ['PROP_RELAY', 'PROP_LEDGER'], 6: ['PROP_SHIM']}
# Interactive objects named in each mission's playable sequence -> concrete asset IDs ([] = nothing suitable exists)
ELEMENTS = {
 1: [('Transport bus arrival', ['DISC15_QUATERNIUS_BUS'], 'IMPORTANT'), ('Intake counter + property tray', ['P15_INTAKE_COUNTER'], 'CRITICAL'),
     ('Holding bay bars', ['P15_CELL_BARS_3M'], 'CRITICAL'), ('Body scanner', [], 'IMPORTANT'), ('Property locker 42', ['P15_LOCKER'], 'CRITICAL'),
     ('Transfer clipboard badge', ['P15_VANTAGE_BADGE'], 'CRITICAL'), ('Cells 13/14 (door, bed, mattress, sink, toilet)', ['P15_CELL_DOOR_1M', 'P15_CELL_BED', 'P15_MATTRESS', 'P15_SINK', 'P15_TOILET'], 'CRITICAL'),
     ('CCTV / lighting dressing', ['P15_CCTV_CAMERA', 'P15_FLUORESCENT_FIXTURE', 'DISC15_PH_SECURITY_CAMERA_01'], 'OPTIONAL')],
 2: [('Yard fence + west lane', ['P15_FENCE_2X5', 'P15_FENCE_END_POST_5M', 'PH15_MODULAR_CHAINLINK_FENCE'], 'CRITICAL'), ('Exercise bench (Silas)', ['P15_YARD_BENCH'], 'CRITICAL'),
     ('Loose basketball', ['P15_BASKETBALL', 'DISC15_OGA_OUREN_BASKETBALL'], 'CRITICAL'), ('Tap alcove', ['P15_WATER_TAP'], 'CRITICAL'), ('Yard gate', ['P15_YARD_GATE_2M'], 'CRITICAL'),
     ('Basketball hoop / court', ['DISC15_OGA_OUREN_BASKETBALL_HOOP'], 'IMPORTANT'), ('Watchtower', ['DISC15_OGA_WATCHTOWER_WOOD'], 'IMPORTANT'), ('Ball rack / barriers', ['DISC15_OGA_OUREN_BALL_RACK', 'PH15_CONCRETE_ROAD_BARRIER_02'], 'OPTIONAL')],
 3: [('Industrial washer (stopped, inspect)', ['P15_LAUNDRY_WASHER'], 'CRITICAL'), ('Laundry press + isolation lever', ['P15_LAUNDRY_PRESS'], 'CRITICAL'),
     ('Power isolator / panel', ['P15_ELECTRICAL_PANEL', 'DISC15_PH_POWER_BOX_01'], 'CRITICAL'), ('Diagram halves', ['P15_MAINTENANCE_DIAGRAM'], 'CRITICAL'), ('Service screen / hatch', ['P15_SERVICE_HATCH_11'], 'CRITICAL'),
     ('Spring shim', ['P15_SPRING_SHIM'], 'CRITICAL'), ('Workbench, shelves, tools', ['P15_STEEL_TABLE', 'PH15_STEEL_FRAME_SHELVES_01', 'PH15_BENCH_VICE_01', 'PH15_METAL_TOOL_CHEST'], 'IMPORTANT'), ('Linen trolley / bins', ['P15_LINEN_TROLLEY', 'P15_SCRAP_BIN'], 'OPTIONAL')],
 4: [('Cell 14 rear service panel + fastener', ['P15_SERVICE_HATCH_11', 'P15_MECHANICAL_LATCH'], 'CRITICAL'), ('Service chase modules', ['P15_PIPE_STRAIGHT_2M', 'PH15_MODULAR_AIRDUCT_RECTANGULAR_01', 'DISC15_PH_MODULAR_ELECTRIC_CABLES'], 'CRITICAL'),
     ('Concrete pier shelters', ['P15_CORNER_PIER'], 'CRITICAL'), ('Manual gate', ['P15_YARD_GATE_2M', 'P15_SECURITY_DOOR_12'], 'CRITICAL'), ('Shim', ['P15_SPRING_SHIM'], 'CRITICAL'), ('Patrol clock', ['PH15_WALL_CLOCK'], 'OPTIONAL')],
 5: [('West catwalk route', ['P15_CATWALK_2M', 'P15_RAILING_2M', 'P15_STAIRS_17_RISERS_3M', 'P15_LADDER_28'], 'CRITICAL'), ('Selector console A/B/C', ['P15_ELECTRICAL_PANEL'], 'CRITICAL'),
     ('Hold brake station', ['P15_BRAKE_STATION'], 'CRITICAL'), ('Wired handsets', ['P15_WIRED_HANDSET'], 'CRITICAL'), ('Lifting grille + latch', ['P15_SECURITY_GRILLE_4M', 'P15_MECHANICAL_LATCH'], 'CRITICAL'),
     ('Pump (reunion, ledger)', ['P15_PUMP_UNIT'], 'CRITICAL'), ('Pump service ledger', ['P15_TRANSFER_LEDGER'], 'CRITICAL'), ('Final door', ['P15_DOUBLE_SPILLWAY_DOOR'], 'CRITICAL')],
 6: [('Lock + paired pull handles', ['P15_DUAL_DOOR_HANDLE', 'P15_DOUBLE_SPILLWAY_DOOR'], 'CRITICAL'), ('Rear security grille closes', ['P15_SECURITY_GRILLE_4M'], 'CRITICAL'),
     ('Alarm beacon', ['VFX15_ALARM_MATERIAL'], 'IMPORTANT'), ('Capture restraint', [], 'IMPORTANT'), ('Solitary cell + pipe', ['P15_CELL_DOOR_1M', 'P15_PIPE_STRAIGHT_2M', 'P15_CELL_BED'], 'CRITICAL')]}
DEPS = {}
for i in range(1, 7):
    t = (R / f'docs/missions/CH01_MISSION_0{i}.md').read_text(encoding='utf-8')
    line = next(l for l in t.splitlines() if l.startswith('CHAR_ADRIAN, CHAR_NOAH'))
    DEPS[i] = [x.strip() for x in line.split('These are requirements')[0].rstrip('. ').split(',')]

def st(aid):
    a = A.get(aid)
    if not a: return 'MISSING'
    if a.get('asset_role') == 'requirement_bundle': return a['functional_status']
    if not a.get('usable', a.get('validation_status') == 'PARTIALLY_VERIFIED'): return a.get('validation_status', 'UNKNOWN')
    if a.get('validation_status') == 'FUNCTIONAL_PROXY': return 'FUNCTIONAL_PROXY'
    return 'AVAILABLE'
def pr(b, mission):
    if b.startswith('CHAR_') or b == 'ANIM_HUMANOID' or b.startswith('ENV_') or b in OBJECTIVE_PROPS.get(mission, []): return 'CRITICAL'
    if b.startswith('MAT_') or b.startswith('AUDIO') or b.startswith('UI_') or b.startswith('VFX') or b.startswith('PROP_'): return 'IMPORTANT'
    return 'OPTIONAL'
out = ['# Chapter 1 asset coverage matrix — Phase 01.5', '',
       'Generated by `tools/phase15_coverage.py` from [assets.json](../../asset_library/manifests/assets.json) and `asset_library/manifests/phase15/integration_summary.json`. Every ID resolves in the manifest unless marked MISSING. '
       '**Functional** = a usable, Godot-loading asset exists (realistic, proxy or construction-grade). **Production** = meets the intended realistic/cinematic standard; tracked separately and never closed by a functional substitute. '
       'CRITICAL = needed to play/stage the mission; IMPORTANT = intended presentation; OPTIONAL = dressing that never blocks implementation.', '',
       'Status words: AVAILABLE (usable asset, PARTIALLY_VERIFIED: loads and renders; collision/nav/listening not tested), FUNCTIONAL (realistic candidate verified for functional use), FUNCTIONAL_PROXY (stand-in only), PARTIAL (some subcomponents missing), MISSING.', '']
summary_rows = []
for i in range(1, 7):
    out += [f'## CH01_M0{i} — {NAMES[i]}', '', '### Requirement bundles', '', '| Bundle | Priority | Functional | Production | Usable children | Remaining gap |', '|---|---|---|---|---:|---|']
    bundles = list(dict.fromkeys(DEPS[i] + ENVS[i]))
    crit_ok = True; subst = False; partial = False
    for b in bundles:
        p = pr(b, i)
        if b in S:
            e = S[b]; f = e['functional_status']; prod = e['production_status']; n = e['verified_usable']; gap = e['missing']
        else:
            a = A.get(b, {}); f = 'AVAILABLE' if a else 'MISSING'; prod = 'PARTIAL' if a else 'BLOCKED'; n = '—'; gap = 'Phase 01 acquired record; physical UV scale / calibration not reviewed.' if a else 'Not in manifest.'
        if p == 'CRITICAL' and f in ('BLOCKED', 'MISSING'): crit_ok = False
        if p == 'CRITICAL' and f == 'FUNCTIONAL_PROXY': subst = True
        if p == 'CRITICAL' and f == 'PARTIAL': partial = True  # QAF-24: an incomplete critical bundle caps the mission at PARTIAL
        out.append(f'| `{b}` | {p} | {f} | {prod} | {n} | {gap} |')
    out += ['', '### Interactive objects named in the playable sequence', '', '| Element | Priority | Asset IDs → status |', '|---|---|---|']
    for name, ids, p in ELEMENTS[i]:
        sts = [(x, st(x)) for x in ids]
        ok = any(s in ('AVAILABLE', 'FUNCTIONAL', 'FUNCTIONAL_PROXY') for _, s in sts)
        if p == 'CRITICAL' and not ok: crit_ok = False
        cell = ', '.join(f'`{x}` {s}' for x, s in sts) if sts else '**MISSING — no asset**'
        out.append(f'| {name} | {p} | {cell} |')
    func = 'BLOCKED' if not crit_ok else 'PARTIAL' if partial else 'FUNCTIONAL (substitutes need approval)' if subst else 'FUNCTIONAL'
    out += ['', f'**Functional asset readiness: {func}.** **Production asset readiness: NOT READY** — see production column and [blockers](BLOCKERS.md).', '']
    summary_rows.append(f'| CH01_M0{i} {NAMES[i]} | {func} | NOT READY |')
out[9:9] = ['## Summary', '', '| Mission | Functional (critical assets) | Production quality |', '|---|---|---|'] + summary_rows + ['', 'A functional substitute (construction-grade module, stylised blockout or recoloured realistic avatar) is not an approved final asset until art direction signs off; until then the functional verdict is conditional, as stated per mission.', '']
(R / 'docs/qa/ASSET_COVERAGE_MATRIX.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(summary_rows))
missing = sorted({x for v in ELEMENTS.values() for _, ids, _ in v for x in ids if x not in A}); print('unresolved IDs:', missing)

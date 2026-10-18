"""Phase 01.5 final integration: merge fragments into assets.json with evidence-based statuses and
write per-bundle status for the 22 original requirement bundles. Idempotent (rebuilds from the Phase 01
baseline + fragments every run). python -I tools/phase15_finalize.py
Inputs (all must already exist): fragment manifests, phase15/godot_validation.json (latest Godot run),
phase15_characters_previews/godot/godot_character_report.json, phase15/audio_materials_audit.json,
phase15/architecture_validation.json. Optional: phase15/architecture_repairs.json, phase15/discovery_candidates.json.
"""
import json, hashlib, collections
from pathlib import Path
R = Path(__file__).resolve().parents[1]; M = R / 'asset_library/manifests'; D = M / 'phase15'
rd = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p, obj):
    p = Path(p); tmp = p.with_suffix(p.suffix + '.tmp'); tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8'); tmp.replace(p)

base_path = D / 'phase01_assets_baseline.json'
if not base_path.exists():
    cur = rd(M / 'assets.json')
    assert len(cur) == 28 and not any('child_asset_ids' in a for a in cur), 'assets.json is not the Phase 01 baseline'
    base_path.write_bytes((M / 'assets.json').read_bytes())
old = rd(base_path)
FRAGS = ['phase15_architecture.json', 'phase15_bulk_assets.json', 'phase15_bulk_oga_assets.json', 'phase15_props_records.json',
         'phase15_ui_records.json', 'phase15_original_audio.json', 'phase15_characters_records.json', 'phase15_critical_records.json',
         'phase15_discovery_records.json']
new = [a for f in FRAGS if (M / f).exists() for a in rd(M / f)]
ids = [a['asset_id'] for a in old + new]; dup = [k for k, v in collections.Counter(ids).items() if v > 1]
assert not dup, dup

godot = {x['path'][6:]: x for x in rd(D / 'godot_validation.json')}
chars = rd(M / 'phase15_characters_previews/godot/godot_character_report.json')
audio = rd(D / 'audio_materials_audit.json'); rejected_audio = {x['runtime_file']: x['reasons'] for x in audio['rejected_audio']}
arch = {x['asset_id']: x for x in rd(D / 'architecture_validation.json')['assets']}
repairs = rd(D / 'architecture_repairs.json') if (D / 'architecture_repairs.json').exists() else None

errors = []
def paths(a):
    p = a.get('runtime_file') or []; return [p] if isinstance(p, str) else p
for a in new:
    # normalise: Godot-generated .import sidecars are not runtime payloads; per-path checksum dicts are verified per path
    if isinstance(a.get('runtime_file'), list):
        a['runtime_file'] = [p for p in a['runtime_file'] if not p.endswith('.import')]
        if len(a['runtime_file']) == 1: a['runtime_file'] = a['runtime_file'][0]
    rc = a.get('runtime_checksum')
    if isinstance(rc, dict):
        rc = {k: v for k, v in rc.items() if not k.endswith('.import')}
        for k, v in rc.items():
            if not (R / k).is_file() or hashlib.sha256((R / k).read_bytes()).hexdigest() != v: errors.append(a['asset_id'] + ' checksum mismatch ' + k)
        a['runtime_checksum'] = rc[a['runtime_file']] if isinstance(a['runtime_file'], str) and a['runtime_file'] in rc else rc
    ps = paths(a)
    for p in ps:
        if not (R / p).is_file(): errors.append(a['asset_id'] + ' missing ' + p)
    a['license_file'] = a.get('license_file') or a.get('license_record')
    if not a['license_file'] or not (R / a['license_file']).is_file(): errors.append(a['asset_id'] + ' missing license')
    if len(ps) == 1 and (R / ps[0]).is_file():
        actual = hashlib.sha256((R / ps[0]).read_bytes()).hexdigest()
        if isinstance(a.get('runtime_checksum'), str) and a['runtime_checksum'] != actual: errors.append(a['asset_id'] + ' checksum mismatch')
    ev = [godot[p] for p in ps if p in godot]
    a['import_status'] = 'FAILED' if any(x['load'] != 'VERIFIED' for x in ev) else 'VERIFIED' if ev and len(ev) == len([p for p in ps if p.split('.')[-1] in ('glb', 'gltf', 'ogg', 'wav', 'png', 'tres', 'ttf', 'svg')]) else 'VERIFIED' if ev else 'NOT_TESTED'
    if ev and ev[0].get('geometry'): a['engine_geometry'] = ev[0]['geometry']; a['engine_bounds'] = ev[0].get('bounds')
    st = a.get('validation_status')
    if a['category'] == 'audio' and any(p in rejected_audio for p in ps):
        st = 'REJECTED'; a['rejection_reasons'] = [r for p in ps for r in rejected_audio.get(p, [])]
    elif a['asset_id'] in arch:
        st = arch[a['asset_id']]['status']; a['architecture_flags'] = arch[a['asset_id']].get('flags', [])[:12]
    elif a['asset_id'].startswith('P15_PROXY_'):
        st = 'SUPERSEDED'; a['superseded_by'] = a['asset_id'].replace('P15_PROXY_', 'P15_UBC_')
    if a['import_status'] == 'FAILED' and st not in ('FAILED', 'REJECTED'): st = 'FAILED'
    if a['import_status'] == 'NOT_TESTED' and st not in ('FAILED', 'REJECTED', 'SUPERSEDED'): st = 'BLOCKED'
    a['validation_status'] = st
    a['usable'] = st in ('VERIFIED', 'PARTIALLY_VERIFIED', 'FUNCTIONAL_PROXY') and a['import_status'] == 'VERIFIED'
    if a['category'] == 'characters' and (a['asset_id'].startswith('P15_UBC_') or a['asset_id'].startswith('P15_RB_')):
        rp = Path(paths(a)[0]); c = chars.get(rp.parent.name + '/' + rp.stem, {})
        a['godot_character_check'] = {k: c.get(k) for k in ('load', 'bone_count', 'mesh_instances', 'null_materials', 'unskinned_meshes', 'triangles')}
        a['godot_character_check']['clips_imported'] = len(c.get('animations', [])); a['godot_character_check']['looping_clips'] = len(c.get('looping', []))
        a['godot_character_check']['pose_renders'] = len([s for s in c.get('shots', []) if s.get('png')])
        if c.get('load') != 'VERIFIED': a['validation_status'] = 'BLOCKED'; a['usable'] = False
    a['validation_scope'] = 'Statuses are scoped: import = Godot 4.7.2 load; geometry/visual/audio checks per phase15 QA reports. Listening, collision, navigation and production art quality are separate and mostly NOT TESTED.'
if errors: raise SystemExit('\n'.join(errors))
lk = {a['asset_id']: a for a in new}
def ids_where(f): return [k for k, a in lk.items() if f(a)]

missions = {t['asset_id']: t['missions'] for t in rd(D / 'missing_bundle_tasks.json')}
priority = {t['asset_id']: t['priority'] for t in rd(D / 'missing_bundle_tasks.json')}
B = {
 'CHAR_ADRIAN': (['P15_RB_ADRIAN', 'P15_UBC_ADRIAN'], 'FUNCTIONAL', 'PARTIAL', 'Facial blendshapes not exported; art-direction likeness approval; overshirt is a recoloured sweater (no layered garment); grey temple/eyebrow cut not authored; calibrated roughness from specular; close-up lighting review.'),
 'CHAR_NOAH': (['P15_RB_NOAH', 'P15_UBC_NOAH'], 'FUNCTIONAL', 'PARTIAL', 'Facial blendshapes not exported; likeness approval (skin darker than brief, hair not wavy); wrist burn not authored; recoloured jacket stands in for undershirt; photo-in-shirt contact.'),
 'CHAR_RUSK': (['P15_RB_RUSK', 'P15_UBC_RUSK'], 'FUNCTIONAL', 'PARTIAL', 'Average (not heavy) build; radio/keys/wedding band props; shares the only realistic guard identity with CHAR_GUARD.'),
 'CHAR_MARA': (['P15_RB_MARA', 'P15_UBC_MARA'], 'FUNCTIONAL', 'PARTIAL', 'Likeness mismatch: avatar is younger with dark hair (brief: 46, silver-streaked); cardigan and inspector badge missing.'),
 'CHAR_SILAS': (['P15_RB_SILAS', 'P15_UBC_SILAS'], 'FUNCTIONAL', 'PARTIAL', 'Uniform patches and chipped incisor not authored; facial performance.'),
 'CHAR_GUARD': (['P15_RB_RUSK', 'P15_UBC_GUARD'], 'FUNCTIONAL', 'PARTIAL', 'Only one realistic guard identity (shared with Rusk); radio/restraints props; more variants needed for crowds.'),
 'CHAR_INMATE': (['P15_RB_INMATE', 'P15_RB_SILAS', 'P15_UBC_INMATE'], 'FUNCTIONAL', 'PARTIAL', 'Two realistic inmate identities; crowd variation and seated/working variants beyond shared clips.'),
 'ANIM_HUMANOID': (ids_where(lambda a: a['asset_id'].startswith('P15_ANIM_')) + ['P15_RB_ADRIAN', 'P15_RB_NOAH', 'P15_UBC_ADRIAN', 'P15_UBC_NOAH'], 'PARTIAL', 'BLOCKED',
                   '37 clips render correctly on realistic Rocketbox and UBC rigs (Blender + Godot); baseline locomotion/crouch/jump/interact/push/climb/pick-up/repair verified. Missing: turn-in-place, pull, door-specific, paired assisted climb/help-up, synchronized two-body contacts, restrained walk, facial/dialogue performance, cinematic takes; foot sliding/root motion untested.'),
 'PROP_PHOTO': (['P15_PHOTO_SLEEVE_EMPTY'] + ids_where(lambda a: a['asset_id'] == 'TEX15_ELENA_PHOTO'), 'FUNCTIONAL_PROXY', 'PARTIAL', 'Hand contact and close-up art direction.'),
 'PROP_VANTAGE_BADGE': (['P15_VANTAGE_BADGE'], 'FUNCTIONAL_PROXY', 'PARTIAL', 'Close-up legibility/art direction.'),
 'PROP_DIAGRAM': (['P15_MAINTENANCE_DIAGRAM'], 'FUNCTIONAL_PROXY', 'PARTIAL', 'Half-screen readability at authored camera.'),
 'PROP_SHIM': (['P15_SPRING_SHIM'], 'FUNCTIONAL_PROXY', 'PARTIAL', 'Grip/contact and cinematic silhouette.'),
 'PROP_RELAY': (['P15_ELECTRICAL_PANEL', 'P15_BRAKE_STATION', 'P15_MECHANICAL_LATCH', 'P15_WIRED_HANDSET', 'P15_SECURITY_GRILLE_4M'], 'FUNCTIONAL_PROXY', 'PARTIAL',
                'Selector lamp states, brake wheel pivot and interlock motion; grille drive animation untested.'),
 'PROP_LEDGER': (['P15_TRANSFER_LEDGER'], 'PARTIAL', 'BLOCKED', 'Readable close-up evidence page and later full VANTAGE ledger.'),
 'ENV_INTAKE': (['P15_WALL_4M', 'P15_FLOOR_4M', 'P15_CEILING_4M', 'P15_BARRED_WINDOW', 'P15_SECURITY_DOOR_12', 'P15_INTAKE_COUNTER', 'P15_STEEL_CHAIR', 'P15_CCTV_CAMERA', 'PH15_SECURITY_LIGHT'],
                'PARTIAL', 'BLOCKED', 'Bus is a stylised exterior blockout (no interior); body scanner missing; realistic prison gate; assembled route and collision/nav.'),
 'ENV_CELLBLOCK': (['P15_WALL_4M', 'P15_FLOOR_4M', 'P15_CELL_BARS_3M', 'P15_CELL_DOOR_1M', 'P15_CELL_BED', 'P15_MATTRESS', 'P15_SINK', 'P15_TOILET', 'P15_RAILING_2M', 'P15_CATWALK_2M', 'P15_SERVICE_HATCH_11', 'PH15_WALL_CLOCK']
                   + ids_where(lambda a: 'STAIR' in a['asset_id']), 'PARTIAL', 'BLOCKED', 'Two-level assembled gallery, solitary annex, clinic envelope, hinge-pivot door motion, collision/nav.'),
 'ENV_YARD': (['P15_FENCE_2X5', 'P15_YARD_GATE_2M', 'P15_YARD_BENCH', 'P15_WATER_TAP', 'P15_BASKETBALL', 'PH15_MODULAR_CHAINLINK_FENCE', 'PH15_CONCRETE_ROAD_BARRIER_02'],
              'PARTIAL', 'BLOCKED', 'Watchtowers are stylised/medieval (blockout only); court markings and tray return missing; searchlight asset is a hand lantern; CC-BY hoop needs credit.'),
 'ENV_WORKSHOP': (['P15_LAUNDRY_WASHER', 'P15_LAUNDRY_PRESS', 'P15_STEEL_TABLE', 'P15_LOCKER', 'P15_LINEN_TROLLEY', 'P15_INSPECTION_LAMP', 'P15_SCRAP_BIN', 'P15_MAINTENANCE_DIAGRAM', 'PH15_BENCH_VICE_01', 'PH15_METAL_TOOL_CHEST', 'PH15_STEEL_FRAME_SHELVES_01'],
                  'PARTIAL', 'PARTIAL', 'Linen stacks/detail, ducts placement, assembled room and collision/nav; machines are simplified originals.'),
 'ENV_MAINTENANCE': (['P15_CATWALK_2M', 'P15_LADDER_28', 'P15_RAILING_2M', 'P15_PIPE_STRAIGHT_2M', 'P15_SERVICE_PANEL', 'P15_DOUBLE_SPILLWAY_DOOR', 'P15_PUMP_UNIT', 'P15_SECURITY_GRILLE_4M', 'PH15_MODULAR_AIRDUCT_RECTANGULAR_01', 'PH15_MODULAR_AIRDUCT_CIRCULAR_01', 'PH15_MODULAR_FIRE_ESCAPE'],
                     'PARTIAL', 'BLOCKED', 'Crawlspace/service trench modules, cable trays, capture bay assembly, collision/nav; grille drive motion untested.'),
 'AUDIO_PRISON': (ids_where(lambda a: a['category'] == 'audio' and a['usable']), 'PARTIAL', 'BLOCKED', 'Original VO, PA speech, crowd walla (only shouting crowd), diesel bus engine, radio speech and score missing; nothing has been listened to; mix review outstanding.'),
 'UI_SUBTITLES': (ids_where(lambda a: a['category'] == 'ui'), 'PARTIAL', 'PARTIAL', 'Half-screen/localized layout, accessibility and prompt composition untested.'),
 'VFX_ALARM': (['VFX15_ALARM_MATERIAL', 'VFX15_DUST_PROCESS'], 'PARTIAL', 'BLOCKED', 'Beacon light rig and particle emitter appearance in scene untested.')}
assert len(B) == 22 and set(B) == set(missions), set(missions) ^ set(B)
bundles = {}
for a in old:
    a['phase01_validation_status'] = a.get('phase01_validation_status', a['validation_status'])
    if a['asset_id'] not in B:
        a['validation_status'] = 'PARTIALLY_VERIFIED'; a['asset_role'] = 'acquired_phase01'; continue
    aid = a['asset_id']; kids, func, prod, missing = B[aid]
    kids = [k for k in dict.fromkeys(kids + ids_where(lambda x: x.get('requirement_bundle') == aid)) if k in lk]
    usable = [k for k in kids if lk[k]['usable']]
    entry = {'priority': priority[aid], 'missions': missions[aid], 'requirement': a.get('asset_name') or a.get('notes'),
             'available': len(kids), 'verified_usable': len(usable), 'unusable_children': [k for k in kids if k not in usable],
             'godot_import': 'VERIFIED' if kids and all(lk[k]['import_status'] == 'VERIFIED' for k in kids) else 'PARTIAL' if usable else 'BLOCKED',
             'license': 'VERIFIED' if kids and all((R / lk[k]['license_file']).is_file() for k in kids) else 'MISSING',
             'functional_status': func if usable else 'BLOCKED', 'production_status': prod, 'missing': missing}
    bundles[aid] = entry
    a.update({'asset_role': 'requirement_bundle', 'child_asset_ids': kids, 'remaining_requirements': missing, 'runtime_file': None,
              'functional_status': entry['functional_status'], 'production_status': prod,
              'validation_status': entry['functional_status'], 'download_status': 'PARTIALLY_ACQUIRED' if kids else 'MISSING',
              'import_status': entry['godot_import'], 'priority': priority[aid],
              'notes': 'Aggregate requirement, not a payload. functional_status != production readiness; FUNCTIONAL_PROXY never closes a realistic-quality requirement.'})
records = old + new
write(M / 'assets.json', records)
cnt = collections.Counter
dl = [a for a in new if a.get('download_status') not in ('ORIGINAL_CREATED', 'CREATED_FROM_LICENSED_SOURCE') and not a['asset_id'].startswith('P15_') and a['category'] != 'vfx']
summary = {
 'records_total': len(records), 'phase01_records': len(old), 'phase15_records': len(new),
 'phase15_by_category': dict(cnt(a['category'] for a in new)), 'phase15_by_status': dict(cnt(a['validation_status'] for a in new)),
 'phase15_by_download_status': dict(cnt(a.get('download_status') for a in new)),
 'usable': sum(a['usable'] for a in new), 'rejected_audio': len(rejected_audio), 'near_duplicate_groups_audio': len(audio['duplicate_groups']),
 'godot_jobs': len(godot), 'godot_load_verified': sum(x['load'] == 'VERIFIED' for x in godot.values()),
 'bundles': bundles, 'bundle_functional': dict(cnt(b['functional_status'] for b in bundles.values())),
 'bundle_production': dict(cnt(b['production_status'] for b in bundles.values())),
 'architecture_repairs_present': repairs is not None}
write(D / 'integration_summary.json', summary)
print(json.dumps({k: v for k, v in summary.items() if k != 'bundles'}, indent=1))

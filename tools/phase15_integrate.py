"""Integrate acquisition fragments without changing story or prior runtime assets."""
from pathlib import Path
import json,hashlib,collections
R=Path(__file__).resolve().parents[1];M=R/'asset_library/manifests';D=M/'phase15'
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def write(p,s):
    f=R/p;f.parent.mkdir(parents=True,exist_ok=True);tmp=f.with_suffix(f.suffix+'.phase15_tmp');tmp.write_text(s,encoding='utf-8');tmp.replace(f)
baseline=D/'phase01_assets_baseline.json'
if not baseline.exists():baseline.write_bytes((M/'assets.json').read_bytes())
old=json.loads(baseline.read_text(encoding='utf-8-sig'))
sources=['phase15_architecture.json','phase15_bulk_assets.json','phase15_bulk_oga_assets.json','phase15_props_records.json','phase15_ui_records.json','phase15_original_audio.json','phase15_characters_records.json']
new=[]
for source in sources:
    if (M/source).exists():new.extend(read('asset_library/manifests/'+source))
jobs=read('asset_library/manifests/phase15/validation_jobs.json')
evidence=read('asset_library/manifests/phase15/godot_validation.json')
by_path={x['path'][6:]:x for x in evidence}
errors=[]
for a in new:
    paths=a.get('runtime_file') or [];paths=[paths] if isinstance(paths,str) else paths
    for path in paths:
        if not (R/path).is_file():errors.append(a['asset_id']+' missing '+path)
    a['license_file']=a.get('license_file',a.get('license_record'))
    if not a.get('license_file') or not (R/a['license_file']).is_file():errors.append(a['asset_id']+' missing license record')
    actual=[by_path[p] for p in paths if p in by_path]
    a['import_status']='VERIFIED' if actual and all(x['load']=='VERIFIED' for x in actual) else 'BLOCKED'
    if a.get('validation_status') not in ['FAILED','BLOCKED']:a['validation_status']='PARTIALLY_VERIFIED'
    if a['import_status']=='BLOCKED' and a['validation_status']!='FAILED':a['validation_status']='BLOCKED'
    a['validation_evidence']={'godot_resources':[x['path'] for x in actual],'scope':'File/resource checks only. Visual, skinning, contact, source audio clipping, collision/nav and production quality have separate limits.'}
    if a['category']=='audio':a['notes']+=' Godot resource load '+a['import_status']+'. Listening/mix remains unverified.'
    if actual and actual[0].get('geometry'):
        a['engine_geometry']=actual[0]['geometry'];a['engine_bounds']=actual[0].get('bounds')
    if len(paths)==1 and (R/paths[0]).is_file():a['runtime_checksum']=hashlib.sha256((R/paths[0]).read_bytes()).hexdigest()
ids=[a['asset_id'] for a in old+new]
if len(ids)!=len(set(ids)):errors.append('Duplicate IDs')
for path,expected in read('asset_library/manifests/phase15/baseline_hashes.json').items():
    if not (R/path).is_file() or hashlib.sha256((R/path).read_bytes()).hexdigest()!=expected:errors.append('Protected baseline changed '+path)
if errors:raise RuntimeError('\n'.join(errors))
lookup={a['asset_id']:a for a in new}
bundle={
'CHAR_ADRIAN':['P15_CHAR_ADRIAN'],'CHAR_NOAH':['P15_CHAR_NOAH'],'CHAR_RUSK':['P15_CHAR_GUARD'],'CHAR_MARA':[],'CHAR_SILAS':[],'CHAR_GUARD':['P15_CHAR_GUARD'],'CHAR_INMATE':['P15_CHAR_INMATE'],
'PROP_PHOTO':['P15_PHOTO_SLEEVE_EMPTY','TEX15_ELENA_PHOTO'],'PROP_VANTAGE_BADGE':['P15_VANTAGE_BADGE'],'PROP_DIAGRAM':['P15_MAINTENANCE_DIAGRAM'],'PROP_SHIM':['P15_SPRING_SHIM'],
'PROP_RELAY':['P15_ELECTRICAL_PANEL','P15_BRAKE_STATION','P15_MECHANICAL_LATCH','P15_WIRED_HANDSET'],
'PROP_LEDGER':['P15_TRANSFER_LEDGER'],
'ENV_INTAKE':['P15_WALL_4M','P15_FLOOR_4M','P15_CEILING_4M','P15_BARRED_WINDOW','P15_SECURITY_DOOR_12','P15_INTAKE_COUNTER','P15_STEEL_CHAIR','P15_CCTV_CAMERA','PH15_SECURITY_LIGHT'],
'ENV_CELLBLOCK':['P15_WALL_4M','P15_FLOOR_4M','P15_CELL_BARS_3M','P15_CELL_DOOR_1M','P15_CELL_BED','P15_MATTRESS','P15_SINK','P15_TOILET','P15_RAILING_2M','P15_STAIRS_10_RISERS','P15_SERVICE_HATCH_11','PH15_WALL_CLOCK'],
'ENV_YARD':['P15_FENCE_2X5','P15_YARD_GATE_2M','P15_YARD_BENCH','P15_WATER_TAP','PH15_MODULAR_CHAINLINK_FENCE','PH15_CONCRETE_ROAD_BARRIER_02','PH15_PORTABLE_SEARCHLIGHT'],
'ENV_WORKSHOP':['P15_LAUNDRY_WASHER','P15_LAUNDRY_PRESS','P15_STEEL_TABLE','P15_LOCKER','P15_LINEN_TROLLEY','P15_INSPECTION_LAMP','P15_SCRAP_BIN','PH15_BENCH_VICE_01','PH15_METAL_TOOL_CHEST','PH15_STEEL_FRAME_SHELVES_01'],
'ENV_MAINTENANCE':['P15_CATWALK_2M','P15_LADDER_28','P15_RAILING_2M','P15_PIPE_STRAIGHT_2M','P15_SERVICE_PANEL','P15_DOUBLE_SPILLWAY_DOOR','PH15_MODULAR_AIRDUCT_RECTANGULAR_01','PH15_MODULAR_AIRDUCT_CIRCULAR_01','PH15_MODULAR_FIRE_ESCAPE'],
'ANIM_HUMANOID':[x for x in lookup if x.startswith('P15_ANIM_')],
'AUDIO_PRISON':[x for x in lookup if x.startswith('AUDIO15_')]+[x for x,a in lookup.items() if a['category']=='audio' and any(term in a['asset_name'].lower() for term in ['door','latch','machine','thunder','storm','rain'])],
'UI_SUBTITLES':[x for x,a in lookup.items() if a['category']=='ui'],
'VFX_ALARM':['VFX15_ALARM_MATERIAL','VFX15_DUST_PROCESS']}
gaps={
'CHAR_ADRIAN':'Experimental body/clothes and retarget fail visual acceptance; no production facial/PBR skin or approved movement.',
'CHAR_NOAH':'Experimental body/clothes and retarget fail visual acceptance; no production facial/PBR skin or approved movement.',
'CHAR_RUSK':'Only experimental generic guard substitute, not accepted Rusk likeness/uniform/rig.',
'CHAR_MARA':'No matching rigged physician model/outfit acquired.',
'CHAR_SILAS':'No matching rigged Silas model/outfit acquired.',
'CHAR_GUARD':'Experimental guard body/clothes and retarget fail visual acceptance.',
'CHAR_INMATE':'Experimental inmate body/clothes and retarget fail visual acceptance.',
'ANIM_HUMANOID':'Licensed raw UAL source exists, but MPFB retarget fails deformation. No accepted baseline on both protagonists; custom contacts, partner actions and facial performances missing.',
'ENV_INTAKE':'No transport bus, scanner, final intake assembly, collision/nav or dimensional route test.',
'ENV_CELLBLOCK':'No assembled gallery/chase/solitary set, fitted opening/snap test, final institutional art or collision/nav.',
'ENV_YARD':'No court/ball/watchtower and assembled route; original fence is simplified. Collision/nav pending.',
'ENV_WORKSHOP':'No final linen detail, complete assembled workshop or collision/nav; machine shapes are authored substitutes.',
'ENV_MAINTENANCE':'No full pump machinery or 4m lifting grille/drive, complete chase assembly, collision/nav or safe moving geometry proof.',
'PROP_PHOTO':'Paper sleeve and generated portrait exist; hand contact, close-up art direction/scale pending.',
'PROP_VANTAGE_BADGE':'Original seal exists; close-up legibility/art direction pending.',
'PROP_DIAGRAM':'Authored route/selector diagram exists; half-screen readability at authored camera and placement pending.',
'PROP_SHIM':'Rounded static mesh exists; grip/contact and cinematic silhouette test pending.',
'PROP_RELAY':'Separate selector/brake/handset/latch exist; door grille drive, pivots/swept clearance and contact animation unverified.',
'PROP_LEDGER':'Folder/label exists; actual readable scene evidence page and close-up art direction missing.',
'AUDIO_PRISON':'Large candidate library plus original synthetic alarm/hum/static, not a selected prison mix. Original VO, PA lines, convincing bus engine, radio speech and score missing; audition/loop seam tests outstanding.',
'UI_SUBTITLES':'Font, original icons and subtitle panel exist; localized half-screen UI, accessibility layouts and prompt composition not validated.',
'VFX_ALARM':'Steady emissive material and dust process settings load; actual beacon lighting/particle emitter appearance and scene placement untested.'}
for a in old:
    a['phase01_validation_status']=a['validation_status']
    if a['asset_id'] not in bundle:
        a['validation_status']='PARTIALLY_VERIFIED'
        continue
    aid=a['asset_id'];children=[x for x in bundle[aid] if x in lookup]
    a['asset_role']='requirement_bundle';a['child_asset_ids']=children;a['remaining_requirements']=gaps[aid]
    a['validation_status']='PARTIALLY_VERIFIED' if children else 'BLOCKED'
    if aid in ['CHAR_ADRIAN','CHAR_NOAH','CHAR_GUARD','CHAR_INMATE'] and any(lookup[x]['validation_status']=='FAILED' for x in children):a['validation_status']='FAILED'
    if aid=='ANIM_HUMANOID':a['validation_status']='BLOCKED'
    a['download_status']='PARTIALLY_ACQUIRED' if children else 'MISSING'
    a['import_status']='PARTIALLY_VERIFIED' if children else 'BLOCKED'
    a['runtime_file']=None;a['notes']='Aggregate requirement, not a fabricated payload. Follow child_asset_ids for exact files, licenses and scoped results.'
    a['priority']='CRITICAL' if aid.startswith('CHAR_') or aid=='ANIM_HUMANOID' else 'IMPORTANT'
records=old+new
write('asset_library/manifests/assets.json',json.dumps(records,indent=2))
counts=collections.Counter(a['category'] for a in new); statuses=collections.Counter(a['validation_status'] for a in new)
summary={'new_catalog_entries':len(new),'new_category_counts':dict(counts),'all_manifest_records':len(records),'requirement_bundles':len(bundle),'new_overall_statuses':dict(statuses),'godot_resource_tests':len(evidence),'godot_load_verified':sum(x['load']=='VERIFIED' for x in evidence),'source_fragments':sources,'readiness':'BLOCKED: accepted realistic protagonists and retargeted baseline locomotion unavailable','missing_requirements':gaps}
write('asset_library/manifests/phase15/integration_summary.json',json.dumps(summary,indent=2))
write('ASSET_MANIFEST.md','# Asset manifest — Phase 01.5\n\n[Machine-readable authority](asset_library/manifests/assets.json). '+str(len(records))+' records: 28 original entries plus '+str(len(new))+' new catalogue entries. The 22 aggregate requirement bundles are not counted as acquired payloads. Material sets count once; texture channels, original/runtime copies and embedded duplicate character clips do not increase the asset count. Animation library/root-motion editions are source resources, not hundreds of independently accepted actions.\n\nNew catalogue breakdown: '+', '.join(str(v)+' '+k for k,v in sorted(counts.items()))+'. Most entries are sound candidates. The 500–1000 catalogue target is met; critical mission readiness is not.\n\n| Requirement ID | State | Available children | Remaining scope |\n|---|---|---:|---|\n'+'\n'.join('| '+a['asset_id']+' | '+a['validation_status']+' | '+str(len(a['child_asset_ids']))+' | '+a['remaining_requirements']+' |' for a in old if a['asset_id'] in bundle)+'\n\n[Coverage](docs/qa/ASSET_COVERAGE_MATRIX.md) · [recovery report](docs/qa/PHASE_01_5_REPORT.md) · [validation](docs/assets/ASSET_VALIDATION_REPORT.md) · [licenses](docs/assets/ASSET_LICENSES.md). Source fragment snapshots and prior phase manifest are retained in asset_library/manifests/.\n')
write('docs/assets/ASSET_GAPS.md','# Remaining asset gaps — Phase 01.5\n\n**BLOCKED for intended realistic Chapter 1.** Quantity is not readiness. Source geometry and broad sound libraries now support art exploration; accepted realistic protagonists and their baseline movement are still missing. Optional dressing does not block gameplay development.\n\n'+ '\n'.join('- **'+aid+'**: '+gap for aid,gap in gaps.items())+'\n\nThe raw experimental character files are retained for diagnosis, marked FAILED. Do not adopt them because they import. See [coverage matrix](../qa/ASSET_COVERAGE_MATRIX.md) and [individual animation gaps](../qa/ANIMATION_VALIDATION.md). No gameplay was implemented.\n')
write('docs/qa/BLOCKERS.md','# Phase 01.5 blockers and disposition\n\n**Readiness: BLOCKED for intended Chapter 1 implementation using accepted characters.** No critical dependency is silently considered complete. 22 original bundles now have child resources or explicit missing scopes; none is claimed fully resolved.\n\n| Severity | Blocker | Evidence needed |\n|---|---|---|\n| CRITICAL | Both protagonists and usable guard/inmate rigs | Repair or acquire licensed realistic clothed characters; inspect final exported rest and walking/crouching deformation on both leads. Current experimental exports failed visual acceptance. |\n| CRITICAL | Baseline locomotion and rig compatibility | Accepted retarget on both protagonists; correct rest basis, skin weights, foot contacts and transition samples. Raw source UAL clips do not certify MPFB retarget. |\n| CRITICAL for exact authored missions | Key partners and machinery | Mara/Silas matching actors, M02 ball, M05 lifting grille/pump and safe contact geometry must be provided or an approved scope change documented. |\n| IMPORTANT | Realistic architecture / cinematic props | Core static source modules now exist; fitted layout, collision/nav, close-up ledger text, bus, watchtower, cinematic material/face quality remain incomplete. |\n| IMPORTANT | Prison audio and subtitle presentation | Audition/select actual events and ambiences; voice/radio/PA/score missing. Font/style/icons and synthetic sound candidates exist. |\n| OPTIONAL | Decorative variation | Extra crate/stool/tool/UI sounds and alternative surfaces can remain unselected without blocking. |\n\n'+ '\n'.join('- **'+aid+'** — '+gap for aid,gap in gaps.items())+'\n\n[Mission coverage](ASSET_COVERAGE_MATRIX.md), [independent review](PHASE15_INDEPENDENT_REVIEW.md), [recovery report](PHASE_01_5_REPORT.md). Source-only acquisition and engine import PASS do not resolve art/rig/animation criteria. No gameplay, missions or cooperative systems were implemented.\n')
mission_chars={1:['CHAR_ADRIAN','CHAR_NOAH','CHAR_RUSK','CHAR_GUARD','CHAR_INMATE'],2:['CHAR_ADRIAN','CHAR_NOAH','CHAR_SILAS','CHAR_GUARD','CHAR_INMATE'],3:['CHAR_ADRIAN','CHAR_NOAH','CHAR_MARA','CHAR_RUSK','CHAR_GUARD','CHAR_INMATE'],4:['CHAR_ADRIAN','CHAR_NOAH','CHAR_RUSK','CHAR_GUARD'],5:['CHAR_ADRIAN','CHAR_NOAH'],6:['CHAR_ADRIAN','CHAR_NOAH','CHAR_RUSK','CHAR_GUARD']}
mission_env={1:['ENV_INTAKE','ENV_CELLBLOCK'],2:['ENV_YARD'],3:['ENV_WORKSHOP'],4:['ENV_CELLBLOCK','ENV_MAINTENANCE'],5:['ENV_MAINTENANCE'],6:['ENV_MAINTENANCE','ENV_CELLBLOCK']}
mission_props={1:['PROP_PHOTO','PROP_VANTAGE_BADGE'],2:['PROP_PHOTO'],3:['PROP_DIAGRAM','PROP_SHIM'],4:['PROP_SHIM'],5:['PROP_SHIM','PROP_RELAY','PROP_LEDGER'],6:['PROP_PHOTO','PROP_SHIM','PROP_VANTAGE_BADGE','PROP_LEDGER']}
lines=['# Chapter 1 asset coverage matrix — Phase 01.5','', 'Every ID below resolves in [assets.json](../../asset_library/manifests/assets.json). Aggregate records list exact child_asset_ids, paths and remaining scopes. CRITICAL means functional dependency; IMPORTANT means intended production appearance/performance; OPTIONAL means decorative polish. No optional ornament blocks implementation.','']
for i in range(1,7):
    fmt=lambda ids:', '.join('`'+x+'`' for x in ids)
    lines.extend([f'## CH01_M{i:02d}', '', '| Category | Manifest IDs | Priority / actual coverage |','|---|---|---|', '| Players and NPCs | '+fmt(mission_chars[i])+' | CRITICAL: accepted protagonists/retarget unavailable; see character report. |','| Animations | `ANIM_HUMANOID` | CRITICAL: raw licensed source exists; accepted player locomotion/scene contacts do not. |','| Environment modules | '+fmt(mission_env[i])+' | Core source modules partially supplied; complete machinery/layout and collision/nav still need work. |','| Props | '+fmt(mission_props[i])+' | Static authored substitutes available, close-up text and contacts remain IMPORTANT; M05 relay/grille functional geometry is CRITICAL. |','| Materials | `MAT_CONCRETE`, `MAT_METAL` plus `MAT_P15_CONCRETE_BLOCK_WALL`, `MAT_P15_METAL_PLATE` | IMPORTANT: original maps plus19 imported material sets; correct per-object UV scale/art calibration pending. |','| Audio | `AUDIO_FOLEY`, `AUDIO_PRISON`, `AUDIO15_RELAY_CLICK`, `AUDIO15_ALARM_SIREN` | Functional synthetic cues and broad candidates exist; selected/authentic mix and voice remain IMPORTANT. |','| Cinematics / readable presentation | `ANIM_HUMANOID`, `UI_SUBTITLES`, `VFX_ALARM` | Facial acting and authored contacts unaccepted; steady alarm material/font/panel source exists. |','| Optional dressing | `PH15_PLASTIC_CRATE_01`, `PH15_METAL_STOOL_01` | OPTIONAL; never part of critical gate. |','', '**Sufficient for intended implementation: NO**, due to accepted protagonists/locomotion. Source geometry may support a separately authorized proxy blockout; this is not approval to implement gameplay now.',''])
write('docs/qa/ASSET_COVERAGE_MATRIX.md','\n'.join(lines))
print(json.dumps(summary,indent=2))

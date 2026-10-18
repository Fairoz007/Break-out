"""Append/refresh manifest records for the UBC replacement characters (idempotent)."""
import json, hashlib, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[1]; M = R / 'asset_library/manifests'
LIC = R / 'asset_library/licenses/phase15_characters'
src_lic = R / 'asset_library/extracted_sources/phase15_characters/universal-base-characters/Universal Base Characters[Standard]/License_Standard.txt'
shutil.copyfile(src_lic, LIC / 'UBC_License_Standard.txt')
sha = lambda p: hashlib.sha256((R / p).read_bytes()).hexdigest()
anim = json.loads((R / 'asset_library/converted/phase15_characters/ubc/animate_report.json').read_text())
build = json.loads((R / 'asset_library/converted/phase15_characters/ubc/build_report.json').read_text())
rows = [('P15_UBC_ADRIAN', 'adrian_cross', 'CHAR_ADRIAN', 'Adrian Cross playable prototype: orange long-sleeve top, grey trousers, brown work shoes, short dark hair, 1.84 m'),
        ('P15_UBC_NOAH', 'noah_reyes', 'CHAR_NOAH', 'Noah Reyes playable prototype: blue short-sleeve undershirt, orange trousers, dark shoes, black cropped hair, warm brown skin tint, 1.78 m'),
        ('P15_UBC_GUARD', 'prison_guard', 'CHAR_GUARD', 'Generic guard prototype: light-blue shirt, navy trousers, black shoes, 1.82 m; no radio/holster/keys props'),
        ('P15_UBC_INMATE', 'prisoner_npc', 'CHAR_INMATE', 'Generic inmate prototype: orange short-sleeve suit, beard, 1.80 m'),
        ('P15_UBC_RUSK', 'tomas_rusk', 'CHAR_RUSK', 'Tomas Rusk prototype: dark navy guard uniform, receding short hair, 1.83 m; not heavy build, no wedding band/radio/keys'),
        ('P15_UBC_SILAS', 'silas_bell', 'CHAR_SILAS', 'Silas Bell prototype: shaved head, orange prison suit, 1.80 m; no patches/chipped incisor'),
        ('P15_UBC_MARA', 'mara_sen', 'CHAR_MARA', 'Dr Mara Sen prototype: UBC female base, teal scrubs + darker cardigan top, short silver hair, 1.67 m; no badge/lanyard')]
recs = json.loads((M / 'phase15_characters_records.json').read_text(encoding='utf-8-sig'))
recs = [r for r in recs if not r['asset_id'].startswith('P15_UBC_')]
for aid, stem, bundle, desc in rows:
    rf = f'assets/characters/phase15/ubc/{stem}.glb'
    recs.append({
        'asset_id': aid, 'asset_name': stem + ' (UBC replacement)', 'category': 'characters',
        'source_url': 'https://quaternius.itch.io/universal-base-characters', 'creator': 'Quaternius (base body, hair, UAL clips); uniform shell, tints and clip transfer by project',
        'license': 'CC0-1.0 base assets; original modifications', 'attribution_required': False,
        'license_record': 'asset_library/licenses/phase15_characters/UBC_License_Standard.txt',
        'original_file': 'asset_library/original_downloads/phase15_characters/Universal Base Characters[Standard].zip', 'animation_source_files': ['asset_library/original_downloads/phase15_characters/Universal Animation Library[Standard].zip', 'asset_library/original_downloads/phase15_characters/Universal Animation Library 2[Standard].zip'],
        'original_checksum': sha('asset_library/original_downloads/phase15_characters/Universal Base Characters[Standard].zip'),
        'runtime_file': rf, 'runtime_checksum': sha(rf), 'format': 'GLB',
        'polygon_count_if_known': None, 'texture_resolution_if_known': '2048 body/hair, 1024 denim normal',
        'skeleton_type_if_applicable': 'Quaternius UAL 65-joint humanoid (native, same joint names as UAL1/UAL2)',
        'animation_compatibility': f"{len(anim[stem]['clips'])} UAL1/UAL2 clips transferred in glTF space (world-delta rotations, own bone lengths, pelvis/root displacement scaled {anim[stem]['clips'][0]['pelvis_ratio']})",
        'animation_clips': [c['clip'] for c in anim[stem]['clips']],
        'required_by_scene': ['CH01_M01', 'CH01_M02', 'CH01_M03', 'CH01_M04', 'CH01_M05', 'CH01_M06'],
        'download_status': 'CREATED_FROM_LICENSED_SOURCE', 'import_status': 'PENDING_GODOT_CHECK', 'validation_status': 'FUNCTIONAL_PROXY', 'production_ready': False,
        'requirement_bundle': bundle,
        'build': {'script': 'tools/phase15_ubc_build.py', 'animate': 'tools/phase15_ubc_animate.py', 'render': 'tools/phase15_ubc_render.py',
                  'authoring_blend': f'asset_library/converted/phase15_characters/ubc/{stem}.blend', 'scale': build[stem]['scale']},
        'visual_evidence': f'asset_library/manifests/phase15_characters_previews/ubc/sheet_{stem}_front.png',
        'notes': desc + '. Replaces failed MPFB retarget path for prototype gameplay. Re-imported GLB renders (rest + 11 clips, front/side) show intact limbs, visible garments and no observed clipping. '
                 'Not cinematic: stylised muscular base body, skin-tight shell garments with jagged hems, no cloth folds, no facial rig/blendshapes, shared face mesh across all four.'})
(M / 'phase15_characters_records.json').write_text(json.dumps(recs, indent=2))
# Unrecorded earlier build leftovers: move out of runtime (not deleted)
rej = R / 'asset_library/rejected/phase15_characters'; rej.mkdir(parents=True, exist_ok=True); moved = []
for n in ['guard_base.glb', 'inmate_base.glb']:
    p = R / 'assets/characters/phase15' / n
    if p.exists():
        shutil.move(str(p), str(rej / n)); moved.append(n)
        imp = p.with_suffix('.glb.import')
        if imp.exists(): imp.unlink()
if moved:
    (rej / 'REJECTED.json').write_text(json.dumps({'files': moved, 'reason': 'Unreferenced intermediate MPFB build outputs (21:41) with no manifest record; superseded. Moved, not deleted.'}, indent=2))
print(len(recs), 'character records; moved', moved)

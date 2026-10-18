"""Copy accepted Rocketbox evaluation outputs to runtime and write their manifest records (idempotent)."""
import json, hashlib, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[1]; M = R / 'asset_library/manifests'
C = R / 'asset_library/converted/phase15_characters/rocketbox'; RT = R / 'assets/characters/phase15/rocketbox'; RT.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
cfg = json.loads((C / 'avatars.json').read_text()); anim = json.loads((C / 'animated/animate_report.json').read_text())
rows = {'rb_adrian_cross': ('P15_RB_ADRIAN', 'CHAR_ADRIAN', 'Adrian Cross realistic candidate: Rocketbox Male_Adult_02 (lean, dark hair); sweater recoloured orange (overshirt), trousers grey; 1.84 m'),
        'rb_noah_reyes': ('P15_RB_NOAH', 'CHAR_NOAH', 'Noah Reyes realistic candidate: Rocketbox Male_Adult_12 (brown skin, short black hair); denim jacket/tee recoloured blue, jeans recoloured orange; 1.78 m'),
        'rb_silas_bell': ('P15_RB_SILAS', 'CHAR_SILAS', 'Silas Bell realistic candidate: Rocketbox Male_Adult_11 (buzz cut); work shirt and jeans recoloured prison orange; 1.80 m'),
        'rb_prisoner_npc': ('P15_RB_INMATE', 'CHAR_INMATE', 'Inmate realistic candidate: Rocketbox Male_Adult_14 (older, balding); shirt/trousers recoloured prison orange; 1.79 m'),
        'rb_tomas_rusk': ('P15_RB_RUSK', 'CHAR_RUSK', 'Tomas Rusk / guard realistic candidate: Rocketbox Security_Male_01 unmodified security uniform with holster; older grey-haired, average (not heavy) build; 1.83 m'),
        'rb_mara_sen': ('P15_RB_MARA', 'CHAR_MARA', 'Dr Mara Sen realistic candidate: Rocketbox Medical_Female_01 scrubs; younger, dark-haired (likeness mismatch vs 46, silver-streaked); 1.67 m')}
recs = json.loads((M / 'phase15_characters_records.json').read_text(encoding='utf-8-sig'))
recs = [r for r in recs if not r['asset_id'].startswith('P15_RB_')]
for stem, (aid, bundle, desc) in rows.items():
    src = C / 'animated' / (stem + '.glb'); dst = RT / (stem[3:] + '.glb'); shutil.copyfile(src, dst)
    av = cfg[stem]['src']; name = Path(av).name; od = R / 'asset_library/original_downloads/phase15_discovery/microsoft_rocketbox' / av
    recs.append({'asset_id': aid, 'asset_name': stem[3:] + ' (Rocketbox realistic)', 'category': 'characters',
        'source_url': f'https://github.com/microsoft/Microsoft-Rocketbox/tree/master/Assets/Avatars/{av}', 'creator': 'Microsoft Rocketbox (avatar); uniform recolour and UAL clip transfer by project',
        'license': 'MIT (Copyright (c) 2020 Microsoft); notice must ship with the game', 'attribution_required': True,
        'license_record': 'asset_library/licenses/phase15_discovery/microsoft_rocketbox/LICENSE.md',
        'original_file': (od / 'Export' / (name + '.fbx')).relative_to(R).as_posix(), 'original_checksum': sha(od / 'Export' / (name + '.fbx')),
        'facial_source_file': (od / 'Export' / (name + '_facial.fbx')).relative_to(R).as_posix(),
        'texture_overrides': cfg[stem].get('overrides', {}),
        'runtime_file': dst.relative_to(R).as_posix(), 'runtime_checksum': sha(dst), 'format': 'GLB',
        'polygon_count_if_known': None, 'texture_resolution_if_known': '2048 body/head (TGA -> PNG)',
        'skeleton_type_if_applicable': '3ds Max Biped Bip01, 80 joints (28 facial, 30 finger); 176 facial blendshapes available in _facial.fbx but NOT in this runtime file',
        'animation_compatibility': '37 UAL1/UAL2 clips transferred in glTF space via UAL->Biped bone map, A-to-T rest swing alignment and world-delta rotations (tools/phase15_rocketbox_animate.py)',
        'animation_clips': [c['clip'] for c in anim[stem]['clips']],
        'required_by_scene': ['CH01_M01', 'CH01_M02', 'CH01_M03', 'CH01_M04', 'CH01_M05', 'CH01_M06'],
        'download_status': 'CREATED_FROM_LICENSED_SOURCE', 'import_status': 'PENDING_GODOT_CHECK', 'validation_status': 'PARTIALLY_VERIFIED',
        'quality_tier': 'REALISTIC_CANDIDATE', 'production_ready': False, 'requirement_bundle': bundle,
        'build': {'convert': 'tools/phase15_rocketbox_convert.py', 'recolor': 'tools/phase15_rocketbox_recolor.py', 'animate': 'tools/phase15_rocketbox_animate.py', 'render': 'tools/phase15_rocketbox_render.py'},
        'visual_evidence': f'asset_library/manifests/phase15_characters_previews/rocketbox_eval/sheet_{stem}_front.png',
        'notes': desc + '. Re-imported GLB renders (rest + 11 clips, front/side) show realistic body, face, hair cards and clothing with intact deformation. '
                 'Open: facial blendshapes not exported, specular maps replaced by constant roughness, recolour is a texture derivative (no new garment geometry), foot sliding/root motion and Godot close-up lighting unreviewed, no likeness approval by art direction.'})
(M / 'phase15_characters_records.json').write_text(json.dumps(recs, indent=2)); print(len(recs), 'character records')
